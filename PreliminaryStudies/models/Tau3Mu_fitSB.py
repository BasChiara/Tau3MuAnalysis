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

args = parser.parse_args()
tag = args.tag


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

mass_window = 0.060 # GeV
tau_mass = 1.78 # GeV
fit_range_lo  , fit_range_hi   = 1.60, 2.00 # GeV
mass_window_lo, mass_window_hi = 1.60, 2.00 # GeV #tau_mass-mass_window, tau_mass+mass_window

nbins = 80 # needed just for plotting, fits are all unbinned

blinded = True # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84


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

### MC SIGNAL ###

sgn_selection = ''
if args.category == 'A' : sgn_selection += 'tau_fit_mass_err/tau_fit_mass < 0.007'
if args.category == 'B' : sgn_selection += 'tau_fit_mass_err/tau_fit_mass > 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012'
if args.category == 'C' : sgn_selection += 'tau_fit_mass_err/tau_fit_mass > 0.012'
sgn_weight = '0.5'

mc_tree = ROOT.TChain('Tau3Mu_HLTemul_tree')
mc_tree.AddFile('../outRoot/recoKinematicsT3m_MC_2022_HLT_Tau3Mu.root')
thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
fullmc = ROOT.RooDataSet('mc', 'mc', mc_tree, thevars, sgn_selection)
fullmc.Print()

# signal PDF
mean  = ROOT.RooRealVar('mean' , 'mean' , tau_mass, -1.7, 1.9)
width1 = ROOT.RooRealVar('width1', 'width', 0.01,    0.005, 0.05)
width2 = ROOT.RooRealVar('width2', 'width', 0.05,    0.01, 0.5)
gaus1  = ROOT.RooGaussian('sig_gaus_1', 'sig_gaus_1', mass, mean, width1)
gaus2  = ROOT.RooGaussian('sig_gaus_2', 'sig_gaus_2', mass, mean, width2)

f = ROOT.RooRealVar("f", "", 0., 1.)
signal_model = ROOT.RooAddPdf("signal_model", "signal_model", ROOT.RooArgList(gaus1,gaus2), f )
nsig = ROOT.RooRealVar('nsig', 'nsig', 4*1e5, 1e3, 1e6)
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
frame.SetTitle('')

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

exit(-1)
#### DATA ####

data_tree = ROOT.TChain('Tau3Mu_HLTemul_tree')
data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022E.root')
data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root')
data_tree.AddFile('/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022G.root')


if blinded:
    print('BLIND')
    # cut for blinding
    blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  ' tau_fit_mass > 1.6 ', ROOT.RooArgList(thevars))
    fulldata = ROOT.RooDataSet('data', 'data', data_tree,  thevars, blinder)
else:
    print('NOW I SEE')
    fulldata = ROOT.RooDataSet('data', 'data', data_tree,  thevars, sgn_selection)
fulldata.Print()
frame_b = mass.frame()
fulldata.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)

# background PDF
slope = ROOT.RooRealVar('slope', 'slope', -0.001, -1e6, 0.)
expo  = ROOT.RooExponential('bkg_expo', 'bkg_expo', mass, slope)

# number of background events
nbkg = ROOT.RooRealVar('nbkg', 'nbkg', 1e5, 1e0, 1e6)
ext_bkg_model = ROOT.RooExtendPdf("ext_bkg_model", "extended bacground pdf", expo, nbkg)

# fit background with exponential model
results_expo = ext_bkg_model.fitTo(fulldata, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save())
#expo.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))     # this is the fit in the entire mass range
ext_bkg_model.plotOn(
    frame_b, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('left_SB,right_SB'),
    ROOT.RooFit.NormRange('left_SB,right_SB')
)

c2 = ROOT.TCanvas("c2", "c2", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_b.Draw()
c2.SaveAs('%s/background_mass.png'%args.plot_outdir)
c2.SaveAs('%s/background_mass.pdf'%args.plot_outdir)
c2.SetLogy(1)
c2.SaveAs('%s/background_mass_log.pdf'%args.plot_outdir)
c2.SaveAs('%s/background_mass_log.png'%args.plot_outdir)
