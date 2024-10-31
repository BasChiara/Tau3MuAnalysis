#! /usr/bin/env python3

import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mva.config as config

argparser = argparse.ArgumentParser()
argparser.add_argument('-y','--year', choices=['22', '23'], default='22')
argparser.add_argument('-b','--b_func', choices=['expo', 'const', 'poly1'], default='expo')
argparser.add_argument('-d','--dry_run', action='store_true')

args = argparser.parse_args()
year = args.year

working_points = config.wp_dict[year]
print(f'Working points for {year}: {working_points}')

input_data   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
input_signal = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
plot_outdir  = '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/working_points/'
#combine_dir = '/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/results/AN_v2/input_combine/'
combine_dir  = '/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/bias_study_v3/input_combine/'
tag         = 'kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16'
#tag          = 'apply_LxyS2.0'
b_func       = args.b_func

for cat in working_points:
    if cat == 'comb': continue
    print(f'\n\n------ CATEGORY {cat} ------\n\n')
    cmd = f'python3 Tau3Mu_fitSB.py -s {input_signal} -d {input_data} --plot_outdir {plot_outdir} --save_ws --sys_unc --combine_dir {combine_dir} --tag {tag}_{b_func} -b {b_func} -c {cat} -y {year} --bdt_cut {working_points[cat]}'
    if args.dry_run:
        print(cmd)
    else:
        os.system(cmd)
