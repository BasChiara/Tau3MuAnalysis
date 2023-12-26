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
parser.add_argument('--mu_pair',    default = '12')

args = parser.parse_args()
tag = args.tag


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
# tau
mass_window = 0.060 # GeV
tau_mass = 1.777 # GeV
mass_window_lo, mass_window_hi = 1.60, 2.00 # GeV #tau_mass-mass_window, tau_mass+mass_window
blinded = True # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84
# phi
phi_mass = 1.020 #GeV
omega_mass = 0.783 #GeV
fit_range_lo  , fit_range_hi   = 0.80, 1.30 # GeV

nbins = 50 if (args.category == 'noCat') else 25# needed just for plotting, fits are all unbinned



input_tree_name = 'tree_w_BDT'
#mc_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2_EFG_MuMuFilter.root'
mc_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_reMiniAOD_2022FG.root'
#data_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2_EFG_MuMuFilter_open.root'
data_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_reMiniAOD_2022FG_open.root'


# ** RooFit Variables
# tau mass
cand_mass = ROOT.RooRealVar('tau_fit_mass', '3-#mu mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
cand_mass.setRange('left_SB', mass_window_lo, blind_region_lo)
cand_mass.setRange('right_SB', blind_region_hi, mass_window_hi)
#mass.setRange('fit_range', fit_range_lo,fit_range_hi)
#mass.setRange('sig_range', blind_region_lo,blind_region_hi)
#mass.setRange('full_range', mass_window_lo, mass_window_hi)
# tau mass resolution
mass_err = ROOT.RooRealVar('tau_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
# BDT score
bdt = ROOT.RooRealVar('bdt', 'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.0,  1.0, '' )
# di-muon mass
label = ''
if(args.mu_pair == '12') :
   label = 'M(#mu_{1} #mu_{2})'
elif (args.mu_pair == '23'):
   label = 'M(#mu_{2} #mu_{3})'
elif (args.mu_pair == '13'):
   label = 'M(#mu_{1} #mu_{3})'
mumu_mass = ROOT.RooRealVar('tau_mu%s_fitM'%(args.mu_pair), label, fit_range_lo,  fit_range_hi, 'GeV' )
mumu_mass.setRange('fit_range', fit_range_lo, fit_range_hi)
#mu23_mass = ROOT.RooRealVar('tau_mu23_M', 'tau_mu23_M'  , -10.0,  10.0, 'GeV' )
#mu13_mass = ROOT.RooRealVar('tau_mu13_M', 'tau_mu13_M'  , -10.0,  10.0, 'GeV' )

thevars = ROOT.RooArgSet()
thevars.add(cand_mass)
thevars.add(mass_err)
thevars.add(bdt)
thevars.add(weight)
thevars.add(mumu_mass)
#thevars.add(mu13_mass)
#thevars.add(mu23_mass)

### IMPORT DATA ###
base_selection = 'bdt > %.4f'%args.bdt_cut
if args.category == 'A'  : base_selection += ' & tau_fit_mass_err/tau_fit_mass < 0.007'
if args.category == 'B'  : base_selection += ' & tau_fit_mass_err/tau_fit_mass > 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012'
if args.category == 'C'  : base_selection += ' & tau_fit_mass_err/tau_fit_mass > 0.012'
if args.category == 'AB' : base_selection += ' & tau_fit_mass_err/tau_fit_mass < 0.012'

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
if blinded:
    print('BLIND')
    # cut for blinding
    blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  ' ((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f)) & (%s)'%(blind_region_lo, blind_region_hi, base_selection) , ROOT.RooArgList(thevars))
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, blinder)
else:
    print('NOW I SEE')
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection)
datatofit.Print()

# signal PDF
# phi->mumu
M_mumu_phi   = ROOT.RooRealVar('M_mumu_phi' , 'M_mumu_phi' , phi_mass, 0.8, 1.2)
width_phi  = ROOT.RooRealVar('width_phi',  'width_phi', 0.01,    0.001, 0.10)
gaus_phi   = ROOT.RooGaussian('signal_phimumu', 'signal_phimumu', mumu_mass, M_mumu_phi, width_phi)
nsig_phi = ROOT.RooRealVar('Nphi', 'signal_phi', datatofit.sumEntries(), 0., 3*datatofit.sumEntries())
# omega->mumu
M_mumu_omega   = ROOT.RooRealVar('M_mumu_omega' , 'M_mumu_omega' , omega_mass, 0.8, 1.2)
width_omega  = ROOT.RooRealVar('width_omega',  'width_omega', 0.01,    0.001, 0.10)
gaus_omega   = ROOT.RooGaussian('signal_omegamumu', 'signal_omegamumu', mumu_mass, M_mumu_omega, width_omega)
nsig_omega = ROOT.RooRealVar('Nomega', 'signal_omega', datatofit.sumEntries(), 0., 3*datatofit.sumEntries())


nbkg = ROOT.RooRealVar('Nb', 'background_phimumu', datatofit.numEntries(), 0., 3*datatofit.numEntries())
a0 = ROOT.RooRealVar('a0', 'a0', 0, -1.0,1.0)
a1 = ROOT.RooRealVar('a1', 'a1', 0, -1.0,1.0)
poly = ROOT.RooPolynomial('background_phimumu', "background_phimumu", mumu_mass, ROOT.RooArgList(a0, a1), 0)

full_model = ROOT.RooAddPdf('full_model', 'full_model', ROOT.RooArgList(gaus_phi,poly), ROOT.RooArgList(nsig_phi, nbkg))

results = full_model.fitTo(
    datatofit, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
)

# * draw & save
frame = mumu_mass.frame()
frame.SetTitle('%s spectrum - CAT %s BDTscore > %.4f'%(label, args.category, args.bdt_cut))
datatofit.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range')
)
print('signal chi2 %.2f'%(frame.chiSquare()))
full_model.paramOn(
    frame,
    ROOT.RooFit.Layout(0.6, 0.95, 0.9),
    ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
)
frame.getAttText().SetTextSize(0.03)
datatofit.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
#full_model.plotOn(
#    frame, 
#    ROOT.RooFit.LineColor(ROOT.kOrange),
#    ROOT.RooFit.Components('signal_phimumu'),
#    ROOT.RooFit.Range('fit_range'),
#    ROOT.RooFit.NormRange('fit_range')
#)

c = ROOT.TCanvas("c", "c", 1000, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
name = {'12': 'Mu1Mu2', '23':'Mu2Mu3', '13':'Mu1Mu3'}
c.SaveAs('%s/%s_mass_bdt%d_%s.png'%(args.plot_outdir, name[args.mu_pair], args.bdt_cut*1000, args.category))
c.SaveAs('%s/%s_mass_bdt%d_%s.pdf'%(args.plot_outdir, name[args.mu_pair], args.bdt_cut*1000, args.category))
