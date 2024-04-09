import ROOT
import argparse
import pickle
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
from config import * 


parser = argparse.ArgumentParser()
#parser.add_argument('--load_model', help='load pkl instead of training')
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/', help=' output directory for plots')
parser.add_argument('--category'   , help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',        default= 'app_emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
#parser.add_argument('--save_output',action = 'store_true' ,help='set it to save the bdt output')
parser.add_argument('--unblind',    action = 'store_true' ,help='set it to unblind the data')

args = parser.parse_args()
tag = args.tag

 # ------------ APPLY SELECTIONS ------------ # 
base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f )'%(mass_range_lo,mass_range_hi) +( '& ' + cat_selection_dict[args.category] if (args.category) else '') 
sig_selection  = base_selection 
bkg_selection  = base_selection + ('& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(blind_range_lo, blind_range_hi) if not (args.unblind) else '')

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

tag += '_cat%s_%s'%(args.category if (args.category) else 'ABC', 'open' if (args.unblind) else 'blind')

#  ------------ PICK SIGNAL & BACKGROUND -------------- #

signals     = [
    '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2_EFG_fullinput.root'
]

backgrounds  = [
    '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2_EFG_fullinput_blind.root'
]

tree_name = 'tree_w_BDT'

branches_to_read = branches + ['bdt','weight']
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches_to_read).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds, branches).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
if(args.debug):print(bkg)

#  ------------ MERGE IN 1 DATASET -------------- #
data = pd.concat([sig, bkg])
data = data.sample(frac = 1, random_state = 1986).reset_index(drop=True)
check_for_nan = data.isnull().values.any()
print ("check for NaN " + str(check_for_nan))
if (check_for_nan):
    data = data.dropna()
    check_for_nan = data.isnull().values.any()
    print ("check again for NaN " + str(check_for_nan))

##                             ##
#---------- ROC CURVE ----------#
##                             ##
cuts_to_display = [0.600, 0.990, 0.995, 0.998]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
plt.plot(xy, xy, color='grey', linestyle='--')
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.xscale('log')

fpr, tpr, wps = roc_curve(data.target, data.bdt, sample_weight=data.weight)
plt.plot(fpr, tpr, label='test sample', color='b')

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]))

print ('ROC AUC full-dataset ', roc_auc_score(data.target, data.bdt, sample_weight=data.weight))
#print ('ROC AUC test  ', roc_auc_score(test.target , test.bdt , sample_weight=test.weight))

plt.legend(loc='best')
plt.grid()
plt.title('ROC')
plt.tight_layout()
plt.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
plt.clf()

##                                      ##
#---------- CORRELATION MATRIX ----------#
##                                      ##
# Compute the correlation matrix for the signal
corr = sig[features + ['tauEta','bdt', 'tau_fit_mass']].corr()
print(corr)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0},  annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical')
g.set_yticklabels(labels.values(), rotation='horizontal')

# plt.show()
plt.title('linear correlation matrix - signal', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_sig_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_sig_%s.pdf' %(args.plot_outdir, tag))
plt.clf()

# Compute the correlation matrix for the signal
corr = bkg[features + ['tauEta','bdt', 'tau_fit_mass']].corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0}, annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical')
g.set_yticklabels(labels.values(), rotation='horizontal')

# plt.show()
plt.title('linear correlation matrix - background', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_bkg_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_bkg_%s.pdf' %(args.plot_outdir, tag))
