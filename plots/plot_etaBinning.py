import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config


base_path = os.path.abspath(__file__)

infile = "/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/categ_number/input_combine/etaBinning_TTree_bdt0.9900_WTau3Mu_22_splitX2.root"
if not os.path.isfile(infile):
    print(f"Error: file {infile} not found")
    exit(1)
tag = "splitX2"
#"../models/workspaces/etaBinning_TTree_bdt0.9000_WTau3Mu_22_prova.root"
outplot_dir = "/eos/user/c/cbasile/www/Tau3Mu_Run3/categorization/optimize_eta/cat_number/"
tree = "sensitivity_tree"
rdf = ROOT.RDataFrame(tree, infile)
if rdf is None:
    print(f"Error: cannot open file {infile}")
    sys.exit(1)
else:
    print(f"Opened file {infile} rdf entries: {rdf.Count().GetValue()}")
#df_columns      = ['bdt_cut', 'eta_lo', 'eta_hi', 'cat', 'sig_Nexp', 'sig_eff', 'sig_width', 'sig_width_err', 'bkg_Nexp', 'bkg_Nexp_Sregion', 'bkg_eff', 'PunziS_val', 'PunziS_err', 'AMS_val']
rdf = rdf.Define("SsqrtB", "sig_Nexp/sqrt(bkg_Nexp_Sregion)")
rdf = rdf.Define("SsqrtB_err", "0.5*SsqrtB*sqrt(1/sig_Nexp + 1/(4*bkg_Nexp_Sregion))")
# define central eta binning
rdf = rdf.Define("eta", "0.5*(eta_lo + eta_hi)")
eta_low = rdf.Min("eta_lo").GetValue()
eta_high = rdf.Max("eta_hi").GetValue()
rdf = rdf.Define("eta_err", "0.5*(eta_hi - eta_lo)")
rdf = rdf.Define("y_err", "0")
rdf = rdf.Define("sig_eff_err", "0")
rdf = rdf.Define("bkg_Nexp_Sregion_err", "0.5*sqrt(bkg_Nexp_Sregion)")

# plot vars vs eta
var_list = ['sig_width', 'sig_eff', 'SsqrtB', 'bkg_Nexp_Sregion']
label_var = {'sig_width': '#sigma_{S} (GeV)', 'sig_eff': '#varepsilon_{S}', 'SsqrtB': 'S/#sqrt{B}', 'bkg_Nexp_Sregion': 'N_{B} in signal region'}

for var in var_list:
    #profile = rdf.Profile1D((f'prof_etaVS{var}', f'|#eta| - {var}', rdf.Count().GetValue(), eta_low, eta_high), "eta", var)
    profile = rdf.GraphAsymmErrors("eta", var, "eta_err", "eta_err", "y_err", "y_err")
    #profile = rdf.Graph("eta", var)
    h = profile.GetValue()
    h.SetTitle("")
    h.GetXaxis().SetTitle("|#eta|")
    h.GetYaxis().SetTitle(label_var[var])
    h.SetMarkerStyle(20)
    h.SetMarkerSize(1)
    h.SetMarkerColor(ROOT.kBlue)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleSize(0.07)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(1.0)
    max_y = 1.2*rdf.Max(var).GetValue()
    min_y = 0.8*rdf.Min(var).GetValue()
    h.GetYaxis().SetRangeUser(min_y, max_y)
    # draw vertical line to mark categories
    lineAB = ROOT.TLine(config.eta_thAB, min_y, config.eta_thAB, max_y)
    lineBC = ROOT.TLine(config.eta_thBC, min_y, config.eta_thBC, max_y)
    lineAB.SetLineColor(ROOT.kRed)
    lineBC.SetLineColor(ROOT.kRed)
    lineAB.SetLineWidth(2)
    lineBC.SetLineWidth(2)
    # write cat label
    textA = ROOT.TLatex(config.eta_thAB/2., 0.9*max_y, "A")
    textB = ROOT.TLatex(config.eta_thAB + (config.eta_thBC-config.eta_thAB)/2., 0.9*max_y, "B")
    textC = ROOT.TLatex(config.eta_thBC + (eta_high-config.eta_thBC)/2., 0.9*max_y, "C")
    textA.SetTextSize(0.1)
    textB.SetTextSize(0.1)
    textC.SetTextSize(0.1)
    textA.SetTextColor(ROOT.kRed)
    textB.SetTextColor(ROOT.kRed)
    textC.SetTextColor(ROOT.kRed)
    
    
    
    c = ROOT.TCanvas("c_"+var, var, 800, 600)
    c.SetGrid()
    ROOT.gPad.SetLeftMargin(0.15)
    h.Draw("AP")
    lineAB.Draw("same")
    lineBC.Draw("same")
    textA.Draw("same")
    textB.Draw("same")
    textC.Draw("same")
    c.Update()
    c.SaveAs(outplot_dir+ var+ "_vs_eta_"+tag+".png")
    c.SaveAs(outplot_dir+ var+ "_vs_eta_"+tag+".pdf")