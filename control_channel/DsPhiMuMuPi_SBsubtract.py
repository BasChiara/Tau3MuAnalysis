#############################################
#  sPlots Ds -> Phi(MuMu)Pi signal and bkg   #
#############################################

import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import numpy as np
import math
import argparse
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
import mva.config as config
import plots.plotting_tools as pt
from plots.color_text import color_text as ct
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(True)
ROOT.gStyle.SetPadTickY(True)
ROOT.gStyle.SetHistMinimumZero()
ROOT.TH1.SetDefaultSumw2()
ROOT.RooMsgService.instance().setSilentMode(True)

import ROOT

def create_hist_weights(h_data, h_bkg):
    h_w = h_bkg.Clone('h_w')
    h_w.Divide(h_data)
    for i in range(1, h_w.GetNbinsX()+1):
        w = h_w.GetBinContent(i)
        h_w.SetBinContent(i,1.0 - w)
        h_w.SetBinError(i,0.0)
        #print(f'bin {i} : data = {h_data.GetBinContent(i)} // bkg = {h_bkg.GetBinContent(i)} // weight = {h_w.GetBinContent(i)}')
    return h_w

def weighted_rdf(selection, h_weight, data_tree_name):

    # Declare the C++ function to calculate the weight based on the mass value
    ROOT.gInterpreter.Declare(f"""
    TH1F* h_weight_global = (TH1F*)gROOT->FindObject("{h_weight.GetName()}");
    
    double get_weight(double mass_value) {{
        int bin = h_weight_global->FindBin(mass_value);
        return h_weight_global->GetBinContent(bin);
    }}
    """)

    # Load the tree into a ROOT RDataFrame
    rdf = ROOT.RDataFrame(data_tree_name)

    # Define a new column "sb_weight" using the declared C++ function and the histogram
    rdf = rdf.Define("sb_weight", "get_weight(Ds_fit_mass)")
    
    # Apply the filter using the provided selection
    rdf_filtered = rdf.Filter(selection)
    
    return rdf_filtered


def draw_SBsubMC(observable, Nbins, xlo, xhi, rdf_weighted, mc_tree, mc_norm, selection, tag):
    
    h_data = rdf_weighted.Filter(selection).Histo1D((f'h_data_{observable}', f'{observable}', Nbins, xlo, xhi), observable, 'sb_weight').GetValue()
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    
    h_mc   = mc_tree.Draw(f'{observable}>>h_mc_{observable}({Nbins}, {xlo}, {xhi})', f'({selection}) * ({mc_norm} * isMCmatching * weight)', 'goff')
    h_mc   = ROOT.gDirectory.Get(f'h_mc_{observable}')
    h_mc.SetLineColor(ROOT.kMagenta + 2)
    h_mc.SetLineWidth(2)
    h_mc.SetMarkerSize(0)
    h_mc.SetTitle('')
    h_mc.GetXaxis().SetTitle(observable)

    pt.ratio_plot_CMSstyle(
        histo_num = [h_data],
        histo_den = h_mc,
        draw_opt_num = 'pe',
        draw_opt_den = 'histe3',
        x_lim = [xlo, xhi],
        y_lim = [0.0, 1.3*np.max([h_data.GetMaximum(), h_mc.GetMaximum()])],
        file_name= f'{args.plot_outdir}/DsPhiPi_{observable}_SBsub_{tag}',
        year = args.year,
    )
    



parser = argparse.ArgumentParser()
parser.add_argument('--input_workspace',default= 'DsPhiPi2022_wspace_reMini.root', help=' RooWorkSpace with signal and background model')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('-y', '--year',     choices= ['2022', '2023'], default= '2022', help='year of data taking')
parser.add_argument('-s','--signal',                                            help='signal MC file')
parser.add_argument('-d','--data',                                              help='data file')
parser.add_argument('--tag',            default= 'reMini', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')

args = parser.parse_args()
tag = f'{args.year}_{args.tag}' 

# **** USEFUL CONSTANT VARIABLES *** #
mass_window_lo, mass_window_hi = config.Ds_mass_range_lo, config.Ds_mass_range_hi# GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV
SB_range_lo   , SB_range_hi    = mass_window_lo, 1.80 # GeV
SR_range_lo   , SR_range_hi    = 1.92, 2.00 # GeV

nbins = int( (mass_window_hi-mass_window_lo)/0.01 ) # needed just for plotting, fits are all unbinned

# *** RooFit VARIABLES *** # 
mass = ROOT.RooRealVar('Ds_fit_mass', '#mu#mu #pi mass'  , config.Ds_mass_range_lo,  config.Ds_mass_range_hi, 'GeV' )
mass.setRange('fit_range', fit_range_lo, fit_range_hi)
mass.setRange('SB_range', SB_range_lo, SB_range_hi)
mass.setRange('SR_range', SR_range_lo, SR_range_hi)

var_list = [mass]
# weights
weight    = ROOT.RooRealVar('weight', 'weight', -np.inf,  np.inf, '' )
var_list.append(weight)
year_id   = ROOT.RooRealVar('year_id', 'year_id'  , 210,  270, '' )
var_list.append(year_id)
# categorization variable
eta      = ROOT.RooRealVar('Ds_fit_eta', '#eta_{3#mu}'  , -2.5,  2.5)
var_list.append(eta)
# observables for selection 
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 2.0,  np.inf)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.0,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass', ''  , 0.5,  2.0, 'GeV')
var_list.append(dspl_sig)
var_list.append(sv_prob)
var_list.append(phi_mass)
# BDT score
bdt       = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
var_list.append(bdt)

thevars = ROOT.RooArgSet()
for var in var_list:
    thevars.add(var)

# *** INPUT DATA AND MONTE CARLO *** #
base_selection = '(' + ' & '.join([
    config.year_selection[args.year],
    config.Ds_base_selection,
    config.Ds_phi_selection,
    config.Tau_sv_selection,
]) + ')'
print('[i] base_selection = %s'%base_selection)
input_tree_name = 'tree_w_BDT'
if args.signal:
    mc_file = [args.signal]
else:
    mc_file     = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output//XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]
if args.data:
    data_file = [args.data]
else:
    data_file   = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output//XGBout_DsPhiMuMuPi_DATA_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]

# signal MC 
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
# data
data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection, 'weight')
fullmc.Print()
print(f'{ct.RED}[+] MC entries = {fullmc.sumEntries():.2f}{ct.END}' )
datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection)
datatofit.Print()
print(f'{ct.BLUE}[+] DATA entries = {datatofit.sumEntries():.2f} {ct.END}' )

# --- FIT MODELS --- #

# signal MC
Mass   = ROOT.RooRealVar('Mass', 'Mass', config.Ds_mass)
dMass  = ROOT.RooRealVar('dM', 'dM', 0, -0.01, 0.01)
width_mc = ROOT.RooRealVar('width_mc', 'width_mc', 0.03, 0.001, 0.1)
mean_mc  = ROOT.RooFormulaVar('mean_mc','mean_mc', '(@0+@1)', ROOT.RooArgList(Mass,dMass) )
gaus_mc  = ROOT.RooGaussian('gaus_mc', 'gaus_mc', mass, mean_mc, width_mc)
# constant background
a_mc = ROOT.RooRealVar('a_mc', 'a_mc', -0.1, -10, 10)
#bkg_mc = ROOT.RooPolynomial('bkg_mc', 'bkg_mc', mass)
bkg_mc = ROOT.RooExponential('bkg_mc', 'bkg_mc', mass, a_mc)
# signal + background
nMC   = ROOT.RooRealVar('nMC', 'nMC', 0.01*fullmc.numEntries(), 1.0, 2.0*fullmc.numEntries())
nB_mc = ROOT.RooRealVar('nB_mc', 'nB_mc', 0.1*fullmc.numEntries(), 1.0, 2*fullmc.numEntries())
Ds_model_mc = ROOT.RooAddPdf('Ds_model_mc', 'Ds_model_mc', ROOT.RooArgList(gaus_mc, bkg_mc), ROOT.RooArgList(nMC, nB_mc))

# fit to MC
mc_results = Ds_model_mc.fitTo(fullmc, 
                  ROOT.RooFit.Range('fit_range'), 
                  ROOT.RooFit.SumW2Error(ROOT.kTRUE),
                  ROOT.RooFit.Save(ROOT.kTRUE)
                  )
print(f'{ct.PURPLE}--- MC FIT RESULTS --- {ct.END}')
mc_results.Print()
#dMass.setConstant()
nMC.setConstant()

# draw MC fit
frame = mass.frame(Title=" ", Bins= nbins)
fullmc.plotOn(
    frame,
    ROOT.RooFit.Binning(nbins),
    ROOT.RooFit.MarkerSize(1.)
)
Ds_model_mc.plotOn(
    frame,
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range'),
    ROOT.RooFit.MoveToBack(),
)
c = ROOT.TCanvas("c_mc", "c_mc", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.GetXaxis().SetRangeUser(fit_range_lo,fit_range_hi)
frame.Draw()
c.SaveAs('%s/DsPhiPi_mass_MC_%s.png'%(args.plot_outdir, tag))
c.SaveAs('%s/DsPhiPi_mass_MC_%s.pdf'%(args.plot_outdir, tag))

# DATA
# Ds -> phi pi signal
width = ROOT.RooRealVar('width',  'width', width_mc.getValV(), 0.01, 0.08)
mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mass,dMass) )

Ds_model  = ROOT.RooGaussian('Ds_model', 'Ds_model', mass, mean, width)

# background PDF
# + D+ -> phi pi
massDp   = ROOT.RooRealVar('massDp' , 'mass_Dp' , config.D_mass)
widthDp  = ROOT.RooRealVar('widthDp' , 'width_Dp' , 0.013, 0.01, 0.08)
Dplus_model  = ROOT.RooGaussian('Dplus_model', '', mass, massDp, widthDp)

# + polynomial background
p1  = ROOT.RooRealVar("p1", "p1", -0.4, -1., -0.05)
bkg_model = ROOT.RooPolynomial('poly', 'poly', mass, ROOT.RooArgList(p1))
# + falling expo
a  = ROOT.RooRealVar("a", "",  -1.0, -10, 10)
bkg_model = ROOT.RooExponential('expo', 'expo', mass, a)


nDs    = ROOT.RooRealVar('nDs', 'Ds yield', 0.01*datatofit.numEntries(), 0.001*datatofit.numEntries(), 1.0*datatofit.numEntries())
nDplus = ROOT.RooRealVar('nDplus', 'D+ yield', 0.01*datatofit.numEntries(), 0.001*datatofit.numEntries(), 1.0*datatofit.numEntries())
nB     = ROOT.RooRealVar('nB',  'background yield', 0.1*datatofit.numEntries(), 1.0, 2*datatofit.numEntries())


full_model = ROOT.RooAddPdf('full_model', 'full_model', ROOT.RooArgList(Ds_model, Dplus_model, bkg_model), ROOT.RooArgList(nDs, nDplus, nB) )

# fit to data
print(f'{ct.BLUE}--- DATA FIT RESULTS --- {ct.END}')
results = full_model.fitTo(datatofit, ROOT.RooFit.Range('fit_range'), ROOT.RooFit.SumW2Error(ROOT.kTRUE), ROOT.RooFit.Save(ROOT.kTRUE))
results.Print()

frame = mass.frame(Title=" ", Bins= nbins)
datatofit.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range'),
    ROOT.RooFit.MoveToBack(),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components(Ds_model.GetName()),
    ROOT.RooFit.LineColor(ROOT.kRed),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components(Dplus_model.GetName()),
    ROOT.RooFit.LineColor(ROOT.kOrange),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components(bkg_model.GetName()),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
)
text_NDs = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.90*frame.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.85*frame.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nDplus.getValV(), nDplus.getError()))
text_Nb  = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.80*frame.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV(), nB.getError()))
text_NDs.SetTextSize(0.035)
text_NDp.SetTextSize(0.035)
text_Nb.SetTextSize(0.035)
frame.addObject(text_NDs)
frame.addObject(text_NDp)
frame.addObject(text_Nb)
c = ROOT.TCanvas("c", "c", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.GetXaxis().SetRangeUser(fit_range_lo,fit_range_hi)
frame.Draw()
c.SaveAs('%s/DsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/DsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag))

# generate toy background and put into an histogram
N_toy = 100000
scaling = nB.getValV() / N_toy
toy_bkg = bkg_model.generate(ROOT.RooArgSet(mass), N_toy)
h_bkg   = toy_bkg.createHistogram('h_bkg', mass, ROOT.RooFit.Binning(nbins))
h_bkg.Scale(scaling)
# draw toy background and fit
frame = mass.frame(Title=" ", Bins= nbins)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components(bkg_model.GetName()),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
)
c = ROOT.TCanvas("c_toy", "c_toy", 1200, 800)
h_bkg.SetLineColor(ROOT.kBlue)
h_bkg.SetLineWidth(2)
h_bkg.SetTitle('')
h_bkg.GetXaxis().SetTitle('#mu#mu #pi mass [GeV]')
h_bkg.GetYaxis().SetTitle('Events / 0.01 GeV')
#frame.Draw()
h_bkg.Draw('pe')
c.SaveAs('%s/DsPhiPi_mass_toyBkg_%s.png'%(args.plot_outdir, tag))
c.SaveAs('%s/DsPhiPi_mass_toyBkg_%s.pdf'%(args.plot_outdir, tag))

# *** SB SUBTRACTION *** # 
N_SB = datatofit.sumEntries(f'Ds_fit_mass > {SB_range_lo} && Ds_fit_mass < {SB_range_hi}')
N_SR = datatofit.sumEntries(f'Ds_fit_mass > {SR_range_lo} && Ds_fit_mass < {SR_range_hi}')
B_yield_SB = nB.getValV() * bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SB_range').getValV() + nDplus.getValV() * Dplus_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SB_range').getValV()
B_yield_SR = nB.getValV() * bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV() + nDplus.getValV() * Dplus_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV()
TOT_yield_SR = nDs.getValV() * Ds_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV() + nDplus.getValV() * Dplus_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV() + nB.getValV() * bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV()
S_yield_SR = nDs.getValV() * Ds_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'SR_range').getValV()

factor = B_yield_SR / B_yield_SB
S_yield_SR_SBsub = N_SR - factor * N_SB

print(f'{ct.BLUE}--- BKG yield ---- {ct.END} ')
print(f'   SB : {B_yield_SB:.2f} (fit) {N_SB:.2f} (data)')
print(f'   SR : {B_yield_SR:.2f} (fit)')
print(f'    = factor = {factor:.2f}')
print(f'{ct.RED}--- SIGNAL ---- {ct.END} ')
print(f'   SR : {S_yield_SR:.2f} (fit) {S_yield_SR_SBsub:.2f} (SB-sub)')

# mass plot with SB subtraction
data_tree.Draw(f'Ds_fit_mass>>h_data({nbins}, {fit_range_lo}, {fit_range_hi})', base_selection, 'goff')
h_data = ROOT.gDirectory.Get('h_data')
# create histogram with weights
histo_weight = create_hist_weights(h_data, h_bkg)

# subtract bkg from data
h_data.Add(h_bkg, -1.0)
norm_mc = nDs.getValV() / nMC.getValV()
mc_tree.Draw(f'Ds_fit_mass>>h_mc({nbins}, {fit_range_lo}, {fit_range_hi})', f'{base_selection} * (weight*isMCmatching*{norm_mc})', 'goff')
h_mc = ROOT.gDirectory.Get('h_mc')
#h_mc.Scale(norm_mc)

print(f'{ct.BLUE}--- DATA ---- {ct.END} ')
print(f'   Entries in full region: {h_data.GetEntries():.0f}')
print(f'   Integral bkg-subtracted: {h_data.Integral():.0f}')
print(f'{ct.RED}--- MC ---- {ct.END} ')
print(f'   Entries : {h_mc.GetEntries():.0f}')
print(f'   Integral scaled by yield in data: {h_mc.Integral():.0f}')

#h_mc.SetFillColor(ROOT.kRed)
h_mc.SetLineColor(ROOT.kRed)
h_mc.SetLineWidth(2)
h_mc.SetMarkerSize(0)
h_mc.SetTitle('')
h_mc.GetXaxis().SetTitle('#mu#mu #pi mass [GeV]')
h_mc.GetYaxis().SetTitle('Events / 0.01 GeV')
h_data.SetMarkerStyle(20)
h_data.SetMarkerSize(1.)
h_data.SetMarkerColor(ROOT.kBlack)
h_data.SetLineColor(ROOT.kBlack)
h_data.SetLineWidth(2)
h_data.SetTitle('')

c = ROOT.TCanvas("c", "c", 1200, 800)

h_data.Draw('pe ')
h_mc.Draw('hist same')
c.SaveAs('%s/DsPhiPi_mass_SBsub_%s.png'%(args.plot_outdir, tag))
c.SaveAs('%s/DsPhiPi_mass_SBsub_%s.pdf'%(args.plot_outdir, tag))


# draw weighted histogram
histo_weight.Draw()
c.SaveAs('%s/DsPhiPi_mass_weight_%s.png'%(args.plot_outdir, tag)) 
rdf_weighted = weighted_rdf(base_selection, histo_weight, data_tree)
rdf_weighted.Snapshot('data_SBsub', 'DsPhiMuMuPi_SBsub.root')
# draw SB subtracted distributions
Ds_selection = f'{base_selection} & (Ds_fit_mass > {SR_range_lo} & Ds_fit_mass < {SR_range_hi})'
draw_SBsubMC('Ds_fit_mass', nbins, fit_range_lo, fit_range_hi, rdf_weighted, mc_tree, norm_mc, Ds_selection, tag)
draw_SBsubMC('Ds_fit_eta', 25, -2.5, 2.5, rdf_weighted, mc_tree, norm_mc, Ds_selection, tag)
observable_list = config.features + ['bdt_score']
for obs in observable_list :
    draw_SBsubMC(obs, config.features_NbinsXloXhiLabelLog[obs][0], config.features_NbinsXloXhiLabelLog[obs][1], config.features_NbinsXloXhiLabelLog[obs][2], rdf_weighted, mc_tree, norm_mc, Ds_selection, tag) 

