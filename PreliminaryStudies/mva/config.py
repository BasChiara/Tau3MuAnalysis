# WTau3Mu Run2 emulation
# useful global variables for python code

# Nexp = Lumi2022 * xs_Wmunu_X *Br(W->tau nu)/Br(W->mu nu) * r(POI) * Br(tau ->3mu)
# factor = Lumi2022/LumiMC

xs_Wmunu_X = 19870*1000 #[fb]
xs_Wmunu_X_err = xs_Wmunu_X*0.056 #[fb]

Br_WtauWnu_ratio = 1.008
Br_WtauWnu_ratio_err = 0.031 

Br_Tau3Mu_default = 1e-7

Lumi2022_D = 3.0063 
Lumi2022_E = 5.8783
Lumi2022_F = 18.0070
Lumi2022_G = 3.1219
Lumi2022_Serr = 0.022 
