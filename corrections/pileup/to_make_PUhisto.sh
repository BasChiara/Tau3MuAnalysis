# create PU histogram for MC and DATA
ERAS_LIST=("2022preEE" "2022EE" "2023preBPix" "2023BPix")
for ERA in ${ERAS_LIST[@]}; do
    echo -e "--- creating PU histogram for ${ERA}\n"
    python3 make_PUweights.py --era $ERA --mc_central --hist_only
    python3 make_PUweights.py --era $ERA --mc_mini --hist_only
    python3 make_PUweights.py --era $ERA --mc_nano --hist_only

    python3 comparePU_profiles.py --era $ERA

done
