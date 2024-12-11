#! /bin/bash

#source ~/setup_proxy.sh

# --- 2022preEE
# t3m
dasgoclient --query="file dataset=/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM" > WtoTauNu_Tauto3Mu_Run3Summer22preEENanoAODv12_fileList.txt
# WtoLNu-2Jets
dasgoclient --query="file dataset=/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM" > WtoLNu-2Jets_Run3Summer22preEENanoAODv12_fileList.txt

# --- 2022EE
# t3m
dasgoclient --query="file dataset=/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM" > WtoTauNu_Tauto3Mu_Run3Summer22EENanoAODv12_fileList.txt
# WtoLNu-2Jets
dasgoclient --query="file dataset=/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM" > WtoLNu-2Jets_Run3Summer22EENanoAODv12_fileList.txt

# 2023preBPix
# t3m
dasgoclient --query="file dataset=/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/NANOAODSIM" > WtoTauNu_Tauto3Mu_Run3Summer23preBPixNanoAODv12_fileList.txt
dasgoclient --query="file dataset=/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2/NANOAODSIM" > WtoLNu-2Jets_Run3Summer23preBPixNanoAODv12_fileList.txt

# 2023BPix
# t3m
dasgoclient --query="file dataset=/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/NANOAODSIM" > WtoTauNu_Tauto3Mu_Run3Summer23BPixNanoAODv12_fileList.txt
dasgoclient --query="file dataset=/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/NANOAODSIM" > WtoLNu-2Jets_Run3Summer23BPixNanoAODv12_fileList.txt
