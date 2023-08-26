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
root [0] .L plots/plot_library.C
root [1] .x plots/makeMCstudies_plots.c
```
