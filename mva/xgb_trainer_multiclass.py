import ROOT 
import matplotlib.pyplot as plt
ROOT.EnableImplicitMT()
import argparse
import datetime 
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance

from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score, balanced_accuracy_score 
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

from scipy.stats import ks_2samp
from collections import OrderedDict, Counter
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
rebalance = True

# ------------ DEFINE SELECTIONS ------------ # 
if not rebalance:
    base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f ) & (HLT_isfired_Tau3Mu | HLT_isfired_DoubleMu)'%(mass_range_lo,mass_range_hi)
else:
    base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f ) & (HLT_isfired_Tau3Mu | HLT_isfired_DoubleMu)'%(mass_range_lo-1.0,mass_range_hi+1.0)
sig_selection  = base_selection
bkg_selection  = base_selection + ('& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(blind_range_lo, blind_range_hi) if not (args.unblind) else '')

print('\n---------------------------------------------')
print('[!] base-selection   : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] data-selection   : %s'%bkg_selection)
print('---------------------------------------------')

# ------------ INPUT DATASET ------------ # 

signals     = [
    '../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap.root',
    '../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap.root',
    '../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap.root',
    '../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap.root',
]
background_W3Mu =[
    '../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_privW3MuNu.root'
]
data_path = '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/'
backgrounds_dataSB  = [
    #2022
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_DoubleMu.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_DoubleMu.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_DoubleMu.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_DoubleMu.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_DoubleMu.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_DoubleMu.root',
    #2023
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023B_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023C_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_DoubleMu.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023D_HLT_DoubleMu.root',
]

tree_name = 'WTau3Mu_tree'
print('[+] adding signal and backgrund samples')
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection).Define('weight', 'lumi_factor')
sig = pd.DataFrame( sig_rdf.AsNumpy() )
bkgD_rdf = ROOT.RDataFrame(tree_name, backgrounds_dataSB, branches).Filter(bkg_selection).Define('weight', '1.0')
bkgD = pd.DataFrame( bkgD_rdf.AsNumpy() )
bkgW3m_rdf = ROOT.RDataFrame(tree_name, background_W3Mu, branches).Filter(sig_selection).Define('weight', 'lumi_factor')
bkgW3m =  pd.DataFrame( bkgW3m_rdf.AsNumpy() )

print('... processing input ...')
print(' Tau3Mu MC(sig)        : %s entries passed the selection' %sig_rdf.Count().GetValue())
print(' data SB  (bkg)        : %s entries passed the selection' %bkgD_rdf.Count().GetValue())
print(' W->3MuNu MC(bkg)      : %s entries passed the selection' %bkgW3m_rdf.Count().GetValue())
print('---------------------------------------------')


## DEFINE TARGETS
# (W) tau3mu - 0
#  data SB   - 1
#  W 3mu nu  - 2
sig.loc[:,'target']     = np.zeros(sig.shape[0]).astype(int)
bkgD.loc[:,'target']    = np.ones(bkgD.shape[0]).astype(int)
bkgW3m.loc[:,'target']  = 2 * np.ones(bkgW3m.shape[0]).astype(int)

## ETA BINS
if(args.debug):print(sig['tau_fit_eta'])
if(args.debug):print(tauEta(sig['tau_fit_eta'].values))
bdt_inputs = features + ['tauEta']
if(args.debug):print(bdt_inputs)
sig.loc[:,'tauEta']     = tauEta(sig['tau_fit_eta'])
bkgD.loc[:,'tauEta']    = tauEta(bkgD['tau_fit_eta'])
bkgW3m.loc[:,'tauEta']  = tauEta(bkgW3m['tau_fit_eta'])

if(args.debug):print(sig)
if(args.debug):print(bkgD)
if(args.debug):print(bkgW3m)
##########################################################################################
## REWEIGHT AND MAKE TAU MASS FLAT
########################################################################################## 

# [...]
########################################################################################## 

## CONCATENATE & SHUFFLE SIGNAL AND BACKGROUND
data = pd.concat([sig, bkgD, bkgW3m])
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

# define the BDT score columns for each category 
data.loc[:,'id'] = np.arange(len(data))
for i in range(kfold):
    data.loc[:,'bdt_fold%d_isTrainSet' %i]  = np.zeros(data.shape[0]).astype(int)
    data.loc[:,'bdt_fold%d_score' %i]       = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_to_apply']      = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_score_t3m']     = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_score_b']       = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_score_w3m']     = -1 * np.ones(data.shape[0]).astype(int)
data.loc[:,'bdt_training_t3m']  = np.zeros(data.shape[0]).astype(int)
data.loc[:,'bdt_training_b']    = np.zeros(data.shape[0]).astype(int)
data.loc[:,'bdt_training_w3m']  = np.zeros(data.shape[0]).astype(int)

# keep only the input features in train set
train = data[bdt_inputs+['tau_fit_mass','weight', 'target', 'id']]
train_target = data.target
counter = Counter(train_target)
print('** classes composition **')
for k,v in counter.items():
    per = v / len(train_target) * 100
    print('\tclass %d, n=%d (%.3f%%)' % (k, v, per))

if(args.debug) : print(train)

# k-Fold SPLITTING
skf = StratifiedKFold(n_splits=kfold, random_state=args.seed, shuffle=True)
if args.load_model is None:
    
    # .pkl file to save BDT weights
    classifier_file = open('classifiers/BDTclassifiers_kFoldMulticlass_%s.pck' % tag, 'wb')
    classifiers = OrderedDict()

    # define the classifier
    clf = XGBClassifier(
            booster          = 'gbtree',
            num_class        = 3,
            max_depth        = 5,
            learning_rate    = 0.01, 
            n_estimators     = 5000, #10000,
            verbosity        = 0,
            subsample        = 0.7,
            colsample_bytree = 0.8,
            min_child_weight = 50, #1E-6 * np.sum(train[train.id.isin(train_index)].weight),
            gamma            = 5, 
            seed             = args.seed,
            reg_alpha        = 5.0,
            reg_lambda       = 5.0,
            use_label_encoder=False,
            eval_metric      = 'mlogloss',
            objective        = 'multi:softprob',
            early_stopping_rounds = 30, #100
        )

    # https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
    # (K-1)/K to train 1/K to use in the analysis
    for i, (train_index, apply_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):
        # extract the trainset 
        kdataset = train[train.id.isin(train_index)]
        print('[fold %d/%d]' % (i + 1, kfold))
        print('  using %.2f %% of the full dataset'% (kdataset.shape[0]/train.shape[0]*100.))    
        
        # split the trainset in training and validation
        #   keep only data sidebands
        train_selection = train.id.isin(train_index)&((data.target == 0) | (data.target == 2) | ((data.target == 1) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi))))
        if (args.debug) : print('[T] training selection', train_selection)
        ktrain, kvalid = train_test_split(
                kdataset.loc[train_selection], 
                test_size=0.2, 
                random_state= args.seed)
        X_train, X_valid = ktrain[bdt_inputs], kvalid[bdt_inputs]
        y_train, y_valid = (ktrain['target']).values.astype(int), (kvalid['target']).values.astype(int)
        ## rebalance classes
        if rebalance :
            print('** rebalenced classes composition **')
            oversample = SMOTE()
            X_train, y_train = oversample.fit_resample(X_train, y_train)
            counter = Counter(y_train)
            for k,v in counter.items():
                per = v / len(y_train) * 100
                print('\tclass %d, n=%d (%.3f%%)' % (k, v, per))
        if(args.debug) : print(max(y_train))
        if(args.debug) : print(min(y_train))
        
        # save the training information
        data.loc[train_selection, 'bdt_fold%d_isTrainSet' %i] = 1
        data.loc[train.id.isin(apply_index), 'bdt_to_apply'] = i

        if(args.debug):print(data)
        
       # fit model 
        clf.fit(
            X_train, 
            y_train,
            eval_set              = [(X_train, y_train),(X_valid, y_valid)],
            verbose               = True,
            #sample_weight         = ktrain['weight'],
        )
        
        best_iteration = clf.get_booster().best_iteration
        print('[Fold %d/%d] - best iteration %d' %(i+1, kfold, best_iteration))
        classifiers[i] = clf
        
        # Predict on our test data (if early stopping in training best_iteration automatically used) 
        #       return (n_samples, n_classes) array

        print('[Fold %d/%d Prediciton:]' % (i + 1, kfold))
        # plot evaluation metric vs epochs
        results = clf.evals_result()
        epochs  = len(results['validation_0']['mlogloss'])
        x_axis  = range(0, epochs)
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(x_axis, results['validation_0']['mlogloss'], label='Train')
        ax.plot(x_axis, results['validation_1']['mlogloss'], label='Test')
        ax.set_yscale('log')
        ax.legend()
        plt.ylabel('mlogloss')
        plt.title('Fold number %d / %d'%(i+1, kfold))
        plt.savefig('%sevalMetricVSepochs_%s_fold%d.png' %(args.plot_outdir,tag, i+1))

        print('\n-------------------- Key Metrics --------------------')
        y_pred = clf.predict(X_valid)
        print('\nAccuracy: {:.2f}'.format(accuracy_score(y_valid, y_pred)))
        print('Balanced Accuracy: {:.2f}\n'.format(balanced_accuracy_score(y_valid, y_pred)))

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
    
    data.loc[:,'bdt_fold%d_score_t3m' %i] = iclas.predict_proba(data[bdt_inputs])[:, 0]
    data.loc[:,'bdt_fold%d_score_b'   %i] = iclas.predict_proba(data[bdt_inputs])[:, 1]
    data.loc[:,'bdt_fold%d_score_w3m' %i] = iclas.predict_proba(data[bdt_inputs])[:, 2]
    data.loc[data['bdt_to_apply'] == i,'bdt_score_t3m'] = iclas.predict_proba(data.loc[data['bdt_to_apply'] == i, bdt_inputs])[:, 0]
    data.loc[data['bdt_to_apply'] == i,'bdt_score_b']   = iclas.predict_proba(data.loc[data['bdt_to_apply'] == i, bdt_inputs])[:, 1]
    data.loc[data['bdt_to_apply'] == i,'bdt_score_w3m'] = iclas.predict_proba(data.loc[data['bdt_to_apply'] == i, bdt_inputs])[:, 2]
    data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training_t3m']  += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs])[:, 0]/(n_class-1)
    data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training_b']    += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs])[:, 1]/(n_class-1)
    data.loc[data['bdt_fold%d_isTrainSet' %i] == 1,'bdt_training_w3m']  += iclas.predict_proba(data.loc[data['bdt_fold%d_isTrainSet' %i] == 1, bdt_inputs])[:, 2]/(n_class-1)


# save data & MC as root trees
if(args.save_output):
    print(data.columns)
    # convert data to dictionary with numpy arrays 
    out_data = {col: data[col].values for col in data.columns}

    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 0').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_%s.root'%(tag))
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 1').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_%s_%s.root'%(tag, 'blind' if not args.unblind else 'open'))
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 2').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_W3MuNu_%s.root'%(tag))

if(args.load_model): exit(-1) 

exit(-1)
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

