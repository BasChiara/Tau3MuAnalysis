# /usr/bin/bash!

# Tau3Mu 2022preEE
MY_JSON="/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/PhysicsTools/Tau3muNANO/production/Tau3MuNano2022_2024Jan29/crab_data_Run2022Cv1_0/results/lumisToProcess.json"
CENTRAL_JSON="/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/PileUp/BCD/pileup_JSON.txt"

pileupCalc.py -i $MY_JSON --inputLumiJSON $CENTRAL_JSON --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 MyDataPileupHistogram.root

