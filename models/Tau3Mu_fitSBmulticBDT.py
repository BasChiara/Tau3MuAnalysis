#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
import os
from math import pi, sqrt, fabs
from glob import glob
from pdb import set_trace
from array import array 
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/Tau3Mu_massFit/reMini', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-u','--unblind',action = 'store_true' ,help='set it to run UN-blind')
parser.add_argument('--save_ws',    action = 'store_true' ,help='set it to save the workspace for combine')
parser.add_argument('--category',   default = 'noCat')
parser.add_argument('-y','--year',      default = '22')
parser.add_argument('--bdt_beta',       type= float, default = 0.990)
parser.add_argument('--bdt_q',          type= float, default = 0.990)
parser.add_argument('--bdt_cut',          type= float, default = 0.990)

args = parser.parse_args()


#tag = 'bdtBeta%d_bdtQ%d_%s%s'%(args.bdt_beta*100, fabs(args.bdt_q)*100, args.category, args.year) + ('_' + args.tag ) if not (args.tag is None) else ''
tag = 'bdtT3M_%s%s'%(args.category, args.year) + ('_' + args.tag ) if not (args.tag is None) else ''
process_name = 'WTau3Mu_%s%s'%(args.category, args.year)

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
mass_window = 0.060 # GeV
tau_mass = 1.777 # GeV
fit_range_lo  , fit_range_hi   = 1.70, 1.85 # GeV
mass_window_lo, mass_window_hi = 1.60, 2.00 # GeV #tau_mass-mass_window, tau_mass+mass_window

nbins = 40 # needed just for plotting, fits are all unbinned

runblind = not args.unblind # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84
# phi
phi_mass = 1.020 #GeV
phi_window = 0.020 #GeV
omega_mass = 0.783 #GeV


input_tree_name = 'tree_w_BDT'
mc_file     = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_HLToverlapResample_kFold_2024Apr21.root'
data_file   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_HLToverlapResample_kFold_2024Apr21_open.root'


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
bdt_t3m = ROOT.RooRealVar('bdt_score_t3m',  'BDT score'  , 0.0,  1.0, '' )
bdt_b   = ROOT.RooRealVar('bdt_score_b',    'BDT score'  , 0.0,  1.0, '' )
bdt_w3m = ROOT.RooRealVar('bdt_score_w3m',  'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.00005,  1.0, '' )
# di-muon mass
mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
# run
run = ROOT.RooRealVar('run', 'run'  , 0,  362800)

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(bdt_b)
thevars.add(bdt_t3m)
thevars.add(bdt_w3m)
thevars.add(weight)
thevars.add(mu12_mass)
thevars.add(mu13_mass)
thevars.add(mu23_mass)
thevars.add(run)

### MC SIGNAL ###
#bdt_selection = '( bdt_score_b/(1-bdt_score_t3m) < (%.2f*bdt_score_t3m + %.2f) )'%(args.bdt_beta, args.bdt_q) 
#bdt_selection = '( (0.25*bdt_score_t3m - bdt_score_b ) > %.3f )'%(args.bdt_cut)
bdt_selection = '(bdt_score_t3m > 0.995 & bdt_score_w3m > 0.0001)' 
phi_veto = '''(fabs(tau_mu12_fitM- {mass:.3f})> {window:.3f} & fabs(tau_mu23_fitM - {mass:.3f})> {window:.3f} & fabs(tau_mu13_fitM -  {mass:.3f})>{window:.3f})'''.format(mass =phi_mass , window = phi_window/2. )
cat_selection = ''
if args.category == 'A'  : cat_selection = '(tau_fit_mass_err/tau_fit_mass <= 0.007)'
if args.category == 'B'  : cat_selection = '(tau_fit_mass_err/tau_fit_mass > 0.007 & tau_fit_mass_err/tau_fit_mass <= 0.012)'
if args.category == 'C'  : cat_selection = '(tau_fit_mass_err/tau_fit_mass > 0.012)'
if args.category == 'AB' : cat_selection = '(tau_fit_mass_err/tau_fit_mass < 0.012)'
data22_selection =  '(run < 362800)' 
blind_selection  =  '((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f))'%(blind_region_lo, blind_region_hi)
mc22_selection   =  ''
base_selection   = ' & '.join([bdt_selection, phi_veto, cat_selection])
sgn_selection    = base_selection 
data_selection   = base_selection

print('\n------------------------------------')
print('SIGNAL SELECTION : %s'%sgn_selection)
print('DATA   SELECTION : %s'%data_selection)
print('------------------------------------\n')
mc_tree = ROOT.TChain(input_tree_name)
mc_tree.AddFile(mc_file)
N_mc = mc_tree.GetEntries(base_selection)

fullmc = ROOT.RooDataSet('mc_%s'%process_name, 'mc_%s'%process_name, mc_tree, thevars, sgn_selection, "weight")
fullmc.Print()
print('entries = %.2f'%fullmc.sumEntries() )
print('weight  = %e'%fullmc.weight() )
sig_efficiency = fullmc.sumEntries()/N_mc/fullmc.weight()

# signal PDF
Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass, -1.7, 1.9)
Mtau.setConstant(True)
dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -0.1, 0.1)
mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
width  = ROOT.RooRealVar('width',  'width', 0.01,    0.005, 0.05)

nsig   = ROOT.RooRealVar('model_sig_%s_norm'%process_name, 'model_sig_%s_norm'%process_name, fullmc.sumEntries(), 0., 3*fullmc.sumEntries())
gaus   = ROOT.RooGaussian('model_sig_%s'%process_name, 'model_sig_%s'%process_name, mass, mean, width)

signal_model = ROOT.RooAddPdf('ext_model_sig_%s'%process_name, 'ext_model_sig_%s'%process_name, ROOT.RooArgList(gaus), nsig )

# signal fit
results_gaus = signal_model.fitTo(
    fullmc, 
    ROOT.RooFit.Range('sig_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
    ROOT.RooFit.PrintLevel(1),
)

# * draw & save
frame = mass.frame()
frame.SetTitle('CAT %s - %s '%(args.category, bdt_selection))

fullmc.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
    DataError="SumW2",
)
signal_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('sig_range'),
    ROOT.RooFit.MoveToBack()
)
print('signal chi2 %.2f'%(frame.chiSquare()))
signal_model.paramOn(
    frame,
    ROOT.RooFit.Title("Signal Fit parameters:"),
    ROOT.RooFit.Layout(0.6, 0.75, 0.9),
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

# -- plot pulls
h_pullMC = frame.pullHist()
frame_pull = mass.frame(Title = '[pull] #tau -> 3 #mu signal - CAT %s'%(args.category))
frame_pull.addPlotable(h_pullMC, 'P')
cp = ROOT.TCanvas("cp", "cp", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_pull.Draw()
cp.SaveAs('%s/pull_signal_mass_%s.png'%(args.plot_outdir, tag)) 
cp.SaveAs('%s/pull_signal_mass_%s.pdf'%(args.plot_outdir, tag)) 

#### DATA ####

data_tree = ROOT.TChain(input_tree_name)
data_tree.AddFile(data_file)
N_data = data_tree.GetEntries(base_selection) 

if runblind:
    print('BLIND')
    # cut for blinding
    blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  ' ((tau_fit_mass < %.3f )|| (tau_fit_mass > %.3f)) & (%s)'%(blind_region_lo, blind_region_hi, data_selection) , ROOT.RooArgList(thevars))
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, blinder)
else:
    print('NOW I SEE')
    datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, data_selection)
datatofit.Print()
bkg_efficiency = datatofit.sumEntries()/N_data

frame_b = mass.frame()
frame_b.SetTitle('CAT %s - %s'%(args.category, bdt_selection))

datatofit.plotOn(
    frame_b, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)

# background PDF
slope = ROOT.RooRealVar('slope', 'slope', -1.0, -10.0, 10.0)
expo  = ROOT.RooExponential('model_bkg_%s'%process_name, 'model_bkg_%s'%process_name, mass, slope)

# number of background events
nbkg = ROOT.RooRealVar('model_bkg_%s_norm'%process_name, 'model_bkg_%s_norm'%process_name, datatofit.numEntries(), 0., 3*datatofit.numEntries())
ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(expo),  ROOT.RooArgList(nbkg))

# fit background with exponential model
results_expo = ext_bkg_model.fitTo(datatofit, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save(),ROOT.RooFit.PrintLevel(-1))
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

if not args.save_ws : exit(-1)
# ----------------------------------------------------------------------------------------------------
#### SAVE MODEL TO A WORKSPACE ####
wspace_filename = "input_combine/wspace_%s_%s.root"%(process_name,tag)
wspace_name     = "WTau3Mu_w"
# fix the signal shape
dMtau.setConstant(True)
#width.setConstant(True)

# save observed data // bkg-only Asimov with name 'dat_obs'
fulldata = ROOT.RooDataSet('full_data', 'full_data', data_tree, thevars, sgn_selection)
if runblind:
    # GenerateAsimovData() generates binned data following the binning of the observables
    mass.setBins(nbins)
    data = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(ext_bkg_model, ROOT.RooArgSet(mass) )
    data.SetName('data_obs') 
else :
    data     = ROOT.RooDataSet('data_obs','data_obs', fulldata, ROOT.RooArgSet(mass))
data.Print()

ws = ROOT.RooWorkspace(wspace_name, wspace_name)
getattr(ws, 'import')(data)
getattr(ws, 'import')(gaus)
getattr(ws, 'import')(nsig)
getattr(ws, 'import')(expo)
getattr(ws, 'import')(nbkg)
ws.Print()
ws.writeToFile(wspace_filename)

#### WRITE THE DATACARD ####
datacard_name = "input_combine/datacard_%s_%s.txt"%(process_name,tag)
# dump the text datacard
with open(datacard_name, 'w') as card:
   card.write(
'''
imax 1 number of channels
jmax * number of background sources
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes bkg         {proc}       {ws_file} {ws_name}:{bkg_model}
shapes sig         {proc}       {ws_file} {ws_name}:{sig_model}
shapes data_obs    {proc}       {ws_file} {ws_name}:data_obs
--------------------------------------------------------------------------------
bin                {proc}
observation        {obs:d}
--------------------------------------------------------------------------------
bin                                     {proc}              {proc}
process                                 sig                 bkg
process                                 0                   1
rate                                    {signal:.4f}        {bkg:.4f}
--------------------------------------------------------------------------------
bkg_norm rateParam                   {proc}      bkg     1. 
slope    param  {slopeval:.4f} {slopeerr:.4f}
'''.format(
         proc     = process_name, 
         ws_file  = wspace_filename, 
         ws_name  = wspace_name, 
         bkg_model= expo.GetName(),
         sig_model= gaus.GetName(),
         obs      = fulldata.numEntries() if runblind==False else -1, # number of observed events
         signal   = fullmc.sumEntries(), # number of EXPECTED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
         bkg      = nbkg.getVal(), # number of expected background events **over the full mass range** using the exponential funciton fitted in the sidebands 
         slopeval = slope.getVal(),
         slopeerr = slope.getError()
         )
)



