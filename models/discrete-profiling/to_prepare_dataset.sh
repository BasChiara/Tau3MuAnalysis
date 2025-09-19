# !/bin/bash

OUTDIR=data-postBDT/invID-WP

# 2022
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c A -y 22 --bdt_cut 0.991
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c B -y 22 --bdt_cut 0.994
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c C -y 22 --bdt_cut 0.995
# 2023
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c A -y 23 --bdt_cut 0.993
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c B -y 23 --bdt_cut 0.993
python3 prepare_dataset.py --outdir $OUTDIR --save_ws --tag invID-mu2mu3 -c C -y 23 --bdt_cut 0.988