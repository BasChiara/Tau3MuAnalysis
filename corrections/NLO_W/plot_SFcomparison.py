import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kBlackBody)
import cmsstyle as cms
import argparse
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

argparser = argparse.ArgumentParser()
argparser.add_argument('--input', '-i', 
                       required=True,
                       action='store',
                       help='list of input root files, separated by comma')
argparser.add_argument('--labels', '-l',
                          required=True,
                          action='store',
                          help='list of labels for the input files, separated by comma')
argparser.add_argument('--year', '-y',
                          required=True,
                          action='store',
                          help='data taking year')
argparser.add_argument('--output', '-o',
                          required=True,
                          action='store',
                          help='output plot file name')
args = argparser.parse_args()

input_files = args.input.split(',')
labels = args.labels.split(',')
if len(input_files) != len(labels):
    raise RuntimeError("Number of input files and labels must be the same")
output_file = args.output
year = args.year

print("Input files: ", input_files)
print("Labels: ", labels)
# variables to plot
cat = 'NLO'
var = ['pT', 'eta']
for v in var:

    histos = []
    hist_tag = f'{cat}_{v}'
    for i, f in enumerate(input_files):
        infile = ROOT.TFile.Open(f)
        # show all keys in the file
        keylist = infile.GetListOfKeys()
        for key in keylist:
            if str(key.GetName()).endswith(hist_tag):
                hist_name = key.GetName()
                histo = infile.Get(hist_name)
                if not histo:
                    raise RuntimeError(f'Histogram {hist_name} not found in file {f}')
                else:
                    print(f'Found histogram {hist_name} in file {f}')
        histo = infile.Get(hist_name)
        histo.SetDirectory(0)
        histo.SetLineColor(i+1)
        histo.SetMarkerColor(i+1)
        histo.SetMarkerStyle(20+i)
        histos.append(histo)
        infile.Close()
    
    canv = ROOT.TCanvas(f'canv_SF_{cat}_{v}', f'canv_SF_{cat}_{v}', 800, 600)
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    legend.SetBorderSize(0)
    for i, h in enumerate(histos):
        legend.AddEntry(h, labels[i], 'lep')
        h.Draw('E same' if i>0 else 'E')
    legend.Draw()
    canv.SaveAs(f'{output_file}/{cat}_{v}.png')

# compare scale factors
hist_tag = 'ratio_pTeta'
histos = []
histo_ref = None
for i, f in enumerate(input_files):
    infile = ROOT.TFile.Open(f)
    keylist = infile.GetListOfKeys()
    for key in keylist:
        if str(key.GetName()).endswith(hist_tag):
            hist_name = key.GetName()
            histo = infile.Get(hist_name)
            if not histo:
                raise RuntimeError(f'Histogram {hist_name} not found in file {f}')
            else:
                print(f'Found histogram {hist_name} in file {f}')
    histo = infile.Get(hist_name)
    histo.SetDirectory(0)
    histo.SetLineColor(i+1)
    histo.SetMarkerColor(i+1)
    histo.SetMarkerStyle(20+i)
    histos.append(histo)
    infile.Close()
histo_ref = histos[0]
histos = histos[1:]
for i, h in enumerate(histos):
    
    hpull = histo_ref.Clone(f'pull_{i}')
    hpull.SetTitle(f'Pull wrt {labels[0]}')
    hpull.Add(h, -1)
    for ix in range(1, hpull.GetNbinsX()+1):
        for iy in range(1, hpull.GetNbinsY()+1):
            if hpull.GetBinContent(ix, iy) == 0: 
                hpull.SetBinContent(ix, iy, -999)  # to make it white in the plot
                continue
            err_ref = histo_ref.GetBinError(ix, iy)
            err_cmp = h.GetBinError(ix, iy)
            denom = (err_ref**2 + err_cmp**2)**0.5
            if denom > 0:
                pull = hpull.GetBinContent(ix, iy) / denom
                hpull.SetBinContent(ix, iy, pull)
            else:
                print(f'[WARNING] Zero uncertainty in bin ({ix}, {iy}), setting pull to 0')
                hpull.SetBinContent(ix, iy, 0)

    canv = ROOT.TCanvas(f'canv_pull_{i}', f'canv_pull_{i}', 800, 600)
    ROOT.gPad.SetRightMargin(0.15)
    hpull.SetAxisRange(-1, 1, 'Z')
    hpull.GetXaxis().SetTitle('gen p_{T} (GeV)')
    hpull.GetYaxis().SetTitle('gen |#eta|')
    hpull.GetZaxis().SetTitle(f'Pull {labels[i+1]}-{labels[0]}')
    hpull.Draw('COLZ')
    canv.SaveAs(f'{output_file}/pull_{labels[0]}_vs_{labels[i+1]}.png')
