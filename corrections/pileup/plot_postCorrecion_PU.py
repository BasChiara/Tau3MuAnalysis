import ROOT
from array import array 
import math
import argparse
import sys
import cmsstyle as CMS
sys.path.append('../../')
import mva.config as config
import plots.plotting_tools as plotting_tools

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'reMini',                          help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,                     help='set it to have useful printout')
parser.add_argument('--year',       choices=['2022preEE', '2022EE','2022', '2023preBPix', '2023BPix','2023', '2024', 'Run3'],       default = '2022', help='year of data-taking')
parser.add_argument('--process',    choices= ['WTau3Mu', 'ZTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'fake_rate'],   help='what process is in the input sample')

args = parser.parse_args()
tag = args.tag

print('\n')

# input DATA and MC
selection   = config.year_selection[args.year] # fixme: add yearID in data
mc_files    = config.mc_samples[args.process]
data_files  = config.data_samples[args.process]
tree_name   = 'WTau3Mu_tree' if not args.process == 'DsPhiMuMuPi' else 'DsPhiMuMuPi_tree' 
mc_rdf      = ROOT.RDataFrame(tree_name, mc_files)
data_rdf    = ROOT.RDataFrame(tree_name, data_files)

# plot variables with PU weights
vars = ['nGoodPV', 'Rho_Fj', 'W_pt']
labels = ['reco PV multiplicity', 'Fastjet #rho', 'W p_{T} [GeV]']
labels = dict(zip(vars, labels))
vars_bins = {
    'nGoodPV': [35, 0, 70],
    'Rho_Fj': [35, 0, 70],
    'W_pt': [40, 0, 100],
}
legend = CMS.cmsLeg(0.6, 0.7, 0.85, 0.85)
for var in vars:
    h_data          = data_rdf.Filter(selection).Histo1D((f'{var}_data', f'{var}_data', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_noWeights  = mc_rdf.Filter(selection).Histo1D((f'{var}_mc_noWeights', f'{var}_mc_noWeights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_weights    = mc_rdf.Filter(selection).Histo1D((f'{var}_mc_weights', f'{var}_mc_weights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var, 'PU_weight').GetPtr()

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerStyle(20)
    h_mc_noWeights.GetXaxis().SetTitle(labels[var])
    h_mc_noWeights.SetLineColor(ROOT.kRed)
    h_mc_noWeights.SetLineWidth(2)
    h_mc_weights.GetXaxis().SetTitle(labels[var])
    h_mc_weights.SetLineColor(ROOT.kBlue)
    h_mc_weights.SetLineWidth(2)

    legend.AddEntry(h_mc_noWeights, 'MC no PU weights', 'l')
    legend.AddEntry(h_mc_weights, 'MC with PU weights', 'l')
    # MC only pre/post PU weights
    plotting_tools.ratio_plot_CMSstyle(
        histo_num = [h_mc_weights],
        histo_den = h_mc_noWeights,
        draw_opt_num = 'hist',
        draw_opt_den = 'hist',
        ratio_w = 0.5,
        ratio_yname = 'post/pre PU weights',
        year = args.year,
        to_ploton=[legend],
        file_name = f'{args.plot_outdir}/{var}_MConly_{args.process}_{args.year}_{tag}',
    )
    legend.Clear()
    # DATA vs MC
    h_data.Scale(1./h_data.Integral())
    h_mc_noWeights.Scale(1./h_mc_noWeights.Integral())
    h_mc_weights.Scale(1./h_mc_weights.Integral())
    # pre PU weights
    legend.AddEntry(h_mc_noWeights, 'MC no PU weights', 'l')
    legend.AddEntry(h_data, 'data', 'pe')
    plotting_tools.ratio_plot_CMSstyle(
        histo_num = [h_data],
        histo_den = h_mc_noWeights,
        draw_opt_num = 'pe0',
        draw_opt_den = 'hist',
        ratio_w = 0.5,
        ratio_yname = 'Data/MC',
        year = args.year,
        to_ploton=[legend],
        file_name = f'{args.plot_outdir}/{var}_preCorr_{args.process}_{args.year}_{tag}',
    )
    legend.Clear()
    # post PU weights
    legend.AddEntry(h_mc_weights, 'MC with PU weights', 'l')
    legend.AddEntry(h_data, 'data', 'pe')
    plotting_tools.ratio_plot_CMSstyle(
        histo_num = [h_data],
        histo_den = h_mc_weights,
        draw_opt_num = 'pe0',
        draw_opt_den = 'hist',
        ratio_w = 0.5,
        ratio_yname = 'Data/MC',
        year = args.year,
        to_ploton=[legend],
        file_name = f'{args.plot_outdir}/{var}_{args.process}_{args.year}_{tag}',
    )
    legend.Clear()
