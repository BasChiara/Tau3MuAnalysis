# script to create input .txt files

#FILE_PATH='/pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/'
#SITE='T2_IT_Rome'

SITE='eos'
OUT_PATH='data_reMini2022/'

FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug06/'
FILE_TAG='tau3muNANO_data_2024Aug06_'
# 2022 C 
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Cv1 -f $FILE_TAG -k 2
# 2022 D 
# (v1)
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Dv1 -f $FILE_TAG 
# (v2)
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Dv2 -f $FILE_TAG 
FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug05/'
FILE_TAG='tau3muNANO_data_2024Aug05_'
# 2022 E 
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Ev1 -f $FILE_TAG -k 2 
# 2022 F
FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug02/'
FILE_TAG='tau3muNANO_data_2024Aug02_'
# v1
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Fv1 -f $FILE_TAG -k 3 
# 2022 G
# v1
python3 makeNanoAOD_inputLists.py -p $FILE_PATH -s $SITE -o $OUT_PATH -y 2022 -e Gv1 -f $FILE_TAG 
