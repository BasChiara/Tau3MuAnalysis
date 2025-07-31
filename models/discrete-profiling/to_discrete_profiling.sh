OUTDIR="multipdf-ANv8"

# - 2022 -
python3 discrete_profiling.py --inputworkspace data-postBDT/data_bdt0.9970_vt3m_A22_wpANv8_blind.root --outdir $OUTDIR -c A -y 22 --bdt_cut 0.997
python3 discrete_profiling.py --inputworkspace data-postBDT/data_bdt0.9960_vt3m_B22_wpANv8_blind.root --outdir $OUTDIR -c B -y 22 --bdt_cut 0.996
python3 discrete_profiling.py --inputworkspace data-postBDT/data_bdt0.9950_vt3m_C22_wpANv8_blind.root --outdir $OUTDIR -c C -y 22 --bdt_cut 0.995