#!/bin/bash
COMBINEDIR=$WORK/Combine-v10/CMSSW_14_1_0_pre4/src/tau3murun3_combination/Wchannel/AN_results/ANv9/datacards
PLOTOUT=$WORK/Combine-v10/CMSSW_14_1_0_pre4/src/tau3murun3_combination/Wchannel/AN_results/ANv9/plots
TAG=ANv9
#UNBLIND="--unblind"
#FIXPDF="--fixBestPdf"

python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_A22.root $FIXPDF -c A -y 22 --bdt_cut 0.9910 $UNBLIND
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_B22.root $FIXPDF -c B -y 22 --bdt_cut 0.9940 $UNBLIND
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_C22.root $FIXPDF -c C -y 22 --bdt_cut 0.9950 $UNBLIND

python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_A23.root $FIXPDF -c A -y 23 --bdt_cut 0.9930 $UNBLIND
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_B23.root $FIXPDF -c B -y 23 --bdt_cut 0.9930 $UNBLIND
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --fix_w --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-invID_wp/multiPDF_workspaces/multipdfs_vt3m_C23.root $FIXPDF -c C -y 23 --bdt_cut 0.9880 $UNBLIND
