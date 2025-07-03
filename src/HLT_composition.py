# check HLT composition after the whole selection
# > HLT_DoubleMu4_3_LowMass
# > HLT_Tau3Mu

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
#from mva.config import base_selection, phi_veto, sidebands_selection, cat_eta_selection_dict_fit, wp_dict, mc_bdt_samples

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root')
parser.add_argument('-t','--tree',      default='Events')
parser.add_argument('--outdir',         default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--bdt_cut',        action= 'append', help='BDT cut to test')
parser.add_argument('--tag',            default= '', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y','--year',      choices= ['2022', '2023'], default = '2022')
parser.add_argument('--isMC',           action='store_true', help='is MC or data')
parser.add_argument('-p','--process',   choices= ['WTau3Mu', 'W3MuNu', 'DsPhiPi', 'ZTau3Mu'], default = 'WTau3Mu')

args = parser.parse_args()
tag = args.tag

# input file
input_sample = ''
if args.input_root : input_sample = args.input_root
else:
    if (not args.year) or (not args.process) :
        print('[ERROR] specify year and process to run the script')
        exit(-1)
    input_sample = config.mc_bdt_samples[args.process] if args.isMC else config.data_bdt_samples[args.process]
if not os.path.isfile(input_sample):
    print(f'[ERROR] input file {input_sample} not found')
    exit(-1)

print(f'[i] input file: {input_sample}')

# event selection
if not args.bdt_cut:
    bdt_selection_dict = config.wp_dict[args.year]
else:
    if (len(args.bdt_cut) == 1):
        bdt_cut_list = [args.bdt_cut[0]] * 3
    elif (len(args.bdt_cut) == 3) :
        bdt_cut_list = args.bdt_cut
    else:
        print(f'[ERROR] number of bdt threshold is {len(args.bdt_cut)} while 3 or 1 is expected')
        exit(-1)
    bdt_selection_dict = dict(zip(['A', 'B', 'C'], bdt_cut_list))
    
print(f'[i] BDT selection : {bdt_selection_dict}')

selection = " & ".join([
    config.base_selection, 
    config.phi_veto, 
    config.year_selection[args.year],
    config.sidebands_selection if not args.isMC else '(1)',
    ])
data_rdf  = ROOT.RDataFrame('tree_w_BDT', input_sample).Filter(selection)

for cat in ['ABC','A', 'B', 'C']:
    print(f'\nCAT {cat}')
    if cat == 'ABC':
        cat_selection = '('+ ' | '.join( [f'({config.cat_eta_selection_dict_fit[cat]} & (bdt_score > {bdt_selection_dict[cat]}))' for cat in ['A', 'B', 'C']] ) + ')'
    else:
        cat_selection = f'({config.cat_eta_selection_dict_fit[cat]} & (bdt_score > {bdt_selection_dict[cat]}))' 
    print(f' selection: {cat_selection}')
    N_events            = data_rdf.Filter(cat_selection).Count().GetValue()
    N_HLT_DoubleMu_only = data_rdf.Filter(cat_selection + ' & (!HLT_isfired_Tau3Mu)  &  (HLT_isfired_DoubleMu)').Count().GetValue() 
    N_HLT_Tau3Mu_only   = data_rdf.Filter(cat_selection + ' &  (HLT_isfired_Tau3Mu)  & (!HLT_isfired_DoubleMu)').Count().GetValue() 
    N_HLT_both          = data_rdf.Filter(cat_selection + ' &  (HLT_isfired_Tau3Mu)  &  (HLT_isfired_DoubleMu)').Count().GetValue()

    print('**************************')
    print(f' events : {N_events}')
    print(f' HLT_DoubleMu       -> {N_HLT_DoubleMu_only + N_HLT_both} ({(N_HLT_DoubleMu_only + N_HLT_both)/N_events * 100:,.2f} %)')
    print(f' HLT_Tau3Mu (only)  -> {N_HLT_Tau3Mu_only} ({N_HLT_Tau3Mu_only/N_events*100:,.2f} %)')
    print(f' HLT both           -> {N_HLT_both} ({N_HLT_both/N_events *100:,.2f} %)')
