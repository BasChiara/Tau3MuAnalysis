#############################################
#  sPlots Ds -> Phi(MuMu)Pi signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(True)
ROOT.gStyle.SetPadTickY(True)
ROOT.gStyle.SetHistMinimumZero()
ROOT.TH1.SetDefaultSumw2()
ROOT.RooMsgService.instance().setSilentMode(True)
ROOT.EnableImplicitMT()

import numpy as np
import pandas as pd

import argparse

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import mva.config as config
import plots.plotting_tools as pt
from plots.color_text import color_text as ct


def plot_sWeights(observable, mc_norm = 1.0 ,selection = '', nbins = 100, lo = 0, hi = 100, color = ROOT.kRed, to_ploton = None, add_tag = ''):
    frame_sw = observable.frame(Title=" ", Bins= nbins)
    mc_tree.Draw(f'{observable.GetName()}>>h_{observable.GetName()}({nbins}, {lo}, {hi})', f'({selection}) * (weight * {mc_norm})', 'goff')
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

def reweight_by_observable(observable = 'Ds_fit_eta', mc_rdf = None, data_rdf = None):
    
    nbins, lo, hi   = 50, -2.5, 2.5#config.features_NbinsXloXhiLabelLog[observable][0:3]
    selection       = '1'
    mc_norm         = 'norm_factor'

    h_mc = mc_rdf.Histo1D(('h_'+observable+'_mc', '', nbins, lo, hi), observable, 'norm_weight').GetPtr()
    h_mc.Sumw2()
    h_data = data_rdf.Histo1D(('h_'+observable+'_data', '', nbins, lo, hi), observable, 'nDs_sw').GetPtr()
    h_data.Sumw2()
    
    h_ratio_eta = h_data.Clone('h_ratio_'+observable)
    h_ratio_eta.Divide(h_mc)
    # print h_ratio_eta content
    for i in range(1, h_ratio_eta.GetNbinsX() + 1):
        print(f'bin {i}: {h_ratio_eta.GetBinContent(i)}')

    
    return h_ratio_eta

def apply_reweighting(h_weights, df, handle = 'Ds_fit_eta', wname = 'w_byEta'):

    this_df = df.copy()
    this_df[wname] = -1.0*np.ones(len(this_df))
    for bin in range(1, h_weights.GetNbinsX() + 1):
        bin_lo = h_weights.GetXaxis().GetBinLowEdge(bin)
        bin_hi = h_weights.GetXaxis().GetBinUpEdge(bin)
        bin_weight = h_weights.GetBinContent(bin)
        mask = (df[handle] >= bin_lo) & (df[handle] < bin_hi)
        this_df.loc[mask, wname] = bin_weight

    return this_df

parser = argparse.ArgumentParser()
parser.add_argument('--input_workspace',default= 'DsPhiPi2022_wspace_reMini.root', help=' RooWorkSpace with signal and background model')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('-y', '--year',     choices= list(config.year_selection.keys()), default= '2022', help='year of data taking')
parser.add_argument('-s','--signal',                                            help='signal MC file')
parser.add_argument('-d','--data',                                              help='data file')
parser.add_argument('--tag',            default= 'reMini', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')

args = parser.parse_args()
tag = f'{args.year}_{args.tag}'
# create output directory
if not os.path.exists(args.plot_outdir):
    os.makedirs(args.plot_outdir)
    print(f'[i] created output directory {args.plot_outdir}')

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
dspl_sig = ROOT.RooRealVar('tau_Lxy_sign_BS', ''  , 0.0,  np.inf)
sv_prob  = ROOT.RooRealVar('tau_fit_vprob', ''  , 0.0,  1.0)
phi_mass = ROOT.RooRealVar('phi_fit_mass', ''  , 0.5,  2.0, 'GeV')
var_list.append(dspl_sig)
var_list.append(sv_prob)
var_list.append(phi_mass)
bdt       = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
var_list.append(bdt)

# BDT input features
bdt_input = config.features
bdt_input.remove('tau_Lxy_sign_BS')
bdt_input.remove('tau_fit_vprob')
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

# signal MC
mc_file = [args.signal] if args.signal else [config.mc_bdt_samples['DsPhiMuMuPi'] ] 
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]

fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection, 'weight')
fullmc = ROOT.RooDataSet('mc_DsPhiMuMuPi', 'mc_DsPhiMuMuPi', mc_tree, thevars, base_selection, 'weight')
fullmc.Print('v')
print('[+] MC entries = %.2f'%fullmc.sumEntries() )
# data
data_file = [args.data] if args.data else [config.data_bdt_samples['DsPhiMuMuPi'] ]
data_tree = ROOT.TChain(input_tree_name)
[data_tree.AddFile(f) for f in data_file]

datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, base_selection)
datatofit.Print('v')
print('[+] DATA entries = %.2f'%datatofit.sumEntries() )

# -- FIT -- #
# Fit to MC & fix the parameters
nMC = wspace_mc['nMC']
nMC.setConstant()
nMC_raw = ROOT.RooRealVar('nMC_raw', 'nMC_raw', fullmc.sumEntries())

# Fit to data & fix the parameters
full_model.fitTo(datatofit, ROOT.RooFit.Range('fit_range'), ROOT.RooFit.SumW2Error(ROOT.kTRUE))
nDs = wspace_data['nDs']
nDs.setConstant()
nDp = wspace_data['nDp']
nDp.setConstant()
nB = wspace_data['nB']
nB.setConstant()

# * MC normalization
fnorm_mc = ROOT.RooFormulaVar('fnorm_mc','fnorm_mc', '(@0/@1)', ROOT.RooArgList(nDs,nMC_raw) )

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
mc_rdf = ROOT.RDataFrame(input_tree_name, mc_file).Filter(base_selection).Define('norm_factor', f'{fnorm_mc.evaluate()}').Define('norm_weight', f'weight * norm_factor')

sDataSet = ROOT.RooDataSet(sData.GetName(), sData.GetTitle(), sData.GetSDataSet(), sData.GetSDataSet().get(), base_selection, 'nDs_sw')
sDataSet.convertToTreeStore()
# store in temporary file
temp_file_name = 'sWeight/temp_sWeighted_data.root'
temp_file = ROOT.TFile(temp_file_name, 'recreate')
sDataSet.Write()
temp_file.Close()
print(f'[i] sWeighted DATA dataset saved in {temp_file_name}')
data_rdf    = ROOT.RDataFrame("RooTreeDataStore_sData_data_fit", temp_file_name)

# --- re-weight MC by eta --- #
h_reWeight_eta  = reweight_by_observable(observable = 'Ds_fit_eta', mc_rdf = mc_rdf, data_rdf = data_rdf)
mc_df_rew       = apply_reweighting(h_reWeight_eta, pd.DataFrame(mc_rdf.AsNumpy()), handle = 'Ds_fit_eta', wname = 'w_byEta')

# *** save results on file *** #
sWeights_file_base = os.path.join(os.path.expandvars('$EOS/Tau3MuRun3/data/control_channel/sWeight/'), f'sWeights_{tag}_')   #f'sWeight/sWeights_{tag}_'
mc_fname = f'{sWeights_file_base}MC.root'
data_fname = f'{sWeights_file_base}DATA.root'
# remove files if already exist
if os.path.exists(mc_fname):
    os.system(f'rm {mc_fname}')
if os.path.exists(data_fname):
    os.system(f'rm {data_fname}')

# attach data driven normalization to MC
ROOT.RDF.MakeNumpyDataFrame({col: mc_df_rew[col].values for col in mc_df_rew.columns}).Define('norm_byEta_weight', 'weight*norm_factor*w_byEta').Snapshot('mc_tree', mc_fname)
print(f'[i] MC normalized saved in {mc_fname}')
data_rdf.Snapshot('data_tree', data_fname)
print(f'[i] sWeights for DATA saved in {data_fname}')

# if the root files exist merge results
if (os.path.exists(mc_fname) and os.path.exists(data_fname)):
    os.system(f'hadd -f {sWeights_file_base}DataMc.root {mc_fname} {data_fname}')
    print(f'[i] sWeights for MC and DATA saved in {sWeights_file_base}DataMc.root')
    os.system(f'rm {mc_fname} {data_fname}')
    os.system(f'rm {temp_file_name}')
else:
    print('[!] something went wrong in saving sWeights')