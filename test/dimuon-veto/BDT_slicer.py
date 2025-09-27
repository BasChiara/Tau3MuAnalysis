import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
import mva.config as config
import plots.plotting_tools as plt

signal = config.mc_bdt_samples['WTau3Mu']
data   = config.data_bdt_samples['WTau3Mu']


sig_rdf = ROOT.RDataFrame("tree_w_BDT", signal).Filter(config.base_selection)
data_rdf = ROOT.RDataFrame("tree_w_BDT", data).Filter('&'.join([config.base_selection, config.sidebands_selection]))
if sig_rdf.Count().GetValue() == 0 or data_rdf.Count().GetValue() == 0:
    print("No events found after selection")
    sys.exit(0)

BDT_th = [0.0, 0.985, 0.990, 0.995]
n_slices = len(BDT_th)
vars = ['tau_mu12_fitM', 'tau_mu13_fitM', 'tau_mu23_fitM']
min_val, max_val, n_bins = 0.4, 1.4, 90

for bdt in BDT_th:
    for var in vars:
        label = config.features_NbinsXloXhiLabelLog[var][3]
        bin_w = (max_val - min_val) / n_bins * 1000 # in MeV
        h_data = data_rdf.Filter(f"bdt_score > {bdt}").Histo1D(("h_data", f";{label}(GeV);Events/{bin_w:.0f}MeV", n_bins, min_val, max_val), var).GetValue()
        h_sig  = sig_rdf.Filter(f"bdt_score > {bdt}").Histo1D(("h_sig", f";{label}(GeV;Events/{bin_w:.0f}MeV",   n_bins, min_val, max_val), var).GetValue()

        h_data.Scale(1.0 / h_data.Integral())
        h_data.SetMarkerStyle(20)
        h_data.SetMarkerSize(1.0)
        h_data.SetLineColor(ROOT.kBlack)
        h_data.SetLineWidth(2)
        h_data.SetMarkerColor(ROOT.kBlack)
        
        h_sig.Scale(1.0 / h_sig.Integral())
        h_sig.SetLineColor(ROOT.kRed)
        h_sig.SetLineWidth(2)
        h_sig.SetMarkerColor(ROOT.kRed)
        h_sig.SetMarkerStyle(0)
        h_sig.SetMarkerSize(0)

        y_max = 1.4*max(h_data.GetMaximum(), h_sig.GetMaximum())
        text = ROOT.TLatex(min_val + 0.05*(max_val - min_val), 0.85*y_max, f"BDT > {bdt:.3f}")
        text.SetTextSize(0.04)
        text.SetTextFont(42)
        text.SetTextAlign(11)

        legend = ROOT.TLegend(0.60, 0.70, 0.85, 0.85)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(h_data, "Data (sidebands)", "PE")
        legend.AddEntry(h_sig,  "MC (WTau3Mu)", "L")

        plt.ratio_plot([h_data], h_sig,
                    file_name=f"BDT_slice_{bdt}_{var}",
                    title=f"BDT score > {bdt}",
                    ratio_w = 8 if bdt > 0.5 else 2.0,
                    draw_opt_num = "PE",
                    draw_opt_den = "HIST",
                    y_lim = (0, y_max),
                    to_ploton=[text, legend]
        )
    