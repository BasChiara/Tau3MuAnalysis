# script to create input .txt files

# 2022 C 
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2022/ -y 2022 -e Cv1 -f tau3muNANO_data_2024Jan29_ -j 240129_121043 240129_121104 240129_121125 240129_121142 240129_121201 240129_121219 240129_121238 240129_121256 -k 2 

# 2022 D 
# (v1)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2022/ -y 2022 -e Dv1 -f tau3muNANO_data_2024Jan29_ -j 240129_121316 240129_121336 240129_121356 240129_121415 240129_121441 240129_121459 240129_121520 240129_121543 
# (v2)
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2022/ -y 2022 -e Dv2 -f tau3muNANO_data_2024Jan29_ -j 240129_121601 240129_121620 240129_121639 240129_121659 240129_121718 240129_121737 240129_121756 240129_121816 

# 2022 E 
python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2024Jan29/ -o data_reMini2022/ -y 2022 -e Ev1 -f tau3muNANO_data_2024Jan29_ -j 240129_174957 240129_175022 240129_175045 240129_175110 240129_175133 240129_175156 240129_175222 240129_175245 -k 2 

# 2022 F
# v1
#python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/user/crovelli/ -o data_reMini2022/ -y 2022 -e Fv1 -f tau3muNANO_data_2024Jan25_ -j 240125_110724 240125_110728 240125_110732 240125_110737 240125_110742 240125_110748 240125_110752 240125_110756 -k 3

# 2022 G
# v1
#python3 makeNanoAOD_inputLists.py -p /pnfs/roma1.infn.it/data/cms/store/user/crovelli/ -o data_reMini2022/ -y 2022 -e Gv1 -f tau3muNANO_data_2024Jan25_ -j 240125_110815 240125_110819 240125_110825 240125_110829 9999_9999 240125_110838 240125_110842 240125_110846 
