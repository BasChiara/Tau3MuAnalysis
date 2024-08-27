#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
#ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
#ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit")
import os
from math import pi, sqrt
import numpy as np
from glob import glob
from array import array 
import argparse
# import custom configurations
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
from plots.color_text import color_text as ct


parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/Tau3Mu_massFit/reMini', help='output directory for plots')
parser.add_argument('--goff',           action = 'store_true' ,                                                             help='set it to produce no plots')
parser.add_argument('--combine_dir',                                default= 'input_combine/',                              help='output directory for combine datacards and ws')
parser.add_argument('-s', '--signal',                                                                                       help='input Tau3Mu MC')
parser.add_argument('-d', '--data',                                                                                         help='input DATA')
parser.add_argument('--tag',                                        default= 'emulateRun2',                                 help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,                                                             help='set it to have useful printout')
parser.add_argument('-u','--unblind',   action = 'store_true' ,                                                             help='set it to run UN-blind')
parser.add_argument('--save_ws',        action = 'store_true' ,                                                             help='set it to save the workspace for combine')
parser.add_argument('-b','--bkg_func',  choices = ['expo', 'const', 'poly1', 'dynamic'], default = 'expo',                  help='background model, \'dynamic\' : fit constant as Nb < --lowB_th')
parser.add_argument('--lowB_th',        type= float,                default= 35.0,                                          help='if --const_lowB is given specyfies the min bkg events to fit with expo')
parser.add_argument('--category',       choices = ['A', 'B', 'C'],  default = 'A',                                          help='which categories to fit')
parser.add_argument('-y','--year',      choices = ['22','23'],      default = '22',                                         help='which CMS dataset to use')
parser.add_argument('--optim_bdt',      action = 'store_true',                                                              help='run BDT cut optimization')
parser.add_argument('--BDTmin',         type =float,                default = 0.9900,                                       help='if --optim_bdt defines in the min BDT threshold in the scan')
parser.add_argument('--BDTmax',         type =float,                default = 0.9995,                                       help='if --optim_bdt defines in the max BDT threshold in the scan')
parser.add_argument('--BDTstep',        type =float,                default = 0.0005,                                       help='if --optim_bdt defines in the step value in the scan')
parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                                       help='single value of the BDT threshold to fit')

args = parser.parse_args()

category_by_eta = True

# **** OUTPUT settings **** 
process_name = 'WTau3Mu_%s%s'%(args.category, args.year)
tag = (f'bdt{args.bdt_cut:,.4f}_{process_name}' if not args.optim_bdt else f'bdt_scan_{process_name}') + ('_' + args.tag ) if not (args.tag is None) else ''
set_bdt_cut = [args.bdt_cut] if not args.optim_bdt else np.arange(args.BDTmin, args.BDTmax, args.BDTstep) 
print('\n')
print(f'BDT selection scenario {set_bdt_cut}')

wspace_filename = f'{args.combine_dir}/wspace_{tag}.root'
out_data_filename = f'{args.combine_dir}/sensitivity_tree_{tag}.root'

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
mass_window = 0.060 # GeV
tau_mass = 1.777 # GeV
fit_range_lo  , fit_range_hi   = 1.68, 1.87 # GeV
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV #tau_mass-mass_window, tau_mass+mass_window

bin_w = 0.01
nbins = int(np.rint((mass_window_hi-mass_window_lo)/bin_w)) # needed just for plotting, fits are all unbinned
if (args.debug): print(f'{ct.BOLD}[INFO]{ct.END} binning {nbins} of type {type(nbins)}')
runblind = not args.unblind # don't show (nor fit!) data in the signal mass window
blind_region_lo, blind_region_hi = 1.72, 1.84
# phi
phi_mass = 1.020 #GeV
phi_window = 0.020 #GeV
omega_mass = 0.783 #GeV

# **** INPUT DATA ****
input_tree_name = 'tree_w_BDT'
mc_file     = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_kFold_HLT_overlap_LxyS150_2024Apr29.root' if not args.signal else args.signal
if not os.path.exists(args.signal):
    print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_file} does NOT exist')
print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added MC file :\n {mc_file}')
data_file   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_kFold_HLT_overlap_LxyS150_2024Apr29_open.root' if not args.data else args.data
if not os.path.exists(args.data):
    print(f'{ct.RED}[ERROR]{ct.END} DATA file {data_file} does NOT exist')
print(f'{ct.BOLD}[+]{ct.END} added DATA file :\n {data_file}')

# ** RooFit Variables
# tau mass
mass = ROOT.RooRealVar('tau_fit_mass', '3-#mu mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
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
weight = ROOT.RooRealVar('weight', 'weight', -1000, 1000, '')
# di-muon mass
mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
#displacement
Lsign = ROOT.RooRealVar('tau_Lxy_sign_BS', 'tau_Lxy_sign_BS', 0, np.inf)
# year/era tag
year_id = ROOT.RooRealVar('year_id', 'year_id', 0, 500, '')

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(eta)
thevars.add(bdt)
thevars.add(weight)
thevars.add(mu12_mass)
thevars.add(mu13_mass)
thevars.add(mu23_mass)
thevars.add(Lsign)
thevars.add(year_id)

# ** data frame to scan Punzi sensitivity

if args.optim_bdt :
    df_columns      = ['bdt_cut', 'sig_Nexp', 'sig_eff', 'bkg_Nexp', 'bkg_Nexp_Sregion', 'bkg_eff', 'PunziS_val', 'PunziS_err', 'AMS_val']
    bdt_cut         = []  
    sig_Nexp        = []
    sig_eff         = []
    bkg_Nexp        = []
    bkg_Nexp_Sregion= []
    bkg_eff         = []
    PunziS_val      = []
    PunziS_err      = []
    AMS_val         = []

# **** EVENT SELEctION ****
phi_veto            = config.phi_veto 
cat_selection       = f'({config.cat_selection_dict[args.category]})' if not category_by_eta else config.cat_eta_selection_dict_fit[args.category]
sidebands_selection = config.sidebands_selection
year_selection      = config.year_selection['20'+args.year]

if args.save_ws : file_ws = ROOT.TFile(wspace_filename, "RECREATE")

for cut in set_bdt_cut:
    # output tag
    point_tag           = f'{args.category}{args.year}' + (('_' + args.tag ) if not (args.tag is None) else '') + f'_bdt{cut:,.4f}'
    # common event selection
    bdt_selection       = f'(bdt_score > {cut:,.4f})'
    base_selection      = ' & '.join([
        cat_selection, 
        year_selection, 
        phi_veto,
    ])
    sgn_selection       = ' & '.join([bdt_selection, base_selection])

    # **** IMPORT SIGNAL ****
    mc_tree = ROOT.TChain(input_tree_name)
    mc_tree.AddFile(mc_file)
    N_mc = mc_tree.GetEntries(base_selection)

    fullmc = ROOT.RooDataSet('mc_%s'%process_name, 'mc_%s'%process_name, mc_tree, thevars, sgn_selection, "weight")
    fullmc.Print()
    sig_efficiency = mc_tree.GetEntries(sgn_selection)/N_mc

    print(f'\n\n{ct.PURPLE}------ SIGNAL MC ------- {ct.END}')
    print(f' entries   : {N_mc}')
    print(f' selection : {sgn_selection}')
    print(f' total entries = %.2f'%fullmc.sumEntries() )
    print(f' signal efficiency = %.4e'%sig_efficiency)
    print(f'{ct.PURPLE}------------------------{ct.END}\n')
    # skip if no signal events
    if fullmc.sumEntries() == 0: continue
    
    # **** IMPORT DATA ****
    data_tree = ROOT.TChain(input_tree_name)
    data_tree.AddFile(data_file)
    N_data = data_tree.GetEntries(base_selection + f' & {sidebands_selection}' if runblind else '') 

    data_selection = ' & '.join([
        base_selection, 
        bdt_selection,
        sidebands_selection if runblind else '(1)',
    ])
    if runblind:
        print('\n *** running BLIND')
        # cut for blinding
        blinder   = ROOT.RooFormulaVar('blinder', 'blinder',  data_selection, ROOT.RooArgList(thevars))
        datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, blinder)
    else:
        print('\n *** running OPEN')
        datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, data_selection)
    datatofit.Print()
    bkg_efficiency = datatofit.sumEntries()/N_data

    print(f'\n{ct.BLUE}------ DATA SIDEBANDS -------{ct.END}')
    print(f' entries in SB  : {N_data}')
    print(f' selection      : {data_selection}')
    print(f' total entries  : %.2f'%datatofit.sumEntries() )
    print(f' background efficiency : %.4e'%bkg_efficiency)
    print(f'{ct.BLUE}------------------------{ct.END}\n\n')
    
    fit_with_const = (args.bkg_func == 'const') or ((args.bkg_func == 'dynamic') and (datatofit.sumEntries() < args.lowB_th))
    # **** SIGNAL MODEL ****
    # signal PDF
    Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass)
    Mtau.setConstant(True)
    dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -0.04, 0.04)
    mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
    width  = ROOT.RooRealVar('width',  'width',  0.01,    0.005, 0.05)
    width2 = ROOT.RooRealVar('width2', 'width2', 0.025,    0.005, 0.05)

    f      = ROOT.RooRealVar('f', 'f', 0.5, 0., 1.0)
    nsig   = ROOT.RooRealVar('model_sig_%s_norm'%process_name, 'model_sig_%s_norm'%process_name, fullmc.sumEntries(), 0.001, 3*fullmc.sumEntries())
    gaus   = ROOT.RooGaussian('gaus1_%s'%process_name, 'gaus1_%s'%process_name, mass, mean, width)
    gaus2  = ROOT.RooGaussian('gaus2_%s'%process_name, 'gaus2_%s'%process_name, mass, mean, width2)
    gsum   = ROOT.RooAddModel(f'model_sig_{process_name}', f'model_sig_{process_name}', ROOT.RooArgList(gaus, gaus2), ROOT.RooArgList(f))
    signal_model = ROOT.RooAddPdf('ext_model_sig_%s'%process_name, 'ext_model_sig_%s'%process_name, ROOT.RooArgList(gsum), nsig )
    

    # **** BACKGROUND MODEL ****
    bkg_model_name = f'model_bkg_{process_name}' 
    # exponential
    slope = ROOT.RooRealVar('slope', 'slope', -1.0, -10.0, -0.001)
    expo  = ROOT.RooExponential(bkg_model_name, bkg_model_name, mass, slope)
    # constant
    const = ROOT.RooPolynomial(bkg_model_name,bkg_model_name, mass)
    # polynomial
    p0 = ROOT.RooRealVar("p0", "p0", -0.01, -1.0, 1.0)
    poly1 = ROOT.RooPolynomial(bkg_model_name,bkg_model_name, mass, ROOT.RooArgList(p0))

    b_model = expo
    if fit_with_const :
        b_model = const
        print(f'{ct.BOLD}[i]{ct.END} fit background with constant')
    elif args.bkg_func == 'poly1' :
        b_model = poly1
        print(f'{ct.BOLD}[i]{ct.END} fit background with 1st order polynimial')
    else : print(f'{ct.BOLD}[i]{ct.END} fit background with exponential')
    # number of background events
    nbkg = ROOT.RooRealVar('model_bkg_%s_norm'%process_name, 'model_bkg_%s_norm'%process_name, datatofit.sumEntries(), 0.5*datatofit.sumEntries(), 5*datatofit.sumEntries())
    print(f'[debug] entries in data {datatofit.numEntries()}')
    #ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(b_model),  nbkg)
    #ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", [b_model],  [nbkg])
    ext_bkg_model = ROOT.RooExtendPdf(f'ext_model_bkg{process_name}', f'ext_model_bkg{process_name}', b_model, nbkg, "full_range")

    # **** TIME TO FIT ****
    # signal fit
    results_gaus = signal_model.fitTo(
        fullmc, 
        ROOT.RooFit.Range('fit_range'), 
        ROOT.RooFit.Save(),
        ROOT.RooFit.Extended(ROOT.kTRUE),
        ROOT.RooFit.SumW2Error(True),
        ROOT.RooFit.PrintLevel(1),
    )
    # * draw & save
    frame = mass.frame()
    frame.SetTitle('#tau -> 3#mu signal - CAT %s BDTscore > %.4f'%(args.category, cut))

    fullmc.plotOn(
        frame, 
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.XErrorSize(0), 
        ROOT.RooFit.LineWidth(2),
        ROOT.RooFit.FillColor(ROOT.kRed),
        ROOT.RooFit.DataError(1),
    )
    signal_model.plotOn(
        frame, 
        ROOT.RooFit.LineColor(ROOT.kRed),
        ROOT.RooFit.Range('fit_range'),
        ROOT.RooFit.NormRange('fit_range'),
        ROOT.RooFit.MoveToBack()
    )
    print('signal chi2 %.2f'%(frame.chiSquare()))
    signal_model.paramOn(
        frame,
        ROOT.RooFit.Layout(0.6, 0.75, 0.9),
        ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
    )
    frame.getAttText().SetTextSize(0.03)

    c = ROOT.TCanvas("c", "c", 800, 800)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
    frame.Draw()
    if not (args.optim_bdt or args.goff) :
        c.SaveAs('%s/signal_mass_%s.png'%(args.plot_outdir, point_tag)) 
        c.SaveAs('%s/signal_mass_%s.pdf'%(args.plot_outdir, point_tag)) 
        c.SetLogy(1)
        c.SaveAs('%s/signal_mass_Log_%s.png'%(args.plot_outdir, point_tag)) 
        c.SaveAs('%s/signal_mass_Log_%s.pdf'%(args.plot_outdir, point_tag)) 

    # -- plot pulls
    h_pullMC = frame.pullHist()
    h_pullMC.setYAxisLimits(-5., 5.)
    frame_pull = mass.frame(ROOT.RooFit.Title('[pull] #tau -> 3 #mu signal - CAT %s BDTscore > %.4f'%(args.category,cut)))
    frame_pull.addPlotable(h_pullMC, 'P')
    cp = ROOT.TCanvas("cp", "cp", 800, 800)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
    frame_pull.Draw()
    if not (args.optim_bdt or args.goff) :
        cp.SaveAs('%s/pull_signal_mass_%s.png'%(args.plot_outdir, point_tag)) 
        cp.SaveAs('%s/pull_signal_mass_%s.pdf'%(args.plot_outdir, point_tag))

    frame_b = mass.frame()
    frame_b.SetTitle('#tau -> 3 #mu signal+bkg - CAT %s BDTscore > %.3f'%(args.category, cut))

    datatofit.plotOn(
        frame_b, 
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.MarkerSize(1.)
    )

    # fit background
    results_expo = ext_bkg_model.fitTo(
        datatofit, 
        ROOT.RooFit.Range('left_SB,right_SB'), 
        ROOT.RooFit.Save(),
        ROOT.RooFit.PrintLevel(1)
    )
    nbkg.Print()
    ext_bkg_model.plotOn(
        frame_b, 
        ROOT.RooFit.LineColor(ROOT.kBlue),
        ROOT.RooFit.Range('full_range'),
        ROOT.RooFit.NormRange('left_SB,right_SB') 
    )
    fullmc.plotOn(
        frame_b, 
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.DrawOption('B'), 
        ROOT.RooFit.DataError(ROOT.RooAbsData.ErrorType(2)), 
        ROOT.RooFit.XErrorSize(0), 
        ROOT.RooFit.LineWidth(2),
        ROOT.RooFit.FillColor(ROOT.kRed),
        ROOT.RooFit.FillStyle(3004),                
    )
    signal_model.plotOn(
        frame_b, 
        ROOT.RooFit.LineColor(ROOT.kRed),
        ROOT.RooFit.Range('sig_range'),
        ROOT.RooFit.NormRange('sig_range')
    )
    # print N signal and N background on plot
    text_S = ROOT.TText(tau_mass, 0.90*frame_b.GetMaximum(), "Ns = %.2f +/- %.2f"%(nsig.getValV(), nsig.getError()))
    text_eS= ROOT.TText(tau_mass, 0.85*frame_b.GetMaximum(), "effS = %.2f"%(sig_efficiency))
    text_B = ROOT.TText(tau_mass, 0.80*frame_b.GetMaximum(), "Nb = %.2f +/- %.2f"%(nbkg.getValV(), nbkg.getError()))
    text_eB= ROOT.TText(tau_mass, 0.75*frame_b.GetMaximum(), "effB = %.2e"%(bkg_efficiency))
    text_S.SetTextSize(0.035)
    text_eS.SetTextSize(0.035)
    text_B.SetTextSize(0.035)
    text_eB.SetTextSize(0.035)
    frame_b.addObject(text_S)
    frame_b.addObject(text_eS)
    frame_b.addObject(text_B)
    frame_b.addObject(text_eB)


    c2 = ROOT.TCanvas("c2", "c2", 800, 800)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
    frame_b.Draw()
    
    c2.SaveAs('%s/SigBkg_mass_%s.png'%(args.plot_outdir, point_tag)) 
    c2.SaveAs('%s/SigBkg_mass_%s.pdf'%(args.plot_outdir, point_tag))
    if not args.goff :
        c2.SetLogy(1)
        c2.SaveAs('%s/SigBkg_mass_Log_%s.png'%(args.plot_outdir, point_tag)) 
        c2.SaveAs('%s/SigBkg_mass_Log_%s.pdf'%(args.plot_outdir, point_tag))

    print(f'\n\n{ct.BOLD}---------- SUMMARY ----------{ct.END}')
    print(' ** selection : \n%s'%base_selection)
    print(' RooExtendPdf = %.2f'%ext_bkg_model.expectedEvents(ROOT.RooArgSet(mass)))
    #B = (nbkg.getValV())*(ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooFit.NormSet(mass), ROOT.RooFit.Range('sig_range')).getValV())
    B = (nbkg.getValV())*(ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'sig_range').getValV())
    print(' B in sig-region : %.2f'%B)
    S = nsig.getValV() 
    print('  Ns = %.2f +/- %.2f'%(nsig.getValV(), nsig.getError()))
    print('  == S efficiency %.4f '%sig_efficiency)
    print('  Nb = %.2f +/- %.2f'%(nbkg.getValV(), nbkg.getError()))
    print('  == B efficiency %.4e '%bkg_efficiency)
    Punzi_S = sig_efficiency/(0.5 + sqrt(B))
    print(' ** Punzi sensitivity = %.4f'%Punzi_S)
    AMS = sqrt(2 * ( (S + B)*np.log(1+S/B) - S) )
    print(' ** AMS = %.4f'%AMS)
    if args.optim_bdt :
        bdt_cut.append(cut)
        sig_Nexp.append(nsig.getValV())
        sig_eff.append(sig_efficiency)
        bkg_Nexp.append(nbkg.getValV())
        bkg_Nexp_Sregion.append(B)
        bkg_eff.append(bkg_efficiency)
        PunziS_val.append(Punzi_S)
        PunziS_err.append(0)
        AMS_val.append(AMS)

    if not args.save_ws : continue
    # ----------------------------------------------------------------------------------------------------
    #### SAVE MODEL TO A WORKSPACE ####
    wspace_tag      = f'WTau3Mu_{point_tag}'
    wspace_name     = f'wspace_{wspace_tag}'
    # fix both signal & background shape
    dMtau.setConstant(True)
    width.setConstant(True)
    width2.setConstant(True)
    f.setConstant(True)

    # save observed data // bkg-only Asimov with name 'dat_obs'
    fulldata = ROOT.RooDataSet('full_data', 'full_data', data_tree, thevars, sgn_selection)
    mass.setBins(2*nbins)
    if runblind:
        # GenerateAsimovData() generates binned data following the binning of the observables
        #asimov_data = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(ext_bkg_model, ROOT.RooArgSet(mass) )
        data = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(ext_bkg_model, ROOT.RooArgSet(mass) )
        #data = ROOT.RooDataSet("data_obs", "data_obs", mass, asimov_data)
        data.SetName('data_obs') 
    else :
        #data     = ROOT.RooDataSet('data_obs','data_obs', fulldata, ROOT.RooArgSet(mass))
        data = ROOT.RooDataHist("data_obs", "data_obs", mass, fulldata)
    data.Print()

    ws = ROOT.RooWorkspace(wspace_name, wspace_name)
    getattr(ws, 'import')(data)
    getattr(ws, 'import')(gsum)  
    getattr(ws, 'import')(b_model)
    ws.Print()
    # save workspace
    file_ws.cd()
    ws.Write()

    #### WRITE THE DATACARD ####
    # make bkg normalization a nuisance parameter 
    #   floating in an interval marked by Clopper Pearson distribution for binomial proportion confidence level
    #   signal strenght for bkg normalizaion varies around 1.0 
    #   within an interval covering 99% CL of efficincy p.d.f. in counting experiment
    bkg_norm_lo, bkg_norm_hi = config.cp_intervals(Nobs = nbkg.getVal(), Ntot= N_data, cl = 0.99, verbose = True)

    datacard_name = f'{args.combine_dir}/datacard_{wspace_tag}.txt'
    # dump the text datacard
    with open(datacard_name, 'w') as card:
        card.write(
    '''
imax 1 number of channels
jmax * number of background sources
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes bkg         {proc}       {ws_file} {ws_name}:{bkg_model}
shapes sig         {proc}       {ws_file} {ws_name}:{sig_model}
shapes data_obs    {proc}       {ws_file} {ws_name}:data_obs
--------------------------------------------------------------------------------
bin                {proc}
observation        {obs:d}
--------------------------------------------------------------------------------
bin                              {proc}         {proc}
process                          sig                 bkg
process                          0                   1
rate                             {signal:.4f}              {bkg:.4f}
--------------------------------------------------------------------------------
lumi               lnN           1.022               -
bkgNorm_{proc}     rateParam     {proc}              bkg      1.      [{bkg_lo:.2f},{bkg_hi:.2f}]
bkgNorm_{proc}     flatParam
{activator}slope_{proc}       param  {slopeval:.4f} {slopeerr:.4f}
    '''.format(
            proc     = process_name, 
            ws_file  = os.path.basename(wspace_filename), 
            ws_name  = wspace_name, 
            bkg_model= b_model.GetName(),
            sig_model= gsum.GetName(),
            obs      = fulldata.numEntries() if runblind==False else -1, # number of observed events
            signal   = nsig.getVal(), #number of EXPEctED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
            bkg      = nbkg.getVal(), # number of expected background events **over the full mass range** using the exponential funciton fitted in the sidebands 
            bkg_lo   = bkg_norm_lo,
            bkg_hi   = bkg_norm_hi, 
            slopeval = slope.getVal(),
            slopeerr = slope.getError(),
            activator= '' if args.bkg_func == 'expo' else '#'
            )
        )
if not args.optim_bdt: exit()
tree_dict = dict(zip(df_columns, np.array([bdt_cut, sig_Nexp, sig_eff, bkg_Nexp, bkg_Nexp_Sregion, bkg_eff, PunziS_val, PunziS_err, AMS_val])))
#if (ROOT.gROOT.GetVersion() == '6.22/09' ):
out_rdf = ROOT.RDF.MakeNumpyDataFrame(tree_dict).Snapshot('sensitivity_tree', out_data_filename)
#elif (ROOT.gROOT.GetVersion() == '6.30/07' ):
#    out_rdf = ROOT.RDF.FromNumpy(tree_dict).Snapshot('sensitivity_tree', out_data_filename)
print(f'[o] output tree saved in {out_data_filename}')
print(tree_dict)


