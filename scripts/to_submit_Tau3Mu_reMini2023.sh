#run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
#make clean
#make ana 
RUNTIME_H=12
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'
EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/'
DATA_PATH='data/data_reMini2023/'


## 2023 B
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 338 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 343 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 341 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 339 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 339 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 348 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 341 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 340 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Bv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  

# 2023 C
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 819 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
#python3 scripts/submit_batch_dev.py -N -1 -s 1 -F *** -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Cv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 821 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 817 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 821 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 827 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 819 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 820 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Cv1.txt  --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
# v2
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 182 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 184 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 184 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 188 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 187 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 183 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 183 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 184 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Cv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
# v3
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 232 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 230 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 231 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 234 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 233 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 239 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 236 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 234 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Cv3.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
# v4
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1587 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1577 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1591 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1576 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1588 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1580 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1574 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1583 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Cv4.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  

## 2023 D
# v1
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1190 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1194 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1199 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1195 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1185 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF} 
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1184 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1188 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 1186 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Dv1.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
## v2
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 222 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass0_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 222 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass1_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 217 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass2_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 218 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass3_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 221 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass4_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 224 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass5_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 218 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass6_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
python3 scripts/submit_batch_dev.py -N -1 -s 1 -F 217 -n ${FILES_PER_JOB} -p job_report --eos $EOS_PATH ${DATA_PATH}ParkingDoubleMuonLowMass7_2023Dv2.txt --runtime ${RUNTIME_H} --HLT_path ${HLT_CONF}  
