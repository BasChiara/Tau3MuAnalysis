import ROOT
import os
import sys
import requests
import json 
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mva.config as config
import style.color_text as color_text

debug = True


def fileList_to_TTree(file_name, tree_name='Events'):
    xrootd_prefix = 'root://cms-xrd-global.cern.ch//'
    file_list_tmp = open(file_name, 'r').readlines()
    if (debug) : file_list_tmp = [file_list_tmp[0]]
    tree = ROOT.TChain(tree_name)
    [tree.Add(xrootd_prefix + file_name.strip()) for file_name in file_list_tmp]
    return tree

# -DESCRIPTION: compare the WpT (gen-level) distribution for tau->3mu to ZpT distribution in data
# -GOAL : extrapolate correction for W kinematics expecially @ low-pT

xrootd_prefix = 'root://cms-xrd-global.cern.ch//'
isLastCopy_string = '(GenPart_statusFlags & (1<<13))'
W_pdgID = 24
Z_dpID  = 23
Wgen_selection = f'(fabs(GenPart_pdgId) == {W_pdgID}) && {isLastCopy_string}'
Zgen_selection = f'(fabs(GenPart_pdgId) == {Z_dpID}) && {isLastCopy_string}'

# Z-> ll NANOAOD file @ NLO
# Run2
tree_ZnloRun2 = fileList_to_TTree('ZtoLL_NLO_RunIISummer16NanoAODv7_fileList.txt')
print(f'{color_text.color_text.GREEN}[+]{color_text.color_text.END} Z->ll NLO @ 13.0 TeV tree has {tree_ZnloRun2.GetEntries()} entries')
# Run3
tree_ZnloRun3 = fileList_to_TTree('ZtoLL_NLO_Run3Summer22NanoAODv12_fileList.txt')
print(f'{color_text.color_text.GREEN}[+]{color_text.color_text.END} Z->ll NLO @ 13.6 TeV tree has {tree_ZnloRun3.GetEntries()} entries')

# W->lnu NANOAOD file @ NLO
tree_WnloRun3 = fileList_to_TTree('../NLO_W/WtoLNu-2Jets_Run3Summer22EENanoAODv12_fileList_demo.txt')
print(f'{color_text.color_text.GREEN}[+]{color_text.color_text.END} W->lnu NLO @ 13.6 TeV tree has {tree_WnloRun3.GetEntries()} entries')

# differential pp->Z xsec @ 13 TeV from https://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-010 
url = "https://www.hepdata.net/record/data/91215/1469155/4/"
jsonfile_name = "diff_ppZll_xsec.json"
if not os.path.exists(jsonfile_name):
    response = requests.get(url)
    print(f'{color_text.color_text.BOLD}[+]{color_text.color_text.END} Downloading diff xsec(pp->Z) JSON file from {url}')
    if response.status_code == 200:
        with open(jsonfile_name, "w") as file:
            file.write(response.text)
        print(f'{color_text.color_text.GREEN}[+]{color_text.color_text.END} JSON file saved as {jsonfile_name}')
    else:
        print("Failed to download the JSON file.")
else:
    print(f'{color_text.color_text.GREEN}[+]{color_text.color_text.END} JSON file {jsonfile_name} already exists')
# read the JSON file
with open(jsonfile_name) as jsonfile:
    data = json.load(jsonfile)

# loop on entries
x = []
ex = []
bins = []
y = []
ey = []
# loop over the entries and fill the THPoly
for entry in data['values']:
    x_high = float(entry['x'][0]['high'])
    x_low  = float(entry['x'][0]['low'])
    if x_high > 150 : continue
    x.append((x_high + x_low)/2)
    bins.append(x_low)
    ex.append((x_high - x_low)/2)
    # Z HEPdata
    y.append(entry['y'][2]['value'])
    ey.append(entry['y'][2]['errors'][0]['symerror'])

    print(f"bin: {x_low} - {x_high} - xsec: {y[-1]} +/- {ey[-1]} pb")
N_bins = len(x)
bins[0] = 0.1
bins.append(150)
x = np.array(x, dtype=float)
bins = np.array(bins, dtype=float)

y = np.array(y, dtype=float)
ex = np.array(ex, dtype=float)
ey = np.array(ey, dtype=float)

# prepare TH1Fs
h_Zll_data  = ROOT.TH1F("h_Zll_data", "Z->ll data",             N_bins, bins)
h_Zll_Run2  = ROOT.TH1F("h_Zll_Run2", "Z->ll NLO @ 13 TeV",     N_bins, bins)
h_Zll_Run3  = ROOT.TH1F("h_Zll_Run3", "Z->ll NLO @ 13.6 TeV",   N_bins, bins)
h_Wlnu_Run3 = ROOT.TH1F("h_Wlnu_Run3", "W->l#nu NLO @ 13.6 TeV",N_bins, bins)
# fill the histograms
[h_Zll_data.SetBinContent(i+1, y[i]) for i in range(N_bins)]
[h_Zll_data.SetBinError(i+1, ey[i]) for i in range(N_bins)]
tree_ZnloRun2.Draw(f'GenPart_pt>>h_Zll_Run2', Zgen_selection, 'goff')
h_Zll_Run2 = ROOT.gDirectory.Get('h_Zll_Run2')
tree_ZnloRun3.Draw(f'GenPart_pt>>h_Zll_Run3', Zgen_selection, 'goff')
h_Zll_Run3 = ROOT.gDirectory.Get('h_Zll_Run3')
tree_WnloRun3.Draw(f'GenPart_pt>>h_Wlnu_Run3', Wgen_selection, 'goff') 
h_Wlnu_Run3 = ROOT.gDirectory.Get('h_Wlnu_Run3')

# save in root file
out_file = ROOT.TFile("ZvsW_pT.root", "RECREATE")
h_Zll_data.Write()
h_Zll_Run2.Write()
h_Zll_Run3.Write()
h_Wlnu_Run3.Write()
out_file.Close()
print(f'{color_text.color_text.BOLD}[+]{color_text.color_text.END} TH1Fs saved in ZvsW_pT.root')