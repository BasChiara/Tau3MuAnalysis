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
tag = 'LxyS2.0_2024Jul16'
tag = 'reviewANv3'
if args.year == 2022:
    wspace_byCat ={
        "A22" : f'../../models/workspaces/DsPhiPi_wspace_catA2022_{tag}.root',
        "B22" : f'../../models/workspaces/DsPhiPi_wspace_catB2022_{tag}.root',
        "C22" : f'../../models/workspaces/DsPhiPi_wspace_catC2022_{tag}.root',
    }
elif args.year == 2023:
    wspace_byCat ={
        "A23" : f'../../models/workspaces/DsPhiPi_wspace_catA2023_{tag}.root',
        "B23" : f'../../models/workspaces/DsPhiPi_wspace_catB2023_{tag}.root',
        "C23" : f'../../models/workspaces/DsPhiPi_wspace_catC2023_{tag}.root',
    }
else:
    print('Year not supported')
    sys.exit(1)


# get the mc/data workspace
data_wspace = 'DsPhiPi_data_wspace'
mc_wspace   = 'DsPhiPi_mc_wspace'
data_width, data_mean = [], []
data_width_error, data_mean_error = [], []
mc_width, mc_mean     = [], []
mc_width_error, mc_mean_error = [], []
for cat in wspace_byCat:
    print(f' ---- category: {cat} ----')
    f = ROOT.TFile.Open(wspace_byCat[cat])
    # mc
    w_mc  = f.Get(mc_wspace)
    #mean  = getattr(w_mc['mean_mc'], 'evaluate')()
    mean  = getattr(w_mc['Ds_Mmc'], 'getVal')() + getattr(w_mc['dM_mc'], 'getVal')()
    mean_err = getattr(w_mc['Ds_Mmc'], 'getError')() + getattr(w_mc['dM_mc'], 'getError')()
    width = getattr(w_mc['width_mc'], 'getVal')() *1000
    width_err = getattr(w_mc['width_mc'], 'getError')() * 1000
    print(f'[MC] mean: {mean:.3f} +/- {mean_err:.3f} width: {width:.3f} +/- {width_err:.3f}')
    mc_mean.append(mean)
    mc_mean_error.append(mean_err)
    mc_width.append(width)
    mc_width_error.append(width_err)
    # data
    w_data = f.Get(data_wspace)
    #mean   = getattr(w_data['mean_mc'], 'evaluate')()
    mean  = getattr(w_data['Ds_Mmc'], 'getVal')() + getattr(w_data['dM'], 'getVal')()
    mean_err = getattr(w_data['Ds_Mmc'], 'getError')() + getattr(w_data['dM'], 'getError')()
    width  = getattr(w_data['width'], 'getVal')() * 1000
    width_err = getattr(w_data['width'], 'getError')() * 1000
    print(f'[DATA] mean: {mean:.3f} +/- {mean_err:.3f} width: {width:.3f} +/- {width_err:.3f}') 
    data_mean.append(mean)
    data_mean_error.append(mean_err)
    data_width.append(width)
    data_width_error.append(width_err)
    f.Close()
    print('\n')
# save the systematic uncertainty in json file
data_mean = np.array(data_mean)
data_mean_error = np.array(data_mean_error)
data_width = np.array(data_width)
data_width_error = np.array(data_width_error)
mc_mean = np.array(mc_mean)
mc_mean_error = np.array(mc_mean_error)
mc_width = np.array(mc_width)
mc_width_error = np.array(mc_width_error)

mean_ratio = np.divide(data_mean, mc_mean)
mean_ratio_error = np.sqrt((data_mean_error/data_mean)**2 + (mc_mean_error/mc_mean)**2) * mean_ratio
width_ratio = np.divide(data_width, mc_width)
width_ratio_error = np.sqrt((data_width_error/data_width)**2 + (mc_width_error/mc_width)**2) * width_ratio
sys_dict = {}
for i, cat in enumerate(wspace_byCat.keys()):
    sys_dict[cat] = {
        'mean':  np.abs(mean_ratio[i]  - 1.0),
        'width': np.abs(width_ratio[i] - 1.0),
    } 
with open(f'signal_shape_comparison_{args.year}_{tag}.json', 'w') as f:
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

# plot the data and mc mean/ width
ax[0,0].grid(zorder = 1, linestyle='--')
#ax[0,0].scatter(wspace_byCat.keys(), data_mean, c='b', label='Data', zorder=2)
#ax[0,0].scatter(wspace_byCat.keys(), mc_mean, c='r', label='MC', zorder = 3)
ax[0,0].errorbar(wspace_byCat.keys(), data_mean, yerr=data_mean_error, fmt='o', c='b', label='Data', zorder=2)
ax[0,0].errorbar(wspace_byCat.keys(), mc_mean, yerr=mc_mean_error, fmt='o', c='r', label='MC', zorder=3)
ax[0,0].set_ylabel('Mean (GeV)', fontsize=label_fontsize)
ax[0,0].set_ylim(cfg.Ds_mass - 0.005, cfg.Ds_mass + 0.005)
ax[0,0].tick_params(axis='both', labelsize=ticks_fontsize)

ax[0,1].grid(zorder = 1, linestyle='--')
#ax[0,1].scatter(wspace_byCat.keys(), data_width, c='b', label='Data', zorder = 2)
#ax[0,1].scatter(wspace_byCat.keys(), mc_width, c='r', label='MC', zorder = 3)
ax[0,1].errorbar(wspace_byCat.keys(), data_width, yerr=data_width_error, fmt='o', c='b', label='Data', zorder=2)
ax[0,1].errorbar(wspace_byCat.keys(), mc_width, yerr=mc_width_error, fmt='o', c='r', label='MC', zorder=3)
ax[0,1].set_ylabel('Width (MeV)', fontsize=label_fontsize)
ax[0,1].set_ylim(5.0, 30.0)
ax[0,1].tick_params(axis='both', labelsize=ticks_fontsize)


# plot the ratio of data to mc mean/width
ax[1,0].grid(zorder = 0, linestyle='--')
#ax[1,0].scatter(wspace_byCat.keys(), mean_ratio, c='k', zorder=2)
ax[1,0].errorbar(wspace_byCat.keys(), mean_ratio, yerr=mean_ratio_error, fmt='o', c='k', zorder=2)
ax[1,0].set_ylabel('|Data/MC - 1| (%)', fontsize=label_fontsize, labelpad=15)
ax[1,0].set_ylim(0.0, 1.6*np.max(mean_ratio))
ax[1,0].tick_params(axis='both', labelsize=ticks_fontsize)

ax[1,1].grid(zorder = 0, linestyle='--')
#ax[1,1].scatter(wspace_byCat.keys(), width_ratio, c='k', zorder=2)
ax[1,1].errorbar(wspace_byCat.keys(), width_ratio, yerr=width_ratio_error, fmt='o', c='k', zorder=2)
ax[1,1].set_ylabel('|Data/MC - 1| (%)', fontsize=label_fontsize, labelpad=25)
ax[1,1].set_ylim(0.0, 1.6*np.max(width_ratio))
ax[1,1].tick_params(axis='both', labelsize=ticks_fontsize)


# Add a legend to the plot
ax[0,0].legend(loc = 'upper left', fontsize=label_fontsize, frameon=False)
ax[0,1].legend(loc = 'upper left', fontsize=label_fontsize, frameon=False)

# Adjust the layout of the subplots

plt.savefig(f'signal_shape_comparison_{args.year}_{tag}.png')
plt.savefig(f'signal_shape_comparison_{args.year}_{tag}.pdf')

