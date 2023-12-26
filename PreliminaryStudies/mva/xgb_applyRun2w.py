#
# apply Run2 XGB weights 
#
import ROOT 
ROOT.EnableImplicitMT()
import argparse
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
# import matplotlib as mpl ; mpl.use('Agg')
import matplotlib.pyplot as plt
# sns.set(style="whitegrid", font_scale=2)
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance
#from sklearn.preprocessing import LabelEncoder

from sklearn.metrics         import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold

from scipy.stats import ks_2samp

from collections import OrderedDict
from itertools import product

from pdb import set_trace

# from my config
from config import * 

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tag')
parser.add_argument('--Run2', action= 'store_true', help='input ntuples to BDT')
parser.add_argument('--data', action= 'store_true', help='option to apply BDT to data')
parser.add_argument('--load_model', help='XGB model to apply')
parser.add_argument('--convert_features', action = 'store_true', help='if apply BDT to Run3 data convert the features name')

args = parser.parse_args()
tag = args.tag

if args.data:
    signals = ['/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/DoubleMuonLowMass_2017E.root '] if args.Run2 else ['']
else:
    signals = ['/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/WTau3Mu_MC2017.root '] if args.Run2 else ['/afs/cern.ch/user/c/cbasile/CMSSW_12_4_11_patch3-Tau3Mu/src/Tau3MuAnalysis/PreliminaryStudies/outRoot/recoKinematicsT3m_MC_2017_HLT_Tau3Mu.root'] 

tree_name = 'tree' if args.Run2 else 'Tau3Mu_HLTemul_tree'

print(' [+] read tree : %s from file %s'%(tree_name, signals))

input_features = features
input_branches = branches_Run2 if args.Run2 else branches

sig_rdf = ROOT.RDataFrame(tree_name, signals)
print(' [+] Entries : %d'%sig_rdf.Count().GetValue())

sig = pd.DataFrame(sig_rdf.AsNumpy(input_branches))
if (args.Run2):
    sig['tauEta'                                   ] = tauEta(sig['cand_refit_tau_eta'])
    sig['abs(cand_refit_dPhitauMET)'               ] = abs(sig['cand_refit_dPhitauMET'])
    sig['abs(mu1_z-mu2_z)'                         ] = abs(sig['mu1_z']-sig['mu2_z'])
    sig['abs(mu1_z-mu3_z)'                         ] = abs(sig['mu1_z']-sig['mu3_z'])
    sig['abs(mu2_z-mu3_z)'                         ] = abs(sig['mu2_z']-sig['mu3_z'])
    sig['cand_refit_tau_pt*(cand_refit_met_pt**-1)'] = sig['cand_refit_tau_pt']/sig['cand_refit_met_pt']
else:
    sig['tauEta'                                   ] = tauEta(sig['tau_fit_eta'])


sig['target'] = np.ones(sig.shape[0]).astype(int) if not args.data else np.zeros(sig.shape[0]).astype(int) 

if (args.convert_features):
    sig.rename( columns= features_Run2toRun3, inplace=True) 

print(sig)
#exit(-1)
###                  ###
#  LOAD Run2 weights   #
###                  ###

classifier_file = args.load_model 
print('[+] load model from %s'%classifier_file)
with open(classifier_file, 'rb') as f:
    classifiers = pickle.load(f)
n_class = len(classifiers)
print("    Number of splits %d"%n_class)

sig['bdt'] =  np.zeros(sig.shape[0])
for i, iclas in classifiers.items():
    print (' evaluating %d/%d classifier' %(i+1, n_class))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))
    sig.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(sig[input_features])[:, 1]
    sig.loc[:,'bdt'] += iclas.predict_proba(sig[input_features])[:, 1] / n_class

newfile = 'ntuplizerRun2_' if args.Run2 else 'ntuplizerRun3_'
newfile += 'data_' if args.data else 'mc_'
newfile += '_2017wBDT.root'
sig_out_data = {col: sig[col].values for col in sig.columns}
sig_out_rdf = ROOT.RDF.MakeNumpyDataFrame(sig_out_data).Snapshot('tree_w_BDT', newfile)
