#
#   make the hadd of data files
#

python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e F
python3 hadd_files.py -p /eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/ -e G --skip_files 4
