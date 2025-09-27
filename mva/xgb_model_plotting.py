import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import OrderedDict
import pickle, json
import matplotlib.pyplot as plt
import argparse

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from mva import config
from plots.color_text import color_text as ct

FONTSIZE = 16

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='XGBoost model plotting')
    parser.add_argument('--model',      dest='model',      
                        help='Path to the trained model', 
                        required=True)
    parser.add_argument('-k', '--kFolds',
                        dest='kFolds',      
                        help='Number of folds for cross-validation', 
                        default=5, type=int)
    parser.add_argument('--signal',     dest='signal',
                        help='Signal w/ BDT applied', 
                        default='Tau3Mu', type=str)
    parser.add_argument('--data',     dest='data',
                        help='Data w/ BDT applied', 
                        default='data', type=str)
    parser.add_argument('--outdir',   dest='outdir',
                        help='Output directory', 
                        default='.', type=str)
    parser.add_argument('--tag',     dest='tag',
                        help='Tag for output files', 
                        default='', type=str)
    args = parser.parse_args()
    
    kFolds = args.kFolds
    
# ---- INPUTS ---- #
    print(f"{ct.BOLD}--- LOADING MODEL ---{ct.END}")
    model_to_load = args.model
    if not os.path.isfile(model_to_load):
        raise FileNotFoundError(f"Model file not found: {model_to_load}")
    # load single model
    if kFolds == 1 and model_to_load.endswith('.json'):
        model = xgb.XGBClassifier(n_jobs=-1)
        model.load_model(model_to_load)
        print(f"[+] Single model loaded from {model_to_load}")
    elif kFolds > 1 and model_to_load.endswith('.pck'):
        with open(model_to_load, 'rb') as f:
            model = pickle.load(f)
        print(f"[+] {kFolds}-fold model loaded from {model_to_load}")
    
# ---- OUTPUT ---- #
    plotdir = args.outdir
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
        print(f"[i] Created output directory: {plotdir}")
    out_tag = args.tag if args.tag else 'model_plots'

# ---- PLOTS ---- #
    # learning curves
    print(f"{ct.BOLD}--- AUC vs Boosting Rounds ---{ct.END}")
    for k, mod in model.items() if kFolds > 1 else [(0, model)]:
        print(f"  model {k+1}/{kFolds} --- ")
        this_out_tag = f"{out_tag}_fold{k+1}" if kFolds > 1 else out_tag
        
        results   = mod.evals_result()
        best_iter = mod.get_booster().best_iteration
        # learning curves
        training_loss = results['validation_0']['auc']
        test_loss     = results['validation_1']['auc']
        rounds        = range(len(training_loss))
        
        plt.figure(figsize=(8, 6))
        plt.plot(rounds, training_loss, label='TRAINING')
        plt.plot(rounds, test_loss, label='VALIDATION')
        plt.axvline(x=best_iter, color='r', linestyle='--', label='Best Iteration')
        plt.legend(
            loc='lower right',
            fontsize=FONTSIZE, frameon=False
        )
        plt.title(f'Learning Curve (fold {k+1}/{kFolds})' if kFolds > 1 else 'Learning Curve')
        plt.xlabel('Boosting Rounds', fontsize=FONTSIZE)
        plt.ylabel('AUC', fontsize=FONTSIZE)
        plt.ylim(0.96, 1.0)
        plt.grid(True, which='both', linestyle='--', linewidth=0.1, alpha=0.4)
        plt.savefig(f'{plotdir}/learning_curve_{this_out_tag}.png')
        plt.savefig(f'{plotdir}/learning_curve_{this_out_tag}.pdf')
        plt.close()

    # feature importance
    print(f"{ct.BOLD}--- Feature Importance ---{ct.END}")
    mod_inputs = []
    for i, mod in model.items():
        myscores = mod.get_booster().get_fscore()
        if i ==0 : 
            mod_inputs = list(myscores.keys())
            fscores = OrderedDict(zip(mod_inputs , np.zeros(len(mod_inputs))))
            print(f"[i] Features used in the model: {mod_inputs}")
        for jj in myscores.keys():
            fscores[jj] += myscores[jj]
    totalsplits = sum(float(value) for value in fscores.values())
    for k, v in fscores.items():
        fscores[k] = float(v)/float(totalsplits) 

    orderedfscores = OrderedDict(sorted(fscores.items(), key=lambda x : x[1], reverse=False ))
    [print(f"  {config.labels[k]:<30} : {v:.4f}") for k, v in orderedfscores.items()]
    bars = [config.labels[k] for k in orderedfscores.keys()]
    y_pos = np.arange(len(bars))
    
    # Create horizontal bars
    plt.figure(figsize=(10, 8))
    plt.barh(y_pos, orderedfscores.values())
    
    # Create names on the y-axis
    plt.xlabel('relative F-score', fontsize=FONTSIZE)
    plt.yticks(y_pos, bars, fontsize=FONTSIZE)
    plt.tight_layout()
    plt.savefig(f'{plotdir}/feature_importance_{out_tag}.png')
    plt.savefig(f'{plotdir}/feature_importance_{out_tag}.pdf')
    plt.close()

    # --------------------------------- #
    # -- LOAD DATA FOR TESTING ----- #
    import ROOT
    ROOT.EnableImplicitMT()
    # import dataset for validation
    print('[+] import signal and background for validation')
    tree_name = 'tree_w_BDT'
    signal = args.signal
    data = args.data
    if not os.path.exists(signal):
        print(f'{ct.RED}[ERROR]{ct.END} cannot find signal input {signal}')
        exit(-1)
    if not os.path.exists(data):
        print(f'{ct.RED}[ERROR]{ct.END} cannot find preprocessed background input {data}')
        exit(-1)
    
    branches_to_load = mod_inputs + ['target', 'bdt_to_apply', 'bdt_score', 'bdt_training']
    sig_rdf = ROOT.RDataFrame(tree_name, signal)
    sig = pd.DataFrame( sig_rdf.AsNumpy(branches_to_load) )
    bkg_rdf = ROOT.RDataFrame(tree_name, data).Filter(config.sidebands_selection)
    bkg = pd.DataFrame( bkg_rdf.AsNumpy(branches_to_load) )
    print(f"  SIGNAL: {sig.shape[0]} events")
    print(f"  DATA  : {bkg.shape[0]} events")
    
    data = pd.concat([sig, bkg], ignore_index=True)

    # ROC curve
    print(f"{ct.BOLD}--- ROC Curve ---{ct.END}")
    from sklearn.metrics import RocCurveDisplay, roc_curve, auc
    
    cuts_to_display = [0.600, 0.990, 0.995, 0.998]
    Y_true  = data['target']
    Y_train = data['bdt_training']
    Y_score = data['bdt_score']
    
    fpr_train, tpr_train, thresholds = roc_curve(Y_true, Y_train)
    fpr, tpr, thresholds = roc_curve(Y_true, Y_score)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, label=f'Analysis set (AUC = {auc(fpr, tpr):.3f})', color='blue')
    ax.plot(fpr_train, tpr_train, label=f'Training set (AUC = {auc(fpr_train, tpr_train):.3f})', color='red', linestyle='--')
    ax.grid(True)
    ax.set_xlabel('False Positive Rate', fontsize=FONTSIZE)
    ax.set_ylabel('True Positive Rate', fontsize=FONTSIZE)
    ax.tick_params(axis='both', which='major', labelsize=FONTSIZE)
    ax.legend(loc='lower right', fontsize=FONTSIZE, frameon=False)
    plt.xscale('log')
    plt.ylim(5e-4, 1.0)
    plt.savefig(f'{plotdir}/ROC_{out_tag}.png')
    plt.savefig(f'{plotdir}/ROC_{out_tag}.pdf')
    plt.close()
    print(f"[i] ROC curve saved to {plotdir}/ROC_{out_tag}.png")
    # dump to json
    roc_results = {
        'analysis': {
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'thresholds': thresholds.tolist(),
            'auc': auc(fpr, tpr)
        },
        'training': {
            'fpr': fpr_train.tolist(),
            'tpr': tpr_train.tolist(),
            'thresholds': thresholds.tolist(),
            'auc': auc(fpr_train, tpr_train)
        }
    }
    with open(f'{plotdir}/ROC_{out_tag}.json', 'w') as fp:
        json.dump(roc_results, fp, indent=4)
    print(f"[i] ROC curve results saved to {plotdir}/ROC_{out_tag}.json")

    # permutation importance
    print(f"{ct.BOLD}--- Permutation Importance ---{ct.END}")
    from sklearn.inspection import permutation_importance

    outfile = f'{plotdir}/permutation_importance_{out_tag}.json'

    if not os.path.exists(outfile):
        perm_results = {}
        N_REPEATS = 100
        for k, mod in model.items() if kFolds > 1 else [(0, model)]:
            print(f"  model {k+1}/{kFolds} --- ")
            this_out_tag = f"{out_tag}_fold{k+1}" if kFolds > 1 else out_tag
                
            data_mask = data[data.bdt_to_apply == k].index
            X_val = data.loc[data_mask, mod_inputs]
            y_val = data.loc[data_mask, 'target']
            #_, X_val, _, y_val = train_test_split(X, y, test_size=1.0, random_state=0, stratify=y)
            
            p_results = permutation_importance(mod, X_val, y_val, n_repeats=N_REPEATS, random_state=42, n_jobs=2)
            sorted_idx = p_results.importances_mean.argsort()
            perm_results['fold'+str(k)] = {}
            #for i in p_results.importances_mean.argsort()[::-1]:
            for f in sorted_idx[::-1]:  perm_results['fold'+str(k)][mod_inputs[f]] = (p_results.importances_mean[f], p_results.importances_std[f])

            # plot results
            fig, ax = plt.subplots(figsize=(10, 8))
            labels  = np.array([config.labels.get(col, col) for col in mod_inputs])
            ax.boxplot(p_results.importances[sorted_idx].T,
                        vert=False, labels=labels[sorted_idx])
            ax.set_title(f'FOLD {k+1}/{kFolds}' if kFolds > 1 else '', fontsize=FONTSIZE)
            ax.set_xlabel('Decrease in accuracy score', fontsize=FONTSIZE)
            ax.tick_params(axis='both', which='major', labelsize=FONTSIZE)

            plt.tight_layout()
            plt.savefig(f'{plotdir}/permutation_importance_{this_out_tag}.png')
            plt.savefig(f'{plotdir}/permutation_importance_{this_out_tag}.pdf')
            plt.close()
            print(f"[i] Permutation importance plot saved to {plotdir}/permutation_importance_{this_out_tag}.png")
        
        # save on jsonfile 
        with open(outfile, 'w') as fp:
            json.dump(perm_results, fp, indent=4)
        print(f"[i] Permutation importance results saved to {outfile}")

    else:
        print(f"[i] Permutation importance results already exist: {outfile}")
        # open json file
        with open(outfile, 'r') as fp:
            perm_results = json.load(fp)
        collective_val = OrderedDict(zip(mod_inputs, np.zeros(len(mod_inputs))))
        collective_err = OrderedDict(zip(mod_inputs, np.zeros(len(mod_inputs))))
        for fold in perm_results.keys():
            for k, v in perm_results[fold].items():
                #print(f"    {config.labels.get(k, k):<30} : {v[0]:.4f} +/- {v[1]:.4f}")
                collective_val[k] += v[0]/kFolds * 100.0 # in percentage
                collective_err[k] += (v[1]/kFolds)**2
        # bar plot of collective
        collective_err = {k: np.sqrt(v)*100. for k, v in collective_err.items()}
        [print(f"  {config.labels.get(k, k):<30} : {v:.4f} +/- {collective_err[k]:.4f}") for k, v in collective_val.items()]
        ordered_collective = OrderedDict(sorted(collective_val.items(), key=lambda x : x[1], reverse=False ))
        bars = [config.labels[k] for k in ordered_collective.keys()]
        y_pos = np.arange(len(bars))
        
        # Create horizontal bars
        plt.figure(figsize=(10, 8))
        plt.barh(y_pos, ordered_collective.values(), xerr=[collective_err[k] for k in ordered_collective.keys()], align='center', alpha=0.7, color = 'orange', ecolor='black', capsize=5)
        # Create names on the y-axis
        plt.xlabel('Decrease in accuracy score (%)', fontsize=FONTSIZE)
        plt.yticks(y_pos, bars, fontsize=FONTSIZE)
        plt.xlim(-1.0, max(ordered_collective.values())*1.2)
        plt.grid(True, which='both', linestyle='--', linewidth=0.1, alpha=0.5)
        plt.tight_layout()
        plt.savefig(f'{plotdir}/permutation_importance_{out_tag}.png')
        plt.savefig(f'{plotdir}/permutation_importance_{out_tag}.pdf')
        plt.close()

        

