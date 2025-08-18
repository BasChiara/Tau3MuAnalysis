import ROOT
import cmsstyle as CMS
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import math
import argparse
# import custom configurations
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import mva.config as config
import plots.plotting_tools as plotting_tools


def draw_by_category(cat_dict, histo_list, x_lim = [-1,-1], fit = False, print_mean = False):
     
    x_min = histo_list[0].GetBinLowEdge(histo_list[0].FindFirstBinAbove(0.)) if (x_lim[0] == x_lim[1]) else x_lim[0] 
    x_max = histo_list[0].GetBinLowEdge(histo_list[0].FindLastBinAbove(0.)+1) if (x_lim[0] == x_lim[1]) else x_lim[1] 
    y_min = histo_list[0].GetMinimum()
    y_max = histo_list[0].GetMaximum()
    c = CMS.cmsCanvas('c', 
                    x_min, 
                    x_max, 
                    y_min, 
                    y_max, 
                    histo_list[0].GetXaxis().GetTitle(),
                    histo_list[0].GetYaxis().GetTitle(), 
                    square = CMS.kSquare, 
                    extraSpace=0.01, 
                    iPos=11
    ) 
    leg_x1, leg_y1, leg_x2, leg_y2 = 0.60, 0.85, 0.90, 0.90
    legend = CMS.cmsLeg(leg_x1, leg_y1 - 0.06 * len(histo_list), leg_x2, leg_y2, textSize=0.05)
    # text-box for fit results
    text_box = ROOT.TLatex()
    text_box.SetNDC()
    text_box.SetTextSize(0.035)
    text_box.SetTextFont(42)
    text_box.SetTextAlign(11)

    cat_list = list(cat_dict)
    for i,histo in enumerate(histo_list):

        CMS.cmsDraw(histo, 
            'hist ' + ('same' if i >0 else ''),
            lwidth = 2,
            marker = histo.GetMarkerStyle(),
            mcolor = histo.GetLineColor(), 
            fcolor = histo.GetFillColor(),
        )
        if fit:
            fit = ROOT.TF1('fit', 'gaus', x_min + 0.1, x_max - 0.1)
            histo.Fit(fit, 'R')
            histo.GetFunction('fit').SetLineColor(histo.GetLineColor())
            histo.GetFunction('fit').SetLineStyle(2)
            histo.GetFunction('fit').SetLineWidth(2)
            histo.GetFunction('fit').Draw('same')
            mass = histo.GetFunction('fit').GetParameter(1)
            mass_err = histo.GetFunction('fit').GetParError(1)
            sigma = histo.GetFunction('fit').GetParameter(2)
            sigma_err = histo.GetFunction('fit').GetParError(2)
            text_box.DrawLatex(leg_x1 - 0.05, 0.6 - 0.05 * i, 
                               '#sigma/M_{'+ f'{cat_list[i]}'+'}' + f' = ({sigma/mass * 1000:.2f} #pm {(sigma/mass * sqrt( (sigma_err/sigma)**2 + (mass_err/mass)**2)) * 1000:.2f})#times 10^{{-3}}')
                               #f'#sigma_{{M}}({cat_list[i]}) = ({sigma * 1000:.2f} #pm {sigma_err * 1000:.2f}) MeV')
        if print_mean:
            mean = histo.GetMean()
            mean_err = histo.GetMeanError()
            #text_box.DrawLatex(leg_x1, 0.5 - 0.05 * i, f'mean_{{cat_list[i]}} = {mean*1000:.1f} #times 10^{{-3}}')

        legend.AddEntry(histo.GetName(), f'cat {cat_list[i]}')
    CMS.fixOverlay()
    c.Update()
    c.RedrawAxis()
    return c, legend


parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/categorization/', help=' output directory for plots')
parser.add_argument('--tag',        default= '', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y', '--year', choices = ['2022', '2023', 'Run3'], default = '2022',help='which data taking year')
parser.add_argument('--isMC',       action = 'store_true')

args = parser.parse_args()


tag = f'{args.year}' + (f'{args.tag}' if args.tag else '') + ('_MC' if args.isMC else '')

ROOT.gROOT.SetBatch(True)
CMS.setCMSStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetHistMinimumZero(False)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.035)
ROOT.TH1.SetDefaultSumw2()
ROOT.gStyle.SetPalette(ROOT.kBird)
CMS.SetExtraText("Preliminary") if not args.isMC else CMS.SetExtraText("Simulation Preliminary") 
CMS.SetLumi(config.LumiVal_plots[args.year]) if not args.isMC else CMS.SetLumi('') 
CMS.SetEnergy(13.6)

# import MC or DATA
data = config.WTau3Mu_signals if args.isMC else config.data_background

# selection
base_selection = '&'.join([
    config.year_selection[args.year],
    config.base_selection, 
    config.phi_veto
])
mass_range_lo = config.mass_range_lo if not args.isMC else 1.6
mass_range_hi = config.mass_range_hi if not args.isMC else 2.0
print('\n---------------------------------------------')
print('[!] base-selection   : %s'%base_selection)
print('---------------------------------------------\n')

tree_name = 'WTau3Mu_tree'
print(f'[+] adding {args.year} data')
data_rdf = ROOT.RDataFrame(tree_name, data, ['tau_fit_mass', 'tau_fit_mass_resol', 'tau_fit_eta']).Filter(base_selection).Define('tau_fit_absEta', 'fabs(tau_fit_eta)')
print(f'   {data_rdf.Count().GetValue()} entries passed selection')
print('---------------------------------------------')

# divide by mass_resolution
max_y = 0.12 if not args.isMC else 0.5
min_y = 0.05 if not args.isMC else 0.0
mass_bin_w     = 0.01 if args.isMC else 0.05
mass_bins = int((mass_range_hi - mass_range_lo) / mass_bin_w)

# resolution VS eta
resol_min, resol_max = 0.0, 0.025

h_resolMvsEta = data_rdf.Histo2D(('h_resolMvsEta', '', 48, 0, 2.4, 50, 0.0, 0.025), 'tau_fit_absEta', 'tau_fit_mass_resol').GetPtr()
prof_resolMvsEta = data_rdf.Profile1D(('prof_resolMvsEta', '', 48, 0, 2.4), 'tau_fit_absEta', 'tau_fit_mass_resol').GetPtr()
h_resolMvsEta.GetYaxis().SetTitle('#sigma_{M}/M(3#mu)')
h_resolMvsEta.GetXaxis().SetTitle('|#eta_{3#mu}|')
h_resolMvsEta.GetXaxis().SetTitleOffset(1.2)

c = ROOT.TCanvas('c_resolMvsEta', 'c_resolMvsEta', 1200, 800)
c.SetMargin(0.15, 0.15, 0.15, 0.05)
prof_resolMvsEta.SetLineColor(ROOT.kBlack)
prof_resolMvsEta.SetMarkerStyle(24)
prof_resolMvsEta.SetMarkerColor(ROOT.kBlack)
prof_resolMvsEta.SetLineWidth(2)
lineAB = ROOT.TLine(0.9, resol_min, 0.9, resol_max)
lineAB.SetLineColor(ROOT.kRed)
lineAB.SetLineWidth(2)
lineBC = ROOT.TLine(1.8, resol_min, 1.8, resol_max)
lineBC.SetLineColor(ROOT.kRed)
lineBC.SetLineWidth(2)
h_resolMvsEta.Draw('colz')
prof_resolMvsEta.Draw('same pe')
lineAB.Draw('same')
lineBC.Draw('same')
c.Modified()
c.Update()
c.SaveAs('%s/ResolMassVsEta_%s.png'%(args.plot_outdir, tag))
c.SaveAs('%s/ResolMassVsEta_%s.pdf'%(args.plot_outdir, tag))


h_bShape = []
h_eta    = []
h_bShape_etaCat = []
h_resolM_etaCat = []
h_bShape_inclusive = data_rdf.Histo1D(('h_bShape_incl', '', mass_bins, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr() 
h_bShape_inclusive.Scale(1./h_bShape_inclusive.Integral())
h_bShape_inclusive.SetMaximum(max_y)
h_bShape_inclusive.SetMinimum(min_y)
h_bShape_inclusive.GetXaxis().SetTitle('M_{3#mu} (GeV)')
h_bShape_inclusive.SetLineColor(ROOT.kBlack)
h_bShape_inclusive.SetMarkerColor(ROOT.kBlack)
h_bShape_inclusive.SetMarkerStyle(20)
h_bShape_inclusive.SetLineWidth(2)

# loop over categories
for cat in list(config.cat_selection_dict):
    # ** rel. mass resolution based 
    # -> mass shape
    h   = data_rdf.Filter(config.cat_selection_dict[cat]).Histo1D(('h_bShape_%s'%cat, '', mass_bins, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
    h.Scale(1./h.Integral())
    h.SetLineColor(config.cat_color_dict[cat])
    h.SetMarkerColor(config.cat_color_dict[cat])
    h.SetMarkerStyle(20 if not args.isMC else 1)
    h.SetMaximum(max_y)
    h.SetMinimum(min_y)
    h.GetXaxis().SetTitle('M_{3#mu} (GeV)')
    h_bShape.append(h)
    # -> eta
    he   = data_rdf.Filter(config.cat_selection_dict[cat]).Histo1D(('h_eta_%s'%cat, '', 26, 0, 2.6), 'tau_fit_absEta').GetPtr()
    he.Scale(1./he.Integral())
    he.SetMaximum(.4)
    he.SetLineColor(config.cat_color_dict[cat])
    he.SetMarkerColor(config.cat_color_dict[cat])
    he.GetXaxis().SetTitle('|#eta_{3#mu}|')
    h_eta.append(he)
    # ** eta based 
    # -> mass shape 
    h_be   = data_rdf.Filter(config.cat_eta_selection_dict[cat]).Histo1D(('h_bShapeEta_%s'%cat, '', mass_bins, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
    h_be.Scale(1./h_be.Integral())
    h_be.SetMaximum(max_y)
    h_be.SetMinimum(min_y)
    h_be.SetLineColor(config.cat_color_dict[cat])
    h_be.SetMarkerColor(config.cat_color_dict[cat])
    h_be.SetMarkerStyle(20 if not args.isMC else 1)
    h_be.GetXaxis().SetTitle('M_{3#mu} (GeV)')
    h_bShape_etaCat.append(h_be)
    # -> rel. mass resolution
    h_me   = data_rdf.Filter(config.cat_eta_selection_dict[cat]).Histo1D(('h_MresolEta_%s'%cat, '', 25, 0.0, 0.025), 'tau_fit_mass_resol').GetPtr()
    h_me.Scale(1./h_me.Integral())
    h_me.SetMaximum(1.3 * h_me.GetMaximum())
    h_me.SetLineColor(config.cat_color_dict[cat]) 
    h_me.GetXaxis().SetTitle('#sigma_{M}/M(3#mu)')
    h_resolM_etaCat.append(h_me)

    
    
# draw plots  
    
plot_name = f'{args.plot_outdir}/ResolMassCategories_bShape_{tag}'
c, l = draw_by_category(config.cat_selection_dict, h_bShape, [mass_range_lo, mass_range_hi])
l.SetHeader('#sigma_{M}/M categorization')
c.Draw()
h_bShape_inclusive.Draw('same pe')
l.AddEntry(h_bShape_inclusive.GetName(), 'inclusive')
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')
if not args.isMC:   
    plotting_tools.ratio_plot_CMSstyle(
        h_bShape, 
        h_bShape_inclusive,
        to_ploton       = [l],
        x_lim           = [mass_range_lo, mass_range_hi],
        draw_opt_den    = 'histe',
        draw_opt_num    = 'pe',
        file_name       = plot_name+'_ratio', 
        ratio_w         = 0.08, 
        ratio_yname     = 'cat /incl',
        CMSextraText    = 'Preliminary', 
        isMC            = args.isMC,
        year            = args.year
    )

plot_name = f'{args.plot_outdir}/ResolMassCategories_AbsEta_{tag}'
c, l = draw_by_category(config.cat_selection_dict, h_eta, [0, 2.6])
l.SetHeader('#sigma_{M}/M categorization')
c.Draw()
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')

plot_name = f'{args.plot_outdir}/EtaCategories_MassResol_{tag}'
c, l = draw_by_category(config.cat_selection_dict, h_resolM_etaCat, [0, 0.025], print_mean = True)
hdf = CMS.GetcmsCanvasHist(c)
hdf.GetXaxis().SetMaxDigits(2)
hdf.GetXaxis().CenterTitle(True)
# Shift multiplier position
ROOT.TGaxis.SetExponentOffset(-0.10, -0.10, "X")
l.SetHeader('|#eta| categorization')
c.Draw()
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')

plot_name = f'{args.plot_outdir}/EtaCategories_bShape_{tag}'
c, l = draw_by_category(config.cat_selection_dict, h_bShape_etaCat, [mass_range_lo, mass_range_hi], fit= args.isMC)
l.SetHeader('|#eta| categorization')
c.Draw()
if not args.isMC:
    h_bShape_inclusive.Draw('same pe')
    l.AddEntry(h_bShape_inclusive.GetName(), 'inclusive')
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')
if not args.isMC:
    plotting_tools.ratio_plot_CMSstyle(
        h_bShape_etaCat, 
        h_bShape_inclusive, 
        to_ploton       = [l],
        x_lim           = [mass_range_lo, mass_range_hi],
        draw_opt_den    = 'histe',
        draw_opt_num    = 'pe',
        file_name       = plot_name+'_ratio', 
        ratio_w         = 0.08,  
        ratio_yname     = 'cat /incl', 
        CMSextraText    = 'Preliminary' if not args.isMC else 'Simulation Preliminary', 
        isMC            = args.isMC,
        year            = args.year
    )
