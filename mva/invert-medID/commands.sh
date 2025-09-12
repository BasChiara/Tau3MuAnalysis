
SIGNAL_FILE=$EOS/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2025May22.root
DATA_FILE=invID-mu2mu3/fit_input/t3m_Hmass_2023.root
PLOTDIR=$WWW/Tau3Mu_Run3/BDTtraining/features/invertedID-mu2mu3/2023/bdt_scan/
COMBINEDIR=/afs/cern.ch/work/c/cbasile/Combine-v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/bdt_cut_optimization/invID-mu2mu3/2023/input_combine
YEAR=23
TAG=invID-mu2mu3

# -- CAT A
python3 mass_fitter.py -s $SIGNAL_FILE -d $DATA_FILE --plot_outdir $PLOTDIR --goff --fix_w --save_ws --combine_dir $COMBINEDIR --tag $TAG -c A -y $YEAR --BDTmin 0.985 --BDTmax 0.999 --BDTstep 0.001 --optim_bdt --unblind
# -- CAT B
python3 mass_fitter.py -s $SIGNAL_FILE -d $DATA_FILE --plot_outdir $PLOTDIR --goff --fix_w --save_ws --combine_dir $COMBINEDIR --tag $TAG -c B -y $YEAR --BDTmin 0.985 --BDTmax 0.999 --BDTstep 0.001 --optim_bdt --unblind
# -- CAT C
python3 mass_fitter.py -s $SIGNAL_FILE -d $DATA_FILE --plot_outdir $PLOTDIR --goff --fix_w --save_ws --combine_dir $COMBINEDIR --tag $TAG -c C -y $YEAR --BDTmin 0.985 --BDTmax 0.999 --BDTstep 0.001 --optim_bdt --unblind