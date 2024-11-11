import ROOT
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
import os
from math import pi, sqrt
import numpy as np
from glob import glob
from array import array 
import argparse
# import custom configurations
import datacard_utils as du
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/categorization/optimize_eta/sig_bkg_fit/', help=' output directory for plots')
parser.add_argument('--combine_dir',    default= 'input_combine/',                                                               help=' output directory for combine datacards and ws')
parser.add_argument('-s', '--signal',                                                                                            help='input Tau3Mu MC')
parser.add_argument('-d', '--data',                                                                                              help='input DATA')
parser.add_argument('--tag',                                                                                                     help='tag to the training')
parser.add_argument('--debug',          action = 'store_true',                                                                   help='set it to have useful printout')
parser.add_argument('--save_ws',        action = 'store_true' ,                                                                  help='set it to save the workspace for combine')
parser.add_argument('-y','--year',      default = '22')
parser.add_argument('--bdt_cut',        type= float, default = 0.990)

args = parser.parse_args()

# **** OUTPUT settings **** 
process_name_base = f'WTau3Mu'
eta_points_AB = np.arange(0.3, 1.2, 0.1)
eta_points_BC = np.arange(0.8, 2.1, 0.1)
tag = f'bdt{args.bdt_cut:,.4f}_{process_name_base}_{args.year}' + (('_' + args.tag ) if not (args.tag is None) else '')
cat_points    = np.array(np.meshgrid(eta_points_AB, eta_points_BC)).T.reshape(-1, 2)
print('\n')
print(f'ETA points AB {eta_points_AB}')
print(f'ETA points BC {eta_points_BC}')
print(f'running over {len(cat_points)} scenarios')

wspace_filename = f'{args.combine_dir}/wspace_cat_scan_{tag}.root'
out_data_filename = f'{args.combine_dir}/cat_scanTTree_{tag}.root'

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

# **** USEFUL CONSTANT VARIABLES *** #
tau_mass = 1.777 # GeV
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV
blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV

runblind = True # don't show (nor fit!) data in the signal mass window
nbins = 65 # needed just for plotting, fits are all unbinned
# **** INPUT DATA ****
input_tree_name = 'tree_w_BDT'
mc_file     = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root' if not args.signal else args.signal
if not os.path.exists(mc_file):
    print(f'[ERROR] MC file {mc_file} does NOT exist')
print(f'[+] added MC file :\n {mc_file}')
data_file   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root' if not args.data else args.data
if not os.path.exists(data_file):
    print(f'[ERROR] DATA file {mc_file} does NOT exist')
print(f'[+] added DATA file :\n {mc_file}')

# ** RooFit Variables
# year_id
year_id = ROOT.RooRealVar('year_id', 'year_id', 0, 500)
# tau mass
mass = ROOT.RooRealVar('tau_fit_mass', '3-#mu mass'  , mass_window_lo,  mass_window_hi, 'GeV' )
mass.setRange('left_SB', mass_window_lo, blind_region_lo)
mass.setRange('right_SB', blind_region_hi, mass_window_hi)
mass.setRange('fit_range', fit_range_lo,fit_range_hi)
mass.setRange('sig_range', blind_region_lo,blind_region_hi)
mass.setRange('full_range', mass_window_lo, mass_window_hi)
# tau mass resolution
mass_err = ROOT.RooRealVar('tau_fit_mass_err', '#sigma_{M(3 #mu)}/ M(3 #mu)'  , 0.0,  100, 'GeV' )
eta = ROOT.RooRealVar('tau_fit_eta', '#eta_{3 #mu}'  , -4.0,  4.0)
# BDT score
bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
# data weights
weight = ROOT.RooRealVar('weight', 'weight'  , -np.inf,  np.inf, '' )
# di-muon mass
mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
#displacement
Lsign = ROOT.RooRealVar('tau_Lxy_sign_BS', 'tau_Lxy_sign_BS', 0., np.inf, '')

thevars = ROOT.RooArgSet()
thevars.add(year_id)
thevars.add(mass)
thevars.add(eta)
thevars.add(mass_err)
thevars.add(bdt)
thevars.add(weight)
thevars.add(mu12_mass)
thevars.add(mu13_mass)
thevars.add(mu23_mass)
thevars.add(Lsign)

# ** data frame to scan Punzi sensitivity
df_columns      = ['bdt_cut', 'eta_thAB', 'eta_thBC', 'cat', 'sig_Nexp', 'sig_eff', 'bkg_Nexp', 'bkg_Nexp_Sregion', 'bkg_eff', 'PunziS_val', 'PunziS_err', 'AMS_val']
bdt_cut         = []
eta_thAB        = []
eta_thBC        = []
cat_id          = []
sig_Nexp        = []
sig_eff         = []
bkg_Nexp        = []
bkg_Nexp_Sregion= []
bkg_eff         = []
PunziS_val      = []
PunziS_err      = []
AMS_val         = []
if args.save_ws : file_ws = ROOT.TFile(wspace_filename, "RECREATE")


print(f'\n**** START OPTIMIZATION ****\n')
# **** EVENT SELECTION ****
zero_selection = '&'.join([
    config.phi_veto,
    config.displacement_selection,
    config.year_selection['20'+ args.year]
]) 
base_selection = '&'.join([
    zero_selection,
    f'(bdt_score > {args.bdt_cut:,.4f})',
])

# **** IMPORT SIGNAL ****
mc_tree = ROOT.TChain(input_tree_name)
mc_tree.Add(mc_file)
N_mc = mc_tree.GetEntries(base_selection)
# **** IMPORT DATA ****
data_tree = ROOT.TChain(input_tree_name)
data_tree.Add(data_file)
N_data = data_tree.GetEntries('&'.join([zero_selection, config.sidebands_selection])) 

for cat_p in cat_points:

    if (cat_p[1] - cat_p[0]) < 0.15 : continue
    print(f'[i] processing cat scenario {cat_p}\n')
    cat_selection_dict  = {
        'A' : f'(fabs(tau_fit_eta) < {cat_p[0]:,.1f})',
        'B' : f'(fabs(tau_fit_eta) > {cat_p[0]:,.1f} & fabs(tau_fit_eta) < {cat_p[1]:,.1f})',
        'C' : f'(fabs(tau_fit_eta) > {cat_p[1]:,.1f})'
    }

    for cat in cat_selection_dict:
        
        sgn_selection       = '&'.join([
            base_selection, 
            cat_selection_dict[cat]
        ])
        data_selection      = '&'.join([
            base_selection, 
            cat_selection_dict[cat], 
            config.sidebands_selection if runblind else '1'
        ])

        process_name = f'{process_name_base}_{cat}{args.year}'
        tag = f'bdt{args.bdt_cut:,.4f}_{cat}{args.year}_etaAB{cat_p[0]:,.1f}_BC{cat_p[1]:,.1f}' + (('_' + args.tag ) if not (args.tag is None) else '')
        print(f' > tag {tag}')

        
        

        fullmc = ROOT.RooDataSet('mc_%s'%process_name, 'mc_%s'%process_name, mc_tree, thevars, sgn_selection, "weight")
        fullmc.Print()
        sig_efficiency = mc_tree.GetEntries(sgn_selection)/N_mc

        print('\n\n------ SIGNAL MC ------- ')
        print(f' entries   : {N_mc}')
        print(f' selection : {sgn_selection}')
        print(f' total entries = %.2f'%fullmc.sumEntries() )
        print(f' signal efficiency = %.4e'%sig_efficiency)
        print('------------------------\n')
        if fullmc.sumEntries() == 0: continue

        
        print('\n *** running BLIND')
        # cut for blinding
        blinder  = ROOT.RooFormulaVar('blinder', 'blinder',  data_selection, ROOT.RooArgList(thevars))
        datatofit = ROOT.RooDataSet('data_fit', 'data_fit', data_tree,  thevars, blinder)
        datatofit.Print()
        bkg_efficiency = datatofit.sumEntries()/N_data

        print('\n------ DATA SIDEBANDS ------- ')
        print(f' entries in SB  : {N_data}')
        print(f' selection      : {sgn_selection}')
        print(f' total entries  : %.2f'%datatofit.sumEntries() )
        print(f' background efficiency : %.4e'%bkg_efficiency)
        print('------------------------\n\n')
        if datatofit.sumEntries() == 0 : continue 
       
        # **** SIGNAL MODEL ****
        # signal PDF
        Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass)
        Mtau.setConstant(True)
        dMtau  = ROOT.RooRealVar('dM', 'dM', 0, -0.04, 0.04)
        mean   = ROOT.RooFormulaVar('mean','mean', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau) )
        width  = ROOT.RooRealVar(f'width_{cat}{args.year}',  f'width_{cat}{args.year}',  0.01,    0.005, 0.05)

        nsig   = ROOT.RooRealVar(f'model_sig_{process_name}_norm', f'model_sig_{process_name}_norm', fullmc.sumEntries(), 0., 3*fullmc.sumEntries())
        gaus   = ROOT.RooGaussian(f'model_sig_{process_name}', f'model_sig_{process_name}', mass, mean, width)
        
        signal_model = ROOT.RooAddPdf(f'ext_model_sig_{process_name}', f'ext_model_sig_{process_name}', ROOT.RooArgList(gaus), nsig )

        # **** BACKGROUND MODEL ****
        # background PDF
        slope = ROOT.RooRealVar(f'slope_{cat}{args.year}', f'slope_{cat}{args.year}', -1.0, -10.0, 10.0)
        expo  = ROOT.RooExponential(f'model_bkg_{process_name}', f'model_bkg_{process_name}', mass, slope)
        const = ROOT.RooPolynomial(f'model_bkg_{process_name}',f'model_bkg_{process_name}', mass)
        b_model = expo #if (datatofit.sumEntries() > 20) else const
        # number of background events
        nbkg = ROOT.RooRealVar('model_bkg_%s_norm'%process_name, 'model_bkg_%s_norm'%process_name, datatofit.numEntries(), 0., 3*datatofit.numEntries())
        ext_bkg_model = ROOT.RooAddPdf("toy_add_model_bkg_WTau3Mu", "add background pdf", ROOT.RooArgList(b_model),  ROOT.RooArgList(nbkg))

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
        # * draw & save
        frame = mass.frame()
        frame.SetTitle('#tau -> 3#mu signal - CAT %s BDTscore > %.4f'%(cat, args.bdt_cut))

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
        if (args.debug):
            c = ROOT.TCanvas("c", "c", 800, 800)
            ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
            frame.Draw()
            c.SaveAs('%s/signal_mass_%s.png'%(args.plot_outdir, tag)) 
            c.SaveAs('%s/signal_mass_%s.pdf'%(args.plot_outdir, tag)) 

        frame_b = mass.frame()
        frame_b.SetTitle('#tau -> 3 #mu signal+bkg - CAT %s BDTscore > %.3f'%(cat, args.bdt_cut))

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
            ROOT.RooFit.PrintLevel(-1)
        )
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
        c2.SaveAs('%s/SigBkg_mass_%s.png'%(args.plot_outdir, tag)) 
        c2.SaveAs('%s/SigBkg_mass_%s.pdf'%(args.plot_outdir, tag)) 
        
        S = nsig.getValV() 
        B = (nbkg.getValV())*(ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'sig_range').getValV())
        Punzi_S = sig_efficiency/(0.5 + sqrt(B))
        AMS = sqrt(2 * ( (S + B)*np.log(1+S/B) - S) )
        print('\n\n---------- SUMMARY ----------')
        print(' ** selection : \n%s'%base_selection)
        print(' RooExtendPdf = %.2f'%ext_bkg_model.expectedEvents(ROOT.RooArgSet(mass)))
        print(' B in sig-region : %.2f'%B)
        print('  Ns = %.2f +/- %.2f'%(nsig.getValV(), nsig.getError()))
        print('  == S efficiency %.4f '%sig_efficiency)
        print('  Nb = %.2f +/- %.2f'%(nbkg.getValV(), nbkg.getError()))
        print('  == B efficiency %.4e '%bkg_efficiency)
        print(' ** Punzi sensitivity = %.4f'%Punzi_S)
        print(' ** AMS = %.4f'%AMS)
        bdt_cut.append(args.bdt_cut)
        eta_thAB.append(cat_p[0])
        eta_thBC.append(cat_p[1])
        cat_id.append({'A':1, 'B':2, 'C':3}[cat])
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
        wspace_tag      = f'{process_name_base}_bdt{args.bdt_cut:,.4f}_{cat}{args.year}_etaAB{cat_p[0]:,.1f}_BC{cat_p[1]:,.1f}'
        wspace_name     = f'wspace_{wspace_tag}'
        
        # fix both signal & background shape
        dMtau.setConstant(True)
        width.setConstant(True)

        # save observed data // bkg-only Asimov with name 'dat_obs'
        fulldata = ROOT.RooDataSet('full_data', 'full_data', data_tree, thevars, sgn_selection)
        mass.setBins(2*nbins)
        if runblind:
            # GenerateAsimovData() generates binned data following the binning of the observables
            data = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(ext_bkg_model, ROOT.RooArgSet(mass) )
            #data = ROOT.RooDataSet("data_obs", "data_obs", mass, ROOT.RooArgSet(asimov_data))
            data.SetName('data_obs') 
        else :
            #data     = ROOT.RooDataSet('data_obs','data_obs', fulldata, ROOT.RooArgSet(mass))
            data = ROOT.RooDataHist("data_obs", "data_obs", mass, fulldata)
        data.Print()

        ws = ROOT.RooWorkspace(wspace_name, wspace_name)
        getattr(ws, 'import')(data)
        getattr(ws, 'import')(gaus) 
        getattr(ws, 'import')(b_model)
        if (args.debug) : ws.Print()
        file_ws.cd()
        ws.Write()

        
        #### WRITE THE DATACARD ####
        datacard_name = f'{args.combine_dir}/datacard_{wspace_tag}.txt'
        du.combineDatacard_writer(
            input_mc     = mc_file,
            selection    = sgn_selection,
            ws_filename  = wspace_filename,
            workspace    = ws,
            datacard_name= datacard_name,
            year         = args.year,
            cat          = cat,
            bkg_func     = 'expo',
            Nobs         = -1 if runblind else fulldata.numEntries(),
            Nsig         = nsig.getVal(),
            Nbkg         = nbkg.getVal(),
            Ndata        = N_data,
            write_sys    = False,
        )
    

#if (ROOT.gROOT.GetVersion() == '6.22/09' ): exit(-1)
tree_dict = dict(zip(df_columns, np.array([bdt_cut, eta_thAB, eta_thBC, cat_id, sig_Nexp, sig_eff, bkg_Nexp, bkg_Nexp_Sregion, bkg_eff, PunziS_val, PunziS_err, AMS_val])))
out_rdf = ROOT.RDF.MakeNumpyDataFrame(tree_dict).Snapshot('sensitivity_tree', out_data_filename)
print(f'[o] output tree saved in {out_data_filename}')
print(tree_dict)
