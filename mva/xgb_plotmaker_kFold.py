import ROOT
import argparse
import pickle
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
#from config import * 
import config

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/', help=' output directory for plots')
parser.add_argument('--category'   ,                                                                 help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',            default= 'app_emulateRun2',                                  help='tag to the training')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                                help='set random state for reproducible results')
parser.add_argument('--debug',          action = 'store_true' ,                                      help='set it to have useful printout')
parser.add_argument('--training_plots', action = 'store_true' ,                                      help='set it to produce also training/test plots')
parser.add_argument('--load_model',                                                                  help='load pkl instead of training')
parser.add_argument('-s', '--signal',   action = 'append',                                           help='file with signal events with BDT applied')
parser.add_argument('-d', '--data',     action = 'append',                                           help='file with data events with BDT applied')

args = parser.parse_args()
tag = args.tag
removeNaN = False 

 # ------------ APPLY SELECTIONS ------------ # 
base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f ) & (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu) & (tau_Lxy_sign_BS > %.2f)'%(config.mass_range_lo,config.mass_range_hi, args.LxySign_cut) 
sig_selection  = base_selection 
bkg_selection  = base_selection + '& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(config.blind_range_lo, config.blind_range_hi) 

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

#  ------------ PICK SIGNAL & BACKGROUND -------------- #
if(args.signal is None):
    signals     = [
        '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_reMini22_23_kFold_2024Feb02.root',
    ]
else :
    signals = args.signal 
if(args.data is None):
    backgrounds  = [
        '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_reMini22_23_kFold_2024Feb02_blind.root',
    ]
else :
    backgrounds = args.data 

print('[+] signal events read from \n', signals)
print('[+] data events read from \n', backgrounds)

tree_name = 'tree_w_BDT'

sig_rdf = ROOT.RDataFrame(tree_name, signals).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
if(args.debug):print(bkg)
#  ------------ MERGE IN 1 DATASET -------------- #
data = pd.concat([sig, bkg])
data = data.sample(frac = 1, random_state = 1986).reset_index(drop=True)
if (removeNaN) :
    check_for_nan = data.isnull().values.any()
    print ("check for NaN " + str(check_for_nan))
    if (check_for_nan):
        data = data.dropna()
        check_for_nan = data.isnull().values.any()
        print ("check again for NaN " + str(check_for_nan))
    
##             ##
#    PLOTTING   #
##             ##
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(1)
ROOT.gStyle.SetPadTickX(1)

plot_data = data[(data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < config.blind_range_lo) | (data.tau_fit_mass > config.blind_range_hi)))]

# ------------ BDT VS MASS ------------ # 
bdt_th = 0.5 

h_BDTmass = bkg_rdf.Histo2D(('h_BDTmass', 'bdt score in data vs reco tau candidate mass', 50, bdt_th , 1.0, 40, config.mass_range_lo, config.mass_range_hi), 'bdt_score', 'tau_fit_mass')
c = ROOT.TCanvas('c1', '', 800,800)
h_BDTmass.Draw('colz')
h_BDTmass.GetXaxis().SetTitle('BDT score')
h_BDTmass.GetXaxis().SetTitleSize(0.35)
h_BDTmass.GetYaxis().SetTitle('M 3#mu (GeV)')
h_BDTmass.GetYaxis().SetTitleSize(0.35)

currentPlot_name = '%sBDTvsMtau_data_%s' %(args.plot_outdir,tag)

c.SaveAs(currentPlot_name+'.png')
c.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs Mtau in %s.png(pdf) '%currentPlot_name)


# ------------ BDT SCORE ACROSS kFOLDs ------------ # 
ROOT.gStyle.SetPalette(ROOT.kCMYK)
kFold = 5
h_BDTfold_data  = []
h_BDTfold_signal = []
for i in range(kFold):
    h_BDTfold_data.append(bkg_rdf.Filter('bdt_to_apply==%d'%i).Histo1D(('h_BDTfold_data_%d'%i, 'bdt score in data n fold %d'%i, 50, 0.0, 1.0), 'bdt_score'))
    h_BDTfold_signal.append(sig_rdf.Filter('bdt_to_apply==%d'%i).Histo1D(('h_BDTfold_signal_%d'%i, 'bdt score in MC in fold %d'%i, 50, 0.0, 1.0), 'bdt_score'))

h_BDTfold_data[0].GetXaxis().SetTitle('BDT score')
h_BDTfold_data[0].GetXaxis().SetTitleSize(0.35)
h_BDTfold_signal[0].GetXaxis().SetTitle('BDT score')
h_BDTfold_signal[0].GetXaxis().SetTitleSize(0.35)

c_dat  = ROOT.TCanvas('c_dat', '', 800,800)
legend_dat = ROOT.TLegend(0.6, 0.6, 0.80, 0.85)
c_sig  = ROOT.TCanvas('c_sig', '', 800,800)
legend_sig = ROOT.TLegend( 0.15, 0.6, 0.35, 0.85)
for i in range(kFold):
    c_dat.cd()
    h_BDTfold_data[i].Scale(1./h_BDTfold_data[i].GetEntries())
    h_BDTfold_data[i].SetLineWidth(2)
    h_BDTfold_data[i].Draw('same hist plc')
    legend_dat.AddEntry('h_BDTfold_data_%d'%i, 'fold %d'%i,'f')
    c_sig.cd()
    h_BDTfold_signal[i].Scale(1./h_BDTfold_signal[i].GetEntries())
    h_BDTfold_signal[i].SetLineWidth(2)
    h_BDTfold_signal[i].Draw('same hist plc')
    legend_sig.AddEntry('h_BDTfold_signal_%d'%i, 'fold %d'%i, 'f')

currentPlot_name = '%sBDTvsFolds_data_%s' %(args.plot_outdir,tag)
c_dat.SetLogy(1)
c_dat.cd()
legend_dat.Draw()
c_dat.SaveAs(currentPlot_name+'.png')
c_dat.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT score vs folds in %s.png(pdf) '%currentPlot_name)
    
currentPlot_name = '%sBDTvsFolds_signal_%s' %(args.plot_outdir,tag)
c_sig.SetLogy(1)
c_sig.cd()
legend_sig.Draw()
c_sig.SaveAs(currentPlot_name+'.png')
c_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT score vs folds in %s.png(pdf) '%currentPlot_name)


# ------------ EFFICIENCY vs Mtau ------------ # 

bdt_cuts = [0.300, 0.600, 0.800, 0.900, 0.950, 0.990, 0.995]
h_bdt0_sig = sig_rdf.Histo1D(('h_bdt0_sig', '', 40,config.mass_range_lo,config.mass_range_hi), 'tau_fit_mass').GetPtr()
h_bdt0_sig.Sumw2()
h_bdt0_bkg = bkg_rdf.Histo1D(('h_bdt0_bkg', '', 40,config.mass_range_lo,config.mass_range_hi), 'tau_fit_mass').GetPtr()
h_bdt0_bkg.Sumw2()
h_bdtSel_sig = []
h_bdtSel_bkg = []
for cut in bdt_cuts:
    h_bdtSel_sig.append( sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_bdtSel%d_sig'%cut*1000, '', 40,config.mass_range_lo,config.mass_range_hi), 'tau_fit_mass').GetPtr() )
    h_bdtSel_bkg.append( bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_bdtSel%d_bkg'%cut*1000, '', 40,config.mass_range_lo,config.mass_range_hi), 'tau_fit_mass').GetPtr() )


c2_sig = ROOT.TCanvas('c2_sig', '', 1000,800)
ROOT.gPad.SetMargin(0.1, 0.2, 0.1,0.1)
c2_bkg = ROOT.TCanvas('c2_bkg', '', 1000,800)
ROOT.gPad.SetMargin(0.1, 0.2, 0.1,0.1)
legend = ROOT.TLegend(0.8, 0.5, 0.99,0.99)
h_bdtSel_sig[0].GetXaxis().SetTitle('M(3 #mu) (GeV)')
h_bdtSel_bkg[0].GetXaxis().SetTitle('M(3 #mu) (GeV)')
h_bdtSel_sig[0].GetYaxis().SetTitle('efficiency')
h_bdtSel_bkg[0].GetYaxis().SetTitle('efficiency')
h_bdtSel_sig[0].GetYaxis().SetRangeUser(0.0, 1.5)
h_bdtSel_bkg[0].GetYaxis().SetRangeUser(0.0001, 0.25)
for i in range(len(bdt_cuts)) :
    h_bdtSel_sig[i].Sumw2()
    h_bdtSel_bkg[i].Sumw2()
    h_bdtSel_sig[i].Divide(h_bdt0_sig)
    h_bdtSel_bkg[i].Divide(h_bdt0_bkg)
    h_bdtSel_sig[i].SetLineWidth(2)
    h_bdtSel_bkg[i].SetLineWidth(2)
    legend.AddEntry(h_bdtSel_sig[i], 'BDT > %.3f'%bdt_cuts[i])
    c2_sig.cd()
    h_bdtSel_sig[i].Draw('EP same plc')
    c2_bkg.cd()
    h_bdtSel_bkg[i].Draw('EP same plc')

currentPlot_name = '%sBDTeffvsMtau_signal_%s' %(args.plot_outdir,tag)
c2_sig.cd()
legend.Draw()
c2_sig.SaveAs(currentPlot_name+'.png')
c2_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)
currentPlot_name = '%sBDTeffvsMtau_sidebands_%s' %(args.plot_outdir,tag)
c2_bkg.cd()
c2_bkg.SetLogy(1)
legend.Draw()
c2_bkg.SaveAs(currentPlot_name+'.png')
c2_bkg.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)

# ------------ BDT score vs TAU CHARGE ------------ # 
# signal
h_bdt_chp1_sig = sig_rdf.Filter('tau_fit_charge==1').Histo1D(('h_bdt_chp1_sig', '', 50, 0.0, 1.0), 'bdt_score', 'train_weight').GetPtr()
h_bdt_chp1_sig.Scale(1./sig_rdf.Count().GetValue())
h_bdt_chm1_sig = sig_rdf.Filter('tau_fit_charge==-1').Histo1D(('h_bdt_chm1_sig', '', 50, 0.0, 1.0), 'bdt_score', 'train_weight').GetPtr()
h_bdt_chm1_sig.Scale(1./sig_rdf.Count().GetValue())

c3_sig = ROOT.TCanvas('c3_sig', '', 1000, 800)
leg_sig = ROOT.TLegend(0.15, 0.75, 0.4, 0.85)

h_bdt_chp1_sig.SetLineColor(ROOT.kGreen + 2)
h_bdt_chp1_sig.SetFillColor(ROOT.kGreen + 2)
h_bdt_chp1_sig.SetFillStyle(3004)
h_bdt_chp1_sig.GetXaxis().SetTitle('BDT score')
leg_sig.AddEntry(h_bdt_chp1_sig, 'q(3 #mu) = +1')
h_bdt_chm1_sig.SetLineColor(ROOT.kOrange + 2)
h_bdt_chm1_sig.SetFillColor(ROOT.kOrange + 2)
h_bdt_chm1_sig.SetFillStyle(3004)
leg_sig.AddEntry(h_bdt_chm1_sig, 'q(3 #mu) = -1')

c3_sig.cd()
h_bdt_chp1_sig.Draw('hist')
h_bdt_chm1_sig.Draw('hist same')
currentPlot_name = '%sBDTvsTauCharge_signal_%s' %(args.plot_outdir,tag)
c3_sig.cd()
c3_sig.SetLogy(1)
leg_sig.Draw()
c3_sig.SaveAs(currentPlot_name+'.png')
c3_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs tau charge in %s.png(pdf) '%currentPlot_name)

# background

h_bdt_chp1_bkg = bkg_rdf.Filter('tau_fit_charge==1').Histo1D(('h_bdt_chp1_bkg', '', 50, 0.0, 1.0), 'bdt_score', 'train_weight').GetPtr()
h_bdt_chp1_bkg.Scale(1./bkg_rdf.Count().GetValue())
h_bdt_chm1_bkg = bkg_rdf.Filter('tau_fit_charge==-1').Histo1D(('h_bdt_chm1_bkg', '', 50, 0.0, 1.0), 'bdt_score', 'train_weight').GetPtr()
h_bdt_chm1_bkg.Scale(1./bkg_rdf.Count().GetValue())

c3_bkg = ROOT.TCanvas('c3_bkg', '', 1000, 800)
leg_bkg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
h_bdt_chp1_bkg.SetLineColor(ROOT.kGreen + 2)
h_bdt_chp1_bkg.SetFillColor(ROOT.kGreen + 2)
h_bdt_chp1_bkg.SetFillStyle(3004)
h_bdt_chp1_bkg.GetXaxis().SetTitle('BDT score')
leg_bkg.AddEntry(h_bdt_chp1_bkg, 'q(3 #mu) = +1')
h_bdt_chm1_bkg.SetLineColor(ROOT.kOrange + 2)
h_bdt_chm1_bkg.SetFillColor(ROOT.kOrange + 2)
h_bdt_chm1_bkg.SetFillStyle(3004)
leg_bkg.AddEntry(h_bdt_chm1_bkg, 'q(3 #mu) = -1')

c3_bkg.cd()
h_bdt_chp1_bkg.Draw('hist')
h_bdt_chm1_bkg.Draw('hist same')
currentPlot_name = '%sBDTvsTauCharge_data_%s' %(args.plot_outdir,tag)
c3_bkg.cd()
c3_bkg.SetLogy(1)
leg_bkg.Draw()
c3_bkg.SaveAs(currentPlot_name+'.png')
c3_bkg.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs tau charge in %s.png(pdf) '%currentPlot_name)

# ------------ DISPLACEMENT ------------ # 
cut = 0.995
c4 = ROOT.TCanvas('c4', '', 800, 800)
h_LxyVal_sig = sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxyVal%d_sig', '', 40, 0, 2), 'tau_Lxy_val_BS').GetPtr()
h_LxyVal_sig.SetLineColor(ROOT.kRed)
h_LxyVal_sig.SetFillColor(ROOT.kRed)
h_LxyVal_sig.SetFillStyle(3004)
h_LxyVal_sig.Scale(10*sig_rdf.Mean('weight').GetValue())
h_LxyVal_bkg = bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxyVal%d_bkg', '', 40, 0, 2), 'tau_Lxy_val_BS').GetPtr()
h_LxyVal_bkg.GetXaxis().SetTitle('L_{xy} (cm)')
h_LxyVal_bkg.SetLineColor(ROOT.kBlue)
h_LxyVal_bkg.SetFillColor(ROOT.kBlue)
h_LxyVal_bkg.SetFillStyle(3004)

c4.cd()
h_LxyVal_bkg.Draw('hist')
h_LxyVal_sig.Draw('hist same')
currentPlot_name = '%sSVdisplacement_value_BDT0p%d%s' %(args.plot_outdir, cut*1000,tag)
c4.SaveAs(currentPlot_name+'.png')
c4.SaveAs(currentPlot_name+'.pdf')


h_LxySig_sig = sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxySig%d_sig', '', 40, 0,10), 'tau_Lxy_sign_BS').GetPtr()
h_LxySig_sig.SetLineColor(ROOT.kRed)
h_LxySig_sig.SetFillColor(ROOT.kRed)
h_LxySig_sig.SetFillStyle(3004)
h_LxySig_sig.Scale(10*sig_rdf.Mean('weight').GetValue())
h_LxySig_bkg = bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxySig%d_bkg', '', 40, 0,10), 'tau_Lxy_sign_BS').GetPtr()
h_LxySig_bkg.GetXaxis().SetTitle('L_{xy}/#sigma')
h_LxySig_bkg.SetLineColor(ROOT.kBlue)
h_LxySig_bkg.SetFillColor(ROOT.kBlue)
h_LxySig_bkg.SetFillStyle(3004)

c4.cd()
h_LxySig_bkg.Draw('hist')
h_LxySig_sig.Draw('hist same')
currentPlot_name = '%sSVdisplacement_significance_BDT0p%d%s' %(args.plot_outdir, cut*1000,tag)
c4.SaveAs(currentPlot_name+'.png')
c4.SaveAs(currentPlot_name+'.pdf')

# ------------ ROC CURVE inclusive ------------ # 
cuts_to_display = [0.600, 0.990, 0.995, 0.998]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
fig = plt.figure(figsize = (8,6))
plt.plot(xy, xy, color='grey', linestyle='--', linewidth=3)
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('background efficiency $\\epsilon_{B}$', fontsize = 18)
plt.xticks(fontsize=16)
plt.ylabel('signal efficiency $\\epsilon_{S}$', fontsize = 18)
plt.yticks(fontsize=16)
plt.xscale('log')

# analysis set
fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_score, sample_weight=plot_data.train_weight)
plt.plot(fpr, tpr, label='analysis set', color='b', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
plt.scatter(wp_x, wp_y)

# train set
fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_training, sample_weight=plot_data.train_weight)
plt.plot(fpr, tpr, label='train set', color='r', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]), horizontalalignment='left')

print ('ROC AUC train ', roc_auc_score(plot_data.target,  plot_data.bdt_training, sample_weight=plot_data.train_weight))
print ('ROC AUC test  ', roc_auc_score(plot_data.target , plot_data.bdt_score , sample_weight=plot_data.train_weight))

plt.legend(loc='best', fontsize='18')
plt.grid()
plt.tight_layout()
plt.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
print('[=] save inclusive  ROC curve %sroc_%s'%(args.plot_outdir, tag))

# ------------ ROC CURVE by category ------------ # 

fig = plt.figure(figsize = (8,6))
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('background efficiency $\\epsilon_{B}$', fontsize = 18)
plt.xticks(fontsize=16)
plt.ylabel('signal efficiency $\\epsilon_{S}$', fontsize = 18)
plt.yticks(fontsize=16)
plt.xscale('log')

eta_limit_category = {
    'A' : [0.0,   eta_thAB],
    'B' : [eta_thAB, eta_thBC],
    'C' : [eta_thBC, 3.5]
}

for cat in ['A', 'B', 'C']:
    #data_cat = plot_data.loc[(plot_data['tau_fit_mass_err']/plot_data['tau_fit_mass'] > resol_limit_category[cat][0]) & (plot_data['tau_fit_mass_err']/plot_data['tau_fit_mass'] < resol_limit_category[cat][1])]
    data_cat = plot_data.loc[(np.abs(plot_data['tau_fit_eta']) > eta_limit_category[cat][0]) & (np.abs(plot_data['tau_fit_eta']) < eta_limit_category[cat][1])]
    fpr, tpr, wps = roc_curve(data_cat.target, data_cat.bdt_score, sample_weight=data_cat.train_weight)
    auc = roc_auc_score(data_cat.target,  data_cat.bdt_training, sample_weight=data_cat.train_weight)
    plt.plot(fpr, tpr, label='category %s AUC= %.3f'%(cat, auc), linewidth=2)
    
    wp_x = []
    wp_y = []
    for icut in cuts_to_display:
        idx = (wps>icut).sum()
        wp_x.append(fpr[idx])
        wp_y.append(tpr[idx])
    #plt.scatter(wp_x, wp_y)
    #for i, note in enumerate(cuts_to_display):
    #    plt.annotate(note, (wp_x[i], wp_y[i]), horizontalalignment='left')
    
plt.legend(loc='best', fontsize='18')
plt.grid()
plt.tight_layout()
plt.savefig('%sROCbyCategory_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sROCbyCategory_%s.pdf' %(args.plot_outdir,tag))
print('[=] save ROC by category curve %sroc_%s'%(args.plot_outdir, tag))

# ------------ CORRELATION MATRIX ------------ # 
# Compute the correlation matrix for the signal
corr = sig[features + ['tauEta','bdt_score', 'tau_fit_mass']].corr()
print(corr)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0},  annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical', fontsize = 16)
g.set_yticklabels(labels.values(), rotation='horizontal', fontsize = 16)

# plt.show()
plt.title('linear correlation matrix - signal', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_sig_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_sig_%s.pdf' %(args.plot_outdir, tag))
print('[=] save signal correlation in %scorr_sig_%s'%(args.plot_outdir, tag))
plt.clf()

# Compute the correlation matrix for the signal
corr = bkg[features + ['tauEta','bdt_score', 'tau_fit_mass']].corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0}, annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical', fontsize = 16)
g.set_yticklabels(labels.values(), rotation='horizontal', fontsize = 16)

# plt.show()
plt.title('linear correlation matrix - background', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_bkg_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_bkg_%s.pdf' %(args.plot_outdir, tag))
print('[=] save background correlation in %scorr_bkg_%s'%(args.plot_outdir, tag))

if not args.training_plots : exit()

# load model for feature importance
if not args.load_model:
    print('[ERROR] you have to specify a the model to load to make plots')
    exit()
else :
    print('[+] load model from %s'%args.load_model)
    with open(args.load_model, 'rb') as f:
        classifiers = pickle.load(f)


# ------------ OVERTRAINING TEST ------------ # 
train_sig = plot_data[plot_data.target==1].bdt_training
train_bkg = plot_data[plot_data.target==0].bdt_training

test_sig = plot_data[plot_data.target==1].bdt_score  
test_bkg = plot_data[plot_data.target==0].bdt_score  

low  = 0
high = 1
low_high = (low,high)
bins = 40
binning = np.linspace(low, high, bins)

# SIGNAL

fig, (ax, rax)  = plt.subplots(2, 1, figsize=(8, 10), tight_layout = True)
hist_test_sig   = ax.hist(test_sig, bins = binning, density = False)
err_test_sig    = np.sqrt(hist_test_sig[0])
hist_test_bkg   = ax.hist(test_bkg, bins = binning, density = False) 
err_test_bkg    = np.sqrt(hist_test_sig[0])
plt.clf()
fig, (ax, rax) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [3, 1]}, tight_layout = True)

hist_train_sig = ax.hist(train_sig, bins = binning, alpha = 0.5, color = 'r', label = 'signal MC (train)')
ax.errorbar((binning[:-1]+binning[1:])/2, hist_test_sig[0], yerr = err_test_sig, fmt = 'ro', ls='none', label = 'signal MC (test)')
hist_train_bkg = ax.hist(train_bkg, bins = binning, alpha = 0.5, color = 'b', label = 'data SB (train)')
ax.errorbar((binning[:-1]+binning[1:])/2, hist_test_bkg[0], yerr = err_test_bkg, fmt = 'bo', ls='none', label = 'data SB (test)')
#ratio
ratio_sig     = hist_test_sig[0]/hist_train_sig[0]
err_ratio_sig = ratio_sig * np.sqrt( 1./hist_test_sig[0] + 1./ hist_train_sig[0]) 
rax.errorbar((binning[:-1]+binning[1:])/2, ratio_sig, yerr = err_ratio_sig , fmt = 'ro', ls='none')
ratio_bkg     = hist_test_bkg[0]/hist_train_bkg[0]
err_ratio_bkg = ratio_bkg * np.sqrt( 1./hist_test_bkg[0] + 1./ hist_train_bkg[0]) 
rax.errorbar((binning[:-1]+binning[1:])/2, ratio_bkg, yerr = err_ratio_bkg, fmt = 'bo', ls='none')

rax.set_xlabel('BDT output')
rax.set_ylabel('test / training')
rax.set_ylim(0.75, 2.0)
ax.set_ylabel('Counts')
ax.legend(loc='best')
ax.set_yscale('log')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
#ax.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))
plot_name = '%sovertrain_%s' %(args.plot_outdir,tag)
plt.savefig(f'{plot_name}.png')
plt.savefig(f'{plot_name}.pdf')
print(f'[OUT] saved OVERTRAIN plot in {plot_name}.png/pdf')

plt.clf()

# ------------ FEATURES IMPORTANCE ------------ # 
bdt_inputs = features + ['tauEta']

fscores = OrderedDict(zip(bdt_inputs, np.zeros(len(bdt_inputs))))
for i, iclas in classifiers.items():
    myscores = iclas.get_booster().get_fscore()
    for jj in myscores.keys():
        fscores[jj] += myscores[jj]

totalsplits = sum(float(value) for value in fscores.values())
for k, v in fscores.items():
    fscores[k] = float(v)/float(totalsplits) 

plt.xlabel('relative F-score')
plt.ylabel('feature')

orderedfscores = OrderedDict(sorted(fscores.items(), key=lambda x : x[1], reverse=False ))

bars = [labels[k] for k in orderedfscores.keys()]
y_pos = np.arange(len(bars))
 
# Create horizontal bars
plt.barh(y_pos, orderedfscores.values())
 
# Create names on the y-axis
plt.yticks(y_pos, bars)
plt.tight_layout()
plot_name = '%sfeat_importance_%s' %(args.plot_outdir,tag)
plt.savefig(f'{plot_name}.png')
plt.savefig(f'{plot_name}.pdf')
print(f'[OUT] saved FEATURE IMPRTANCE plot in {plot_name}.png/pdf')
plt.clf()

