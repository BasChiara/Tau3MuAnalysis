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
parser.add_argument('--load_model',                                                                     help='load pkl instead of training')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/',    help=' output directory for plots')
parser.add_argument('--data_outdir',    default= '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/',       help='output directory for ntuples with BDT applied')
parser.add_argument('--tag',            default= 'emulateRun2',                                         help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,                                         help='set it to have useful printout')
parser.add_argument('--save_output',    action = 'store_true' ,                                         help='set it to save the bdt output')
parser.add_argument('--isDsPhiPi',      action = 'store_true' ,                                         help='set apply BDT to control channel')
parser.add_argument('--isFakeRate',     action = 'store_true' ,                                         help='set apply BDT to control channel')
parser.add_argument('--isMC',           action = 'store_true' ,                                         help='set if running on MonteCarlo')
parser.add_argument('-d', '--data',     action = 'append',                                              help='dataset to apply BDT weights')

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
elif (args.isFakeRate):
    base_selection = 'tau_fit_mass > %.2f'%mass_range_lo
else:
    base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f )'%(mass_range_lo,mass_range_hi) 
selection  = base_selection 
data_selection  = base_selection 
bkg_selection  = base_selection

print('[!] base-selection : %s'%base_selection)
print('---------------------------------------------')

 # ------------ INPUT DATASET ------------ # 

if(args.data is None):
    dataset     = [
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022preEE_HLT_Tau3Mu.root', 
    '../outRoot//DsPhiMuMuPi_MCanalyzer_2022EE_HLT_Tau3Mu.root']
else:
    dataset = args.data

tree_name = 'WTau3Mu_tree' if not args.isDsPhiPi else 'DsPhiMuMuPi_tree' 

data_rdf = ROOT.RDataFrame(tree_name, dataset, branches).Filter(data_selection).Define('weight', 'lumi_factor')
dat = pd.DataFrame( data_rdf.AsNumpy() )

print('... processing input ...')
print('[+] input-dataset is %s : %s entries passed the selection' %( 'MC' if args.isMC else 'DATA' ,data_rdf.Count().GetValue()))
print('---------------------------------------------')

## ETA BINS
bdt_inputs = features + ['tauEta']
if(args.isDsPhiPi): 
    if(args.debug): print(features_DsPhiPi_to_Tau3Mu)
    # rename Ds branches to match BDT structure 
    dat.rename( columns= features_DsPhiPi_to_Tau3Mu, inplace=True) 
    dat.loc[:,'tauEta'] = tauEta(dat['Ds_fit_eta'])
else:
    dat.loc[:,'tauEta'] = tauEta(dat['tau_fit_eta'])

if(args.debug):print(dat.columns)

###                ###
#  LOAD BDT weights  #
###                ###

classifier_file = args.load_model 
print('[+] load model from %s'%classifier_file)
with open(classifier_file, 'rb') as f:
    classifiers = pickle.load(f)

n_class = len(classifiers)
print("[BDT] number of splits %d"%n_class)

dat['bdt_score'] =  np.zeros(dat.shape[0])
for i, iclas in classifiers.items():
    print ('[BDT] evaluating %d/%d classifier' %(i+1, n_class))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))

    dat.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 1]
    dat.loc[:,'bdt_score'] += iclas.predict_proba(dat[bdt_inputs])[:, 1] / n_class

newfile_base = '%s/XGBout_'%(args.data_outdir) + ('DsPhiMuMuPi_' if args.isDsPhiPi else 'WTau3Mu_')
newfile_tail = ('MC_' if args.isMC else 'DATA_') + args.tag + ".root"
newfile      = newfile_base + newfile_tail

print('[OUT] output file saved in %s'%newfile)
data_out_rdf = ROOT.RDF.MakeNumpyDataFrame({col: dat[col].values for col in dat.columns}).Snapshot('tree_w_BDT', newfile)
