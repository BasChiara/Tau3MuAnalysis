import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
import style.color_text as ct

def style_plot(h, color, marker=20):

    h.Sumw2()
    h.Scale(1./h.Integral())
    h.SetLineColor(color)
    h.SetLineWidth(2)
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(1.5)
    h.SetMarkerColor(color)
    h.GetYaxis().SetRangeUser(0., 1.0)
    h.GetXaxis().SetLabelSize(0.07)
    h.GetYaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.0)

year = '2022EE'

decay_modes = {
    0 : '',
    1 : 'e#nu_{e}#nu_{#tau}',
    2 : '#mu#nu_{#mu}#nu_{#tau}',
    3 : 'hadrons',
    4 : ''
}
branching_ratios = {
    0 : 1.0,
    1 : 0.1780,
    2 : 0.1740,
    3 : 0.6480,
    4 : 1.0
}
bdt_cut = 0.980

rdf = ROOT.RDataFrame('WTau3Mu_tree', config.mc_samples['ZTau3Mu'][1]).Filter(config.year_selection[year])
rdf_postBDT = ROOT.RDataFrame('tree_w_BDT', config.mc_bdt_samples['ZTau3Mu']).Filter(config.year_selection[year] + f' && bdt_score > {bdt_cut}')
print(f'N entries = {rdf.Count().GetValue()}')
# plot the decay modes
h_decayTau = rdf.Histo1D((f'h_decayTau_{year}', f'GEN-LEVEL: opposite #tau decay modes - {year}', 5, 0, 5 ), 'opposite_side_tag').GetValue()
h_decayTau_bdt = rdf_postBDT.Histo1D((f'h_decayTau_{year}_bdt', f'GEN-LEVEL: opposite #tau decay modes - {year}', 5, 0, 5 ), 'opposite_side_tag').GetValue()
for i in range(h_decayTau.GetNbinsX()):
    h_decayTau.GetXaxis().SetBinLabel(i+1, decay_modes[i])
    h_decayTau_bdt.GetXaxis().SetBinLabel(i+1, decay_modes[i])

style_plot(h_decayTau, ROOT.kBlue)
style_plot(h_decayTau_bdt, ROOT.kRed, marker=24)
h_decayTau.GetYaxis().SetTitle('Events')
legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.85)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.AddEntry(h_decayTau, 'preselection', 'p')
legend.AddEntry(h_decayTau_bdt, f'BDT > {bdt_cut}', 'p')

c = ROOT.TCanvas('c', 'c', 800, 600)
h_decayTau.Draw()
h_decayTau_bdt.Draw('same')
legend.Draw()
c.SetGrid()
c.SaveAs(f'decayTau_{year}.png')
c.SaveAs(f'decayTau_{year}.pdf')

# normalize to the branching ratio
h_decayTau_norm = h_decayTau.Clone()
[ h_decayTau_norm.SetBinContent(i+1, h_decayTau.GetBinContent(i+1)/branching_ratios[i]) for i in range(h_decayTau_norm.GetNbinsX()) ]
h_decayTau_bdt_norm = h_decayTau_bdt.Clone()
[ h_decayTau_bdt_norm.SetBinContent(i+1, h_decayTau_bdt.GetBinContent(i+1)/branching_ratios[i]) for i in range(h_decayTau_bdt_norm.GetNbinsX()) ]

c_norm = ROOT.TCanvas('c_norm', 'c_norm', 800, 600)
#style_plot(h_decayTau_norm, ROOT.kBlue)
#style_plot(h_decayTau_bdt_norm, ROOT.kRed, marker=24)
h_decayTau_norm.GetYaxis().SetTitle('Events/Br(#tau decay)')

h_decayTau_norm.GetYaxis().SetRangeUser(0.5,2.0)
h_decayTau_norm.Draw()
h_decayTau_bdt_norm.Draw('same')
legend.Draw()
c_norm.SetGrid()
c_norm.SaveAs(f'decayTau_{year}_presel_norm.png')
c_norm.SaveAs(f'decayTau_{year}_presel_norm.pdf')





