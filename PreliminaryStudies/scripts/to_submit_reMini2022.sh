# run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/CMSSW_12_4_11_patch3-Tau3Mu/src/Tau3MuAnalysis/PreliminaryStudies 
make clean
make reco
## 2022 era E ##
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1107 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1105 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1107 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1105 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1104 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1104 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1108 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022E.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 1105 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022E.txt

## 2022 era F ##
python3 scripts/submit_batch.py -N -1 -n 1 -F 2603 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022F.txt 
python3 scripts/submit_batch.py -N -1 -n 1 -F 2587 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2602 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2609 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2567 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2584 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2595 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022F.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 2584 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022F.txt

## 2022 era G ##
python3 scripts/submit_batch.py -N -1 -n 1 -F 422 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 418 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 417 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 421 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022G.txt
#python3 scripts/submit_batch.py -N -1 -n 1 -F 419 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 420 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 426 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022G.txt
python3 scripts/submit_batch.py -N -1 -n 1 -F 421 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022G.txt
