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

year = '2022EE'

decay_modes = {
    0 : '',
    1 : 'e#nu_{e}#nu_{#tau}',
    2 : '#mu#nu_{#mu}#nu_{#tau}',
    3 : 'hadrons',
    4 : ''
}

rdf = ROOT.RDataFrame('WTau3Mu_tree', config.mc_samples['ZTau3Mu'][1]).Filter(config.year_selection[year])
rdf_postBDT = ROOT.RDataFrame('tree_w_BDT', config.mc_bdt_samples['ZTau3Mu']).Filter(config.year_selection[year])
print(f'N entries = {rdf.Count().GetValue()}')
# plot the decay modes
h_decayTau = rdf.Histo1D((f'h_decayTau_{year}', f'opposite #tau decay modes - {year}', 5, 0, 5 ), 'opposite_side_tag').GetValue()
h_decayTau_bdt = rdf_postBDT.Histo1D((f'h_decayTau_{year}_bdt', f'opposite #tau decay modes - {year}', 5, 0, 5 ), 'opposite_side_tag').GetValue()
for i in range(h_decayTau.GetNbinsX()):
    h_decayTau.GetXaxis().SetBinLabel(i+1, decay_modes[i])
    h_decayTau_bdt.GetXaxis().SetBinLabel(i+1, decay_modes[i])

style_plot(h_decayTau, ROOT.kBlue)
style_plot(h_decayTau_bdt, ROOT.kRed, marker=24)
legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.85)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.AddEntry(h_decayTau, 'preselection', 'p')
legend.AddEntry(h_decayTau_bdt, 'post-BDT', 'p')
c = ROOT.TCanvas('c', 'c', 800, 600)
h_decayTau.Draw()
h_decayTau_bdt.Draw('same')
legend.Draw()
c.SetGrid()
c.SaveAs(f'decayTau_{year}.png')
c.SaveAs(f'decayTau_{year}.pdf')




