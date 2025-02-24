import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import numpy as np
import argparse

import os
import sys
sys.path.append('../../..')
import mva.config as config
import plots.plotting_tools as plotting_tools

SYS_FROM_CUTNCOUNT = True
VERBOSE = False

def histo_style(h, color):
    yaxis = h.GetYaxis()
    yaxis.SetTitle('Efficiency')
    yaxis.SetTitleOffset(1.3)
    yaxis.SetTitleSize(0.06)
    yaxis.SetLabelSize(0.05)
    yaxis.SetRangeUser(0, 1.2)

    h.SetTitle('')
    h.SetMarkerColor(color)
    h.SetMarkerStyle(20)
    h.SetMarkerSize(0.5)
    h.SetLineColor(color)
    h.SetLineWidth(2)

    return h

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('--input', 
                    dest='input', 
                    help='input root file', 
                    default=None)
parser.add_argument('--output', 
                    dest='output', 
                    help='output root file', 
                    default=None)
parser.add_argument('--cut_ncount', 
                    dest='cut_ncount', 
                    help='cutNcount root file', 
                    default=None)
parser.add_argument('--trigger', 
                    dest='trigger',
                    choices=['L1', 'HLT'],
                    help='choose trigger', 
                    default='L1')
parser.add_argument('--year',
                    choices=['2022', '2023'],
                    help='year of the data taking',
                    )
parser.add_argument('--sysname', 
                    dest='sysname', 
                    help='the systematic name', 
                    default='sys')
args = parser.parse_args()

if not args.input:
    print("No input file specified")
    sys.exit(1)

base_name_L1 = f'NUM_HLT_Mu0_L1DoubleMu_DEN_HLT_Mu8_abseta_pt'
base_name_HLT = f'NUM_HLT_DoubleMu4_3_LowMass_DEN_HLT_Mu4_L1DoubleMu_abseta_pt'
histogram_names ={
    'L1' :{
        'mc'   : f'{base_name_L1}_efficiencyMC',
        'data' : f'{base_name_L1}_efficiencyData',
        'sys'  : f'{base_name_L1}_efficiencyData_{args.sysname}'
    },
    'HLT' :{
        'mc'   : f'{base_name_HLT}_efficiencyMC',
        'data' : f'{base_name_HLT}_efficiencyData',
        'sys'  : f'{base_name_HLT}_efficiencyData_{args.sysname}'
    },
}

tester = [0.6, 10.5] #eta, pt
faulty_bin = [1.0, 2.5]

file = ROOT.TFile.Open(args.input)
efficiency_mc = file.Get(histogram_names[args.trigger]['mc'])
ROOT.gDirectory.Get('efficiency_mc')
efficiency_mc.SetName(f'{args.trigger}_MCefficiency')
efficiency_data = file.Get(histogram_names[args.trigger]['data'])
ROOT.gDirectory.Get('efficiency_data')
efficiency_data.SetName(f'{args.trigger}_DATAefficiency_statOnly')
syst = file.Get(histogram_names[args.trigger]['sys'])
ROOT.gDirectory.Get('syst')
syst.SetName(f'{args.trigger}_DATAefficiency_{args.sysname}')

# clone efficiency histogram
eff_sys = efficiency_data.Clone(f'{args.trigger}_DATAefficiency_sysOnly')
eff_sys.SetDirectory(0)
eff_total = efficiency_data.Clone(f'{args.trigger}_DATAefficiency')
eff_total.SetDirectory(0)


# test if the bin is in the range
print(f' test eta = {tester[0]} pt = {tester[1]}')
print(f'   eff-data = {efficiency_data.GetBinContent(efficiency_data.FindFixBin(tester[0], tester[1])):.3f} +/- {efficiency_data.GetBinError(efficiency_data.FindFixBin(tester[0], tester[1])):.3f}')
print(f'   eff-mc = {efficiency_mc.GetBinContent(efficiency_mc.FindFixBin(tester[0], tester[1])):.3f} +/- {efficiency_mc.GetBinError(efficiency_mc.FindFixBin(tester[0], tester[1])):.3f}')
print(f'   syst = {syst.GetBinContent(syst.FindFixBin(tester[0], tester[1])):.3f} +/- {syst.GetBinError(syst.FindFixBin(tester[0], tester[1])):.3f}')


if SYS_FROM_CUTNCOUNT:
    # get the cutNcount efficiency
    cutNcount_filename = os.path.abspath(args.cut_ncount)
    cutNcount_file = ROOT.TFile.Open(cutNcount_filename)
    efficiency_cnc = cutNcount_file.Get(histogram_names[args.trigger]['data'])
    efficiency_cnc.SetDirectory(0)
    cutNcount_file.Close()

    cnc_syst = efficiency_data.Clone(f'{args.trigger}_DATAefficiency_cnc')

# loop over bins
for i in range(1, eff_sys.GetNbinsX()+1):
    for j in range(1, eff_sys.GetNbinsY()+1):

        eta = eff_sys.GetXaxis().GetBinCenter(i)
        pt = eff_sys.GetYaxis().GetBinCenter(j)
        bin = efficiency_data.FindFixBin(eta, pt) 
        if VERBOSE :print(f' eta = {eta:.1f}  --- pt = {pt:.2f}')
        
        stat_unc = efficiency_data.GetBinError(bin)
        # systtematic uncertainty
        if SYS_FROM_CUTNCOUNT:
            cnc_diff = np.abs(efficiency_cnc.GetBinContent(bin) - efficiency_data.GetBinContent(bin))
            cnc_syst.SetBinError(i, j, 0)
            cnc_syst.SetBinError(i, j, cnc_diff)
        else : cnc_diff = 0
        syst_unc  = np.sqrt(syst.GetBinError(bin)**2 + cnc_diff**2)
        total_unc = np.sqrt(stat_unc**2 + syst_unc**2)
        if VERBOSE :print(f'   stat = {stat_unc:.3f} \t syst = {syst_unc:.3f} total = {total_unc:.3f}')

        # canacel the bin errror and set the new one
        eff_sys.SetBinError(i, j, 0)
        eff_sys.SetBinError(i, j, syst.GetBinError(bin))
        eff_total.SetBinError(i, j, 0)
        eff_total.SetBinError(i, j, total_unc)


# plot with breakdown of the uncertainties
# . slice over eta
for i in range(1, eff_total.GetNbinsX()+1):
    
    # MC
    bin_mc = efficiency_mc.ProjectionY(f'proj_abseta_{i}_mc', i, i)
    bin_mc = histo_style(bin_mc, ROOT.kBlue)
    # DATA
    bin_eff_total = eff_total.ProjectionY(f'proj_abseta_{i}', i, i)
    bin_eff_total = histo_style(bin_eff_total, ROOT.kBlack)

    bin_eff_syst = eff_sys.ProjectionY(f'proj_abseta_{i}_syst', i, i)
    bin_eff_syst = histo_style(bin_eff_syst, ROOT.kRed)

    if SYS_FROM_CUTNCOUNT:
        bin_cnc = cnc_syst.ProjectionY(f'proj_abseta_{i}_cnc', i, i)
        bin_cnc = histo_style(bin_cnc, ROOT.kGreen +2)

    # TEXT
    x_text = 0.65
    y_text, delta = 0.80, 0.05
    # text with eta range
    eta_min, eta_max = eff_total.GetXaxis().GetBinLowEdge(i), eff_total.GetXaxis().GetBinUpEdge(i)
    eta_text = ROOT.TLatex(x_text, y_text, f'{eta_min:.1f} < |#eta| < {eta_max:.1f}')
    eta_text.SetTextFont(42)
    eta_text.SetNDC()
    eta_text.SetTextSize(0.04)
    # text with trigger
    trigger_text = ROOT.TLatex(x_text, y_text+1*delta, f'{args.trigger}')
    trigger_text.SetTextFont(42)
    trigger_text.SetNDC()
    trigger_text.SetTextSize(0.04)

    out_name = f'{os.path.dirname(args.output)}/plots/abseta_{i}_{args.trigger}efficiency'
    print(f'Saving plot {out_name}')

    plotting_tools.plot_CMSstle(
        histo=[bin_eff_total, bin_cnc, bin_eff_syst, bin_mc],
        description=[f'data tot unc', f'data cut&count sys.', 'data bkg-fit sys.', 'MC'],
        leg_coord=[0.50, 0.15, 0.80, 0.45],
        year=args.year,
        y_lim = [0, 1.3],
        file_name= out_name,
        to_ploton=[eta_text, trigger_text],
        draw_opt='PE1',
    )
    # plot with ratio
    plotting_tools.ratio_plot_CMSstyle(
        histo_num=[bin_eff_total, bin_cnc, bin_eff_syst],
        histo_den=bin_mc,
        description=[f'data tot unc', f'data cut&count sys.', 'data bkg-fit sys.', 'MC'],
        leg_coord=[0.50, 0.15, 0.80, 0.45],
        draw_opt_num='PE1',
        draw_opt_den='PE1',
        year = args.year,
        file_name= out_name+'_ratio',
        y_lim = [0, 1.3],
        x_lim=[0,50],
        to_ploton=[eta_text, trigger_text],
        draw_opt='PE1',
    )


# write the new histogram
output_file = ROOT.TFile(args.output, 'RECREATE')
eff_total.Write() # total uncertainty
eff_sys.Write() # syst only
if SYS_FROM_CUTNCOUNT: cnc_syst.Write() # cnc only
efficiency_data.Write() # stat only
efficiency_mc.Write()
output_file.Close()
print(f'New histogram written to {args.output}')

## plot scale factor in the ntuples
pT_bins  = ROOT.std.vector('double')([0,10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 60, 100])

data_rdf = ROOT.RDataFrame('WTau3Mu_tree', config.mc_samples['WTau3Mu'])
data_rdf = data_rdf.Filter(config.year_selection[args.year])
profile_list = []
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]
for i, val in enumerate(['', '_sysUP', '_sysDOWN']):
    
    histo2D = data_rdf.Histo2D(
        ('scale_factor', 'scale_factor', 
        len(pT_bins)-1, pT_bins.data(), 10, 0.8, 1.2), 
        'tau_fit_pt', 'tau_DoubleMu4_3_LowMass_SF'+val    
    ).GetValue()
    profile = histo2D.ProfileX(f'tau_DoubleMu4_3_LowMass_SF'+val)
    profile.SetLineColor(colors[i])
    profile.SetMarkerColor(colors[i])
    profile.SetMarkerStyle(20 if i == 0 else 24)
    profile.SetLineStyle(1 if i == 0 else 2)
    profile_list.append(profile)


out_name = f'Run{args.year}/plots/tau_DoubleMu4_3_LowMass_SF'
plotting_tools.plot_CMSstle(
    histo=profile_list,
    description=['Nominal', '+ sys', '- sys'],
    draw_opt='PE1',
    year=args.year,
    y_lim = [0.7, 1.1],
    y_label='HLT_DoubleMu4_3_LowMass SF',
    x_label='p_{T}(3#mu) [GeV]',
    file_name= out_name,
    leg_coord=[0.50, 0.15, 0.80, 0.40],
)









