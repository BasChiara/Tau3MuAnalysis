import ROOT
ROOT.gROOT.SetBatch(True)
import argparse
import numpy as np

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
print(f'[i] sys.path = {sys.path[0]}')
import mva.config as cfg
import plots.plotting_tools as pt

def make_sPlot(
        observable, 
        mc_norm = 'norm_factor' ,
        selection = '', 
        nbins = 100, lo = 0, hi = 100, 
        log_scale = False,
        x_axis_title = '', y_axis_title = '',
        color = ROOT.kRed, 
        to_ploton = None, 
        add_tag = ''
    ):
    # MC matched
    mc_tree.Draw(f'{observable}>>h_{observable}_mc({nbins}, {lo}, {hi})', f'({selection}) * (weight * {mc_norm})', 'goff')
    h_mc = ROOT.gDirectory.Get(f"h_{observable}_mc")
    h_mc.SetFillColor(color)
    h_mc.SetFillStyle(3004)
    h_mc.SetLineColor(color)
    h_mc.SetLineWidth(2)
    h_mc.Sumw2()
    # DATA sWeighted
    sData_tree.Draw(f'{observable}>>h_{observable}_data({nbins}, {lo}, {hi})', f'{selection} * nDs_sw', 'goff')
    h_sData = ROOT.gDirectory.Get(f"h_{observable}_data")
    h_sData.SetMarkerColor(ROOT.kBlack)
    h_sData.SetMarkerStyle(20)
    h_sData.SetLineColor(ROOT.kBlack)
    h_sData.SetLineWidth(2)
    h_sData.Sumw2()
    # build legend
    leg = ROOT.TLegend(0.40, 0.70, 0.75, 0.90)
    leg.AddEntry(h_mc, "MC (norm. to D_{s}#rightarrow#phi(#mu#mu)#pi in data)", "F")
    leg.AddEntry(h_sData, "data (bkg subtracted)")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetFillStyle(0)
    # set up axis
    h_mc.GetXaxis().SetTitle(x_axis_title)
    h_mc.GetYaxis().SetTitle(y_axis_title)
    #h_mc.SetMaximum(1.3 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()]))
    to_ploton.append(leg)

    tag = f'_{args.year}' + (f'_{args.tag}' if args.tag else '') + (f'_{add_tag}' if add_tag else '')
    pt.ratio_plot_CMSstyle(
        [h_sData],
        h_mc,
        to_ploton = to_ploton,
        file_name = f'{args.plot_outdir}/DsPhiPi_SW{observable}{tag}',
        draw_opt_num = 'pe',
        draw_opt_den = 'histe2',
        ratio_w      = 1.0,
        y_lim = [0, 1.5 * np.max([h_mc.GetMaximum(), h_sData.GetMaximum()])],
        x_lim = [lo, hi],
        log_y = log_scale,
        year = args.year,
    )
    return 0

def reweight_by_observable(observable = 'Ds_fit_eta'):
    
    nbins, lo, hi = cfg.features_NbinsXloXhiLabelLog[observable][0:3]
    selection = '1'
    mc_norm = 'norm_factor'

    mc_tree.Draw(f'{observable}>>h_{observable}_mc({nbins}, {lo}, {hi})', f'({selection}) * (weight * {mc_norm})', 'goff')
    h_mc = ROOT.gDirectory.Get(f"h_{observable}_mc")
    h_mc.Sumw2()
    sData_tree.Draw(f'{observable}>>h_{observable}_data({nbins}, {lo}, {hi})', f'{selection} * nDs_sw', 'goff')
    h_sData = ROOT.gDirectory.Get(f"h_{observable}_data")
    h_sData.Sumw2()

    h_ratio_eta = h_sData.Clone('h_ratio_eta')
    h_ratio_eta.Divide(h_mc)

    # print h_ratio_eta content
    for i in range(1, h_ratio_eta.GetNbinsX() + 1):
        print(f'bin {i}: {h_ratio_eta.GetBinContent(i)}')

    
    return h_ratio_eta

def apply_reweighting(observable, h_weights, weight_by = 'Ds_fit_eta', nbins = 30, lo = -3, hi = 3, selection = '1', to_ploton = [], add_tag = '', cat = 'ABC'):
    # create reweighted histogram
    h_reweighted = ROOT.TH1F(f'h_{observable}_reweighted', f'{observable} reweighted by #eta', nbins, lo, hi)
    for i in range(mc_tree.GetEntries()):
        # get entry
        mc_tree.GetEntry(i)
        if cat == 'A' and not (np.abs(mc_tree.Ds_fit_eta) < cfg.eta_thAB) : continue
        elif cat == 'B' and not (np.abs(mc_tree.Ds_fit_eta) > cfg.eta_thAB and np.abs(mc_tree.Ds_fit_eta) < cfg.eta_thBC) : continue
        elif cat == 'C' and not (np.abs(mc_tree.Ds_fit_eta) > cfg.eta_thBC) : continue
        # fill histogram
        this_weight = h_weights.GetBinContent(h_weights.FindBin(getattr(mc_tree, weight_by)))
        h_reweighted.Fill(
            getattr(mc_tree, observable), 
            this_weight * mc_tree.weight * mc_tree.norm_factor
        )
    
    # crate sData histogram
    sData_tree.Draw(f'{observable}>>h_{observable}_data({nbins}, {lo}, {hi})', f'{selection} * nDs_sw', 'goff')
    h_sData = ROOT.gDirectory.Get(f"h_{observable}_data")
    h_sData.SetMarkerColor(ROOT.kBlack)
    h_sData.SetMarkerStyle(20)
    h_sData.SetLineColor(ROOT.kBlack)
    h_sData.SetLineWidth(2)
    h_sData.Sumw2()
    # plot reweighted histogram with sData
    h_reweighted.SetStats(0)
    h_reweighted.SetFillColor(ROOT.kGreen+1)
    h_reweighted.SetFillStyle(3004)
    h_reweighted.SetLineColor(ROOT.kGreen+1)
    h_reweighted.SetLineWidth(2)
    h_reweighted.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[observable][3])
    h_reweighted.GetYaxis().SetTitle('Events')
    h_reweighted.GetYaxis().SetTitleOffset(1.5)
    h_reweighted.GetYaxis().SetTitleSize(0.04)
    h_reweighted.GetYaxis().SetLabelSize(0.04)
    h_reweighted.GetXaxis().SetTitleSize(0.04)
    h_reweighted.GetXaxis().SetLabelSize(0.04)
    h_reweighted.GetXaxis().SetTitleOffset(1.5)
    h_reweighted.SetMinimum(0)
    #h_reweighted.SetMaximum(1.3 * h_reweighted.GetMaximum())

    # create legend
    leg = ROOT.TLegend(0.40, 0.70, 0.75, 0.85)
    leg.AddEntry(h_reweighted, f'{observable} reweighted by#eta', 'F')
    leg.AddEntry(h_sData, 'data (bkg subtracted)')
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    to_ploton.append(leg)

    # draw ratio plot
    pt.ratio_plot_CMSstyle(
        [h_sData],
        h_reweighted,
        #to_ploton = to_ploton,
        file_name = f'{args.plot_outdir}/DsPhiPi_reweighted_{observable}{add_tag}',
        draw_opt_num = 'pe',
        draw_opt_den = 'histe2',
        ratio_w      = 1.0,
        y_lim = [0, 1.5 * h_reweighted.GetMaximum()],
        x_lim = [lo, hi],
        log_y = False,
        year = args.year,
    )
    return h_reweighted
    

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
infile = ROOT.TFile.Open(args.input)
# mc
mc_tree_name = 'mc_tree'
mc_tree = getattr(infile, mc_tree_name)
if not mc_tree:
    print(f'[ERROR]: tree {mc_tree_name} not found in file {args.input}')
    sys.exit(1)
data_tree_name = 'RooTreeDataStore_sData_data_fit'
sData_tree = getattr(infile, data_tree_name)
if not sData_tree:
    print(f'[ERROR]: tree {data_tree_name} not found in file {args.input}')
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
#observable_list = cfg.features + ['bdt_score']
observable_list  = ['bdt_score', 'Ds_Lxy_val_BS', 'Ds_Lxy_err_BS', 'tau_Lxy_sign_BS', 'Ds_fit_eta']
for obs in observable_list:

    print(f'\n[+] plotting {obs}')

    make_sPlot(
        observable = obs,
        mc_norm = 'norm_factor',
        selection = base_selection,
        nbins   = cfg.features_NbinsXloXhiLabelLog[obs][0],
        lo      = cfg.features_NbinsXloXhiLabelLog[obs][1],
        hi      = cfg.features_NbinsXloXhiLabelLog[obs][2],
        x_axis_title = cfg.features_NbinsXloXhiLabelLog[obs][3],
        y_axis_title= 'Events',
        log_scale   = cfg.features_NbinsXloXhiLabelLog[obs][4],
        color   = ROOT.kAzure if not 'bdt' in obs else ROOT.kRed,
        to_ploton = [],
        add_tag = '',
    )
# Ds eta
make_sPlot(
    observable = 'Ds_fit_eta',
    mc_norm = 'norm_factor',
    selection = base_selection,
    nbins   =   25,
    lo      = -2.5,
    hi      =  2.5,
    x_axis_title = '#eta(#mu#mu#pi)',
    y_axis_title= 'Events',
    log_scale   = False,
    color   = ROOT.kOrange,
    to_ploton = [],
    add_tag = '',
)


# --- reweight by eta
h_ratio_eta = reweight_by_observable(observable='Ds_fit_eta')
# --- reweight by Lxy sigma
#h_ratio_Lxy = reweight_by_observable(observable='Ds_Lxy_err_BS')

# --- apply reweighting
tag = f'_{args.year}' + (f'_{args.tag}' if args.tag else '')
#apply_reweighting('Ds_fit_eta', h_ratio_eta) # closure test
# bdt_score
apply_reweighting('bdt_score', 
                    h_ratio_eta, weight_by='Ds_fit_eta',
                    nbins=25, lo=0, hi=1, 
                    selection=base_selection, 
                    add_tag=f'{args.tag}_byEta'
                    )

for cat in cfg.Ds_category_selection:
    if cat == 'ABC' : continue
    to_ploton = []
    CAT_txt = ROOT.TLatex(0.4, 0.6, f"CAT {cat}")
    CAT_txt.SetNDC()
    CAT_txt.SetTextFont(43)
    CAT_txt.SetTextSize(40)
    to_ploton.append(CAT_txt)
    
   
    apply_reweighting('bdt_score', h_ratio_eta, 
                      nbins=25, lo=0, hi=1, 
                      selection=cfg.Ds_category_selection[cat], 
                      add_tag=f'cat{cat}{tag}', 
                      to_ploton=[CAT_txt], 
                      cat=cat)
    
# -- input features
for obs in observable_list:
    apply_reweighting(obs, h_ratio_eta, 
                      nbins   = cfg.features_NbinsXloXhiLabelLog[obs][0],
                      lo      = cfg.features_NbinsXloXhiLabelLog[obs][1],
                      hi      = cfg.features_NbinsXloXhiLabelLog[obs][2],
                      selection = base_selection,
                      to_ploton = [],
                      add_tag = tag +'_byEta',
    )

# --- close input file
infile.Close()
