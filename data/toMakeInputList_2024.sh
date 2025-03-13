# script to create input .txt files

FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2025Mar06/'
SITE='eos'
OUT_PATH='data_PromptReco2024/'
FILE_TAG='tau3muNANO_data_2025Mar06_'

# 2024 B
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Bv1 -f $FILE_TAG 
# 2024 C 
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Cv1 -f $FILE_TAG -k 2
# 2024 D 
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Dv1 -f $FILE_TAG -k 2
# 2024 E
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Ev1 -f $FILE_TAG
# 2024 F 
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Fv1 -f $FILE_TAG -k 4
# 2024 G 
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Gv1 -f $FILE_TAG -k 5
# 2024 H 
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Hv1 -f $FILE_TAG 
# 2024 I
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Iv1 -f $FILE_TAG 

FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2025Mar12/'
FILE_TAG='tau3muNANO_data_2025Mar12_'
# 2024 E
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Ev2 -f $FILE_TAG 
# 2024 I
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2024 -e Iv2 -f $FILE_TAG 
