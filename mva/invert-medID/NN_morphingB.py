import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from mva import config


NORM_INPUTS = False

# ---- INPUT SAMPLES ---- #
target_sample = config.data_bdt_samples['WTau3Mu']
proxy_sample  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples//XGBout_invMedID_DATA_2022_invID-mu3.root'
if not os.path.exists(proxy_sample):
    raise FileNotFoundError(f"Proxy sample not found: {proxy_sample}")
if not os.path.exists(target_sample):
    raise FileNotFoundError(f"Target sample not found: {target_sample}")

# ---- SELECTION ---- #
base_selection = '&'.join([
    config.base_selection,
    config.displacement_selection,
    config.sidebands_selection,
    config.year_selection['2022'], #FIXME: 2022 only to try
])

# ---- LOAD DATA ---- #
treename = 'tree_w_BDT'
target_rdf = ROOT.RDataFrame(treename, target_sample).Filter(base_selection)
proxy_rdf = ROOT.RDataFrame(treename, proxy_sample).Filter(base_selection)
Ntarget = target_rdf.Count().GetValue()
Nproxy = proxy_rdf.Count().GetValue()
frac = Nproxy / Ntarget if Ntarget > 0 else 0
print(f"[+] proxy & target sample loaded with {Nproxy} / {Ntarget} ({frac:.1f}) entries.")


target_df = pd.DataFrame(target_rdf.AsNumpy())
proxy_df  = pd.DataFrame(proxy_rdf.AsNumpy())
# use only 10% for test
target_df = target_df.sample(frac=0.1, random_state=123456).reset_index(drop=True)
proxy_df = proxy_df.sample(frac=0.1, random_state=123456).reset_index(drop=True)
print(f"[+] Target sample has {len(target_df)} entries, Proxy sample has {len(proxy_df)} entries.")

# ----- PREPROCESSING ---- #
target_df["label"] = np.ones(len(target_df)).astype(int)       # real background = 1
proxy_df["label"] = np.zeros(len(proxy_df)).astype(int)  # flipped ID = 0

df = pd.concat([target_df, proxy_df], ignore_index=True)
df = df.sample(frac=1, random_state=123456).reset_index(drop=True)
print(f"[+] Combined dataset has {len(df)} entries.")
print(df.head())


# ---- TRAINING ---- #
input_features = config.features + ['tau_fit_eta']

X = df[input_features].copy()
y = df["label"].copy()
# normalize inputs  X = (X - X.mean()) / X.std()
if NORM_INPUTS:
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
print(f"[+] Training set has {len(X_train)} entries, test set has {len(X_test)} entries.")

# model definition
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense( 1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# training
model.fit(X_train, y_train, 
          epochs=10, batch_size=256, 
          validation_data=(X_test, y_test), 
          verbose=1
          )

# ---- EVALUATION ---- #
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"[+] Model evaluation: Loss = {loss:.4f}, Accuracy = {accuracy:.4f}")
# ---- PREDICTIONS ---- #
epsilon = 1e-6
proba = model.predict(df[input_features]).flatten()
proba = np.clip(proba, epsilon, 1 - epsilon)

df.loc[:,'sb_prob'] = proba
df.loc[:,'sb_weight'] = 1.0 / (1.0 - df['sb_prob'])

# ---- SAVE OUTPUT ---- #
out_data = {col: df[col].values for col in df.columns}
out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Snapshot(treename, 'reweight-test.root')
