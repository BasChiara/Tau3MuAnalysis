import ROOT
import cmsstyle as CMS
import argparse
import pickle
import os
import numpy  as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics         import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold

from scipy.stats import ks_2samp

from collections import OrderedDict
from itertools import product

from pdb import set_trace

# from my config
import config as cfg

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/features', help=' output directory for plots')
parser.add_argument('--category'   ,                                                                 help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',            default= 'app_emulateRun2',                                  help='tag to the training')
parser.add_argument('--bdt_cut',        default= 0.995, type= float,                                 help='bdt threshold')
parser.add_argument('--debug',          action = 'store_true' ,                                      help='set it to have useful printout')
parser.add_argument('--isMulticlass',   action = 'store_true',                                       help='set to use teh multiclass setting')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                                help='set random state for reproducible results')
parser.add_argument('-p', '--process',  choices = ['WTau3Mu', 'W3MuNu', 'DsPhiPi', 'ZTau3Mu', 'invMedID'], default = 'Tau3Mu',help='which process in the simulation')
parser.add_argument('-s', '--signal',   action = 'append',                                           help='file with signal events with BDT applied')
parser.add_argument('-d', '--data',     action = 'append',                                           help='file with data events with BDT applied')
parser.add_argument('-y', '--year',     choices= ['2022', '2023', 'Run3'],   default= '2022',                 help='data-taking year to process')

args = parser.parse_args()
tag = args.tag + '_%s'%args.year
removeNaN = False

# ------------ INPUT/OUTPUT ------------ # 
if not os.path.isdir(args.plot_outdir):
    os.makedirs(args.plot_outdir)
    os.system(f'cp ~/public/index.php {args.plot_outdir}')
    print(f'[i] created directory for output plots : {args.plot_outdir}')
else:
    print(f'[i] already existing directory for output plots : {args.plot_outdir}')

# ------------ APPLY SELECTIONS ------------ #
base_selection = ' & '.join([
    cfg.base_selection,
    cfg.phi_veto,
    cfg.year_selection[args.year],
    f' (tau_Lxy_sign_BS > {args.LxySign_cut})',

])
sig_selection  = base_selection 
if (args.process == 'invMedID') : 
    sig_selection = base_selection
bkg_selection  = base_selection + f'& {cfg.sidebands_selection}'
if (args.process == 'W3MuNu') : 
    sig_selection = bkg_selection

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

#  ------------ PICK SIGNAL & BACKGROUND -------------- #
if(args.signal is None):
    signals     = [
        cfg.mc_bdt_samples[args.process]
    ]
else :
    signals = args.signal 
if(args.data is None):
    backgrounds  = [
        cfg.data_bdt_samples[args.process]
    ]
else :
    backgrounds = args.data 

print('[+] signal events read from \n', signals)
print('[+] data events read from \n', backgrounds)

tree_name = 'tree_w_BDT'
bdt_score = 'bdt_score' if not args.isMulticlass else 'bdt_score_t3m'

sig_rdf = ROOT.RDataFrame(tree_name, signals).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
if(args.debug):print(bkg)
    
##             ##
#    PLOTTING   #
##             ##
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.035)
CMS.SetExtraText("Preliminary")
CMS.SetLumi(f'{args.year}, {cfg.LumiVal_plots[args.year]}')
CMS.SetEnergy(13.6)

observables = cfg.features + ['tau_fit_eta', 'tauEta', bdt_score, 'tau_fit_mass', 'tau_mu12_fitM', 'tau_mu23_fitM', 'tau_mu13_fitM']

#c = ROOT.TCanvas('c', '', 800,800)
#c_cut = ROOT.TCanvas('c_cut', '', 800,800)
legend = ROOT.TLegend(0.55, 0.70, 0.85, 0.85)
legend_cut = ROOT.TLegend(0.40, 0.75, 0.85, 0.85)
for i,obs in enumerate(observables):
    ### signal MC
    h_sig     = sig_rdf.Histo1D(('h_sig_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
    h_sig.Scale(1./h_sig.Integral())
    #  after BDT selection
    sig_amplify = None
    if    args.process == 'Tau3Mu' : sig_amplify = 10.0
    elif  args.process == 'ZTau3Mu': sig_amplify = 20.0
    
    h_sig_cut = sig_rdf.Filter('%s>%f'%( bdt_score, args.bdt_cut)).Histo1D(('h_sig_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs, 'weight').GetPtr()
    if sig_amplify : h_sig_cut.Scale(sig_amplify)
    ### background
    h_bkg = bkg_rdf.Histo1D(('h_bkg_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
    h_bkg.Scale(1./h_bkg.Integral())
    #   after BDT cut
    h_bkg_cut = bkg_rdf.Filter('%s>%f'%( bdt_score, args.bdt_cut)).Histo1D(('h_bkg_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
    #h_bkg_cut.Scale(1./h_bkg.Integral())
    
    # inputs 
    h_bkg.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3]) 
    h_bkg.SetLineColor(ROOT.kBlue)
    h_bkg.SetLineWidth(3)
    h_bkg.SetFillColor(ROOT.kBlue)
    h_bkg.SetFillStyle(3004)
    h_bkg.SetMaximum(1.4*max(h_bkg.GetMaximum(),h_sig.GetMaximum()))
    h_sig.SetLineColor(cfg.color_process[args.process])
    h_sig.SetLineWidth(3)
    h_sig.SetMarkerStyle(0)
    h_sig.SetFillColor(cfg.color_process[args.process])
    h_sig.SetFillStyle(3004)
    # after BDT cut
    h_sig_cut.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3]) 
    h_bkg_cut.SetLineColor(ROOT.kBlack)
    h_bkg_cut.SetLineWidth(3)
    h_bkg_cut.SetMarkerStyle(20)
    h_sig_cut.SetMaximum(2.0*max(h_bkg_cut.GetMaximum(),h_sig_cut.GetMaximum()))
    h_sig_cut.SetLineColor(cfg.color_process[args.process])
    h_sig_cut.SetLineWidth(3)
    h_sig_cut.SetFillColor(cfg.color_process[args.process])
    h_sig_cut.SetFillStyle(3004)

    if(i == 0):
        legend.AddEntry(h_bkg, 'data sidebands', 'f')
        legend_cut.AddEntry(h_bkg_cut, 'data sidebands (BDT>%.4f)'%args.bdt_cut, 'p')
        legend.AddEntry(h_sig, f'{cfg.legend_process[args.process]} MC', 'f')
        legend_cut.AddEntry(h_sig_cut, f'{cfg.legend_process[args.process]} MC' + (f' #times {sig_amplify:.1f} ' if sig_amplify else '') +  f'(BDT>{args.bdt_cut:.3f})', 'f')

    c = CMS.cmsCanvas(f'c_{obs}', 
        cfg.features_NbinsXloXhiLabelLog[obs][1], 
        cfg.features_NbinsXloXhiLabelLog[obs][2], 
        max(min(h_bkg.GetMinimum(),h_sig.GetMinimum()), 1e-4) if cfg.features_NbinsXloXhiLabelLog[obs][4] else 0.0,
        1.4*max(h_bkg.GetMaximum(),h_sig.GetMaximum()), 
        cfg.features_NbinsXloXhiLabelLog[obs][3], 
        'Events', 
        square = CMS.kSquare, 
        extraSpace=0.02, 
        iPos=11
    ) 
    c.cd()
    c.SetLogy(cfg.features_NbinsXloXhiLabelLog[obs][4])
    CMS.cmsDraw(h_bkg, 
        'hist',
        lwidth = 2,
        marker = h_bkg.GetMarkerStyle(),
        mcolor = h_bkg.GetLineColor(), 
        fcolor = h_bkg.GetFillColor(),
        fstyle = h_bkg.GetFillStyle(), 
    )
    CMS.cmsDraw(h_sig, 
        'hist same',
        lwidth = 2,
        marker = h_sig.GetMarkerStyle(),
        mcolor = h_sig.GetLineColor(), 
        fcolor = h_sig.GetFillColor(),
        fstyle = h_sig.GetFillStyle(), 
    )
    legend.Draw()
    #ROOT.gPad.RedrawAxis()
    plot_name = '%s/BDTinput_%s'%(args.plot_outdir,obs)
    c.SaveAs(plot_name+'.png')
    c.SaveAs(plot_name+'.pdf')

    c_cut = CMS.cmsCanvas(f'c_cut_{obs}', 
        cfg.features_NbinsXloXhiLabelLog[obs][1], 
        cfg.features_NbinsXloXhiLabelLog[obs][2], 
        max(min(h_bkg.GetMinimum(),h_sig.GetMinimum()), 1e-4) if cfg.features_NbinsXloXhiLabelLog[obs][4] else 0.0,
        h_sig_cut.GetMaximum(), 
        cfg.features_NbinsXloXhiLabelLog[obs][3], 
        'Events', 
        square = CMS.kSquare, 
        extraSpace=0.02, 
        iPos=11
    ) 
    c_cut.cd()
    c_cut.SetLogy(cfg.features_NbinsXloXhiLabelLog[obs][4])
    CMS.cmsDraw(h_sig_cut, 
        'hist',
        lwidth = 2,
        marker = h_sig_cut.GetMarkerStyle(),
        mcolor = h_sig_cut.GetLineColor(), 
        fcolor = h_sig_cut.GetFillColor(),
        fstyle = h_sig_cut.GetFillStyle(), 
    )
    CMS.cmsDraw(h_bkg_cut, 
        'pe same',
        lwidth = 2,
        marker = h_bkg_cut.GetMarkerStyle(),
        mcolor = h_bkg_cut.GetLineColor(), 
        fcolor = h_bkg_cut.GetFillColor(),
        fstyle = h_bkg_cut.GetFillStyle(), 
    )
    c_cut.SetLogy(cfg.features_NbinsXloXhiLabelLog[obs][4])
    #h_sig_cut.Draw('hist')
    #h_bkg_cut.Draw('pe same')
    legend_cut.Draw()
    ROOT.gPad.RedrawAxis()
    plot_name = '%s/BDTcut0p%d_%s'%(args.plot_outdir, args.bdt_cut*10000,obs)
    c_cut.SaveAs(plot_name+'.png')
    c_cut.SaveAs(plot_name+'.pdf')

