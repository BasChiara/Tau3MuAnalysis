#run ./bin/RecoLevelAnalysis on data
cd /afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/ 
#make clean
#make ana 

## 2023 B
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 339 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 344 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 343 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 340 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 340 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 348 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 342 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 341 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023B.txt  --runtime 24 --HLT_path HLT_DoubleMu  

# 2023 C
# v1
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 820 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F *** -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv1.txt --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 823 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F *** -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 822 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 829 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 820 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 822 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv1.txt  --runtime 24 --HLT_path HLT_DoubleMu 
# v2
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 186 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 185 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 184 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
##python3 scripts/submit_batch_dev.py -N -1 -n 1 -F *** -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv.2.txt --runtime 24 --HLT_path HLT_DoubleMu
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 191 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 185 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 183 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 185 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv2.txt --runtime 24 --HLT_path HLT_DoubleMu 
# v3
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 234 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 231 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 234 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
##python3 scripts/submit_batch_dev.py -N -1 -n 1 -F *** -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 234 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 240 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 237 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 236 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Cv3.txt --runtime 24 --HLT_path HLT_DoubleMu  
# v4
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1593 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1578 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1602 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1577 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1600 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1584 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1575 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1596 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023C.txt --runtime 24 --HLT_path HLT_DoubleMu  

## 2023 D
# v1
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1190 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1200 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1204 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1206 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F **** -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu 
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1175 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1188 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 1176 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023Dv1.txt --runtime 24 --HLT_path HLT_DoubleMu  
## v2
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 224 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass0_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 225 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass1_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 218 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass2_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 219 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass3_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 222 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass4_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 229 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass5_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 219 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass6_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
#python3 scripts/submit_batch_dev.py -N -1 -n 1 -F 224 -p job_report --eos /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ data/data_reMini2023/ParkingDoubleMuonLowMass7_2023D.txt --runtime 24 --HLT_path HLT_DoubleMu  
