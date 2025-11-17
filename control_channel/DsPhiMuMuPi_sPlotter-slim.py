import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import argparse
import numpy as np

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
print(f'[i] sys.path = {sys.path[0]}')
import mva.config as cfg
import plots.plotting_tools as pt

def add_overunderflow(histo):
    """
    Add overflow and underflow bins to the histogram.
    """
    nbins = histo.GetNbinsX()
    xlow  = histo.GetXaxis().GetXmin()
    xhigh = histo.GetXaxis().GetXmax()
    bin_width = (xhigh - xlow) / nbins

    # new histogram with N+2 bins to include underflow and overflow
    h_with_extra = ROOT.TH1F(histo.GetName()+"_extra", histo.GetTitle(), nbins + 2, xlow - bin_width, xhigh + bin_width)

    # Fill bin contents: shift everything by 1 to make room for underflow at bin 1
    for i in range(nbins + 2):  # bins 0 to nbins+1 in original
        content = histo.GetBinContent(i)
        error = histo.GetBinError(i)
        h_with_extra.SetBinContent(i + 1, content)
        h_with_extra.SetBinError(i + 1, error)
    
    return h_with_extra

def make_sPlot(
        observable, 
        mc_norm = 'total_weight',
        selection = '', 
        nbins = 100, lo = 0, hi = 100, 
        log_scale = False,
        x_axis_title = '', y_axis_title = '',
        color = ROOT.kRed, 
        to_ploton = None, 
        add_tag = '',
        underoverflow = False,
        ratio_w = 1.0,
    ):
    
    h_mc = mc_rdf.Histo1D(('h_'+observable+'_mc', '', nbins, lo, hi), observable, mc_norm).GetValue()
    if underoverflow: h_mc = add_overunderflow(h_mc)
    h_mc.SetFillColor(color)
    h_mc.SetFillStyle(3004)
    h_mc.SetLineColor(color)
    h_mc.SetLineWidth(2)
    h_mc.SetMarkerStyle(0)

    h_sData = sData_rdf.Histo1D(('h_'+observable+'_sData', '', nbins, lo, hi), observable, 'nDs_sw').GetValue()
    if underoverflow: h_sData = add_overunderflow(h_sData)
    h_sData.SetMarkerColor(ROOT.kBlack)
    h_sData.SetMarkerStyle(20)
    h_sData.SetLineColor(ROOT.kBlack)
    h_sData.SetLineWidth(2)

    # build legend
    leg = ROOT.TLegend(0.40, 0.75, 0.90, 0.89)
    leg.AddEntry(h_mc, f"{cfg.legend_process['DsPhiPi']} MC", "F")
    leg.AddEntry(h_sData, "data (bkg subtracted)", "pe")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetFillStyle(0)
    # set up axis
    h_mc.GetXaxis().SetTitle(x_axis_title)
    h_mc.GetYaxis().SetTitle(y_axis_title)
    #h_mc.SetMaximum(1.3 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()]))
    to_ploton.append(leg)

    lo, hi = h_mc.GetXaxis().GetXmin(), h_mc.GetXaxis().GetXmax()
    tag = f'_{args.year}' + (f'_{args.tag}' if args.tag else '') + (f'_{add_tag}' if add_tag else '')
    pt.ratio_plot_CMSstyle(
        [h_sData],
        h_mc,
        to_ploton = to_ploton,
        file_name = f'{args.plot_outdir}/DsPhiPi_SW{observable}{tag}',
        draw_opt_num = 'pe',
        draw_opt_den = 'histe2',
        ratio_w      = ratio_w,
        y_lim = [0, 1.5 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()])],
        x_lim = [lo, hi],
        log_y = log_scale,
        year = args.year,
    )
    return 0


    

# --- parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='../models/sWeights_Optuna_HLT_overlap_LxyS2.1_2024Jul11_2022only_DataMc.root')
parser.add_argument('--plot_outdir', type=str, default='/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/cut_LxySign/Training_kFold_Optuna_HLT_overlap_LxyS2.1_2024Jul11/DsPhiPi_control/')
parser.add_argument('-y','--year',   type=str, default='2022')
parser.add_argument('--tag', type=str, default='')
args = parser.parse_args()

# --- check if output directory exists
if not os.path.exists(args.plot_outdir):
    os.makedirs(args.plot_outdir)
    os.system(f'cp ~/public/index.php {args.plot_outdir}')
    print(f'[+] created output directory {args.plot_outdir}')
else:
    print(f'[+] output directory {args.plot_outdir} already exists')

# --- get tree from input file
# mc
mc_rdf = ROOT.RDataFrame('mc_tree', args.input).Define('total_weight', 'weight*norm_factor*w_byEta')
if not mc_rdf:
    print(f'[ERROR]: tree not found in file {args.input}')
    sys.exit(1)
sData_rdf = ROOT.RDataFrame('data_tree', args.input)
if not sData_rdf:
    print(f'[ERROR]: tree not found in file {args.input}')
    sys.exit(1)

# --- do sPlot
base_selection = '(' + ' & '.join([
    cfg.year_selection[args.year],
    cfg.Ds_base_selection,
    cfg.Ds_phi_selection,
    cfg.Tau_sv_selection,
]) + ')'
print('[i] base_selection = %s'%base_selection)
# BDT input features
observable_list = cfg.features + ['Ds_fit_eta', 'bdt_score']
observable_list  = ['bdt_score', 'Ds_fit_eta']
no_overunderflow = ['tauEta', 'tau_mu1_TightID_PV', 'tau_mu2_TightID_PV', 'tau_mu3_TightID_PV', 'tau_fit_vprob', 'bdt_score']

for obs in observable_list:

    print(f'\n[+] plotting {obs}')
    nbins, xlo, xhi, xlabel, logscale = cfg.features_NbinsXloXhiLabelLog[obs]
    make_sPlot(
        observable = obs,
        mc_norm = 'total_weight',
        selection = base_selection,
        nbins   = nbins,
        lo      = xlo,
        hi      = xhi,
        x_axis_title = xlabel,
        y_axis_title= 'Events',
        log_scale   = logscale,
        color   = ROOT.kGreen+1,
        to_ploton = [],
        add_tag = '',
        underoverflow = obs not in no_overunderflow
    )

# ZOOM on BDT score
make_sPlot(
        observable = 'bdt_score',
        mc_norm = 'total_weight',
        selection = base_selection,
        nbins   = 25,
        lo      = 0.900,
        hi      = 1.0,
        x_axis_title = 'BDT score',
        y_axis_title= 'Events',
        log_scale   = False,
        color   =  ROOT.kGreen+1,
        to_ploton = [],
        add_tag = 'zoom',
        underoverflow = False,
        ratio_w = 2.0,
    )
# print BDT efficiency
bdt_th = 0.993
Nmc = mc_rdf.Sum('total_weight')
bdt_eff_mc = mc_rdf.Filter(f'bdt_score>{bdt_th}').Sum('total_weight').GetValue() / Nmc.GetValue()
bdt_eff_mc_err = np.sqrt(bdt_eff_mc * (1 - bdt_eff_mc) / Nmc.GetValue())
print(f'  = BDT >{bdt_th:.3f} = {bdt_eff_mc*100:.2f}% +/- {bdt_eff_mc_err*100:.2f}% of MC kept ({Nmc.GetValue():.1f} -> {bdt_eff_mc*Nmc.GetValue():.1f})')
Ndata = sData_rdf.Sum('nDs_sw')
bdt_eff_data = sData_rdf.Filter(f'bdt_score>{bdt_th}').Sum('nDs_sw').GetValue() / Ndata.GetValue()
bdt_eff_data_err = np.sqrt(bdt_eff_data * (1 - bdt_eff_data) / Ndata.GetValue())
print(f'  = BDT >{bdt_th:.3f} = {bdt_eff_data*100:.2f}% +/- {bdt_eff_data_err*100:.2f}% of data kept ({Ndata.GetValue():.1f} -> {bdt_eff_data*Ndata.GetValue():.1f})')