# script to create input .txt files

FILE_PATH='/pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2023_2024Jan24/'
SITE='T2_IT_Rome'

FILE_PATH='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug03/'
SITE='eos'
OUT_PATH='data_reMini2023/'
FILE_TAG='tau3muNANO_data_2024Aug03_'

# 2023 B
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Bv1 -f $FILE_TAG 
# 2023 C 
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Cv1 -f $FILE_TAG 
# (v2)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Cv2 -f $FILE_TAG 
# (v3)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Cv3 -f $FILE_TAG 
# (v4)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Cv4 -f $FILE_TAG -k 2 
# 2023 D 
# (v1)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Dv1 -f $FILE_TAG -k 2 
# (v2)
python3 makeNanoAOD_inputLists.py -p ${FILE_PATH} -s $SITE -o ${OUT_PATH}/ -y 2023 -e Dv2 -f $FILE_TAG 
