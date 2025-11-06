import argparse
import sys
import os
import numpy as np

sys.path.append('../../')
from plots.plotting_tools import ratio_plot_CMSstyle
import mva.config as cfg

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import cmsstyle as CMS
CMS.SetExtraText("Simulation Preliminary")
CMS.SetLumi("")
CMS.SetEnergy("13.6")

# parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default='W_NLOvsT3m_2022EE_demo.root', help='root input file')
parser.add_argument('--year',  choices=['2022', '2022preEE', '2022EE', '2023', '2023preBPix', '2023BPix'], default='2022preEE', help='year/era of the data')
parser.add_argument('--Vboson', choices=['W', 'Z'], default='W', help='which V boson to consider')
parser.add_argument('--output', type=str, default='W_NLOvsT3m_Run3.root', help='root output file')
parser.add_argument('--debug', action='store_true', help='print debug information')
args = parser.parse_args()
print('\n')

V = args.Vboson

input_file = ROOT.TFile(args.input)
if not input_file:
    print(f'[ERRROR] input file {args.input} not found')
    exit()
else:
    print(f'[+] input file {args.input}\n')
# -- SF 2D map
h_lo_2D  = input_file.Get(f'h_Wgen_{args.year}_t3m_pTeta')
h_nlo_2D = input_file.Get(f'h_Wgen_{args.year}_NLO_pTeta')
ratio2D  = input_file.Get(f'h_Wgen_{args.year}_ratio_pTeta')
ratio2D.SetDirectory(0)
ratio2D.SetTitle(V+'_{gen} NLO/LO SF')
ratio2D.SetName(f'h_Wgen_{args.year}_ratio_pTeta_nominal')
ratio2D_sysUP = ROOT.TH2F(f'h_Wgen_{args.year}_ratio_pTeta_up', V+'_{gen} NLO/LO SF + sys', 
                          ratio2D.GetNbinsX(), ratio2D.GetXaxis().GetXmin(), ratio2D.GetXaxis().GetXmax(),
                          ratio2D.GetNbinsY(), ratio2D.GetYaxis().GetXmin(), ratio2D.GetYaxis().GetXmax())
ratio2D_sysUP.SetDirectory(0)
ratio2D_sysDOWN = ROOT.TH2F(f'h_Wgen_{args.year}_ratio_pTeta_down', V+'_{gen} NLO/LO SF - sys', 
                          ratio2D.GetNbinsX(), ratio2D.GetXaxis().GetXmin(), ratio2D.GetXaxis().GetXmax(),
                          ratio2D.GetNbinsY(), ratio2D.GetYaxis().GetXmin(), ratio2D.GetYaxis().GetXmax()) 
ratio2D_sysDOWN.SetDirectory(0)
stat_threshold = 5 * 1e-5
for i,j in np.ndindex((ratio2D.GetNbinsX(), ratio2D.GetNbinsY())):
    # remove SF from bins with low statistics
    if h_lo_2D.GetBinContent(i+1, j+1) < stat_threshold or h_nlo_2D.GetBinContent(i+1, j+1) < stat_threshold:
        ratio2D.SetBinContent(i+1, j+1, 0.0)
        ratio2D.SetBinError(i+1, j+1, 0.0)
        if (args.debug) : print(f'[i] low statistics in (pT,eta) = ({ratio2D.GetXaxis().GetBinCenter(i+1)}, {ratio2D.GetYaxis().GetBinCenter(j+1)})')
    # fill the systematic variations
    ratio2D_sysUP.SetBinContent(i+1, j+1, ratio2D.GetBinContent(i+1, j+1) + ratio2D.GetBinError(i+1, j+1))
    ratio2D_sysDOWN.SetBinContent(i+1, j+1, ratio2D.GetBinContent(i+1, j+1) - ratio2D.GetBinError(i+1, j+1))

# draw 2D ratio
c = CMS.cmsCanvas(
                canvName = 'c',
                x_min = 0, x_max = 150, y_min = 0, y_max = 10,
                nameXaxis = V+'_{gen} p_{T} (GeV)', nameYaxis = V+"_{gen} |#eta|",
                square=False ,extraSpace=0.03,
                iPos=0,
                with_z_axis=True,
                scaleLumi=0.8,
                )
c.SetRightMargin(0.20)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat('4.3f')
CMS.SetCMSPalette()

ratio2D.SetMarkerColor(ROOT.kWhite)
ratio2D.GetZaxis().SetTitle('NLO/LO SF')
ratio2D.GetZaxis().SetTitleSize(0.05)
ratio2D.GetZaxis().SetRangeUser(0.6, 3.0)
#CMS.cmsDraw(ratio2D, 'colz text error 0', mcolor = ROOT.kWhite)
CMS.cmsDraw(ratio2D, 'colz', mcolor = ROOT.kWhite)
CMS.UpdatePalettePosition(ratio2D, c)
text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(31)
text.SetTextFont(42)
text.DrawLatex(0.80, 0.94, f'{args.year}')
c.SaveAs(f'plots/{V}_NLOvsT3m_ratio_{args.year}_2D.png')
c.SaveAs(f'plots/{V}_NLOvsT3m_ratio_{args.year}_2D.pdf')
c.Close()

# draw 1D ratio
obs_list = ['eta', 'pT']
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.SetBorderSize(0)
for obs in obs_list:
    histo_LO    = input_file.Get(f'h_Wgen_{args.year}_t3m_{obs}')
    if not histo_LO:
        print(f'[i] histogram h_Wgen_{args.year}_t3m_{obs} not found')
        exit()
    histo_LO.SetLineColor(ROOT.kBlue)
    histo_LO.SetLineWidth(2)
    histo_LO.SetTitle(f'W {obs} distribution')
    histo_LO.GetXaxis().SetTitle(f'{obs}')
    histo_LO.GetYaxis().SetTitle('Events')
    histo_NLO   = input_file.Get(f'h_Wgen_{args.year}_NLO_{obs}')
    if not histo_NLO:
        print(f'[i] histogram h_Wgen_{args.year}_NLO_{obs} not found')
        exit()
    histo_NLO.SetLineColor(ROOT.kRed)
    histo_NLO.SetLineWidth(2)
    
    legend.AddEntry(histo_LO, 'LO', 'l')
    legend.AddEntry(histo_NLO, 'NLO', 'l')

    # ratio plot
    ratio_plot_CMSstyle(
        histo_num = [histo_NLO], 
        histo_den = histo_LO,
        isMC = True,
        year = args.year,
        ratio_yname = 'NLO/LO',
        ratio_w = 2.0,
        to_ploton=[legend],
        file_name = f'plots/{V}_NLOvsLO_ratio_{args.year}_{obs}', 
    )


    legend.Clear()
input_file.Close()


# update the outout file if it exixsts
if os.path.exists(args.output):
    print(f'[i] output file {args.output} exists, updating it')
    output_file = ROOT.TFile(args.output, 'UPDATE')
else:    
    print(f'[i] output file {args.output} does not exist, creating it')
    output_file = ROOT.TFile(args.output, 'RECREATE')

output_file.cd()
ratio2D.Write()
ratio2D_sysUP.Write()
ratio2D_sysDOWN.Write()
output_file.Close()