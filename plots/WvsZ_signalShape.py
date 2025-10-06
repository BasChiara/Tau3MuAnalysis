import ROOT
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config

W_wspace_file = "/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/categ_number/input_combine/wspace_etaBinning_bdt0.9900_WTau3Mu_22_NOsplit.root"
Z_wspace_file = "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/models/workspaces/wspace_etaBinning_bdt0.9900_WTau3Mu_22_Ztautau.root"
# open W and Z files
if not os.path.isfile(W_wspace_file):
    print(f"Error: file {W_wspace_file} not found")
    exit(1)
if not os.path.isfile(Z_wspace_file):
    print(f"Error: file {Z_wspace_file} not found")
    exit(1)

W_file = ROOT.TFile.Open(W_wspace_file)
Z_file = ROOT.TFile.Open(Z_wspace_file)

w_space_names = {
    'A' : "wspace_WTau3Mu_bdt0.9900_A022_etaAB0.0_BC0.9",
    'B' : "wspace_WTau3Mu_bdt0.9900_B022_etaAB0.9_BC1.8",
    'C' : "wspace_WTau3Mu_bdt0.9900_C022_etaAB1.8_BC2.5"
}

year = '22'

plot_dir = "/eos/user/c/cbasile/www/Tau3Mu_Run3/Ztautau/sensitivity/"

widths = []
means = []
for cat in config.cat_eta_selection_dict:
    if cat == 'ABC' : continue
    print(f'** category {cat} **')
    ws_W = W_file.Get(w_space_names[cat])
    ws_Z = Z_file.Get(w_space_names[cat])

    W_width =  ws_W.var(f'width_{cat}{year}')
    W_mean  =  ws_W.var(f'dM')
    Z_width =  ws_Z.var(f'width_{cat}0{year}')
    Z_mean  =  ws_Z.var(f'dM')

    print(f'W: width = {W_width.getVal():.3f} +/- {W_width.getError():.3f}')
    print(f'W: mass  = {W_mean.getVal():.3f} +/- {W_mean.getError():.3f}')
    print(f'Z: width = {Z_width.getVal():.3f} +/- {Z_width.getError():.3f}')
    print(f'Z: mass  = {Z_mean.getVal():.3f} +/- {Z_mean.getError():.3f}')

    widths.append([W_width, Z_width])
    means.append([W_mean, Z_mean])
pull_width = [ (w[0].getVal() - w[1].getVal())*1000 for w in widths ]
pull_mean  = [ (m[0].getVal() - m[1].getVal())*1000 for m in means ]

import matplotlib.pyplot as plt
# plot widths w/ pulls
fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]}, tight_layout=True)
ax[0].set_ylabel(r'width m$_{3\mu}$ (MeV)', fontsize=20)
ax[1].set_ylabel('difference (MeV)', fontsize=20)
plt.xticks(range(3), ['A', 'B', 'C'], fontsize=20)
ax[0].errorbar(range(3), [w[0].getVal()*1000 for w in widths], yerr=[w[0].getError()*1000 for w in widths], fmt='o', label=r'$W\rightarrow \tau(3\mu)\nu$', color='r')
ax[0].errorbar(range(3), [w[1].getVal()*1000 for w in widths], yerr=[w[1].getError()*1000 for w in widths], fmt='o', label=r'$Z\rightarrow \tau(3\mu)\tau$', color='g')
ax[0].legend(loc='upper left', fontsize=20)
ax[0].grid()
ax[1].axhline(0, color='black', linestyle='--') 
ax[1].errorbar(range(3), pull_width, fmt='o', color='k')
ax[1].grid()
ax[1].set_ylim(-1.0, 1.0)
ax[0].tick_params(axis='y', labelsize=16)
ax[1].tick_params(axis='y', labelsize=16)
plt.savefig(f'{plot_dir}/WvsZ_widths.png')
plt.savefig(f'{plot_dir}/WvsZ_widths.pdf')


# plot mass shifts
fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]}, tight_layout=True)
ax[0].set_ylabel(r'mean m$_{3\mu}$ (MeV)', fontsize=20)
ax[1].set_ylabel('difference (MeV)', fontsize=20)
ax[0].errorbar(range(3), [m[0].getVal()*1000 for m in means], yerr=[m[0].getError()*1000 for m in means], fmt='o', label=r'$W\rightarrow \tau(3\mu)\nu$', color='r')
ax[0].errorbar(range(3), [m[1].getVal()*1000 for m in means], yerr=[m[1].getError()*1000 for m in means], fmt='o', label=r'$Z\rightarrow \tau(3\mu)\tau$', color='g')
plt.xticks(range(3), ['A', 'B', 'C'], fontsize=20)
ax[0].legend(loc='upper left', fontsize=20 )
ax[0].grid()
ax[1].axhline(0, color='black', linestyle='--')
ax[1].errorbar(range(3), pull_mean, fmt='o', color='k')
ax[1].grid()
ax[1].set_ylim(-1.0, 1.0)
ax[0].tick_params(axis='y', labelsize=16)
ax[1].tick_params(axis='y', labelsize=16)
plt.savefig(f'{plot_dir}/WvsZ_means.png')
plt.savefig(f'{plot_dir}/WvsZ_means.pdf')
