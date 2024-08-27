#!/usr/bin/bash

#
#   make the hadd of data files
#
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Bv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap --skip_files 1
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv3 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Cv4 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -e Dv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
