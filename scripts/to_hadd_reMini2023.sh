#!/usr/bin/bash

#
#   make the hadd of data files
#
DESTDIR=/eos/cms/store/group/phys_bphys/cbasile/Tau3MuFlat_2025Sep30/reMini2023/

python3 hadd_files.py -p $DESTDIR -y 2023 -e Bv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p $DESTDIR -y 2023 -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap --skip_files 1
python3 hadd_files.py -p $DESTDIR -y 2023 -e Cv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p $DESTDIR -y 2023 -e Cv3 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p $DESTDIR -y 2023 -e Cv4 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p $DESTDIR -y 2023 -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
python3 hadd_files.py -p $DESTDIR -y 2023 -e Dv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
