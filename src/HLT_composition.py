# check HLT composition after the whole selection
# > HLT_DoubleMu4_3_LowMass
# > HLT_Tau3Mu

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

import sys
sys.path.append('..')
from mva.config import base_selection, phi_veto, sidebands_selection, cat_eta_selection_dict_fit

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root')
parser.add_argument('--tree',           default='Events')
parser.add_argument('--outdir',         default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--bdt_cut',        default= '0.995', help='BDT cut to test')
parser.add_argument('--tag',            default= '', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y','--year',      choices= ['2022', '2023'], default = '2022')
parser.add_argument('-p','--process',   choices= ['WTau3Mu', 'W3MuNu', 'DsPhiPi'], default = 'WTau3Mu')

args = parser.parse_args()
tag = args.tag


# event selection
bdt_selection = f'(bdt_score > {args.bdt_cut})'
selection = " & ".join([base_selection, phi_veto, bdt_selection,sidebands_selection])
data_rdf  = ROOT.RDataFrame(args.tree, args.input_root).Filter(selection)

for cat in cat_eta_selection_dict_fit:
    print(f'\nCAT {cat}')
    N_events            = data_rdf.Filter(cat_eta_selection_dict_fit[cat]).Count().GetValue()
    N_HLT_DoubleMu_only = data_rdf.Filter(cat_eta_selection_dict_fit[cat] + ' & (!HLT_isfired_Tau3Mu)  &  (HLT_isfired_DoubleMu)').Count().GetValue() 
    N_HLT_Tau3Mu_only   = data_rdf.Filter(cat_eta_selection_dict_fit[cat] + ' &  (HLT_isfired_Tau3Mu)  & (!HLT_isfired_DoubleMu)').Count().GetValue() 
    N_HLT_both          = data_rdf.Filter(cat_eta_selection_dict_fit[cat] + ' &  (HLT_isfired_Tau3Mu)  &  (HLT_isfired_DoubleMu)').Count().GetValue()

    print('**************************')
    print(f' events : {N_events}')
    print(f' HLT_DoubleMu       -> {N_HLT_DoubleMu_only + N_HLT_both} ({(N_HLT_DoubleMu_only + N_HLT_both)/N_events * 100:,.2f} %)')
    print(f' HLT_Tau3Mu (only)  -> {N_HLT_Tau3Mu_only} ({N_HLT_Tau3Mu_only/N_events*100:,.2f} %)')
    print(f' HLT both           -> {N_HLT_both} ({N_HLT_both/N_events *100:,.2f} %)')
