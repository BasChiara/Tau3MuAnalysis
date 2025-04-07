#!/usr/bin/bash
# run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
#make clean
#make ana 

RUNTIME_H=12
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'
EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/'
#EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/reMini2022/'
DATA_PATH='data/data_PromptReco2024/'

## 2024 era B ##
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 299 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 300 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 261 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 300 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 299 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 300 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 175 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 276 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Bv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}

## 2024 era C ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1221 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1217 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1222 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1221 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1115 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1222 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1192 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1223 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Cv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}

# 2024 era D ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1168 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1166 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1167 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1167 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1166 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1166 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1165 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1104 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Dv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}

# 2024 era E ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 770 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 853 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 853 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 853 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 852 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 853 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 854 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 852 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Ev1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}

python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 728 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 729 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 728 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 726 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 728 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 729 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 728 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 728 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Ev2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}

# 2024 era F ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3517 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3507 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3511 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3507 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3504 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3516 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3517 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 3522 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Fv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}

# 2024 era G ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4620 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4621 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4621 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4621 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4621 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4619 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4620 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 4621 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Gv1.txt --runtime ${RUNTIME_H} --DsPhiPi  --HLT_path ${HLT_CONF}

# 2024 era H ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 656 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 657 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 657 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 658 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 659 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 659 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 656 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 655 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Hv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}

# 2024 era I ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 703 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 702 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 700 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 701 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 701 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 579 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 703 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 702 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Iv1.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}

python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 654 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass0_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 654 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass1_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 656 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass2_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 655 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass3_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 654 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass4_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 655 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass5_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 655 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass6_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 656 -n ${FILES_PER_JOB} -p job_report --eos ${EOS_PATH} ${DATA_PATH}ParkingDoubleMuonLowMass7_2024Iv2.txt --runtime ${RUNTIME_H}  --DsPhiPi --HLT_path ${HLT_CONF}
