# run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
make clean
make ana 

RUNTIME_H=48
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'

## 2022 era C ##
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1295 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1295 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1296 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1296 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1296 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1295 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1294 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1296 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}

## 2022 era Dv1 ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 227 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 228 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 226 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 229 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 230 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 228 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 225 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 226 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
## 2022 era Dv2 ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 334 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 334 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 334 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 335 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 335 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 336 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 334 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 334 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 


## 2022 era E ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1107 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1101 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1104 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1105 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1104 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1104 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1108 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1105 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Ev1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 

## 2022 era F ##
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2603 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2586 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2611 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2607 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2583 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2583 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2590 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 2584 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Fv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}

## 2022 era G ##
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 421 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass0_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 418 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass1_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 417 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass2_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 421 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass3_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 416 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass4_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 420 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass5_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 425 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass6_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 420 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ data/data_reMini2022/ParkingDoubleMuonLowMass7_2022Gv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
