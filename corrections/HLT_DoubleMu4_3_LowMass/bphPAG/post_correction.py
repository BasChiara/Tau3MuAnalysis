import ROOT
ROOT.gROOT.SetBatch(True)

import cmsstyle as CMS

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import mva.config as config

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'reMini',                          help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,                     help='set it to have useful printout')
parser.add_argument('--year',       choices=['2022preEE', '2022EE','2022', '2023preBPix', '2023BPix','2023', '2024', 'Run3'],       default = '2022', help='year of data-taking')
parser.add_argument('--process',    choices= ['WTau3Mu', 'ZTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'fake_rate'],   help='what process is in the input sample')

args = parser.parse_args()
tag = '_'.join([args.tag, args.year, args.process])

# input DATA and MC
selection   = config.year_selection[args.year] # fixme: add yearID in data
mc_files    = config.mc_samples[args.process]
tree_name   = 'WTau3Mu_tree' if not args.process == 'DsPhiMuMuPi' else 'DsPhiMuMuPi_tree' 
mc_rdf      = ROOT.RDataFrame(tree_name, mc_files)
mc_rdf      = mc_rdf.Filter(selection)

# plot HLT scale factor as funtion of 
var_list = ['tau_fit_pt', 'tau_mu3_pt', 'tau_fit_mass']

sf_nom_branch  = 'tau_DoubleMu4_3_LowMass_SF'
sf_up_branch   = f'{sf_nom_branch}_sysUP'
sf_down_branch = f'{sf_nom_branch}_sysDOWN'

# settings for plotting

legend = CMS.cmsLeg(0.6, 0.70, 0.85, 0.85)
CMS.SetLumi(f'{args.year}, {config.LumiVal_plots[args.year]}')
CMS.SetEnergy("13.6")
# Write extra lines below the extra text (usuful to define regions/channels)
CMS.ResetAdditionalInfo()
#CMS.AppendAdditionalInfo("Signal region")
#CMS.AppendAdditionalInfo("#mu-channel")

for var in var_list:
    
    h_nominal = mc_rdf.Profile1D(('h_nominal', 'h_nominal', config.features_NbinsXloXhiLabelLog[var][0], config.features_NbinsXloXhiLabelLog[var][1], config.features_NbinsXloXhiLabelLog[var][2]), var, sf_nom_branch ).GetPtr()
    h_up = mc_rdf.Profile1D(('h_up', 'h_up', config.features_NbinsXloXhiLabelLog[var][0], config.features_NbinsXloXhiLabelLog[var][1], config.features_NbinsXloXhiLabelLog[var][2]), var, sf_up_branch ).GetPtr()
    h_down = mc_rdf.Profile1D(('h_down', 'h_down', config.features_NbinsXloXhiLabelLog[var][0], config.features_NbinsXloXhiLabelLog[var][1], config.features_NbinsXloXhiLabelLog[var][2]), var, sf_down_branch ).GetPtr()
    

    canv = CMS.cmsCanvas(
            'canv',
            config.features_NbinsXloXhiLabelLog[var][1], config.features_NbinsXloXhiLabelLog[var][2], 
            0.75, 1.25,
            config.features_NbinsXloXhiLabelLog[var][3], 'HLT_DoubleMu4_3_LowMass SF',
            square=True,
            extraSpace=0.01,
            iPos=11,
    )
    
    CMS.cmsDraw(h_nominal, "PE", mcolor=ROOT.kBlack)
    legend.AddEntry(h_nominal, 'Nominal SF', 'lp')
    CMS.cmsDraw(h_up, "PE", mcolor=ROOT.kRed)
    legend.AddEntry(h_up, 'SF + sys', 'lp')
    CMS.cmsDraw(h_down, "PE", mcolor=ROOT.kBlue)
    legend.AddEntry(h_down, 'SF - sys', 'lp')
    
    legend.Draw()
    CMS.SaveCanvas(canv, f'./test_{var}_{tag}.png', False)
    CMS.SaveCanvas(canv, f'./test_{var}_{tag}.pdf', True)

    legend.Clear()