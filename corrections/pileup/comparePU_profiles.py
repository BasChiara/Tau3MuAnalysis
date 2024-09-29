# compare PU profiles in data and MC for different MC samples and eras

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def get_histo(file_name, histo_name):
    file = ROOT.TFile.Open(file_name)
    histo = file.Get(histo_name)
    histo.SetDirectory(0)
    file.Close()
    return histo

# input files
parser = argparse.ArgumentParser(description='Make pileup weights')
parser.add_argument('--era', choices=['2022preEE', '2022EE', '2023preBPix', '2023BPix'], default='2022preEE', help='era to be used')
args = parser.parse_args()

era = args.era
# general output settings
out_dir = 'pileup_histograms'
# data file [central pileupcalc]
histo_name_data = 'pileup'
out_file_data = f'{out_dir}/pileupDATA_{era}.root'
# mc files
histo_name_mc = 'h_mc_PU'
out_file_mc   = {
    'central_69p2mb' : f'{out_dir}/pileupMC_central_MinBxsec69p2mb_{era}.root',
    'central_80mb' : f'{out_dir}/pileupMC_central_MinBxsec80mb_{era}.root',
    'miniAOD' : f'{out_dir}/pileupMC_miniAOD_{era}.root',
    'nanoAOD' : f'{out_dir}/pileupMC_nanoAOD_{era}.root',
}

# PU bins
n_pu_bins = 100
pu_lo, pu_hi = 0, 100

# ------- MC PILEUP ------- #
# central configuration
h_central_mc = get_histo(out_file_mc['central_69p2mb'], histo_name_mc) 
h_central_mc.Scale(1./h_central_mc.Integral())
h_central_mc.SetLineColor(ROOT.kBlack)
h_central_mc.SetLineWidth(2)
h_central_mc.SetTitle(f'MC pileup profile - {era}')
h_central_mc.GetXaxis().SetTitle('n True Interactions')
# --
h_central_mc_80mb = get_histo(out_file_mc['central_80mb'], histo_name_mc) 
h_central_mc_80mb.Scale(1./h_central_mc.Integral())
h_central_mc_80mb.SetLineColor(ROOT.kBlack)
h_central_mc_80mb.SetLineStyle(ROOT.kDashed)
h_central_mc_80mb.SetLineWidth(2)
# miniAOD 
h_miniAOD_mc = get_histo(out_file_mc['miniAOD'], histo_name_mc) 
h_miniAOD_mc.Scale(1./h_miniAOD_mc.Integral())
h_miniAOD_mc.SetLineColor(ROOT.kRed)
h_miniAOD_mc.SetLineWidth(2)
h_miniAOD_mc.SetTitle(f'MC pileup profile - {era}')
h_miniAOD_mc.GetXaxis().SetTitle('n True Interactions')
# nanoAOD
h_nanoAOD_mc = get_histo(out_file_mc['nanoAOD'], histo_name_mc)
h_nanoAOD_mc.Scale(1./h_nanoAOD_mc.Integral())
h_nanoAOD_mc.SetLineColor(ROOT.kBlue)
h_nanoAOD_mc.SetLineWidth(2)
h_nanoAOD_mc.SetTitle(f'MC pileup profile - {era}')
h_nanoAOD_mc.GetXaxis().SetTitle('n True Interactions')


#legend
leg = ROOT.TLegend(0.65, 0.65, 0.89, 0.89)
leg.SetBorderSize(0)
# all
c = ROOT.TCanvas('c', 'c', 800, 600)
h_central_mc.Draw('hist')
h_central_mc_80mb.Draw('hist same')
h_miniAOD_mc.Draw('hist same')
h_nanoAOD_mc.Draw('hist same')
leg.AddEntry(h_central_mc, 'central 69.2 mb', 'l')
leg.AddEntry(h_central_mc_80mb, 'central 80mb', 'l')
leg.AddEntry(h_miniAOD_mc, 'miniAOD', 'l')
leg.AddEntry(h_nanoAOD_mc, 'nanoAOD', 'l')
leg.Draw()
c.SaveAs(f'{out_dir}/pileupMC_{era}.png')
c.Clear()
leg.Clear()

exit(0)
# miniAOD vs central
c = ROOT.TCanvas('c', 'c', 800, 600)
h_central_mc.Draw('hist')
h_miniAOD_mc.Draw('hist same')
leg.AddEntry(h_central_mc, 'central', 'l')
leg.AddEntry(h_miniAOD_mc, 'miniAOD', 'l')
leg.Draw()
c.SaveAs(f'{out_dir}/pileupMC_central_vs_miniAOD_{era}.png')
c.Clear()
leg.Clear()
# nanoAOD vs central
h_central_mc.Draw('hist')
h_nanoAOD_mc.Draw('hist same')
leg.AddEntry(h_central_mc, 'central', 'l')
leg.AddEntry(h_nanoAOD_mc, 'nanoAOD', 'l')
leg.Draw()
c.SaveAs(f'{out_dir}/pileupMC_central_vs_nanoAOD_{era}.png')
c.Clear()
leg.Clear()
# miniAOD vs nanoAOD
h_miniAOD_mc.Draw('hist')
h_nanoAOD_mc.Draw('hist same')
leg.AddEntry(h_miniAOD_mc, 'miniAOD', 'l')
leg.AddEntry(h_nanoAOD_mc, 'nanoAOD', 'l')
leg.Draw()
c.SaveAs(f'{out_dir}/pileupMC_miniAOD_vs_nanoAOD_{era}.png')
c.Clear()


