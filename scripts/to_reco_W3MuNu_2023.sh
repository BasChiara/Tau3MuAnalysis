# run the reconstruction after preselection on W3MuNu MC sample
# 2023 pre BPix
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023preBPix.txt -o outRoot/ -d MC -y 2023preBPix -p W3MuNu
# 2023 post BPix
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023BPix.txt -o outRoot/ -d MC -y 2023BPix -p W3MuNu
