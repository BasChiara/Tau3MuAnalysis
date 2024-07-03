# Analysis (W) Tau -> 3 Mu Run3 
Analysis framework for tau3mu in W channel for Run3.\
This analysis uses CMS `nanoAOD` privately produced from CMS `miniAOD` and runs with `lxplus9`.

**Set up CMSSW release**
Download the CMSSW release and compile
```
cmsrel CMSSW_13_0_13
CMSSW_13_0_13/src/
cmsenv
git cms-init
scram b -j 8
```
**Clone this repository**
```
git init
git clone ...
```
**Running the code**
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
