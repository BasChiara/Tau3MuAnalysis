import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

import pingouin as pg
from joblib import Parallel, delayed

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


# input MC
YEAR = 'Run3'
isMC = False
files = config.mc_bdt_samples['WTau3Mu'] if isMC else config.data_bdt_samples['WTau3Mu']
rdf = ROOT.RDataFrame("tree_w_BDT", files).Filter(config.year_selection[YEAR])
#print("Number of events in MC: ", rdf.Count().GetValue())

#sample N events to speed up computation
Nevents = 10000#10000
col_toread = config.features + ['tauEta', 'bdt_score', 'tau_fit_mass']
df_signal = pd.DataFrame(rdf.AsNumpy(columns=col_toread)).sample(n=Nevents, random_state=123)
print("Number of events in DataFrame: ", len(df_signal))

columns = df_signal.columns
print("Columns in DataFrame: ", columns)
n = len(columns.tolist())
corrMatrix_signal = np.zeros((n, n))

# Run in parallel (adjust n_jobs as needed)
results_signal = Parallel(n_jobs=8, verbose=1)(delayed(compute_pair)(i, j, df_signal) for i in range(n) for j in range(i, n))

for i, j, val in results_signal:
    corrMatrix_signal[i, j] = val
    corrMatrix_signal[j, i] = val  # symmetric
# Plotting the correlation matrix
plt.figure(figsize=(9, 9))
labels = [config.labels[c] for c in columns]
g_signal = sn.heatmap(
        corrMatrix_signal,
        square=True,
        #cbar_kws={'shrink':.9 },
        cbar=False,
        annot=True,
        linewidths=0.1,vmax=1.0, linecolor='white',
        annot_kws={'fontsize':6},
        fmt=".1%",
        yticklabels=labels,
        xticklabels=labels,
    )
g_signal.set_yticklabels(g_signal.get_yticklabels(), rotation = 0, fontsize = 9)
g_signal.set_xticklabels(g_signal.get_xticklabels(), rotation = 90, fontsize = 9)

if isMC : 
    plt.title('distance correlation - signal MC' , y=1.05, size=14)
    plt.savefig(f'distance_correlation_MC{YEAR}.png', dpi=800)
    plt.savefig(f'distance_correlation_MC{YEAR}.pdf', dpi=800)
else : 
    plt.title('distance correlation - DATA' , y=1.05, size=14)
    plt.savefig(f'distance_correlation_data{YEAR}.png', dpi=800)
    plt.savefig(f'distance_correlation_data{YEAR}.pdf', dpi=800)
plt.tight_layout()
plt.close()
