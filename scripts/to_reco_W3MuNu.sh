#!/usr/bin/bash
# run the reconstruction after preselection
# ./bin/Analyzer_app
#Allowed options:
#  -h [ --help ]                    produce help message
#  -i [ --input ] arg               input file list
#  -o [ --output ] arg (=./outRoot) output directory
#  -d [ --dataset ] arg             DATA - MC - file.root
#  -y [ --year ] arg                year-era
#  -a [ --analyzer ] arg (=Tau3Mu)  analyzer : [Tau3Mu,DsPhiPi]
#  -p [ --process ] arg (=data)     process: [data, Tau3Mu, DsPhiPi, W3MuNu]
#  -N [ --Nfiles ] arg (=1000)      number of files
#  -f [ --init_file ] arg (=0)      initial file
#  -t [ --tag ] arg                 tag

# 2022
./bin/Analyzer_app -i data/mc_reMini2022/MonteCarlo_W3MuNu_2022preEE.txt     -o outRoot/ -d MC -y 2022preEE     -p W3MuNu
./bin/Analyzer_app -i data/mc_reMini2022/MonteCarlo_W3MuNu_2022EE.txt        -o outRoot/ -d MC -y 2022EE        -p W3MuNu

# 2023
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023preBPix.txt   -o outRoot/ -d MC -y 2023preBPix   -p W3MuNu
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_W3MuNu_2023BPix.txt      -o outRoot/ -d MC -y 2023BPix      -p W3MuNu
