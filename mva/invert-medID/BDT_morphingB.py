import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from mva import config

SAVE_MODEL = True  # save model to file
LOAD_MODEL = True
model_to_load = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/xgbBDTmodel_invID_nT15k_invIDopen.json'

# ---- INPUT SAMPLES ---- #
target_sample = config.data_bdt_samples['WTau3Mu']
#proxy_sample  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples//XGBout_invMedID_DATA_2022_invID-mu3.root'
proxy_sample  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples//XGBout_invMedID_DATA_2022_invID-mu2mu3.root'
if not os.path.exists(proxy_sample):
    raise FileNotFoundError(f"Proxy sample not found: {proxy_sample}")
if not os.path.exists(target_sample):
    raise FileNotFoundError(f"Target sample not found: {target_sample}")

# ---- OUTPUT ---- #
out_tag = 'nT15k_invIDopen'
output_sample = os.path.join(
    os.path.dirname(proxy_sample),
    #f'XGBout_invMedIDandSideBands_DATA_2022_invID-mu3_{out_tag}_reweight.root'
    f'XGBout_invMedIDandSideBands_DATA_2022_invID-mu2mu3_{out_tag}_reweight.root'
)
if os.path.exists(output_sample):
    print(f"[i] Output sample already exists: {output_sample}")
else:
    print(f"[i] Output sample will be saved to: {output_sample}")

model_file = None
if SAVE_MODEL and not LOAD_MODEL:
    model_file = os.path.join(os.path.dirname(proxy_sample), f'xgbBDTmodel_invID_{out_tag}.json')
    if os.path.exists(model_file):
        print(f"[i] Model file already exists: {model_file}")
    else:
        print(f"[i] Model will be saved to: {model_file}")

# ---- SELECTION ---- #
base_selection = '&'.join([
    config.base_selection,
    config.displacement_selection,
    #config.sidebands_selection,
    config.year_selection['2022'], #FIXME: 2022 only to try
])
real_data_selection = '&'.join([
    base_selection,
    config.sidebands_selection,
])

# ---- LOAD DATA ---- #
treename = 'tree_w_BDT'
target_rdf = ROOT.RDataFrame(treename, target_sample).Filter(real_data_selection)
proxy_rdf = ROOT.RDataFrame(treename, proxy_sample).Filter(base_selection)
Ntarget = target_rdf.Count().GetValue()
Nproxy = proxy_rdf.Count().GetValue()
frac = Nproxy / Ntarget if Ntarget > 0 else 0
print(f"[+] proxy & target sample loaded with {Nproxy} / {Ntarget} ({frac:.1f}) entries.")

target_df = pd.DataFrame(target_rdf.AsNumpy())
proxy_df  = pd.DataFrame(proxy_rdf.AsNumpy())
# use only 10% for test
#target_df = target_df.sample(frac=0.1, random_state=123456).reset_index(drop=True)
#proxy_df = proxy_df.sample(frac=0.1, random_state=123456).reset_index(drop=True)
#print(f"[+] Target sample has {len(target_df)} entries, Proxy sample has {len(proxy_df)} entries.")

# ----- PREPROCESSING ---- #
target_df["is_dataSB"] = np.ones(len(target_df)).astype(int)       # real background = 1
proxy_df["is_dataSB"] = np.zeros(len(proxy_df)).astype(int)  # flipped ID = 0

full_df = pd.concat([target_df, proxy_df], ignore_index=True)
full_df = full_df.sample(frac=1, random_state=123456).reset_index(drop=True)
print(f"[+] Combined dataset has {len(full_df)} entries.")

input_features = config.features + ['tau_fit_eta']
if not LOAD_MODEL:
    # balance the dataset
    if frac > 1.0:
        # if proxy sample is larger than target, downsample proxy
        train_df = pd.concat([
            target_df,
            proxy_df.sample(frac=1.0 / frac, random_state=123456).reset_index(drop=True)
        ], ignore_index=True)
    else:
        # if target sample is larger than proxy, downsample target
        train_df = pd.concat([
            target_df.sample(frac=frac, random_state=123456).reset_index(drop=True),
            proxy_df
        ], ignore_index=True)
    print(f"[+] Training dataset has {len(train_df)} entries after balancing.")
    print(f"    target sample: {len(target_df)}, proxy sample: {len(proxy_df)}")

    # ---- TRAINING ---- #


    # parameters
    parameters = {
            'booster'               :  'gbtree',
            'device'                :  'cuda',
            'tree_method'           :  'hist',
            'objective'             :  'binary:logistic',
            'eval_metric'           :  'logloss',
            #hyperparameters
            'n_estimators'          :  15000,   # number of sequential trees to be modeled
            'max_depth'             :  10,       # max depth of a single tree
            'eta'                   :  0.01,    # step size shrinkage used in update to prevent overfitting (learning rate) 
            'subsample'             :  0.7,     # subsample ratio of the training instance at every boosting iteration
            'colsample_bytree'      :  0.7,     # subsample ratio of columns when constructing each tree
            'min_child_weight'      :  50,      # min sum of instance weight (hessian) needed in a child
            'gamma'                 :  5,       # min loss reduction required to make a further partition on a leaf node of the tree
            # scale_pos_weight      :  0.5,     # control the balance of positive and negative weights
            'reg_alpha'             :  5.0,     # L1 regularization term on weights [0, inf)
            'reg_lambda'            :  5.0,     # L2 regularization term on weights [0, inf)
            'early_stopping_rounds' :  100,
            'use_label_encoder'     :  False,
            'seed'                  :  12345,
            'verbosity'             :  1,
        }

    X = train_df[input_features].copy()
    y = train_df["is_dataSB"].copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
    print(f"[+] Training set has {len(X_train)} entries, test set has {len(X_test)} entries.")

    model = xgb.XGBClassifier(**parameters)
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train),(X_test, y_test)],
        verbose=True,
    )
    # save model
    if SAVE_MODEL : 
        model.save_model(model_file)
        print(f"[+] Model saved to {model_file}")
else:
    # load model
    model = xgb.XGBClassifier()
    model.load_model(model_to_load)
    print(f"[+] Model loaded from {model_to_load}")

# ---- EVALUATION ---- #
proba = model.predict_proba(full_df[input_features])[:, 1]
full_df.loc[:, 'p_data'] = proba
print("[+] Proxy sample probabilities computed.")
# save to R dataframe and snapshot
out_data = {col : full_df[col].values for col in full_df.columns}
out_rdf  = ROOT.RDF.MakeNumpyDataFrame(out_data).Snapshot(treename, output_sample)
print(f"[+] Output sample saved to {output_sample}")