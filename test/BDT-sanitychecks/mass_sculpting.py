import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
import numpy as np

import cmsstyle as CMS
CMS.setCMSStyle()
cmsStyle = CMS.getCMSStyle()
cmsStyle.SetErrorX(0)
CMS.SetEnergy(13.6)
CMS.SetLumi('')

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config

def get_bdt_efficiency(tree, selection='(1)', BDT_cut=0.990):

    bdt_selection = '||'.join([
        f'({config.cat_eta_selection_dict_fit["A"]}) && (bdt_score > {BDT_cut})',
        f'({config.cat_eta_selection_dict_fit["B"]}) && (bdt_score > {BDT_cut})',
        f'({config.cat_eta_selection_dict_fit["C"]}) && (bdt_score > {BDT_cut})',
    ])
    bdt_selection = f'({bdt_selection}) && ({selection})'
    #print(f"Selection: {selection}")
    print(f"BDT Selection: {bdt_selection}")
    n_total    = tree.GetEntries(selection)
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
output_dir = os.path.expandvars('$WWW/Tau3Mu_Run3/BDTtraining/validations/')

sel = '&&'.join([config.base_selection, config.phi_veto, config.year_selection['2022preEE']])
BDTcut = 0.990
results = {}
for m in mc_files:
    file_path = mc_files[m]
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping.")
        continue
    
    tree = ROOT.TChain("tree_w_BDT")
    tree.Add(file_path)
    print(f" [i] processing {m} with {tree.GetEntries()} entries")
    efficiency, error = get_bdt_efficiency(tree, selection=sel, BDT_cut=BDTcut)
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
        #stack.Add(hist)
        legend.AddEntry(hist, get_legend_entry(m), "l")


# plot the results
graph = ROOT.TGraphErrors(len(results))
#graph.SetTitle("BDT Efficiency vs Mass")
graph.GetXaxis().SetTitle("simulated #tau mass (GeV)")
graph.GetYaxis().SetTitle("Efficiency")
i = 0
iref = 2
for m, res in results.items():
    mass = float(m.replace("M", ""))/1000.0  # Convert to GeV
    graph.SetPoint(i, mass, res["efficiency"])
    graph.SetPointError(i, 0, res["error"])
    i += 1
# add horizontal line at 1, 3, and 5 sigma levels based on M1777
line1_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 1 * results['M1777']['error'], color=ROOT.kGreen)
line1_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 1 * results['M1777']['error'], color=ROOT.kGreen)
line3_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 3 * results['M1777']['error'], color=ROOT.kBlue)
line3_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 3 * results['M1777']['error'], color=ROOT.kBlue)
line5_p = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] + 5 * results['M1777']['error'], color=ROOT.kRed)
line5_m = get_hline(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax(), results['M1777']['efficiency'] - 5 * results['M1777']['error'], color=ROOT.kRed)
# plot with cmsstyle
canvas = CMS.cmsCanvas("c",
                        x_min=1.6, x_max=2.0,
                        y_min=0.45, y_max=0.60,
                        nameXaxis="simulated #tau mass (GeV)",
                        nameYaxis=f"efficiency BDT score > {BDTcut}",
                        square=False,
                        extraSpace=0.15,
                        yTitOffset=1.2,
                        )
# add horizontal lines
CMS.cmsDrawLine(line1_p, lcolor=ROOT.kGreen+1,  lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDrawLine(line1_m, lcolor=ROOT.kGreen+1,  lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDrawLine(line3_p, lcolor=ROOT.kBlue,     lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDrawLine(line3_m, lcolor=ROOT.kBlue,     lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDrawLine(line5_p, lcolor=ROOT.kRed,      lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDrawLine(line5_m, lcolor=ROOT.kRed,      lstyle=ROOT.kDashed, lwidth=2)
CMS.cmsDraw(
    graph,
    'P',
    lcolor=ROOT.kBlack,
    marker=20,
    mcolor=ROOT.kBlack,
)

CMS.SaveCanvas(canvas, os.path.join(output_dir, "bdt_efficiency_vs_mass.png"), False)
CMS.SaveCanvas(canvas, os.path.join(output_dir, "bdt_efficiency_vs_mass.pdf"), False)




