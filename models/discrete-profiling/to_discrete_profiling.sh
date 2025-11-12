#!/bin/bash

OUTDIR="multipdf-invID_wp-thesis"
INDIR="data-postBDT/invID-WP-thesis"

# - 2022 -
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_A22_bdt0.9910_invID-mu2mu3_blind.root --outdir $OUTDIR -c A -y 22 --bdt_cut 0.991
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_B22_bdt0.9940_invID-mu2mu3_blind.root --outdir $OUTDIR -c B -y 22 --bdt_cut 0.994
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_C22_bdt0.9950_invID-mu2mu3_blind.root --outdir $OUTDIR -c C -y 22 --bdt_cut 0.995

# - 2023 -
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_A23_bdt0.9930_invID-mu2mu3_blind.root --outdir $OUTDIR -c A -y 23 --bdt_cut 0.993
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_B23_bdt0.9930_invID-mu2mu3_blind.root --outdir $OUTDIR -c B -y 23 --bdt_cut 0.993
python3 discrete_profiling.py --inputworkspace ${INDIR}/data_vt3m_C23_bdt0.9880_invID-mu2mu3_blind.root --outdir $OUTDIR -c C -y 23 --bdt_cut 0.988