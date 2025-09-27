import ROOT 
ROOT.EnableImplicitMT()
import argparse
import datetime 
import pickle
import json
import numpy  as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
import shutil

#import xgboost
from xgboost import XGBClassifier, callback, plot_importance
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics         import roc_curve, roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from scipy.stats import ks_2samp
from collections import OrderedDict
from itertools import product
from pdb import set_trace

# from my config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
from plots.color_text import color_text as ct
from data_preprocessing_lib import kFold_splitting

##########################################################################################

parser = argparse.ArgumentParser()
# I/O
parser.add_argument('--load_model',                                                                 help='load pkl instead of training')
parser.add_argument('--preprocess',     action = 'store_true',                                      help='run data preprocessing to split in kFold')
parser.add_argument('--prep_sig',                                                                   help='preprocessed signal input')
parser.add_argument('--prep_bkg',                                                                   help='preprocessed background input')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/',help='output directory for plots')
parser.add_argument('--plot_only',      action = 'store_true',                                      help='output directory for plots')
parser.add_argument('--save_output',    action = 'store_true',                                      help='set it to save the bdt output')
parser.add_argument('--data_outdir',    default= '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/',   help='output directory for MVA data')
parser.add_argument('--tag',                                                                        help='tag to the training')
# training mode
parser.add_argument('-s','--seed',      default=  3872, type = int,                                 help='set random state for reproducible results')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                               help='cut over 3muons SV displacement significance')
parser.add_argument('--useW3MuNu',      action = 'store_true' ,                                     help='use W->3MuNu (SM) MC in bkg training sample')
parser.add_argument('--fracW3MuNu',     default = 1.0,  type = float,                               help='which fraction of the W3MuNu sample to use')
parser.add_argument('--opt_parameters',                                                             help='.json file with optimized parameters')
parser.add_argument('--debug',          action = 'store_true' ,                                     help='set it to have useful printout')

args    = parser.parse_args()
if (args.plot_only and not args.load_model):
    print(f'{ct.RED}[ERROR]{ct.END} you have to specify a the model to load to make plots')
    exit()
print("\n")

# [INPUT]
if args.opt_parameters and not os.path.exists(args.opt_parameters) :
    print(f'{ct.RED}[ERROR]{ct.END} specified file for BDT params does not exist')
    exit()


# [OUTPUT]
# setup output tag
tag = 'kFold_' + (f'{args.tag}_' if args.tag else '') + (f'LxyS{args.LxySign_cut}_' if args.LxySign_cut > 0 else '') + (f'enrichW3MuNu_' if args.useW3MuNu else '')+ datetime.date.today().strftime('%Y%b%d')
# setup output directories...
# ...for plots
plot_outpath = args.plot_outdir + '/Training_' + tag + '/'
try:
    os.makedirs(plot_outpath)
    shutil.copy2('/afs/cern.ch/user/c/cbasile/public/index.php', plot_outpath)
    print(f'{ct.BOLD}[OUT]{ct.END} created out-directory for plots {plot_outpath}')
except OSError as e:
    if os.path.exists(plot_outpath) and os.path.isdir(plot_outpath):
        print(f'{ct.BOLD}[OUT]{ct.END} already existing out-directory for plots {plot_outpath}')
    else:
        print(f'{ct.RED}[ERROR]{ct.END} cannot create plot-output directory {plot_outpath}')
        exit(-1)
# ...for data
out_data_filename = f'{args.data_outdir}/XGBout_data_{tag}.root'
out_signal_filename = f'{args.data_outdir}/XGBout_signal_{tag}.root'
if args.save_output:
    try:
        os.makedirs(args.data_outdir)
        print(f'{ct.BOLD}[OUT]{ct.END} created out-directory for data {args.data_outdir}')
    except OSError as e:
        if os.path.exists(args.data_outdir) and os.path.isdir(args.data_outdir):
            print(f'{ct.BOLD}[OUT]{ct.END} already existing out-directory for data {args.data_outdir}')
        else:
            print(f'{ct.RED}[ERROR]{ct.END} cannot create out-directory for data {args.data_outdir}')
            exit(-1)
else :
    print(f'{ct.BOLD}[i]{ct.END} data with BDT applied will NOT be saved')

removeNaN = False

# ------------ DEFINE SELECTIONS ------------ # 
base_selection = '&'.join([config.base_selection,
                           f'(tau_Lxy_sign_BS > {args.LxySign_cut} )' if args.LxySign_cut > 0 else '',
                           config.phi_veto,
                           ])
sig_selection  = base_selection
bkg_selection  = base_selection
print('\n---------------------------------------------')
print(f'[!] base-selection   : {base_selection}')
print(f'{ct.RED}[S]{ct.END} signal-selection : {sig_selection}')
print(f'{ct.BLUE}[B]{ct.END} data-selection   : {bkg_selection}')
print('---------------------------------------------')

# ------------ BDT settings ------------ #
kfold = 5
bdt_inputs = config.features + ['tauEta']
print('[i] BDT inputs')
[print(f'  - {f}') for f in bdt_inputs]

# ------------ INPUT DATASET ------------ #
tree_name = 'WTau3Mu_tree'

if args.preprocess:
    print('[i] run data preprocessing')
    tree_name = 'WTau3Mu_tree'
    signals         = config.WTau3Mu_signals
    backgrounds     = config.data_background
    if (args.useW3MuNu): enrich_bkg      = config.W3MuNu_background
else :
    print('[i] import preprocessed data')
    tree_name = 'tree_w_BDT'
    signals = args.prep_sig
    if not os.path.exists(signals):
        print(f'{ct.RED}[ERROR]{ct.END} cannot find preprocessed signal input {signals}')
        exit(-1)
    backgrounds = args.prep_bkg
    if not os.path.exists(backgrounds):
        print(f'{ct.RED}[ERROR]{ct.END} cannot find preprocessed background input {backgrounds}')
        exit(-1)

print('... processing input ...')
print(f'{ct.RED}[+]{ct.END} adding WTau3Mu SIGNAL samples')
print(f'{ct.BLUE}[+]{ct.END} adding data-sidebands background samples')
sig_rdf = ROOT.RDataFrame(tree_name, signals).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
print(' SIGNAL      : %s entries passed selection' %len(sig.index))
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
print(' DATA-SB BACKGROUND  : %s entries passed selection' %len(bkg.index))
if (args.useW3MuNu):
    print('[+] adding W3MuNu MC samples')
    W3MuNu_bkg_rdf = ROOT.RDataFrame(tree_name, enrich_bkg).Filter(bkg_selection).Define('weight', 'lumi_factor')
    W3MuNu_bkg = pd.DataFrame( W3MuNu_bkg_rdf.AsNumpy() ) 
    W3MuNu_bkg = W3MuNu_bkg.sample(frac = args.fracW3MuNu, random_state = args.seed).reset_index(drop=True)
    print(' W3MuNu(MC) BACKGROUND  : %s entries passed selection' %len(W3MuNu_bkg.index))
print('---------------------------------------------')

# ------------ DATA PREPROCESSING ------------ #
if args.preprocess:
    # DEFINE TARGETS
    sig.loc[:,'target'] = np.ones(sig.shape[0]).astype(int)
    if args.useW3MuNu :
        bkg = pd.concat([bkg, W3MuNu_bkg]) 
    bkg.loc[:,'target'] = np.zeros(bkg.shape[0]).astype(int)

    # DEFINE WEIGHTS FOR TRAINING
    # charge unbalance
    sig.loc[:,'tau_charge_weight'] = np.ones(sig.shape[0]).astype(float)
    Nplus  = sig[sig.tau_fit_charge>0].shape[0]
    Nminus = sig[sig.tau_fit_charge<0].shape[0]
    sig.loc[sig.tau_fit_charge<0,'tau_charge_weight'] = Nplus/Nminus #* np.ones(sig[sig.tau_fit_charge<0].shape[0]).astype(float)
    print(f' N+ = {Nplus} \t N- = {Nminus} -> weight = {Nplus/Nminus:.2f}')

    sig.loc[:,'train_weight'] = sig.NLO_weight * sig.tau_charge_weight 
    bkg.loc[:,'train_weight'] = np.ones(bkg.shape[0]).astype(float)

    # REBIN ETA
    sig.loc[:,'tauEta'] = config.tauEta(sig['tau_fit_eta'])
    bkg.loc[:,'tauEta'] = config.tauEta(bkg['tau_fit_eta'])

    ## CONCATENATE & SHUFFLE SIGNAL AND BACKGROUND
    data = pd.concat([sig, bkg])
    if(args.debug) : print(data)
    data = data.sample(frac = 1, random_state = args.seed).reset_index(drop=True)

    ## REMOVE NaN
    if(removeNaN):
        check_for_nan = data.isnull().values.any()
        print ("[!] check for NaN " + str(check_for_nan))
        if (check_for_nan):
            data = data.dropna()
            check_for_nan = data.isnull().values.any()
            print ("[!] check again for NaN " + str(check_for_nan))

    # K-FOLD SPLITTING & SAVE TRAINING SAMPLES 
    kFold_splitting(
        data = data, 
        bdt_inputs = bdt_inputs, 
        kfold = kfold,
        out_data_dir = args.data_outdir,
        tag = tag,
        rnd_seed = args.seed,
        debug = args.debug,
    )

    if(args.debug):print(sig)
    if(args.debug):print(bkg)
    exit()  
else:
    ## CONCATENATE & SHUFFLE SIGNAL AND BACKGROUND
    data = pd.concat([sig, bkg])
    if(args.debug) : print(data)
    data = data.sample(frac = 1, random_state = args.seed).reset_index(drop=True)


# ------------ MODEL TRAINING ------------ #
if (args.load_model is None) or (args.plot_only is None):

    # ------------ BDT HPARAMETERS ------------ # 
    # - default -
    parameters = {
        'booster'               :  'gbtree',
        'device'                :  'cuda',
        'tree_method'           :  'hist',
        'objective'             :  'binary:logistic',
        'eval_metric'           :  'auc',
        #hyperparameters
        'n_estimators'          :  15000,   # number of sequential trees to be modeled
        'max_depth'             :  7,       # max depth of a single tree
        'eta'                   :  0.01,    # step size shrinkage used in update to prevent overfitting (learning rate) 
        'subsample'             :  0.7,     # subsample ratio of the training instance at every boosting iteration
        'colsample_bytree'      :  0.7,     # subsample ratio of columns when constructing each tree
        'min_child_weight'      :  50,      # min sum of instance weight (hessian) needed in a child
        'gamma'                 :  5,       # min loss reduction required to make a further partition on a leaf node of the tree
        # scale_pos_weight      :  0.5,     # control the balance of positive and negative weights
        'reg_alpha'             :  5.0,     # L1 regularization term on weights [0, inf)
        'reg_lambda'            :  5.0,     # L2 regularization term on weights [0, inf)
        #'early_stopping_rounds' :  100,
        'use_label_encoder'     :  False,
        'seed'                  :  args.seed,
        'verbosity'             :  0,
    }
    # - load optimized parameters if any
    if not (args.opt_parameters):
        print(f'[i] using default parameters {parameters}')
    else :
        print(f'[i] loading optimized parameters from {args.opt_parameters}')
        with open(args.opt_parameters) as fj:
            opt_parameters = json.load(fj)
        if args.debug : [print(f'{key} : {opt_parameters[key]}') for key in opt_parameters]
        parameters.update(opt_parameters)

    [print(f' - {key} : {parameters[key]}') for key in parameters]

    # open .pkl file to save BDT weights
    classifier_file = open('/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/classifiers/classifiers_%s.pck' % tag, 'wb')
    classifiers = OrderedDict()
    
    # https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
    # (K-1)/K to train 1/K to use in the analysis
    #for i, (train_index, apply_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):
    for i in range(kfold):

        print(f'{ct.BOLD}[fold {i+1}/{kfold}]{ct.END}')
        kdataset        = data[data[f'bdt_fold{i}_isTrainSet'] == 1]
        print('  using %.2f percent of the full dataset'% (kdataset.shape[0]/data.shape[0]*100.))    
        
        # create a copy of the apply-dataset to check the performance 
        sub = data[data[f'bdt_to_apply'] == i].copy()
        sub.loc[:, 'score']  = np.zeros_like(sub.id)
        
        # split the train set in training and validation + select SB
        ktrain, kvalid = train_test_split(
                kdataset[(kdataset.target == 1) | ((kdataset.target == 0) & ((kdataset.tau_fit_mass < config.blind_range_lo) | (kdataset.tau_fit_mass > config.blind_range_hi)))], 
                test_size=0.2, 
                random_state= args.seed)
        X_train, X_valid = ktrain[bdt_inputs], kvalid[bdt_inputs]
        y_train, y_valid = (ktrain['target']).values.astype(int), (kvalid['target']).values.astype(int)
        if(args.debug) : print(max(y_train))
        if(args.debug) : print(min(y_train))

# ------------ MODEL SETUP ------------ #
        # early stopping callback
        # https://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.callback
        early_stopping = callback.EarlyStopping(
            data_name   = 'validation_1',
            rounds      = 150,
            #min_delta   = 1e-6,
            metric_name = 'auc', 
            save_best   = True,
        ) 
        clf = XGBClassifier(
            **parameters,
            callbacks             = [early_stopping],
        )
# ------ MODEL FITTING & ON-THE-FLY EVALUATION ------ #
        clf.fit(
            X_train, 
            y_train,
            sample_weight         = ktrain.train_weight,
            eval_set              = [(X_train, y_train),(X_valid, y_valid)],
            verbose               = True,
        )
        classifiers[i] = clf
        
        # get #epoch & best iteration
        results = clf.evals_result()
        epochs  = len(results['validation_0']['auc'])
        best_iteration = clf.get_booster().best_iteration
        print(f'[fold {i+1}/{kfold}] - best iteration / #epochs : {best_iteration}/{epochs}')

        
        print(' > prediciton:')
        # plot evaluation metric vs epochs
        x_axis  = range(0, epochs)
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(x_axis, results['validation_0']['auc'], label='Train')
        ax.plot(x_axis, results['validation_1']['auc'], label='Validation')
        #ax.set_yscale('log')
        ax.grid()
        ax.set_ylim(0.96, 1)
        ax.legend(fontsize = 15)
        plt.ylabel('AUC')
        plt.title('Fold number %d / %d'%(i+1, kfold))
        plt.savefig('%sevalMetricVSepochs_%s_fold%d.png' %(plot_outpath,tag, i+1))

        # eval performance on the apply-dataset
        p_test = clf.predict_proba(sub[bdt_inputs], iteration_range = (0, best_iteration +1))[:, 1]
        sub.loc[:,'score'] += p_test #/kfold

        # adjust the score to match 0,1
        smin = min(p_test)
        smax = max(p_test)
        sub.loc[:,'score_norm'] = (p_test - smin) / (smax - smin)

        print ('\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_norm'] - sub['target']))/len(sub)))
        print ('\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_norm'] - sub[sub.target>0.5]['target']))/len(sub[sub.target>0.5])))
        print ('\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_norm'] - sub[sub.target<0.5]['target']))/len(sub[sub.target<0.5])))

    # save the models
    pickle.dump(classifiers, classifier_file)
    classifier_file.close()
    print(f'{ct.BOLD}[OUT]{ct.END} saved classifiers in classifiers/classifiers_{tag}.pck')

# ------------ PARSE EXISTING WEIGHTS ------------ #
else:
    print(f'{ct.BOLD}[+]{ct.END} load model from {args.load_model}')
    with open(args.load_model, 'rb') as f:
        classifiers = pickle.load(f)


# ------------ SAVE BDT SCORES ------------ # 
if not args.plot_only:
    print('-----------------------------')
    print('SAVE the scores')
    n_class = len(classifiers)
    print(f' Number of splits : {n_class}')

    for i, iclas in classifiers.items():
        
        print (f' evaluating {i+1}/{n_class} classifier')
        epochs = len(iclas.evals_result()['validation_0']['auc'])
        best_iteration = iclas.get_booster().best_iteration
        print(f'\tbest iteration/epochs {best_iteration}/{epochs}')  
        
        # save scores
        # remove initial transient
        data.loc[:,'bdt_fold%d_score' %i]                               = iclas.predict_proba(data[bdt_inputs], iteration_range = (0, best_iteration +1))[:, 1]
        data.loc[data.bdt_to_apply == i,'bdt_score']                    = iclas.predict_proba(data.loc[data.bdt_to_apply == i, bdt_inputs], iteration_range = (0, best_iteration +1))[:, 1]
        data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training'] += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs], iteration_range = (0, best_iteration +1))[:, 1]/(n_class-1)

    # save data & MC as root trees
    if(args.save_output):
        print(data.columns)
        # convert data to dictionary with numpy arrays 
        out_data = {col: data[col].values for col in data.columns}
        out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 0').Snapshot('tree_w_BDT', out_data_filename)
        print(f'{ct.BOLD}[OUT]{ct.END} output DATA saved in {out_data_filename}')
        out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 1').Snapshot('tree_w_BDT', out_signal_filename)
        print(f'{ct.BOLD}[OUT]{ct.END} output SIGNAL saved in {out_signal_filename}')



###              ###
#   PLOT SECTION   # 
###              ###
plot_data = data[(data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < config.blind_range_lo) | (data.tau_fit_mass > config.blind_range_hi)))]

# ------------ ROC CURVE ------------ # 
plt.clf()
cuts_to_display = [0.500, 0.900, 0.950, 0.990, 0.995, 0.999]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
fig = plt.figure(figsize = (8,6))
plt.plot(xy, xy, color='grey', linestyle='--')
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('background efficiency $\\epsilon_{B}$', fontsize = 18)
plt.xticks(fontsize=16)
plt.ylabel('signal efficiency $\\epsilon_{S}$', fontsize = 18)
plt.yticks(fontsize=16)

plt.xscale('log')

fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_score, sample_weight=plot_data.train_weight)
plt.plot(fpr, tpr, label='analysis set', color='b', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
#for i, note in enumerate(cuts_to_display):
    #plt.annotate(note, (wp_x[i], wp_y[i]))

fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_training, sample_weight=plot_data.train_weight)
plt.plot(fpr, tpr, label='train set', color='r', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
dx = 0.1
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]),horizontalalignment='left')

print ('ROC AUC train ', roc_auc_score(plot_data.target,  plot_data.bdt_training, sample_weight=plot_data.train_weight))
print ('ROC AUC test  ', roc_auc_score(plot_data.target , plot_data.bdt_score , sample_weight=plot_data.train_weight))

plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plot_name = '%sroc_%s' %(plot_outpath,tag)
plt.savefig(f'{plot_name}.png')
plt.savefig(f'{plot_name}.pdf')
print(f'{ct.BOLD}[OUT]{ct.END} saved {ct.CYAN}ROC{ct.END} curve in {plot_name}.png/pdf')
plt.clf()

# ------------ OVERTRAINING TEST ------------ # 
train_sig = plot_data[plot_data.target==1].bdt_training
train_bkg = plot_data[plot_data.target==0].bdt_training

test_sig = plot_data[plot_data.target==1].bdt_score  
test_bkg = plot_data[plot_data.target==0].bdt_score  

low  = 0
high = 1
low_high = (low,high)
bins = 20
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
rax.grid(True)

rax.set_xlabel('BDT output')
rax.set_ylabel('test / train')
rax.set_ylim(0.5, 1.5)
ax.set_ylabel('Counts')
ax.legend(loc='best')
ax.set_yscale('log')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
#ax.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))
plot_name = '%sovertrain_%s' %(plot_outpath,tag)
plt.savefig(f'{plot_name}.png')
plt.savefig(f'{plot_name}.pdf')
print(f'{ct.BOLD}[OUT]{ct.END} saved {ct.CYAN}OVERTRAIN{ct.END} plot in {plot_name}.png/pdf')

plt.clf()

# ------------ FEATURES IMPORTANCE ------------ # 
plt.figure(figsize=(8,6))
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

bars = [config.labels[k] for k in orderedfscores.keys()]
y_pos = np.arange(len(bars))
 
# Create horizontal bars
plt.barh(y_pos, orderedfscores.values())
 
# Create names on the y-axis
plt.yticks(y_pos, bars)
plt.tight_layout()
plot_name = '%sfeat_importance_%s' %(plot_outpath,tag)
plt.savefig(f'{plot_name}.png')
plt.savefig(f'{plot_name}.pdf')
print(f'{ct.BOLD}[OUT]{ct.END} saved {ct.CYAN}FEATURE IMPRTANCE{ct.END} plot in {plot_name}.png/pdf')
plt.clf()

