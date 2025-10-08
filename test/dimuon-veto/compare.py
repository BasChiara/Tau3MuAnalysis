import ROOT
ROOT.gROOT.SetBatch(True)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys

input_dict = {
    'PhiOmega_pre':
    {
        'description': r'$\phi$ & $\omega/\rho$ veto (pre BDT)',
        'color': 'green',
        'label': '',
        'files': {
            'A22' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2022_PhiOmegaVETO.root',
            'B22' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2022_PhiOmegaVETO.root',
            'C22' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2022_PhiOmegaVETO.root',
            'A23' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2023_PhiOmegaVETO.root',
            'B23' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2023_PhiOmegaVETO.root',
            'C23' :'veto_preBDT/datacards/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2023_PhiOmegaVETO.root',
        }
    },
    'PhiOmega_post':
    {
        'description': r'$\phi$ & $\omega/\rho$ veto (post BDT)',
        'color': 'blue',
        'label': '',
        'files': {
            'A22' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2022_OmPhiVeto.root',
            'B22' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2022_OmPhiVeto.root',
            'C22' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2022_OmPhiVeto.root',
            'A23' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2023_OmPhiVeto.root',
            'B23' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2023_OmPhiVeto.root',
            'C23' :'veto_postBDT/omega-phi/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2023_OmPhiVeto.root',
        }
    },
    'Phi_post':
    {
        'description': r'$\phi$ veto (post BDT)',
        'color': 'red',
        'label': '',
        'files': {
            'A22' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2022_PhiVeto.root',
            'B22' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2022_PhiVeto.root',
            'C22' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2022_PhiVeto.root',
            'A23' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_A_2023_PhiVeto.root',
            'B23' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_B_2023_PhiVeto.root',
            'C23' :'veto_postBDT/phi/input_combine/sensitivity_tree_bdt_scan_wt3m_C_2023_PhiVeto.root',
        }
    },
}
outdir = os.path.expandvars('plots-v2/bdt-scan/')

def get_data(file, tree='sensitivity_tree'):
    rdf = ROOT.RDataFrame(tree, file)
    df = pd.DataFrame(rdf.AsNumpy())
    # remove events w/ Nbkg_Sregion < 1
    df = df[df['bkg_Nexp_Sregion'] >= 1]
    return df

if __name__ == '__main__':

    ref_key = 'Phi_post'
    tst_key = 'PhiOmega_post'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for cat in ['A22', 'B22', 'C22', 'A23', 'B23', 'C23']:
        df_ref  = get_data(input_dict[ref_key]['files'][cat])
        df_test = get_data(input_dict[tst_key]['files'][cat])

        plt.figure(figsize=(8,6))
        plt.plot(df_ref['bdt_cut'], df_ref['sig_Nexp']/df_ref['PunziS_val'], 
                label=input_dict[ref_key]['description'],
                marker='o', ls='--',
                color=input_dict[ref_key]['color'])
        plt.plot(df_test['bdt_cut'], df_test['sig_Nexp']/df_test['PunziS_val'],
                label=input_dict[tst_key]['description'], 
                marker='o', ls='--',
                color=input_dict[tst_key]['color'])
        plt.xlabel('BDT cut', fontsize=20)
        plt.xticks(fontsize=16)
        plt.ylabel('Punzi significance', fontsize=20)
        plt.yticks(fontsize=16)

        plt.grid()
        plt.legend(loc='best', fontsize=16, frameon=False)
        plt.text(0.05, 0.75, f'{cat}', 
                transform=plt.gca().transAxes, 
                fontsize=20, verticalalignment='top')
        plot_name = os.path.join(outdir, f'sensitivityPunzi_comparison_{cat}')
        plt.tight_layout()
        plt.savefig(plot_name+'.png')
        plt.savefig(plot_name+'.pdf')
        print(f'[OUT] plot saved in {plot_name}.(png|pdf)')
