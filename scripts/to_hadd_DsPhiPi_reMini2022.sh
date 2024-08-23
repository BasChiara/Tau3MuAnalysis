#!/usr/bin/bash

# hadd reco data files 

python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Cv1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Dv2 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Dv1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Ev1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Fv1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_eosbkp/ -t 2022 -a DsPhiMuMuPi_DATAanalyzer -e Gv1 --hlt HLT_overlap
