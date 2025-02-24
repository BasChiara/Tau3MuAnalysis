
# Run2022
# -- L1
python3 efficiency_handling.py --input Run2022/NUM_HLT_Mu0_L1DoubleMu_DEN_HLT_Mu8_abseta_pt.root --output Run2022/L1_efficiency_abseta_pt.root --cut_ncount Run2022/NUM_HLT_Mu0_L1DoubleMu_DEN_HLT_Mu8_cutNcount_abseta_pt.root --trigger L1 --sysname AltBkg --year 2022
# -- HLT
python3 efficiency_handling.py --input Run2022/NUM_HLT_DoubleMu4_3_LowMass_DEN_HLT_Mu4_L1DoubleMu_abseta_pt.root --output Run2022/HLT_efficiency_abseta_pt.root --cut_ncount Run2022/NUM_HLT_DoubleMu4_3_LowMass_DEN_HLT_Mu4_L1DoubleMu_cutNcount_abseta_pt.root --trigger HLT --sysname AltBkg --year 2022

# Run2023
# -- L1
python3 efficiency_handling.py --input Run2023/NUM_HLT_Mu0_L1DoubleMu_DEN_HLT_Mu8_abseta_pt.root --output Run2023/L1_efficiency_abseta_pt.root --cut_ncount Run2023/NUM_HLT_Mu0_L1DoubleMu_DEN_HLT_Mu8_cutNcount_abseta_pt.root --trigger L1 --sysname AltBkg  --year 2023
# -- HLT
python3 efficiency_handling.py --input Run2023/NUM_HLT_DoubleMu4_3_LowMass_DEN_HLT_Mu4_L1DoubleMu_abseta_pt.root --output Run2023/HLT_efficiency_abseta_pt.root --cut_ncount Run2023/NUM_HLT_DoubleMu4_3_LowMass_DEN_HLT_Mu4_L1DoubleMu_cutNcount_abseta_pt.root --trigger HLT --sysname AltBkg  --year 2023
