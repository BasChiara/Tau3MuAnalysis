#run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
make clean
make ana 
RUNTIME_H=12
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'

## 2023 B
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 339 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 344 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 343 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 340 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 340 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 348 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 342 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 341 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023B.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  

# 2023 C
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 820 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F *** -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 823 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F *** -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 822 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 829 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 820 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 822 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
# v2
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 186 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 185 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 184 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F *** -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv.2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 191 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 185 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 183 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 185 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
# v3
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 234 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 231 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 234 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F *** -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 234 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 240 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 237 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 236 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
# v4
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1593 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1578 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1602 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1577 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1600 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1584 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1575 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1596 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023C.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  

## 2023 D
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1190 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1200 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1204 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1206 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F **** -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1175 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1188 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1176 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
## v2
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 224 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 225 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 218 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 219 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 222 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 229 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 219 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 224 -n ${FILES_PER_JOB} -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023D.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
