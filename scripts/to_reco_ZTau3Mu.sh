#!/usr/bin/bash

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
./bin/Analyzer_app -i data/mc_reMini2022/MonteCarlo_ZTau3Mu_2022preEE.txt    -o outRoot/ -d MC -y 2022preEE      -a Tau3Mu -p ZTau3Mu
./bin/Analyzer_app -i data/mc_reMini2022/MonteCarlo_ZTau3Mu_2022EE.txt       -o outRoot/ -d MC -y 2022EE         -a Tau3Mu -p ZTau3Mu
# 2023
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_ZTau3Mu_2023preBPix.txt  -o outRoot/ -d MC -y 2023preBPix    -a Tau3Mu -p ZTau3Mu
./bin/Analyzer_app -i data/mc_reMini2023/MonteCarlo_ZTau3Mu_2023BPix.txt     -o outRoot/ -d MC -y 2023BPix       -a Tau3Mu -p ZTau3Mu
# 2024
./bin/Analyzer_app -i data/mc_PromptReco_2024/MonteCarlo_ZTau3Mu_2024.txt    -o outRoot/ -d MC -y 2024           -a Tau3Mu -p ZTau3Mu