import ROOT
import pandas as pd
import os
from sklearn.model_selection import train_test_split, StratifiedKFold
# my libraries
from config import *

# ------------ K-FOLD SPLITTING ------------ #
def kFold_splitting(data, bdt_inputs, kfold = 5, out_data_dir = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/', tag ='kFold_splitting',rnd_seed = 1234, shuffle = True, debug = False ):

    # sanity checks
    if not os.path.isdir(out_data_dir):
        print(f'[ERROR] output directory NOT found : {out_data_dir}')
        exit(-1)
    
    # define the bdt score related columns 
    data.loc[:,'id'] = np.arange(len(data))
    for i in range(kfold):
        data.loc[:,'bdt_fold%d_isTrainSet' %i]  = np.zeros(data.shape[0]).astype(int)
        data.loc[:,'bdt_fold%d_score' %i]       = -1 * np.ones(data.shape[0]).astype(int)
        data.loc[:,'bdt_to_apply']              = -1 * np.ones(data.shape[0]).astype(int)
        data.loc[:,'bdt_score']                 = -1 * np.ones(data.shape[0]).astype(int)
        data.loc[:,'bdt_training']              = np.zeros(data.shape[0]).astype(int)
    
    # implement k-fold splitting
    skf = StratifiedKFold(n_splits=kfold, random_state=rnd_seed, shuffle=shuffle)    
    for i, (train_index, apply_index) in enumerate(skf.split(data[bdt_inputs].values, data['target'].values)):
        # select training sample -> mass sidebands if is background
        data.loc[data.id.isin(train_index)&((data.target == 1) | ((data.target == 0) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi)))), 'bdt_fold%d_isTrainSet' %i] = 1
        data.loc[data.id.isin(apply_index), 'bdt_to_apply'] = i

    # save output
    if (debug) : print(data.columns)
    # convert data to dictionary with numpy arrays 
    out_data = {col: data[col].values for col in data.columns}
    out_data_filename = f'{out_data_dir}/XGBinput_data_{tag}.root'
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 0').Snapshot('tree_w_BDT', out_data_filename)
    print(f'[o] output DATA saved in {out_data_filename}')
    out_data_filename = f'{out_data_dir}/XGBinput_signal_{tag}.root'
    out_rdf = ROOT.RDF.MakeNumpyDataFrame(out_data).Filter('target == 1').Snapshot('tree_w_BDT', out_data_filename)
    print(f'[o] output SIGNAL saved in {out_data_filename}')

    return 0