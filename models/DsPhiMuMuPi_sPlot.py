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
sys.path.append('..')
import mva.config as config
import plots.plotting_tools as pt
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(True)
ROOT.gStyle.SetPadTickY(True)
ROOT.gStyle.SetHistMinimumZero()
ROOT.TH1.SetDefaultSumw2()
ROOT.RooMsgService.instance().setSilentMode(True)

def plot_sWeights(observable, mc_norm = 1.0 ,selection = '', nbins = 100, lo = 0, hi = 100, color = ROOT.kRed, to_ploton = None, add_tag = ''):
    frame_sw = observable.frame(Title=" ", Bins= nbins)
    # MC matched
    mc_tree.Draw(f'{observable.GetName()}>>h_{observable.GetName()}({nbins}, {lo}, {hi})', selection + ' * (weight)', 'goff')
    h_mc = ROOT.gDirectory.Get(f"h_{observable.GetName()}")
    h_mc.Scale(mc_norm)
    h_mc.SetFillColor(color)
    h_mc.SetFillStyle(3004)
    h_mc.SetLineColor(color)
    h_mc.SetLineWidth(2)
    h_mc.Sumw2()
    # DATA sWeighted
    h_sData = sDataSet.reduce(selection).createHistogram(f"sData_{observable.GetName()}", observable, ROOT.RooFit.Binning(nbins))
    h_sData.SetMarkerColor(ROOT.kBlack)
    h_sData.SetMarkerStyle(20)
    h_sData.SetLineColor(ROOT.kBlack)
    h_sData.SetLineWidth(2)
    h_sData.Sumw2()
    # build legend
    leg = ROOT.TLegend(0.40, 0.70, 0.75, 0.90)
    leg.AddEntry(h_mc, "MC (norm. to D_{s}#rightarrow#phi(#mu#mu)#pi in data)", "F")
    leg.AddEntry(h_sData, "data (bkg subtracted)")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetFillStyle(0)
    # set up axis
    h_mc.GetXaxis().SetTitle(h_sData.GetXaxis().GetTitle())
    h_mc.GetYaxis().SetTitle(h_sData.GetYaxis().GetTitle())
    #h_mc.SetMaximum(1.3 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()]))
    to_ploton.append(leg)
    pt.ratio_plot_CMSstyle(
        [h_sData],
        h_mc,
        to_ploton = to_ploton,
        file_name = f'{args.plot_outdir}/DsPhiPi_SW{observable.GetName()}_{tag}{add_tag}',
        draw_opt_num = 'pe',
        draw_opt_den = 'hist',
        y_lim = [0, 1.3 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()])],
    )

parser = argparse.ArgumentParser()
parser.add_argument('--input_workspace',default= 'DsPhiPi2022_wspace_reMini.root', help=' RooWorkSpace with signal and background model')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('-y', '--year',     choices= ['2022', '2023'], default= '2022', help='year of data taking')
parser.add_argument('--tag',            default= 'reMini', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')

args = parser.parse_args()
tag = args.tag 

# **** USEFUL CONSTANT VARIABLES *** #
mass_window_lo, mass_window_hi = config.Ds_mass_range_lo, config.Ds_mass_range_hi # GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV

nbins = 40 # needed just for plotting, fits are all unbinned

# *** GET FIT MODEL FROM WSPACE *** #
# + signal model
wspace_mc_name = 'DsPhiPi_mc_wspace' 
wspace_mc = ROOT.TFile(args.input_workspace).Get(wspace_mc_name)
wspace_mc.Print()
signal_model = wspace_mc['extMCmodel_DsPhiMuMuPi']

# + full model
wspace_data_name = 'DsPhiPi_data_wspace' 
wspace_data = ROOT.TFile(args.input_workspace).Get(wspace_data_name)
wspace_data.Print()
full_model = wspace_data['extDATAmodel_DsPhiMuMuPi']

mass = wspace_data['Ds_fit_mass']

# *** RooFit VARIABLES *** # 
## data weights
weight    = ROOT.RooRealVar('weight', 'weight'  , -10.0,  1000.0, '' )
year_id   = ROOT.RooRealVar('year_id', 'year_id'  , 210,  270, '' )
# Ds variables 
#mass_err = ROOT.RooRealVar('Ds_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
eta      = ROOT.RooRealVar('Ds_fit_eta', '#eta_{M(3 #mu)}'  , -4.0,  4.0)
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 0.0,  100)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.0,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass', ''  , 0.5,  2.0, 'GeV')
# MET variables
puppi_met = ROOT.RooRealVar('tau_met_pt',     'Puppi MET', 0.0,  100, 'GeV' )
deep_met  = ROOT.RooRealVar('tau_DeepMet_pt', 'deep MET' , 0.0,  100, 'GeV' )
raw_met   = ROOT.RooRealVar('tau_rawMet_pt',  'raw MET'  , 0.0,  100, 'GeV' )
## BDT score
bdt       = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )

thevars = ROOT.RooArgSet()
thevars.add(weight)
thevars.add(year_id)
thevars.add(mass)
#thevars.add(mass_err)
thevars.add(eta)
thevars.add(dspl_sig)
thevars.add(sv_prob)
thevars.add(phi_mass)
thevars.add(bdt)

thevars.add(puppi_met)
thevars.add(deep_met)
thevars.add(raw_met)

# *** INPUT DATA AND MONTE CARLO *** #
base_selection = '(' + ' & '.join([
    config.year_selection[args.year],
    config.Ds_base_selection,
    config.Ds_phi_selection,
    config.Tau_sv_selection,
]) + ')'
print('[i] base_selection = %s'%base_selection)
sgn_selection  = base_selection 
input_tree_name = 'tree_w_BDT'
mc_file     = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS1.9_2024Jul12.root' ]
data_file   = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_DATA_Optuna_HLT_overlap_LxyS1.9_2024Jul12.root' ]

# signal MC 
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
# data
data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, sgn_selection, 'weight')
fullmc.Print()
print('[+] MC entries = %.2f'%fullmc.sumEntries() )
datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, sgn_selection, 'weight')
datatofit.Print()
print('[+] DATA entries = %.2f'%datatofit.sumEntries() )

# Fit to mc & fix the parameters
signal_model.fitTo(fullmc, ROOT.RooFit.Range('fit_range'))
nMC = wspace_mc['nMC']
nMC.setConstant()
nBflat = wspace_mc['nBflat']
nBflat.setConstant()
# Fit to data & fix the parameters
full_model.fitTo(datatofit, ROOT.RooFit.Range('fit_range'))
nDs = wspace_data['nDs']
nDs.setConstant()
Dp_f = wspace_data['Dp_f']
Dp_f.setConstant()
nB = wspace_data['nB']
nB.setConstant()
# * MC normalization
fnorm_mc = ROOT.RooFormulaVar('fnorm_mc','fnorm_mc', '(@0/@1)', ROOT.RooArgList(nDs,nMC) )

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
    ROOT.RooFit.Components('gsum_data'),
    ROOT.RooFit.LineColor(ROOT.kRed),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components('gaus_Dp'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
)
text_NDs = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.90*frame.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.85*frame.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nB.getValV() * (Dp_f.getValV()), nB.getError()))
text_Nb  = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.80*frame.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV() * (1-Dp_f.getValV()), nB.getError()))
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


# *** sPlot *** #
sMC   = ROOT.RooStats.SPlot("sMC",  "SPlot of signal MC", fullmc, signal_model, ROOT.RooArgList(nMC, nBflat))
sData = ROOT.RooStats.SPlot("sData","SPlot of data",datatofit, full_model, ROOT.RooArgList(nDs,nB))

# check the weights
# the yield must be unchanged
print(' check sWeights in Monte Carlo...')
print(' yield of Ds  is %d / from sWeigts is %d'%(nMC.getVal(), sMC.GetYieldFromSWeight('nMC')))
print(' yield of flat-BKG is %d / from sWeigts is %d'%(nBflat.getVal(), sMC.GetYieldFromSWeight('nBflat')))
print(' check sWeights in data ...')
print(' yield of Ds  is %d / from sWeigts is %d'%(nDs.getVal(), sData.GetYieldFromSWeight('nDs')))
print(' yield of comb-BKG + D+ is %d / from sWeigts is %d'%(nB.getVal(), sData.GetYieldFromSWeight('nB')))

# create a weighted datasets
sWeigths_selection = base_selection 
#sWeigths_selection = "Ds_fit_mass > %.2f & Ds_fit_mass < %.2f"%(1.92, 2.0)
sMcSet   = ROOT.RooDataSet(sMC.GetName(),   sMC.GetTitle(),   sMC.GetSDataSet(),   sMC.GetSDataSet().get(),   sWeigths_selection, 'nMC_sw')
sDataSet = ROOT.RooDataSet(sData.GetName(), sData.GetTitle(), sData.GetSDataSet(), sData.GetSDataSet().get(), sWeigths_selection, 'nDs_sw')

# *** PLOT sWeights ** #

# sPlot - Ds weights
frame_sw = mass.frame(Title=" ", Bins= nbins)
sMcSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.MarkerColor(ROOT.kRed))
sDataSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) )
sc = ROOT.TCanvas("canv", "canv", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_sw.Draw()
sc.SaveAs('%s/DsPhiPi_SWmass_%s.png'%(args.plot_outdir, tag)) 
sc.SaveAs('%s/DsPhiPi_SWmass_%s.pdf'%(args.plot_outdir, tag)) 

# sPlot - Ds mass
plot_sWeights(mass, fnorm_mc.evaluate(), sWeigths_selection, nbins, mass_window_lo, mass_window_hi, ROOT.kBlue, [])

# sPlot - BDT score
plot_sWeights(bdt, fnorm_mc.evaluate(), sWeigths_selection, 25, 0.0, 1.0, ROOT.kRed, [])

# -- split by category
cat_selection_dict = {
    'A' : f'(fabs(Ds_fit_eta) < {config.eta_thAB})',
    'B' : f'(fabs(Ds_fit_eta) > {config.eta_thAB} & fabs(Ds_fit_eta) < {config.eta_thBC})',
    'C' : f'(fabs(Ds_fit_eta) > {config.eta_thBC})',
}
# text on plot
CAT_txt = ROOT.TText()
CAT_txt.SetTextFont(43)
CAT_txt.SetTextAngle(0)
CAT_txt.SetTextColor(ROOT.kBlack)    
CAT_txt.SetTextSize(40)
CAT_txt.SetTextAlign(11)
for i, cat in enumerate(cat_selection_dict.keys()):
    print(' - category %d %s'%(i,cat))
    max_fixed = 2000
    CAT_txt.SetText(0.30, 0.90*max_fixed, "CAT %s"%cat)
    plot_sWeights(bdt, fnorm_mc.evaluate(), f'({sWeigths_selection} & {cat_selection_dict[cat]})', 25, 0.0, 1.0, ROOT.kRed, [CAT_txt], add_tag=f'_cat{cat}')

# sPlot - MET
METalgos = [puppi_met, deep_met, raw_met]
#METalgos = ['tau_met_pt', 'tau_DeepMet_pt', 'tau_rawMet_pt']
met_bins = 25
for met in METalgos:
    plot_sWeights(met, fnorm_mc.evaluate(), sWeigths_selection, met_bins, 0, 100, ROOT.kViolet, [])

# sPlot - Lxy significance
lxy_bins = 40
lxy_max = 100
plot_sWeights(dspl_sig, fnorm_mc.evaluate(), sWeigths_selection, lxy_bins, 0, lxy_max, ROOT.kGreen, [])


