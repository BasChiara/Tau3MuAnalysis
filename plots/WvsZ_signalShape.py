import ROOT
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config

W_wspace_file = "/afs/cern.ch/user/c/cbasile/Combine_v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/categ_number/input_combine/wspace_etaBinning_bdt0.9900_WTau3Mu_22_NOsplit.root"
Z_wspace_file = "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/models/wspace_etaBinning_bdt0.9900_WTau3Mu_22_Ztautau.root"
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
mass_shifts = []

for cat in config.cat_eta_selection_dict:
    print(f'** category {cat} **')
    ws_W = W_file.Get(w_space_names[cat])
    ws_Z = Z_file.Get(w_space_names[cat])

    W_width =  ws_W.var(f'width_{cat}{year}')
    W_mass_shift =  ws_W.var(f'dM')
    Z_width =  ws_Z.var(f'width_{cat}{year}')
    Z_mass_shift =  ws_Z.var(f'dM')

    print(f'W: width = {W_width.getVal()} +/- {W_width.getError()}')
    print(f'W: mass shift = {W_mass_shift.getVal()} +/- {W_mass_shift.getError()}')
    print(f'Z: width = {Z_width.getVal()} +/- {Z_width.getError()}')
    print(f'Z: mass shift = {Z_mass_shift.getVal()} +/- {Z_mass_shift.getError()}')

    widths.append([W_width, Z_width])
    mass_shifts.append([W_mass_shift, Z_mass_shift])

import matplotlib.pyplot as plt
# plot widths
plt.figure()
plt.title('W vs Z signal parameters')
plt.ylabel(r'signal width $\sigma_S$ (MeV)', fontsize=14)
plt.xticks(range(3), ['A', 'B', 'C'], fontsize=14)
plt.errorbar(range(3), [w[0].getVal()*1000 for w in widths], yerr=[w[0].getError()*1000 for w in widths], fmt='o', label='W')
plt.errorbar(range(3), [w[1].getVal()*1000 for w in widths], yerr=[w[1].getError()*1000 for w in widths], fmt='o', label='Z')
plt.legend()
plt.grid()
plt.savefig(f'{plot_dir}/WvsZ_widths.png')
plt.savefig(f'{plot_dir}/WvsZ_widths.pdf')
# plot mass shifts
plt.figure()
plt.title('W vs Z signal parameters')
plt.ylabel(r'mass shift $\Delta m$ (MeV)', fontsize=14)
plt.xticks(range(3), ['A', 'B', 'C'], fontsize=14)
plt.errorbar(range(3), [m[0].getVal()*1000 for m in mass_shifts], yerr=[m[0].getError()*1000 for m in mass_shifts], fmt='o', label='W')
plt.errorbar(range(3), [m[1].getVal()*1000 for m in mass_shifts], yerr=[m[1].getError()*1000 for m in mass_shifts], fmt='o', label='Z')
plt.legend()
plt.grid()
plt.savefig(f'{plot_dir}/WvsZ_mass_shifts.png')
plt.savefig(f'{plot_dir}/WvsZ_mass_shifts.pdf')
