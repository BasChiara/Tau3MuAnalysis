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

plot_outdir  = '$WWW/Tau3Mu_Run3/Ztautau/sensitivity/'
combine_dir  = '/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/WZresults/W_wp/input_combine/'
tag         = 'fix_ZWratio'
b_func       = args.b_func

for cat in working_points:
    if cat == 'comb': continue
    print(f'\n\n------ CATEGORY {cat} ------\n\n')
    cmd = f'python3 WZTau3Mu_fitSB.py --plot_outdir {plot_outdir} --save_ws --sys_unc --combine_dir {combine_dir} --tag {tag}_{b_func} -b {b_func} -c {cat} -y {year} --bdt_cut {working_points[cat]}'
    if args.dry_run:
        print(cmd)
    else:
        os.system(cmd)
