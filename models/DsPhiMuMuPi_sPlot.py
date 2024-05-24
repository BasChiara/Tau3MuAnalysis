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
sys.path.insert(0, '../plots/')
from plotting_tools import ratio_plot, ratio_plot_CMSstyle

parser = argparse.ArgumentParser()
parser.add_argument('--input_workspace',default= 'DsPhiPi2022_wspace_reMini.root', help=' RooWorkSpace with signal and background model')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('--tag',            default= 'reMini', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')

args = parser.parse_args()
tag = args.tag 


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(True)
ROOT.gStyle.SetPadTickY(True)
ROOT.gStyle.SetHistMinimumZero()
ROOT.TH1.SetDefaultSumw2()
ROOT.RooMsgService.instance().setSilentMode(True)

# **** USEFUL CONSTANT VARIABLES *** #
Ds_mass = 1.9678 # GeV
D_mass  = 1.8693 # GeV
fit_range_lo  , fit_range_hi   = 1.70, 2.10 # GeV
mass_window_lo, mass_window_hi = 1.70, 2.10 # GeV #Ds_mass-mass_window, Ds_mass+mass_window

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
# Ds variables 
mass_err = ROOT.RooRealVar('Ds_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  0.03, 'GeV' )
eta      = ROOT.RooRealVar('Ds_fit_eta', '#eta_{M(3 #mu)}'  , -3.5,  3.5)
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 1.5,  1000)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.01,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass', ''  , 0.98,  1.05, 'GeV')
# MET variables
puppi_met = ROOT.RooRealVar('tau_met_pt',     'Puppi MET', 0.0,  100, 'GeV' )
deep_met  = ROOT.RooRealVar('tau_DeepMet_pt', 'deep MET' , 0.0,  100, 'GeV' )
raw_met   = ROOT.RooRealVar('tau_rawMet_pt',  'raw MET'  , 0.0,  100, 'GeV' )
## BDT score
bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
## data weights
weight = ROOT.RooRealVar('weight', 'weight'  , 0.0,  1.0, '' )

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(mass_err)
thevars.add(eta)
thevars.add(dspl_sig)
thevars.add(sv_prob)
thevars.add(phi_mass)
thevars.add(bdt)
thevars.add(weight)
thevars.add(puppi_met)
thevars.add(deep_met)
thevars.add(raw_met)

# *** INPUT DATA AND MONTE CARLO *** #
sgn_selection  = '' 
base_selection = ''
input_tree_name = 'tree_w_BDT'
mc_file = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_MC_HLT_overlap_LxyS150_2024Apr29.root' ]
data_file = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_DATA_HLT_overlap_LxyS150_2024Apr29.root ' ]

# signal MC 
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
# data
data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, sgn_selection)
fullmc.Print()
print('[+] MC entries = %.2f'%fullmc.sumEntries() )
datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, sgn_selection)
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
    ROOT.RooFit.NormRange('fit_range')
)
c = ROOT.TCanvas("c", "c", 800, 800)
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
sWeigths_selection = "Ds_fit_mass > %.2f & Ds_fit_mass < %.2f"%(mass_window_lo, mass_window_hi)
#sWeigths_selection = ""
sMcSet   = ROOT.RooDataSet(sMC.GetName(),   sMC.GetTitle(),   sMC.GetSDataSet(),   sMC.GetSDataSet().get(),   sWeigths_selection, 'nMC_sw')
sDataSet = ROOT.RooDataSet(sData.GetName(), sData.GetTitle(), sData.GetSDataSet(), sData.GetSDataSet().get(), sWeigths_selection, 'nDs_sw')

# sPlot - Ds mass
frame_sw = mass.frame(Title=" ", Bins= nbins)
sMcSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.MarkerColor(ROOT.kRed))
sDataSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) )
sc = ROOT.TCanvas("canv", "canv", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_sw.Draw()
sc.SaveAs('%s/DsPhiPi_SWmass_%s.png'%(args.plot_outdir, tag)) 
sc.SaveAs('%s/DsPhiPi_SWmass_%s.pdf'%(args.plot_outdir, tag)) 

# sPlot - BDT score
frameBDT_sw = bdt.frame(Title=" ", Bins= 20)
# MC matching histo
mc_tree.Draw('bdt_score>>h_BDT(20, 0.0, 1.0)', sWeigths_selection + ' & isMCmatching') 
h_mcBDT = ROOT.gDirectory.Get("h_BDT")
h_mcBDT.SetLineColor(ROOT.kRed)
h_mcBDT.SetLineWidth(2)
h_mcBDT.SetFillColor(ROOT.kRed)
h_mcBDT.SetFillStyle(3004)
h_mcBDT.Sumw2()
h_mcBDT.Scale(fnorm_mc.evaluate())
h_mcBDT.GetYaxis().SetTitle('Events/%.2f'%(1.0/20))
h_mcBDT.GetYaxis().SetRangeUser(0,4000)
h_mcBDT.GetXaxis().SetTitle('BDT score')
# MC sWeighted
h_sMc_BDT = sMcSet.createHistogram("sMc_BDT", bdt, ROOT.RooFit.Binning(20))
h_sMc_BDT.Scale(fnorm_mc.evaluate())
h_sMc_BDT.SetFillColor(ROOT.kRed)
h_sMc_BDT.SetFillStyle(3004)
h_sMc_BDT.SetMarkerStyle(0)
h_sMc_BDT.SetLineColor(ROOT.kRed)
h_sMc_BDT.SetLineWidth(2)
h_sMc_BDT.Sumw2()
# DATA sWeighted
h_sData_BDT = sDataSet.createHistogram("sData_BDT", bdt, ROOT.RooFit.Binning(20))
h_sData_BDT.SetMarkerColor(ROOT.kBlack)
h_sData_BDT.SetMarkerStyle(20)
h_sData_BDT.SetLineColor(ROOT.kBlack)
h_sData_BDT.SetLineWidth(2)
h_sData_BDT.Sumw2()
h_sMc_BDT.GetYaxis().SetRangeUser(0,1.2*np.max([frameBDT_sw.GetMaximum(),h_mcBDT.GetMaximum()]))

# build legend
leg = ROOT.TLegend(0.40, 0.50, 0.80, 0.65)
leg.AddEntry(h_mcBDT, "MC (norm. to D_{s}#rightarrow#phi(#mu#mu)#pi in data)", "F")
leg.AddEntry(h_sData_BDT, "data (background subtracted)");
leg.SetBorderSize(0)
leg.SetTextSize(0.04)
leg.SetFillStyle(0)

# draw
h_mcBDT.SetMaximum(1.3 * np.max([h_mcBDT.GetMaximum(), h_sData_BDT.GetMaximum()]))
ratio_plot_CMSstyle([h_sData_BDT], 
h_mcBDT, 
to_ploton = [leg], 
file_name = '%s/DsPhiPi_SWbdt_score_%s'%(args.plot_outdir, tag),
draw_opt_num = 'pe',
draw_opt_den = 'histe',
)

# -- split by category
cat_selection_dict = {
    #'A' : '(Ds_fit_mass_err/Ds_fit_mass < 0.007)',
    #'B' : '(Ds_fit_mass_err/Ds_fit_mass >= 0.007 & Ds_fit_mass_err/Ds_fit_mass < 0.012)',
    #'C' : '(Ds_fit_mass_err/Ds_fit_mass >= 0.012)',
    'A' : '(fabs(Ds_fit_eta) < 0.9)',
    'B' : '(fabs(Ds_fit_eta) > 0.9 & fabs(Ds_fit_eta) < 1.9)',
    'C' : '(fabs(Ds_fit_eta) > 1.9)'
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
    CAT_txt.SetText(0.30, 0.95*max_fixed, "CAT %s"%cat)
    # MC sWeighted
    #h_mcBDT = sMcSet.reduce(cat_selection_dict[cat]).createHistogram("sMc_BDT", bdt, ROOT.RooFit.Binning(20))
    # MC matched
    mc_tree.Draw(f'bdt_score>>h_BDT_{cat}(20, 0.0, 1.0)', sWeigths_selection + ' & isMCmatching & '+cat_selection_dict[cat]) 
    h_mcBDT = ROOT.gDirectory.Get(f'h_BDT_{cat}')
    h_mcBDT.Scale(fnorm_mc.evaluate())
    h_mcBDT.SetFillColor(ROOT.kRed)
    h_mcBDT.SetFillStyle(3004)
    h_mcBDT.SetLineColor(ROOT.kRed)
    h_mcBDT.SetLineWidth(2)
    h_mcBDT.Sumw2()
    # DATA sWeighted
    h_sData_BDT = sDataSet.reduce(cat_selection_dict[cat]).createHistogram(f'sData_BDT_{cat}', bdt, ROOT.RooFit.Binning(20))
    h_sData_BDT.SetMarkerColor(ROOT.kBlack)
    h_sData_BDT.SetMarkerStyle(20)
    h_sData_BDT.SetLineColor(ROOT.kBlack)
    h_sData_BDT.SetLineWidth(2)
    h_sData_BDT.Sumw2()
    h_mcBDT.GetYaxis().SetRangeUser(0,max_fixed)

    ratio_plot_CMSstyle([h_sData_BDT], h_mcBDT, to_ploton = [leg, CAT_txt], file_name = '%s/DsPhiPi_SWbdt_score_cat%s_%s'%(args.plot_outdir, cat, tag), draw_opt_num = 'pe', draw_opt_den = 'histe')

# sPlot - MET
METalgos = [puppi_met, deep_met, raw_met]
#METalgos = ['tau_met_pt', 'tau_DeepMet_pt', 'tau_rawMet_pt']
met_bins = 25
for met in METalgos:
    # MC sWeighted
    #h_sMc_MET   = sMcSet.createHistogram("sMc_MET", met, ROOT.RooFit.Binning(met_bins))
    # MC matched
    mc_tree.Draw(met.GetName()+'>>h_MET(%d, %.1f, %.1f)'%(met_bins, 0, 100), sWeigths_selection + ' & isMCmatching') 
    h_mcMET = ROOT.gDirectory.Get("h_MET")
    h_mcMET.Scale(fnorm_mc.evaluate())
    h_mcMET.SetFillColor(ROOT.kViolet)
    h_mcMET.SetFillStyle(3004)
    h_mcMET.SetLineColor(ROOT.kViolet)
    h_mcMET.SetLineWidth(2)
    h_mcMET.Sumw2()
    # DATA sWeighted
    h_sData_MET = sDataSet.createHistogram("sData_MET", met, ROOT.RooFit.Binning(met_bins))
    h_sData_MET.SetMarkerColor(ROOT.kBlack)
    h_sData_MET.SetMarkerStyle(20)
    h_sData_MET.SetLineColor(ROOT.kBlack)
    h_sData_MET.SetLineWidth(2)
    h_sData_MET.Sumw2()
    # build legend
    leg = ROOT.TLegend(0.40, 0.70, 0.75, 0.90)
    leg.AddEntry(h_mcMET, "MC (norm. to D_{s}#rightarrow#phi(#mu#mu)#pi in data)", "F")
    leg.AddEntry(h_sData_MET, "data (bkg subtracted)")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetFillStyle(0)
    h_mcMET.GetXaxis().SetTitle(h_sData_MET.GetXaxis().GetTitle()) 
    h_mcMET.GetYaxis().SetTitle(h_sData_MET.GetYaxis().GetTitle()) 
    h_mcMET.SetMaximum(1.3 * np.max([h_mcMET.GetMaximum(), h_sData_MET.GetMaximum()]))
    ratio_plot_CMSstyle([h_sData_MET], h_mcMET, to_ploton = [leg], file_name = '%s/DsPhiPi_SW%s_%s'%(args.plot_outdir, met.GetName(), tag), draw_opt_num = 'pe', draw_opt_den = 'hist' )


