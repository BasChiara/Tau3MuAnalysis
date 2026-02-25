import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import os
import json
import argparse
import numpy as np

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import mva.config as config
import cmsstyle as CMS
CMSStyle = CMS.getCMSStyle()
ROOT.TGaxis.SetMaxDigits(3)
CMS.SetEnergy(13.6)
CMS.SetExtraText("Preliminary")
#ROOT.gStyle.SetErrorY(0.0)


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--input', help='Input json file with efficiency summary', required=True)
    argparser.add_argument('-o', '--output', help='output dest.', default='.')
    argparser.add_argument('-y', '--year', choices = ['22', '23'], default='22', help='Year of the data taking period')
    args = argparser.parse_args()

    if not os.path.exists(args.input):
        print(f'[ERROR]: input file {args.input} not found')
        sys.exit(1)
    with open(args.input, 'r') as f:
        eff_summary = json.load(f)

    print('\n-----------------------------\n')
    x_min, x_max = -0.5, 2.5
    y_min, y_max = 0.7, 1.1
    r_min, r_max = 0.0, 10.0
    h_mc_eff = ROOT.TH1F('h_mc_eff', 'h_mc_eff', 3, x_min, x_max)
    h_data_eff = ROOT.TH1F('h_data_eff', 'h_data_eff', 3, x_min, x_max)
    h_ratio = ROOT.TH1F('h_ratio', 'h_ratio', 3, x_min, x_max)
    h_stat_err = ROOT.TH1F('h_stat_err', 'h_stat_err', 3, x_min, x_max)
    icat = 0
    for cat, values in eff_summary.items():
        icat += 1
        print(f' Category: {cat}')
        effdata = values['effdata'][0]
        effdata_err = values['effdata'][1]
        effmc = values['effmc'][0]
        effmc_err = values['effmc'][1]
        syst  = (values['total'] - 1.) * 100.
        stat  = (values['stat'] -1.) * 100.

        print(f'  Efficiency data: {effdata:.4f} +/- {effdata_err:.4f}')
        print(f'  Efficiency MC:   {effmc:.4f} +/- {effmc_err:.4f}')
        print(f'  Systematic unc.: {syst:.4f}')
        print(f'  Statistical unc.: {stat:.4f}')

        h_mc_eff.SetBinContent(icat, effmc)
        h_mc_eff.SetBinError(icat, effmc_err)
        h_mc_eff.GetXaxis().SetBinLabel(icat, cat)
        h_data_eff.SetBinContent(icat, effdata)
        h_data_eff.SetBinError(icat, effdata_err)
        h_data_eff.GetXaxis().SetBinLabel(icat, cat)
        h_ratio.SetBinContent(icat, syst)
        h_ratio.GetXaxis().SetBinLabel(icat, cat)
        #h_ratio.SetBinError(icat, 0)
        h_stat_err.SetBinContent(icat, stat)
        #h_stat_err.SetBinError(icat, 0)

    h_mc_eff.SetTitle('')

    name = f'{args.output}/LxyS_efficiency_20{args.year}'
    CMS.SetLumi(config.LumiVal_plots['20'+str(args.year)], run='20'+str(args.year))
    c = CMS.cmsDiCanvas('c', 
                    x_min, 
                    x_max, 
                    y_min, 
                    y_max,
                    r_min,
                    r_max,
                    'CAT',
                    "#varepsilon(L_{xy}/#sigma > 2.0)",
                    "syst. unc. (%)",
                    square = CMS.kSquare, 
                    extraSpace=0, 
                    iPos=11
    )
    c.cd(1)
    CMS.cmsDraw(
        h_mc_eff, 'PE',
        lwidth = 2,
        mcolor = ROOT.kBlue,
        marker = 20,
        fcolor = ROOT.kBlue,
        fstyle = -1,
    )
    CMS.cmsDraw(
        h_data_eff, 'PE same',
        lwidth = 2,
        mcolor = ROOT.kBlack,
        marker = 20,
        fcolor = ROOT.kBlack,
        fstyle = -1,
    )
    leg = ROOT.TLegend(0.6, 0.70, 0.9, 0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(h_data_eff, 'Data', 'lep')
    leg.AddEntry(h_mc_eff, 'D_{s}#rightarrow #phi(#mu#mu)#pi MC', 'lep')
    leg.Draw()
    c.cd(2)
    CMS.cmsDraw(
        h_ratio, 'P',
        lwidth = 2,
        mcolor = ROOT.kBlack,
        marker = 20,
        fcolor = 0,
        fstyle = 0,
    )
    c.SaveAs(name+'.pdf')
    c.SaveAs(name+'.png')

    
