#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()
#ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
#ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit")
import os
from math import sqrt
import numpy as np
import argparse
# import custom configurations
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mva.config as config
from style.color_text import color_text as ct
import models.datacard_utils as du
import models.fit_utils as fitu
import models.CMSStyle as CMS


def get_multipdf(file, workspace, name):
    
    pdf = None
    # open file and get pdf workspace
    multipdf_file = ROOT.TFile(file, 'READ')
    if not multipdf_file: 
        print(f'{ct.RED}[ERROR]{ct.END} multipdf workspace {args.multipdf_ws} not found')
        return pdf
    
    multipdf_ws = multipdf_file.Get(workspace)
    if not multipdf_ws:
        print(f'{ct.RED}[ERROR]{ct.END} multipdf workspace {args.multipdf_ws} does not contain a workspace named "w"')
        return pdf
    # get the multipdf
    multipdf = multipdf_ws.pdf(f'multipdf_bkg_{name}')
    if not multipdf:
        print(f'{ct.RED}[ERROR]{ct.END} multipdf workspace {args.multipdf_ws} does not contain a pdf named "multipdf_bkg_{name}"')
        return pdf
    bestpdf = multipdf.getCurrentPdf()
    print(f'{ct.BOLD}[i]{ct.END} multipdf {bestpdf.GetName()} loaded from {args.multipdf_ws}')

    return bestpdf, multipdf


parser = argparse.ArgumentParser()
parser.add_argument('--signal_W',                                                                           help='input WTau3Mu MC')
parser.add_argument('--signal_Z',                                                                           help='input ZTau3Mu MC')
parser.add_argument('-d', '--data',                                                                         help='input DATA')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/',      help='output directory for plots')
parser.add_argument('--goff',           action = 'store_true' ,                                             help='NO plots')
parser.add_argument('--save_ws',        action = 'store_true' ,                                             help='set it to save the workspace for combine')
parser.add_argument('--sys_unc',        action = 'store_true' ,                                             help='put systematics in the datacard')
parser.add_argument('--fix_w',          action = 'store_true' ,                                             help='fix the signal width')
parser.add_argument('--combine_dir',                                default= 'input_combine/',              help='output directory for combine datacards and ws')
parser.add_argument('--tag',                                                                                help='tag to the training')
parser.add_argument('-u','--unblind',   action = 'store_true' ,                                             help='set it to run UN-blind')
parser.add_argument('-b','--bkg_func',  choices = ['expo', 'const', 'multipdf'],    default = 'expo',       help='background model, expo or const or multipdf. If multipdf, specify the PDF workspace')
parser.add_argument('--multipdf_ws',                                                                        help='workspace with the multipdf background model')
parser.add_argument('-c','--category',  choices = ['A', 'B', 'C'],  default = 'A',                          help='which categories to fit')
parser.add_argument('-y','--year',      choices = config.year_list, default = '22',                         help='which CMS dataset to use')
parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')

args = parser.parse_args()

USE_CMS_STYLE = True
runblind = not args.unblind # don't show (nor fit!) data in the signal mass window

# **** INPUT ****
input_tree_name = 'tree_w_BDT'

mc_W_file     = config.mc_bdt_samples['WTau3Mu'] if not args.signal_W else args.signal_W
mc_Z_file     = config.mc_bdt_samples['ZTau3Mu'] if not args.signal_Z else args.signal_Z

#check if the file exists
if not os.path.exists(mc_W_file):
    print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_W_file} does NOT exist')
    exit()
if not os.path.exists(mc_Z_file):
    print(f'{ct.RED}[ERROR]{ct.END} MC file {mc_Z_file} does NOT exist')
    exit()
print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added W MC file :\n {mc_W_file}')
print(f'{ct.BOLD}{ct.BOLD}[+]{ct.END}{ct.END} added Z MC file :\n {mc_Z_file}')

data_file   = config.data_bdt_samples['WTau3Mu'] if not args.data else args.data
if not os.path.exists(data_file):
    print(f'{ct.RED}[ERROR]{ct.END} DATA file {data_file} does NOT exist')
    exit()
print(f'{ct.BOLD}[+]{ct.END} added DATA file :\n {data_file}')

# **** OUTPUT settings **** 
if not os.path.exists(args.plot_outdir): os.makedirs(args.plot_outdir)
if not os.path.exists(args.combine_dir): os.makedirs(args.combine_dir)


cat  = args.category
year = args.year
catYY = f'{args.category}{args.year}'
catYYYY = f'{args.category}_20{args.year}'
process_name = f'vt3m_{catYYYY}'
cut = args.bdt_cut if hasattr(args, 'bdt_cut') else 0.0

point_tag   =  catYY + (('_' + args.tag ) if args.tag else '') + f'_bdt{cut:,.3f}'
point_tag.replace('.', 'p')

wspace_tag          = f'VTau3Mu_{point_tag}'
wspace_filename     = os.path.join(args.combine_dir, f'wspace_{wspace_tag}.root')
wspace_name         = f'wspace_vt3m'

# **** CONSTANTS  *** #
tau_mass = 1.777 # GeV
mass_window_lo, mass_window_hi = config.mass_range_lo, config.mass_range_hi # GeV
blind_region_lo, blind_region_hi = config.blind_range_lo, config.blind_range_hi # GeV
fit_range_lo  , fit_range_hi   = blind_region_lo - 0.05, blind_region_hi + 0.05 # GeV

vars, mass = fitu.load_data(mass_window_lo, mass_window_hi, blind_region_lo, blind_region_hi, fit_range_lo, fit_range_hi)
thevars = ROOT.RooArgSet(*vars)

# binning
bin_w = 0.01 # GeV
nbins = int(np.rint((mass_window_hi-mass_window_lo)/bin_w)) # needed just for plotting, fits are all unbinned

# **** EVENT SELECTION ****
base_selection      = ' & '.join([
    config.cat_eta_selection_dict_fit[args.category], 
    config.year_selection['20'+args.year],
    config.phi_veto,
])

if args.save_ws : file_ws = ROOT.TFile(wspace_filename, "RECREATE")



   
# output tag
 # replace dot with p for the tag
# BDT selection
bdt_selection       = f'(bdt_score > {cut:,.4f})'
sgn_selection       = ' & '.join([bdt_selection, base_selection])

# **** IMPORT SIGNAL ****
print(f'\n\n{ct.PURPLE}------ SIGNAL (W)Tau3Mu MC ------- {ct.END}')
mc_W_dataset, W_eff, W_Nmc = fitu.import_data_from_file(
    mc_W_file,
    thevars, 
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
    thevars, 
    input_tree_name, 
    dataset_name = f'mc_Z_{process_name}',
    base_cut=base_selection,
    full_cut=sgn_selection,
    verbose=True,
)
# exit if no signal events
if mc_W_dataset.sumEntries() == 0: exit()

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
    thevars,
    dataset_name = f'data_{process_name}',
    base_cut=base_selection + f' & {config.sidebands_selection}',
    full_cut=data_selection,
    verbose=True,
)
# skip if no events in one of the 2 sidebands
print (f'entries in left SB {bkg_dataset.sumEntries("", "left_SB")}')
print (f'entries in right SB {bkg_dataset.sumEntries("", "right_SB")}')
#if (bkg_dataset.sumEntries("", "left_SB") == 0 or bkg_dataset.sumEntries("", "right_SB") == 0): continue


# **** SIGNAL MODEL ****
Mtau   = ROOT.RooRealVar('Mtau' , 'Mtau' , tau_mass)
Mtau.setConstant(True)
# W -> tau(3mu) nu
dMtau_W   = ROOT.RooRealVar('dM_W', 'dM_W', 0, -0.04, 0.04)
mean_W    = ROOT.RooFormulaVar('mean_W','mean_W', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau_W) )
width_W   = ROOT.RooRealVar(f'signal_width_W_{catYY}',  f'signal_width_W_{catYY}',  0.01,    0.005, 0.05)
n_W       = ROOT.RooRealVar(f'n_W_{catYY}', f'n_W_{catYY}', 1.0, 0.1, 10.0)
alpha_W   = ROOT.RooRealVar(f'alpha_W_{catYY}', f'alpha_W_{catYY}', 1.0, 0.0, 10.0)

nsig_W         = ROOT.RooRealVar('model_sig_W%s_norm'%process_name, 'model_sig_W%s_norm'%process_name, mc_W_dataset.sumEntries(), 0.0, 10*mc_W_dataset.sumEntries())

gaus_W         = ROOT.RooGaussian('model_sig_W%s'%process_name, 'gaus_W%s'%process_name, mass, mean_W, width_W)
cb_W           = ROOT.RooCBShape('model_sig_W%s'%process_name, 'cb_W%s'%process_name, mass, mean_W, width_W, alpha_W, n_W)
signal_model_W = ROOT.RooAddPdf('ext_model_sig_W%s'%process_name, 'ext_model_sig_W%s'%process_name, ROOT.RooArgList(cb_W), nsig_W )

# Z -> tau(3mu) tau
dMtau_Z   = ROOT.RooRealVar('dM_Z', 'dM_Z', 0, -0.04, 0.04)
mean_Z    = ROOT.RooFormulaVar('mean_Z', 'mean_Z', '(@0+@1)', ROOT.RooArgList(Mtau,dMtau_Z) )
width_Z   = ROOT.RooRealVar(f'signal_width_Z_{catYY}',  f'signal_width_Z_{catYY}',  0.01,    0.005, 0.05)
n_Z       = ROOT.RooRealVar(f'n_Z_{catYY}', f'n_Z_{catYY}', 1.0, 0.1, 10.0)
alpha_Z   = ROOT.RooRealVar(f'alpha_Z_{catYY}', f'alpha_Z_{catYY}', 1.0, 0.0, 10.0)

nsig_Z   = ROOT.RooRealVar('model_sig_Z%s_norm'%process_name, 'model_sig_Z%s_norm'%process_name, mc_Z_dataset.sumEntries(), 0.0, 10*mc_Z_dataset.sumEntries())

cb_Z           = ROOT.RooCBShape('model_sig_Z%s'%process_name, 'cb_Z%s'%process_name, mass, mean_Z, width_Z, alpha_Z, n_Z)
gaus_Z         = ROOT.RooGaussian('model_sig_Z%s'%process_name, 'gaus_Z%s'%process_name, mass, mean_Z, width_Z)
signal_model_Z = ROOT.RooAddPdf('ext_model_sig_Z%s'%process_name, 'ext_model_sig_Z%s'%process_name, ROOT.RooArgList(cb_Z), nsig_Z )

# fix W to Z yield
nsig_W.setConstant(True)
nsig_Z.setConstant(True)
r_wz = ROOT.RooRealVar(f'r_wz_{catYY}', f'r_wz_{catYY}', nsig_W.getValV()/(nsig_W.getValV()+nsig_Z.getValV()))

s_model = ROOT.RooAddPdf(f'model_sig_{process_name}', f'model_sig_{process_name}', ROOT.RooArgList(cb_W, cb_Z), ROOT.RooArgList(r_wz))

# **** BACKGROUND MODEL ****
bkg_model_name = f'model_bkg_{process_name}'
    
# exponential
slope = ROOT.RooRealVar(f'background_slope_{catYY}', f'background_slope_{catYY}', 0.0, -5.0, 5.0)
expo  = ROOT.RooExponential(bkg_model_name, bkg_model_name, mass, slope)
# constant
const = ROOT.RooPolynomial(bkg_model_name,bkg_model_name, mass)

b_model = expo
if args.bkg_func == 'const':
    b_model = const
    print(f'{ct.BOLD}[i]{ct.END} fit background with constant')
elif args.bkg_func == 'multipdf':
    b_model, enevlope = get_multipdf(args.multipdf_ws, 'w', catYY)
    if not b_model:
        print(f'{ct.RED}[ERROR]{ct.END} multipdf model not found in {args.multipdf_ws}')
        exit()
    b_model.SetName(bkg_model_name)
else : print(f'{ct.BOLD}[i]{ct.END} fit background with exponential')

# number of background events
nbkg = ROOT.RooRealVar('model_bkg_%s_norm'%process_name, 'model_bkg_%s_norm'%process_name, bkg_dataset.sumEntries(), 0., 3*bkg_dataset.sumEntries())
print(f'[debug] entries in data {bkg_dataset.numEntries()}')
#ext_bkg_model = ROOT.RooExtendPdf(f'ext_model_bkg{process_name}', f'ext_model_bkg{process_name}', b_model, nbkg, "full_range")
ext_bkg_model = ROOT.RooAddPdf(f'ext_model_bkg{process_name}', f'ext_model_bkg{process_name}', ROOT.RooArgSet(b_model), ROOT.RooArgSet(nbkg))

# **** TIME TO FIT ****
# signal fit
results_gaus_W = signal_model_W.fitTo(
    mc_W_dataset, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
    ROOT.RooFit.PrintLevel(-1),
)
results_gaus_W.Print()
results_gaus_Z = signal_model_Z.fitTo(
    mc_Z_dataset, 
    ROOT.RooFit.Range('fit_range'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.Extended(ROOT.kTRUE),
    ROOT.RooFit.SumW2Error(True),
    ROOT.RooFit.PrintLevel(-1),
)
results_gaus_Z.Print()
# * draw & save
frame_W = mass.frame()
frame_W.SetTitle('#tau -> 3#mu signal - CAT %s BDTscore > %.4f'%(args.category, cut))

mc_W_dataset.plotOn(
    frame_W, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kRed),
    ROOT.RooFit.DataError(1),
)
signal_model_W.plotOn(
    frame_W, 
    ROOT.RooFit.LineColor(ROOT.kRed),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range'),
    ROOT.RooFit.MoveToBack()
)

frame_Z = mass.frame()
frame_Z.SetTitle('#tau -> 3#mu signal - CAT %s BDTscore > %.4f'%(args.category, cut))
mc_Z_dataset.plotOn(
    frame_Z, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.XErrorSize(0), 
    ROOT.RooFit.LineWidth(2),
    ROOT.RooFit.FillColor(ROOT.kGreen+3),
    ROOT.RooFit.DataError(1),
)
signal_model_Z.plotOn(
    frame_Z, 
    ROOT.RooFit.LineColor(ROOT.kGreen+3),
    ROOT.RooFit.Range('full_range'),
    ROOT.RooFit.NormRange('full_range'),
    ROOT.RooFit.MoveToBack()
)    
if not args.goff:
    fitu.draw_fit_pull(frame_W, fitvar=mass, out_name=f'{args.plot_outdir}/massfit_S_Wt3m_{point_tag}')
    fitu.draw_fit_pull(frame_Z, fitvar=mass, out_name=f'{args.plot_outdir}/massfit_S_Zt3m_{point_tag}')

# fit background
results_expo = ext_bkg_model.fitTo(
    bkg_dataset, 
    ROOT.RooFit.Range('left_SB,right_SB'), 
    ROOT.RooFit.Save(),
    ROOT.RooFit.PrintLevel(-1),
)
results_expo.Print()

# * draw & save
frame_b = fitu.draw_full_fit(
    mass, 
    [mc_W_dataset, mc_Z_dataset], [signal_model_W, signal_model_Z], 
    bkg_dataset, ext_bkg_model, 
    nbins, 
    title='#tau -> 3 #mu signal+bkg - CAT %s BDTscore > %.3f'%(args.category, cut),
) 
if USE_CMS_STYLE:
    frame_b.SetTitle('')
    fitu.apply_cms_style(frame_b, 
                            outfile='%s/massfit_SB_%s'%(args.plot_outdir, point_tag), 
                            cat=args.category, 
                            year='20'+args.year, 
                            Preliminary=True,
                            ymax=np.round(1.2*frame_b.GetMaximum()) if args.bdt_cut < 0.990 else 10,
                            )
else:
    # print N signal and N background on plot
    fitu.add_summary_text(frame_b, f'Nw = {nsig_W.getValV():.2f} +/- {nsig_W.getError():.2f}', x = tau_mass, y=0.90*frame_b.GetMaximum())
    fitu.add_summary_text(frame_b, f'Nz = {nsig_Z.getValV():.2f} +/- {nsig_Z.getError():.2f}', x = tau_mass, y=0.85*frame_b.GetMaximum())
    fitu.add_summary_text(frame_b, f'Nb = {nbkg.getValV():.2f} +/- {nbkg.getError():.2f}',     x = tau_mass, y=0.80*frame_b.GetMaximum())  
    c2 = ROOT.TCanvas("c2", "c2", 800, 800)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
    frame_b.SetMinimum(1e-5)
    frame_b.Draw()
    c2.SaveAs('%s/massfit_SB_%s.png'%(args.plot_outdir, point_tag)) 
    c2.SaveAs('%s/massfit_SB_%s.pdf'%(args.plot_outdir, point_tag))
    if not args.goff :
        c2.SetLogy(1)
        c2.SaveAs('%s/massfit_SB_Log_%s.png'%(args.plot_outdir, point_tag)) 
        c2.SaveAs('%s/massfit_SB_Log_%s.pdf'%(args.plot_outdir, point_tag))



# S/B in SR
B = (nbkg.getValV())*(ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), 'sig_range').getValV())
# debug
print(f'\n\n{ct.BOLD}------ DEBUG ------{ct.END}')
print(f'  B normalization (fit) : {nbkg.getValV():.1f} ({ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "full_range").getValV():.3f})')
print(f'  B in SR (fit)         : {B:.1f} ({ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "sig_range").getValV():.3f})')
print(f'  B in SB (fit)         : {nbkg.getValV()*ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "left_SB").getValV():.1f} ({ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "left_SB").getValV():.3f}) || {nbkg.getValV()*ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "right_SB").getValV():.1f} ({ext_bkg_model.createIntegral(ROOT.RooArgSet(mass), ROOT.RooArgSet(mass), "right_SB").getValV():.3f})')
Berr = np.sqrt(B) if B > 0.5 else 3.0
Sw = nsig_W.getValV() 
Punzi_S = W_eff/(0.5 + sqrt(B))
Punzi_S_err = Punzi_S * np.sqrt( (W_eff_error/W_eff)**2 + (Berr/(2*sqrt(B)*(0.5 + np.sqrt(B))))**2)
AMS = sqrt(2 * ( (Sw + B)*np.log(1+Sw/B) - Sw) )

print(f'\n\n{ct.BOLD}---------- SUMMARY ----------{ct.END}')
print(f'{ct.GREEN}SELECTION{ct.END} :')
print(base_selection)
print(f' Nb in SR (fit)     : {B:.3f} +/- {Berr:.3f}')
print(f' Nb in FR (fit)     : {nbkg.getValV():.3f} +/- {nbkg.getError():.3f}')
print(f' Nb in SB (raw)     : {bkg_dataset.numEntries()}')
print(f' Nb in FR (raw)     : {N_data_BDT}')
print(f' Nw       (fit): {nsig_W.getValV():.3f} +/- {nsig_W.getError():.3f}')
print(f' Nz       (fit): {nsig_Z.getValV():.3f} +/- {nsig_Z.getError():.3f}')
print(f' Nw/Nz    (fit): {nsig_W.getValV()/nsig_Z.getValV():.2f}')
print(f' Nw/Nz    (raw): {mc_W_dataset.sumEntries()/mc_Z_dataset.sumEntries():.2f}')
print(f'{ct.BOLD}---------------------------------{ct.END}\n\n')

if not args.save_ws: exit()
# ----------------------------------------------------------------------------------------------------
#### SAVE MODEL TO A WORKSPACE ####
print(f'{ct.BOLD}[i]{ct.END} saving workspace {wspace_name} to {wspace_filename}')

# W channel: fix signal mean value - width is fixed only during wp optimization
dMtau_W.setConstant(True)
alpha_W.setConstant(True)
n_W.setConstant(True)
if (args.fix_w) : width_W.setConstant(True)
# Z channel: fix everything but width
dMtau_Z.setConstant(True)
alpha_Z.setConstant(True)
n_Z.setConstant(True)
if (args.fix_w) : width_Z.setConstant(True)

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

ws   = ROOT.RooWorkspace(wspace_name, wspace_name)
if args.bkg_func == 'multipdf':
    pdfs = ROOT.RooArgSet(s_model, enevlope)
else:
    pdfs = ROOT.RooArgSet(s_model, b_model)
ws.Import(
    pdfs,
    ROOT.RooFit.RenameVariable("tau_fit_mass", "m3m"),
    ROOT.RooFit.RecycleConflictNodes()
)
ws.Import(
    data,
    ROOT.RooFit.RenameVariable("tau_fit_mass", "m3m"),
    ROOT.RooFit.RecycleConflictNodes()
)
#getattr(ws, 'import')(data)
#getattr(ws, 'import')(s_model) 
#getattr(ws, 'import')(b_model)
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
    input_mc     = [mc_W_file, mc_Z_file],
    selection    = sgn_selection,
    ws_filename  = wspace_filename,
    workspace    = ws,
    datacard_name= datacard_name,
    year         = args.year,
    cat          = args.category,
    bkg_func     = args.bkg_func,
    Nobs         = -1 if runblind else fulldata.numEntries(),
    Nsig         = nsig_W.getValV() + nsig_Z.getValV(),
    Nbkg         = nbkg.getVal(),
    Ndata        = N_data,
    write_sys    = args.sys_unc,
)
