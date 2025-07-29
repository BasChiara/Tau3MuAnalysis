#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()
ROOT.EnableImplicitMT()
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("libRooFitCore")

import os
from math import sqrt
import numpy as np
import argparse
# import custom configurations
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
from style.color_text import color_text as ct
import models.datacard_utils as du
import models.fit_utils as fitu
import models.CMSStyle as CMS
USE_CMS_STYLE = True

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
    mass = ROOT.RooRealVar('tau_fit_mass', 'M(3#mu)'  , mass_window_lo,  mass_window_hi, 'GeV' )
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
    parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/',      help='output directory for plots')
    parser.add_argument('--combine_dir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/Combine/',            help='output directory for combine')
    parser.add_argument('--save_ws',        action = 'store_true' ,                                             help='set it to save the workspace for combine')
    parser.add_argument('--tag',                                                                                help='tag to the training')
    parser.add_argument('-u','--unblind',   action = 'store_true' ,                                             help='set it to run UN-blind')
    parser.add_argument('-c','--category',  choices = ['A', 'B', 'C'],  default = 'A',                          help='which categories to fit')
    parser.add_argument('-y','--year',      choices = config.year_list, default = '22',                         help='which CMS dataset to use')
    parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')
    parser.add_argument('--debug',          action = 'store_true' ,                                             help='set it to have useful printout')

    args = parser.parse_args()

    
    runblind = not args.unblind # don't show (nor fit!) data in the signal mass window
    year = args.year
    catYY = f'{args.category}_20{year}'
    
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
    data_file = parse_input(args)
    input_tree_name = 'tree_w_BDT'

    # ---- OUTPUT ----
    if not os.path.exists(args.plot_outdir): os.makedirs(args.plot_outdir)
    if not os.path.exists(args.combine_dir): os.makedirs(args.combine_dir)
    wspace_filename = os.path.join(args.combine_dir, f'ws_multipdf_{label}.root' ) 
    

    # **** CONSTANTS  *** #
    tau_mass = 1.777 # GeV
    mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
    blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV
    fit_range_lo  , fit_range_hi   = blind_region_lo - 0.05, blind_region_hi + 0.05 # GeV

    # binning
    bin_w = 0.01 # GeV
    nbins = int(np.rint((mass_window_hi-mass_window_lo)/bin_w)) # needed just for plotting, fits are all unbinned
    if (args.debug): print(f'{ct.BOLD}[INFO]{ct.END} binning {nbins} of type {type(nbins)}')

    # ---- LOAD DATA ----
    vars, mass = load_data()
    vars_set = ROOT.RooArgSet(*vars)
    base_selection      = ' & '.join([
        config.cat_eta_selection_dict_fit[args.category], 
        config.year_selection['20'+args.year],
        config.phi_veto,
    ])
    bdt_selection  = f'(bdt_score > {cut:.4f})' if hasattr(args, 'bdt_cut') else '(bdt_score > 0.0)'

    # **** IMPORT DATA ****
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
        config.sidebands_selection if runblind else '(1)',
    ])
    
    print(f'\n{ct.BLUE}------ DATA SIDEBANDS -------{ct.END}')
    print(f' entries (pre BDT)          : {N_data}')
    print(f' entries in SB (pre BDT)    : {N_data_SB:.0f}')
    bkg_dataset, bkg_eff, N_sb = fitu.import_data_from_tree(
        data_tree,
        vars_set,
        dataset_name = f'data_{process_name}',
        base_cut=base_selection + f' & {config.sidebands_selection}',
        full_cut=data_selection,
        verbose=True,
    )
    bkg_dataset = bkg_dataset.reduce(ROOT.RooArgSet(mass))
    print (f'entries in left SB {bkg_dataset.sumEntries("", "left_SB")}')
    print (f'entries in right SB {bkg_dataset.sumEntries("", "right_SB")}')
    #if (bkg_dataset.sumEntries("", "left_SB") == 0 or bkg_dataset.sumEntries("", "right_SB") == 0): continue 

    # **** BACKGROUND MODELS ****
    
    # exponential
    bkg_model_name = f'expo_{process_name}'
    slope = ROOT.RooRealVar(f'expoalpha_{catYY}', f'expoalpha_{catYY}', 0.0, -5.0, 5.0)
    expo  = ROOT.RooExponential(bkg_model_name, bkg_model_name, mass, slope)
    #getattr(pdfs, 'import')(expo)
    #expo.fitTo(bkg_dataset, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))

    # constant
    bkkg_model_name = f'const_{process_name}'
    const = ROOT.RooPolynomial(bkg_model_name,bkg_model_name, mass)
    #getattr(pdfs, 'import')(const)
    #const.fitTo(bkg_dataset, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))

    # power law
    bkg_model_name = f'powlaw_{process_name}'
    pow_1 = ROOT.RooRealVar(f'c_powlaw_{catYY}',f'c_powlaw_{catYY}', 1, -100, 100)
    powlaw = ROOT.RooGenericPdf(bkg_model_name, "TMath::Power(@0, @1)", ROOT.RooArgList(mass, pow_1) )
    #getattr(pdfs, 'import')(powlaw)
    #powlaw.fitTo(bkg_dataset, ROOT.RooFit.Range('left_SB,right_SB'), ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))

    pdf_idx = ROOT.RooCategory(f'pdf_idx_{catYY}', f"PDF index for {catYY}")
    models = ROOT.RooArgList()
    models.add(expo)
    models.add(const)
    models.add(powlaw)

    multipdf = ROOT.RooMultiPdf(f'multipdf_{catYY}', f'multipdf_{catYY}', pdf_idx, models)
    
    # --- save workspace ---
    pdfs = ROOT.RooWorkspace('pdfs_'+catYY)
    print("[+] creating workspace")
    getattr(pdfs, 'import')(mass)
    getattr(pdfs, 'import')(pdf_idx)
    getattr(pdfs, 'import')(multipdf)
    pdfs.Print()
    if args.save_ws:
        file_ws = ROOT.TFile(wspace_filename, "RECREATE")
        file_ws.cd()
        pdfs.Write()
        file_ws.Close()
        print(f'{ct.BOLD}[+]{ct.END} saved workspace to {wspace_filename}')

    # --- plot ---
    frame = mass.frame(ROOT.RooFit.Bins(nbins), ROOT.RooFit.Title(f'Background model for {catYY}'))
    bkg_dataset.plotOn(frame, ROOT.RooFit.Name('data'))
    expo.plotOn(frame, ROOT.RooFit.Name('expo'), ROOT.RooFit.LineColor(ROOT.kRed))
    const.plotOn(frame, ROOT.RooFit.Name('const'), ROOT.RooFit.LineColor(ROOT.kBlue))
    powlaw.plotOn(frame, ROOT.RooFit.Name('powlaw'), ROOT.RooFit.LineColor(ROOT.kGreen))
    
    canvas = ROOT.TCanvas(f'c_{catYY}', f'c_{catYY}', 800, 600)
    frame.Draw()
    canvas.SetGrid()
    canvas.SaveAs(os.path.join(args.plot_outdir, f'multipdf_{label}.png'))



    