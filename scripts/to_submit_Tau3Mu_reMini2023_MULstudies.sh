#run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
#make clean
#make ana 
RUNTIME_H=12
FILES_PER_JOB=50
HLT_CONF='HLT_overlap'
EOS_PATH='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023_MULstudies/'
DATA_PATH='data/data_reMini2023/'



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
