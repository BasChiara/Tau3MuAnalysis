#!/usr/bin/bash
# run the reconstruction after preselection

# 2022 pre-EE
./bin/Analyzer_app -i data/mc_reMini2022/MonteCarlo_W3MuNu_2022preEE.txt -o outRoot/ -d MC -y 2022preEE -p W3MuNu
# 2022 post-EE
# 2023 pre BPix
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023preBPix.txt -o outRoot/ -d MC -y 2023preBPix -p W3MuNu
# 2023 post BPix
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023BPix.txt -o outRoot/ -d MC -y 2023BPix -p W3MuNu
