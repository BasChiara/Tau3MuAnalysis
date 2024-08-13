import ROOT
import argparse
import sys
sys.path.append('../../')
from plots.plotting_tools import ratio_plot_CMSstyle


# parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default='W_NLOvsT3m_2022EE_demo.root', help='root input file')
parser.add_argument('--year',  choices=['2022', '2022preEE', '2022EE', '2023', '2023preBPix', '2023BPix'], default='2022preEE', help='year/era of the data')
args = parser.parse_args()
print('\n')

input_file = ROOT.TFile(args.input)

# draw 2D ratio 
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat('4.3f')
c = ROOT.TCanvas(f'c_2D', "c", 1200, 800)
ratio2D = input_file.Get('h_Wgen_ratio')
ratio2D.SetTitle('W NLO/LO ratio')
ratio2D.GetXaxis().SetTitle('eta')
ratio2D.GetYaxis().SetTitle('pT')
ratio2D.Draw('colz text error 0')
print(f' bin content: {ratio2D.GetBinContent(1,1)} and error {ratio2D.GetBinError(1,1)}')
c.SaveAs(f'plots/W_NLOvsT3m_ratio_{args.year}_2D.png')
c.SaveAs(f'plots/W_NLOvsT3m_ratio_{args.year}_2D.pdf')

# draw 1D ratio
obs_list = ['eta', 'pT']
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.SetBorderSize(0)
for obs in obs_list:
    histo_LO    = input_file.Get(f'h_Wgen_t3m_{obs}')
    histo_LO.SetLineColor(ROOT.kBlue)
    histo_LO.SetLineWidth(2)
    histo_LO.SetTitle(f'W {obs} distribution')
    histo_LO.GetXaxis().SetTitle(f'{obs}')
    histo_LO.GetYaxis().SetTitle('Events')
    histo_NLO   = input_file.Get(f'h_Wgen_NLO_{obs}')
    histo_NLO.SetLineColor(ROOT.kRed)
    histo_NLO.SetLineWidth(2)

    c = ROOT.TCanvas(f'c_{obs}', "c", 800, 800)
    c.cd()
    histo_LO.Draw("HISTE")
    histo_NLO.Draw("HISTE same")
    legend.AddEntry(histo_LO, 'LO', 'l')
    legend.AddEntry(histo_NLO, 'NLO', 'l')
    legend.Draw()
    c.SaveAs(f'plots/W_{obs}_NLOvsLO.png')
    c.SaveAs(f'plots/W_{obs}_NLOvsLO.pdf')

    # ratio plot
    ratio_plot_CMSstyle(
        histo_num = [histo_NLO], 
        histo_den = histo_LO, 
        isMC = True,
        year = 2022,
        ratio_yname = 'NLO/LO',
        ratio_w = 2.0,
        to_ploton=[legend],
        file_name = f'plots/W_NLOvsT3m_ratio_{args.year}_{obs}', 
    )


    legend.Clear()


