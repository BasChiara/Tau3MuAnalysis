import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import math
import argparse
# import custom configurations
import sys
sys.path.append('..')
from mva.config import mass_range_lo, mass_range_hi, cat_selection_dict, cat_color_dict,cat_eta_selection_dict
from plots.plotting_tools import ratio_plot


def draw_by_category(cat_dict, histo_list, histo_inclusive = None):
    c = ROOT.TCanvas('c', '', 800,800) 
    legend = ROOT.TLegend(0.15, 0.70, 0.50, 0.85)
    cat_list = list(cat_dict)
    for i,histo in enumerate(histo_list):
        histo.Draw('hist' + ('same' if i >0 else ''))
        legend.AddEntry(histo.GetName(), f'cat {cat_list[i]}')
    c.Update()
    return c, legend


parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/categorization/', help=' output directory for plots')
parser.add_argument('--tag',        default= '', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('-y', '--year',  choices = ['2022', '2023', 'Run3'], default = '2022',help='which data taking year')
#parser.add_argument('--bdt_cut',    type= float, default = 0.990)

args = parser.parse_args()


tag = ''

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetHistMinimumZero()
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.035)
ROOT.TH1.SetDefaultSumw2()

# import DATA
data_path = '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/'
data_22 = [
    #2022
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root',
]
data_23 = [
    #2023
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023B_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023C_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023D_HLT_overlap.root',
]


if  (args.year == '2022'): data = data_22
elif(args.year == '2023'): data = data_23
#data = ['/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_WTau3Mu_DATA_apply_bkgW3MuNu_LxyS0_2024May01.root']
phi_mass = 1.020 #GeV
phi_window = 0.020 #GeV
phi_veto = '''(fabs(tau_mu12_fitM- {mass:.3f})> {window:.3f} & fabs(tau_mu23_fitM - {mass:.3f})> {window:.3f} & fabs(tau_mu13_fitM -  {mass:.3f})>{window:.3f})'''.format(mass =phi_mass , window = phi_window/2. )
base_selection = f'(tau_fit_mass > {mass_range_lo} & tau_fit_mass < {mass_range_hi} ) & (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu) & {phi_veto}'
print('\n---------------------------------------------')
print('[!] base-selection   : %s'%base_selection)
print('---------------------------------------------\n')

tree_name = 'WTau3Mu_tree'
print(f'[+] adding {args.year} data')
data_rdf = ROOT.RDataFrame(tree_name, data, ['tau_fit_mass', 'tau_fit_mass_resol', 'tau_fit_eta']).Filter(base_selection).Define('tau_fit_absEta', 'fabs(tau_fit_eta)')
print(f'   {data_rdf.Count().GetValue()} entries passed selection')
print('---------------------------------------------')

# divide by mass_resolution
h_bShape = []
h_eta    = []
h_bShape_etaCat = []
h_bShape_inclusive = data_rdf.Histo1D(('h_bShape_incl', '', 10, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr() 
h_bShape_inclusive.Scale(1./h_bShape_inclusive.Integral())
h_bShape_inclusive.SetMaximum(.12)
h_bShape_inclusive.SetMinimum(.08)
h_bShape_inclusive.SetLineColor(ROOT.kBlack)
h_bShape_inclusive.SetMarkerColor(ROOT.kBlack)
h_bShape_inclusive.SetMarkerStyle(20)
h_bShape_inclusive.SetLineWidth(2)
for cat in list(cat_selection_dict):
    # relative mass resolution bkg shape
    h   = data_rdf.Filter(cat_selection_dict[cat]).Histo1D(('h_bShape_%s'%cat, '', 10, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
    h.Scale(1./h.Integral())
    h.SetLineColor(cat_color_dict[cat])
    h.SetMarkerColor(cat_color_dict[cat])
    h.SetMarkerStyle(20)
    h.SetMaximum(.12)
    h.SetMinimum(0.09)
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle('M_{3#mu} (GeV)')
    h_bShape.append(h)
    # relative mass resolution eta
    he   = data_rdf.Filter(cat_selection_dict[cat]).Histo1D(('h_eta_%s'%cat, '', 26, 0, 2.6), 'tau_fit_absEta').GetPtr()
    he.Scale(1./he.Integral())
    he.SetMaximum(.4)
    he.SetLineColor(cat_color_dict[cat])
    he.SetLineWidth(2)
    he.SetMarkerColor(cat_color_dict[cat])
    he.SetMarkerStyle(20)
    he.GetXaxis().SetTitle('#eta_{3#mu}')
    h_eta.append(he)
    # eta based bkg Shape  
    h_be   = data_rdf.Filter(cat_eta_selection_dict[cat]).Histo1D(('h_bShapeEta_%s'%cat, '', 10, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
    h_be.Scale(1./h_be.Integral())
    h_be.SetMaximum(.12)
    h_be.SetMinimum(0.09)
    h_be.SetLineColor(cat_color_dict[cat])
    h_be.SetLineWidth(2)
    h_be.SetMarkerColor(cat_color_dict[cat])
    h_be.SetMarkerStyle(20)
    h_be.GetXaxis().SetTitle('M_{3#mu} (GeV)')
    h_bShape_etaCat.append(h_be)

    
    
    
    
plot_name = f'{args.plot_outdir}/ResolMassCategories_bShape'
c, l = draw_by_category(cat_selection_dict, h_bShape)
l.SetHeader('#sigma_{M}/M categorization')
c.Draw()
h_bShape_inclusive.Draw('same pe')
l.AddEntry(h_bShape_inclusive.GetName(), 'inclusive')
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')

ratio_plot(h_bShape, h_bShape_inclusive, to_ploton = [l], file_name = plot_name+'_ratio', ratio_w = 0.05, ratio_yname = 'cat /incl')


plot_name = f'{args.plot_outdir}/ResolMassCategories_AbsEta'
c, l = draw_by_category(cat_selection_dict, h_eta)
l.SetHeader('#sigma_{M}/M categorization')
c.Draw()
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')

plot_name = f'{args.plot_outdir}/EtaCategories_bShape'
c, l = draw_by_category(cat_selection_dict, h_bShape_etaCat)
l.SetHeader('|#eta| categorization')
c.Draw()
h_bShape_inclusive.Draw('same pe')
l.AddEntry(h_bShape_inclusive.GetName(), 'inclusive')
l.Draw()
c.SaveAs(plot_name+'.png')
c.SaveAs(plot_name+'.pdf')
ratio_plot(h_bShape_etaCat, h_bShape_inclusive, to_ploton = [l], file_name = plot_name+'_ratio', ratio_w = 0.05,  ratio_yname = 'cat /incl')