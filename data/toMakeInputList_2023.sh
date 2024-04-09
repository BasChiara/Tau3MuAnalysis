# script to create input .txt files
# 2023 B
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2023_2024Jan24/ -o data_reMini2023/ -y 2023 -e B -f tau3muNANO_data_2024Jan24_ -j 240124_155628 240124_155633 240124_155637 240124_155642 240124_155646 240124_155651 240124_155656 240124_155700

# 2023 C 
# (v1)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2023/ -y 2023 -e Cv1 -f tau3muNANO_data_2024Jan29_ -j 240129_161840 000000_000000 240129_161901 000000_000000 240129_161919 240129_161929 240129_161939 240129_161948 
# (v2)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2023/ -y 2023 -e Cv2 -f tau3muNANO_data_2024Jan29_ -j 240129_161957 240129_162009 240129_162019 000000_000000 240129_162041 240129_162051 240129_162100 240129_162111 
# (v3)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2023/ -y 2023 -e Cv3 -f tau3muNANO_data_2024Jan29_ -j 240129_162118 240129_162126 240129_162136 000000_000000 240129_162155 240129_162205 240129_162213 240129_162221 
# (v4)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2023_2024Jan24/ -o data_reMini2023/ -y 2023 -e C -f tau3muNANO_data_2024Jan24_ -j 240124_155704 240124_155709 240124_155713 240124_155718 240124_155723 240124_155727 240124_155731 240124_155736 -k 2 

# 2023 D 
# (v1)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2023/ -y 2023 -e Dv1 -f tau3muNANO_data_2024Jan29_ -j 240129_162859 240129_162909 240129_162918 240129_162931 000000_000000 240129_162951 240129_163003 240129_163018 -k 2
# (v2)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2023_2024Jan24/ -o data_reMini2023/ -y 2023 -e D -f tau3muNANO_data_2024Jan24_ -j 240124_161131 240124_161136 240124_161140 240124_161145 240124_161149 240124_161153 240124_161158 240124_161202
