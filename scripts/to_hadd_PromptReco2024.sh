#!/usr/bin/bash

#
#   make the hadd of data files
#
#python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Bv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Ev1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Ev2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Fv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Gv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Hv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Iv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/PromptReco2024/ -y 2024 -e Iv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
