#! /usr/bin/env python3

import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mva.config as config

argparser = argparse.ArgumentParser()
argparser.add_argument('-y','--year', choices=['22', '23'], default='22')
argparser.add_argument('-b','--b_func', choices=['expo', 'const', 'poly1'], default='expo')
argparser.add_argument('-o','--output')
argparser.add_argument('--plot_outdir')
argparser.add_argument('-d','--dry_run', action='store_true')

args = argparser.parse_args()
year = args.year

working_points = config.wp_dict[year]
print(f'Working points for {year}: {working_points}')

input_data   = config.data_bdt_samples['WTau3Mu']
input_signal = config.mc_bdt_samples['WTau3Mu'] 
if not args.plot_outdir : plot_outdir  = '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/working_points/'
else: plot_outdir = args.plot_outdir
#combine_dir = '/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/results/AN_v2/input_combine/'
if not args.output: combine_dir  = '/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/bias_study_v3/input_combine/'
else: combine_dir = args.output
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
