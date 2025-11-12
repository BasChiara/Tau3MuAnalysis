#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)

import numpy as np
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as cfg
import models.fit_utils as fit_utils
from plots.color_text import color_text as ct

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   choices=['ABC', 'A', 'B', 'C'],  default = 'ABC', help='which category to select')
parser.add_argument('--year',       choices=['2022', '2023', 'all'], default = 'all', help='which year to select')
parser.add_argument('--bdt_cut',    type= float, default = 0.990)
parser.add_argument('--mu_pair',    choices=['12', '13', '23', 'all'], default = '12')
parser.add_argument('--resonance',  choices=['phi', 'omega'], default = 'phi', help='which resonance to fit')

args = parser.parse_args()
tag = args.tag
name = {'12': 'Mu1Mu2', '23':'Mu2Mu3', '13':'Mu1Mu3', 'all':'MuMu'}


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

initial_width = {
    'phi' : {
        'ABC' : 13.3e-3,
        'A'   : 9.0e-3,
        'B'   : 14.0e-3,
        'C'   : 18.0e-3,
    },
    'omega' : {
        'ABC' : 15.0e-3,
        'A'   : 10.0e-3,
        'B'   : 16.0e-3,
        'C'   : 20.0e-3,
    }
}

# **** USEFUL CONSTANT VARIABLES *** #

# phi
phi_mass = 1.019 #GeV
omega_mass = 0.783 #GeV
rho_mass = 0.770 #GeV
if args.resonance == 'phi':
    fit_range_lo  , fit_range_hi   = 0.90, 1.16 # GeV
    res_mass = phi_mass
elif args.resonance == 'omega':
    fit_range_lo  , fit_range_hi   = 0.70, 0.86 # GeV
    res_mass = omega_mass
binw  = 0.005 if args.resonance == 'phi' else 0.004 # GeV
nbins = int((fit_range_hi - fit_range_lo)/binw) + ( 1 if args.resonance == 'phi' else 0)



### IMPORT DATA ###
input_tree_name = 'tree_w_BDT'
#mc_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2_EFG_MuMuFilter.root'
#data_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2_EFG_MuMuFilter_open.root'
data_file = cfg.data_bdt_samples['WTau3Mu'] if args.mu_pair != 'all' else 'data_mumuOS.root'
base_selection = '&'.join([
    f'(bdt_score>{args.bdt_cut:.3f})',
    cfg.cat_eta_selection_dict_fit[args.category],
    cfg.year_selection[args.year] if args.year != 'all' else '(1)',
    ])
print(f'[+] selection: {base_selection}')
catyyyy = f'{args.category}{args.year}' if args.year != 'all' else f'{args.category}'

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
if data_tree.GetEntries() == 0:
    print(f'{ct.RED}[ERROR]{ct.END} data tree empty!')
    exit()

# open a logger
logger_file = f'{args.plot_outdir}/fit_{args.resonance}To{name[args.mu_pair]}_bdt{args.bdt_cut:.3f}_{catyyyy}.log'
logger = open(logger_file, 'w')
logger.write(f'Fit log for {args.resonance}->mu mu, pair {name[args.mu_pair]}, BDT > {args.bdt_cut:.3f}\n')
logger.write(f'Selection: {base_selection}\n\n')

# ** RooFit Variables ** #
thevars = ROOT.RooArgSet()
# BDT score
bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
thevars.add(bdt)
weight = ROOT.RooRealVar('weight',    'event weight', 0.0, 10.0, '' )
# eta
eta = ROOT.RooRealVar('tau_fit_eta', 'tau eta'  , -5.0,  5.0, '' )
thevars.add(eta)
# year ID
year = ROOT.RooRealVar('year_id', 'year ID'  , 0,  300, '' )
thevars.add(year)
# di-muon mass
if args.mu_pair == 'all':
    ref_var= 'tau_mumuOS_M'
    mass_var = 'tau_mumuOS_fitM'
    mumu_ref  = ROOT.RooRealVar(ref_var,  "m(#mu^{+}#mu^{-})", 0.0, 10.0, 'GeV' )
    mumu_mass = ROOT.RooRealVar(mass_var, "m(#mu^{+}#mu^{-})", fit_range_lo,  fit_range_hi, 'GeV' )

else :
    ref_var= f'tau_mu{args.mu_pair}_M'
    mass_var = f'tau_mu{args.mu_pair}_fitM'
    mumu_ref = ROOT.RooRealVar(ref_var, cfg.features_NbinsXloXhiLabelLog[ref_var][3], 0.0, 10.0, 'GeV' )
    mumu_mass = ROOT.RooRealVar(mass_var, cfg.features_NbinsXloXhiLabelLog[mass_var][3], fit_range_lo,  fit_range_hi, 'GeV' )
    thevars.add(weight)

mumu_mass.setRange('fit_range', fit_range_lo, fit_range_hi)
thevars.add(mumu_ref)
thevars.add(mumu_mass)

# ** IMPORT DATASET ** #
datatofit = ROOT.RooDataSet('data', 'data', data_tree, thevars, base_selection)
datatofit = datatofit.reduce(ROOT.RooArgSet(mumu_mass))
print(f'\n {ct.GREEN}[INFO]{ct.END} dataset to fit, entries = {datatofit.numEntries()}')
datatofit.Print('v')
if datatofit.numEntries() == 0:
    print(f'{ct.RED}[ERROR]{ct.END} dataset to fit empty!')
    logger.write('ERROR: dataset to fit empty!\n')
    logger.close()
    exit()

# PHI -> mumu signal model + bkg
M_mumu   = ROOT.RooRealVar('M_mumu' , 'M_{#mu#mu}' , res_mass, res_mass - 0.002, res_mass + 0.002)
dw = 0.01 if args.bdt_cut > 0.9 else 0.20
width  = ROOT.RooRealVar('width',  'width', 
                            initial_width[args.resonance][args.category],    
                            0.005,#initial_width[args.category]*(1.-dw), 
                            0.100 #initial_width[args.category]*(1.+dw)
                        )
if args.bdt_cut >= 0.899:
    if args.resonance == 'omega': width.setConstant(ROOT.kTRUE)
    M_mumu.setConstant(ROOT.kTRUE)
smodel = ROOT.RooGaussian('signal_mumu', 'signal_mumu', mumu_mass, M_mumu, width)

# COMBINATORIAL BACKGROUND
a0 = ROOT.RooRealVar('a0', 'a0', 0, -1.0,1.0)
a1 = ROOT.RooRealVar('a1', 'a1', 0, -1.0,1.0)
a2 = ROOT.RooRealVar('a2', 'a2', 0, -1.0,1.0)
a3 = ROOT.RooRealVar('a3', 'a3', 0, -1.0,1.0)
#bmodel = ROOT.RooPolynomial('background_phimumu', "background_phimumu", mumu_mass, ROOT.RooArgList(a0, a1), 0)
order =  ROOT.RooArgList(a0, a1, a2, a3) if args.bdt_cut < 0.5 else ROOT.RooArgList(a0, a1)
if args.resonance == 'omega' and args.bdt_cut < 0.5:
    order = ROOT.RooArgList(a0, a1)
bmodel = ROOT.RooChebychev('bmodel', 'bmodel', mumu_mass, order)

nsig = ROOT.RooRealVar('Ns', 'N signal', 0.2*datatofit.sumEntries(), 0., datatofit.sumEntries())
nbkg = ROOT.RooRealVar('Nb', 'N combinatorics', 0.8*datatofit.numEntries(), 0., datatofit.numEntries())
full_model = ROOT.RooAddPdf('full_model', 'full_model', ROOT.RooArgList(smodel,bmodel), ROOT.RooArgList(nsig, nbkg))

# -- FITTING
results = full_model.fitTo(
    datatofit, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
)
mumu_mass.setRange('sig_range', M_mumu.getVal() - 3*width.getVal(), M_mumu.getVal() + 3*width.getVal())
B = nbkg.getVal()*(bmodel.createIntegral(ROOT.RooArgSet(mumu_mass), ROOT.RooArgSet(mumu_mass), 'sig_range').getValV())
significance = nsig.getVal()/((nsig.getVal()+B)**0.5) if (nsig.getVal()+B)>0 else 0

# - summary text
print(f'\n {ct.GREEN}[INFO]{ct.END} fit results:')
print(f'  - signal mean = {M_mumu.getVal():.4f} +/- {M_mumu.getError():.4f} GeV')
print(f'  - signal width = {width.getVal():.4f} +/- {width.getError():.4f} GeV')
print(f'  - N signal = {nsig.getVal():.1f} +/- {nsig.getError():.1f}')
print(f'  - N bkg = {nbkg.getVal():.1f} +/- {nbkg.getError():.1f} ( {B:.1f} in +/- { (nbkg.getError()/nbkg.getVal())*B:.1f} in the signal region )')
print(f'  - significance = {significance:.2f}')
# into logger
logger.write(
'''
    Fit results:
    - signal mean = {:.4f} +/- {:.4f} GeV
    - signal width = {:.4f} +/- {:.4f} GeV
    - N signal = {:.1f} +/- {:.1f}
    - N bkg = {:.1f} +/- {:.1f} ( {:.1f} in +/- {:.1f} in the signal region )
    - significance = {:.2f}
    '''.format(
        M_mumu.getVal(), M_mumu.getError(),
        width.getVal(), width.getError(),
        nsig.getVal(), nsig.getError(),
        nbkg.getVal(), nbkg.getError(), B, (nbkg.getError()/nbkg.getVal())*B,
        significance,
    )
)

# - draw the fit result
frame = mumu_mass.frame()
frame.SetTitle(f'#{args.resonance}#rightarrow#mu#mu')
datatofit.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.),
    ROOT.RooFit.Name('data'),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range'),
    ROOT.RooFit.MoveToBack(),
    ROOT.RooFit.Name('fit')
)
chi2 = frame.chiSquare()
print(f'  - chi2/ndof = {chi2:.2f}\n')
logger.write(f'  - chi2/ndof = {chi2:.2f}\n')

# --- OPTIMIZE THE VETO WINDOW ---
sigma_thresholds = np.linspace(0.5, 5, 10)
print(f'\n {ct.GREEN}[INFO]{ct.END} optimizing veto window:')
logger.write('Veto window optimization:\n')

best_n_sigma = 0.
for n_sigma in sigma_thresholds:
    region_name = f'sig_region_{n_sigma:.1f}sigma'
    mumu_mass.setRange(region_name, M_mumu.getVal() - n_sigma*width.getVal(), M_mumu.getVal() + n_sigma*width.getVal())
    res_signal = nsig.getVal()*(1. - smodel.createIntegral(
        ROOT.RooArgSet(mumu_mass), 
        ROOT.RooArgSet(mumu_mass), 
        region_name
    ).getValV())
    log_string = f' +/- {n_sigma:.1f} sigma: expected signal = {res_signal:.1f} (efficiency = {res_signal/nsig.getVal()*100:.2f} %)\n'
    print(log_string)
    logger.write(log_string)
    # optimal window -> less than 1 expected signal event
    if res_signal < 1.0:
        best_n_sigma = n_sigma
        break


# add line in the veto region
line = ROOT.TLine(M_mumu.getVal() - best_n_sigma*width.getVal(), 0, M_mumu.getVal() - best_n_sigma*width.getVal(), frame.GetMaximum())
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(ROOT.kDashed)
line.SetLineWidth(2)
line2 = ROOT.TLine(M_mumu.getVal() + best_n_sigma*width.getVal(), 0, M_mumu.getVal() + best_n_sigma*width.getVal(), frame.GetMaximum())
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(ROOT.kDashed)
line2.SetLineWidth(2)
frame.addObject(line)
frame.addObject(line2)
# legend
legend = ROOT.TLegend(0.70, 0.70, 0.90, 0.90)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.04)
legend.AddEntry(frame.findObject('data'), 'Data', 'PE')
legend.AddEntry(frame.findObject('fit'),  'Fit', 'L')
frame.addObject(legend)

dY = 0.12*frame.GetMaximum()
frame.SetMaximum(frame.GetMaximum() + 8*dY)
text_X, text_Y = fit_range_lo+2*width.getVal(), frame.GetMaximum() - 2*dY
bdt_text = f'BDT > {args.bdt_cut:.3f}' if args.bdt_cut>0 else 'no BDT selection'
fit_utils.add_summary_text(frame, text = bdt_text, x=text_X, y=text_Y+dY, size=0.04)
fit_utils.add_summary_text(frame, text = f'#sigma = ({width.getVal()*1000:.1f} #pm {width.getError()*1000:.1f}) MeV', x=text_X, y=text_Y-dY, size=0.04)
fit_utils.add_summary_text(frame, text = f'#chi^{{2}}/nDoF = {frame.chiSquare():.2f}', x=text_X, y=text_Y-2*dY, size=0.04)
fit_utils.add_summary_text(frame, text = f'S/#sqrt{{B}} = {significance:.1f}', x=text_X, y=text_Y-3*dY, size=0.04)
fit_utils.draw_fit_pull(frame, fitvar=mumu_mass, out_name = f'{args.plot_outdir}/{args.resonance}To{name[args.mu_pair]}_mass_bdt{args.bdt_cut:.3f}_{catyyyy}')

logger.close()