import ROOT
import numpy as np
import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import mva.config as config
import plots.color_text as ct

# systematics sources wich are uncorrelated among categories 
sys_sources = [
    'tau_mu1_IDrecoSF',
    'tau_mu2_IDrecoSF',
    'tau_mu3_IDrecoSF',
    #'tau_DoubleMu4_3_LowMass_SF',
    'NLO_weight',
    'PU_weight',
    'mc_stat',
]

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input',  type=str, help='Monte Cralo root file')
parser.add_argument('-t', '--tree',   type=str, help='tree name')
parser.add_argument('-y', '--year',   choices= ['2022', '2023'],   type=str, help='data taking year')
parser.add_argument('-o', '--output', type=str, help='output json file')

args = parser.parse_args()
print('\n')

# get the mc tree
chain = ROOT.TChain(args.tree)
if args.input:
    print(f'[+] input file: {args.input}')
    chain.Add(args.input)
elif args.year == '2022':
    print(f'[+] input file: {config.WTau3Mu_signals[0]}')
    chain.Add(config.WTau3Mu_signals[0])
    print(f'[+] input file: {config.WTau3Mu_signals[1]}')
    chain.Add(config.WTau3Mu_signals[1])
elif args.year == '2023':
    print(f'[+] input file: {config.WTau3Mu_signals[2]}')
    chain.Add(config.WTau3Mu_signals[2])
    print(f'[+] input file: {config.WTau3Mu_signals[3]}')
    chain.Add(config.WTau3Mu_signals[3])
rdf = ROOT.RDataFrame(chain).Filter(config.base_selection)  
print(f'{ct.color_text.BOLD}[+]{ct.color_text.END} entries in the tree: {rdf.Count().GetValue()}')

# set systematics dictionary
sys_dict = {}

# loop on categories
for cat in config.cat_eta_selection_dict_fit:
    print(f' {ct.color_text.BLUE}---- CATEGORY {cat}{ct.color_text.END}')
    rdf_cat = rdf.Filter(config.cat_eta_selection_dict_fit[cat])
    dict_cat = {}
    # loop on systematics
    for sy_src in sys_sources:
        print(f' > {sy_src}')
        # MC stat systematics
        if sy_src == 'mc_stat':
            S_nominal = rdf_cat.Count().GetValue()
            f_up = 1. / np.sqrt(S_nominal) + 1.
            f_down = f_up
            print(f'  f_up = {f_up:.4f} \t f_down = {f_down:.4f}')
        # other systematics
        else:
            S_nominal = rdf_cat.Sum(sy_src).GetValue()
            S_up = rdf_cat.Sum(f'{sy_src}_sysUP').GetValue()
            f_up = S_up / S_nominal
            S_down = rdf_cat.Sum(f'{sy_src}_sysDOWN').GetValue()
            f_down = S_down / S_nominal
            dict_cat[sy_src] = {'up': f_up, 'down': f_down}
            #print(f'   S_nominal = {S_nominal:.2f} \t S_up = {S_up:.2f} \t S_down = {S_down:.2f}')
            print(f'   f_up = {f_up:.4f} \t f_down = {f_down:.4f}')
    sys_dict[cat] = dict_cat

# save the systematics to a json file
import json
with open(args.output, 'w') as f:
    json.dump(sys_dict, f, indent=4)
print(f'[+] systematics saved to {args.output}')
