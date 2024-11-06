import ROOT 
ROOT.EnableImplicitMT()
import argparse
import pickle
import numpy  as np
import pandas as pd

from xgboost import XGBClassifier, plot_importance
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics         import roc_curve, roc_auc_score
from collections import OrderedDict

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# my imports
import sys
import os
import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from plots.color_text import color_text as ct


##########################################################################################
# Define the gini metric - from https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703#5897

##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--load_model',                                                                     help='load pkl instead of training')
parser.add_argument('--data_outdir',    default= '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/',       help='output directory for ntuples with BDT applied')
parser.add_argument('--tag',            default= 'emulateRun2',                                         help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,                                         help='set it to have useful printout')
parser.add_argument('--save_output',    action = 'store_true' ,                                         help='set it to save the bdt output')
parser.add_argument('--process',        choices= ['WTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'peakingBkg', 'ZTau3Mu'],   help='what process is in the input sample')
parser.add_argument('--isMC',           action = 'store_true' ,                                         help='set if running on MonteCarlo')
parser.add_argument('--isMulticlass',   action = 'store_true' ,                                         help='set if applying a multiclass classifier')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                               help='cut over 3muons SV displacement significance')
parser.add_argument('-d', '--data',     action = 'append',                                              help='dataset to apply BDT weights')

args = parser.parse_args()
tag = '_'.join([args.process, 'MC' if args.isMC else 'DATA']) + ( ('_' + args.tag)  if args.tag else '')
removeNaN = False 
print('\n')

 # ------------ DEFINE SELECTIONS ------------ # 
if(args.process == 'DsPhiMuMuPi'):
    base_selection = '&'.join([
        config.Ds_base_selection,
        config.Ds_phi_selection,
        config.Ds_sv_selection,
    ])
elif (args.process == 'peakingBkg'):
    base_selection = '&'.join([
        config.base_selection,
        config.displacement_selection,
    ])
else:
    base_selection = ' & '.join([
        config.base_selection,
        config.displacement_selection,
    ]) 

print(f'{ct.BOLD}[!] base-selection : %s'%base_selection)
print(f'---------------------------------------------{ct.END}')

 # ------------ INPUT DATASET ------------ # 

if(args.data is None):
    dataset = config.mc_samples[args.process] if args.isMC else config.data_samples[args.process]
else:
    dataset = args.data
tree_name = 'WTau3Mu_tree' if not args.process == 'DsPhiMuMuPi' else 'DsPhiMuMuPi_tree' 
print('[+] processing files :')
[print(f' - {sample}') for sample in dataset]


data_rdf = ROOT.RDataFrame(tree_name, dataset).Filter(base_selection)
input_branches = [str(name) for name in data_rdf.GetColumnNames()]
if (args.debug) : print("[i] Extracted Column Names:", input_branches)
print('... processing input ...')
print('[+] input-dataset is %s : %s entries passed the selection' %( args.process ,data_rdf.Count().GetValue()))
dat = pd.DataFrame( data_rdf.AsNumpy())
dat.columns = input_branches
if (args.debug): print(dat)

print('---------------------------------------------')

## ETA BINS
bdt_inputs = config.features + ['tauEta']
#if (args.LxySign_cut > 1.0): bdt_inputs.remove('tau_Lxy_sign_BS')
if(args.process == 'DsPhiMuMuPi'): 
    if(args.debug): print(config.features_DsPhiPi_to_Tau3Mu)
    # rename Ds branches to match BDT structure 
    dat.rename( columns= config.features_DsPhiPi_to_Tau3Mu, inplace=True) 
    dat.loc[:,'tauEta'] = config.tauEta(dat['Ds_fit_eta'])
else:
    dat.loc[:,'tauEta'] = config.tauEta(dat['tau_fit_eta'])

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
    # make prediction using the iterations after the transient up to the best iteration
    starting_epoch = 0 #int(0.01 * len(iclas.evals_result()['validation_0']['auc']))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))
    if args.isMulticlass :
        dat.loc[:,'bdt_fold%d_score_t3m' %i]    = iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 0]
        dat.loc[:,'bdt_score_t3m']             += iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 0] / n_class
        dat.loc[:,'bdt_fold%d_score_b' %i]      = iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 1]
        dat.loc[:,'bdt_score_b']               += iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 1] / n_class
        dat.loc[:,'bdt_fold%d_score_w3m' %i]    = iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 2]
        dat.loc[:,'bdt_score_w3m']             += iclas.predict_proba(dat[bdt_inputs], iteration_range = (starting_epoch, best_iteration +1))[:, 2] / n_class
    else:
        dat.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(dat[bdt_inputs])[:, 1]
        dat.loc[:,'bdt_score'] += iclas.predict_proba(dat[bdt_inputs])[:, 1] / n_class

#newfile_base = '%s/XGBout_'%(args.data_outdir) + args.process
#newfile_tail = ('MC_' if args.isMC else 'DATA_') + args.tag + ".root"
newfile      = '%s/XGBout_'%(args.data_outdir) + tag + '.root' 

print('[OUT] output file saved in %s'%newfile)
print("[i] Final data branches : ",dat.columns)
data_out_rdf = ROOT.RDF.MakeNumpyDataFrame({col: dat[col].values for col in dat.columns}).Snapshot('tree_w_BDT', newfile)
