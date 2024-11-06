import ROOT
import argparse
ROOT.gROOT.SetBatch(True)


import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config

argparser = argparse.ArgumentParser()
argparser.add_argument('--process', choices=['WTau3Mu', 'W3MuNu', 'ZTau3Mu'], help='For which process to compute the efficiency breakdown')
args = argparser.parse_args()
samples = config.mc_samples[args.process]


for sample in samples:
    
    print(f' -- processing {sample} --')
    rdf = ROOT.RDataFrame('WTau3Mu_tree', sample)

    N = rdf.Count().GetValue()
    # - displacement selection
    selection = config.displacement_selection
    N_LxyS       = rdf.Filter(selection).Count().GetValue()
    print(f'Displacement selection: {N_LxyS} ({N_LxyS/N*100:,.2f} %)')
    # - base selection
    selection    = selection + ' && ' + config.base_selection
    N_mass_range = rdf.Filter(selection).Count().GetValue()
    print(f'Base selection: {N_mass_range} ({N_mass_range/N*100:,.2f} %)')
    # - phi veto
    selection    = selection + ' && ' + config.phi_veto
    N_phi_veto   = rdf.Filter(selection).Count().GetValue()
    print(f'Phi veto: {N_phi_veto} ({N_phi_veto/N*100:,.2f} %)')
    # - BDT selection
    year = '22' if '2022' in sample else '23' # fixme : tremendo
    wp_BDT = config.wp_dict[year]
    bdt_selection = '|'.join(
        [f'((bdt_score > {wp_BDT[cat]}) & {config.cat_eta_selection_dict_fit[cat]}) ' for cat in ['A','B','C']])
    print(bdt_selection)
