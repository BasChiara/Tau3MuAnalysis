import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

import sys
sys.path.append('..')
from mva.config import WTau3Mu_signals, DsPhiPi_signals

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root')
parser.add_argument('--tree',           default='Events')
parser.add_argument('--outdir',         default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--tag',            default= '', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y','--year',      choices= ['2022', '2023'], default = '2022')
parser.add_argument('-p','--process',   choices= ['WTau3Mu', 'W3MuNu', 'DsPhiPi'], default = 'WTau3Mu')

args = parser.parse_args()
tag = args.tag

year_id_dict = {
    '2022preEE'  : '220',
    '2022EE'     : '221',
    '2023preBPix': '230',
    '2023BPix'   : '231',
}

# -- read inputs
if not args.input_root:
    if args.process == 'WTau3Mu':
        signals = WTau3Mu_signals
        tree    ='WTau3Mu_tree'
    elif args.process == 'DsPhiPi':
        signals = DsPhiPi_signals
        tree    = 'DsPhiMuMuPi_tree'
    tree_rdf = ROOT.RDataFrame(tree, signals)
else:
    try:
        infile = ROOT.TFile.Open(args.input_root)
    except:
        print(f' [+] error cannot open {args.input_root}')
    else:
        tree_rdf = ROOT.RDataFrame(args.tree, args.input_root)
        print(f' [+] get tree from {args.input_root} with {tree_rdf.Count()} events')

N_tot = tree_rdf.Count().GetValue()
print(f'[+] Nevents (2022+2023) {N_tot}')
N_2022 = tree_rdf.Filter('year_id == 220').Count().GetValue()
print(f'[+] Nevents (2022) {N_2022}')
N_2023 = tree_rdf.Filter('year_id == 230').Count().GetValue()
print(f'[+] Nevents (2023) {N_2023}')

eff_by_year_T3m = ROOT.TH1F("eff_by_year_T3m", "eff_by_year_T3m", len(year_id_dict.keys()), -2, 2)
eff_by_year_T3m.SetLineWidth(3)
eff_by_year_T3m.SetFillColor(ROOT.kBlue)
eff_by_year_T3m.SetFillStyle(3004)
eff_by_year_T3m.SetMarkerSize(2)
eff_by_year_T3m.GetXaxis().SetNdivisions(-2*len(year_id_dict.keys()))
eff_by_year_T3m.GetXaxis().ChangeLabel(-1,-1,-1,-1,-1,-1," ")
eff_by_year_T3m.GetXaxis().SetTitle("Year")
eff_by_year_T3m.GetYaxis().SetTitle("fraction [%]")
eff_by_year_T3m.GetYaxis().SetRangeUser(50, 100)
eff_by_year_T3m.SetTitle("N(HLT_Tau3Mu* & HLT_DoubleMu4_3_LowMass)/N(HLT_Tau3Mu*)")

eff_by_year_Dm = ROOT.TH1F("eff_by_year_Dm", "eff_by_year_Dm", len(year_id_dict.keys()), -2, 2)
eff_by_year_Dm.SetLineWidth(3)
eff_by_year_Dm.SetFillColor(ROOT.kBlue)
eff_by_year_Dm.SetFillStyle(3004)
eff_by_year_Dm.SetMarkerSize(2)
eff_by_year_Dm.GetXaxis().ChangeLabel(-1,-1,-1,-1,-1,-1," ")
eff_by_year_Dm.GetXaxis().SetNdivisions(-2*len(year_id_dict.keys()))
eff_by_year_Dm.GetXaxis().SetTitle("Year")
eff_by_year_Dm.GetYaxis().SetTitle("fraction [%]")
eff_by_year_Dm.GetYaxis().SetRangeUser(50, 100)
eff_by_year_Dm.SetTitle("N(HLT_Tau3Mu* & HLT_DoubleMu4_3_LowMass)/N(HLT_DoubleMu4_3_LowMass)")

for i, year in enumerate(year_id_dict.keys()) :
    print(f'[i] process year {year}')
    sub_rdf = tree_rdf.Filter(f'year_id == {year_id_dict[year]}')
    print(f'  {sub_rdf.Count().GetValue()}')
    N_HLT_DoubleMu = sub_rdf.Filter("HLT_isfired_DoubleMu").Count().GetValue() 
    N_HLT_Tau3Mu   = sub_rdf.Filter("HLT_isfired_Tau3Mu").Count().GetValue() 
    N_HLT_overlap  = sub_rdf.Filter("HLT_isfired_DoubleMu & HLT_isfired_Tau3Mu").Count().GetValue() 
    
    #f_HLT_DoubleMu_fired_by_HLT_Tau3Mu
    eff_by_year_T3m.SetBinContent(i+1, N_HLT_overlap/N_HLT_Tau3Mu*100)
    eff_by_year_T3m.GetXaxis().ChangeLabel(2*i+2,-1,-1,-1,-1,-1,year)
    eff_by_year_T3m.GetXaxis().ChangeLabel(2*i+1,-1,-1,-1,-1,-1," ")
    #f_HLT_Tau3Mu_fired_by_HLT_DoubleMu
    eff_by_year_Dm.SetBinContent(i+1, N_HLT_overlap/N_HLT_DoubleMu*100)
    eff_by_year_Dm.GetXaxis().ChangeLabel(2*i+2,-1,-1,-1,-1,-1,year)
    eff_by_year_Dm.GetXaxis().ChangeLabel(2*i+1,-1,-1,-1,-1,-1," ")

c = ROOT.TCanvas("c", "", 800, 800)
ROOT.gStyle.SetPaintTextFormat("4.1f %")

eff_by_year_T3m.Draw("hist text0")
c.SaveAs(f'{args.outdir}/HLT_eff_Tau3Mu_over_DoubleMu_on{args.process}.png')
c.SaveAs(f'{args.outdir}/HLT_eff_Tau3Mu_over_DoubleMu_on{args.process}.pdf')

eff_by_year_Dm.Draw("hist text0")
c.SaveAs(f'{args.outdir}/HLT_eff_DoubleMu_over_Tau3Mu_on{args.process}.png')
c.SaveAs(f'{args.outdir}/HLT_eff_DoubleMu_over_Tau3Mu_on{args.process}.pdf')


exit()

c = ROOT.TCanvas("c", "", 800, 800)
legend = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
legend.SetBorderSize(0)
legend.SetTextSize(0.035)

intree.Draw("HLT_isfired_Tau3Mu:HLT_isfired_DoubleMu>>h_overlap(2, -0.5, 1.5, 2, -0.5, 1.5)", '', 'colz')
h_overlap = ROOT.gPad.GetPrimitive('h_overlap')
h_overlap.SetMarkerSize(1.5)

h_overlap.Draw("colz text0")
c.SaveAs('%s/HLToverlap_%s.png'%(args.outdir, tag))
c.SaveAs('%s/HLToverlap_%s.pdf'%(args.outdir, tag))
