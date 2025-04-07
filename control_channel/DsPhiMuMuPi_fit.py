#############################################
#  fit Ds -> Phi(MuMu)Pi signal and bkg   #
#############################################

import ROOT

import numpy as np
import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import mva.config as config
from   plots.color_text import color_text as ct
import models.fit_utils as fitu


category_list = ['A', 'B', 'C', 'ABC']


parser = argparse.ArgumentParser()
parser.add_argument('--peak_bkg',  
                    action='store_true',                        
                    help='activate it when running on 3 muons')
parser.add_argument('-s','--signal',                                            
                    help='signal MC file')
parser.add_argument('-d','--data',                                              
                    help='data file')
parser.add_argument('--plot_outdir',
                    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', 
                    help=' output directory for plots')
parser.add_argument('--tag',        
                    default= 'reMini',                          
                    help='tag to the training')
parser.add_argument('--debug',      
                    action = 'store_true' ,                     
                    help='set it to have useful printout')
parser.add_argument('--category',   
                    choices=category_list,   
                    default = 'ABC',
                    help='category to be used')
parser.add_argument('-y','--year',       
                    choices=list(config.year_selection.keys()), 
                    default = '2022', help='year of data-taking')
parser.add_argument('--bdt_cut',    
                    default = -1.0, type=float,                
                    help='BDT cut value')

args = parser.parse_args()
tag = f'cat{args.category}{args.year}' + (f'_bdt{args.bdt_cut:,.2f}' if args.bdt_cut > 0. else '') + f'_{args.tag}'

# *** ROOT STYLES *** #
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** CONSTANT VARIABLES **** #
fit_range_lo = config.Ds_mass_range_lo if not args.peak_bkg else config.peakB_mass_lo
fit_range_hi = config.Ds_mass_range_hi if not args.peak_bkg else config.peakB_mass_hi
binwidth = 0.01 
nbins = int((fit_range_hi-fit_range_lo)/binwidth) + 1


# *** INPUT DATA AND MONTE CARLO ***
input_tree_name = 'tree_w_BDT'
if not args.signal: mc_file   = [config.mc_bdt_samples['DsPhiMuMuPi']]
else : mc_file     = [args.signal]
if not args.data: data_file   = [config.data_bdt_samples['DsPhiMuMuPi']]
else : data_file   = [args.data]
# *** OUTPUT FILE *** #
f_out_name = "workspaces/DsPhiPi_wspace_%s.root"%(tag)
f_out = ROOT.TFile(f_out_name, "RECREATE")

# ** RooFit Variables
# Ds mass
mass = ROOT.RooRealVar('Ds_fit_mass', '#mu#mu #pi mass'  , config.Ds_mass_range_lo,  config.Ds_mass_range_hi, 'GeV' )
if args.peak_bkg:
    mass = ROOT.RooRealVar('tau_MuMuPi_mass', '#mu#mu #pi mass'  , config.peakB_mass_lo,  config.peakB_mass_hi, 'GeV' )
mass.setRange('fit_range', fit_range_lo, fit_range_hi)
#mass.setRange('full_range', config.Ds_mass_range_lo, config.Ds_mass_range_lo)

weight   = ROOT.RooRealVar('weight', 'weight'  , -np.inf,  np.inf, '')
year_id  = ROOT.RooRealVar('year_id', 'year_id'  , 210,  270, '')
eta      = ROOT.RooRealVar('Ds_fit_eta' if not args.peak_bkg else 'tau_fit_eta', '#eta_{#mu#mu#pi}'  , -4.0,  4.0)
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 0.0,  np.inf)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.0,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass' if not args.peak_bkg else 'tau_phiMuMu_mass', ''  , 0.5,  2.0, 'GeV')
bdt_score= ROOT.RooRealVar('bdt_score', 'bdt_score', 0.0, 1.0)

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(weight)
thevars.add(year_id)
thevars.add(eta)
thevars.add(dspl_sig)
thevars.add(sv_prob)
thevars.add(phi_mass)
thevars.add(bdt_score)

# --- common selection --- #
base_selection = '(' + ' & '.join([
    config.year_selection[args.year],
    config.Ds_base_selection,
    config.Ds_phi_selection,
    config.Tau_sv_selection,
    config.Ds_category_selection[args.category],
]) + ')'
if args.peak_bkg:
    base_selection = '(' + ' & '.join([
        config.year_selection[args.year],
        config.peakB_base_selection,
        config.peakB_phi_selection,
        config.peakB_sv_selection,
    ]) + ')'
if args.bdt_cut > 0.:
    base_selection += ' & (bdt_score > %.2f)'%args.bdt_cut


### MC SIGNAL - FIT ###
print(f'{ct.RED}[+] MC DATASET  {ct.END}')
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
#N_mc = mc_tree.GetEntries(base_selection)
#fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection, 'weight')
fullmc, sig_efficiency, N_mc = fitu.import_data_from_tree(
    mc_tree,
    thevars,
    dataset_name='mc_DsPhiMuMuPi',
    full_cut=base_selection,
    weight = 'weight',
    verbose = True,
)
if args.peak_bkg: fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection) # no weight for peak bkg
fullmc.Print()
#sig_efficiency = fullmc.sumEntries()/N_mc/fullmc.weight()

# signal PDF : resonance + combinatorics
Mass      = ROOT.RooRealVar('Ds_Mmc' , 'Ds_Mmc' , config.Ds_mass)
dMass_mc  = ROOT.RooRealVar('dM_mc', 'dM_mc', 0, -0.1, 0.1)
mean_mc   = ROOT.RooFormulaVar('mean_mc','mean_mc', '(@0+@1)', ROOT.RooArgList(Mass,dMass_mc) )

width_mc  = ROOT.RooRealVar('width_mc',   'width_mc',  0.01,    0.001, 0.1)
width1_mc = ROOT.RooRealVar('width1_mc',  'width1_mc', 0.05,    0.001, 0.1)
width2_mc = ROOT.RooRealVar('width2_mc',  'width2_mc', 0.01,    0.001, 0.1)

alphaCB_mc  = ROOT.RooRealVar("alphaCB_mc", "alphaCB_mc", 4.0, 1., 20.)
nCB_mc      = ROOT.RooRealVar('nCB_mc', 'nCB_mc', 50.0, 10. ,100.0)

gfrac       = ROOT.RooRealVar("gfrac", "", 0.2, 0.0, 1.0)
gaus1_mc    = ROOT.RooGaussian('gaus1_mc', 'gaus1', mass, mean_mc, width1_mc)
gaus2_mc    = ROOT.RooGaussian('gaus2_mc', 'gaus2', mass, mean_mc, width2_mc)
gsum_mc     = ROOT.RooAddModel('gsum_mc', '', [gaus1_mc, gaus2_mc], [gfrac]) if not args.peak_bkg else gaus1_mc 

gaus_mc     = ROOT.RooGaussian('gaus_mc',  'gaus',  mass, mean_mc, width_mc)

CryBall_mc  = ROOT.RooCBShape('CryBall_mc', 'CryBall_mc', mass, mean_mc, width_mc, alphaCB_mc, nCB_mc)
nMC = ROOT.RooRealVar('nMC', 'model_DsPhiMuMuPi_norm', fullmc.sumEntries(), 0.001*fullmc.sumEntries(), 3*fullmc.sumEntries())

# MC cobinatorial PDF
alpha = ROOT.RooRealVar("alpha", "", -1.0, -10, 10)
expo  = ROOT.RooExponential('expo_bkg', 'expo_bkg', mass, alpha)
poly  = ROOT.RooPolynomial('flat_bkg', "flat_bkg", mass, ROOT.RooArgList())
nCombMC = ROOT.RooRealVar('nCombMC', 'background', 0.5*fullmc.sumEntries(), 0., fullmc.sumEntries())

# signal + combinatorial
signal_model = ROOT.RooAddPdf("extMCmodel_DsPhiMuMuPi", "extMCmodel_DsPhiMuMuPi", ROOT.RooArgList(CryBall_mc,expo), ROOT.RooArgList(nMC,nCombMC))
# signal fit
results_gaus = signal_model.fitTo(
    fullmc, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
)

# * draw & save
frame = mass.frame(Title='D_{s} -> #phi(1020)#pi signal') 

fullmc.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
)
if results_gaus.status() > 1:
    print(f'{ct.RED}[-] fit failed: status {results_gaus.status()}{ct.END}')
else :
    signal_model.paramOn(
        frame,
        ROOT.RooFit.Layout(0.2, 0.50, 0.85),
        ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
    )
    frame.getAttText().SetTextSize(0.03)
    sig_curve = signal_model.plotOn(
        frame,
        ROOT.RooFit.MoveToBack(),
    )
    fitu.draw_fit_pull(
        frame, 
        fitvar = mass, 
        out_name = '%s/mcDsPhiPi_mass_%s'%(args.plot_outdir, tag), 
        logy = True
    )
    print('signal chi2 %.2f'%(frame.chiSquare(4)))
    
if (args.peak_bkg): exit()

# save workspace
f_out.cd()

width1_mc.setConstant(True)
width2_mc.setConstant(True)
gfrac.setConstant(True)
dMass_mc.setConstant(True)
wspace_mc = ROOT.RooWorkspace("DsPhiPi_mc_wspace", "DsPhiPi_mc_wspace")
try:
    getattr(wspace_mc, 'import')(signal_model)
    print("signal_model imported successfully.")
    wspace_mc.Print()
except Exception as e:
    print("Error importing signal_model:", e)

wspace_mc.Write()

#### DATA ####
print(f'{ct.BLUE}[+] DATA DATASET  {ct.END}')
data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]
N_data = data_tree.GetEntries(base_selection) 

#datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection, 'weight')
datatofit, bkg_efficiency, N_data = fitu.import_data_from_tree(
    data_tree,
    thevars,
    dataset_name='data_fit',
    full_cut=base_selection,
    weight = 'weight',
    verbose = True,
)

# Ds -> phi pi signal 
width  = ROOT.RooRealVar('width',   'width',  width_mc.getVal(), 0.001, 0.05)
alphaCB_mc.setConstant()
nCB_mc.setConstant()

width1 = ROOT.RooRealVar('width1',  'width1', width1_mc.getVal(), 0.001, 0.05)
width2 = ROOT.RooRealVar('width2',  'width2', width2_mc.getVal(), 0.001, width1_mc.getVal())
dMass  = ROOT.RooRealVar('dM', 'dM', dMass_mc.getVal(), -0.1, 0.1)

mean   = ROOT.RooFormulaVar('mean_mc','mean_mc', '(@0+@1)', ROOT.RooArgList(Mass,dMass) )

gfrac.setConstant()
gaus1_data  = ROOT.RooGaussian('gaus1_data', 'gaus1_data', mass, mean, width1)
gaus2_data  = ROOT.RooGaussian('gaus2_data', 'gaus2_data', mass, mean, width2)
# fix signal shape for peak bkg
#if args.peak_bkg:
    #width1.setConstant(True)
    #dMass.setConstant(True)
gaus_data   = ROOT.RooGaussian('gaus_data',  'gaus_data',  mass, mean, width1)
CryBall_data = ROOT.RooCBShape('CryBall_data', 'CryBall_data', mass, mean, width, alphaCB_mc, nCB_mc)

#if args.peak_bkg: dMass.setConstant()
#gsum_data   = ROOT.RooAddModel("gsum_data", "", [gaus1_data, gaus2_data], [gfrac]) if not args.peak_bkg else gaus1_data
#Ds_model = ROOT.RooGaussian('Ds_model', 'Ds_model', mass, mean, width1)
Ds_model = CryBall_data
# background PDF
# + D+ -> phi pi
massDp   = ROOT.RooRealVar('massDp' , 'mass_Dp' , config.D_mass)
massDp.setConstant(True)
widthDp  = ROOT.RooRealVar('widthDp' , 'width_Dp' , 0.02, 0.01, 0.05)
gaus_Dp  = ROOT.RooGaussian('gaus_Dp', '', mass, massDp, widthDp)

# + falling expo
a  = ROOT.RooRealVar("a", "",  -1.0, -10, 10)
comb_bkg = ROOT.RooExponential('model_bkg_Ds', 'model_bkg_Ds', mass, a)

# + polynomial background
p1  = ROOT.RooRealVar("p1", "p1", -0.1, -1., -0.0001)
poly = ROOT.RooPolynomial('poly', 'poly', mass, ROOT.RooArgList(p1))

bkg_model = comb_bkg

# D+ fraction
Dp_f     = ROOT.RooRealVar("Dp_f", "", 0.0001, 0.005, 0.5)
# no D+ in category C
if (args.category == 'C' and args.bdt_cut > 0.9):
    Dp_f.setVal(0.0)
    Dp_f.setConstant(True)

nDs = ROOT.RooRealVar('nDs', 'Ds yield', 0.01*datatofit.numEntries(), 0.001*datatofit.numEntries(), 0.5*datatofit.numEntries())
nDp = ROOT.RooRealVar('nDp', 'D+ yield', 0.01*datatofit.numEntries(), 0.001*datatofit.numEntries(), 0.5*datatofit.numEntries())
nB  = ROOT.RooRealVar('nB',  'background yield', 0.5*datatofit.numEntries(), 0., 2*datatofit.numEntries())

if args.peak_bkg: # no D+ in peak bkg
    full_model = ROOT.RooAddPdf("extDATAmodel_DsPhiMuMuPi", "extDATAmodel_DsPhiMuMuPi", ROOT.RooArgList(Ds_model, bkg_model), ROOT.RooArgList(nDs, nB))
else:
    full_model = ROOT.RooAddPdf("extDATAmodel_DsPhiMuMuPi", "extDATAmodel_DsPhiMuMuPi", ROOT.RooArgList(Ds_model, gaus_Dp, bkg_model), ROOT.RooArgList(nDs, nDp, nB))

frame_b = mass.frame(Title=" ")

datatofit.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)

# fit background with exponential model
results = full_model.fitTo(datatofit, ROOT.RooFit.Range('fit_range'), ROOT.RooFit.Save())
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components(Ds_model.GetName()),
    ROOT.RooFit.LineColor(ROOT.kRed),
)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components(gaus_Dp.GetName()),
    ROOT.RooFit.LineColor(ROOT.kOrange),
    )
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components(bkg_model.GetName()),
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
    )
text_NDs = ROOT.TText(fit_range_lo + 0.02, 0.90*frame_b.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(fit_range_lo + 0.02, 0.85*frame_b.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nDp.getValV(), nDp.getError()))
text_Nb  = ROOT.TText(fit_range_lo + 0.02, 0.80*frame_b.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV(), nB.getError()))
text_NDs.SetTextSize(0.035)
text_NDp.SetTextSize(0.035)
text_Nb.SetTextSize(0.035)
frame_b.addObject(text_NDs)
if not args.peak_bkg: frame_b.addObject(text_NDp)
frame_b.addObject(text_Nb)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    #ROOT.RooFit.MoveToBack(),
)
fitu.draw_fit_pull(
    frame_b,
    fitvar = mass,
    out_name = '%s/DsPhiPi_mass_%s'%(args.plot_outdir, tag),
    logy = True
)

print(f'\n\n {ct.BOLD} ------------ SUMMARY ------------{ct.END}')
print('base_selection    = \n %s'%base_selection)
print('[MC] entries(w)   =  %.2f'%fullmc.sumEntries())
print('nDs in MC         = %.2f +/- %.2f'%(nMC.getValV(), nMC.getError()))
print('[DATA] exp-events = %.2f'%full_model.expectedEvents(ROOT.RooArgSet(mass)))
print(' nDs in data       = %.2f +/- %.2f'%(nDs.getValV(), nDs.getError()))
print(f'{ct.BOLD} --------------------------------------{ct.END}\n\n')


# *** SAVE WORKSPACE ***
f_out.cd()
wspace_data = ROOT.RooWorkspace("DsPhiPi_data_wspace", "DsPhiPi_data_wspace")
try:
    getattr(wspace_data, 'import')(full_model)
    print("full_model imported successfully.")
    #wspace_data.Print()
except Exception as e:
    print("Error importing full_model:", e)

#wspace_mc.Write()
wspace_data.Write()
f_out.Close()
print(f'{ct.BOLD} [+] saved workspace in {f_out_name}{ct.END}')
