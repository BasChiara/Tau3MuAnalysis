python3 DsPhiMuMuPi_fit.py              --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/ --tag ANv10 --category ABC --year 2022
python3 DsPhiMuMuPi_sWeight.py          --input_workspace workspaces/DsPhiPi_wspace_catABC2022_ANv10.root -y 2022 --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/ --tag ANv10
python3 DsPhiMuMuPi_sPlotter-slim.py    -i $EOS/Tau3MuRun3/data/control_channel/sWeight/sWeights_2022_ANv10_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/  -y 2022 --tag ANv10
python3 DsPhiMuMuPi_toWTau3Mu.py        -i $EOS/Tau3MuRun3/data/control_channel/sWeight/sWeights_2022_ANv10_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/  -y 2022 --tag ANv10

python3 DsPhiMuMuPi_fit.py              --plot_outdir plots/test-ANv10 --tag test-ANv10 --category ABC --year 2023
python3 DsPhiMuMuPi_sWeight.py          --input_workspace workspaces/DsPhiPi_wspace_catABC2023_test-ANv10.root -y 2023  --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/ --tag ANv10
python3 DsPhiMuMuPi_sPlotter-slim.py    -i $EOS/Tau3MuRun3/data/control_channel/sWeight/sWeights_2023_ANv10_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/  -y 2023 --tag ANv10
python3 DsPhiMuMuPi_toWTau3Mu.py        -i $EOS/Tau3MuRun3/data/control_channel/sWeight/sWeights_2023_ANv10_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv10/  -y 2023 --tag ANv10








#python3 DsPhiMuMuPi_fit.py --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9 --category ABC --year 2022
#python3 DsPhiMuMuPi_sPlot.py --input_workspace workspaces/DsPhiPi_wspace_catABC2022_ANv9.root -y 2022 --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9
#python3 DsPhiMuMuPi_sPlotter.py -i sWeight/sWeights_2022_ANv9_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/sPlots -y 2022 --tag ANv9
#
#python3 DsPhiMuMuPi_fit.py --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9 --category ABC --year 2023
#python3 DsPhiMuMuPi_sPlot.py --input_workspace workspaces/DsPhiPi_wspace_catABC2023_ANv9.root -y 2023 --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/ --tag ANv9
#python3 DsPhiMuMuPi_sPlotter.py -i sWeight/sWeights_2023_ANv9_DataMc.root --plot_outdir $WWW/Tau3Mu_Run3/DsPhiMuMuPi/ANv9/sPlots -y 2023 --tag ANv9
