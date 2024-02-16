import ROOT 
ROOT.EnableImplicitMT()
import argparse
import datetime 
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
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# from my config
from config import * 

##########################################################################################
# Define the gini metric - from https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703#5897

##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--load_model', help='load pkl instead of training')
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--save_output',action = 'store_true' ,help='set it to save the bdt output')
parser.add_argument('--isDsPhiPi',  action = 'store_true' ,help='set apply BDT to control channel')
parser.add_argument('-s', '--signal',   action = 'append',                                           help='file with signal events with BDT applied')
parser.add_argument('-d', '--data',     action = 'append',                                           help='file with data events with BDT applied')

args = parser.parse_args()
tag = args.tag 
removeNaN = False 

 # ------------ DEFINE SELECTIONS ------------ # 
if(args.isDsPhiPi):
    base_selection = '&'.join([
                            '(Ds_fit_mass > %.2f & Ds_fit_mass < %.2f )'%(Ds_mass_range_lo,Ds_mass_range_hi),
                            '(Ds_Lxy_sign_BS > 5.0)',
                            '(Ds_fit_vprob > 0.01)',
                            '(phi_fit_mass > 0.98 & phi_fit_mass < 1.05)'
                        ])
else:
    base_selection = '' 
sig_selection  = base_selection 
bkg_selection  = base_selection

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)
print('---------------------------------------------')

 # ------------ INPUT DATASET ------------ # 

if(args.signal is None):
    signals     = [
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022preEE_HLT_Tau3Mu.root', 
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022EE_HLT_Tau3Mu.root']
else:
    signals = args.signal 
if(args.data is None):
    backgrounds  = [
        ''
    ]
else:
    backgrounds = args.data

tree_name = 'Tau3Mu_HLTemul_tree'
if(args.isDsPhiPi): tree_name = 'DsPhiMuMuPi_tree'

# MC dataframe
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection).Define('weight', 'lumi_factor')
sig = pd.DataFrame( sig_rdf.AsNumpy() )
#bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds, branches).Filter(bkg_selection).Define('weight', '1')
#bkg = pd.DataFrame( bkg_rdf.AsNumpy() )

print('... processing input ...')
print(' SIGNAL : %s entries passed the selection' %sig_rdf.Count().GetValue())
#print(' BACKGROUND : %s entries passed the selection' %bkg_rdf.Count().GetValue())
print('---------------------------------------------')

## DEFINE TARGETS
#sig.loc[:,'target'] = np.ones (sig.shape[0]).astype(int)
#bkg.loc[:,'target'] = np.zeros(bkg.shape[0]).astype(int)

## ETA BINS
bdt_inputs = features + ['tauEta']
if(args.isDsPhiPi): 
    if(args.debug): print(features_DsPhiPi_to_Tau3Mu)
    sig.rename( columns= features_DsPhiPi_to_Tau3Mu, inplace=True) 
    #bkg.rename( columns= features_DsPhiPi_to_Tau3Mu, inplace=True) 
    sig.loc[:,'tauEta'] = tauEta(sig['Ds_fit_eta'])
    #bkg.loc[:,'tauEta'] = tauEta(bkg['Ds_fit_eta'])
else:
    sig.loc[:,'tauEta'] = tauEta(sig['tau_fit_eta'])
    #bkg.loc[:,'tauEta'] = tauEta(bkg['tau_fit_eta'])

if(args.debug):print(sig.columns)
#if(args.debug):print(bkg)


## CONCATENATE & SHUFFLE SIGNAL AND BACKGROUND
data = pd.concat([sig])#, bkg])
if(args.debug) : print(data)
data = data.sample(frac = 1, random_state = 3872).reset_index(drop=True)

## REMOVE NaN
if(removeNaN):
    check_for_nan = data.isnull().values.any()
    print ("[!] check for NaN " + str(check_for_nan))
    if (check_for_nan):
        data = data.dropna()
        check_for_nan = data.isnull().values.any()
        print ("[!] check again for NaN " + str(check_for_nan))

###                ###
#  LOAD BDT weights  #
###                ###

classifier_file = args.load_model 
print('[+] load model from %s'%classifier_file)
with open(classifier_file, 'rb') as f:
    classifiers = pickle.load(f)

n_class = len(classifiers)
print("    Number of splits %d"%n_class)

sig['bdt_score'] =  np.zeros(sig.shape[0])
for i, iclas in classifiers.items():
    print (' evaluating %d/%d classifier' %(i+1, n_class))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))
    sig.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(sig[bdt_inputs])[:, 1]
    sig.loc[:,'bdt_score'] += iclas.predict_proba(sig[bdt_inputs])[:, 1] / n_class

newfile = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_MC' if args.isDsPhiPi else 'WTau3Mu_'
newfile += 'kFold_2024Feb02.root' 
print('[OUT] MC output file saved in %s'%newfile)
sig_out_data = {col: sig[col].values for col in sig.columns}
sig_out_rdf = ROOT.RDF.MakeNumpyDataFrame(sig_out_data).Snapshot('DsPhiMuMuPi_tree', newfile)

###
