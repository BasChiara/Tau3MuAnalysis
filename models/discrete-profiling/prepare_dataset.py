import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()

import os
from math import sqrt
import numpy as np
import argparse
# import custom configurations
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from style.color_text import color_text as ct
import mva.config as config
import models.fit_utils as fitu

#-----
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV
fit_range_lo  , fit_range_hi   = blind_region_lo - 0.05, blind_region_hi + 0.05 # GeV


def parse_input(arguments):
    # - data -
    data_file   = config.data_bdt_samples['WTau3Mu'] if not arguments.data else arguments.data
    if not os.path.exists(data_file):
        print(f'{ct.RED}[ERROR]{ct.END} DATA file {data_file} does NOT exist')
        exit()
    print(f'{ct.BOLD}[+]{ct.END} added DATA file :\n {data_file}')

    return data_file

def load_data():
    mass = ROOT.RooRealVar('tau_fit_mass', 'm_{3#mu}'  , mass_window_lo,  mass_window_hi, 'GeV' )
    mass.setRange('left_SB', mass_window_lo, blind_region_lo)
    mass.setRange('right_SB', blind_region_hi, mass_window_hi)
    mass.setRange('fit_range', fit_range_lo,fit_range_hi)
    mass.setRange('sig_range', blind_region_lo,blind_region_hi)
    mass.setRange('full_range', mass_window_lo, mass_window_hi)

    # tau mass resolution
    eta = ROOT.RooRealVar('tau_fit_eta', '#eta_{3 #mu}'  , -4.0,  4.0)
    # BDT score
    bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
    # data weights
    weight = ROOT.RooRealVar('weight', 'weight', -np.inf, np.inf, '')
    # di-muon mass
    mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
    mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
    mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
    #displacement
    Lsign = ROOT.RooRealVar('tau_Lxy_sign_BS', 'tau_Lxy_sign_BS', 0, np.inf)
    # year/era tag
    year_id = ROOT.RooRealVar('year_id', 'year_id', 0, 500, '')

    return [mass, eta, bdt, weight, mu12_mass, mu23_mass, mu13_mass, Lsign, year_id], mass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data',                                                                         help='input DATA')
    parser.add_argument('--outdir',         default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/Combine/',            help='output directory for combine')
    parser.add_argument('--save_ws',        action = 'store_true' ,                                             help='set it to save the workspace for combine')
    parser.add_argument('--tag',                                                                                help='tag to the training')
    parser.add_argument('-u','--unblind',   action = 'store_true' ,                                             help='set it to run UN-blind')
    parser.add_argument('-c','--category',  choices = ['A', 'B', 'C'],  default = 'A',                          help='which categories to fit')
    parser.add_argument('-y','--year',      choices = config.year_list, default = '22',                         help='which CMS dataset to use')
    parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')
    parser.add_argument('--debug',          action = 'store_true' ,                                             help='set it to have useful printout')

    args = parser.parse_args()

    # --- SETTINGS ---
    year_set = args.year
    year     = f'20{args.year}'
    cat      = args.category
    catYY    = f'{cat}{year_set}'
    isblind  = not args.unblind
    mass_name = 'tau_fit_mass'

    process_name = f'vt3m_{catYY}'
    
    cut = args.bdt_cut if hasattr(args, 'bdt_cut') else 0.0
    label = '_'.join([
        f'bdt{cut:,.4f}',
        process_name,
        args.tag, 
        'blind' if isblind else 'unblind']
    ).strip('_')
    print('\n')
    
    isblind = not args.unblind
    process_name = f'vt3m_{catYY}'
    cut = args.bdt_cut if hasattr(args, 'bdt_cut') else 0.0
    label = '_'.join([
        f'bdt{cut:,.4f}',
        process_name,
        args.tag, 
        'blind' if isblind else 'unblind']
    ).strip('_')
    print('\n')

    # ---- INPUT ----
    data_file       = parse_input(args)
    input_tree_name = 'tree_w_BDT'
    data_tree       = fitu.get_tree_from_file(data_file, input_tree_name)

    # ---- OUTPUT ----
    if not os.path.exists(args.outdir):
        os.path.makedirs(args.outdir)
    print(f'{ct.BOLD}[+]{ct.END} output directory: {args.outdir}')


    # ---- LOAD DATA ----
    vars, mass = load_data()
    vars_set = ROOT.RooArgSet(*vars)
    
    selection      = ' & '.join([
        config.cat_eta_selection_dict_fit[args.category], 
        config.year_selection['20'+args.year],
        config.phi_veto,
        f'bdt_score > {cut:.4f}'
    ])
    sideband_selection = '&'.join([
        selection,
        config.sidebands_selection,
    ])
    bkg_dataset, _, _ = fitu.import_data_from_tree(
        data_tree,
        vars_set,
        dataset_name = f'data_{process_name}',
        base_cut=selection,
        full_cut=selection,
        verbose=True,
    )
    bkg_dataset = bkg_dataset.reduce(ROOT.RooArgSet(mass))

    if bkg_dataset.numEntries() == 0:
        print(f'{ct.RED}[ERROR]{ct.END} no events found with selection {selection}')
        exit()
    print(f'{ct.BOLD}[+]{ct.END} imported {bkg_dataset.numEntries()} events')

    if not args.save_ws:
        print(f'{ct.BOLD}[+]{ct.END} not saving the workspace, exiting')
        exit()
    # ---- SAVE in WORKSPACE ----
    ws = ROOT.RooWorkspace(f'data_{process_name}', f'ws_data')
    getattr(ws, 'import')(bkg_dataset, ROOT.RooFit.Rename('data_obs'))
    #getattr(ws, 'import')(mass)
    #getattr(ws, 'import')(vars_set)
    #ws.writeToFile(os.path.join(args.outdir, f'data_{label}.root'), True)
    
    # frame 
    frame = mass.frame(ROOT.RooFit.Title(f'{process_name} - {args.category}'))
    bkg_dataset.plotOn(frame, ROOT.RooFit.Name('data_obs'), ROOT.RooFit.MarkerStyle(20), ROOT.RooFit.MarkerSize(0.8))
    frame.SetTitle(f'{process_name} - {args.category} - {args.year}')

    
    outfile = ROOT.TFile(os.path.join(args.outdir, f'data_{label}.root'), 'recreate')
    ws.Write()
    frame.Write()
    outfile.Close()
    print(f'{ct.BOLD}[+]{ct.END} saved the workspace in {args.outdir}/data_{label}.root')