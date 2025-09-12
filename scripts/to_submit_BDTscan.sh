# /usr/bin/bash!
cd $T3M_ANA/Tau3MuAnalysis/

CATEGORY="ABC"
YEAR=("22")
INPUT_FOLDER=""

SIGNAL_SAMPLE="/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2025May22.root"
DATA_SAMPLE="/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/XGBout_invMedIDandSideBands_DATA_2022_invID-mu3_nT15k_invIDopen_reweight_reweighted.root"

WORKDIR="/afs/cern.ch/work/c/cbasile/Combine-v10/CMSSW_14_1_0_pre4/src/WTau3Mu_limits/bdt_cut_optimization/invID-mu3/"
PLOT_DIR="/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/features/invertedID-mu3/bdt_scan/"

YYYYMonDD="2025Sep04"
CUT_LIST=(2.0)
for CUT in ${CUT_LIST[@]}; do
    for Y in ${YEAR[@]}; do
        
        #echo -e ".... submitting jobs for LxyS > ${CUT} year 20${Y} ...."
        TAG="kFold_LxyS-sameffyear_${YYYYMonDD}"
        OUT_TAG="invID-mu3_${YYYYMonDD}"
        
        python3 scripts/submitBDTscan_onCondor.py -s $SIGNAL_SAMPLE -d $DATA_SAMPLE  --plot_outdir $PLOT_DIR --workdir $WORKDIR --tag $OUT_TAG --plot_outdir $PLOT_DIR --category $CATEGORY --year $Y --BDTmin 0.9850 --BDTmax 0.9990 --BDTstep 0.0010 --runtime 3 -c
        #python3 scripts/submitBDTscan_onCondor.py --runtime 3 -s ${INPUT_FOLDER}/XGBout_signal_${TAG}.root -d ${INPUT_FOLDER}/XGBout_data_${TAG}.root --workdir ${WORKDIR}/binBDT_${OUT_TAG} --tag $OUT_TAG --plot_outdir ${PLOT_DIR} --category $CATEGORY --year $Y --BDTmin 0.9850 --BDTmax 0.9990 --BDTstep 0.0010
    done
done