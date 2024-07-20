# submit on condor both BDT hyperparameters optimization and training
#-L 1.4 -L 1.5 -L 1.7 -L 1.9 -L 2.0 -L 2.1

python3 scripts/submitOptuna_onCondor.py -s /eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBinput_signal_kFold_HLT_overlap_LxyS0.0_2024Jun24.root -d /eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBinput_data_kFold_HLT_overlap_LxyS0.0_2024Jun24.root -L 2.0 -T 100 --workdir ./mva/ --tag HLT_overlap --plot_outdir /eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/cut_LxySign/ --cpu 1 --runtime 24
