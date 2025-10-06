#!/usr/bin/bash

#   make the hadd of data files
DESTDIR=/eos/cms/store/group/phys_bphys/cbasile/Tau3MuFlat_2025Sep30/reMini2022/

python3 hadd_files.py -p $DESTDIR -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p $DESTDIR -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p $DESTDIR -e Dv2 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p $DESTDIR -e Ev1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p $DESTDIR -e Fv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap
python3 hadd_files.py -p $DESTDIR -e Gv1 -a WTau3Mu_DATAanalyzer --hlt HLT_overlap 
