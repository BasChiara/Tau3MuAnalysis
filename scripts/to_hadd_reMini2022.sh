#
#   make the hadd of data files
#

python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Cv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Dv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Dv2 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Ev1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Fv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e Gv1 -a WTau3Mu_DATAanalyzer --hlt HLT_DoubleMu 
