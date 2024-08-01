import ROOT
from array import array 
import math
import argparse
import sys
sys.path.append('../../')
import mva.config as config
import plots.plotting_tools as plotting_tools

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'reMini',                          help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,                     help='set it to have useful printout')
parser.add_argument('--category',                                   default = 'noCat',help='category to be used')
parser.add_argument('--year',       choices=['2022', '2023'],       default = '2022', help='year of data-taking')
parser.add_argument('--process',    choices= ['WTau3Mu', 'W3MuNu', 'data', 'DsPhiMuMuPi', 'fake_rate'],   help='what process is in the input sample')

args = parser.parse_args()
tag = args.tag

print('\n')

# input DATA and MC
mc_files   = config.mc_samples[args.process]
data_files = config.data_samples[args.process]
tree_name = 'WTau3Mu_tree' if not args.process == 'DsPhiMuMuPi' else 'DsPhiMuMuPi_tree' 
mc_rdf      = ROOT.RDataFrame(tree_name, mc_files)
data_rdf    = ROOT.RDataFrame(tree_name, data_files)

# plot variables with PU weights
vars = ['nGoodPV']
#vars = ['W_pt']
vars_bins = {
    'nGoodPV': [30, 0, 60],
    'W_pt': [40, 0, 100],
}
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for var in vars:
    h_data          = data_rdf.Histo1D((f'{var}_data', f'{var}_data', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_noWeights  = mc_rdf.Histo1D((f'{var}_mc_noWeights', f'{var}_mc_noWeights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var).GetPtr()
    h_mc_weights    = mc_rdf.Histo1D((f'{var}_mc_weights', f'{var}_mc_weights', vars_bins[var][0], vars_bins[var][1], vars_bins[var][2]), var, 'PU_weight').GetPtr()

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerStyle(20)
    h_mc_noWeights.SetLineColor(ROOT.kRed)
    h_mc_weights.SetLineColor(ROOT.kBlue)

    legend.AddEntry(h_data, 'data', 'l')
    legend.AddEntry(h_mc_noWeights, 'MC no PU weights', 'l')
    legend.AddEntry(h_mc_weights, 'MC with PU weights', 'l')

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
    
    h_data.Scale(1./h_data.Integral())
    h_mc_noWeights.Scale(1./h_mc_noWeights.Integral())
    h_mc_weights.Scale(1./h_mc_weights.Integral())
    plotting_tools.ratio_plot_CMSstyle(
        histo_num = [h_mc_noWeights, h_mc_weights],
        histo_den = h_data,
        draw_opt_num = 'hist',
        draw_opt_den = 'pe0',
        ratio_w = 0.5,
        ratio_yname = 'MC/Data',
        year = args.year,
        file_name = f'{args.plot_outdir}/{var}_{args.process}_{args.year}_{tag}',
    )

