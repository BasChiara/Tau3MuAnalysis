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

def plot_sWeights(observable, mc_norm = 1.0 ,selection = '', nbins = 100, lo = 0, hi = 100, color = ROOT.kRed, to_ploton = None, add_tag = ''):
    frame_sw = observable.frame(Title=" ", Bins= nbins)
    # MC matched
    mc_tree.Draw(f'{observable.GetName()}>>h_{observable.GetName()}({nbins}, {lo}, {hi})', f'({selection}) * (weight * isMCmatching * {mc_norm})', 'goff')
    h_mc = ROOT.gDirectory.Get(f"h_{observable.GetName()}")
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
        year      = args.year,
        draw_opt_num = 'pe',
        draw_opt_den = 'hist e',
        ratio_w      = 1.0,
        y_lim = [0, 1.5 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()])],
        x_lim = [lo, hi],
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
mass_window_lo, mass_window_hi = config.Ds_mass_range_lo, config.Ds_mass_range_hi # GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV
binwidth = 0.01 
nbins = int((fit_range_hi-fit_range_lo)/binwidth) + 1 # just for plotting

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
# MET variables
puppi_met = ROOT.RooRealVar('tau_met_pt',     'Puppi MET', 0.0,  np.inf, 'GeV' )
deep_met  = ROOT.RooRealVar('tau_DeepMet_pt', 'deep MET' , 0.0,  np.inf, 'GeV' )
raw_met   = ROOT.RooRealVar('tau_rawMet_pt',  'raw MET'  , 0.0,  np.inf, 'GeV' )
var_list.append(puppi_met)
var_list.append(deep_met)
var_list.append(raw_met)
# BDT input features
bdt_input = config.features
bdt_input.remove('tau_Lxy_sign_BS')
bdt_input.remove('tau_fit_vprob')
bdt_input.remove('tau_met_pt')
for feat in bdt_input:
    var = ROOT.RooRealVar(feat, feat, -np.inf, np.inf)
    var_list.append(var)
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
print('[+] MC entries = %.2f'%fullmc.sumEntries() )
datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection)
datatofit.Print()
print('[+] DATA entries = %.2f'%datatofit.sumEntries() )

# Fit to mc & fix the parameters
#signal_model.fitTo(fullmc, ROOT.RooFit.Range('fit_range'), ROOT.RooFit.SumW2Error(ROOT.kTRUE))
nMC = wspace_mc['nMC']
nMC.setConstant()
#nBflat = wspace_mc['nBflat']
#nBflat.setConstant()
# Fit to data & fix the parameters
full_model.fitTo(datatofit, ROOT.RooFit.Range('fit_range'), ROOT.RooFit.SumW2Error(ROOT.kTRUE))
nDs = wspace_data['nDs']
nDs.setConstant()
#Dp_f = wspace_data['Dp_f']
#Dp_f.setConstant()
nDp = wspace_data['nDp']
nDp.setConstant()
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
    ROOT.RooFit.Components('Ds_model'),
    ROOT.RooFit.LineColor(ROOT.kRed),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components('gaus_Dp'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
)
text_NDs = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.90*frame.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.85*frame.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nDp.getValV(), nDp.getError()))
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

# *** sPlot *** #
#sMC   = ROOT.RooStats.SPlot("sMC",  "SPlot of signal MC", fullmc, signal_model, ROOT.RooArgList(nMC, nBflat))
sData = ROOT.RooStats.SPlot("sData","SPlot of data",datatofit, full_model, ROOT.RooArgList(nDs, nDp, nB))

# check the weights
# the yield must be unchanged
print('\n')
print(f'{ct.BOLD} --- SUMMARY --- {ct.END}')
print(' Ds yield in MC is %d'%nMC.getVal())
print(f'{ct.BOLD} --- sWeights --- {ct.END}')
print(' Ds yield in DATA is %d (fit) / %d (sDataset)'%(nDs.getVal(), sData.GetYieldFromSWeight('nDs')))
print(' BKG + D+ yield in DATA %d (fit) / %d (sDataset)'%(nB.getVal(), sData.GetYieldFromSWeight('nB')))

# create a weighted datasets
sWeigths_selection = base_selection 
#sWeigths_selection = "Ds_fit_mass > %.2f & Ds_fit_mass < %.2f"%(1.92, 2.0)
#sMcSet   = ROOT.RooDataSet(sMC.GetName(),   sMC.GetTitle(),   sMC.GetSDataSet(),   sMC.GetSDataSet().get(),   sWeigths_selection, 'nMC_sw')
sDataSet = ROOT.RooDataSet(sData.GetName(), sData.GetTitle(), sData.GetSDataSet(), sData.GetSDataSet().get(), sWeigths_selection, 'nDs_sw')

# *** PLOT sWeights ** #

# sPlot - Ds weights
frame_sw = mass.frame(Title=" ", Bins= nbins)
#sMcSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.MarkerColor(ROOT.kRed))
sDataSet.plotOn(frame_sw, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) )
sc = ROOT.TCanvas("canv", "canv", 800, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_sw.Draw()
sc.SaveAs('%s/DsPhiPi_SWmass_%s.png'%(args.plot_outdir, tag)) 
sc.SaveAs('%s/DsPhiPi_SWmass_%s.pdf'%(args.plot_outdir, tag)) 

# sPlot - Ds mass
plot_sWeights(mass, fnorm_mc.evaluate(), sWeigths_selection, nbins, mass_window_lo, mass_window_hi, ROOT.kBlue, [])
# sPlot - Ds eta
eta_bins, eta_min, eta_max = 25, eta.getMin(), eta.getMax()
plot_sWeights(eta, fnorm_mc.evaluate(), sWeigths_selection, eta_bins, eta_min, eta_max, ROOT.kOrange, [])
plot_sWeights(eta, fnorm_mc.evaluate(), sWeigths_selection + '&(bdt_score> 0.960)', int(eta_bins/2), eta_min, eta_max, ROOT.kOrange, [], add_tag='_bdt960')
# sPlot - BDT score
plot_sWeights(bdt, fnorm_mc.evaluate(), sWeigths_selection, 25, 0.0, 1.0, ROOT.kRed, [])
plot_sWeights(bdt, fnorm_mc.evaluate(), sWeigths_selection + '&(bdt_score > 0.960)', 25, 0.0, 1.0, ROOT.kRed, [], add_tag='_bdt960')

# text on plot
CAT_txt = ROOT.TText()
CAT_txt.SetTextFont(43)
CAT_txt.SetTextAngle(0)
CAT_txt.SetTextColor(ROOT.kBlack)    
CAT_txt.SetTextSize(40)
CAT_txt.SetTextAlign(11)
CAT_txt.SetNDC()
for i, cat in enumerate(config.Ds_category_selection.keys()):
    if cat == 'ABC': continue
    CAT_txt.SetText(0.40, 0.60, "CAT %s"%cat)
    plot_sWeights(bdt, fnorm_mc.evaluate(), f'({sWeigths_selection} & {config.Ds_category_selection[cat]})', 25, 0.0, 1.0, ROOT.kRed, [CAT_txt], add_tag=f'_cat{cat}')

# *** save results on file *** #
sWeights_file_base = f'sWeights_{tag}_'
mc_fname = f'{sWeights_file_base}MC.root'
data_fname = f'{sWeights_file_base}DATA.root'
# remove files if already exist
if os.path.exists(mc_fname):
    os.system(f'rm {mc_fname}')
if os.path.exists(data_fname):
    os.system(f'rm {data_fname}')

# attach data driven normalization to MC
mc_rdf = ROOT.RDataFrame(input_tree_name, mc_file).Filter(base_selection).Define('norm_factor', f'{fnorm_mc.evaluate()}')
mc_rdf.Snapshot('mc_tree', mc_fname)
print(f'[i] MC normalized saved in {mc_fname}')

# save sWeights for DATA
sWeights_file = ROOT.TFile(data_fname, 'recreate')
sWeights_file.cd()
sDataSet.convertToTreeStore()
sDataSet.Write()
sWeights_file.Close()
print(f'[i] sWeights for DATA saved in {data_fname}')
# if the root files exist merge results
if (os.path.exists(mc_fname) and os.path.exists(data_fname)):
    os.system(f'hadd -f {sWeights_file_base}DataMc.root {mc_fname} {data_fname}')
    print(f'[i] sWeights for MC and DATA saved in {sWeights_file_base}DataMc.root')
    os.system(f'rm {mc_fname} {data_fname}')
else:
    print('[!] something went wrong in saving sWeights')