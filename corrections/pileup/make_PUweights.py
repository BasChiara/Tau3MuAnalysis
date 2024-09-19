import ROOT
import numpy as np
import os
import sys
import argparse

sys.path.append('../..')
from plots.color_text import color_text as ct


parser = argparse.ArgumentParser(description='Make pileup weights')
parser.add_argument('--era', choices=['2022preEE', '2022EE', '2023preBPix', '2023BPix'], default='2022preEE', help='era to be used')
parser.add_argument('--mc_central', action='store_true', help='extract MC PU from central configuration')
parser.add_argument('--mc_central_nano',    action='store_true', help='extract MC PU from nanoAOD files with NO selection')
parser.add_argument('--mc_nano',    action='store_true', help='extract MC PU from nanoAOD files with tau3mu preselection')
parser.add_argument('--mc_mini',    action='store_true', help='extract MC PU from miniAOD files')
parser.add_argument('--hist_only',  action='store_true', help='only create histograms')
args = parser.parse_args()


era = args.era
# general output settings
ROOT.gROOT.SetBatch(True)
out_dir = 'pileup_histograms'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
# data
out_file_data = f'{out_dir}/pileupDATA_{era}'
# mc
mc_tag = 'central'
if args.mc_nano:
    mc_tag = 'T3MnanoAOD'
elif args.mc_central_nano:
    mc_tag = 'nanoAOD'
elif args.mc_mini:
    mc_tag = 'miniAOD'
out_file_mc   = f'{out_dir}/pileupMC_{mc_tag}_{era}'


# -------------- PILEUP in DATA ----------------

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
    "2022preEE"     : base_cJson + "Collisions22/PileUp/BCD/pileup_JSON.txt",
    "2022EE"        : base_cJson + "Collisions22/PileUp/EFG/pileup_JSON.txt",
    "2023preBPix"   : base_cJson + "Collisions23/PileUp/BC/pileup_JSON.txt",
    "2023BPix"      : base_cJson + "Collisions23/PileUp/D/pileup_JSON.txt",
    
}

# pileup histogram
print(f'{ct.BOLD}[+] processing era {era}{ct.END}')
#pileupCalc.py -i MyAnalysisJSON.txt --inputLumiJSON pileup_JSON.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 MyDataPileupHistogram.root

for j, jfile in enumerate(central_GoldenJson[era]):
    out_file_j = f'{out_file_data}_{j}.root'
    cmd = f'./pileupCalc_fix.py -i {jfile} --inputLumiJSON {central_PuJson[era]} --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100  {out_file_j}'
    print(f'\n> {cmd}')
    os.system(cmd)
    # check if the file is created
    if not os.path.exists(out_file_j):
        print(f'{ct.RED}[-] ERROR: file {out_file_j} not created{ct.END}')
        sys.exit(1)
# hadd histogram togeter
hadd_cmd = f'hadd -f -v 1 {out_file_data}.root {out_file_data}_*.root'
print('\n[+] hadd DATA pileup hstogram')
os.system(hadd_cmd)
os.system(f'rm {out_file_data}_*.root')




# -------------- PILEUP in MC -------------- #
# central nanoAOD files
nano_files ={
    "2022preEE"     : "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/corrections/NLO_W/WtoTauNu_Tauto3Mu_Run3Summer22preEENanoAODv12_fileList.txt",
    "2022EE"        : "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/corrections/NLO_W/WtoTauNu_Tauto3Mu_Run3Summer22EENanoAODv12_fileList.txt",
    "2023preBPix"   : "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/corrections/NLO_W/WtoTauNu_Tauto3Mu_Run3Summer23preBPixNanoAODv12_fileList.txt",
    "2023BPix"      : "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/corrections/NLO_W/WtoTauNu_Tauto3Mu_Run3Summer23BPixNanoAODv12_fileList.txt",
}
# nanoAOD files with tau3mu preselection
nano_base = '/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/'
t3m_nano_files ={
    "2022preEE"     : nano_base + "crab_WnuTau3Mu_2022/240803_095729/0000/",
    "2022EE"        : nano_base + "crab_WnuTau3Mu_2022EE/240803_095719/0000/",
    "2023preBPix"   : nano_base + "crab_WnuTau3Mu_2023preBPix/240803_095748/0000/", 
    "2023BPix"      : nano_base + "crab_WnuTau3Mu_2023BPix/240803_095801/0000/" 
}

# miniAOD files
mini_base = '/eos/cms/store/group/phys_bphys/cbasile/Tau3MuPUprofile_2024Sep07/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/'
mini_files ={
    "2022preEE"     : mini_base + "crab_WnuTau3Mu_2022/240907_130417/0000/",
    "2022EE"        : mini_base + "crab_WnuTau3Mu_2022EE/240907_130452/0000/",
    "2023preBPix"   : mini_base + "crab_WnuTau3Mu_2023preBPix/240907_130532/0000/", 
    "2023BPix"      : mini_base + "crab_WnuTau3Mu_2023BPix/240907_130611/0000/" 
}
h_mc_PU = ROOT.TH1F('h_mc_PU', 'h_mc_PU', 100, 0, 100)
if args.mc_central:
    print(f'{ct.BOLD}[+] extracting PU from central configuration{ct.END}')
#  PU used for simulation (2022) -> https://github.com/cms-sw/cmssw/blob/CMSSW_13_3_X/SimGeneral/MixingModule/python/Run3_2022_LHC_Simulation_10h_2h_cfi.py
#  PU used for simulation (2023) -> https://github.com/CMS-LUMI-POG/cmssw/blob/master/SimGeneral/MixingModule/python/mix_2023_25ns_RunIII2023Summer24_PoissonOOTPU_cfi.py
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
    mc_pu_23 = [ 8.116278344749134e-05, 5.5987969004788374e-05, 6.677898582941577e-05, 7.137503028766281e-05, 9.431933415744541e-05,
        0.0001023845026191297, 9.960846322677061e-05, 0.00010738495275134475, 0.00010979972300512113, 0.00011327541982905317,
        0.00014643418805414227, 0.0001432058638282947, 0.00016234245814776687, 0.00020275708314691687, 0.0002950812457607141,
        0.0004759129304992025, 0.0006747743441107274, 0.0009100053933076372, 0.0012592148574153373, 0.0017383675584680713,
        0.002389205555468726, 0.003270776226583364, 0.004453998536649548, 0.005939678688714035, 0.007787117434534316,
        0.009910586962123618, 0.011961857118914614, 0.013970348243434117, 0.01582537823156475, 0.017540070641917434,
        0.019152870863063727, 0.020723914371610908, 0.021965706072013463, 0.023015666030278468, 0.023893542848212778,
        0.024748076488291797, 0.02538403423449164, 0.02598795618093042, 0.026411981892580757, 0.0270248009703733,
        0.02777775800740078, 0.028775994088665668, 0.03002482287006016, 0.031487967654889065, 0.03309553417219972,
        0.03512324863913352, 0.03721072409275871, 0.03953750395511365, 0.04167021006622745, 0.04290148907576494,
        0.04285019947395152, 0.04147920175787501, 0.0388103252024252, 0.034857491473899986, 0.03022141658748453,
        0.025707741879936, 0.02147792024675864, 0.017638691987518676, 0.014260779172668731, 0.011352880434199124,
        0.008962650048458793, 0.0069264602964894196, 0.00523916662369792, 0.0038960153250320747, 0.0029329254375063452,
        0.0022137927924821945, 0.0016878416507048078, 0.001270029531498029, 0.000852475503220966, 0.0005797890365890959,
        0.00038547177946587365, 0.00023724418104355103, 0.0001245946970750199, 6.764278274045408e-05, 3.9244477235073656e-05,
        2.544429722963923e-05, 1.3642418255344302e-05, 7.821952477586498e-06, 4.89133655752742e-06, 2.454128879581351e-06,
        6.42895936025524e-07, 9.589122608465836e-08, 2.1398618675588528e-08, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0]
        
    PU_values ={
        "2022preEE"     : mc_pu_22,
        "2022EE"        : mc_pu_22,
        "2023preBPix"   : mc_pu_23,
        "2023BPix"      : mc_pu_23,
    }
    # fill histogram with 0 error
    [h_mc_PU.SetBinContent(i+1, PU_values[era][i]) for i in range(100)]
    [h_mc_PU.SetBinError(i+1, 0) for i in range(100)]
elif args.mc_mini:
    print(f'{ct.BOLD}[+] extracting PU from miniAOD files{ct.END}')
    # extract PU from miniAOD
    mini_chain = ROOT.TChain('Events')
    mini_chain.Add(f'{mini_files[era]}*.root')
    print(f'{ct.BOLD}[+]{ct.END} {mini_chain.GetEntries()} entries')
    mini_chain.Draw(f'Pileup_nTrueInt>>{h_mc_PU.GetName()}', '', 'goff')
elif args.mc_nano:
    print(f'{ct.BOLD}[+] extracting PU from nanoAOD+t3m preselection files{ct.END}')
    # extract PU from miniAOD
    nano_chain = ROOT.TChain('Events')
    nano_chain.Add(f'{t3m_nano_files[era]}*.root')
    print(f'{ct.BOLD}[+]{ct.END} {nano_chain.GetEntries()} entries')
    nano_chain.Draw(f'Pileup_nTrueInt>>{h_mc_PU.GetName()}', '', 'goff') 
elif args.mc_central_nano:
    print(f'{ct.BOLD}[+] extracting PU from nanoAOD files{ct.END}')
    xrootd_prefix = "root://cms-xrd-global.cern.ch//"
    # extract PU from nanoAOD
    nano_chain = ROOT.TChain('Events')
    [nano_chain.Add(f'{xrootd_prefix}{line.strip()}') for line in open(nano_files[era])]
    print(f'{ct.BOLD}[+]{ct.END} {nano_chain.GetEntries()} entries')
    nano_chain.Draw(f'Pileup_nTrueInt>>{h_mc_PU.GetName()}', '', 'goff')

h_mc_PU.Sumw2()
print(f'[MC] PU integral: {h_mc_PU.Integral()}')
h_mc_PU.Scale(1./h_mc_PU.Integral())

# save MC PU
out_file = ROOT.TFile.Open(f'{out_file_mc}.root', 'recreate')
h_mc_PU.Write()

# -------------- PU WEIGHTS -------------- #
if args.hist_only:
    sys.exit(0)
# calculate PU weights
data_file = ROOT.TFile.Open(f'{out_file_data}.root')
h_data_PU = data_file.Get('pileup')
h_data_PU.SetDirectory(0)
data_file.Close()

h_data_PU.Sumw2()
h_data_PU.Scale(1./h_data_PU.Integral())

base_name = f'myPUweights_GoldenJson_{era}'
h_weights = h_data_PU.Clone(f'{base_name}_nominal')
h_weights.Divide(h_mc_PU)
h_weights.SetTitle(f'PU weights {era} ')
# fixme :set errors to 0
#[h_weights.SetBinError(i+1, 0) for i in range(100)]
h_weights_down  = ROOT.TH1F(f'{base_name}_down', f'{base_name}_down', 100, 0, 100)
h_weights_down.Sumw2()
[h_weights_down.SetBinContent(i+1, h_weights.GetBinContent(i+1) - h_weights.GetBinError(i+1)) for i in range(100)]
h_weights_up    = ROOT.TH1F(f'{base_name}_up', f'{base_name}_up', 100, 0, 100)
h_weights_up.Sumw2()
[h_weights_up.SetBinContent(i+1, h_weights.GetBinContent(i+1) + h_weights.GetBinError(i+1)) for i in range(100)]


# save PU weights
out_file = ROOT.TFile.Open(f'weights/PUweights_{era}.root', 'recreate')
h_weights.Write()
h_weights_down.Write()
h_weights_up.Write()
out_file.Close()

