#!/usr/bin/bash

# run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
make clean
make ana 

RUNTIME_H=12
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'
EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/'
DATA_PATH='data/data_reMini2022_eosbkp/'

### 2022 era C ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1295 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1295 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1296 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1296 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1296 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1295 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1294 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1296 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF} 

## 2022 era Dv1 ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 227 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 228 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 226 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 229 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 230 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 228 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 225 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 226 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
# 2022 era Dv2 ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 334 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 334 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 334 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 335 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 335 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 336 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 334 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 334 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Dv2.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}


## 2022 era E ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1107 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1101 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1104 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1105 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1104 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1104 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1108 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 1105 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Ev1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}

## 2022 era F ##
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2603 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2586 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2611 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2607 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2583 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2583 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2590 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 2584 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}

## 2022 era G ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 421 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 418 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 417 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 421 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 416 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 420 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 425 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -n ${FILES_PER_JOB} -F 420 -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2022Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi --HLT_path ${HLT_CONF}
