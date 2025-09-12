import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import OrderedDict

import matplotlib.pyplot as plt

import os, sys
from sys import argv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from mva import config


if __name__ == '__main__':

    '''
    usage : python BDT_model_plotting.py <year> <muon-to-invert[mu3, mu2mu3]>
    '''
    year = argv[1] if len(argv) > 1 else '2022'
    muontoinv = argv[2] if len(argv) > 2 else 'mu2mu3' # 'mu3' or 'mu2mu3'
    
# ---- INPUTS ---- #
    print(f"  --- LOADING MODEL --- ")
    model_to_load = f'/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/xgbBDTmodel_{year}_invID-{muontoinv}_nT15k_invIDopen.json'
    # load model
    model = xgb.XGBClassifier(n_jobs=-1)
    model.load_model(model_to_load)
    print(f"[+] Model loaded from {model_to_load}")
    plotdir = f'invID-{muontoinv}/plot'
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
        print(f"[i] Created plot directory: {plotdir}")
    out_tag = os.path.basename(model_to_load).replace('xgbBDTmodel_','').replace('.json','')

# ---- PLOTS ---- #

    results   = model.evals_result()
    best_iter = model.get_booster().best_iteration
    # learning curves
    training_loss = results['validation_0']['logloss']
    test_loss     = results['validation_1']['logloss']
    rounds        = range(len(training_loss))
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, training_loss, label='Training Loss')
    plt.plot(rounds, test_loss, label='Test Loss')
    plt.axvline(x=best_iter, color='r', linestyle='--', label='Best Iteration')
    plt.xlabel('Boosting Rounds')
    plt.ylabel('Log Loss')
    plt.yscale('log')
    plt.savefig(f'{plotdir}/learning_curve_{out_tag}.png')
    plt.savefig(f'{plotdir}/learning_curve_{out_tag}.pdf')

    # feature importance
    fscores = model.get_booster().get_fscore()
    plt.figure(figsize=(8,6))
    totalsplits = sum(float(value) for value in fscores.values())
    for k, v in fscores.items():
        fscores[k] = float(v)/float(totalsplits) 
    print('Feature importances (relative F-score):')
    [print(f' {k} : {v}') for k,v in fscores.items()]
    orderedfscores = OrderedDict(sorted(fscores.items(), key=lambda x : x[1], reverse=False ))

    plt.xlabel('relative F-score')


    bars = [config.labels[k] for k in orderedfscores.keys()]
    y_pos = np.arange(len(bars))
    
    # Create horizontal bars
    plt.barh(y_pos, orderedfscores.values())
    
    # Create names on the y-axis
    plt.yticks(y_pos, bars)
    plt.tight_layout()
    plt.savefig(f'{plotdir}/feature_importance_{out_tag}.png')
    plt.savefig(f'{plotdir}/feature_importance_{out_tag}.pdf')
    