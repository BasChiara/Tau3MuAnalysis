import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import plots.plotting_tools as plotting_tools

def style_hist(h, color, marker = 20, norm = False):
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(1.2)
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle("p_{T} (GeV)")
    h.GetYaxis().SetTitle("1/N dN/dp_{T} (1/GeV)")
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.04)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.04)
    h.GetXaxis().SetTitleOffset(1.2)
    if(norm) :
        h.Scale(1, "width")
        h.Scale(1./h.Integral())

infile = ROOT.TFile("ZvsW_pT.root")
h_Zll_data = infile.Get("h_Zll_data")
h_Zll_data.SetDirectory(0)
h_Zll_Run2 = infile.Get("h_Zll_Run2")
h_Zll_Run2.SetDirectory(0)
h_Zll_Run3 = infile.Get("h_Zll_Run3")
h_Zll_Run3.SetDirectory(0)
h_Wlnu_Run3 = infile.Get("h_Wlnu_Run3")
h_Wlnu_Run3.SetDirectory(0)
infile.Close()

infile_prova = ROOT.TFile("/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/GenLevel_analyzer.root")
h_Zll_Run2_skimmed = infile_prova.Get("h_V_pT")
h_Zll_Run2_skimmed.SetDirectory(0)
infile_prova.Close()

# style the histograms
style_hist(h_Zll_data, ROOT.kBlack, 20, norm=False)
h_Zll_data.Scale(1./h_Zll_data.Integral())
style_hist(h_Zll_Run2, ROOT.kRed, 20, norm=True)
style_hist(h_Zll_Run3, ROOT.kBlue, 20, norm=True)
style_hist(h_Wlnu_Run3, ROOT.kGreen+3, 20, norm=True)

style_hist(h_Zll_Run2_skimmed, ROOT.kViolet+2, 20, norm=True)

# TLegend
legend = ROOT.TLegend(0.50, 0.65, 0.85, 0.85)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

# plot  Z->ll data VS MC NLO @ 13 TeV
legend.AddEntry(h_Zll_data, "Z->ll data", "lep")
legend.AddEntry(h_Zll_Run2, "Z->ll NLO @ 13 TeV", "lep")
plotting_tools.ratio_plot(
    histo_num=[h_Zll_Run2],
    histo_den=h_Zll_data,
    x_lim=[1., 150],
    ratio_w = 0.5,
    ratio_yname = "aMC@NLO/Data",
    draw_opt_num="E1",
    draw_opt_den="E1",
    to_ploton=[legend],
    log_x=True,
    file_name="Zll_dataVSmcNLO_Run2",
)
legend.Clear()

# plot Z->ll MC NLO @ 13 TeV skimmed VS inclusive
legend.AddEntry(h_Zll_Run2, "Z->ll inclusive", "lep")
legend.AddEntry(h_Zll_Run2_skimmed, "Z->ll skimmed", "lep")
plotting_tools.ratio_plot(
    histo_num=[h_Zll_Run2_skimmed],
    histo_den=h_Zll_Run2,
    x_lim=[1., 150],
    ratio_w = 0.2,
    ratio_yname = "skim./incl.",
    draw_opt_num="E1",
    draw_opt_den="E1",
    to_ploton=[legend],
    log_x=True,
    file_name="ZllmcNLO_Run2_skimmedVSinclusive",
)
legend.Clear()
# plot Z->ll MC NLO @ 13 TeV VS 13.6 TeV
legend.AddEntry(h_Zll_Run2, "Z->ll NLO @ 13 TeV", "lep")
legend.AddEntry(h_Zll_Run3, "Z->ll NLO @ 13.6 TeV", "lep")
plotting_tools.ratio_plot(
    histo_num=[h_Zll_Run3],
    histo_den=h_Zll_Run2,
    ratio_w = 0.5,
    ratio_yname = "Run3/Run2",
    x_lim=[1., 150],
    draw_opt_num="E1",
    draw_opt_den="E1",
    to_ploton=[legend],
    log_x=True,
    file_name="ZllmcNLO_Run2vsRun3",
)
legend.Clear()
# plot 13.6 TeV Z->ll VS W->l nu
legend.AddEntry(h_Zll_Run3, "Z->ll NLO @ 13.6 TeV", "lep")
legend.AddEntry(h_Wlnu_Run3, "W->l#nu NLO @ 13.6 TeV", "lep")
plotting_tools.ratio_plot(
    histo_num=[h_Zll_Run3, h_Wlnu_Run3],
    histo_den=h_Zll_Run3,
    ratio_w = 1.0,
    ratio_yname = "Zll/Wl#nu",
    x_lim=[1., 150],
    draw_opt_num="E1",
    draw_opt_den="E1",
    to_ploton=[legend],
    log_x=True,
    file_name="ZllvsWlnu_nloRun3",
)
legend.Clear()