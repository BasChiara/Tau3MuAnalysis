import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

import sys
sys.path.append('..')
from mva.config import mc_samples, mc_bdt_samples, base_selection

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root')
parser.add_argument('--tree',           default='Events')
parser.add_argument('--outdir',         default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--tag',            default= '', help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y','--year',      choices= ['2022', '2023'], default = '2022')
parser.add_argument('-p','--process',   choices= ['WTau3Mu', 'W3MuNu', 'DsPhiPi', 'ZTau3Mu'], default = 'WTau3Mu')

args = parser.parse_args()
tag = args.tag

year_id_dict = {
    '2022preEE'  : '220',
    '2022EE'     : '221',
    '2023preBPix': '230',
    '2023BPix'   : '231',
}
bdt_cut = 0.995
# -- read inputs
if not args.input_root:
    signals = mc_bdt_samples[args.process]
    print(f'[i] input files: {signals}')
    tree_rdf = ROOT.RDataFrame(args.tree, signals).Filter(base_selection)
else:
    try:
        infile = ROOT.TFile.Open(args.input_root)
    except:
        print(f' [+] error cannot open {args.input_root}')
        exit(-1)
    else:
        tree_rdf = ROOT.RDataFrame(args.tree, args.input_root).Filter(base_selection)
if not tree_rdf:
    print(f' [+] error reading tree {args.tree} from {args.input_root}')
    exit(-1)

print(f' [+] get tree from {args.input_root} with {tree_rdf.Count().GetValue()} events')

N_tot = tree_rdf.Count().GetValue()
print(f'[+] Nevents (2022+2023) {N_tot}')
N_2022 = tree_rdf.Filter('(year_id>219) &  (year_id<230)').Count().GetValue()
print(f'[+] Nevents (2022) {N_2022}')
N_2023 = tree_rdf.Filter('(year_id>229) & (year_id<240)').Count().GetValue()
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

# yields per year
for i, year in enumerate(year_id_dict.keys()) :
    sub_rdf = tree_rdf.Filter(f'year_id == {year_id_dict[year]}')
    print(f'[i] process year {year} : {sub_rdf.Count().GetValue()} events')
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


# ------ HLT OPVERLAP ------ #
c = ROOT.TCanvas("c", "", 800, 800)
margin = 0.12
ROOT.gPad.SetMargin(margin, margin, margin, margin)
ROOT.gStyle.SetPaintTextFormat("3.1f %")

bdt_cut = 0.995
if bdt_cut > 0. : tag += '_'+'bdt' + str(bdt_cut).replace('.', 'p')
for i, year in enumerate(year_id_dict.keys()) :
    this_selection = f'(year_id == {year_id_dict[year]}) & (bdt_score > {bdt_cut})'
    h_overlap = tree_rdf.Filter(this_selection).Histo2D((f'HLT_overlap_{year}', '', 2, -0.5, 1.5, 2, -0.5, 1.5), "HLT_isfired_Tau3Mu", "HLT_isfired_DoubleMu").GetPtr()
    #h_overlap = ROOT.gPad.GetPrimitive('h_overlap')
    h_overlap.SetMarkerSize(3)
    h_overlap.SetTitle(f'HLT overlap {year}')
    h_overlap.Scale(100./h_overlap.Integral())
    h_overlap.GetXaxis().SetTitle("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15*")
    h_overlap.GetXaxis().SetNdivisions(2)
    h_overlap.GetYaxis().SetTitle("HLT_DoubleMu4_3_LowMass")
    h_overlap.GetYaxis().SetNdivisions(2)
    h_overlap.GetZaxis().SetRangeUser(0.0, 100.0)

    h_overlap.Draw("colz text0")
    c.SaveAs(f'{args.outdir}/HLToverlap_{year}_{tag}.png')
    c.SaveAs(f'{args.outdir}/HLToverlap_{year}_{tag}.pdf')
