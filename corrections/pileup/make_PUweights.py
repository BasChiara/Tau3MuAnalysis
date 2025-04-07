import ROOT
import numpy as np
import os
import sys
import argparse

sys.path.append('../..')
from plots.color_text import color_text as ct


parser = argparse.ArgumentParser(description='Make pileup weights')
parser.add_argument('--era', choices=['2022preEE', '2022EE', '2023preBPix', '2023BPix', '2024'], default='2022preEE', help='era to be used')
parser.add_argument('--mc_central', action='store_true', help='extract MC PU from central configuration')
parser.add_argument('--mc_central_nano',    action='store_true', help='extract MC PU from nanoAOD files with NO selection')
parser.add_argument('--mc_nano',    action='store_true', help='extract MC PU from nanoAOD files with tau3mu preselection')
parser.add_argument('--mc_mini',    action='store_true', help='extract MC PU from miniAOD files')
parser.add_argument('--hist_only',  action='store_true', help='only create histograms')
args = parser.parse_args()


era = args.era
xsec_69p2mb = True

# general output settings
ROOT.gROOT.SetBatch(True)
out_dir = 'pileup_histograms'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
# data
out_file_data = f'{out_dir}/pileupDATA_{era}'
# mc
mc_tag = 'central' + ('_MinBxsec69p2mb' if xsec_69p2mb else '_MinBxsec80mb')
if args.mc_nano:
    mc_tag = 'T3MnanoAOD'
elif args.mc_central_nano:
    mc_tag = 'nanoAOD'
elif args.mc_mini:
    mc_tag = 'miniAOD'
out_file_mc   = f'{out_dir}/pileupMC_{mc_tag}_{era}'


# -------------- PILEUP in DATA ----------------
 
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
    "2024" : [
        base_cJson + "Collisions24/Cert_Collisions2024_378981_386951_Golden.json",
    ]
}
#base_myJson_120X = "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/PhysicsTools/Tau3muNANO/production/"
#base_myJson_130X = "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_13_0_13/src/PhysicsTools/Tau3muNANO/production/"
#my_AnalysisJson = {
#    "2022preEE" : [
#        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Cv1_0/results/lumisToProcess.json",
#        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Dv1_0/results/lumisToProcess.json",
#        base_myJson_120X + "Tau3MuNano_2024Aug06/crab_data_Run2022Dv2_0/results/lumisToProcess.json",
#        ],
#    "2022EE"    :[
#        base_myJson_120X + "Tau3MuNano_2024Aug05/crab_data_Run2022Ev1_0/results/lumisToProcess.json",
#        base_myJson_130X + "Tau3MuNano_2024Aug02/crab_data_Run2022Fv1_0/results/lumisToProcess.json",
#        base_myJson_130X + "Tau3MuNano_2024Aug02/crab_data_Run2022Gv1_0/results/lumisToProcess.json",
#    ]
#}
central_PuJson ={
    "2022preEE"     : base_cJson + "Collisions22/PileUp/BCD/pileup_JSON.txt",
    "2022EE"        : base_cJson + "Collisions22/PileUp/EFG/pileup_JSON.txt",
    "2023preBPix"   : base_cJson + "Collisions23/PileUp/BC/pileup_JSON.txt",
    "2023BPix"      : base_cJson + "Collisions23/PileUp/D/pileup_JSON.txt",
    "2024"          : "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_14_0_16/src/PhysicsTools/Tau3muNANO/production/PileUp/pileup_JSON.txt",  # made with brilcalc -> https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJSONFileforData#Creating_the_pileup_files 
    
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
    "2024"         : None, # fixme: search for the file
}
# nanoAOD files with tau3mu preselection
nano_base = '/eos/cms/store/group/phys_bphys/cbasile/'
t3m_nano_files ={
    "2022preEE"     : nano_base + "Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2022/240803_095729/0000/",
    "2022EE"        : nano_base + "Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2022EE/240803_095719/0000/",
    "2023preBPix"   : nano_base + "Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2023preBPix/240803_095748/0000/", 
    "2023BPix"      : nano_base + "Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2023BPix/240803_095801/0000/",
    "2024"          : nano_base + "Tau3MuNano_2025Mar07/WtoTauNu-Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2024/250307_172820/0000/"
}

# miniAOD files with no preselection
mini_base = '/eos/cms/store/group/phys_bphys/cbasile/Tau3MuPUprofile_2024Sep07/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/'
mini_files ={
    "2022preEE"     : mini_base + "crab_WnuTau3Mu_2022/240907_130417/0000/",
    "2022EE"        : mini_base + "crab_WnuTau3Mu_2022EE/240907_130452/0000/",
    "2023preBPix"   : mini_base + "crab_WnuTau3Mu_2023preBPix/240907_130532/0000/", 
    "2023BPix"      : mini_base + "crab_WnuTau3Mu_2023BPix/240907_130611/0000/",
    "2024"          : None # not produced yet
}
# -- PU profile from MC campaign configuarion -- #
h_mc_PU = ROOT.TH1F('h_mc_PU', 'h_mc_PU', 100, 0, 100)
if args.mc_central:

#  PU used for simulation (2022) -> https://github.com/cms-sw/cmssw/blob/CMSSW_13_3_X/SimGeneral/MixingModule/python/Run3_2022_LHC_Simulation_10h_2h_cfi.py
#  PU used for simulation (2023) -> https://github.com/CMS-LUMI-POG/cmssw/blob/master/SimGeneral/MixingModule/python/mix_2023_25ns_RunIII2023Summer24_PoissonOOTPU_cfi.py
    import FWCore.ParameterSet.Config as cms

    print(f'{ct.BOLD}[+] extracting PU from central configuration{ct.END}')
    # 2022 has only minBias xsec = 69.2 mb
    if xsec_69p2mb:
        from SimGeneral.MixingModule.Run3_2022_LHC_Simulation_10h_2h_cfi import mix as PU_69p2mb_22_mix
        mc_pu_22 = PU_69p2mb_22_mix.input.nbPileupEvents.probValue
    else : mc_pu_22 = None
    # 2023 has 2 minBias xsec scenarios
    if xsec_69p2mb:
        # 2023 minBias xsec = 69.2 mb
        from python.mix_2023_25ns_RunIII2023Summer24_PoissonOOTPU_cfi import mix as PU_69p2mb_23_mix
        mc_pu_23 = PU_69p2mb_23_mix.input.nbPileupEvents.probValue
    else:
        # 2023  minBias xsec = 80 mb
        from SimGeneral.MixingModule.mix_2023_Fills_8807_8901_ProjectedPileup_PoissonOOTPU_cfi import mix as PU_80mb_23_mix
        mc_pu_23 = PU_80mb_23_mix.input.nbPileupEvents.probValue
        
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
print(f'{ct.BOLD}[+]{ct.END} MC PU histogram saved in {out_file_mc}.root')

# -------------- PU WEIGHTS -------------- #
if args.hist_only: sys.exit(0)
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

