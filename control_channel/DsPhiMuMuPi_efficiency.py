#############################################
#  sPlots Ds -> Phi(MuMu)Pi signal and bkg   #
#############################################

import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import numpy as np
import math
import argparse
import sys
sys.path.append('..')
import mva.config as config
import plots.plotting_tools as pt
import plots.color_text as ct
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(True)
ROOT.gStyle.SetPadTickY(True)
ROOT.gStyle.SetHistMinimumZero()
ROOT.TH1.SetDefaultSumw2()
ROOT.RooMsgService.instance().setSilentMode(True)

category_list = ['ABC','A', 'B', 'C']
parser = argparse.ArgumentParser()
parser.add_argument('--workspace_preBDT', help=' RooWorkSpace with signal and background model')
parser.add_argument('--workspace_postBDT',help=' RooWorkSpace with signal and background model')
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/sPlot/', help=' output directory for plots')
parser.add_argument('-y', '--year',     choices= ['2022', '2023'], default= '2022', help='year of data taking')
parser.add_argument('--category',       choices= category_list, default= 'A', help='category to be used for the efficiency')
parser.add_argument('--bdt_cut',        type=float, default= 0.960, help='BDT cut value')
parser.add_argument('--tag',            default= 'reMini', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')

args = parser.parse_args()
tag = f'cat{args.category}' + (f'_bdt{args.bdt_cut:,.2f}' if args.bdt_cut > 0. else '') + f'_{args.tag}'

wspace_preBDT_list = [
    f'workspaces/DsPhiPi2022_wspace_catABC_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catA_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catB_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catC_{args.tag}.root',
]
wspace_postBDT_list = [
    f'workspaces/DsPhiPi2022_wspace_catABC_bdt{args.bdt_cut}_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catA_bdt{args.bdt_cut}_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catB_bdt{args.bdt_cut}_{args.tag}.root',
    f'workspaces/DsPhiPi2022_wspace_catC_bdt{args.bdt_cut}_{args.tag}.root',
]

preBDT_dict = dict(zip(category_list, wspace_preBDT_list))
postBDT_dict = dict(zip(category_list, wspace_postBDT_list))


# **** USEFUL CONSTANT VARIABLES *** #
mass_window_lo, mass_window_hi = config.Ds_mass_range_lo, config.Ds_mass_range_hi # GeV
fit_range_lo  , fit_range_hi   = mass_window_lo, mass_window_hi # GeV

nbins = 20 # needed just for plotting, fits are all unbinned

# *** INPUT DATA AND MONTE CARLO *** #
base_selection = '(' + ' & '.join([
    config.year_selection[args.year],
    config.Ds_base_selection,
    config.Ds_phi_selection,
    config.Tau_sv_selection,
]) + ')'
print('[i] base_selection = %s'%base_selection)

input_tree_name = 'tree_w_BDT'
mc_file     = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]
data_file   = [ '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_DsPhiMuMuPi_DATA_Optuna_HLT_overlap_LxyS2.1_2024Jul11.root' ]

# signal MC 
mc_tree = ROOT.TChain(input_tree_name)
[mc_tree.AddFile(f) for f in mc_file]
mc_rdf = ROOT.RDataFrame(input_tree_name, mc_file)
print('[+] MC entries = %.2f'%mc_rdf.Count().GetValue())

wspace_data_name = 'DsPhiPi_data_wspace' 
efficiency_data, efficiency_data_err = [], []
effiency_mc, effiency_mc_err = [], []
for cat in category_list:
#cat = args.category
    # *** YIELDS in DATA FROM WSPACE *** #
    ## + pre BDT model
    if not args.workspace_preBDT: wspace_data_preBDT = ROOT.TFile(preBDT_dict[cat]).Get(wspace_data_name)
    nDs_data_preBDT = wspace_data_preBDT['nDs'].getValV()
    nDs_data_preBDT_err = wspace_data_preBDT['nDs'].getError()
    ## + post BDT model
    if not args.workspace_postBDT: wspace_postBDT = ROOT.TFile(postBDT_dict[cat]).Get(wspace_data_name)
    nDs_data_postBDT = wspace_postBDT['nDs'].getValV()
    nDs_data_postBDT_err = wspace_postBDT['nDs'].getError()

    eff_d = nDs_data_postBDT / nDs_data_preBDT
    eff_de = eff_d * sqrt( (nDs_data_postBDT_err/nDs_data_postBDT)**2 + (nDs_data_preBDT_err/nDs_data_preBDT)**2 )
    print(f'{ct.color_text.BOLD}[+] DATA efficiency for category {cat}  {nDs_data_postBDT:,.0f} / {nDs_data_preBDT:,.0f} = ({eff_d*100:,.2f} +/- {eff_de*100:,.2f}) %{ct.color_text.END}')
    efficiency_data.append(eff_d)
    efficiency_data_err.append(eff_de)

    bdt_selection = ' & '.join([config.Ds_category_selection[cat], f'(bdt_score > {args.bdt_cut})'])
    # MC efficiency
    nDs_mc_preBDT = mc_rdf.Filter(config.Ds_category_selection[cat]).Sum('weight').GetValue()
    nDs_mc_postBDT= mc_rdf.Filter(bdt_selection).Sum('weight').GetValue()
    effiency_mc.append(nDs_mc_postBDT/nDs_mc_preBDT)
    effiency_mc_err.append(0.0)
    print(f'{ct.color_text.BOLD}[+] MC efficiency for category {cat} {nDs_mc_postBDT:,.0f} / {nDs_mc_preBDT:,.0f}  = {nDs_mc_postBDT/nDs_mc_preBDT*100:,.2f} %{ct.color_text.END}')

# PLOT RESULTS wit ratio data/mc
import matplotlib.pyplot as plt
import numpy as np
fig, (ax, ax_ratio) = plt.subplots(2,1, sharex=True, figsize=(6,6), gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0, )
# Calculate the ratio of data efficiency to MC efficiency
efficiency_ratio = [data_eff/mc_eff for data_eff, mc_eff in zip(efficiency_data, effiency_mc)]

ax.errorbar(category_list, efficiency_data, yerr=efficiency_data_err, fmt='o', label='Data')
ax.errorbar(category_list, effiency_mc, yerr=effiency_mc_err, fmt='o', label='MC')
ax.grid()
ax.set_ylim(0.02,0.10)
ax.set_ylabel('Efficiency', fontsize=16)
ax.legend(fontsize=16)

# Create a new subplot for the ratio
ax_ratio.plot(category_list, efficiency_ratio, 'o', color='green')
ax_ratio.set_ylabel('Data / MC ', fontsize=16)
ax_ratio.set_ylim(0.5, 2.0)
ax_ratio.set_xlabel('Category', fontsize=16)
ax_ratio.grid()

# Adjust the layout to accommodate the new subplot
fig.tight_layout()

plt.savefig(f'{args.plot_outdir}/DsPhiPi_efficiency_{tag}.png')
plt.savefig(f'{args.plot_outdir}/DsPhiPi_efficiency_{tag}.pdf')
print(f'[+] Efficiency plot saved in {args.plot_outdir}/DsPhiPi_efficiency_{tag}.png')

exit()
# DATA efficiency
#  fit data pre BDT cut ...
data_preBDT = datatofit.reduce(cat_selection_dict[cat])
full_model.fitTo(data_preBDT, ROOT.RooFit.Range('fit_range'))
N_data_preBDT = wspace_data['nDs'].getValV()

# plot pre BDT data and fit
frame_preBDT = mass.frame(Title=" ", Bins= 2*nbins)
data_preBDT.plotOn(
    frame_preBDT,
    ROOT.RooFit.Binning(2*nbins),
    ROOT.RooFit.MarkerSize(1.)
)
full_model.plotOn(
    frame_preBDT,
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range'),
    ROOT.RooFit.MoveToBack(),
)
full_model.paramOn(frame_preBDT, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
c = ROOT.TCanvas("c", "c", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame_preBDT.Draw()
c.SaveAs('%s/DsPhiPi_mass_preBDT_%s.png'%(args.plot_outdir, tag))
c.SaveAs('%s/DsPhiPi_mass_preBDT_%s.pdf'%(args.plot_outdir, tag))


N_data_preBDT_tot += N_data_preBDT

data_postBDT = data_preBDT.reduce(bdt_selection)
full_model.fitTo(data_postBDT, ROOT.RooFit.Range('fit_range'))
N_data_postBDT = wspace_data['nDs'].getValV()
N_data_postBDT_tot += N_data_postBDT

frame = mass.frame(Title=" ", Bins= nbins)
data_postBDT.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
full_model.plotOn(
frame, 
ROOT.RooFit.LineColor(ROOT.kBlue),
ROOT.RooFit.Range('fit_range'),
ROOT.RooFit.NormRange('fit_range'),
ROOT.RooFit.MoveToBack(),
)
full_model.paramOn(frame, ROOT.RooFit.Layout(0.6, 0.9, 0.9))
c = ROOT.TCanvas("c", "c", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.GetXaxis().SetRangeUser(fit_range_lo,fit_range_hi)
frame.Draw()
c.SaveAs('%s/DsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/DsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag))


print(f'{ct.color_text.BOLD}[+] MC efficiency for category {cat} {N_mc_postBDT} / {N_mc_preBDT}  = {N_mc_postBDT/N_mc_preBDT*100:,.2f} %{ct.color_text.END}')
print(f'{ct.color_text.BOLD}[+] MC efficiency from RooDataSet {fullmc.sumEntries(bdt_selection):,.0f} / {fullmc.sumEntries(cat_selection_dict[cat]):,.0f} {ct.color_text.END}')
print(f'{ct.color_text.BOLD}[+] DATA efficiency for category {cat} {N_data_postBDT} / {N_data_preBDT}  = {N_data_postBDT/N_data_preBDT*100:,.2f} % {ct.color_text.END}')


print(f'[+] MC efficiency total {N_mc_postBDT_tot} / {N_mc_preBDT_tot} = { N_mc_postBDT_tot/N_mc_preBDT_tot*100:,.2f} %')

exit()
# Fit to mc & fix the parameters
#signal_model.fitTo(fullmc, ROOT.RooFit.Range('fit_range'))
#nMC = wspace_mc['nMC']
#nMC.setConstant()
#nBflat = wspace_mc['nBflat']
#nBflat.setConstant()
# Fit to data & fix the parameters

# * MC normalization
#fnorm_mc = ROOT.RooFormulaVar('fnorm_mc','fnorm_mc', '(@0/@1)', ROOT.RooArgList(nDs,nMC) )

frame = mass.frame(Title=" ", Bins= nbins)
datatofit.plotOn(
    frame, 
    ROOT.RooFit.Binning(nbins), 
    ROOT.RooFit.MarkerSize(1.)
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.LineColor(ROOT.kBlue),
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.NormRange('fit_range'),
    ROOT.RooFit.MoveToBack(),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components('gsum_data'),
    ROOT.RooFit.LineColor(ROOT.kRed),
)
full_model.plotOn(
    frame, 
    ROOT.RooFit.Components('gaus_Dp'),
    ROOT.RooFit.LineColor(ROOT.kOrange),
)
text_NDs = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.90*frame.GetMaximum(), "N_Ds = %.0f +/- %.0f"%(nDs.getValV(), nDs.getError()))
text_NDp = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.85*frame.GetMaximum(), "N_D+ = %.0f +/- %.0f"%(nB.getValV() * (Dp_f.getValV()), nB.getError()))
text_Nb  = ROOT.TText(config.Ds_mass_range_lo + 0.02, 0.80*frame.GetMaximum(), "Nb   = %.0f +/- %.0f"%(nB.getValV() * (1-Dp_f.getValV()), nB.getError()))
text_NDs.SetTextSize(0.035)
text_NDp.SetTextSize(0.035)
text_Nb.SetTextSize(0.035)
frame.addObject(text_NDs)
frame.addObject(text_NDp)
frame.addObject(text_Nb)
c = ROOT.TCanvas("c", "c", 1200, 800)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.15)
frame.GetXaxis().SetRangeUser(fit_range_lo,fit_range_hi)
frame.Draw()
c.SaveAs('%s/DsPhiPi_mass_%s.png'%(args.plot_outdir, tag)) 
c.SaveAs('%s/DsPhiPi_mass_%s.pdf'%(args.plot_outdir, tag))