import os
import sys


data_dir="/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/"
combine_dir="/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src//WTau3Mu_limits/bias_study/"

tag="apply_LxyS2.0"

year_list=['22', '23']
cat_list=['A', 'B', 'C']
bdt_cuts_22 = [0.995, 0.996, 0.995]
bdt_cuts_23 = [0.987, 0.996, 0.992]


wp_dict = dict(zip(year_list, [dict(zip(cat_list, bdt_cuts_22)), dict(zip(cat_list, bdt_cuts_23))]))
print(wp_dict)
func_list=['expo', 'const', 'poly1']

for year in wp_dict:
    for cat in wp_dict[year]:
        for func in func_list:

            print(f"--> Year: {year}, Category: {cat}, Function: {func}\n")            
            command = f"python3 models/Tau3Mu_fitSB.py --plot_outdir {combine_dir}/plots/ --combine_dir {combine_dir}/input_combine/ -s {data_dir}XGBout_signal_kFold_Optuna_HLT_overlap_{tag}_2024Oct10.root -d {data_dir}XGBout_data_kFold_Optuna_HLT_overlap_{tag}_2024Oct10.root --category {cat} -y {year} --tag {tag}_{func} --save_ws --bkg_func {func} --bdt_cut {wp_dict[year][cat]} --goff"
            os.system(command)
            print('\n')