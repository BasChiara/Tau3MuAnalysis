import ROOT
import os
import sys
import numpy as np
import argparse
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import mva.config as cfg


def double_gaussian_width(w1, w2, frac, MeV = True):
    
    return np.sqrt((w1 * frac)**2 + (w2 * (1-frac))**2) * (1000 if MeV else  1)

argparser = argparse.ArgumentParser()
argparser.add_argument('-y', '--year', choices = [2022, 2023], type=int, default=2022, help='Year of the data taking period')
args = argparser.parse_args()

wspace_byCat = {}
if args.year == 2022:
    wspace_byCat ={
        "A22" : '../../models/workspaces/DsPhiPi_wspace_catA2022_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
        "B22" : '../../models/workspaces/DsPhiPi_wspace_catB2022_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
        "C22" : '../../models/workspaces/DsPhiPi_wspace_catC2022_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
    }
elif args.year == 2023:
    wspace_byCat ={
        "A23" : '../../models/workspaces/DsPhiPi_wspace_catA2023_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
        "B23" : '../../models/workspaces/DsPhiPi_wspace_catB2023_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
        "C23" : '../../models/workspaces/DsPhiPi_wspace_catC2023_HLT_overlap_LxyS2.1_HLTsf_2024Jul11.root',
    }
else:
    print('Year not supported')
    sys.exit(1)


# get the mc/data workspace
data_wspace = 'DsPhiPi_data_wspace'
mc_wspace   = 'DsPhiPi_mc_wspace'
data_width, data_mean = [], []
mc_width, mc_mean     = [], []
for cat in wspace_byCat:
    print(f' ---- category: {cat} ----')
    f = ROOT.TFile.Open(wspace_byCat[cat])
    # mc
    w_mc = f.Get(mc_wspace)
    mean = getattr(w_mc['mean_mc'], 'evaluate')()
    width = double_gaussian_width(getattr(w_mc['width1_mc'], 'getVal')(), getattr(w_mc['width2_mc'], 'getVal')(), getattr(w_mc['gfrac'], 'getVal')())
    print(f'[MC] mean: {mean:.3f} width: {width:.6f}')
    mc_mean.append(mean)
    mc_width.append(width)
    # data
    w_data = f.Get(data_wspace)
    mean = getattr(w_data['mean_mc'], 'evaluate')()
    width = double_gaussian_width(getattr(w_data['width1'], 'getVal')(), getattr(w_data['width2'], 'getVal')(), getattr(w_data['gfrac'], 'getVal')())
    print(f'[Data] mean: {mean:.3f} width: {width:.6f}')
    data_mean.append(mean)
    data_width.append(width)
    f.Close()
    print('\n')
# save the systematic uncertainty in json file
mean_ratio = np.divide(data_mean, mc_mean)
width_ratio = np.divide(data_width, mc_width)
sys_dict = {}
for i, cat in enumerate(wspace_byCat.keys()):
    sys_dict[cat] = {
        'mean':  mean_ratio[i],
        'width': width_ratio[i],
    } 
with open(f'signal_shape_comparison_{args.year}.json', 'w') as f:
    json.dump(sys_dict, f)
print(f'[o] json file with systematic uncertainty saved as signal_shape_comparison_{args.year}.json')


# comparison plot data/mc with ratio plot
import matplotlib.pyplot as plt
# pads for direct comparison and ratio plot
fig, ax = plt.subplots(nrows=2, ncols=2, 
                       gridspec_kw={'height_ratios':[2,1]}, figsize=(10, 5))
plt.tight_layout()
# no space between upper and lower plots
plt.subplots_adjust(hspace=0.0, wspace=0.4,
                    left=0.1, right=0.9, top=0.9, bottom=0.1)

label_fontsize = 14
ticks_fontsize = 12

# calculate the ratio of data to mc mean/width
mean_ratio  = np.abs(mean_ratio  - 1 ) * 100
width_ratio = np.abs(width_ratio - 1 ) * 100

# plot the data ans mc mean/ width
ax[0,0].grid(zorder = 1, linestyle='--')
ax[0,0].scatter(wspace_byCat.keys(), data_mean, c='b', label='Data', zorder=2)
ax[0,0].scatter(wspace_byCat.keys(), mc_mean, c='r', label='MC', zorder = 3)
ax[0,0].set_ylabel('Mean (GeV)', fontsize=label_fontsize)
ax[0,0].set_ylim(cfg.Ds_mass - 0.005, cfg.Ds_mass + 0.005)
ax[0,0].tick_params(axis='both', labelsize=ticks_fontsize)

ax[0,1].grid(zorder = 1, linestyle='--')
ax[0,1].scatter(wspace_byCat.keys(), data_width, c='b', label='Data', zorder = 2)
ax[0,1].scatter(wspace_byCat.keys(), mc_width, c='r', label='MC', zorder = 3)
ax[0,1].set_ylabel('Width (MeV)', fontsize=label_fontsize)
ax[0,1].set_ylim(5.0, 25.0)
ax[0,1].tick_params(axis='both', labelsize=ticks_fontsize)


# plot the ratio of data to mc mean/width
ax[1,0].grid(zorder = 0, linestyle='--')
ax[1,0].scatter(wspace_byCat.keys(), mean_ratio, c='k', zorder=2)
ax[1,0].set_ylabel('|Data/MC - 1| (%)', fontsize=label_fontsize, labelpad=15)
ax[1,0].set_ylim(0.6*np.min(mean_ratio), 1.6*np.max(mean_ratio))
ax[1,0].tick_params(axis='both', labelsize=ticks_fontsize)

ax[1,1].grid(zorder = 0, linestyle='--')
ax[1,1].scatter(wspace_byCat.keys(), width_ratio, c='k', zorder=2)
ax[1,1].set_ylabel('|Data/MC - 1| (%)', fontsize=label_fontsize, labelpad=25)
ax[1,1].set_ylim(0.1*np.min(width_ratio), 1.6*np.max(width_ratio))
ax[1,1].tick_params(axis='both', labelsize=ticks_fontsize)


# Add a legend to the plot
ax[0,0].legend(loc = 'upper left', fontsize=label_fontsize, frameon=False)
ax[0,1].legend(loc = 'upper left', fontsize=label_fontsize, frameon=False)

# Adjust the layout of the subplots

plt.savefig(f'signal_shape_comparison_{args.year}.png')
plt.savefig(f'signal_shape_comparison_{args.year}.pdf')

