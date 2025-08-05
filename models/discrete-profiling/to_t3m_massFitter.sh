COMBINEDIR=$WORK/Combine-v10/CMSSW_14_1_0_pre4/src/tau3murun3_combination/Wchannel/AN_results/ANv8-multipdf
PLOTOUT=$WWW/Tau3MuRun3//BPH-24-010_review/multipdf-ANv8/workingpoints/
TAG=ANv8-multipdf

python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-ANv8/multiPDF_workspaces/multipdfs_vt3m_A22.root -c A -y 22 --bdt_cut 0.9970
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-ANv8/multiPDF_workspaces/multipdfs_vt3m_B22.root -c B -y 22 --bdt_cut 0.9960
python3 t3m_massFitter.py --plot_outdir $PLOTOUT --goff --sys_unc --save_ws --combine_dir $COMBINEDIR --tag $TAG -b multipdf --multipdf_ws multipdf-ANv8/multiPDF_workspaces/multipdfs_vt3m_C22.root -c C -y 22 --bdt_cut 0.9950
