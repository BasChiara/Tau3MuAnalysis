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
parser.add_argument('--category',                                   default = 'noCat',help='category to be used')
parser.add_argument('--year',       choices=['2022', '2023', 'Run3'],       default = '2022', help='year of data-taking')
parser.add_argument('--process',    choices= ['WTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'fake_rate'],   help='what process is in the input sample')

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
vars = ['W_pt', 'W_eta_min', 'W_eta_min', 'tau_fit_pt', 'tau_fit_eta', 'tau_fit_mass']
labels = ['p_{T}(W) (GeV)', '#eta(W)_{min}', '#eta(W)_{min}', 'p_T(3#mu) (GeV)', '#eta(3#mu)', 'M(3#mu) (GeV)']
labels = dict(zip(vars, labels))
vars_bins = {
    'W_pt'        : [30, 0, 150],
    'W_eta_min'   : [35, -3.5, 3.5],
    'W_eta_min'   : [35, -3.5, 3.5],
    'tau_fit_pt'  : [50, 0, 100],
    'tau_fit_eta' : [35, -3.5, 3.5],
    'tau_fit_mass': [40, config.mass_range_lo, config.mass_range_hi],
}
legend = CMS.cmsLeg(0.6, 0.7, 0.85, 0.85)
for var in vars:
    h_data          = data_rdf.Histo1D((f'{var}_data', f'{var}_data', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_noWeights  = mc_rdf.Histo1D((f'{var}_mc_noWeights', f'{var}_mc_noWeights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_weights    = mc_rdf.Histo1D((f'{var}_mc_weights', f'{var}_mc_weights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var, 'NLO_weight').GetPtr()

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerStyle(20)
    h_mc_noWeights.SetLineColor(ROOT.kRed)
    h_mc_noWeights.SetLineWidth(2)
    h_mc_weights.SetLineColor(ROOT.kBlue)
    h_mc_weights.SetLineWidth(2)
    h_mc_noWeights.GetXaxis().SetTitle(labels[var])

    legend.AddEntry(h_mc_noWeights, 'MC', 'l')
    legend.AddEntry(h_mc_weights, 'MC NLO re-weight', 'l')
    # MC only pre/post PU weights
    plotting_tools.ratio_plot_CMSstyle(
        histo_num = [h_mc_weights],
        histo_den = h_mc_noWeights,
        draw_opt_num = 'hist',
        draw_opt_den = 'hist',
        ratio_w = 2.0 if ('pt' in var) else 0.5,
        ratio_yname = 'post/pre',
        year = args.year,
        to_ploton=[legend],
        file_name = f'{args.plot_outdir}/{var}_MConly_{args.process}_{args.year}_{tag}',
        isMC = True,
    )
    legend.Clear()
    continue
    # DATA vs MC
    h_data.Scale(1./h_data.Integral())
    h_mc_noWeights.Scale(1./h_mc_noWeights.Integral())
    h_mc_weights.Scale(1./h_mc_weights.Integral())
    # pre PU weights
    legend.AddEntry(h_mc_noWeights, 'MC', 'l')
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
    legend.AddEntry(h_mc_weights, 'MC NLO re-weight', 'l')
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

