#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
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
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/Tau3Mu_massFit/reMini', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')
parser.add_argument('--bdt_cut',    type= float, default = 0.990)

args = parser.parse_args()
tag = 'bdt%d_%s'%(args.bdt_cut*1000, args.category) + ('_' + args.tag ) if not (args.tag is None) else ''


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
mass_window = 0.060 # GeV
tau_mass = 1.777 # GeV
fit_range_lo  , fit_range_hi   = 1.73, 1.82 # GeV
mass_window_lo, mass_window_hi = 1.60, 2.00 # GeV #tau_mass-mass_window, tau_mass+mass_window

nbins = 40 # needed just for plotting, fits are all unbinned

blinded = True # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84
# phi
phi_mass = 1.020 #GeV
phi_window = 0.020 #GeV
omega_mass = 0.783 #GeV


input_tree_name = 'tree_w_BDT'
mc_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_reMini22_23_kFold_2024Feb02.root'
data_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_reMini22_23_kFold_2024Feb02_blind.root'


# ** RooFit Variables
# tau mass
mass = ROOT.RooRealVar('tau_fit_mass', '3-#mu mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
mass.setRange('left_SB', mass_window_lo, blind_region_lo)
mass.setRange('right_SB', blind_region_hi, mass_window_hi)
mass.setRange('fit_range', fit_range_lo,fit_range_hi)
mass.setRange('sig_range', blind_region_lo,blind_region_hi)
mass.setRange('full_range', mass_window_lo, mass_window_hi)
# tau mass resolution
mass_err = ROOT.RooRealVar('tau_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
# BDT score
bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.0,  1.0, '' )
# di-muon mass
mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
# run
run = ROOT.RooRealVar('run', 'run'  , 0,  362800)

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(bdt)
thevars.add(weight)
thevars.add(mu12_mass)
thevars.add(mu13_mass)
thevars.add(mu23_mass)
thevars.add(run)

### MC SIGNAL ###
sgn_selection = 'bdt_score > %.4f'%args.bdt_cut
phi_veto = '''fabs(tau_mu12_fitM- {mass:.3f})> {window:.3f} & fabs(tau_mu23_fitM - {mass:.3f})> {window:.3f} & fabs(tau_mu13_fitM -  {mass:.3f})>{window:.3f}'''.format(mass =phi_mass , window = phi_window/2. )
cat_selection = ''
if args.category == 'A'  : cat_selection = ' & tau_fit_mass_err/tau_fit_mass < 0.007'
if args.category == 'B'  : cat_selection = ' & tau_fit_mass_err/tau_fit_mass > 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012'
if args.category == 'C'  : cat_selection = ' & tau_fit_mass_err/tau_fit_mass > 0.012'
if args.category == 'AB' : cat_selection = ' & tau_fit_mass_err/tau_fit_mass < 0.012'
base_selection = phi_veto + '&' + cat_selection + ' & run < 362800'
sgn_selection += '& '+ base_selection 

mc_tree = ROOT.TChain(input_tree_name)
mc_tree.AddFile(mc_file)
N_mc = mc_tree.GetEntries(base_selection)

fullmc = ROOT.RooDataSet('mc_WTau3Mu', 'mc_WTau3Mu', mc_tree, thevars, sgn_selection, "weight")
fullmc.Print()
print('entries = %.2f'%fullmc.sumEntries() )
print('weight  = %e'%fullmc.weight() )
sig_efficiency = fullmc.sumEntries()/N_mc/fullmc.weight()

# signal PDF
Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass, -1.7, 1.9)
Mtau.setConstant(True)
dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -1., 1.)
mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
width  = ROOT.RooRealVar('width',  'width', 0.01,    0.001, 0.10)
gaus   = ROOT.RooGaussian('model_WTau3Mu', 'model_WTau3Mu', mass, mean, width)

f = ROOT.RooRealVar("f", "", 0., 1.)
nsig = ROOT.RooRealVar('Ns', 'model_WTau3Mu_norm', fullmc.sumEntries(), 0., 3*fullmc.sumEntries())
signal_model = ROOT.RooAddPdf("ext_model_WTau3Mu", "model_WTau3Mu", ROOT.RooArgList(gaus), nsig )

# signal fit
results_gaus = signal_model.fitTo(
    fullmc, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
)

# * draw & save
frame = mass.frame()
frame.SetTitle('#tau -> 3 #mu signal - CAT %s BDTscore > %.4f'%(args.category, args.bdt_cut))

fullmc.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    #ROOT.RooFit.DrawOption('B'), 
    #ROOT.RooFit.DataError(ROOT.RooAbsData.None), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
    #ROOT.RooFit.FillStyle(3003),                
)

signal_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('sig_range'),
    ROOT.RooFit.NormRange('fit_range')
)
print('signal chi2 %.2f'%(frame.chiSquare()))
signal_model.paramOn(
    frame,
    ROOT.RooFit.Title("Signal Fit parameters:"),
    ROOT.RooFit.Layout(0.6, 0.95, 0.9),
    ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
)
frame.getAttText().SetTextSize(0.03)

c = ROOT.TCanvas("c", "c", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
c.SaveAs('%s/signal_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/signal_mass_%s.pdf'%(args.plot_outdir, tag)) 
c.SetLogy(1)
c.SaveAs('%s/signal_mass_Log_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/signal_mass_Log_%s.pdf'%(args.plot_outdir, tag)) 

#### DATA ####
base_selection += ' & ((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f))'%(blind_region_lo, blind_region_hi)

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
N_data = data_tree.GetEntries(base_selection) 

if blinded:
    print('BLIND')
    # cut for blinding
    blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  ' ((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f)) & (%s)'%(blind_region_lo, blind_region_hi, sgn_selection) , ROOT.RooArgList(thevars))
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, blinder)
else:
    print('NOW I SEE')
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, sgn_selection)
datatofit.Print()
bkg_efficiency = datatofit.sumEntries()/N_data

frame_b = mass.frame()
frame_b.SetTitle('#tau -> 3 #mu signal - CAT %s BDTscore > %.3f'%(args.category, args.bdt_cut))

datatofit.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)

# background PDF
slope = ROOT.RooRealVar('slope', 'slope', -1.0, -50.0, 0.001)
expo  = ROOT.RooExponential('model_bkg_WTau3Mu', 'model_bkg_WTau3Mu', mass, slope)

# number of background events
#nbkg = ROOT.RooRealVar('model_bkg_WTau3Mu_norm', 'model_bkg_WTau3Mu_norm', datatofit.numEntries(), 0., 3*datatofit.numEntries())
nbkg = ROOT.RooRealVar('Nb', 'model_bkg_WTau3Mu_norm', datatofit.numEntries(), 0., 3*datatofit.numEntries())
#ext_bkg_model = ROOT.RooExtendPdf("ext_model_bkg_WTau3Mu", "extended background pdf", expo, nbkg)
ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(expo),  ROOT.RooArgList(nbkg))

# fit background with exponential model
results_expo = ext_bkg_model.fitTo(datatofit, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save())
ext_bkg_model.plotOn(
    frame_b, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('left_SB,right_SB')
)
fullmc.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.DrawOption('B'), 
    ROOT.RooFit.DataError(ROOT.RooAbsData.ErrorType(2)), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
    ROOT.RooFit.FillStyle(3004),                
)
signal_model.plotOn(
    frame_b, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('sig_range'),
    ROOT.RooFit.NormRange('sig_range')
)
# print N signal and N background on plot
text_S = ROOT.TText(tau_mass, 0.90*frame_b.GetMaximum(), "Ns = %.2f +/- %.2f"%(nsig.getValV(), nsig.getError()))
text_eS= ROOT.TText(tau_mass, 0.85*frame_b.GetMaximum(), "effS = %.2f"%(sig_efficiency))
text_B = ROOT.TText(tau_mass, 0.80*frame_b.GetMaximum(), "Nb = %.2f +/- %.2f"%(nbkg.getValV(), nbkg.getError()))
text_eB= ROOT.TText(tau_mass, 0.75*frame_b.GetMaximum(), "effB = %.2e"%(bkg_efficiency))
text_S.SetTextSize(0.035)
text_eS.SetTextSize(0.035)
text_B.SetTextSize(0.035)
text_eB.SetTextSize(0.035)
frame_b.addObject(text_S)
frame_b.addObject(text_eS)
frame_b.addObject(text_B)
frame_b.addObject(text_eB)


c2 = ROOT.TCanvas("c2", "c2", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_b.Draw()
c2.SaveAs('%s/SigBkg_mass_%s.png'%(args.plot_outdir, tag)) 
c2.SaveAs('%s/SigBkg_mass_%s.pdf'%(args.plot_outdir, tag)) 
c2.SetLogy(1)
c2.SaveAs('%s/SigBkg_mass_Log_%s.png'%(args.plot_outdir, tag)) 
c2.SaveAs('%s/SigBkg_mass_Log_%s.pdf'%(args.plot_outdir, tag)) 
print(' -- RooExtendPdf = %.2f'%ext_bkg_model.expectedEvents(ROOT.RooArgSet(mass)))
print(' -- BaseSelection %s'%base_selection)
print(' == S efficiency %.2f '%sig_efficiency)
print(' == B efficiency %.2e '%bkg_efficiency)

exit(-1)
# ----------------------------------------------------------------------------------------------------
#### SAVE MODEL TO A WORKSPACE ####
dMtau.setConstant(True)
width1.setConstant(True)
width2.setConstant(True)
f.setConstant(True)
fulldata = ROOT.RooDataSet('full_data', 'full_data', data_tree, thevars, sgn_selection)
data     = ROOT.RooDataSet('data_obs','data_obs', fulldata, ROOT.RooArgSet(mass))
data.Print()
ws = ROOT.RooWorkspace("workspace_SB", "workspace_SB")
getattr(ws, 'import')(data)
getattr(ws, 'import')(signal_model)
getattr(ws, 'import')(nsig)
getattr(ws, 'import')(expo)
getattr(ws, 'import')(nbkg)
f_out_name = "workspace_2022SB_%s.root"%tag
f_out = ROOT.TFile(f_out_name, "RECREATE")
ws.Print()
ws.Write()
f_out.Close()
