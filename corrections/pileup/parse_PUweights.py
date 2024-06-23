import ROOT
import correctionlib
import datetime 
import numpy as np

debug = False

json_file_list = [
    "weights/puWeights_Collisions2022_355100_357900_eraBCD_GoldenJson.json",
    "weights/puWeights_Collisions2022_359022_362760_eraEFG_GoldenJson.json",
    "weights/puWeights_Collisions2023_366403_369802_eraBC_GoldenJson.json",
    "weights/puWeights_Collisions2023_369803_370790_eraD_GoldenJson.json"
]
value_list = ["nominal", "up", "down"]

PU_lo, PU_hi, binw = 0.0, 100.0, 1.0
binning = np.arange(PU_lo, PU_hi, binw)
if debug : print(binning)
outfile = ROOT.TFile("./puWeights_CollisionsRun3_GoldenJson_"+datetime.date.today().strftime('%Y%b%d')+".root", "RECREATE")
print(f'[+] PU weights will be saved in {outfile}')

for json_file in json_file_list:
    
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
            #w_hist.Scale(1./w_hist.Integral()) # !!! should I normalize them?
            w_hist.Write()
        ## + sys uncertainty
        #w_sysUP_hist = ROOT.TH1D(corr_set+"_sysUP", corr_set+"_sysUP", len(binning), binning[0], binning[-1]+binw)
        #[w_sysUP_hist.SetBinContent(int(bin)+1, ceval[corr_set].evaluate(bin, "up")) for bin in binning]
        #w_sysUP_hist.Write()
        ## - sys uncertainty
        #w_sysDOWN_hist = ROOT.TH1D(corr_set+"_sysDOWN", corr_set+"_sysDOWN", len(binning), binning[0], binning[-1]+binw)
        #[w_sysDOWN_hist.SetBinContent(int(bin)+1, ceval[corr_set].evaluate(bin, "down")) for bin in binning]
        #w_sysDOWN_hist.Write()
    

outfile.Close()
