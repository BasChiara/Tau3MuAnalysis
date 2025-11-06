import ROOT
ROOT.gROOT.SetBatch(True)

import pandas as pd
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as cfg
from plots.color_text import color_text as ct

isMC = True
### IMPORT DATA ###
input_tree_name = 'tree_w_BDT'
#mc_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_signal_emulateRun2_EFG_MuMuFilter.root'
#data_file = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/mva_data/XGBout_data_emulateRun2_EFG_MuMuFilter_open.root'
mc_file = cfg.mc_bdt_samples['WTau3Mu'] 
data_file = cfg.data_bdt_samples['WTau3Mu']

selection = cfg.base_selection
data_rdf = ROOT.RDataFrame(input_tree_name, data_file if not isMC else mc_file)
data_rdf = data_rdf.Filter(selection)
columns_to_read = [ 'bdt_score', 'tau_mu12_M', 'tau_mu13_M', 'tau_mu23_M', 'tau_mu12_fitM', 'tau_mu13_fitM', 'tau_mu23_fitM']
data_df = pd.DataFrame(data_rdf.AsNumpy(columns_to_read))

mass_data = pd.DataFrame()
for pair in ['12', '13', '23']:
    tmp = data_df[data_df['tau_mu'+pair+'_M'] > 0][['bdt_score', 'tau_mu'+pair+'_fitM', 'tau_mu'+pair+'_M']]
    tmp = tmp.rename(columns={'tau_mu'+pair+'_fitM': 'tau_mumuOS_fitM', 'tau_mu'+pair+'_M': 'tau_mumuOS_M'})
    mass_data = pd.concat([mass_data, tmp], ignore_index=True)
    print(f' [+] added pair {pair} with {len(tmp)} entries')
# save to tree
data_outfile = 'data_mumuOS.root' if not isMC else 'mc_mumuOS.root'
ROOT.RDF.MakeNumpyDataFrame({col: mass_data[col].values for col in mass_data.columns}).Snapshot('tree_w_BDT', data_outfile)