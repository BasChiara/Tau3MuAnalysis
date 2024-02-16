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
parser.add_argument('-N',          type= int, default = 1000, help='dumber of events in the toy data')

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
data_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_reMini_2024Jan04_open.root'

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

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(bdt)
thevars.add(weight)

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)

# load model
f_in_name = "workspace_2022SB_cat%s_btd%d.root"%(args.category, args.bdt_cut*1000)
in_file = ROOT.TFile(f_in_name)
ws = in_file.Get('workspace_SB')
#ws.Print()
bkg_model = ws.pdf('model_bkg_WTau3Mu')
in_alpha  = ws.var('slope')
bkg_model.Print()

toy_data = bkg_model.generate(ROOT.RooArgSet(mass), args.N)
toy_data.Print()

# background PDF
toy_slope = ROOT.RooRealVar('toy_slope', 'toy_slope', -1.0, -10.0, -0.01)
toy_expo  = ROOT.RooExponential('toy_model_bkg_WTau3Mu', 'toy_model_bkg_WTau3Mu', mass, toy_slope)

# number of background events
toy_nbkg = ROOT.RooRealVar('toy_model_bkg_WTau3Mu_norm', 'model_bkg_WTau3Mu_norm', toy_data.numEntries(), 0, 3*toy_data.numEntries())
#toy_ext_bkg_model = ROOT.RooExtendPdf("toy_ext_model_bkg_WTau3Mu", "extended background pdf", toy_expo, toy_nbkg)
toy_ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(toy_expo),  ROOT.RooArgList(toy_nbkg))

# fit background with exponential model
results_expo = toy_ext_bkg_model.fitTo(toy_data, 
                                       ROOT.RooFit.Range('left_SB,right_SB'), 
                                       ROOT.RooFit.Save(),
                                       )

# ------------- PLOT RESULTS -------------
frame = mass.frame()
frame.SetTitle('toy model for #tau -> 3 #mu bkg - CAT %s BDTscore > %.4f'%(args.category, args.bdt_cut))

toy_data.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
toy_ext_bkg_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('left_SB,right_SB')
)


c = ROOT.TCanvas("c2", "c2", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.Draw()
c.SaveAs('toyN%d_bkg_mass_%s.png'%(args.N, args.category))
#c.SaveAs('toyN%d_bkg_mass_%s.pdf'%(args.N, args.category))

print("\t  (IN val) \t (from TOY fit)")
print("alpha  %.2f +/- %.2f \t %.2f +/- %.2f "%(in_alpha.getValV(), in_alpha.getError(),toy_slope.getValV(), toy_slope.getError() ))
print(" N          %d       \t   %d +/- %d   \t %.2f "%(args.N, toy_nbkg.getValV(), toy_nbkg.getError(), toy_nbkg.getValV()/args.N))
