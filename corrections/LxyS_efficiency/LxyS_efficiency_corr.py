import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import os
import json
import argparse
import numpy as np

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import mva.config as config
import plots.plotting_tools as pt


def make_eta_weights(dataframe_mc, dataframe_data, nbins, lo, hi, selection):
    # create histograms
    h_data = dataframe_data.Filter(selection).Histo1D((f'h_data_Ds_fit_eta', f'h_data_Ds_fit_eta', nbins, lo, hi), 'Ds_fit_eta', 'nDs_sw').GetValue()
    h_data.Sumw2()
    h_mc = dataframe_mc.Filter(selection).Define('total_w', f'norm_factor*weight').Histo1D((f'h_mc_Ds_fit_eta', f'h_mc_Ds_fit_eta', nbins, lo, hi), 'Ds_fit_eta', 'total_w').GetValue()
    h_mc.Sumw2()

    # create reweighting histogram
    h_reweight = h_data.Clone(f'h_reweight_Ds_fit_eta')
    h_reweight.Divide(h_mc)

    return h_reweight


def weighted_rdf(h_weight, dataframe):
    # Declare the C++ function to calculate the weight based on the mass value
    ROOT.gInterpreter.Declare(f"""
    TH1F* h_weight_global = (TH1F*)gROOT->FindObject("{h_weight.GetName()}");

    double get_weight(double eta_value) {{
        int bin = h_weight_global->FindBin(eta_value);
        return h_weight_global->GetBinContent(bin);
    }}
    """)
    # Define a new column "sb_weight" using the declared C++ function and the histogram
    dataframe = dataframe.Define("eta_weight", "get_weight(Ds_fit_eta)")
    dataframe = dataframe.Define("total_w", "eta_weight*norm_factor*weight")
    
    return dataframe

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='Input root file with sWeigted data', required=True)
argparser.add_argument('-o', '--output', help='output dest.', default='.')
argparser.add_argument('-y', '--year', choices = ['22', '23'], default='22', help='Year of the data taking period')
argparser.add_argument('--make_plots', action='store_true',  help='Wether to make plots or not')
args = argparser.parse_args()

# check if input file exists
if not os.path.exists(args.input):
    print(f'[ERROR]: input file {args.input} not found')
    sys.exit(1)
categories = ['A', 'B', 'C', 'ABC']
eff_data_list = []
eff_error_data_list = []
eff_mc_list = []
eff_error_mc_list = []
corr_dict = {}

base_selection = '(' + ' & '.join([
        config.year_selection['20'+args.year],
        config.Ds_base_selection,
        config.Ds_phi_selection,
        config.Tau_sv_selection
]) + ')'

#h_reweight = make_eta_weights(
#    ROOT.RDataFrame('mc_tree', args.input),
#    ROOT.RDataFrame('RooTreeDataStore_sData_data_fit', args.input), 
#    25, -2.5, 2.5, 
#    base_selection
#)
 
observables = {
    'tau_Lxy_sign_BS':{
        'bins' :np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30], dtype=float),
        'x_title': 'L_{xy}/#sigma',
    },
    'Ds_Lxy_val_BS':{
        'bins' : np.concatenate((np.linspace(0, 0.2, 10, dtype=float), np.linspace(0.3, 0.8, 5, dtype=float), np.array([1.0], dtype=float))),
        'x_title': 'L_{xy} (cm)',
    },
    'Ds_Lxy_err_BS':{
        'bins' : np.concatenate((np.array([0.002, 0.005, 0.008], dtype=float), np.linspace(0.010, 0.020, 10, dtype=float), np.array([0.030], dtype=float))),
        'x_title': 'L_{xy} error (cm)',
    },
}

for cat in categories:

    selection = '(' + ' & '.join([
        base_selection,
        config.Ds_category_selection[cat]
    ]) + ')'
    print(f'[i] CAT: {cat}')
    print(f' ->  selection: {selection}')

    # put data in RootDataFrame
    rdf_sData   = ROOT.RDataFrame('data_tree', args.input).Filter(selection)
    data_weight = 'nDs_sw'
    rdf_mc      = ROOT.RDataFrame('mc_tree', args.input).Filter(selection)
    mc_weight   = 'norm_byEta_weight'
    # apply the weights to MC dataframe
    #rdf_mc = weighted_rdf(h_reweight, rdf_mc)

    # evaluate efficeincy in Data and MC
    N_Data    = rdf_sData.Sum(data_weight).GetValue()
    eff_Data  = rdf_sData.Filter('tau_Lxy_sign_BS > 2.0').Sum(data_weight).GetValue() / N_Data
    eff_Data_err = np.sqrt(eff_Data*(1-eff_Data)/ N_Data)
    print(f'N_Data: {N_Data}, passed: {rdf_sData.Filter("tau_Lxy_sign_BS > 2.0").Sum(data_weight).GetValue()}')
    
    eff_data_list.append(eff_Data)
    eff_error_data_list.append(eff_Data_err)
    
    N_mc      = rdf_mc.Sum(mc_weight).GetValue()
    eff_mc    = rdf_mc.Filter('tau_Lxy_sign_BS > 2.0').Sum(mc_weight).GetValue() / N_mc
    eff_mc_err = np.sqrt(eff_mc*(1-eff_mc)/ N_mc)
    
    eff_mc_list.append(eff_mc)
    eff_error_mc_list.append(eff_mc_err)

    print(f'Efficiency Data: {eff_Data:.3f}')
    print(f'Efficiency MC: {eff_mc:.3f}')
    print(f'Data/MC: {eff_Data/eff_mc:.3f}')

    correction = abs(eff_Data/eff_mc - 1) + 1
    corr_dict[cat] = { 'total' : correction, 'sys' : eff_Data/eff_mc * np.sqrt((eff_Data_err/eff_Data)**2 + (eff_mc_err/eff_mc)**2), 'corregree': f'{cat}{args.year}'} 

    if not args.make_plots: continue
    # draw histograms
    for obs in observables:
        settings = observables[obs]
        h_Data = rdf_sData.Histo1D(('h_Data', 'h_Data', len(settings['bins'])-1 ,settings['bins']), obs, data_weight).GetValue()
        #h_mc  = rdf_mc.Define('total_w', 'norm_factor*weight').Histo1D(('h_mc', 'h_mc', 30, 0, 30), 'tau_Lxy_sign_BS', 'total_w').GetValue()
        h_mc   = rdf_mc.Histo1D(('h_mc', 'h_mc', len(settings['bins'])-1, settings['bins']), obs, mc_weight).GetValue()

        # normalize to bin width
        for h in [h_Data, h_mc]:
            for i in range(1, h.GetNbinsX()+1):
                bin_width = h.GetBinWidth(i)
                bin_content = h.GetBinContent(i)
                bin_error = h.GetBinError(i)
                if bin_width > 0:
                    h.SetBinContent(i, bin_content / bin_width)
                    h.SetBinError(i, bin_error / bin_width)
            h.Sumw2()

        c = ROOT.TCanvas('c', 'c', 800, 600)
        h_Data.SetMarkerStyle(20)
        h_Data.SetMarkerColor(ROOT.kBlack)
        h_Data.SetLineColor(ROOT.kBlack)
        h_Data.SetLineWidth(2)
        h_Data.SetTitle('')
        
        h_mc.SetFillColor(ROOT.kBlue)
        h_mc.SetFillStyle(3004)
        h_mc.SetLineColor(ROOT.kBlue)
        h_mc.SetLineWidth(2)
        h_mc.GetXaxis().SetTitle(settings['x_title'])
        h_mc.GetYaxis().SetTitle('Events')

        leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.85)
        leg.AddEntry(h_Data, 'sWeighted data', 'lep')
        leg.AddEntry(h_mc, 'D_{s}#rightarrow #phi(#mu#mu)#pi MC', 'f')
        leg.SetBorderSize(0)

        text = ROOT.TLatex(0.20, 0.8, f'CAT {cat} - 20{args.year}')
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextFont(42)


        name = f'{args.output}/LxyS_sPlot_{cat}20{args.year}-{obs}'

        pt.ratio_plot_CMSstyle(
            histo_num = [h_Data],
            draw_opt_num = 'PE',
            histo_den = h_mc,
            draw_opt_den = 'HISTE',
            isMC = False, year = '20'+args.year,
            CMSadditionalText = 'CAT ' + cat,
            y_lim = [0., 1.5*max(h_Data.GetMaximum(), h_mc.GetMaximum())],
            to_ploton = [leg],
            file_name = name,
            ratio_w = 1.0,
        )
        
# save the efficiencies in a json file
with open(f'test/LxyS_efficiency_20{args.year}.json', 'w') as f:
    json.dump(corr_dict, f)
print(f'[o] json file with efficiencies saved as LxyS_efficiency_20{args.year}.json')
print(corr_dict)
if not args.make_plots: sys.exit(0)

h_mc_eff = ROOT.TH1F('h_mc_eff', 'h_mc_eff', 3, -0.5, 3.5)
h_data_eff = ROOT.TH1F('h_data_eff', 'h_data_eff', 3, -0.5, 3.5)
h_ratio = ROOT.TH1F('h_ratio', 'h_ratio', 3, -0.5, 3.5)
for i, cat in enumerate(categories):
    h_mc_eff.SetBinContent(i+1, eff_mc_list[i])
    h_mc_eff.SetBinError(i+1, eff_error_mc_list[i])
    h_mc_eff.Sumw2()
    h_data_eff.SetBinContent(i+1, eff_data_list[i])
    h_data_eff.SetBinError(i+1, eff_error_data_list[i])
    h_data_eff.Sumw2()

h_mc_eff.SetTitle('L_{xy}/#sigma > 2.0'+ f' - 20{args.year}')
h_mc_eff.GetXaxis().SetTitle('')
h_mc_eff.GetYaxis().SetTitle('Efficiency')
h_mc_eff.GetYaxis().SetRangeUser(0.7, 1.1)
h_mc_eff.GetYaxis().SetLabelSize(0.05)
h_mc_eff.GetYaxis().SetTitleSize(0.05)
h_mc_eff.SetMarkerStyle(20)
h_mc_eff.SetMarkerSize(1.2)
h_mc_eff.SetMarkerColor(ROOT.kBlue)
h_mc_eff.SetLineColor(ROOT.kBlue)
h_mc_eff.SetLineWidth(2)
h_mc_eff.Draw('pe')
h_data_eff.SetMarkerStyle(20)
h_data_eff.SetMarkerSize(1.2)
h_data_eff.SetMarkerColor(ROOT.kBlack)
h_data_eff.SetLineColor(ROOT.kBlack)
h_data_eff.SetLineWidth(2)
h_data_eff.Draw('pe same')
leg = ROOT.TLegend(0.6, 0.70, 0.9, 0.85)
leg.SetBorderSize(0)
leg.AddEntry(h_data_eff, 'Data', 'lep')
leg.AddEntry(h_mc_eff, 'D_{s}#rightarrow #phi(#mu#mu)#pi MC', 'lep')
leg.Draw()

name = f'{args.output}/LxyS_efficiency_20{args.year}'
pt.ratio_plot_CMSstyle(
            histo_num = [h_data_eff],
            draw_opt_num = 'PE',
            histo_den = h_mc_eff,
            draw_opt_den = 'PE',
            isMC = False, year = '20'+args.year,
            y_lim = [0.5, 1.2],
            to_ploton = [leg],
            file_name = name,
            ratio_w = 0.2,
        )

