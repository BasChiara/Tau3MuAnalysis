import ROOT
import argparse
ROOT.gROOT.SetBatch(True)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
import style.color_text as ct

def get_Nevents(rdf, selection):
    Nraw = rdf.Filter(selection).Count().GetValue()
    Nweight = rdf.Filter(selection).Sum('weight').GetValue()
    return Nraw, Nweight

def plot_WZvsYear(df_list, selection_step_list, var='yield_ratio', exp_WZratio=5.30, y_label=None):
    fig, ax = plt.subplots()
    ax.axhline(exp_WZratio, color='grey', linestyle='--', label='expected')
    for year in df_list: ax.plot(selection_step_list, df_list[year][var], label=year, marker='o')
    # add orizontal line for expected ratio  
    ax.legend(loc='upper left')
    ax.grid()
    if not y_label : ax.set_ylabel(f'W/Z {var}', fontsize=14)
    else: ax.set_ylabel(y_label, fontsize=14)
    ax.set_ylim(0.5*exp_WZratio, 2*exp_WZratio)
    fig.savefig(f'../outRoot/WvsZ_{var}.png')

argparser = argparse.ArgumentParser()
argparser.add_argument('--process', choices=['WTau3Mu', 'W3MuNu', 'ZTau3Mu'], help='For which process to compute the efficiency breakdown')
argparser.add_argument('--bdt',     action='store_true', help='Take the tree with BDT scores')
argparser.add_argument('--compareWZ', action='store_true', help='Compare W and Z')
args = argparser.parse_args()

years_list = ['2022preEE', '2022EE', '2023preBPix', '2023BPix']

make_csv = not args.compareWZ

if make_csv:
    samples = config.mc_samples[args.process]
    tree_name = 'WTau3Mu_tree'

    for i, year in enumerate(years_list):
        sample = samples[i]

        N_raw = np.array([], dtype=int)
        N_w = np.array([], dtype=float) 
        
        print(f'{ct.color_text.BOLD} -- {year} {ct.color_text.END} : {sample}  --')
        
        rdf = ROOT.RDataFrame(tree_name, sample).Filter(config.year_selection[year])

        N, Nw = get_Nevents(rdf, '1')
        
        # - displacement selection
        selection = config.displacement_selection
        N_LxyS, N_LxyS_w       = get_Nevents(rdf, selection)
        N_raw = np.append(N_raw, N_LxyS)
        N_w   = np.append(N_w, N_LxyS_w)
        print(f'Displacement selection: {N_LxyS} {N_LxyS_w:.3f}(w) ----> ({N_LxyS/N*100:,.2f} %)')
        # - base selection
        selection    = selection + ' && ' + config.base_selection
        N_mass_range, N_mass_range_w = get_Nevents(rdf, selection)
        N_raw = np.append(N_raw, N_mass_range)
        N_w   = np.append(N_w, N_mass_range_w)
        print(f'Base selection: {N_mass_range} {N_mass_range_w:.3f}(w) ----> ({N_mass_range/N*100:,.2f} %)')
        # - phi veto
        selection    = selection + ' && ' + config.phi_veto
        N_phi_veto, N_phi_veto_w = get_Nevents(rdf, selection)
        N_raw = np.append(N_raw, N_phi_veto)
        N_w   = np.append(N_w, N_phi_veto_w)
        print(f'Phi veto: {N_phi_veto} {N_phi_veto_w:.3f}(w) ----> ({N_phi_veto/N*100:,.2f} %)')
        # - BDT selection
        yy = '22' if '2022' in sample else '23' # fixme : tremendo
        bdt_selection = '('+ '|'.join(
            [f'((bdt_score > {config.wp_dict[yy][cat]}) & {config.cat_eta_selection_dict_fit[cat]}) ' for cat in ['A','B','C']]) + ')'
        if args.bdt:
            rdf_bdt = ROOT.RDataFrame('tree_w_BDT', config.mc_bdt_samples[args.process]).Filter(config.year_selection[year])
            # check number of events are consistent
            N_check, N_check_w = get_Nevents(rdf_bdt, selection)
            if (N_check != N_raw[-1] or N_check_w != N_w[-1]):
                print(f'{ct.color_text.RED}WARNING: number of events in BDT tree are not consistent with the main tree{ct.color_text.END}')
                print(f'N_check: {N_check} {N_check_w:.2f}(w)')
                exit(-1)
            selection = selection + ' && ' + bdt_selection
            N_bdt, N_bdt_w = get_Nevents(rdf_bdt, selection)
            N_raw = np.append(N_raw, N_bdt)
            N_w   = np.append(N_w, N_bdt_w)
            print(f'BDT selection: {N_bdt} {N_bdt_w:.2f}(w) ----> ({N_bdt/N*100:,.2f} %)')
        else:
            print(bdt_selection)
        print('\n\n')

        df = pd.DataFrame({'N_raw': N_raw, 'N_w': N_w})
        df['efficiency'] = df['N_raw']/N
        df['efficiency_w'] = df['N_w']/Nw
        df.to_csv(f'../outRoot/efficiency_breakdown_{year}_{args.process}.csv', index=False)
else:
    
    print(f'Comparing W and Z')

    base_eff_W = [0.2362, 0.2341, 0.2277, 0.2257]
    base_eff_Z = [0.2649, 0.2642, 0.2585, 0.2559]
    selection_step_list = ['LxyS', 'mass_range', 'phi_veto', 'BDT']
    df_list = []

    for i, year in enumerate(years_list):
        W_csv = pd.read_csv(f'../outRoot/efficiency_breakdown_{year}_WTau3Mu.csv')
        Z_csv = pd.read_csv(f'../outRoot/efficiency_breakdown_{year}_ZTau3Mu.csv')

        df = pd.DataFrame()
        df['NW'] = W_csv['N_w']
        df['efficiencyW'] = W_csv['efficiency_w']*base_eff_W[i]
        df['NZ'] = Z_csv['N_w']
        df['efficiencyZ'] = Z_csv['efficiency_w']*base_eff_Z[i]
        df['efficiency_ratio'] = W_csv['efficiency_w']/Z_csv['efficiency_w']
        df['yield_ratio'] = W_csv['N_w']/Z_csv['N_w']
        df['effyield_W'] = df['NW']/(df['efficiencyW'])
        df['effyield_Z'] = df['NZ']/(df['efficiencyZ'])
        df['effyield_ratio'] = df['effyield_W']/df['effyield_Z']

        df_list.append(df)
        print(f'{year} :')
    dict_df = dict(zip(years_list, df_list))

    y_label_dict = {
        'yield_ratio'       : r'$N_W/N_Z$', 
        'efficiency_ratio'  : r'$\epsilon_W/\epsilon_Z$', 
        'effyield_ratio'    : r'$(N_W/\epsilon_W) / (N_Z/\epsilon_Z)$'}

    exp_Yratio = config.xsec_ppWxTauNu/(2.0 * config.xsec_ppZxTauTau)
    plot_WZvsYear(dict_df, selection_step_list, var='yield_ratio', exp_WZratio=exp_Yratio, y_label=y_label_dict['yield_ratio'])
    plot_WZvsYear(dict_df, selection_step_list, var='effyield_ratio', exp_WZratio=exp_Yratio, y_label=y_label_dict['effyield_ratio'])
    plot_WZvsYear(dict_df, selection_step_list, var='efficiency_ratio', exp_WZratio=1.0, y_label=y_label_dict['efficiency_ratio'])
