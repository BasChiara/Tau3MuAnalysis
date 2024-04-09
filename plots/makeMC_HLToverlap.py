import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root', default='/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/WTau3Mu_MC2017.root')
parser.add_argument('--tree', default='Events')
parser.add_argument('--outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')

args = parser.parse_args()
tag = args.tag

# -- read inputs
try:
    infile = ROOT.TFile.Open(args.input_root)
except:
    print(f' [+] error cannot open {args.input_root}')
else:
    intree = infile.Get(args.tree)
    print(f' [+] get tree from {args.input_root} with {intree.GetEntries()} events')

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
