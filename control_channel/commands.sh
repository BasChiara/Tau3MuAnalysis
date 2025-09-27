#python3 DsPhiMuMuPi_fit.py --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9 --category ABC --year 2022
#python3 DsPhiMuMuPi_sPlot.py --input_workspace workspaces/DsPhiPi_wspace_catABC2022_ANv9.root -y 2022 --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9
#python3 DsPhiMuMuPi_sPlotter.py -i sWeight/sWeights_2022_ANv9_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/sPlots -y 2022 --tag ANv9

python3 DsPhiMuMuPi_fit.py --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9 --category ABC --year 2023
python3 DsPhiMuMuPi_sPlot.py --input_workspace workspaces/DsPhiPi_wspace_catABC2023_ANv9.root -y 2023 --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9
python3 DsPhiMuMuPi_sPlotter.py -i sWeight/sWeights_2023_ANv9_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/sPlots -y 2023 --tag ANv9
