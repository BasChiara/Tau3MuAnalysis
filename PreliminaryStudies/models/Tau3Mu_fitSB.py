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
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')
parser.add_argument('--bdt_cut',    type= float, default = 0.990)

args = parser.parse_args()
tag = args.tag


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
mass_window = 0.060 # GeV
tau_mass = 1.777 # GeV
fit_range_lo  , fit_range_hi   = 1.60, 2.00 # GeV
mass_window_lo, mass_window_hi = 1.60, 2.00 # GeV #tau_mass-mass_window, tau_mass+mass_window

nbins = 80 # needed just for plotting, fits are all unbinned

blinded = True # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84

input_tree_name = 'tree_w_BDT'
mc_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2.root'
data_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2.root'


# ** RooFit Variables
# tau mass
mass = ROOT.RooRealVar('tau_fit_mass', '3-#mu mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
mass.setRange('left_SB', fit_range_lo, blind_region_lo)
mass.setRange('right_SB', blind_region_hi, fit_range_hi)
mass.setRange('fit_range', fit_range_lo,fit_range_hi)
mass.setRange('sig_range', blind_region_lo,blind_region_hi)
mass.setRange('full_range', mass_window_lo, mass_window_hi)
# tau mass resolution
mass_err = ROOT.RooRealVar('tau_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
# BDT score
bdt = ROOT.RooRealVar('bdt', 'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.0,  1.0, '' )


### MC SIGNAL ###
sgn_selection = 'bdt > %.4f'%args.bdt_cut
if args.category == 'A'  : sgn_selection += ' & tau_fit_mass_err/tau_fit_mass < 0.007'
if args.category == 'B'  : sgn_selection += ' & tau_fit_mass_err/tau_fit_mass > 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012'
if args.category == 'C'  : sgn_selection += ' & tau_fit_mass_err/tau_fit_mass > 0.012'
if args.category == 'AB' : sgn_selection += ' & tau_fit_mass_err/tau_fit_mass < 0.012'

mc_tree = ROOT.TChain(input_tree_name)
mc_tree.AddFile(mc_file)
thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(bdt)
thevars.add(weight)

fullmc = ROOT.RooDataSet('mc_WTau3Mu', 'mc_WTau3Mu', mc_tree, thevars, sgn_selection, "weight")
fullmc.Print()

# signal PDF
Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass, -1.7, 1.9)
Mtau.setConstant(True)
dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -1., 1.)
mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
width1 = ROOT.RooRealVar('width1', 'width', 0.01,    0.005, 0.05)
width2 = ROOT.RooRealVar('width2', 'width', 0.05,    0.01, 0.5)
gaus1  = ROOT.RooGaussian('sig_gaus_1', 'sig_gaus_1', mass, mean, width1)
gaus2  = ROOT.RooGaussian('sig_gaus_2', 'sig_gaus_2', mass, mean, width2)

f = ROOT.RooRealVar("f", "", 0., 1.)
signal_model = ROOT.RooAddPdf("model_WTau3Mu", "model_WTau3Mu", ROOT.RooArgList(gaus1,gaus2), f )
nsig = ROOT.RooRealVar('model_WTau3Mu_norm', 'model_WTau3Mu_norm', 4*1e5, 1e3, 1e6)
ext_signal_model = ROOT.RooExtendPdf("ext_signal_model", "extended signal pdf", signal_model, nsig)
N_sig_params = 5

# signal fit
results_gaus = ext_signal_model.fitTo(
    fullmc, 
    ROOT.RooFit.Range('sig_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE)
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
    ROOT.RooFit.Components('sig_gaus_1'),
    ROOT.RooFit.LineColor(ROOT.kGreen),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
    ROOT.RooFit.Range('sig_range'),
    #ROOT.RooFit.NormRange('full_range')
)
signal_model.plotOn(
    frame, 
    ROOT.RooFit.Components('sig_gaus_2'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
    ROOT.RooFit.Range('sig_range'),
    #ROOT.RooFit.NormRange('full_range')
)

ext_signal_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('sig_range'),
    ROOT.RooFit.NormRange('sig_range')
)
print('signal chi2 %.2f'%(frame.chiSquare()))

c = ROOT.TCanvas("c", "c", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
c.SaveAs('%s/signal_mass_%s.png'%(args.plot_outdir, args.category))
c.SaveAs('%s/signal_mass_%s.pdf'%(args.plot_outdir, args.category))
c.SetLogy(1)
c.SaveAs('%s/signal_mass_log_%s.png'%(args.plot_outdir, args.category))
c.SaveAs('%s/signal_mass_log_%s.pdf'%(args.plot_outdir, args.category))

#exit(-1)
#### DATA ####

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
#data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022E.root')
#data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root')
#data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022G.root')


if blinded:
    print('BLIND')
    # cut for blinding
    blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  ' ((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f)) & (%s)'%(blind_region_lo, blind_region_hi, sgn_selection) , ROOT.RooArgList(thevars))
    fulldata = ROOT.RooDataSet('data_obs', 'data_obs', data_tree,  thevars, blinder)
else:
    print('NOW I SEE')
    fulldata = ROOT.RooDataSet('data_obs', 'data_obs', data_tree,  thevars, sgn_selection)
fulldata.Print()

frame_b = mass.frame()
frame_b.SetTitle('#tau -> 3 #mu signal - CAT %s BDTscore > %.4f'%(args.category, args.bdt_cut))

fulldata.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)

# background PDF
slope = ROOT.RooRealVar('slope', 'slope', -0.01, -10.0, -1e-4)
expo  = ROOT.RooExponential('model_bkg_WTau3Mu', 'model_bkg_WTau3Mu', mass, slope)

# number of background events
nbkg = ROOT.RooRealVar('ext_model_bkg_WTau3Mu_norm', 'ext_model_bkg_WTau3Mu_norm', fulldata.numEntries(), 0, 3*fulldata.numEntries())
ext_bkg_model = ROOT.RooExtendPdf("ext_model_bkg_WTau3Mu", "extended background pdf", expo, nbkg)

# fit background with exponential model
results_expo = ext_bkg_model.fitTo(fulldata, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save())
#expo.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))     # this is the fit in the entire mass range
ext_bkg_model.plotOn(
    frame_b, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('full_tange'),
    ROOT.RooFit.NormRange('left_SB,right_SB')
)

c2 = ROOT.TCanvas("c2", "c2", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_b.Draw()
c2.SaveAs('%s/background_mass_%s.png'%(args.plot_outdir, args.category))
c2.SaveAs('%s/background_mass_%s.pdf'%(args.plot_outdir, args.category))
c2.SetLogy(1)
c2.SaveAs('%s/background_mass_log_%s.png'%(args.plot_outdir, args.category))
c2.SaveAs('%s/background_mass_log_%s.pdf'%(args.plot_outdir, args.category))

# ----------------------------------------------------------------------------------------------------
#### SAVE MODEL TO A WORKSPACE ####
dMtau.setConstant(True)
width1.setConstant(True)
width2.setConstant(True)
f.setConstant(True)

ws = ROOT.RooWorkspace("workspace_SB", "workspace_SB")
getattr(ws, 'import')(fulldata)
getattr(ws, 'import')(signal_model)
getattr(ws, 'import')(expo)
f_out_name = "workspace_2022SB_cat%s_btd%d.root"%(args.category, args.bdt_cut*1000)
f_out = ROOT.TFile(f_out_name, "RECREATE")
ws.Print()
ws.Write()
f_out.Close()


# dump the text datacard
with open('datacard_2022_cat%s_btd%d.txt'%(args.category, args.bdt_cut*1000), 'w') as card:
   card.write(
'''
imax 1 number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes background    WTau3Mu       {f_root:s} workspace_SB:model_bkg_WTau3Mu
shapes signal        WTau3Mu       {f_root:s} workspace_SB:model_WTau3Mu
shapes data_obs      WTau3Mu       {f_root:s} workspace_SB:data_obs
--------------------------------------------------------------------------------
bin                  WTau3Mu
observation          {obs:d}
--------------------------------------------------------------------------------
bin                                     WTau3Mu             WTau3Mu
process                                 signal              background
process                                 0                   1
rate                                    {signal:.4f}        {bkg:.4f}
--------------------------------------------------------------------------------
lumi          lnN                       1.022               -   
--------------------------------------------------------------------------------
bkgScale      rateParam                 WTau3Mu        background      1.
slope         param   {slopeval:.4f} {slopeerr:.4f}
'''.format(
         f_root  = f_out_name,
         obs     = fulldata.numEntries() if blinded==False else -1, # number of observed events
         #signal   = mass_histo_mc.Integral(), # number of EXPECTED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
         signal   = fullmc.numEntries(), # number of EXPECTED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
         bkg      = nbkg.getVal(), # number of expected background events **over the full mass range** using the exponential funciton fitted in the sidebands 
         slopeval = slope.getVal(), 
         slopeerr = slope.getError(),
         )
)