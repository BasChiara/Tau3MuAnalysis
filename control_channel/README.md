## Validation with control channel $D_s \to \phi (\mu\mu) \pi$
The event selection is defined in `mva/config.py` library and automatically parsed by the scripts
```
(Ds_fit_mass > 1.75 & Ds_fit_mass < 2.05 ) & (phi_fit_mass > 0.98 & phi_fit_mass < 1.05 ) & (tau_Lxy_sign_BS > 2.0 & tau_fit_vprob > 0.1 )
```
### 1. Fit $D_s$ resonance
Fit the $\mu\mu\pi$ invariant mass distribution and save the workspace in the `/workspaces/` folder.</br>
For example to run the fit on 2022 data and MC:
```
mkdir -p workspaces 
python3 DsPhiMuMuPi_fit.py -y 2022 --plot_outdir [directory] --category ABC --tag [nice_name]
```
The fit results are stored in the workspaces saved in `workspaces/DsPhiPi_wspace_catABC2022_[nice_name].root` file, for both data and MC.

> ⚠️ **Top-up** to run over 2024 you must use input files that are not in the `mva/config.py` so run with 
> ```
> mkdir -p workspaces 
> python3 DsPhiMuMuPi_fit.py -y 2024 --plot_outdir [directory] --category ABC --tag [nice_name] -s /eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/topup/XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root  -d /eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/topup/XGBout_DsPhiMuMuPi_DATA_2024only_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root
> ```

### 2. Produce sPlots
The workspace produced in the previous point is used to calculate the sWeights for the background subtraction to data
```
python3 DsPhiMuMuPi_sPlot.py --input_workspace workspaces/DsPhiPi_wspace_catABC2022_[nice_name].root  -y 2022 --plot_outdir [directory]
```
The results are stored in `control_channel/sWeight/sWeights_2022_[nice_name]_DataMc.root`. The file contains 
- `mc_tree` : tree for MC events, the `norm_factor` branch stores the normalization factor to the Ds yield in data
- `RooTreeDataStore_sData_data_fit`  : tree for s-weighted data events, the `nDs_sw` contains the per-event sWeight

### 3. Draw sPlots for DATA/MC comparison
Produce sPlot for Data/MC comparison for all the input features to the BDT and the BDT score. Also re-produce sPlots after reweighting the MC to correct the Data/MC disagreement observed in the $D_s$ pseudorapidity.
```
python3 DsPhiMuMuPi_sPlotter.py -i control_channel/sWeight/sWeights_2022_[nice_name]_DataMc.root --plot_outdir [directory] -y 2022 --tag [nice_name]
```