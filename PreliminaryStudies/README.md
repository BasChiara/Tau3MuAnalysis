# Preliminary Analysis Tau -> 3 Mu
before compiling 
```
mkdir lib
mkdir bin
mkdir outRoot
```
run on MonteCarlo & make plots
```
make gen
./bin/analysisGenLevel data/MonteCarlo_2022preEE.txt 2022_preEE
root -l -b
root [0] .L plots/plot_library.C
root [1] .x plots/makeMCstudies_plots.c
```
run on data
```
make reco
./bin/RecoLevelAnalysis data/ParkingDoubleMuonLowMass0_2022E.txt ./outRoot/ Data_2022_E0 [Nfiles]
```
