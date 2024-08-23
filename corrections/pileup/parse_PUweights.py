#####
# Parse the PU weights from CENTRAL json files and save them in a root file
#####

import ROOT
import correctionlib
import datetime 
import numpy as np

debug = False
base_cJson = "/eos/user/c/cmsdqm/www/CAF/certification/"
json_file_list = [
   "Collisions22/PileUp/BCD/pileup_JSON.txt", 
   "Collisions22/PileUp/EFG/pileup_JSON.txt", 
   "Collisions23/PileUp/BC/pileup_JSON.txt", 
   "Collisions23/PileUp/D/pileup_JSON.txt", 
]
value_list = ["nominal", "up", "down"]

PU_lo, PU_hi, binw = 0.0, 100.0, 1.0
binning = np.arange(PU_lo, PU_hi, binw)
if debug : print(binning)
outfile = ROOT.TFile("./puWeights_CollisionsRun3_GoldenJson_"+datetime.date.today().strftime('%Y%b%d')+".root", "RECREATE")
print(f'[+] PU weights will be saved in {outfile}')

for json_file in json_file_list:
    # use correction lib to extract SFs
    print(f'[+] PU weights from {json_file}')
    ceval = correctionlib.CorrectionSet.from_file(json_file)
    corr_names = list(ceval.keys())
    [print(f'\t -  {corr}') for corr in corr_names]

    for corr_set in corr_names:
        if debug : print(f' histo settings BINS {len(binning)} x_lo {binning[0]} x_hi {binning[-1]+binw}')

        for val in value_list: # nominal and +/- sys values
            
            w_hist = ROOT.TH1D(corr_set+"_"+val, corr_set+"_"+val, len(binning), binning[0], binning[-1]+binw)
            [w_hist.SetBinContent(int(bin)+1, ceval[corr_set].evaluate(bin, val)) for bin in binning]
            w_hist.Sumw2()
            print (f'\t - {corr_set} {val} integral {w_hist.Integral(w_hist.FindBin(5), w_hist.FindBin(65))}')
            #w_hist.Scale(1./w_hist.Integral()) # !!! should I normalize them?
            w_hist.Write()

outfile.Close()
