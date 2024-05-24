#!/usr/bin/bash

# hadd reco data files 

python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Cv1
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Dv1
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Dv2
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Ev1
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Fv1
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -a DsPhiMuMuPi_DATAanalyzer -e Gv1 
