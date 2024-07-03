import argparse
import logging
import sys
import datetime
import os

import warnings, uproot, time, json, math
from xgboost import XGBClassifier
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

import matplotlib.pyplot  as plt

# from my config
from config import *



def objective(trial):
    bdt_inputs = features + ['tauEta']
    all_inputs = bdt_inputs + ['train_weight']
    print(f'\n [...] new optimization starting\n')
    train_x, valid_x, train_y, valid_y = train_test_split(data[all_inputs], data.target, test_size=0.25)
    # hyperparameters of the model
    parameters = {
        'booster'               : 'gbtree',
        'objective'             : 'binary:logistic',
        'device'                : 'cuda',       #to run on GPUs
        'tree_method'           :  'hist',      # should be same as default 'auto'
        'n_estimators'          :  trial.suggest_int('n_estimators', 5000, 20000, step=5000),       # number of sequential trees to be modeled
        'max_depth'             :  trial.suggest_int('max_depth', 3, 9, step=2),                    # max depth of a single tree
        'eta'                   :  trial.suggest_float("eta", 1e-3, 1.0, log=True),                 # step size shrinkage used in update to prevent overfitting 
        'subsample'             :  trial.suggest_float("subsample", 0.5, 1.0, step = 0.1),          # subsample ratio of the training instance at every boosting iteration
        'colsample_bytree'      :  trial.suggest_float('colsample_bytree', 0.5, 1.0, step = 0.1),   # subsample ratio of columns when constructing each tree
        'min_child_weight'      :  trial.suggest_int('min_child_weight', 1, 100, step=10),          # min sum of instance weight (hessian) needed in a child
        'gamma'                 :  trial.suggest_float('gamma', 1e-8, 1.0, log = True),             # min loss reduction required to make a further partition on a leaf node of the tree
        # scale_pos_weight      :  0.5,                                                             # control the balance of positive and negative weights
        'reg_alpha'             :  trial.suggest_float('reg_alpha', 1e-8, 1.0, log = True),         # L1 regularization term on weights [0, inf)
        'reg_lambda'            :  trial.suggest_float('reg_lambda', 1e-8, 1.0, log = True),        # L2 regularization term on weights [0, inf)
        'seed'                  :  args.seed,
        'verbosity'             :  0,
        'use_label_encoder'     : False,
        'eval_metric'           : 'auc',
        'early_stopping_rounds' : 100, #100
    }
    parameters_list.append(parameters)

    clf = XGBClassifier(**parameters)
    clf.fit(
        train_x[bdt_inputs], train_y,
        eval_set              = [(valid_x[bdt_inputs], valid_y)],
        verbose               = False,
        sample_weight         = train_x.train_weight,
         
    )

    #pred_labels = np.rint(clf.predict(valid_x))
    #accuracy    = accuracy_score(valid_y, pred_labels)
    train_pred_proba = clf.predict_proba(train_x[bdt_inputs])[:,1]
    auc_train        = roc_auc_score(train_y, train_pred_proba)
    auc_score_trainV.append(auc_train)
    val_pred_proba   = clf.predict_proba(valid_x[bdt_inputs])[:,1]
    auc_val          = roc_auc_score(valid_y, val_pred_proba)
    auc_score_testV.append(auc_val)

    return auc_val





parser = argparse.ArgumentParser()
# I/O
parser.add_argument('--prep_sig',                                                                   help='preprocessed signal input')
parser.add_argument('--prep_bkg',                                                                   help='preprocessed background input')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                               help='cut over 3muons SV displacement significance')
parser.add_argument('-s','--seed',      default=  3872, type = int,                                 help='set random state for reproducible results')
parser.add_argument('-N','--Ntrials',   default=  100,  type = int,                                 help='number of trials by optuna')
parser.add_argument('--tag',                                                                        help='tag for outputs')
parser.add_argument('--debug',          action = 'store_true' ,                                     help='set it to have useful printout')
args    = parser.parse_args()
print('\n')

# IMPORTING DATA

print('[i] import preprocessed data')
tree_name = 'tree_w_BDT'
base_selection = f'(tau_fit_mass > {mass_range_lo} & tau_fit_mass < {mass_range_hi} ) & (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu) & (tau_Lxy_sign_BS >{args.LxySign_cut})'
sig_selection  = base_selection
bkg_selection  = base_selection + f' & (tau_fit_mass < {blind_range_lo} | tau_fit_mass > {blind_range_hi})'
print('\n---------------------------------------------')
print('[!] base-selection   : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] data-selection   : %s'%bkg_selection)
print('---------------------------------------------')

signals = args.prep_sig
if not os.path.exists(signals):
    print(f'[ERROR] cannot find preprocessed signal input {signals}')
    exit(-1)
backgrounds = args.prep_bkg
if not os.path.exists(backgrounds):
    print(f'[ERROR] cannot find preprocessed background input {backgrounds}')
    exit(-1)

print('[+] adding WTau3Mu SIGNAL samples')
sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
print(' SIGNAL      : %s entries passed selection' %len(sig.index))
print('[+] adding data-sidebands background samples')
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds, branches).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
print(' DATA-SB BACKGROUND  : %s entries passed selection' %len(bkg.index))

data = pd.concat([sig, bkg]).sample(frac = 1, random_state = args.seed).reset_index(drop=True)

# SET-UP OUTPUT TAGS
out_dir = './optimization' 
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
    print(f'[i] created directory for optimization outputs : {out_dir}')
job_tag = f'OptunaXGBopt_LxyS{round(args.LxySign_cut,1)}' + (f'_{tag}' if args.tag else '') + '_' + datetime.date.today().strftime('%Y%b%d')

# START OPTIMIZATION
# add a stream handler of stdout for optuna
optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))
# create the optimizer
study = optuna.create_study(
    study_name=f'optimize_LxyS{round(args.LxySign_cut,1)}',
    #storage='sqlite:///optim_LxyS1p5_try.db',
    direction="maximize",
    )

# save the optimization progrsses
parameters_list = []
auc_score_testV = []
auc_score_trainV= []

# run optimization & evaluate the comuputing time
start_time = time.time()
study.optimize(objective, n_trials = args.Ntrials)
end_time = time.time()
elapsed_time = end_time - start_time

# report and save to json file
print(f'\n[=] Optuna has done is job in {round(elapsed_time/60, 2)} min ')
print("\tnumber of finished trials: ", len(study.trials))
print("\tbest trial:")
best_trial = study.best_trial
best_trial_index = best_trial.number

print("  Value: {}".format(best_trial.value))
print("  Params: ")
for key, value in best_trial.params.items():
    print("    {}: {}".format(key, value))

with open(f'{out_dir}/BestTrial_{job_tag}.json', 'w') as fp:
    json.dump(best_trial.params, fp)


# plotting

# scatter plot training VS test score
print(auc_score_testV)
plt.scatter(auc_score_testV, auc_score_trainV, color=['blue'] * len(auc_score_testV), marker='.', label='trainings')
plt.scatter(auc_score_testV[best_trial_index], auc_score_trainV[best_trial_index], color='red', marker='o', label='best training')

min_val = min(min(auc_score_testV), min(auc_score_trainV)) - 0.005
max_val = 1.0 #max(max(auc_score_testV), max(auc_score_trainV))
plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='gray', label='bisector')

plt.xlabel('auc_score_test')
plt.ylabel('auc_score_train')

plt.xlim(min_val, max_val)
plt.ylim(min_val, max_val) 

plt.legend()
# Visualizzazione del plot
plt.savefig(f'{out_dir}/TrialHistory_{job_tag}.png')
