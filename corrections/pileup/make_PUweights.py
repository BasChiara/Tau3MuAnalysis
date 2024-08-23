import ROOT
import numpy as np
import os
import sys
import argparse

sys.path.append('../..')
from plots.color_text import color_text as ct


parser = argparse.ArgumentParser(description='Make pileup weights')
parser.add_argument('--era', choices=['2022preEE', '2022EE', '2023preBPix', '2023BPix'], default='2022preEE', help='era to be used')
args = parser.parse_args()


era = args.era

# PILEUP in DATA
# fixme : error when running on central json 
base_cJson = "/eos/user/c/cmsdqm/www/CAF/certification/"
central_GoldenJson = {
    "2022preEE" : [
        base_cJson + "Collisions22/Cert_Collisions2022_eraB_355100_355769_Golden.json",
        base_cJson + "Collisions22/Cert_Collisions2022_eraC_355862_357482_Golden.json",
        base_cJson + "Collisions22/Cert_Collisions2022_eraD_357538_357900_Golden.json",
        ],
    "2022EE" : [
        base_cJson + "Collisions22/Cert_Collisions2022_eraE_359022_360331_Golden.json",
        base_cJson + "Collisions22/Cert_Collisions2022_eraF_360390_362167_Golden.json",
        base_cJson + "Collisions22/Cert_Collisions2022_eraG_362433_362760_Golden.json",
    ],
    "2023preBPix" : [
        base_cJson + "Collisions23/Cert_Collisions2023_eraB_366403_367079_Golden.json",
        base_cJson + "Collisions23/Cert_Collisions2023_eraC_367095_368823_Golden.json",
    ],
    "2023BPix" : [
        base_cJson + "Collisions23/Cert_Collisions2023_eraD_369803_370790_Golden.json",
        ],
}
base_myJson_120X = "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/PhysicsTools/Tau3muNANO/production/"
base_myJson_130X = "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_13_0_13/src/PhysicsTools/Tau3muNANO/production/"
my_AnalysisJson = {
    "2022preEE" : [
        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Cv1_0/results/lumisToProcess.json",
        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Dv1_0/results/lumisToProcess.json",
        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Dv2_0/results/lumisToProcess.json",
        ],
    "2022EE"    :[
        base_myJson_120X + "Tau3MuNano_2024Aug05/crab_data_Run2022Ev1_0/results/lumisToProcess.json",
        base_myJson_130X + "Tau3MuNano_2024Aug02/crab_data_Run2022Fv1_0/results/lumisToProcess.json",
        base_myJson_130X + "Tau3MuNano_2024Aug02/crab_data_Run2022Gv1_0/results/lumisToProcess.json",
    ]
}
central_PuJson ={
    "2022preEE" : base_cJson + "Collisions22/PileUp/BCD/pileup_JSON.txt",
    "2022EE"    : base_cJson + "Collisions22/PileUp/EFG/pileup_JSON.txt",
    
}

# pileup histogram
print(f'{ct.BOLD}[+] processing era {era}{ct.END}')
#pileupCalc.py -i MyAnalysisJSON.txt --inputLumiJSON pileup_JSON.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 MyDataPileupHistogram.root
for j, jfile in enumerate(central_GoldenJson[era]):
    cmd = f'pileupCalc.py -i {jfile} --inputLumiJSON {central_PuJson[era]} --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100  pileup_{era}_{j}.root'
    print(f'\n> {cmd}')
    os.system(cmd)
    # check if the file is created
    if not os.path.exists(f'pileup_{era}_{j}.root'):
        print(f'{ct.RED}[-] ERROR: file pileup_{era}_{j}.root not created{ct.END}')
        sys.exit(1)
# hadd histogram togeter
hadd_cmd = f'hadd -f -v 1 pileup_{era}.root pileup_{era}_*.root'
print('\n[+] hadd DATA pileup hstogram')
os.system(hadd_cmd)
os.system(f'rm pileup_{era}_*.root')

# PILEUP in MC
#  PU used for simulation (2022) -> https://github.com/cms-sw/cmssw/blob/CMSSW_13_3_X/SimGeneral/MixingModule/python/Run3_2022_LHC_Simulation_10h_2h_cfi.py
#  PU used for simulation (2023) ->
mc_pu_22 = [7.075550618391933e-8, 1.8432226484975646e-7, 4.6156514471969593e-7, 0.0000011111611991838491, 
	0.0000025719752161798103, 0.000005724865812608344, 0.000012255841383374045, 0.000025239403069596116, 0.00005001054998201597, 
	0.00009536530158990567, 0.00017505633393457624, 0.00030942214916825035, 0.0005268123536229287, 0.0008642843968521786, 
	0.0013669182280399903, 0.0020851167548246985, 0.0030695148409245446, 0.004363635945105083, 0.005995143197404548, 
	0.007967247822222358, 0.010252302872826594, 0.01278957659177177, 0.015488544412469806, 0.01823784978331645, 
	0.020918669702105028, 0.023420019399650906, 0.025652949149203495, 0.027560835627835043, 0.02912397347687914, 
	0.030358091266301533, 0.03130778480604892, 0.03203676872496023, 0.0326170853351521, 0.03311902652393314, 
	0.033602777248239, 0.0341120235754556, 0.03466927947785801, 0.03527261707506484, 0.035893786618889145, 
	0.03647817900850185, 0.036947435730750315, 0.03720550450678737, 0.037148460727673235, 0.03667753703450604, 
	0.03571377296329832, 0.034211859754226276, 0.032170439241889726, 0.029636506070368274, 0.02670262519076345, 
	0.023497154911314072, 0.020169158697337236, 0.016870783471647905, 0.013740289679427057, 0.010888563843704815, 
	0.008390977574442656, 0.006285186751143873, 0.004574246293656772, 0.003233538335807419, 0.002219622271900557, 
	0.0014792038980537092, 0.0009568560481315006, 0.0006007171037926386, 0.00036596934105178995, 0.0002163349104153549, 
	0.00012407362512604619, 0.0000690356949524181, 0.000037263645547231494, 0.00001951170588910065, 0.000009910336118978026, 
	0.0000048826244075428666, 0.0000023333596885075797, 0.0000010816029570543702, 4.863048449289416e-7, 2.1208148308081624e-7, 
	8.97121135679932e-8, 3.6809172420519874e-8, 1.4649459937201982e-8, 5.655267024863598e-9, 2.117664468591336e-9, 
	7.692038404370259e-10, 2.7102837405697987e-10, 9.263749466613295e-11, 3.071624552355945e-11, 9.880298997379985e-12, 
	3.0832214331312204e-12, 9.33436314183754e-13, 2.7417209623761203e-13, 7.813293248960901e-14, 2.1603865264197903e-14, 
	5.796018523167997e-15, 1.5088422256459697e-15, 3.811436255838504e-16, 9.342850737730402e-17, 2.2224464483477953e-17, 
	5.130498608124184e-18, 1.1494216669980747e-18, 2.499227229379666e-19, 5.2741621866055994e-20, 1.080281961755894e-20, 
	2.1476863811171814e-21]
PU_values ={
    "2022preEE" : mc_pu_22,
    "2022EE"    : mc_pu_22,
}
h_mc_PU = ROOT.TH1F('h_mc_PU', 'h_mc_PU', 100, 0, 100)
[h_mc_PU.SetBinContent(i+1, PU_values[era][i]) for i in range(100)]
h_mc_PU.Scale(1./h_mc_PU.Integral())
h_mc_PU.Sumw2()

# extract PU weights
data_file = ROOT.TFile.Open(f'pileup_{era}.root')
h_data_PU = data_file.Get('pileup')
h_data_PU.Scale(1./h_data_PU.Integral())
h_data_PU.Sumw2()

h_weights = h_data_PU.Clone('h_weights')
h_weights.Divide(h_mc_PU)
h_weights.SetTitle(f'PU weights {era}')
# fixme :set errors to 0
[h_weights.SetBinError(i+1, 0) for i in range(100)]

# save PU weights
out_file = ROOT.TFile.Open(f'PUweights_{era}.root', 'recreate')
h_weights.Write()
out_file.Close()

