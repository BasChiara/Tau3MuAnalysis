# Preliminary Analysis Tau -> 3 Mu
before compiling 
```
mkdir lib
mkdir bin
mkdir outRoot
```
make MonteCarlo plots
```
make gen
./bin/analysisGenLevel data/MonteCarlo_2022preEE.txt 2022_preEE
root -l -b
[1] .L plots/plot_library.C
[2] .x plots/makeMCstudies_plots.c
```
