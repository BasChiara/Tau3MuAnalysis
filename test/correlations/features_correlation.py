import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
general_cmap = sn.color_palette(palette='vlag') #sn.diverging_palette(220, 20, as_cmap=True)

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config


def compute_pair(i,j,df):
    
    x = df.iloc[:, i].dropna()
    y = df.iloc[:, j].dropna()
    common_index = x.index.intersection(y.index)
    val = pg.distance_corr(x.loc[common_index], y.loc[common_index],n_boot=None)
    var1 = df.columns[i]
    var2 = df.columns[j]
    print(var1, var2, val)
    
    return (i, j, val)

def linear_correlation(dataframe):
    corr = dataframe.corr()
    labels = [config.labels[c] for c in dataframe.columns]
    return corr, labels

def plot_correlation_matrix(corr, labels, vmax=1., vmin=-1, center=0, text=True, isMC=False, title = 'correlation matrix', plotname='correlation_matrix'):
    fig, ax = plt.subplots(figsize=(10, 10))
    g = sn.heatmap(corr, cmap=general_cmap, 
                   ax =ax,
                   vmax=vmax, vmin=vmin, center=center, 
                   annot=text, fmt='.2f',
                   square=True, linewidths=.5, 
                   cbar_kws={
                       "shrink": 0.75,     # make cbar not taller than the matrix
                        "aspect": 20,       # control width-to-height ratio
                        "pad": 0.02,        # bring it closer to the matrix
                    },  
                   annot_kws={"size":9})
    cbar = g.collections[0].colorbar
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label(title, fontsize=16, labelpad=10)

    # rotate axis labels
    g.set_xticklabels(labels, rotation='vertical', fontsize = 16)
    g.set_yticklabels(labels, rotation='horizontal', fontsize = 16)
    cbar = g.collections[0].colorbar
    cbar.ax.tick_params(labelsize=14)
    # plt.show()
    plt.title('data sidebands' if not isMC else r'$W\to\tau(3\mu)\nu$ MC', fontsize=20)
    plt.tight_layout()
    plt.savefig(plotname+'.png', dpi=800)
    plt.savefig(plotname+'.pdf', dpi=800)
    print(f"[+] saved linear correlation plot as {plotname}.png and {plotname}.pdf")
    plt.close()


import argparse
parser = argparse.ArgumentParser(description='Compute correlation matrices for features.')
parser.add_argument('--read_from_input', action='store_true', help='Read DataFrame from input file')
parser.add_argument('--year', choices=['Run3'], required=True, help='Year of the data/MC')
parser.add_argument('--isMC', action='store_true', help='Flag to indicate if input is MC')
args = parser.parse_args()

YEAR = args.year
isMC = args.isMC
read_from_input = args.read_from_input
plot_dir = os.path.expandvars('$WWW/Tau3Mu_Run3/BDTtraining/validations')

if read_from_input:
    file_lin = f'linear_correlation_matrix_{"MC" if isMC else "data"}{YEAR}.npy'
    linMtx = np.load(file_lin)
    file_dist = f'distance_correlation_matrix_{"MC" if isMC else "data"}{YEAR}.npy'
    distMtx = np.load(file_dist)
    columns = config.features + ['tauEta', 'bdt_score', 'tau_fit_mass']
    labels = [config.labels[c] for c in columns]


else :
    files = config.mc_bdt_samples['WTau3Mu'] if isMC else config.data_bdt_samples['WTau3Mu']
    rdf = ROOT.RDataFrame("tree_w_BDT", files).Filter(config.year_selection[YEAR])

    #sample N events to speed up computation
    Nevents = 10000
    col_toread = config.features + ['tauEta', 'bdt_score', 'tau_fit_mass']
    df_signal = pd.DataFrame(rdf.AsNumpy(columns=col_toread)).sample(n=Nevents, random_state=123)
    print("Number of events in DataFrame: ", len(df_signal))

    columns = df_signal.columns
    print("Columns in DataFrame: ", columns)
    n = len(columns.tolist())

    # --- LINEAR CORRELATION MATRIX ---
    linMtx, labels = linear_correlation(df_signal)
    # save linear correlation matrix
    np.save(f'linear_correlation_matrix_{"MC" if isMC else "data"}{YEAR}.npy', linMtx)

    # --- DISTANCE CORRELATION MATRIX ---
    import pingouin as pg
    from joblib import Parallel, delayed
    distMtx = np.zeros((n, n))
    results_signal = Parallel(n_jobs=8, verbose=1)(delayed(compute_pair)(i, j, df_signal) for i in range(n) for j in range(i, n))

    for i, j, val in results_signal:
        distMtx[i, j] = val
        distMtx[j, i] = val  # symmetric
    # save distance correlation matrix
    np.save(f'distance_correlation_matrix_{"MC" if isMC else "data"}{YEAR}.npy', distMtx)

# plot linear correlation matrix
plot_correlation_matrix(corr=linMtx, labels=labels, 
                        vmax=1., vmin=-1.0, center=0,
                        title='Linear Correlation',
                        text=False, isMC=isMC,
                        plotname=os.path.join(plot_dir,f'linear_correlation_{"MC" if isMC else "data"}{YEAR}')
)
# plot distance correlation matrix
plot_correlation_matrix(corr=distMtx, labels=labels,
                        vmax=1., vmin=0.0, center=0.5,
                        title='Distance Correlation',
                        text=False, isMC=isMC,
                        plotname=os.path.join(plot_dir,f'distance_correlation_{"MC" if isMC else "data"}{YEAR}')
)