Here you find some standalone codes to fit S+B models for tau -> 3 mu analysis

# Fit 3 muon mass distribution
The `Tau3Mu_fitSB.py` scripts fits the MC and DATA for the tau -> 3 mu decay. You want to use different BDT cuts and shapes for different categories A, B, and C.
To fit category A 2022 run :
```
python3 Tau3Mu_fitSB.py --plot_outdir [directory] --tag [tag_output] --category A -y 22 --bdt_cut 0.9947 --save_ws
```
produces a fit to the MC signal (normalized to data lumi) and a fit to the data sidebands to extrapolate the signal & background yield, respectively. Also it produce the datacard and the workespace and saves them in `combine_input`. Use the m as inputs to combine to compute the UL. 
