#!/usr/bin/bash

# hadd reco data files 

python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Bv1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Cv1 --hlt HLT_overlap --skip_files 1
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Cv2 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Cv3 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Cv4 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Dv1 --hlt HLT_overlap
python3 scripts/hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/ -y 2023 -a DsPhiMuMuPi_DATAanalyzer -e Dv2 --hlt HLT_overlap
