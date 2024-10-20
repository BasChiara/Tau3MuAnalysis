# /usr/bin/bash!
cd $T3M_ANA/Tau3MuAnalysis/

CATEGORY="ABC"
YEAR=("22" "23")
INPUT_FOLDER="/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/"
WORKDIR="$COMBINEv10/WTau3Mu_limits/bdt_cut_optimization"
PLOT_DIR="/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/cut_LxySign/"

YYYYMonDD="2024Oct10"
CUT_LIST=(2.0)
for CUT in ${CUT_LIST[@]}; do
    for Y in ${YEAR[@]}; do
        
        echo -e ".... submitting jobs for LxyS > ${CUT} year 20${Y} ...."
        TAG="kFold_Optuna_HLT_overlap_apply_LxyS${CUT}_${YYYYMonDD}"
        OUT_TAG="LxyS${CUT}_Optuna_HLT_overlap_apply_$YYYYMonDD"

        python3 scripts/submitBDTscan_onCondor.py --runtime 3 -s ${INPUT_FOLDER}/XGBout_signal_${TAG}.root -d ${INPUT_FOLDER}/XGBout_data_${TAG}.root --workdir ${WORKDIR}/binBDT_${OUT_TAG} --tag $OUT_TAG --plot_outdir ${PLOT_DIR}/Training_${TAG}/bdt_scan/ --category $CATEGORY --year $Y --BDTmin 0.9850 --BDTmax 0.9990 --BDTstep 0.0010
    done
done
        
#echo -e ".... submitting jobs for LxyS > 0.0 year 20${Y} ...."
#TAG="kFold_HLT_overlap_limOT_${YYYYMonDD}"
#OUT_TAG="LxyS0.0_HLT_overlap_limOT_phiW40_$YYYYMonDD"
#python3 scripts/submitBDTscan_onCondor.py --runtime 3 -s ${INPUT_FOLDER}/XGBout_signal_${TAG}.root -d ${INPUT_FOLDER}/XGBout_data_${TAG}.root --workdir ${WORKDIR}/binBDT_${OUT_TAG} --tag $OUT_TAG --plot_outdir ${PLOT_DIR}/Training_${TAG}/bdt_scan/ --category $CATEGORY --year $Y --BDTmin 0.9700 --BDTmax 0.9980 --BDTstep 0.0020
