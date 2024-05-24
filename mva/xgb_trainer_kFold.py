import ROOT 
ROOT.EnableImplicitMT()
import argparse
import datetime 
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import shutil
sns.set(style="white")

import warnings
# Suppress the specific UserWarning
warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float64'> type is zero.")

import xgboost
from xgboost import XGBClassifier, plot_importance
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics         import roc_curve, roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from scipy.stats import ks_2samp
from collections import OrderedDict
from itertools import product
from pdb import set_trace

# from my config
from config import * 

##########################################################################################
# Define the gini metric - from https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703#5897

##########################################################################################

parser = argparse.ArgumentParser()
# I/O
parser.add_argument('--load_model',                                                                 help='load pkl instead of training')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/',help='output directory for plots')
parser.add_argument('--save_output',    action = 'store_true',                                      help='set it to save the bdt output')
parser.add_argument('--data_outdir',    default= '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/',   help='output directory for MVA data')
parser.add_argument('--unblind',        action = 'store_true',                                      help='set it to save data unblind')
parser.add_argument('--tag',                                                                        help='tag to the training')
# training mode
parser.add_argument('-s','--seed',      default=  3872, type = int,                                 help='set random state for reproducible results')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                               help='cut over 3muons SV displacement significance')
parser.add_argument('--useW3MuNu',      action = 'store_true' ,                                     help='use W->3MuNu (SM) MC in bkg training sample')
parser.add_argument('--fracW3MuNu',     default = 1.0,  type = float,                               help='which fraction of the W3MuNu sample to use')
parser.add_argument('--debug',          action = 'store_true' ,                                     help='set it to have useful printout')

args    = parser.parse_args()
print("\n")

# [OUTPUT]
# setup output tag
tag = 'kFold_' + (f'{args.tag}_' if args.tag else '') + (f'LxyS{args.LxySign_cut*100}_' if args.LxySign_cut > 0 else '') + (f'enrichW3MuNu_' if args.useW3MuNu else '')+ datetime.date.today().strftime('%Y%b%d')
# setup output directories
# for plots
plot_outpath = args.plot_outdir + '/Training_' + tag + '/'
if not args.load_model:
    try:
        os.makedirs(plot_outpath)
        shutil.copy2('/afs/cern.ch/user/c/cbasile/public/index.php', plot_outpath)
        print(f'[OUT] created out-directory for plots {plot_outpath}')
    except OSError as e:
        if os.path.exists(plot_outpath) and os.path.isdir(plot_outpath):
            print(f'[OUT] already existing out-directory for plots {plot_outpath}')
        else:
            print(f'[ERROR] cannot create plot-output directory {plot_outpath}')
            exit(-1)
# for data
if args.save_output:
    try:
        os.makedirs(args.data_outdir)
        print(f'[OUT] created out-directory for data {plot_outpath}')
    except OSError as e:
        if os.path.exists(args.data_outdir) and os.path.isdir(args.data_outdir):
            print(f'[OUT] already existing out-directory for data {args.data_outdir}')
        else:
            print(f'[ERROR] cannot create out-directory for data {args.data_outdir}')
            exit(-1)
else :
    print(f'[i] data with BDT applied will NOT be saved')

removeNaN = False

# ------------ DEFINE SELECTIONS ------------ # 
base_selection = f'(tau_fit_mass > {mass_range_lo} & tau_fit_mass < {mass_range_hi} ) & (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu) & (tau_Lxy_sign_BS >{args.LxySign_cut})'
sig_selection  = base_selection
bkg_selection  = base_selection + (f'& (tau_fit_mass < {blind_range_lo} | tau_fit_mass > {blind_range_hi})' if not (args.unblind) else '')
print('\n---------------------------------------------')
print('[!] base-selection   : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] data-selection   : %s'%bkg_selection)
print('---------------------------------------------')

# ------------ INPUT DATASET ------------ #
tree_name = 'WTau3Mu_tree'

print('[+] adding WTau3Mu SIGNAL samples')
signals     = [
    # 2022
    '../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap.root',
    '../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap.root',
    # 2023
    '../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap.root',
    '../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap.root '
]
print('[+] adding data-sidebands backgrund samples')
data_path = '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/'
dataSB_background  = [
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
if (args.useW3MuNu):
    print(f'[+] adding W3MuNu MC samples')
    W3MuNu_background = [
        #2022
        '../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onW3MuNu.root',
        '../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_privW3MuNu.root',
        #2023
        '../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onW3MuNu.root',
        '../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onW3MuNu.root',
    ]

print('... processing input ...')
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection).Define('weight', 'lumi_factor')
sig = pd.DataFrame( sig_rdf.AsNumpy() )
print(' SIGNAL      : %s entries passed selection' %len(sig.index))
bkg_rdf = ROOT.RDataFrame(tree_name, dataSB_background, branches).Filter(bkg_selection).Define('weight', '1.0')
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
print(' DATA-SB BACKGROUND  : %s entries passed selection' %len(bkg.index))
if (args.useW3MuNu):
    W3MuNu_bkg_rdf = ROOT.RDataFrame(tree_name, W3MuNu_background, branches).Filter(bkg_selection).Define('weight', 'lumi_factor')
    W3MuNu_bkg = pd.DataFrame( W3MuNu_bkg_rdf.AsNumpy() ) 
    W3MuNu_bkg = W3MuNu_bkg.sample(frac = args.fracW3MuNu, random_state = args.seed).reset_index(drop=True)
    print(' W3MuNu(MC) BACKGROUND  : %s entries passed selection' %len(W3MuNu_bkg.index))
print('---------------------------------------------')

## DEFINE TARGETS
sig.loc[:,'target'] = np.ones (sig.shape[0]).astype(int)
if args.useW3MuNu :
    bkg = pd.concat([bkg, W3MuNu_bkg]) 
bkg.loc[:,'target'] = np.zeros(bkg.shape[0]).astype(int)

## BDT inputs
#   rebin eta
#   remove displacement significance if cut Lxy/sigma
bdt_inputs = features + ['tauEta']
if (args.LxySign_cut > 0 ) : bdt_inputs.remove('tau_Lxy_sign_BS')
print('[i] BDT inputs')
[print(f'  - {f}') for f in bdt_inputs]
sig.loc[:,'tauEta'] = tauEta(sig['tau_fit_eta'])
bkg.loc[:,'tauEta'] = tauEta(bkg['tau_fit_eta'])

if(args.debug):print(sig)
if(args.debug):print(bkg)
##########################################################################################
## REWEIGHT AND MAKE TAU MASS FLAT
########################################################################################## 

# [...]
########################################################################################## 

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

# ------------ K-FOLD TRAINING ------------ # 
kfold = 5

# define the bdt score related columns 
data.loc[:,'id'] = np.arange(len(data))
for i in range(kfold):
    data.loc[:,'bdt_fold%d_isTrainSet' %i]  = np.zeros(data.shape[0]).astype(int)
    data.loc[:,'bdt_fold%d_score' %i]       = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_to_apply']  = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_score']     = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_training']  = np.zeros(data.shape[0]).astype(int)

# keep only the input features in train set
train = data[bdt_inputs+['tau_fit_mass','weight','target','id']]
if(args.debug) : print(train)
skf = StratifiedKFold(n_splits=kfold, random_state=args.seed, shuffle=True)
if args.load_model is None:
    
    # .pkl file to save BDT weights
    classifier_file = open('classifiers/classifiers_%s.pck' % tag, 'wb')
    classifiers = OrderedDict()
    
    
    # https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
    # (K-1)/K to train 1/K to use in the analysis
    for i, (train_index, apply_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):

        print('[fold %d/%d]' % (i + 1, kfold))    
        kdataset = train[train.id.isin(train_index)]
        print('  using %.2f percent of the full dataset'% (kdataset.shape[0]/train.shape[0]*100.))    
        
        # split the train set in training and validation + select SB
        ktrain, kvalid = train_test_split(
                kdataset[(kdataset.target == 1) | ((kdataset.target == 0) & ((kdataset.tau_fit_mass < blind_range_lo) | (kdataset.tau_fit_mass > blind_range_hi)))], 
                test_size=0.2, 
                random_state= args.seed)
        X_train, X_valid = ktrain[bdt_inputs], kvalid[bdt_inputs]
        y_train, y_valid = (ktrain['target']).values.astype(int), (kvalid['target']).values.astype(int)
        if(args.debug) : print(max(y_train))
        if(args.debug) : print(min(y_train))
        
        # create a copy of the apply-dataset to check the performance 
        sub = train[train.id.isin(apply_index)] #pd.DataFrame()
        sub['score']  = np.zeros_like(sub.id)
        
        # save the training information 
        data.loc[train.id.isin(train_index)&((data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi)))), 'bdt_fold%d_isTrainSet' %i] = 1
        data.loc[train.id.isin(apply_index), 'bdt_to_apply'] = i

        if(args.debug):print(data)

        # classifier definition
        clf = XGBClassifier(
            booster          = 'gbtree',
            max_depth        = 5,
            learning_rate    = 0.01, 
            n_estimators     = 10000, #10000,
            verbosity        = 0,
            subsample        = 0.7,
            colsample_bytree = 0.7,
            min_child_weight = 50, #1E-6 * np.sum(train[train.id.isin(train_index)].weight),
            gamma            = 5, 
            seed             = args.seed,
            # scale_pos_weight = 0.5,
            reg_alpha        = 5.0,
            reg_lambda       = 5.0,
            use_label_encoder=False,
            eval_metric      ='auc',
            objective        ='binary:logistic',
            early_stopping_rounds = 100, #100
        )

        clf.fit(
            X_train, 
            y_train,
            eval_set              = [(X_train, y_train),(X_valid, y_valid)],
            verbose               = False,
            #sample_weight         = ktrain['weight'],
        )
        
        best_iteration = clf.get_booster().best_iteration
        print('[fold %d/%d] - best iteration %d' %(i+1, kfold, best_iteration))
        classifiers[i] = clf
        
        # Predict on our test data (if early stopping in training best_iteration automatically used) 
        #       return (n_samples, n_classes) array
        print('[fold %d/%d Prediciton:]' % (i + 1, kfold))
        # plot evaluation metric vs epochs
        results = clf.evals_result()
        epochs  = len(results['validation_0']['auc'])
        x_axis  = range(0, epochs)
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(x_axis, results['validation_0']['auc'], label='Train')
        ax.plot(x_axis, results['validation_1']['auc'], label='Validation')
        ax.set_yscale('log')
        ax.legend()
        plt.ylabel('AUC')
        plt.title('Fold number %d / %d'%(i+1, kfold))
        plt.savefig('%sevalMetricVSepochs_%s_fold%d.png' %(plot_outpath,tag, i+1))

        p_test = clf.predict_proba(sub[bdt_inputs])[:, 1]
        sub.loc[:,'score'] += p_test #/kfold

        # adjust the score to match 0,1
        smin = min(p_test)
        smax = max(p_test)
        sub.loc[:,'score_norm'] = (p_test - smin) / (smax - smin)

        print ('round %d' %(i+1))
        print ('\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_norm'] - sub['target']))/len(sub)))
        print ('\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_norm'] - sub[sub.target>0.5]['target']))/len(sub)))
        print ('\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_norm'] - sub[sub.target<0.5]['target']))/len(sub)))

    # save the models
    pickle.dump(classifiers, classifier_file)
    classifier_file.close()
else :
    print('[+] load model from %s'%args.load_model)
    with open(args.load_model, 'rb') as f:
        classifiers = pickle.load(f)

    for i, (train_index, apply_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):
        data.loc[train.id.isin(train_index)&((data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi)))), 'bdt_fold%d_isTrainSet' %i] = 1
        data.loc[train.id.isin(apply_index), 'bdt_to_apply'] = i

# ------------ FINALLY SAVE BDT SCORES ------------ # 
print('-----------------------------')
print('SAVE the scores')
n_class = len(classifiers)
print(" Number of splits %d"%n_class)

for i, iclas in classifiers.items():
    
    print (' evaluating %d/%d classifier' %(i+1, n_class))
    
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))  
    
    data.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(data[bdt_inputs])[:, 1]
    data.loc[data['bdt_to_apply'] == i,'bdt_score'] = iclas.predict_proba(data.loc[data['bdt_to_apply'] == i, bdt_inputs])[:, 1]
    data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training'] += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs])[:, 1]/(n_class-1)

# save data & MC as root trees
if(args.save_output):
    print(data.columns)
    # convert data to dictionary with numpy arrays 
    out_data = {col: data[col].values for col in data.columns}
    out_data_filename = f'{args.data_outdir}/XGBout_data_{tag}.root'
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 0').Snapshot('tree_w_BDT', out_data_filename)
    print(f'[o] output DATA saved in {out_data_filename}')
    out_data_filename = f'{args.data_outdir}/XGBout_signal_{tag}.root'
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 1').Snapshot('tree_w_BDT', out_data_filename)
    print(f'[o] output SIGNAL saved in {out_data_filename}')

if(args.load_model): exit(-1) 


###              ###
#   PLOT SECTION   # 
###              ###
plot_data = data[(data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi)))]

# ------------ ROC CURVE ------------ # 
plt.clf()
cuts_to_display = [0.500, 0.990, 0.995, 0.999]

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

fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_score, sample_weight=plot_data.weight)
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

fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_training, sample_weight=plot_data.weight)
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

print ('ROC AUC train ', roc_auc_score(plot_data.target,  plot_data.bdt_training, sample_weight=plot_data.weight))
print ('ROC AUC test  ', roc_auc_score(plot_data.target , plot_data.bdt_score , sample_weight=plot_data.weight))

plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('%sroc_%s.png' %(plot_outpath,tag))
plt.savefig('%sroc_%s.pdf' %(plot_outpath,tag))
plt.clf()

roc_file = open('roc_%s.pck' % tag, 'wb')
pickle.dump((tpr, fpr), roc_file)
roc_file.close()


# ------------ OVERTRAINING TEST ------------ # 
train_sig = plot_data[plot_data.target==1].bdt_training
train_bkg = plot_data[plot_data.target==0].bdt_training

test_sig = plot_data[plot_data.target==1].bdt_score  
test_bkg = plot_data[plot_data.target==0].bdt_score  

low  = 0
high = 1
low_high = (low,high)
bins = 50

# signal sample
hist, bins = np.histogram(
    test_sig,
    bins=bins, 
#     range=low_high, 
#    normed=True
)
hist_norm = hist / len(test_sig)
width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_sig) / sum(hist)
err    = np.sqrt(hist)/len(test_sig) #np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist_norm, 
    yerr=err, 
    fmt='o', 
    c='r', 
    label='S (analysis)'
)

sns.histplot(train_sig, bins=bins, kde=False, stat='probability', alpha = 0.5, color = "r", label='S (train)')

# background sample
hist, bins = np.histogram(
    test_bkg,
    bins=bins, 
#     range=low_high, 
#    normed=True
)

hist_norm = hist / len(test_bkg)
width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_bkg) / sum(hist)
err    = np.sqrt(hist)/len(test_bkg) #np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist_norm, 
    yerr=err, 
    fmt='o', 
    c='b', 
    label='B (test)'
)

sns.histplot(train_bkg, bins=bins, kde=False, stat='probability', alpha = 0.5, color = "b", label='B (train)')

plt.xlabel('BDT output')
plt.ylabel('Arbitrary units')
plt.legend(loc='best')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))

plt.savefig('%sovertrain_%s.pdf' %(plot_outpath,tag))
plt.savefig('%sovertrain_%s.png' %(plot_outpath,tag))

plt.yscale('log')

plt.savefig('%sovertrain_log_%s.pdf' %(plot_outpath, tag))
plt.savefig('%sovertrain_log_%s.png' %(plot_outpath, tag))

plt.clf()

# ------------ FEATURES IMPORTANCE ------------ # 

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
plt.savefig('%sfeat_importance_%s.pdf' %(plot_outpath,tag))
plt.savefig('%sfeat_importance_%s.png' %(plot_outpath,tag))
plt.clf()

