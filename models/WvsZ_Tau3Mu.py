import ROOT
import numpy as np
import argparse

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config  as config


argparser = argparse.ArgumentParser()
argparser.add_argument('-y', '--year', choices=['22', '23'], default='22', help='input data file')
argparser.add_argument('-c', '--category', choices=['A', 'B', 'C', 'ABC'], default='ABC', help='input data file')
args = argparser.parse_args()

input_data    = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
input_Wsignal = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
input_Zsignal = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_ZTau3Mu_MC_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root'

year_ = args.year
category_ = args.category

plot_dir = f'/eos/user/c/cbasile/www/Tau3Mu_Run3/Ztautau/sensitivity/'

# **** EVENT SELECTION ****
base_selection      = ' & '.join([
    config.cat_eta_selection_dict_fit[category_], 
    config.year_selection['20'+year_],
    config.phi_veto,
])

sidebands_selection = ' & '.join([ base_selection, config.sidebands_selection ])

# **** INPUT DATA ****
input_tree_name = 'tree_w_BDT'
rdf_data = ROOT.RDataFrame(input_tree_name, input_data).Filter(sidebands_selection)
rdf_Wsignal = ROOT.RDataFrame(input_tree_name, input_Wsignal).Filter(base_selection)
rdf_Zsignal = ROOT.RDataFrame(input_tree_name, input_Zsignal).Filter(base_selection)

B0  = rdf_data.Sum('lumi_factor').GetValue()
Ws0 = rdf_Wsignal.Sum('lumi_factor').GetValue()
Zs0 = rdf_Zsignal.Sum('lumi_factor').GetValue()
print(f'** events @ baseline selection **')
print(' B0:', B0)
print(' Ws0:', Ws0)
print(' Zs0:', Zs0)

bdt_cut_list = np.arange(0.985, 0.999, 0.001)
B_list = []
Ws_list = []
Zs_list = []
for cut in bdt_cut_list:
    bdt_cut = f'bdt_score > {cut:.3f}'
    print(f'** cut: {bdt_cut} **')

    B  = rdf_data.Filter(bdt_cut).Sum('lumi_factor').GetValue()
    Ws = rdf_Wsignal.Filter(bdt_cut).Sum('lumi_factor').GetValue()
    Zs = rdf_Zsignal.Filter(bdt_cut).Sum('lumi_factor').GetValue()

    B_list.append(B)
    Ws_list.append(Ws)
    Zs_list.append(Zs)

# transform in np.array
B_array = np.array(B_list)
Ws_array = np.array(Ws_list)
Zs_array = np.array(Zs_list)

# compute significance
Sig_factor = 5
SigW  = Ws_array / np.sqrt(B_array)
SigZ  = Zs_array / np.sqrt(B_array) * Sig_factor
SigWZ = (Ws_array + Zs_array) / np.sqrt(B_array)

# **** PLOT ****
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))
# -- significance W and W+Z vs BDT
plt.plot(bdt_cut_list, SigW,  '--o',  label='W signal')
plt.plot(bdt_cut_list, SigZ,  '--o',  label=f'Z signal x{Sig_factor}')
plt.plot(bdt_cut_list, SigWZ, '--o',  label='W+Z signal')
plt.xlabel('BDT score')
plt.ylabel(r'S/$\sqrt{B}$')
if not category_ == 'ABC': plt.axvline(x=config.wp_dict[year_][category_], color='r', linestyle='--', label=f'WP 20{year_}{category_}')
plt.legend(loc='best')
plt.grid()
plt.savefig(f'{plot_dir}/significance_WZvsBDT_20{year_}{category_}.png')
plt.savefig(f'{plot_dir}/significance_WZvsBDT_20{year_}{category_}.pdf')

# -- efficiency W and W+Z vs BDT
effW  = Ws_array / Ws0
effZ  = Zs_array / Zs0
effWZ = (Ws_array + Zs_array) / (Ws0 + Zs0)

plt.figure(figsize=(8, 6))
plt.plot(bdt_cut_list, effW, label='W signal')
plt.plot(bdt_cut_list, effZ, label='Z signal')
plt.plot(bdt_cut_list, effWZ, label='W+Z signal')
# add working point
if not category_ == 'ABC': plt.axvline(x=config.wp_dict[year_][category_], color='r', linestyle='--', label=f'WP 20{year_}{category_}')

plt.xlabel('BDT score')
plt.ylabel('efficiency')
plt.legend(loc='best')
plt.grid()
plt.savefig(f'{plot_dir}/efficiency_WZvsBDT_20{year_}{category_}.png')
plt.savefig(f'{plot_dir}/efficiency_WZvsBDT_20{year_}{category_}.pdf')