#############################################
#  fit Ds -> Phi(MuMu)Pi signal and bkg   #
#############################################

import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import math
import argparse
import sys
sys.path.append('..')
import mva.config as config


category_list = ['A', 'B', 'C', 'ABC']


parser = argparse.ArgumentParser()
parser.add_argument('--fake_cand',  action='store_true',                        help='activate it when running on 3 muons')
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'reMini',                          help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,                     help='set it to have useful printout')
parser.add_argument('--category',   choices=category_list,   default = 'ABC',help='category to be used')
parser.add_argument('--year',       choices=['2022', '2023'], default = '2022', help='year of data-taking')
parser.add_argument('--bdt_cut',    default = -1.0, type=float,                help='BDT cut value')

args = parser.parse_args()
tag = f'cat{args.category}' + (f'_bdt{args.bdt_cut:,.2f}' if args.bdt_cut > 0. else '') + f'_{args.tag}'

# *** ROOT STYLES *** #
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** CONSTANT VARIABLES **** #
fit_range_lo = config.Ds_mass_range_lo
fit_range_hi = config.Ds_mass_range_hi
nbins = 40 if not args.fake_cand else 25 # needed just for plotting, fits are all unbinned


# *** INPUT DATA AND MONTE CARLO ***
#input_tree_name = 'DsPhiMuMuPi_tree' if not args.fake_cand else 'WTau3Mu_tree'
input_tree_name = 'tree_w_BDT'
mc_file     = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]
data_file   = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_DATA_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]
# *** OUTPUT FILE *** #
f_out_name = "DsPhiPi2022_wspace_%s.root"%(tag)
f_out = ROOT.TFile(f_out_name, "RECREATE")

# ** RooFit Variables
# Ds mass
mass = ROOT.RooRealVar('Ds_fit_mass' if not args.fake_cand else 'tau_MuMuPi_mass', '#mu#mu #pi mass'  , config.Ds_mass_range_lo,  config.Ds_mass_range_hi, 'GeV' )
mass.setRange('fit_range', fit_range_lo, fit_range_hi)
mass.setRange('full_range', config.Ds_mass_range_lo, config.Ds_mass_range_lo)

weight   = ROOT.RooRealVar('weight', 'weight'  , -1000,  1000, '')
year_id  = ROOT.RooRealVar('year_id', 'year_id'  , 210,  270, '')
mass_err = ROOT.RooRealVar('tau_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
eta      = ROOT.RooRealVar('Ds_fit_eta', '#eta_{#mu#mu#pi}'  , -4.0,  4.0)
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 0.0,  1000)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.0,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass' if not args.fake_cand else 'tau_phiMuMu_mass', ''  , 0.5,  2.0, 'GeV')
bdt_score= ROOT.RooRealVar('bdt_score', 'bdt_score', args.bdt_cut, 1.0)

thevars = ROOT.RooArgSet()
thevars.add(mass)
#thevars.add(mass_err)
thevars.add(weight)
thevars.add(year_id)
thevars.add(eta)
thevars.add(dspl_sig)
thevars.add(sv_prob)
thevars.add(phi_mass)
thevars.add(bdt_score)

### MC SIGNAL - FIT ###
base_selection = '(' + ' & '.join([
    config.year_selection[args.year],
    config.Ds_base_selection,
    config.Ds_phi_selection,
    config.Tau_sv_selection,
    config.Ds_category_selection[args.category],
]) + ')'
if args.bdt_cut > 0.:
    base_selection += ' & (bdt_score > %.2f)'%args.bdt_cut
print('[i] base_selection = %s'%base_selection)

mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
N_mc = mc_tree.GetEntries(base_selection)

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection, 'weight')
fullmc.Print()
print('entries = %.2f'%fullmc.sumEntries() )
print('weight  = %e'%fullmc.weight() )
sig_efficiency = fullmc.sumEntries()/N_mc/fullmc.weight()

# signal PDF : double gaussian + constant
Mass   = ROOT.RooRealVar('Ds_Mmc' , 'Ds_Mmc' , config.Ds_mass, 1.7, 1.9)
Mass.setConstant(True)
dMass_mc  = ROOT.RooRealVar('dM_mc', 'dM_mc', 0, -0.1, 0.1)
mean_mc   = ROOT.RooFormulaVar('mean_mc','mean_mc', '(@0+@1)', ROOT.RooArgList(Mass,dMass_mc) )
width1_mc = ROOT.RooRealVar('width1_mc',  'width1_mc', 0.05,    0.001, 0.1)
width2_mc = ROOT.RooRealVar('width2_mc',  'width2_mc', 0.01,    0.001, 0.1)


gfrac       = ROOT.RooRealVar("gfrac", "", 0.2, 0.0, 1.0)
# single gaussian for cat C
if (args.category == 'C' and args.bdt_cut > 0.9):
    gfrac.setVal(0.0)
    gfrac.setConstant(True)
    width1_mc.setVal(0.01)
    width1_mc.setConstant(True)
gaus1_mc    = ROOT.RooGaussian('gaus1_mc', 'gaus1', mass, mean_mc, width1_mc)
gaus2_mc    = ROOT.RooGaussian('gaus2_mc', 'gaus2', mass, mean_mc, width2_mc)
gsum_mc     = ROOT.RooAddModel('gsum_mc', "", [gaus1_mc, gaus2_mc], [gfrac])

nMC = ROOT.RooRealVar('nMC', 'model_DsPhiMuMuPi_norm', fullmc.sumEntries(), 0.5*fullmc.sumEntries(), 3*fullmc.sumEntries())
# MC cobinatorial PDF
poly = ROOT.RooPolynomial('flat_bkg', "flat_bkg", mass, ROOT.RooArgList())
nBflat = ROOT.RooRealVar('nBflat', 'background', 0.5*fullmc.sumEntries(), 0., fullmc.sumEntries())

# signal + combinatorial
signal_model = ROOT.RooAddPdf("extMCmodel_DsPhiMuMuPi", "extMCmodel_DsPhiMuMuPi", ROOT.RooArgList(gsum_mc,poly), ROOT.RooArgList(nMC,nBflat))

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

sig_curve = signal_model.plotOn(
    frame,
    ROOT.RooFit.MoveToBack(),
)
print('signal chi2 %.2f'%(frame.chiSquare(4)))
signal_model.paramOn(
    frame,
    ROOT.RooFit.Layout(0.2, 0.50, 0.85),
    ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
)
frame.getAttText().SetTextSize(0.03)

c = ROOT.TCanvas("c", "c", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
c.SaveAs('%s/mcDsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/mcDsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag)) 
c.SetLogy(1)
c.SaveAs('%s/mcDsPhiPi_mass_Log_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/mcDsPhiPi_mass_Log_%s.pdf'%(args.plot_outdir, tag)) 
if (args.fake_cand): exit(-1)

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

data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]
N_data = data_tree.GetEntries(base_selection) 

datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection, 'weight')
datatofit.Print()
bkg_efficiency = datatofit.sumEntries()/N_data

# Ds -> phi pi signal 
width1 = ROOT.RooRealVar('width1',  'width1', width1_mc.getVal())
width2 = ROOT.RooRealVar('width2',  'width2', width2_mc.getVal())
dMass  = ROOT.RooRealVar('dM', 'dM', dMass_mc.getVal(), -0.1, 0.1)
mean   = ROOT.RooFormulaVar('mean_mc','mean_mc', '(@0+@1)', ROOT.RooArgList(Mass,dMass) )

gfrac.setConstant()
gaus1_data  = ROOT.RooGaussian('gaus1_data', 'gaus1_data', mass, mean, width1)
gaus2_data  = ROOT.RooGaussian('gaus2_data', 'gaus2_data', mass, mean, width2)
gsum_data   = ROOT.RooAddModel("gsum_data", "", [gaus1_data, gaus2_data], [gfrac])

# background PDF
# + D+ -> phi pi
massDp   = ROOT.RooRealVar('massDp' , 'mass_Dp' , config.D_mass)
massDp.setConstant(True)
widthDp  = ROOT.RooRealVar('widthDp' , 'width_Dp' , 0.02, 0.01, 0.05)
gaus_Dp  = ROOT.RooGaussian('gaus_Dp', '', mass, massDp, widthDp)
# + falling expo
a  = ROOT.RooRealVar("a", "",  -1.0, -5, -0.1)
comb_bkg = ROOT.RooExponential('model_bkg_Ds', 'model_bkg_Ds', mass, a)

# + polynomial background
p1  = ROOT.RooRealVar("p1", "p1", -0.1, -1., 1.)
poly = ROOT.RooPolynomial('poly', 'poly', mass, ROOT.RooArgList(p1))

# D+ fraction
Dp_f     = ROOT.RooRealVar("Dp_f", "", 0.0001, 0.005, 0.5)
# no D+ in category C
if (args.category == 'C' and args.bdt_cut > 0.9):
    Dp_f.setVal(0.0)
    Dp_f.setConstant(True)
full_bkg = ROOT.RooAddModel("full_bkg", "", [gaus_Dp, poly], [Dp_f])

nDs = ROOT.RooRealVar('nDs', 'Ds yield', 0.01*datatofit.numEntries(), 0.001*datatofit.numEntries(), 0.5*datatofit.numEntries())
nB  = ROOT.RooRealVar('nB',  'background yield', 0.5*datatofit.numEntries(), 0., datatofit.numEntries())
full_model = ROOT.RooAddPdf("extDATAmodel_DsPhiMuMuPi", "extDATAmodel_DsPhiMuMuPi", ROOT.RooArgList(full_bkg,gsum_data), ROOT.RooArgList(nB,nDs))

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
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.MoveToBack(),
)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components('gsum_data'),
    ROOT.RooFit.LineColor(ROOT.kRed),
    #ROOT.RooFit.Range('full_range'),
    #ROOT.RooFit.NormRange('full_range')
)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components('gaus_Dp'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
    #ROOT.RooFit.Range('full_range'),
    #ROOT.RooFit.NormRange('full_range')
)
text_NDs = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.90*frame_b.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.85*frame_b.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nB.getValV() * (Dp_f.getValV()), nB.getError()))
text_Nb  = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.80*frame_b.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV() * (1-Dp_f.getValV()), nB.getError()))
text_NDs.SetTextSize(0.035)
text_NDp.SetTextSize(0.035)
text_Nb.SetTextSize(0.035)
frame_b.addObject(text_NDs)
frame_b.addObject(text_NDp)
frame_b.addObject(text_Nb)

c2 = ROOT.TCanvas("c2", "c2", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_b.Draw()
c2.SaveAs('%s/DsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c2.SaveAs('%s/DsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag)) 
c2.SetLogy(1)
c2.SaveAs('%s/DsPhiPi_mass_log_%s.png'%(args.plot_outdir, tag)) 
c2.SaveAs('%s/DsPhiPi_mass_log_%s.pdf'%(args.plot_outdir, tag)) 
print(' -- RooExtendPdf = %.2f'%full_model.expectedEvents(ROOT.RooArgSet(mass)))
print(' -- BaseSelection %s'%base_selection)
print(' == S efficiency %.2f '%sig_efficiency)
print(' == B efficiency %.2e '%bkg_efficiency)


# *** SAVE WORKSPACE ***
f_out.cd()
wspace_data = ROOT.RooWorkspace("DsPhiPi_data_wspace", "DsPhiPi_data_wspace")
try:
    getattr(wspace_data, 'import')(full_model)
    print("full_model imported successfully.")
    wspace_data.Print()
except Exception as e:
    print("Error importing full_model:", e)

#wspace_mc.Write()
wspace_data.Write()
f_out.Close()
print(' -- saved workspace in %s'%f_out_name)
