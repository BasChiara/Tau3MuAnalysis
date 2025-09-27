import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
FONTSIZE = 16
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import mva.config as cfg

import argparse

def get_pdDataset(file, tree, branches, selection='(1)'):
    if not os.path.isfile(file):
        raise RuntimeError(f"File {file} does not exist")
    sig_rdf = ROOT.RDataFrame(tree, file).Filter(selection)
    df = pd.DataFrame(sig_rdf.AsNumpy(branches))

    return df

DEBUG = False

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--reference', '-r', type=str, required=True, help='Reference .json config file')
    argparser.add_argument('--test', '-t', type=str, required=True, help='Test .json config file')
    argparser.add_argument('--output', '-o', type=str, required=True, help='Output directory')
    args = argparser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    output_dir = os.path.abspath(args.output)

    if not os.path.isfile(args.reference):
        raise RuntimeError(f"Reference config file {args.reference} does not exist")
    if not os.path.isfile(args.test):
        raise RuntimeError(f"Test config file {args.test} does not exist")
    
    with open(args.reference, 'r') as f:
        reference_config = json.load(f)
    with open(args.test, 'r') as f:
        test_config = json.load(f)
    
    print("Reference config:")
    print(json.dumps(reference_config, indent=4))
    print("Test config:")
    print(json.dumps(test_config, indent=4))

    # DATASETS
    branches_to_load = cfg.features+['tauEta', 'bdt_score', 'target']
    selection = '&'.join([
        cfg.base_selection,
        cfg.phi_veto
    ])
    # ---- reference ----
    df_ref_sig = get_pdDataset(reference_config['signal'], 'tree_w_BDT', branches_to_load, selection)
    df_ref_bkg = get_pdDataset(reference_config['data'],   'tree_w_BDT', branches_to_load, selection + f'& {cfg.sidebands_selection}')
    df_ref = pd.concat([df_ref_sig, df_ref_bkg], ignore_index=True)
    print(f"Reference dataset: {len(df_ref_sig)} signal and {len(df_ref_bkg)} background events")
    # ---- test ----
    df_test_sig = get_pdDataset(test_config['signal'], 'tree_w_BDT', branches_to_load, selection)
    df_test_bkg = get_pdDataset(test_config['data'], 'tree_w_BDT', branches_to_load, selection + f'& {cfg.sidebands_selection}')
    df_test = pd.concat([df_test_sig, df_test_bkg], ignore_index=True)
    print(f"Test dataset: {len(df_test_sig)} signal and {len(df_test_bkg)} background events")


    # ---- ROC curve ----
    from sklearn.metrics import roc_curve, auc
    fpr_ref, tpr_ref, th_ref = roc_curve(df_ref['target'], df_ref['bdt_score'])
    fpr_tst, tpr_tst, th_tst = roc_curve(df_test['target'], df_test['bdt_score'])
    # plot and compare
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(fpr_ref, tpr_ref, label=reference_config['tag'], color='blue')
    ax.plot(fpr_tst, tpr_tst, label=test_config['tag'], color='red')
    ax.grid(True)
    ax.set_xlabel('False Positive Rate', fontsize=FONTSIZE)
    ax.set_ylabel('True Positive Rate', fontsize=FONTSIZE)
    ax.tick_params(axis='both', which='major', labelsize=FONTSIZE)
    ax.legend(loc='lower right', fontsize=FONTSIZE, frameon=False)
    plt.xscale('log')
    plt.ylim(5e-4, 1.0)
    plot_name = os.path.join(output_dir, 'ROC_comparison')
    plt.savefig(f'{plot_name}.png')
    plt.savefig(f'{plot_name}.pdf')
    plt.close()
    print(f"ROC curve comparison plot saved to {plot_name}.(png|pdf)")

    # ---- BDT score distribution ----
    bins = np.linspace(0, 1, 50)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    fig, (ax, ax_ratio) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    ref_sig_hist, edges  = np.histogram(df_ref_sig['bdt_score'],  bins=bins, weights=1./len(df_ref_sig)*np.ones(len(df_ref_sig)))
    ref_bkg_hist, _  = np.histogram(df_ref_bkg['bdt_score'],  bins=bins, weights=1./len(df_ref_bkg)*np.ones(len(df_ref_bkg)))
    test_sig_hist, _ = np.histogram(df_test_sig['bdt_score'], bins=bins, weights=1./len(df_test_sig)*np.ones(len(df_test_sig)))
    test_bkg_hist, _ = np.histogram(df_test_bkg['bdt_score'], bins=bins, weights=1./len(df_test_bkg)*np.ones(len(df_test_bkg)))

    bin_centers = 0.5 * (edges[1:] + edges[:-1])
    bin_widths = np.diff(edges)

    ## reference
    ax.bar(bin_centers, ref_sig_hist, width=bin_widths, align='center', label=f"{reference_config['tag']} (MC)",   color='blue',fill=False, edgecolor='blue')
    ax.bar(bin_centers, ref_bkg_hist, width=bin_widths, align='center', label=f"{reference_config['tag']} (Data)", color='red', fill=False, edgecolor='red')
    #ax.plot(bin_centers, ref_bkg_hist, drawstyle='steps-mid', label=f"{reference_config['tag']} Background", color='red')
    # test
    ax.bar(bin_centers, test_sig_hist, width=bin_widths, align='center', label=f"{test_config['tag']} (MC)", color='blue', fill=True, alpha=0.3, edgecolor='blue', linestyle='dashed')
    ax.bar(bin_centers, test_bkg_hist, width=bin_widths, align='center', label=f"{test_config['tag']} (Data)", color='red', fill=True, alpha=0.3, edgecolor='red', linestyle='dashed')
    #ax.plot(bin_centers, test_sig_hist, drawstyle='steps-mid', label=f"{test_config['tag']} Signal", color='blue', linestyle='dashed')
    #ax.plot(bin_centers, test_bkg_hist, drawstyle='steps-mid', label=f"{test_config['tag']} Background", color='red', linestyle='dashed')
    
    ax.grid(True)
    ax.set_ylabel('', fontsize=FONTSIZE)
    #ax.set_ylim(100, max(ref_sig_hist.max(), ref_bkg_hist.max(), test_sig_hist.max(), test_bkg_hist.max())*1.2)
    ax.set_xlim(0, 1)
    ax.tick_params(axis='both', which='major', labelsize=FONTSIZE)
    ax.legend(loc='upper center', fontsize=FONTSIZE, frameon=False, ncol=2)
    ax.set_yscale('log')

    
    # Avoid division by zero
    ratio_sig = test_sig_hist / ref_sig_hist
    pull_sig  = (test_sig_hist - ref_sig_hist) / ref_sig_hist
    ratio_bkg = test_bkg_hist / ref_bkg_hist
    pull_bkg  = (test_bkg_hist - ref_bkg_hist) / ref_bkg_hist
    ratio_sig[~np.isfinite(ratio_sig)] = 0
    ratio_bkg[~np.isfinite(ratio_bkg)] = 0
    pull_sig[~np.isfinite(pull_sig)] = 0
    pull_bkg[~np.isfinite(pull_bkg)] = 0

    # Plot ratios
    ax_ratio.plot(bin_centers, ratio_sig, drawstyle='steps-mid', label='Signal ratio',     color='blue')
    ax_ratio.plot(bin_centers, ratio_bkg, drawstyle='steps-mid', label='Background ratio', color='red')
    #ax_ratio.plot(bin_centers, pull_sig, drawstyle='steps-mid', label='Signal pull',     color='blue')
    #ax_ratio.plot(bin_centers, pull_bkg, drawstyle='steps-mid', label='Background pull', color='red')

    rc, dr = 1.0,0.5
    ax_ratio.set_ylim(rc-dr, rc+dr)
    ax_ratio.set_xlim(0, 1)
    ax_ratio.set_xlabel('BDT score', fontsize=FONTSIZE)
    ax_ratio.set_ylabel('Ratio', fontsize=FONTSIZE)
    ax_ratio.axhline(1, color='black', linestyle='dashed', linewidth=1)
    ax_ratio.grid(True)
    #ax_ratio.legend(loc='upper right', fontsize=FONTSIZE, frameon=False)

    plot_name = os.path.join(output_dir, 'BDTscore_comparison')
    plt.tight_layout()
    plt.savefig(f'{plot_name}.png')
    plt.savefig(f'{plot_name}.pdf')

    if DEBUG : [print(f"Bin {i}: BDT score [{bins[i]:.2f}, {bins[i+1]:.2f}] | Ref sig: {ref_sig_hist[i]:.4f}, bkg: {ref_bkg_hist[i]:.4f} | Test sig: {test_sig_hist[i]:.4f}, bkg: {test_bkg_hist[i]:.4f} | Ratio sig: {ratio_sig[i]:.4f}, bkg: {ratio_bkg[i]:.4f}") for i in range(len(ref_sig_hist))]