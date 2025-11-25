#!/bin/bash
TAG=ANv10
COMBINEDIR=$WORK/Combine-v10/CMSSW_14_1_0_pre4/src/tau3murun3_combination/Wchannel/unblind/${TAG}-bin/datacards
PLOTOUT=$WORK/Combine-v10/CMSSW_14_1_0_pre4/src/tau3murun3_combination/Wchannel/unblind/${TAG}-bin/plots
MULTIPDFSRC=multipdf-invID_wp-ANv10/multiPDF_workspaces
UNBLIND="--unblind"
#FIXPDF="--fixBestPdf"
BINNED="--binned"

python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_A22.root $FIXPDF -c A -y 22 --bdt_cut 0.9910 $UNBLIND $BINNED
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_B22.root $FIXPDF -c B -y 22 --bdt_cut 0.9940 $UNBLIND $BINNED
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_C22.root $FIXPDF -c C -y 22 --bdt_cut 0.9950 $UNBLIND $BINNED

python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_A23.root $FIXPDF -c A -y 23 --bdt_cut 0.9930 $UNBLIND $BINNED
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_B23.root $FIXPDF -c B -y 23 --bdt_cut 0.9930 $UNBLIND $BINNED
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --fix_w --sys_unc --save_ws --goff --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws $MULTIPDFSRC/multipdfs_vt3m_C23.root $FIXPDF -c C -y 23 --bdt_cut 0.9910 $UNBLIND $BINNED
