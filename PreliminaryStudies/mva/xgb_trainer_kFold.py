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

# from my config
from config import * 

##########################################################################################
# Define the gini metric - from https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703#5897

##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--load_model', help='load pkl instead of training')
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('-s','--seed',  default=  3872, type = int, help='set random state for reproducible results')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--save_output',action = 'store_true' ,help='set it to save the bdt output')
parser.add_argument('--unblind',    action = 'store_true' ,help='set it to unblind the data')

args = parser.parse_args()
tag = args.tag + '_kFold_' + datetime.date.today().strftime('%Y%b%d')
removeNaN = False 

 # ------------ DEFINE SELECTIONS ------------ # 
base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f )'%(mass_range_lo,mass_range_hi) 
sig_selection  = base_selection 
bkg_selection  = base_selection + ('& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(blind_range_lo, blind_range_hi) if not (args.unblind) else '')

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)
print('---------------------------------------------')

 # ------------ INPUT DATASET ------------ # 

signals     = [
    '../outRoot/recoKinematicsT3m_MC_2022_reMini_HLT_Tau3Mu.root',
    '../outRoot/recoKinematicsT3m_MC_2022EE_reMini_HLT_Tau3Mu.root',
]

backgrounds  = [
    #2022
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Cv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Dv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Dv2.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Ev1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Fv1.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Gv1.root',
    #2023
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023B.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023Cv1.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023Cv2.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023Cv3.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023C.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023Dv1.root', 
    #'/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/recoKinematicsT3m_ParkingDoubleMuonLowMass_2023D.root', 
]

tree_name = 'Tau3Mu_HLTemul_tree'
mc_factor = MC_norm_factor_dict['2022reMini']  
print('[!] MC normalization factor = %.3e'%mc_factor)
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection).Define('weight', 'lumi_factor')
sig = pd.DataFrame( sig_rdf.AsNumpy() )
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds, branches).Filter(bkg_selection).Define('weight', '1')
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )

print('... processing input ...')
print(' SIGNAL : %s entries passed the selection' %sig_rdf.Count().GetValue())
print(' BACKGROUND : %s entries passed the selection' %bkg_rdf.Count().GetValue())
print('---------------------------------------------')

## DEFINE TARGETS
sig.loc[:,'target'] = np.ones (sig.shape[0]).astype(int)
bkg.loc[:,'target'] = np.zeros(bkg.shape[0]).astype(int)

## ETA BINS
if(args.debug):print(sig['tau_fit_eta'])
if(args.debug):print(tauEta(sig['tau_fit_eta'].values))
bdt_inputs = features + ['tauEta']
if(args.debug):print(bdt_inputs)
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
    classifier_file = open('classifiers_%s.pck' % tag, 'wb')
    classifiers = OrderedDict()

    # https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
    # (K-1)/K to train 1/K to use in the analysis
    for i, (train_index, apply_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):

        print('[Fold %d/%d]' % (i + 1, kfold))    
        kdataset = train[train.id.isin(train_index)]
        print('  using %.2f percent of the full dataset'% (kdataset.shape[0]/train.shape[0]*100.))    
        
        # split the train set in training and validation
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
        
        clf = XGBClassifier(
            booster          = 'gbtree',
            max_depth        = 5,
            learning_rate    = 0.01, 
            n_estimators     = 10000, #10000,
            verbosity        = 1,
            subsample        = 0.7,
            colsample_bytree = 0.7,
            min_child_weight = 50, #1E-6 * np.sum(train[train.id.isin(train_index)].weight),
            gamma            = 5, 
            seed             = args.seed,
            # scale_pos_weight = 0.5,
            reg_alpha        = 5.0,
            reg_lambda       = 5.0,
            use_label_encoder=False,
            objective='binary:logistic',
        )

        clf.fit(
            X_train, 
            y_train,
            eval_set              = [(X_train, y_train),(X_valid, y_valid)],
            early_stopping_rounds = 10, #100
            eval_metric           = 'auc',
            verbose               = True,
            #sample_weight         = ktrain['weight'],
        )
        
        best_iteration = clf.get_booster().best_iteration
        print('[Fold %d/%d] - best iteration %d' %(i+1, kfold, best_iteration))
        classifiers[i] = clf
        
        # Predict on our test data (if early stopping in training best_iteration automatically used) 
        #       return (n_samples, n_classes) array
        print('[Fold %d/%d Prediciton:]' % (i + 1, kfold))
        p_test = clf.predict_proba(sub[bdt_inputs])[:, 1]
        sub['score'] += p_test #/kfold

        # adjust the score to match 0,1
        smin = min(p_test)
        smax = max(p_test)
        sub['score_norm'] = (p_test - smin) / (smax - smin)

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

#sig.loc[:,'bdt'] = np.zeros(sig.shape[0]).astype(float)
#bkg.loc[:,'bdt'] = np.zeros(bkg.shape[0]).astype(float)
for i, iclas in classifiers.items():
    
    print (' evaluating %d/%d classifier' %(i+1, n_class))
    
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))  
    
    data.loc[:,'bdt_fold%d_score' %i] = iclas.predict_proba(data[bdt_inputs])[:, 1]
    data.loc[data['bdt_to_apply'] == i,'bdt_score'] = iclas.predict_proba(data.loc[data['bdt_to_apply'] == i, bdt_inputs])[:, 1]
    data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training'] += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs])[:, 1]/(n_class-1)

    #sig.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(sig[bdt_inputs])[:, 1]
    #bkg.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(bkg[bdt_inputs])[:, 1]
    #sig.loc[:,'bdt'] += iclas.predict_proba(sig[bdt_inputs])[:, 1] / n_class
    #bkg.loc[:,'bdt'] += iclas.predict_proba(bkg[bdt_inputs])[:, 1] / n_class

# save data & MC as root trees
if(args.save_output):
    print(data.columns)
    # convert data to dictionary with numpy arrays 
    out_data = {col: data[col].values for col in data.columns}

    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 0').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_%s_%s.root'%(tag, 'blind' if not args.unblind else 'open'))
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 1').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_%s.root'%(tag))

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
plt.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
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

plt.savefig('%sovertrain_%s.pdf' %(args.plot_outdir,tag))
plt.savefig('%sovertrain_%s.png' %(args.plot_outdir,tag))

plt.yscale('log')

plt.savefig('%sovertrain_log_%s.pdf' %(args.plot_outdir, tag))
plt.savefig('%sovertrain_log_%s.png' %(args.plot_outdir, tag))

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
plt.savefig('%sfeat_importance_%s.pdf' %(args.plot_outdir,tag))
plt.savefig('%sfeat_importance_%s.png' %(args.plot_outdir,tag))
plt.clf()

