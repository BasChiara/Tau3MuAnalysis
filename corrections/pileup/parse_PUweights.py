#####
# Parse the PU weights from CENTRAL json files and save them in a root file
#####

import ROOT
import correctionlib
import datetime 
import numpy as np

debug = False
# central corrections in correctionlib format
#       --> from https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration
base_cJson = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/LUM/"
json_file_list = [
   base_cJson +  "2022_Summer22/puWeights.json.gz",
   base_cJson +  "2022_Summer22EE/puWeights.json.gz",
   base_cJson +  "2023_Summer23/puWeights.json.gz",
   base_cJson +  "2023_Summer23BPix/puWeights.json.gz",
]
value_list = ["nominal", "up", "down"]

PU_lo, PU_hi, binw = 0.0, 100.0, 1.0
binning = np.arange(PU_lo, PU_hi, binw)
if debug : print(binning)
outfile = ROOT.TFile("./weights/puWeights_CollisionsRun3_GoldenJson_"+datetime.date.today().strftime('%Y%b%d')+".root", "RECREATE")
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
