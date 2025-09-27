#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)

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
parser.add_argument('--category',   default = 'noCat')
parser.add_argument('--bdt_cut',    type= float, default = 0.990)
parser.add_argument('--mu_pair',    default = '12')
parser.add_argument('--resonance',  choices=['phi', 'omega'], default = 'phi', help='which resonance to fit')

args = parser.parse_args()
tag = args.tag
name = {'12': 'Mu1Mu2', '23':'Mu2Mu3', '13':'Mu1Mu3'}


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #

# phi
phi_mass = 1.019 #GeV
omega_mass = 0.783 #GeV
rho_mass = 0.770 #GeV
if args.resonance == 'phi':
    fit_range_lo  , fit_range_hi   = 0.90, 1.20 # GeV
    res_mass = phi_mass
elif args.resonance == 'omega':
    fit_range_lo  , fit_range_hi   = 0.70, 0.85 # GeV
    res_mass = omega_mass
binw  = 0.005 # GeV
nbins = int((fit_range_hi - fit_range_lo)/binw)



input_tree_name = 'tree_w_BDT'
#mc_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2_EFG_MuMuFilter.root'
#data_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2_EFG_MuMuFilter_open.root'
mc_file = cfg.mc_bdt_samples['WTau3Mu'] 
data_file = cfg.data_bdt_samples['WTau3Mu']


# ** RooFit Variables
# BDT score
bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.0,  1.0, '' )
# di-muon mass
mass_var = f'tau_mu{args.mu_pair}_fitM'
mumu_mass = ROOT.RooRealVar(mass_var, cfg.features_NbinsXloXhiLabelLog[mass_var][3], fit_range_lo,  fit_range_hi, 'GeV' )
mumu_mass.setRange('fit_range', fit_range_lo, fit_range_hi)

thevars = ROOT.RooArgSet()
thevars.add(bdt)
thevars.add(weight)
thevars.add(mumu_mass)

### IMPORT DATA ###
base_selection = f'(bdt_score>{args.bdt_cut:.3f})'

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
if data_tree.GetEntries() == 0:
    print(f'{ct.RED}[ERROR]{ct.END} data tree empty!')
    exit()
datatofit = ROOT.RooDataSet('data', 'data', data_tree, thevars, base_selection)
datatofit = datatofit.reduce(ROOT.RooArgSet(mumu_mass))
datatofit.Print('v')

# PHI -> mumu signal model + bkg

M_mumu   = ROOT.RooRealVar('M_mumu' , 'M_{#mu#mu}' , res_mass, res_mass - 0.010, res_mass + 0.010)
width  = ROOT.RooRealVar('width',  'width', 0.01,    0.005, 0.05 if args.resonance=='phi' else 0.10) #GeV
if args.bdt_cut >= 0.980:
    width.setConstant(ROOT.kTRUE)
    M_mumu.setConstant(ROOT.kTRUE)
smodel = ROOT.RooGaussian('signal_mumu', 'signal_mumu', mumu_mass, M_mumu, width)

# COMBINATORIAL BACKGROUND
a0 = ROOT.RooRealVar('a0', 'a0', 0, -1.0,1.0)
a1 = ROOT.RooRealVar('a1', 'a1', 0, -1.0,1.0)
a2 = ROOT.RooRealVar('a2', 'a2', 0, -1.0,1.0)
a3 = ROOT.RooRealVar('a3', 'a3', 0, -1.0,1.0)
#bmodel = ROOT.RooPolynomial('background_phimumu', "background_phimumu", mumu_mass, ROOT.RooArgList(a0, a1), 0)
order =  ROOT.RooArgList(a0, a1, a2) if args.bdt_cut < 0.5 else ROOT.RooArgList(a0)
bmodel = ROOT.RooChebychev('bmodel', 'bmodel', mumu_mass, order)

nsig = ROOT.RooRealVar('Ns', 'N signal', datatofit.sumEntries(), 0., 3*datatofit.sumEntries())
nbkg = ROOT.RooRealVar('Nb', 'N combinatorics', datatofit.numEntries(), 0., 3*datatofit.numEntries())
full_model = ROOT.RooAddPdf('full_model', 'full_model', ROOT.RooArgList(smodel,bmodel), ROOT.RooArgList(nsig, nbkg))

results = full_model.fitTo(
    datatofit, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
)

# * draw & save
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
    ROOT.RooFit.NormRange('fit_range')
)
print('chi2 %.2f'%(frame.chiSquare()))
fit_utils.add_summary_text(frame, text = f'#sigma = ({width.getVal()*1000:.1f} #pm {width.getError()*1000:.1f}) MeV', x=fit_range_lo+0.010, y=0.20*frame.GetMaximum(), size=0.04)
fit_utils.add_summary_text(frame, text = f'#chi^{{2}}/nDoF = {frame.chiSquare():.2f}', x=fit_range_lo+0.010, y=0.20*frame.GetMaximum()-500, size=0.04)

fit_utils.draw_fit_pull(frame, fitvar=mumu_mass, out_name = f'{args.plot_outdir}/{args.resonance}To{name[args.mu_pair]}_mass_bdt{args.bdt_cut:.3f}_{args.category}')