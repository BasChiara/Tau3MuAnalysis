############################################
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
from style.color_text import color_text as ct
import models.datacard_utils as du
import models.fit_utils as fitu

INVID_MUON = False # set True if the input sample is with inverted muon ID

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--signal',                                                                       help='input Tau3Mu MC')
parser.add_argument('-d', '--data',                                                                         help='input DATA')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/',      help='output directory for plots')
parser.add_argument('--goff',           action = 'store_true' ,                                             help='NO plots')
parser.add_argument('--save_ws',        action = 'store_true' ,                                             help='set it to save the workspace for combine')
parser.add_argument('--sys_unc',        action = 'store_true' ,                                             help='put systematics in the datacard')
parser.add_argument('--fix_w',          action = 'store_true' ,                                             help='fix the signal width')
parser.add_argument('--combine_dir',                                default= 'input_combine/',              help='output directory for combine datacards and ws')
parser.add_argument('--tag',                                                                                help='tag to the training')
parser.add_argument('-u','--unblind',   action = 'store_true' ,                                             help='set it to run UN-blind')
parser.add_argument('-b','--bkg_func',  choices = ['expo', 'const', 'poly1', 'dynamic'], default = 'expo',  help='background model, \'dynamic\' : fit constant as Nb < --lowB_th')
parser.add_argument('--lowB_th',        type= float,                default= 35.0,                          help='if --const_lowB is given specyfies the min bkg events to fit with expo')
parser.add_argument('-c','--category',  choices = ['A', 'B', 'C', 'ABC'],  default = 'A',                          help='which categories to fit')
parser.add_argument('-y','--year',      choices = ['22','23', '24'],default = '22',                         help='which CMS dataset to use')
parser.add_argument('--optim_bdt',      action = 'store_true',                                              help='run BDT cut optimization')
parser.add_argument('--BDTmin',         type =float,                default = 0.9900,                       help='if --optim_bdt defines in the min BDT threshold in the scan')
parser.add_argument('--BDTmax',         type =float,                default = 0.9995,                       help='if --optim_bdt defines in the max BDT threshold in the scan')
parser.add_argument('--BDTstep',        type =float,                default = 0.0005,                       help='if --optim_bdt defines in the step value in the scan')
parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')
parser.add_argument('--debug',          action = 'store_true' ,                                             help='set it to have useful printout')

args = parser.parse_args()

category_by_eta = True
runblind = not args.unblind # don't show (nor fit!) data in the signal mass window

# **** INPUT ****
input_tree_name = 'tree_w_BDT'

mc_file     = config.mc_bdt_samples['WTau3Mu'] if not args.signal else args.signal
print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added MC file :\n {mc_file}')

data_file   = config.data_bdt_samples['WTau3Mu'] if not args.data else args.data
print(f'{ct.BOLD}[+]{ct.END} added DATA file :\n {data_file}')

if not os.path.exists(mc_file):
    print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_file} does NOT exist')
    exit()
if not os.path.exists(data_file):
    print(f'{ct.RED}[ERROR]{ct.END} DATA file {data_file} does NOT exist')
    exit()

# **** OUTPUT settings **** 
process_name = f'wt3m_{args.category}_20{args.year}' 
tag = (f'bdt{args.bdt_cut:,.4f}_{process_name}' if not args.optim_bdt else f'bdt_scan_{process_name}') + ('_' + args.tag ) if not (args.tag is None) else ''
set_bdt_cut = [args.bdt_cut] if not args.optim_bdt else np.arange(args.BDTmin, args.BDTmax, args.BDTstep) 
print('\n')
print(f'BDT selection scenario {set_bdt_cut}')

wspace_filename = f'{args.combine_dir}/wspace_{tag}.root'
out_data_filename = f'{args.combine_dir}/sensitivity_tree_{tag}.root'

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANTS  *** #
tau_mass = 1.777 # GeV
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV

# binning
bin_w = 0.01 # GeV
nbins = int(np.rint((mass_window_hi-mass_window_lo)/bin_w)) # needed just for plotting, fits are all unbinned
if (args.debug): print(f'{ct.BOLD}[INFO]{ct.END} binning {nbins} of type {type(nbins)}')

# *** RooFit Variables ***
varlist, mass = fitu.load_data(mass_window_lo, mass_window_hi, blind_region_lo, blind_region_hi, fit_range_lo, fit_range_hi)
thevars = ROOT.RooArgSet()
[thevars.add(v) for v in varlist]
reducedvars = ROOT.RooArgSet()
[reducedvars.add(v) for v in varlist if not 'fitM' in v.GetName()]

# *** Punzi Sensitivity and AMS ***
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

# **** EVENT SELECTION ****
base_selection      = ' & '.join([
    config.cat_eta_selection_dict_fit[args.category], 
    config.year_selection['20'+args.year],
    config.phi_veto, #config.omega_veto,
])

if args.save_ws : file_ws = ROOT.TFile(wspace_filename, "RECREATE")
# loop on BDT cuts
for cut in set_bdt_cut:

    catYY = f'{args.category}_20{args.year}'
    # output tag
    point_tag           = f'{args.category}{args.year}' + (('_' + args.tag ) if args.tag else '') + f'_bdt{cut:,.4f}'
    # BDT selection
    bdt_selection       = f'(bdt_score > {cut:,.4f})'
    sgn_selection       = ' & '.join([bdt_selection, base_selection])

    # **** IMPORT SIGNAL ****
    mc_tree = ROOT.TChain(input_tree_name)
    mc_tree.AddFile(mc_file)
    N_mc = mc_tree.GetEntries(base_selection)

    fullmc = ROOT.RooDataSet('mc_%s'%process_name, 'mc_%s'%process_name, mc_tree, thevars, sgn_selection, "weight")
    fullmc.Print()
    sig_efficiency = mc_tree.GetEntries(sgn_selection)/N_mc
    sig_efficiency_error = np.sqrt(sig_efficiency*(1-sig_efficiency)/N_mc)

    print(f'\n\n{ct.PURPLE}------ SIGNAL MC ------- {ct.END}')
    print(f' MC events    : {N_mc}')
    print(f' selection    : {sgn_selection}')
    print(f' weighted entries (BDT > {cut:.3f})    = {fullmc.sumEntries():.2f}' )
    print(f' signal efficiency                = {sig_efficiency*100:.2f}%')
    print(f'{ct.PURPLE}------------------------{ct.END}\n')
    # skip if no signal events
    if fullmc.sumEntries() == 0: continue
    
    # **** IMPORT DATA ****
    data_tree = ROOT.TChain(input_tree_name)
    data_tree.AddFile(data_file)
    N_data    = data_tree.GetEntries(base_selection) # events in the full mass range pre-BDT
    N_data_SB = data_tree.GetEntries(base_selection + f' & {config.sidebands_selection}') # events in the sidebands pre-BDT

    
    if INVID_MUON : 
        data_selection = ' & '.join([bdt_selection, config.year_selection['20'+args.year], config.cat_eta_selection_dict_fit[args.category]])
        datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  reducedvars, data_selection, "weight")
    else :
        data_selection = ' & '.join([
            base_selection, 
            bdt_selection,
            config.sidebands_selection if runblind else '(1)',
        ])
        datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, data_selection, "weight")
        
    datatofit.Print()
    bkg_efficiency = datatofit.sumEntries(config.sidebands_selection)/N_data_SB

    print(f'\n{ct.BLUE}------ DATA SIDEBANDS -------{ct.END}')
    print(f' entries (pre BDT)          : {N_data}')
    print(f' entries in SB (pre BDT)    : {N_data_SB}')
    print(f' selection                  : {data_selection}')
    print(f' entries  (post BDT)        : %.2f'%datatofit.sumEntries() )
    print(f' BDT background efficiency  : %.4e'%bkg_efficiency)
    print(f'{ct.BLUE}------------------------{ct.END}\n\n')
    # skip if no events in one of the 2 sidebands
    print (f'entries in left SB {datatofit.sumEntries("", "left_SB")}')
    print (f'entries in right SB {datatofit.sumEntries("", "right_SB")}')
    if (datatofit.sumEntries("", "left_SB") == 0 or datatofit.sumEntries("", "right_SB") == 0): continue
    
    fit_with_const = (args.bkg_func == 'const') or ((args.bkg_func == 'dynamic') and (datatofit.sumEntries() < args.lowB_th))
    # **** SIGNAL MODEL ****
    # signal PDF
    Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass)
    Mtau.setConstant(True)
    dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -0.04, 0.04)
    mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
    width  = ROOT.RooRealVar(f'width_{catYY}',  f'width_{catYY}',  0.01,    0.005, 0.05)

    nsig   = ROOT.RooRealVar('model_sig_%s_norm'%process_name, 'model_sig_%s_norm'%process_name, fullmc.sumEntries(), 0.0, 3*fullmc.sumEntries())
    gaus   = ROOT.RooGaussian('model_sig_%s'%process_name, 'gaus1_%s'%process_name, mass, mean, width)
    signal_model = ROOT.RooAddPdf('ext_model_sig_%s'%process_name, 'ext_model_sig_%s'%process_name, ROOT.RooArgList(gaus), nsig )
    

    # **** BACKGROUND MODEL ****
    bkg_model_name = f'model_bkg_{process_name}'
    # exponential
    slope = ROOT.RooRealVar(f'background_slope_{catYY}', f'slope_{catYY}', -1.0, -10.0, 10.0)
    expo  = ROOT.RooExponential(bkg_model_name, bkg_model_name, mass, slope)
    # constant
    const = ROOT.RooPolynomial(bkg_model_name,bkg_model_name, mass)
    # polynomial
    p0 = ROOT.RooRealVar(f'p0_{catYY}', f'p0_{catYY}', 0.0, -1.0, 1.0)
    p1 = ROOT.RooRealVar(f'p1_{catYY}', f'p1_{catYY}', 0.0, -1.0, 1.0)
    poly1 = ROOT.RooChebychev(bkg_model_name,bkg_model_name, mass, ROOT.RooArgList(p1))

    b_model = expo
    if fit_with_const :
        b_model = const
        print(f'{ct.BOLD}[i]{ct.END} fit background with constant')
    elif args.bkg_func == 'poly1' :
        b_model = poly1
        print(f'{ct.BOLD}[i]{ct.END} fit background with 1st order polynimial')
    else : print(f'{ct.BOLD}[i]{ct.END} fit background with exponential')
    # number of background events
    nbkg = ROOT.RooRealVar('model_bkg_%s_norm'%process_name, 'model_bkg_%s_norm'%process_name, datatofit.sumEntries(), 0., 3*datatofit.sumEntries())
    print(f'[debug] entries in data {datatofit.numEntries()}')
    #ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(b_model),  nbkg)
    #ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", [b_model],  [nbkg])
    ext_bkg_model = ROOT.RooAddPdf(f'ext_model_bkg{process_name}', f'ext_model_bkg{process_name}', b_model, nbkg)

    # **** TIME TO FIT ****
    # signal fit
    results_gaus = signal_model.fitTo(
        fullmc, 
        ROOT.RooFit.Range('fit_range'), 
        ROOT.RooFit.Save(),
        ROOT.RooFit.Extended(ROOT.kTRUE),
        ROOT.RooFit.SumW2Error(True),
        ROOT.RooFit.PrintLevel(-1),
    )
    results_gaus.Print()
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
        #ROOT.RooFit.Extended(ROOT.kTRUE),
        #ROOT.RooFit.SumW2Error(True),
        ROOT.RooFit.PrintLevel(-1),
    )
    results_expo.Print()

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
        ROOT.RooFit.MoveToBack(),
        ROOT.RooFit.PrintLevel(-1),
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
    
    c2.SaveAs('%s/massfit_SB_%s.png'%(args.plot_outdir, point_tag)) 
    c2.SaveAs('%s/massfit_SB_%s.pdf'%(args.plot_outdir, point_tag))
    if not args.goff :
        c2.SetLogy(1)
        c2.SaveAs('%s/massfit_SB_Log_%s.png'%(args.plot_outdir, point_tag)) 
        c2.SaveAs('%s/massfit_SB_Log_%s.pdf'%(args.plot_outdir, point_tag))

    # S/B in SR
    B = (nbkg.getValV())*(ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'sig_range').getValV())
    Berr = np.sqrt(B) if B > 0.5 else 3.0
    S = nsig.getValV() 
    Punzi_S = sig_efficiency/(0.5 + sqrt(B))
    Punzi_S_err = Punzi_S * np.sqrt( (sig_efficiency_error/sig_efficiency)**2 + (Berr/(2*sqrt(B)*(0.5 + np.sqrt(B))))**2)
    AMS = sqrt(2 * ( (S + B)*np.log(1+S/B) - S) )

    print(f'\n\n{ct.BOLD}---------- SUMMARY ----------{ct.END}')
    print(f'{ct.GREEN}SELECTION{ct.END} :')
    print(base_selection)
    print(' Nb in SR : %.2f +/- %.2f'%(B, Berr))
    print(' Ns       : %.2f +/- %.2f'%(nsig.getValV(), nsig.getError()))
    print('  = S efficiency %.4f '%sig_efficiency)
    print(' Nb       : %.2f +/- %.2f'%(nbkg.getValV(), nbkg.getError()))
    print('  = B efficiency %.4e '%bkg_efficiency)
    print(' * Punzi sensitivity = %.3f +/- %.3f'%(Punzi_S, Punzi_S_err))
    print(' * AMS               = %.4f'%AMS)
    print(f'{ct.BOLD}---------------------------------{ct.END}\n\n')

    if args.optim_bdt :
        bdt_cut.append(cut)
        sig_Nexp.append(nsig.getValV())
        sig_eff.append(sig_efficiency)
        bkg_Nexp.append(nbkg.getValV())
        bkg_Nexp_Sregion.append(B)
        bkg_eff.append(bkg_efficiency)
        PunziS_val.append(Punzi_S)
        PunziS_err.append(Punzi_S_err)
        AMS_val.append(AMS)

    if not args.save_ws : continue
    # ----------------------------------------------------------------------------------------------------
    #### SAVE MODEL TO A WORKSPACE ####
    wspace_tag      = f'WTau3Mu_{point_tag}'
    wspace_name     = f'wspace_{wspace_tag}'
    print(f'{ct.BOLD}[i]{ct.END} saving workspace {wspace_name} to {wspace_filename}')
    
    # fix signal mean value - width is fixed only during wp optimization
    dMtau.setConstant(True)
    if (args.fix_w) : width.setConstant(True)

    # save observed data // bkg-only Asimov with name 'dat_obs'
    fulldata = ROOT.RooDataSet('full_data', 'full_data', data_tree, thevars, sgn_selection) # fixme : this is useless
    mass.setBins(nbins)
    if runblind:
        # GenerateAsimovData() generates binned data following the binning of the observables
        print(f'{ct.RED}[i]{ct.END} running BLIND -- asimov dataset into workspace')
        data = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(ext_bkg_model, ROOT.RooArgSet(mass) )
        data.SetName('data_obs') 
    else :
        print(f'{ct.GREEN}[i]{ct.END} running OPEN -- real data into workspace !!!!')
        data     = ROOT.RooDataSet('data_obs','data_obs', fulldata, ROOT.RooArgSet(mass))
        #data = ROOT.RooDataHist("data_obs", "data_obs", mass, fulldata)
    data.Print()

    ws = ROOT.RooWorkspace(wspace_name, wspace_name)
    getattr(ws, 'import')(data)
    getattr(ws, 'import')(datatofit)
    getattr(ws, 'import')(gaus)  
    getattr(ws, 'import')(b_model)
    ws.Print()
    # save workspace
    file_ws.cd()
    ws.Write()
    print(f'{ct.BOLD}[o]{ct.END} workspace saved to {wspace_filename}')

    #### WRITE THE DATACARD ####
    print(f'{ct.BOLD}[i]{ct.END} writing datacard')
    datacard_name = f'{args.combine_dir}/datacard_{wspace_tag}.txt'
    du.combineDatacard_writer(
        process_name = process_name,
        input_mc     = mc_file,
        selection    = sgn_selection,
        ws_filename  = wspace_filename,
        workspace    = ws,
        datacard_name= datacard_name,
        year         = args.year,
        cat          = args.category,
        bkg_func     = args.bkg_func,
        Nobs         = -1 if runblind else fulldata.numEntries(),
        Nsig         = nsig.getVal(),
        Nbkg         = nbkg.getVal(),
        Ndata        = N_data,
        write_sys    = args.sys_unc,
    )

if not args.optim_bdt: exit()
tree_dict = dict(zip(df_columns, np.array([bdt_cut, sig_Nexp, sig_eff, bkg_Nexp, bkg_Nexp_Sregion, bkg_eff, PunziS_val, PunziS_err, AMS_val])))
#if (ROOT.gROOT.GetVersion() == '6.22/09' ):
out_rdf = ROOT.RDF.MakeNumpyDataFrame(tree_dict).Snapshot('sensitivity_tree', out_data_filename)
#elif (ROOT.gROOT.GetVersion() == '6.30/07' ):
#    out_rdf = ROOT.RDF.FromNumpy(tree_dict).Snapshot('sensitivity_tree', out_data_filename)
print(f'[o] output tree saved in {out_data_filename}')
print(tree_dict)
