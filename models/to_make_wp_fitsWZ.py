#! /usr/bin/env python3

import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mva.config as config

argparser = argparse.ArgumentParser()
argparser.add_argument('-y','--year',   choices=['22', '23', '24'], default='22')
argparser.add_argument('-b','--b_func', choices=['expo', 'const', 'powerlaw', 'dynamic'], default='expo')
argparser.add_argument('-t','--tag',    default='apply_LxyS2.0')
argparser.add_argument('-o','--output',
                    default='$COMBINEv10/WTau3Mu_limits/bias_study_v3/input_combine/',
                    help='Output directory for the combine datacards. If not specified, the default is used')
argparser.add_argument('--plot_outdir',
                    default='$WWW/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/working_points/',
                    help='Output directory for the plots. If not specified, the default is used')
argparser.add_argument('-d','--dry_run', action='store_true')

args = argparser.parse_args()
year = args.year

working_points = config.wp_dict[year]
print(f'Working points for {year}: {working_points}')

plot_outdir  = args.plot_outdir
if plot_outdir.startswith('$'):
    plot_outdir = os.path.expandvars(plot_outdir)
if not os.path.exists(plot_outdir):
    os.makedirs(plot_outdir)
    print(f'[OUT] created directory {plot_outdir}')
else:
    print(f'[OUT] using existing directory {plot_outdir}')
combine_dir  = args.output
if combine_dir.startswith('$'):
    combine_dir = os.path.expandvars(combine_dir)
if not os.path.exists(combine_dir):
    os.makedirs(combine_dir)
    print(f'[OUT] created directory {combine_dir}')
else:
    print(f'[OUT] using existing directory {combine_dir}')
tag          = args.tag
b_func       = args.b_func

for cat in working_points:
    if cat == 'comb': continue
    print(f'\n\n------ CATEGORY {cat} ------\n\n')
    cmd = f'python3 WZTau3Mu_fitSB.py --plot_outdir {plot_outdir} --goff --save_ws --sys_unc --combine_dir {combine_dir} --tag {tag}_{b_func} -b {b_func} -c {cat} -y {year} --bdt_cut {working_points[cat]}'
    if args.dry_run:
        print(cmd)
    else:
        os.system(cmd)
