    # import pandas
# import root_numpy #(available until ROOT 6.09)
import ROOT 
ROOT.EnableImplicitMT()
import argparse
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
# import matplotlib as mpl ; mpl.use('Agg')
import matplotlib.pyplot as plt
# sns.set(style="whitegrid", font_scale=2)
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics         import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold
#from sklearn.externals       import joblib

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
tag = args.tag

 # ------------ APPLY SELECTIONS ------------ # 
base_selection = '(tau_fit_mass > %.2f & tau_fit_mass < %.2f )'%(mass_range_lo,mass_range_hi) 
sig_selection  = base_selection 
bkg_selection  = base_selection + ('& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(blind_range_lo, blind_range_hi) if not (args.unblind) else '')

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

##########################################################################################

signals     = [
    '/afs/cern.ch/user/c/cbasile/CMSSW_12_4_11_patch3-Tau3Mu/src/Tau3MuAnalysis/PreliminaryStudies/outRoot/recoKinematicsT3m_MC_2022EE_reMini_HLT_Tau3Mu.root',
]

backgrounds  = [
    #'/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022E.root',
    #'/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root',
    #'/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022G.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root',
    '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022G.root',
]

tree_name = 'Tau3Mu_HLTemul_tree'
mc_factor = MC_norm_factor_dict['2022reMini']  
print('[!] MC normalization factor = %.3e'%mc_factor)
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection).Define('weight', '%f'%mc_factor)
#sig = pd.DataFrame( root_numpy.root2array(signals    , 'tree', branches  = branches + ['weight'], selection = sig_selection) )
sig = pd.DataFrame( sig_rdf.AsNumpy() )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds, branches).Filter(bkg_selection).Define('weight', '1')
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
if(args.debug):print(bkg)
#bkg = pd.DataFrame( root_numpy.root2array(backgrounds, 'tree', branches  = branches + ['weight'], selection = bkg_selection) )

print('... processing input ...')
print(' SIGNAL : %s entries passed the selection' %sig_rdf.Count().GetValue())
print(' BACKGROUND : %s entries passed the selection' %bkg_rdf.Count().GetValue())
print('---------------------------------------------')

## DEFINE TARGETS

sig.loc[:,'target'] = np.ones (sig.shape[0]).astype(int)
bkg.loc[:,'target'] = np.zeros(bkg.shape[0]).astype(int)

## ETA BINS
if(args.debug): print(sig['tau_fit_eta'])
if(args.debug): print(tauEta(sig['tau_fit_eta'].values))
bdt_inputs = features + ['tauEta']
if(args.debug): print(bdt_inputs)
sig.loc[:,'tauEta'] = tauEta(sig['tau_fit_eta'])
bkg.loc[:,'tauEta'] = tauEta(bkg['tau_fit_eta'])

##########################################################################################
## REWEIGHT AND MAKE TAU MASS FLAT
########################################################################################## 

# [...]
########################################################################################## 

data = pd.concat([sig, bkg])
data = data.sample(frac = 1, random_state = args.seed).reset_index(drop=True)
check_for_nan = data.isnull().values.any()
print ("check for NaN " + str(check_for_nan))
if (check_for_nan):
    data = data.dropna()
    check_for_nan = data.isnull().values.any()
    print ("check again for NaN " + str(check_for_nan))
data.loc[:,'id'] = np.arange(len(data))
if(args.debug):print(data)
train, test = train_test_split(data, test_size=0.4, random_state= args.seed)
kfold = 5 # DA CAMBIARE 
skf = StratifiedKFold(n_splits=kfold, random_state=args.seed, shuffle=True)


if args.load_model is None:
    sub = pd.DataFrame()
    sub['id']     = test.id
    sub['target'] = test.target
    sub['score']  = np.zeros_like(test.id)

    classifier_file = open('classifiers_%s.pck' % tag, 'wb')
    classifiers = OrderedDict()

    # https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
    for i, (train_index, test_index) in enumerate(skf.split(train[bdt_inputs].values, train['target'].values)):
    #     if i>2: break
        print('[Fold %d/%d]' % (i + 1, kfold))    
        X_train, X_valid = train[train.id.isin(train_index)][bdt_inputs], train[train.id.isin(test_index)][bdt_inputs]
        y_train, y_valid = (train[train.id.isin(train_index)]['target']).values.astype(int), (train[train.id.isin(test_index)]['target']).values.astype(int)
        print(max(y_train))
        print(min(y_train))
        
        clf = XGBClassifier(
            booster          = 'gbtree',
            max_depth        = 5,
            learning_rate    = 0.01, 
            n_estimators     = 1000, #10000,
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
            early_stopping_rounds = 80, #100
            eval_metric           = 'auc',
            verbose               = True,
            #sample_weight         = train['weight'],
        )
        
        best_iteration = clf.get_booster().best_iteration
        print('[Fold %d/%d] - best iteration %d' %(i+1, kfold, best_iteration))
        classifiers[i] = clf
        
        print('[Fold %d/%d Prediciton:]' % (i + 1, kfold))
        # Predict on our test data
        # to use the best iteration 
        p_test = clf.predict_proba(test[bdt_inputs])[:, 1]
        sub['score'] += p_test/kfold

        # adjust the score to match 0,1
        smin = min(p_test)
        smax = max(p_test)

        sub['score_norm'] = (p_test - smin) / (smax - smin)

        print ('round %d' %(i+1))
        print ('\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_norm'] - sub['target']))/len(sub)))
        print ('\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_norm'] - sub[sub.target>0.5]['target']))/len(sub)))
        print ('\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_norm'] - sub[sub.target<0.5]['target']))/len(sub)))

        smin = min(sub['score'])
        smax = max(sub['score'])
        
        sub['score_i'] = (sub['score'] - smin) / (smax - smin)

        print ('global score as of round %d' %(i+1))
        print ('\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_i'] - sub['target']))/len(sub)))
        print ('\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_i'] - sub[sub.target>0.5]['target']))/len(sub)))
        print ('\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_i'] - sub[sub.target<0.5]['target']))/len(sub)))

    pickle.dump(classifiers, classifier_file)
    classifier_file.close()
else :
    print('[+] load model from %s'%args.load_model)
    with open(args.load_model, 'rb') as f:
        classifiers = pickle.load(f)
##########################################################################################

n_class = len(classifiers)
print(" Number of splits %d"%n_class)

train.loc[:,'bdt'] = np.zeros(train.shape[0]).astype(float)
test.loc[:,'bdt'] = np.zeros(test.shape[0]).astype(float)
sig.loc[:,'bdt'] = np.zeros(sig.shape[0]).astype(float)
bkg.loc[:,'bdt'] = np.zeros(bkg.shape[0]).astype(float)

for i, iclas in classifiers.items():
    print (' evaluating %d/%d classifier' %(i+1, n_class))
    best_iteration = iclas.get_booster().best_iteration
    print('\tbest iteration %d' %(best_iteration))  
    train.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(train[bdt_inputs])[:, 1]
    test.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(test [bdt_inputs])[:, 1]
    sig.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(sig[bdt_inputs])[:, 1]
    bkg.loc[:,'bdt_fold%d' %i] = iclas.predict_proba(bkg[bdt_inputs])[:, 1]

    train.loc[:,'bdt'] += iclas.predict_proba(train[bdt_inputs])[:, 1] / n_class
    test.loc[:,'bdt'] += iclas.predict_proba(test [bdt_inputs])[:, 1] / n_class
    sig.loc[:,'bdt'] += iclas.predict_proba(sig[bdt_inputs])[:, 1] / n_class
    bkg.loc[:,'bdt'] += iclas.predict_proba(bkg[bdt_inputs])[:, 1] / n_class


if(args.save_output):
    # convert dat ato dictionary with numpy arrays 
    print(sig.columns)
    sig_out_data = {col: sig[col].values for col in sig.columns}
    sig_out_rdf = ROOT.RDF.MakeNumpyDataFrame(sig_out_data).Filter('bdt > 0.0').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_%s.root'%(args.tag))
    bkg_out_data = {col: bkg[col].values for col in bkg.columns}
    bkg_out_rdf = ROOT.RDF.MakeNumpyDataFrame(bkg_out_data).Filter('bdt > 0.0').Snapshot('tree_w_BDT', '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_%s_%s.root'%(args.tag, 'blind' if not args.unblind else 'open'))

if(args.load_model): exit(-1) 
##########################################################################################
#####   ROC CURVE
##########################################################################################
plt.clf()

cuts_to_display = [0.500, 0.990, 0.995, 0.999]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
plt.plot(xy, xy, color='grey', linestyle='--')
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.xscale('log')

fpr, tpr, wps = roc_curve(test.target, test.bdt, sample_weight=test.weight)
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

fpr, tpr, wps = roc_curve(train.target, train.bdt, sample_weight=train.weight)
plt.plot(fpr, tpr, label='train sample', color='r')

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]))

print ('ROC AUC train ', roc_auc_score(train.target, train.bdt, sample_weight=train.weight))
print ('ROC AUC test  ', roc_auc_score(test.target , test.bdt , sample_weight=test.weight))

plt.legend(loc='best')
plt.grid()
plt.title('ROC')
plt.tight_layout()
plt.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
plt.clf()

roc_file = open('roc_%s.pck' % tag, 'wb')
pickle.dump((tpr, fpr), roc_file)
roc_file.close()


##########################################################################################
#####   OVERTRAINING TEST
##########################################################################################
train_sig = train[train.target>0.5].bdt
train_bkg = train[train.target<0.5].bdt

test_sig = test[test.target>0.5].bdt
test_bkg = test[test.target<0.5].bdt

low  = 0
high = 1
low_high = (low,high)
bins = 50


#################################################
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
    label='S (test)'
)

#################################################
#sns.distplot(train_sig, bins=bins, kde=False, rug=False, norm_hist=True, hist_kws={"alpha": 0.5, "color": "r"}, label='S (train)')
sns.histplot(train_sig, bins=bins, kde=False, stat='probability', alpha = 0.5, color = "r", label='S (train)')

#################################################
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

#################################################
#sns.distplot(train_bkg, bins=bins, kde=False, rug=False, norm_hist=True, hist_kws={"alpha": 0.5, "color": "b"}, label='B (train)')
sns.histplot(train_bkg, bins=bins, kde=False, stat='probability', alpha = 0.5, color = "b", label='B (train)')

#################################################
plt.xlabel('BDT output')
plt.ylabel('Arbitrary units')
plt.legend(loc='best')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))

# train_sig_w = np.ones_like(train_sig) * 1./len(train_sig)
# train_bkg_w = np.ones_like(train_bkg) * 1./len(train_bkg)
# test_sig_w  = np.ones_like(test_sig)  * 1./len(test_sig )
# test_bkg_w  = np.ones_like(test_bkg)  * 1./len(test_bkg )
# 
# ks_sig = ks_w2(train_sig, test_sig, train_sig_w, test_sig_w)
# ks_bkg = ks_w2(train_bkg, test_bkg, train_bkg_w, test_bkg_w)
# plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig * 100., '%', ks_bkg * 100., '%'))

plt.savefig('%sovertrain_%s.pdf' %(args.plot_outdir,tag))
plt.savefig('%sovertrain_%s.png' %(args.plot_outdir,tag))

plt.yscale('log')

plt.savefig('%sovertrain_log_%s.pdf' %(args.plot_outdir, tag))
plt.savefig('%sovertrain_log_%s.png' %(args.plot_outdir, tag))

plt.clf()

###############################8##########################################################
#####   FEATURE IMPORTANCE
##########################################################################################
fscores = OrderedDict(zip(bdt_inputs, np.zeros(len(bdt_inputs))))
#fscores = pd.Series(np.zeros(len(bdt_inputs)).astype(float), index = bdt_inputs)
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
# plot_importance(clf)
plt.tight_layout()
plt.savefig('%sfeat_importance_%s.pdf' %(args.plot_outdir,tag))
plt.savefig('%sfeat_importance_%s.png' %(args.plot_outdir,tag))
plt.clf()

