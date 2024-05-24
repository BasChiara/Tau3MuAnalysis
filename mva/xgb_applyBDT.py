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
parser.add_argument('--process',        choices= ['WTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'fake_rate'],   help='what process is in the input sample')
parser.add_argument('--isMC',           action = 'store_true' ,                                         help='set if running on MonteCarlo')
parser.add_argument('--isMulticlass',   action = 'store_true' ,                                         help='set if applying a multiclass classifier')
parser.add_argument('--LxySign_cut',    default=  0.05,  type = float,                               help='cut over 3muons SV displacement significance')
parser.add_argument('-d', '--data',     action = 'append',                                              help='dataset to apply BDT weights')

args = parser.parse_args()
tag = '_'.join([args.process, 'MC' if args.isMC else 'DATA']) + ( ('_' + args.tag)  if args.tag else '')
removeNaN = False 

 # ------------ DEFINE SELECTIONS ------------ # 
if(args.process == 'DsPhiMuMuPi'):
    base_selection = '&'.join([
                            '(Ds_fit_mass > %.2f & Ds_fit_mass < %.2f )'%(Ds_mass_range_lo,Ds_mass_range_hi),
                            '(Ds_Lxy_sign_BS > %.2f)'%args.LxySign_cut,
                            '(Ds_fit_vprob > 0.01)',
                            '(phi_fit_mass > 0.98 & phi_fit_mass < 1.05)'
                        ])
elif (args.process == 'fake_rate'):
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
    data_path = '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/'
    dataset     = [
    #2022
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root',
    #2023
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023B_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023C_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023D_HLT_overlap.root',
]
else:
    dataset = args.data

tree_name = 'WTau3Mu_tree' if not args.process == 'DsPhiMuMuPi' else 'DsPhiMuMuPi_tree' 

data_rdf = ROOT.RDataFrame(tree_name, dataset, branches).Filter(data_selection).Define('weight', 'lumi_factor')
dat = pd.DataFrame( data_rdf.AsNumpy() )

print('... processing input ...')
print('[+] input-dataset is %s : %s entries passed the selection' %( args.process ,data_rdf.Count().GetValue()))
print('---------------------------------------------')

## ETA BINS
bdt_inputs = features + ['tauEta']
if (args.LxySign_cut > 1.0): bdt_inputs.remove('tau_Lxy_sign_BS')
if(args.process == 'DsPhiMuMuPi'): 
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

if args.isMulticlass :
    dat['bdt_score_t3m'] =  np.zeros(dat.shape[0])
    dat['bdt_score_b']   =  np.zeros(dat.shape[0])
    dat['bdt_score_w3m'] =  np.zeros(dat.shape[0])
else:
    dat['bdt_score'] =  np.zeros(dat.shape[0])
for i, iclas in classifiers.items():
    print ('[BDT] evaluating %d/%d classifier' %(i+1, n_class))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))
    if args.isMulticlass :
        dat.loc[:,'bdt_fold%d_score_t3m' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 0]
        dat.loc[:,'bdt_score_t3m'] += iclas.predict_proba(dat[bdt_inputs])[:, 0] / n_class
        dat.loc[:,'bdt_fold%d_score_b' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 1]
        dat.loc[:,'bdt_score_b']   += iclas.predict_proba(dat[bdt_inputs])[:, 1] / n_class
        dat.loc[:,'bdt_fold%d_score_w3m' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 2]
        dat.loc[:,'bdt_score_w3m'] += iclas.predict_proba(dat[bdt_inputs])[:, 2] / n_class
    else:
        dat.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 1]
        dat.loc[:,'bdt_score'] += iclas.predict_proba(dat[bdt_inputs])[:, 1] / n_class

newfile_base = '%s/XGBout_'%(args.data_outdir) + ('DsPhiMuMuPi_' if args.process == 'DsPhiMuMuPi' else 'WTau3Mu_')
#newfile_tail = ('MC_' if args.isMC else 'DATA_') + args.tag + ".root"
newfile      = '%s/XGBout_'%(args.data_outdir) + tag + '.root' 

print('[OUT] output file saved in %s'%newfile)
data_out_rdf = ROOT.RDF.MakeNumpyDataFrame({col: dat[col].values for col in dat.columns}).Snapshot('tree_w_BDT', newfile)
