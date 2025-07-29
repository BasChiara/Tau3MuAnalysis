from ROOT import gROOT, gPad, TCanvas, TLatex, TLegend, TChain, EnableImplicitMT, RooRealVar, RooArgSet, RooDataSet, RooJohnson, RooFit, RDataFrame, gInterpreter, RooExtendPdf, TFile, TH1, gStyle
from ROOT import TCut, RooSimultaneous, RooFormulaVar, RooCategory, RooWorkspace, RooArgList, RooAddPdf, RooExponential, RooGaussian, RooCBShape, RooNumber, RooVoigtian, RooStats
gROOT.SetBatch(True)
EnableImplicitMT(16)
gStyle.SetOptStat(True)
TH1.SetDefaultSumw2()

import ctypes
import argparse
import numpy as np 
import CMSStyle as CMS

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
from style.color_text import color_text as ct
import models.datacard_utils as du
import models.fit_utils as fitu

branches = {}
categories = []
bdt_cuts = {}
year_set = 2022 #updated from argparse
year_lab = 22 #updated from argparse
label = ""

#-----
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV
fit_range_lo  , fit_range_hi   = blind_region_lo - 0.05, blind_region_hi + 0.05 # GeV

def parse_input(arguments):
    # - signal -
    mc_W_file     = config.mc_bdt_samples['WTau3Mu'] if not arguments.signal_W else arguments.signal_W
    mc_Z_file     = config.mc_bdt_samples['ZTau3Mu'] if not arguments.signal_Z else arguments.signal_Z
        #check if the file exists
    if not os.path.exists(mc_W_file):
        print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_W_file} does NOT exist')
        exit()
    if not os.path.exists(mc_Z_file):
        print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_Z_file} does NOT exist')
        exit()
    print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added W MC file :\n {mc_W_file}')
    print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added Z MC file :\n {mc_Z_file}')
    # - data -
    data_file   = config.data_bdt_samples['WTau3Mu'] if not arguments.data else arguments.data
    if not os.path.exists(data_file):
        print(f'{ct.RED}[ERROR]{ct.END} DATA file {data_file} does NOT exist')
        exit()
    print(f'{ct.BOLD}[+]{ct.END} added DATA file :\n {data_file}')

    return mc_W_file, mc_Z_file, data_file

def load_data():
    mass = RooRealVar('tau_fit_mass', 'M(3#mu)'  , mass_window_lo,  mass_window_hi, 'GeV' )
    mass.setRange('left_SB', mass_window_lo, blind_region_lo)
    mass.setRange('right_SB', blind_region_hi, mass_window_hi)
    mass.setRange('fit_range', fit_range_lo,fit_range_hi)
    mass.setRange('sig_range', blind_region_lo,blind_region_hi)
    mass.setRange('full_range', mass_window_lo, mass_window_hi)

    # tau mass resolution
    eta = RooRealVar('tau_fit_eta', '#eta_{3 #mu}'  , -4.0,  4.0)
    # BDT score
    bdt = RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
    # data weights
    weight = RooRealVar('weight', 'weight', -np.inf, np.inf, '')
    # di-muon mass
    mu12_mass = RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
    mu23_mass = RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
    mu13_mass = RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
    #displacement
    Lsign = RooRealVar('tau_Lxy_sign_BS', 'tau_Lxy_sign_BS', 0, np.inf)
    # year/era tag
    year_id = RooRealVar('year_id', 'year_id', 0, 500, '')

    return [mass, eta, bdt, weight, mu12_mass, mu23_mass, mu13_mass, Lsign, year_id], mass


def signal_model(catYY, process_name='vt3m', Nw = [10, 1e6], Nz = [10, 1e6]):

    Mtau   = RooRealVar('Mtau' , 'Mtau' , 1.777)
    Mtau.setConstant(True)
    # W -> tau(3mu) nu
    dMtau_W   = RooRealVar('dM_W', 'dM_W', 0, -0.04, 0.04)
    mean_W    = RooFormulaVar('mean_W','mean_W', '(@0+@1)', RooArgList(Mtau,dMtau_W) )
    width_W   = RooRealVar(f'signal_width_W_{catYY}',  f'signal_width_W_{catYY}',  0.01,    0.005, 0.05)
    n_W       = RooRealVar(f'n_W_{catYY}', f'n_W_{catYY}', 1.0, 0.1, 10.0)
    alpha_W   = RooRealVar(f'alpha_W_{catYY}', f'alpha_W_{catYY}', 1.0, 0.0, 10.0)

    nsig_W         = RooRealVar('model_sig_W%s_norm'%process_name, 'model_sig_W%s_norm'%process_name, Nw[0], 0.0, Nw[1])
    
    cb_W           = RooCBShape('model_sig_W%s'%process_name, 'cb_W%s'%process_name, mass, mean_W, width_W, alpha_W, n_W)

    # Z -> tau(3mu) tau
    dMtau_Z   = RooRealVar('dM_Z', 'dM_Z', 0, -0.04, 0.04)
    mean_Z    = RooFormulaVar('mean_Z', 'mean_Z', '(@0+@1)', RooArgList(Mtau,dMtau_Z) )
    width_Z   = RooRealVar(f'signal_width_Z_{catYY}',  f'signal_width_Z_{catYY}',  0.01,    0.005, 0.05)
    n_Z       = RooRealVar(f'n_Z_{catYY}', f'n_Z_{catYY}', 1.0, 0.1, 10.0)
    alpha_Z   = RooRealVar(f'alpha_Z_{catYY}', f'alpha_Z_{catYY}', 1.0, 0.0, 10.0)
   
    nsig_Z   = RooRealVar('model_sig_Z%s_norm'%process_name, 'model_sig_Z%s_norm'%process_name, Nz[0], 0.0, Nz[1])
    
    cb_Z           = RooCBShape('model_sig_Z%s'%process_name, 'cb_Z%s'%process_name, mass, mean_Z, width_Z, alpha_Z, n_Z)

    # fix W to Z yield
    nsig_W.setConstant(True)
    nsig_Z.setConstant(True)
    r_wz = RooRealVar(f'r_wz_{catYY}', f'r_wz_{catYY}', nsig_W.getValV()/(nsig_W.getValV()+nsig_Z.getValV()))
    
    s_model = RooAddPdf(f'model_sig_{process_name}', f'model_sig_{process_name}', RooArgList(cb_W, cb_Z), RooArgList(r_wz))

    dMtau_W.setConstant(True)
    dMtau_Z.setConstant(True)

    return s_model, nsig_W, nsig_Z


if __name__ == "__main__":
    # Import info from user
    parser = argparse.ArgumentParser(description="config and root file, settings")
    #parser.add_argument("--config", type=str, help="config name")
    #parser.add_argument("--inputfile", type=str, help="path to input ntuple")
    parser.add_argument('--signal_W',   help='input WTau3Mu MC')
    parser.add_argument('--signal_Z',   help='input ZTau3Mu MC')
    parser.add_argument('-d', '--data', help='input DATA')
    parser.add_argument('--plot_outdir',default= './',      help='output directory for plots')
    parser.add_argument('--goff', action = 'store_true' , help='NO plots')
    parser.add_argument('--combine_dir', default= 'input_combine/', help='output directory for combine datacards and ws')
    parser.add_argument('--tag',                                                                                help='tag to the training')
    parser.add_argument('-u','--unblind',   action = 'store_true' , help='set it to run UN-blind')
    parser.add_argument("--multipdf", action="store_true", help="is multipdf")
    parser.add_argument('-b','--bkg_func',  choices = ['expo', 'const', 'poly1'], default = 'expo',  help='background model')
    parser.add_argument('-c','--category',  choices = ['A', 'B', 'C'],  default = 'A',                          help='which categories to fit')
    parser.add_argument('-y','--year',      choices = config.year_list, default = '22',                         help='which CMS dataset to use')
    parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')
    parser.add_argument("--label", type=str, default="", help="some label to identify this workspace/datacard production")
    args = parser.parse_args()

    year_set = args.year
    year_lab = str(year_set)[-2:]
    ismultipdf = True if args.multipdf else False
    isblind = not args.unblind
    process_name = f'vt3m_{args.category}_20{args.year}'
    label = '_'.join([
        f'bdt{args.bdt_cut:,.4f}',
        process_name,
        args.label,  
        'multipdf' if ismultipdf else args.bkg_func, 
        'blind' if isblind else 'unblind']
    ).strip('_')
    print('\n')

    # ---- INPUT ----
    mc_W_file, mc_Z_file, data_file = parse_input(args)
    input_tree_name = 'tree_w_BDT'
    
    # ---- OUTPUT ----
    if not os.path.exists(args.plot_outdir): os.makedirs(args.plot_outdir)
    if not os.path.exists(args.combine_dir): os.makedirs(args.combine_dir)
    wspace_filename = f'{args.combine_dir}/wspace_{label}.root'
    plotwspace_filename = f'{args.plot_outdir}/wspace_plot_{label}.root'
    out_data_filename = f'{args.combine_dir}/sensitivity_tree_{label}.root'

    # ---- LOAD DATA ----
    vars, mass = load_data()
    vars_set = RooArgSet(*vars)
    base_selection      = ' & '.join([
        config.cat_eta_selection_dict_fit[args.category], 
        config.year_selection['20'+args.year],
        config.phi_veto,
    ])
    bdt_selection  = f'(bdt_score > {args.bdt_cut:.4f})' if hasattr(args, 'bdt_cut') else '(bdt_score > 0.0)'
    sgn_selection       = ' & '.join([bdt_selection, base_selection])

    # ---- IMPORT SIGNAL ----
    print(f'\n\n{ct.PURPLE}------ SIGNAL (W)Tau3Mu MC ------- {ct.END}')
    mc_W_dataset, W_eff, W_Nmc = fitu.import_data_from_file(
        mc_W_file,
        vars_set, 
        input_tree_name, 
        dataset_name = f'mc_W_{process_name}',
        base_cut=base_selection,
        full_cut=sgn_selection,
        verbose=True,
    )
    W_eff_error = np.sqrt((1-W_eff)*W_eff/W_Nmc)
    print(f'\n\n{ct.PURPLE}------ SIGNAL (Z)Tau3Mu MC ------- {ct.END}')
    mc_Z_dataset, Z_eff, Z_Nmc = fitu.import_data_from_file(
        mc_Z_file,
        vars_set, 
        input_tree_name, 
        dataset_name = f'mc_Z_{process_name}',
        base_cut=base_selection,
        full_cut=sgn_selection,
        verbose=True,
    )
    # skip if no signal events
    if mc_W_dataset.sumEntries() == 0: 
        print(f'{ct.RED}[ERROR]{ct.END} No WTau3Mu MC events after selection {sgn_selection}')
        exit()

    # ---- IMPORT DATA ----
    data_tree        = fitu.get_tree_from_file(data_file, input_tree_name)
    # pre-BDT
    SB_eff, N_data   = fitu.breakdown_efficiency(data_tree, base_selection, base_selection + f' & {config.sidebands_selection}' , True ) # events in the full mass range pre-BDT
    N_data_SB        = N_data * SB_eff
    # post-BDT
    BDT_eff, N_data  = fitu.breakdown_efficiency(data_tree, base_selection, '&'.join([base_selection,bdt_selection]), True )
    N_data_BDT       = N_data * BDT_eff

    data_selection = ' & '.join([
        base_selection, 
        bdt_selection,
        config.sidebands_selection if isblind else '(1)',
    ])
    
    print(f'\n{ct.BLUE}------ DATA SIDEBANDS -------{ct.END}')
    print(f' entries (pre BDT)          : {N_data}')
    print(f' entries in SB (pre BDT)    : {N_data_SB:.0f}')
    bkg_dataset, bkg_eff, N_sb = fitu.import_data_from_tree(
        data_tree,
        vars,
        dataset_name = f'data_{process_name}',
        base_cut=base_selection + f' & {config.sidebands_selection}',
        full_cut=data_selection,
        verbose=True,
    )
    # skip if no events in one of the 2 sidebands
    print (f'entries in left SB {bkg_dataset.sumEntries("", "left_SB")}')
    print (f'entries in right SB {bkg_dataset.sumEntries("", "right_SB")}')



    # binning
    bin_w = 0.01 # GeV
    nbins = int(np.rint((mass_window_hi-mass_window_lo)/bin_w)) # needed just for plotting, fits are all unbinned


    # ---- SIGNAL MODEL ----
    print(f'\n{ct.BLUE}------ SIGNAL MODEL -------{ct.END}')
    s_model, nsig_W, nsig_Z = signal_model(args.category, process_name, Nw=[W_Nmc, 1e6], Nz=[Z_Nmc, 1e6])
    s_model.