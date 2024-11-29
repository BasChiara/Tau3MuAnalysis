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

def plot_comparison(h_num, h_den, y_name = 'MC/Data', legend_dict = None , ratio_yw = 0.5, outname = 'plot'):
    # TLegend
    legend = ROOT.TLegend(0.50, 0.65, 0.85, 0.85)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(h_num, legend_dict[h_num.GetName()], "lep")
    legend.AddEntry(h_den, legend_dict[h_den.GetName()], "lep")
    plotting_tools.ratio_plot(
        histo_num=[h_num],
        histo_den=h_den,
        x_lim=[0.1, 1500],
        ratio_w = ratio_yw,
        ratio_yname = y_name,
        draw_opt_num="E1",
        draw_opt_den="E1",
        to_ploton=[legend],
        log_x=True,
        file_name=outname,
    )
    del legend


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

infile_prova = ROOT.TFile("/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/GenLevel_analyzer_MiniAODv2.root")
h_Zll_Run2_skimmed = infile_prova.Get("h_V_pT")
h_Zll_Run2_skimmed.SetDirectory(0)
infile_prova.Close()
h_Zll_Run2_skimmed.SetName("h_Zll_Run2_skimmed")

legend_dict = {
    'h_Zll_data' : "Z->ll data",
    'h_Zll_Run2' : "Z->ll NLO @ 13 TeV",
    'h_Zll_Run3' : "Z->ll NLO @ 13.6 TeV",
    'h_Wlnu_Run3' : "W->lnu NLO @ 13.6 TeV",
    'h_Zll_Run2_skimmed' : "Z->ll NLO @ 13 TeV skimmed",
}

# style the histograms
style_hist(h_Zll_data, ROOT.kBlack, 20, norm=False)
h_Zll_data.Scale(1./h_Zll_data.Integral())
style_hist(h_Zll_Run2, ROOT.kRed, 20, norm=True)
style_hist(h_Zll_Run3, ROOT.kBlue, 20, norm=True)
style_hist(h_Wlnu_Run3, ROOT.kGreen+3, 20, norm=True)
style_hist(h_Zll_Run2_skimmed, ROOT.kViolet+2, 20, norm=True)



# plot  Z->ll data VS MC NLO @ 13 TeV
plot_comparison(
    h_num= h_Zll_Run2, 
    h_den = h_Zll_data, 
    y_name = 'aMC@NLO/Data', 
    legend_dict = legend_dict, 
    outname = 'Zll_dataVSmcNLO_Run2'
    )
# plot  Z->ll data VS skimmed MC NLO @ 13 TeV
plot_comparison(
    h_num= h_Zll_Run2_skimmed, 
    h_den = h_Zll_data, 
    y_name = 'aMC@NLO/Data', 
    legend_dict = legend_dict, 
    outname = 'Zll_dataVSmcNLOskmd_Run2'
    )
# plot  Z->ll data VS MC NLO @ 13.6 TeV
plot_comparison(
    h_num= h_Zll_Run3, 
    h_den = h_Zll_data, 
    y_name = 'aMC@NLO/Data', 
    legend_dict = legend_dict, 
    outname = 'Zll_dataVSmcNLO_Run3'
    )
# plot Z->ll MC NLO @ 13 TeV skimmed VS inclusive
plot_comparison(
    h_num= h_Zll_Run2_skimmed, 
    h_den = h_Zll_Run2, 
    y_name = 'skim./incl.', 
    legend_dict = legend_dict, 
    outname = 'ZllmcNLO_Run2_skimmedVSinclusive'
    )
# plot Z->ll MC NLO @ 13 TeV VS 13.6 TeV
plot_comparison(
    h_num= h_Zll_Run3,
    h_den = h_Zll_Run2,
    y_name = 'Run3 / Run2',
    legend_dict = legend_dict,
    outname = 'ZllmcNLO_Run2vsRun3'
    )
# plot 13.6 TeV Z->ll VS W->l nu
plot_comparison(
    h_num= h_Zll_Run3, 
    h_den = h_Wlnu_Run3, 
    y_name = 'Zll/Wl#nu', 
    legend_dict = legend_dict, 
    outname = 'ZllvsWlnu_nloRun3'
    )