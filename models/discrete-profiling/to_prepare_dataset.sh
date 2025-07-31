OUTDIR=data-postBDT

# 2022
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c A -y 22 --bdt_cut 0.997
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c B -y 22 --bdt_cut 0.996
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c C -y 22 --bdt_cut 0.995
# 2023
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c A -y 23 --bdt_cut 0.987
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c B -y 23 --bdt_cut 0.996
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag wpANv8 -c C -y 23 --bdt_cut 0.992