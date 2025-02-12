import ROOT
import argparse
import pickle
import os
import numpy  as np
import pandas as pd

# from my config
import config as cfg

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def style_hist(h, x_title, color, fillstyle = 3004):
    h.GetXaxis().SetTitle(x_title)
    h.SetLineColor(color)
    h.SetLineWidth(3)
    h.SetFillColor(color)
    h.SetFillStyle(fillstyle)

    return h


def reweight_by(h_to_reweight, h_ref, name = '', debug = False):

    h_to_reweight.Sumw2()
    h_ref.Sumw2()

    h_weights = h_to_reweight.Clone(f'h_weights_{name}')
    h_weights.Divide(h_ref)
    h_weights.SetDirectory(0)

    if debug :[print(f'bin {i}: {h_weights.GetBinContent(i)}') for i in range(1, h_weights.GetNbinsX() + 1)]
    set_of_weights = [[ [h_weights.GetBinLowEdge(i), h_weights.GetBinLowEdge(i+1)], h_weights.GetBinContent(i)] for i in range(1, h_weights.GetNbinsX() + 1)]
    
    return set_of_weights

def apply_reweighting(set_of_weights, dataset_to_reweight, variable, name = '', debug = False):
    
    # add a new column with the weights for the given variable
    col_name = f'wBy_{variable}'
    dataset = dataset_to_reweight.copy()
    dataset[col_name] = dataset[variable].apply(lambda x: next((w for (bin, w) in set_of_weights if x >= bin[0] and x < bin[1]), 0))

    # merge the weights for all the variables used for reweighting
    w_columns = [col for col in dataset.columns if 'wBy' in col]
    print(f'[i] reweighting by {variable} - columns: {w_columns}')
    dataset['weight_to_data'] = dataset[w_columns].prod(axis = 1)
    
    # test the reweighting
    if debug :
        [print(f' iso {dataset[variable].iloc[i]:.2f} - weight {dataset[col_name].iloc[i]:.2f}') for i in range(1, 10)]
    
    return dataset


# ------------ APPLY SELECTIONS ------------ #
base_selection = ' & '.join([
    cfg.base_selection,
    cfg.phi_veto,
    cfg.displacement_selection,
    cfg.sidebands_selection,
])

year = '2022'

# ------------ INPUT/OUTPUT ------------ # 
plot_outdir = '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/features'
if not os.path.isdir(plot_outdir):
    os.makedirs(plot_outdir)
    os.system(f'cp ~/public/index.php {plot_outdir}')
    print(f'[i] created directory for output plots : {plot_outdir}')
else:
    print(f'[i] already existing directory for output plots : {plot_outdir}')

data_file = cfg.data_bdt_samples['WTau3Mu']
#invID_file = "/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/XGBout_data_DATA2022Cv1_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root" #cfg.data_bdt_samples['invMedID']
invID_file = "/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/XGBout_data_DATA2022Cv1_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16_rew_by_tau_fit_eta.root" #cfg.data_bdt_samples['invMedID']

# create root dataframes with the data
data_rdf = ROOT.RDataFrame("tree_w_BDT", data_file)
data_rdf = data_rdf.Filter(base_selection).Define("tri_muonID", "tau_mu1_MediumID + tau_mu2_MediumID + tau_mu3_MediumID") if not data_rdf.HasColumn('tri_muonID') else data_rdf.Filter(base_selection)
print(f'[i] data file: {data_file} - entries: {data_rdf.Count().GetValue()}')
invID_rdf = ROOT.RDataFrame("tree_w_BDT", invID_file)
invID_rdf = invID_rdf.Filter(base_selection)
# inevrt muon ID for only 1 muon
if not invID_rdf.HasColumn('tri_muonID') : invID_rdf = invID_rdf.Define("tri_muonID", "tau_mu1_MediumID + tau_mu2_MediumID + tau_mu3_MediumID")
invID_rdf = invID_rdf.Filter("tri_muonID > 1")
# add weight to data column
if not invID_rdf.HasColumn('tri_muonID') : invID_rdf = invID_rdf.Define("weight_to_data", "1")

print(f'[i] invID file: {invID_file} - entries: {invID_rdf.Count().GetValue()}')


# ------------ REWEIGHTING ------------ #
#var_for_reweight = 'tau_fit_eta'
var_for_reweight = 'tau_relIso'
to_save_reweight = True
binning = cfg.features_NbinsXloXhiLabelLog[var_for_reweight]
h_data = data_rdf.Histo1D(
       (f'h_data_{var_for_reweight}', 
        '', 
        binning[0], 
        binning[1], 
        binning[2]
        ), 
        var_for_reweight
    ).GetPtr()
h_data.Scale(1./h_data.Integral())
h_invID = invID_rdf.Histo1D(
         (f'h_data_{var_for_reweight}', 
          '', 
          binning[0], 
          binning[1], 
          binning[2]
          ), 
          var_for_reweight,
          'weight_to_data'
        ).GetPtr()
h_invID.Scale(1./h_invID.Integral())
set_of_weights = reweight_by( h_data, h_invID, name = var_for_reweight)

# apply reweighting and save the reweighted tree
invID_pdf = pd.DataFrame(invID_rdf.AsNumpy())
invID_pdf = apply_reweighting(set_of_weights, invID_pdf, var_for_reweight, name = var_for_reweight)
#invID_pdf.loc[:, 'weight_to_data'] = invID_pdf['wBy_tau_fit_eta'].values * invID_pdf['wBy_tau_relIso'].values
rew_invID_rdf = ROOT.RDF.MakeNumpyDataFrame({col: invID_pdf[col].values for col in invID_pdf.columns})
if to_save_reweight:
    rew_invID_rdf.Snapshot('tree_w_BDT', f'{invID_file.replace(".root", f"_rew_by_{var_for_reweight}.root")}')
    print(f'[i] reweighted file saved as {invID_file.replace(".root", f"_rew_by_{var_for_reweight}.root")}')


##             ##
#    PLOTTING   #
##             ##
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.035)

observables = cfg.features + ['tri_muonID', 'tau_fit_eta', 'tauEta', 'bdt_score', 'tau_fit_mass', 'tau_mu12_fitM', 'tau_mu23_fitM', 'tau_mu13_fitM']
#observables = ['tau_fit_eta', 'tauEta', 'bdt_score', 'tau_relIso']
legend = ROOT.TLegend(0.55, 0.70, 0.85, 0.85)
legend_cut = ROOT.TLegend(0.40, 0.75, 0.85, 0.85)

kolmogorov_test = {}
Chi2Test = {}

for obs in observables:
    print(f'[i] plotting {obs}')
    c = ROOT.TCanvas(f'c_{obs}', '', 800,800)
    binning = cfg.features_NbinsXloXhiLabelLog[obs]

    h_data = data_rdf.Histo1D(
       ('h_data_%s'%obs, 
        '', 
        binning[0], 
        binning[1], 
        binning[2]
        ), 
        obs
    ).GetPtr()
    h_data.Scale(1./h_data.Integral())

    h_invID = invID_rdf.Histo1D(
       ('h_invID_%s'%obs, 
        '', 
        binning[0], 
        binning[1], 
        binning[2]
        ), 
        obs
    ).GetPtr()
    h_invID.Scale(1./h_invID.Integral())

    h_w_invID = rew_invID_rdf.Histo1D(
         ('h_w_invID_%s'%obs, 
          '', 
          binning[0], 
          binning[1], 
          binning[2]
          ), 
          obs, 'weight_to_data'
     ).GetPtr()
    h_w_invID.Scale(1./h_w_invID.Integral())

    # Kolmogorov test
    #kolmogorov_test[obs] = h_data.KolmogorovTest(h_invID, 'UO')
    # Chi2 test
    Chi2Test[obs] = h_data.Chi2Test(h_invID, 'CHI2/NDF UF OF')
    
    
    h_data = style_hist(h_data, binning[3], ROOT.kBlue)
    h_invID = style_hist(h_invID, binning[3], ROOT.kRed)
    h_w_invID = style_hist(h_w_invID, binning[3], ROOT.kGreen)
    h_data.SetMaximum(1.4*max(h_data.GetMaximum(),h_invID.GetMaximum()))

    c.cd()
    legend.AddEntry(h_data, 'data sidebands', 'f')
    legend.AddEntry(h_invID, 'inv. #mu ID', 'f')
    legend.AddEntry(h_w_invID, 'inv. muon ID re-w', 'f')
    h_data.Draw('hist')
    h_invID.Draw('hist same')
    h_w_invID.Draw('hist same')
    legend.Draw()
    c.SetLogy(binning[4])
    c.SaveAs(f'{plot_outdir}/invID_{obs}.png')
    c.SaveAs(f'{plot_outdir}/invID_{obs}.pdf')
    c.Close()
    legend.Clear()

# print Kolmogorov test results
#[print(f'{obs} Kolmogorov test: {kolmogorov_test[obs]}') for obs in observables]
[print(f'{obs} Chi2 test: {Chi2Test[obs]:.1f}') for obs in observables]



