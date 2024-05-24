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

parser = argparse.ArgumentParser()
parser.add_argument('--fake_cand',  action='store_true', help='activate it when running on 3 muons')
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'reMini', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')

args = parser.parse_args()
tag = args.tag 


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
mass_window = 0.060 # GeV
Ds_mass = 1.9678 # GeV
D_mass  = 1.8693 # GeV
fit_range_lo  , fit_range_hi   = 1.70, 2.10 # GeV
mass_window_lo, mass_window_hi = 1.70, 2.10 # GeV #Ds_mass-mass_window, Ds_mass+mass_window

nbins = 40 if not args.fake_cand else 25 # needed just for plotting, fits are all unbinned


# *** INPUT DATA AND MONTE CARLO ***
input_tree_name = 'DsPhiMuMuPi_tree' if not args.fake_cand else 'WTau3Mu_tree'
mc_file = [
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022preEE_HLT_Tau3Mu.root', 
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022EE_HLT_Tau3Mu.root'] if not args.fake_cand else \
    [
    #'../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_FakeDsRate.root',
    #'../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_FakeDsRate.root',
    '../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_FakeDsRate.root',
    '../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_FakeDsRate.root',
    ] 
data_file = [
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1.root',
]
# ** RooFit Variables
# Ds mass
mass = ROOT.RooRealVar('Ds_fit_mass' if not args.fake_cand else 'tau_MuMuPi_mass', '#mu#mu #pi mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
mass.setRange('fit_range', fit_range_lo,fit_range_hi)
mass.setRange('full_range', mass_window_lo, mass_window_hi)
# Ds mass resolution
mass_err = ROOT.RooRealVar('%s_fit_mass_err'%('Ds' if not args.fake_cand else 'tau'), '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
dspl_sig = ROOT.RooRealVar('%s_Lxy_sign_BS'%('Ds' if not args.fake_cand else 'tau'), ''  , 0.0,  1000)
sv_prob  = ROOT.RooRealVar('%s_fit_vprob'%('Ds' if not args.fake_cand else 'tau'), ''  , 0.01,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass' if not args.fake_cand else 'tau_phiMuMu_mass', ''  , 0.99,  1.05, 'GeV')

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(dspl_sig)
thevars.add(sv_prob)
thevars.add(phi_mass)

### MC SIGNAL ###
sgn_selection  = '' 
base_selection = ''

mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
N_mc = mc_tree.GetEntries(base_selection)

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, sgn_selection)
fullmc.Print()
print('entries = %.2f'%fullmc.sumEntries() )
print('weight  = %e'%fullmc.weight() )
sig_efficiency = fullmc.sumEntries()/N_mc/fullmc.weight()

# signal PDF : double gaussian + constant
Mass   = ROOT.RooRealVar('Mass' , 'Mass' , Ds_mass, -1.7, 1.9)
Mass.setConstant(True)
dMass  = ROOT.RooRealVar('dM', 'dM', 0, -0.1, 0.1)
mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mass,dMass) )
width1 = ROOT.RooRealVar('width1',  'width1', 0.01,    0.001, 0.1)
width2 = ROOT.RooRealVar('width2',  'width2', 0.01,    0.001, 0.1)

gfrac   = ROOT.RooRealVar("gfrac", "", 0.5, 0.0, 1.0)
gaus1_mc  = ROOT.RooGaussian('gaus1_mc', 'gaus1', mass, mean, width1)
gaus2_mc  = ROOT.RooGaussian('gaus2_mc', 'gaus2', mass, mean, width2)
gsum_mc = ROOT.RooAddModel('gsum_mc', "", [gaus1_mc, gaus2_mc], [gfrac])

nMC = ROOT.RooRealVar('nMC', 'model_DsPhiMuMuPi_norm', fullmc.sumEntries(), 0., 10*fullmc.sumEntries())
# background
poly = ROOT.RooPolynomial('flat_bkg', "flat_bkg", mass, ROOT.RooArgList())
nBflat = ROOT.RooRealVar('nBflat', 'background', 0.5*fullmc.numEntries(), 0., fullmc.numEntries())

# signal + background
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
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range')
)
print('signal chi2 %.2f'%(frame.chiSquare(4)))
fullmc.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
)
signal_model.paramOn(
    frame,
    ROOT.RooFit.Layout(0.2, 0.50, 0.85),
    ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
)
frame.getAttText().SetTextSize(0.03)

c = ROOT.TCanvas("c", "c", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
c.SaveAs('%s/mcDsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/mcDsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag)) 
c.SetLogy(1)
c.SaveAs('%s/mcDsPhiPi_mass_Log_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/mcDsPhiPi_mass_Log_%s.pdf'%(args.plot_outdir, tag)) 
if (args.fake_cand): exit(-1)
#### DATA ####

data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]
N_data = data_tree.GetEntries(base_selection) 

datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, sgn_selection)
datatofit.Print()
bkg_efficiency = datatofit.sumEntries()/N_data

# Ds -> phi pi signal 
width1.setConstant()
width2.setConstant()
gfrac.setConstant()
gaus1_data  = ROOT.RooGaussian('gaus1_data', 'gaus1_data', mass, mean, width1)
gaus2_data  = ROOT.RooGaussian('gaus2_data', 'gaus2_data', mass, mean, width2)
gsum_data   = ROOT.RooAddModel("gsum_data", "", [gaus1_data, gaus2_data], [gfrac])

# background PDF
# + D+ -> phi pi
massDp   = ROOT.RooRealVar('massDp' , 'mass_Dp' , D_mass)
widthDp  = ROOT.RooRealVar('widthDp' , 'width_Dp' , 0.01, 0.008, 0.05)
gaus_Dp  = ROOT.RooGaussian('gaus_Dp', '', mass, massDp, widthDp)
# + falling expo
a  = ROOT.RooRealVar("a", "",  -1.0, -5, -0.1)
comb_bkg = ROOT.RooExponential('model_bkg_Ds', 'model_bkg_Ds', mass, a)

Dp_f     = ROOT.RooRealVar("Dp_f", "", 0.1, 0.0, 1.0)
full_bkg = ROOT.RooAddModel("full_bkg", "", [gaus_Dp, comb_bkg], [Dp_f])

nDs = ROOT.RooRealVar('nDs', 'Ds yield', 20000, 0., datatofit.sumEntries())
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
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range')
)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components('gsum_data'),
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range')
)
full_model.plotOn(
    frame_b, 
    ROOT.RooFit.Components('gaus_Dp'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range')
)
text_NDs = ROOT.TText(mass_window_lo + 0.02, 0.90*frame_b.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(mass_window_lo + 0.02, 0.85*frame_b.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nB.getValV() * (Dp_f.getValV()), nB.getError()))
text_Nb  = ROOT.TText(mass_window_lo + 0.02, 0.80*frame_b.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV() * (1-Dp_f.getValV()), nB.getError()))
text_NDs.SetTextSize(0.035)
text_NDp.SetTextSize(0.035)
text_Nb.SetTextSize(0.035)
frame_b.addObject(text_NDs)
frame_b.addObject(text_NDp)
frame_b.addObject(text_Nb)

datatofit.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)


c2 = ROOT.TCanvas("c2", "c2", 800, 800)
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
#nMC.setConstant(True)
dMass.setConstant(True)
width1.setConstant(True)
width2.setConstant(True)
gfrac.setConstant()

widthDp.setConstant(True)

a.setConstant(True)

wspace_mc = ROOT.RooWorkspace("DsPhiPi_mc_wspace", "DsPhiPi_mc_wspace")
getattr(wspace_mc, 'import')(signal_model)
wspace_mc.Print()
#getattr(wspace, 'import')(poly)
#getattr(wspace, 'import')(nBflat)
#getattr(wspace, 'import')(nMC)
wspace_data = ROOT.RooWorkspace("DsPhiPi_data_wspace", "DsPhiPi_data_wspace")
getattr(wspace_data, 'import')(full_model)
wspace_data.Print()
f_out_name = "DsPhiPi2022_wspace_%s.root"%(tag)
f_out = ROOT.TFile(f_out_name, "RECREATE")
wspace_mc.Write()
wspace_data.Write()
f_out.Close()


