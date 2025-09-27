import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kBird)
import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config

def style_histo(histo, title, xlabel, ylabel, color=None, ylim=None):
    histo.SetTitle(title)
    histo.GetXaxis().SetTitle(xlabel)
    histo.GetYaxis().SetTitle(ylabel)
    histo.GetXaxis().SetTitleSize(0.045)
    histo.GetYaxis().SetTitleSize(0.045)
    histo.GetXaxis().SetTitleOffset(1.1)
    histo.GetYaxis().SetTitleOffset(1.1)
    histo.SetLineWidth(2)
    histo.SetMarkerStyle(20)
    histo.SetMarkerSize(0.8)
    if ylim: histo.GetYaxis().SetRangeUser(ylim[0], ylim[1])
    if color:
        histo.SetLineColor(color)
        histo.SetMarkerColor(color)
    


year = '2022'
#infile = config.mc_bdt_samples['WTau3Mu']
infile = config.data_bdt_samples['WTau3Mu']
selection = '&'.join([
    config.year_selection[year],
    '(1)'
    ])
rdf = ROOT.RDataFrame("tree_w_BDT", infile).Filter(config.year_selection[year])
plotpath = os.path.expandvars('$WWW/Tau3Mu_Run3/BPH-24-010_review/Lxy-significance')

feature = 'tau_Lxy_sign_BS'
min_feat, max_feat = 2.0, 100.0
nbins_feature = int((max_feat - min_feat) / 0.5)
# BDT correlation
reference = 'bdt_score'
min_ref, max_ref = 0.0, 1.0
nbins = int((max_ref - min_ref) / 0.01)


# --- profile
h2d = rdf.Histo2D((f"hprof_{feature}", "", nbins*2, min_ref, max_ref, nbins_feature, min_feat, max_feat), reference, feature)
style_histo(h2d, f"{feature} vs BDT (data {year})", config.features_NbinsXloXhiLabelLog[reference][3], config.features_NbinsXloXhiLabelLog[feature][3], ylim=None)
profile = rdf.Profile1D(("hprof", "", nbins, min_ref, max_ref, min_feat, max_feat), reference, feature)
style_histo(profile, f"{feature} vs BDT (data {year})", config.features_NbinsXloXhiLabelLog[reference][3], config.features_NbinsXloXhiLabelLog[feature][3], color=ROOT.kBlack, ylim=[0, 30])
# --- draw
c = ROOT.TCanvas("c", "c", 800, 600)
profile.Draw("profcolz")
c.SetGrid()
c.SaveAs(os.path.join(plotpath,f"bdtVS{feature}_{year}_DATA-v2.png") )
c.Clear()
# --- draw 2D histogram
h2d.Draw("COLZ")
c.SetLogz()
c.SetLogy()
c.SaveAs(os.path.join(plotpath, f"bdtVS{feature}_2D_{year}_DATA-v2.png"))

sys.exit(0)
# tau mass correlation
ROOT.gStyle.SetPalette(ROOT.kCMYK)
thresh = np.linspace(2.0, 10.0, 9)
reference = 'tau_fit_mass'
min_ref, max_ref = 1.70, 1.85
nbins = int((max_ref - min_ref) / 0.005)

h_list = []
for i, t in enumerate(thresh):
    print(f"{feature} > {t}")
    h = rdf.Filter(f"{feature} > {t}").Histo1D((f"h_{feature}_vs_{reference}_{i}", "", nbins, min_ref, max_ref), reference, feature)
    h.Scale(1.0 / h.Integral())
    style_histo(h, f"{feature} vs {reference} (signal {year})", config.features_NbinsXloXhiLabelLog[reference][3], f"events", color=i, ylim=None)
    h_list.append(h)
# ratio plots
ratio_list = []
h_reference = h_list[0].Clone("h_reference")
for i, h in enumerate(h_list):
    print(f"Ratio {feature} > {thresh[i]} / {feature} > {thresh[0]}")
    h_ratio = h_list[i].Clone(f"h_ratio_{i}")
    h_ratio.Divide(h_reference)  # Divide by the first histogram
    style_histo(h_ratio, "", config.features_NbinsXloXhiLabelLog[reference][3], "ratio", color=None, ylim=[0.75, 1.25])
    ratio_list.append(h_ratio)
# --- draw
legend = ROOT.TLegend(0.7, 0.3, 0.99, 0.90)


c2 = ROOT.TCanvas("c2", "c2", 800, 1024)
rpad_quota = 0.35
c2.cd()
# upper pad
upper_pad = ROOT.TPad("upper_pad", "upper_pad", 0, rpad_quota, 1, 1)
upper_pad.SetBottomMargin(0.01)
upper_pad.Draw()
upper_pad.cd()
for i, h in enumerate(h_list):
    h.Draw("HIST PLC" + ("SAME" if i > 0 else ""))
    legend.AddEntry(h.GetName(), f"{config.features_NbinsXloXhiLabelLog[feature][3]} > {thresh[i]:.1f}", "l")
legend.Draw("SAME")
c2.cd()
# lower pad
lower_pad = ROOT.TPad("lower_pad", "lower_pad", 0, 0, 1, rpad_quota)
lower_pad.SetTopMargin(0.01)
lower_pad.SetBottomMargin(0.4)
lower_pad.Draw()
lower_pad.cd()
for i, h_ratio in enumerate(ratio_list):
    if i ==0 :
        h_ratio.GetYaxis().SetTitleSize(0.1)
        h_ratio.GetYaxis().SetTitleOffset(1.2)
        h_ratio.GetYaxis().SetLabelSize(0.05)
        h_ratio.GetXaxis().SetTitleSize(0.1)
        h_ratio.GetXaxis().SetTitleOffset(1.2)
        h_ratio.GetXaxis().SetLabelSize(0.05)

    h_ratio.Draw("PLC PMC PFC" + ("SAME" if i > 0 else ""))
lower_pad.SetGrid()
c2.SaveAs(os.path.join(plotpath, f"{feature}_vs_{reference}_{year}.png"))