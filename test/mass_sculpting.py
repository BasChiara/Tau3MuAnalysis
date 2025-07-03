import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
import numpy as np

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mva.config as config

def get_bdt_efficiency(tree, selection='(1)'):

    bdt_selection = '||'.join([
        f'({config.cat_eta_selection_dict_fit["A"]}) && (bdt_score > {config.bdt_cuts_22[0]})',
        f'({config.cat_eta_selection_dict_fit["B"]}) && (bdt_score > {config.bdt_cuts_22[1]})',
        f'({config.cat_eta_selection_dict_fit["C"]}) && (bdt_score > {config.bdt_cuts_22[2]})',
    ])
    bdt_selection = f'({bdt_selection}) && ({selection})'
    print(f"Selection: {selection}")
    print(f"BDT Selection: {bdt_selection}")
    n_total = tree.GetEntries(selection)
    n_selected = tree.GetEntries(bdt_selection)
    efficiency = n_selected / n_total if n_total > 0 else 0.0
    error = np.sqrt(efficiency * (1 - efficiency) / n_total) if n_total > 0 else 0.0
    
    return efficiency, error

def get_histogram(tree, variable, selection='(1)', bins=100, x_min=0, x_max=1):
    hist = ROOT.TH1F(f'h_{variable}', f'{variable} distribution', bins, x_min, x_max)
    tree.Draw(f'{variable}>>h_{variable}', selection, 'goff')
    hist.SetDirectory(0)  # Prevent ROOT from deleting the histogram
    hist.Scale(1.0 / hist.Integral())  # Normalize the histogram
    return hist

def get_hline(x1, x2, y, color=ROOT.kRed):
    hline = ROOT.TLine(x1, y, x2, y)
    hline.SetLineColor(color)
    hline.SetLineStyle(2)
    hline.SetLineWidth(2)
    
    return hline

# some kinematic plots
variables = {
    'bdt_score': (50,0.95, 1),
}
colors = {
    'M1650': ROOT.kBlue,
    'M1700': ROOT.kGreen,
    'M1777': ROOT.kRed,
    'M1850': ROOT.kMagenta,
    'M1900': ROOT.kCyan,
    'M1950': ROOT.kOrange,
}
legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.9)
legend.SetBorderSize(0)

def get_legend_entry(mass):
    return f"MTauX = {mass} GeV"

mc_files = {
    "M1650" : "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1650.root",
    "M1700" : "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1700.root",
    "M1777" : config.mc_bdt_samples['WTau3Mu'],
    "M1850" : "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1850.root",
    "M1900" : "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1900.root",
    "M1950" : "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1950.root",
}

sel = '&&'.join([config.base_selection, config.phi_veto, config.year_selection['2022preEE']])

results = {}
stack = ROOT.THStack("stack", "Kinematic Distributions")
for m in mc_files:
    file_path = mc_files[m]
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping.")
        continue
    
    tree = ROOT.TChain("tree_w_BDT")
    tree.Add(file_path)
    print(f" [i] processing {m} with {tree.GetEntries()} entries")
    efficiency, error = get_bdt_efficiency(tree, selection=sel)
    results[m] = {
        "efficiency": efficiency,
        "error": error
    }
    
    print(f"{m}: Efficiency = {efficiency:.4f}, Error = {error:.4f}\n")

    for var, (bins, x_min, x_max) in variables.items():
        hist = get_histogram(tree, var, selection=sel, bins=bins, x_min=x_min, x_max=x_max)
        hist.SetLineColor(colors[m])
        hist.SetLineWidth(2)
        hist.SetMarkerStyle(20)
        hist.SetMarkerColor(colors[m])
        stack.Add(hist)
        legend.AddEntry(hist, get_legend_entry(m), "l")


# plot the results
graph = ROOT.TGraphErrors(len(results))
graph.SetTitle("BDT Efficiency vs Mass")
graph.GetXaxis().SetTitle("Mass (GeV)")
graph.GetYaxis().SetTitle("Efficiency")
i = 0
iref = 2
for m, res in results.items():
    mass = float(m.replace("M", ""))/1000.0  # Convert to GeV
    graph.SetPoint(i, mass, res["efficiency"])
    graph.SetPointError(i, 0, res["error"])
    i += 1
canvas = ROOT.TCanvas("c", "BDT Efficiency", 800, 600)
graph.SetMarkerStyle(20)
graph.SetMarkerColor(ROOT.kBlack)
graph.SetLineColor(ROOT.kBlack)
graph.Draw("AP")
# add horizontal line at 1, 3, and 5 sigma levels
text = ROOT.TLatex()
text.SetTextSize(0.03)
line1_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 1 * results['M1777']['error'], color=ROOT.kGreen)
line1_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 1 * results['M1777']['error'], color=ROOT.kGreen)
line3_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 3 * results['M1777']['error'], color=ROOT.kBlue)
line3_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 3 * results['M1777']['error'], color=ROOT.kBlue)
line5_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 5 * results['M1777']['error'], color=ROOT.kRed)
line5_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 5 * results['M1777']['error'], color=ROOT.kRed)
line1_p.Draw("SAME")
line1_m.Draw("SAME")
line3_p.Draw("SAME")
line3_m.Draw("SAME")
line5_p.Draw("SAME")
line5_m.Draw("SAME")
graph.Draw("P SAME")
canvas.SetGrid()

canvas.SaveAs("bdt_efficiency_vs_mass.png")

# plot the histograms
canvas_hist = ROOT.TCanvas("c_hist", "Kinematic Distributions", 800, 600)
stack.Draw("nostack hist")
legend.Draw("SAME")
canvas_hist.SetLogy(1)
canvas_hist.SaveAs("kinematic_distributions.png")




