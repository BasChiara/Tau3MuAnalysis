#
#   make the hadd of data files
#
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e B   -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu --skip_files 1 3
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv2 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu --skip_files 2 3
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv3 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu --skip_files 3
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e C   -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu --skip_files 4
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e D   -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu 
