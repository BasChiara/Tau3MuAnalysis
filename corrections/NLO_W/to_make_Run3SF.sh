#! /bin/bash

OUTFILE="SF_source/W_NLOvsT3m_Run3.root"
rm $OUTFILE

ERAS_LIST=("2022preEE" "2022EE" "2023preBPix" "2023BPix")

for ERA in ${ERAS_LIST[@]}; do
    echo " ------ $ERA ------ "
    python3 NLOweight_producer.py --input SF_source/W_NLOvsT3m_${ERA}.root --year $ERA --output $OUTFILE
done