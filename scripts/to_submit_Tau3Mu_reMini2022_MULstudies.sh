#!/usr/bin/bash
# run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
#make clean
#make ana 

RUNTIME_H=8
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'
EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_MULstudies/'
DATA_PATH='data/data_reMini2022/'

## 2022 era G ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 420 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 417 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 416 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 417 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 416 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 419 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 420 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 419 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
