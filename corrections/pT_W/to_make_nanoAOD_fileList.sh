# Z->ll @ NLO Run2
dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM" > ZtoLL_NLO_RunIISummer16NanoAODv7_fileList.txt
dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext2-v1/NANOAODSIM" > ZtoLL_NLO_RunIISummer16NanoAODv0_fileList.txt
# Z->ll @ NLO Run3 
dasgoclient --query="file dataset=/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM" > ZtoLL_NLO_Run3Summer22NanoAODv12_fileList.txt
dasgoclient --query="file dataset=/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM" >> ZtoLL_NLO_Run3Summer22NanoAODv12_fileList.txt
#dasgoclient --query="file dataset=/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/NANOAODSIM" >> ZtoLL_NLO_Run3Summer22NanoAODv12_fileList.txt
#dasgoclient --query="file dataset=DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/NANOAODSIM" >> ZtoLL_NLO_Run3Summer22NanoAODv12_fileList.txt