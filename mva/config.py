# WTau3Mu Run2 emulation
# useful global variables for python code
from collections import OrderedDict
import numpy  as np
import pandas as pd


###                        ###
#  MONTECARLO NORMALIZATION  #
###                        ###

# Nexp = Lumi2022 * xs_Wmunu_X *Br(W->tau nu)/Br(W->mu nu) * r(POI) * Br(tau ->3mu)
# factor = Lumi2022/LumiMC

xs_Wmunu_X = 63199.9 /3.*1000 #[fb] [MADGRAPH] - from AN2022_153 [SMP-20-004]
xs_Wmunu_X_err = 0.0 #[fb] don't know Madgraph unc.

Br_WtauWnu_ratio = 1.008
Br_WtauWnu_ratio_err = 0.031 

Br_Tau3Mu_default = 1e-7
# Lumi 2022
Lumi2022_C =  4.979
Lumi2022_D =  2.952
Lumi2022_E =  5.80
Lumi2022_F = 17.778
Lumi2022_G =  3.071 

Lumi2022_preEE  = Lumi2022_D
Lumi2022_EE     = Lumi2022_E+Lumi2022_F+Lumi2022_G
Lumi2022_reMini = Lumi2022_F+Lumi2022_G

Lumi2022_Serr = 0.022

# Lumi 2023
Lumi2023_B = 0.600 
Lumi2023_C = 9.909
Lumi2023_D = 1.669

Lumi2023_preBPix = Lumi2023_B + Lumi2023_C
Lumi2023_BPix = Lumi2023_D

Lumi2023_Serr = 0.0

# --- MC
Nev_MC_2022preEE = 197789
Nev_MC_2022EE    = 792640 
Nev_MC_2023preBPix = 0 
Nev_MC_2023BPix    = 0 
Filter_eff       = 1.0

# --- MC Luminosity
Lumi_MC_2022preEE  = Nev_MC_2022preEE/(Filter_eff * xs_Wmunu_X * Br_Tau3Mu_default)
Lumi_MC_2022EE  = Nev_MC_2022EE/(Filter_eff * xs_Wmunu_X * Br_Tau3Mu_default)
Lumi_MC_2023preBPix  = Nev_MC_2023preBPix/(Filter_eff * xs_Wmunu_X * Br_Tau3Mu_default)
Lumi_MC_2023BPix  = Nev_MC_2023BPix/(Filter_eff * xs_Wmunu_X * Br_Tau3Mu_default)


# --- NORM FACTOR TO USE 

MC_norm_factor_dict = {
   '2022EE' : Lumi2022_EE/Lumi_MC_2022EE,
   '2022reMini' : Lumi2022_reMini/Lumi_MC_2022EE,
}


###                ###
#  TAU MASS REGIONS  #
###                ###
mass_range_lo  = 1.60 # GeV
mass_range_hi  = 2.00 # GeV
blind_range_lo = 1.72 # GeV
blind_range_hi = 1.84 # GeV

###                     ###
#  CATEGORIES DEFINITION  #
###                     ###

cat_selection_dict = {
    'A' : '(tau_fit_mass_err/tau_fit_mass < 0.007)',
    'B' : '(tau_fit_mass_err/tau_fit_mass >= 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012)',
    'C' : '(tau_fit_mass_err/tau_fit_mass >= 0.012)'
}

##############
#    BDT     #
##############
# give labels human readable names
# IMPORTANT : same order as features!!!
labels = OrderedDict()

labels['tau_fit_pt'         ] = '$\\tau$ $p_{T}$'
labels['tau_fit_mt'         ] = '$m_{T}(\\tau, MET)$'
labels['tau_relIso'         ] = '$\\tau$ iso'
labels['tau_met_Dphi'       ] = '$\Delta\phi(\\tau MET)$'
labels['tau_met_pt'         ] = 'MET $p_{T}$'
labels['tau_met_ratio_pt'   ] = '$\\tau$ $p_{T}$/MET $p_{T}$' # only for >= v2
labels['W_pt'               ] = 'W $p_{T}$'
labels['miss_pz_min'        ] = '$min(ME_z^i)$'
labels['miss_pz_max'        ] = '$max(ME_z^i)$'
labels['tau_mu12_dZ'        ] = '$\Delta z (\mu_1, \mu_2)$'
labels['tau_mu13_dZ'        ] = '$\Delta z (\mu_1, \mu_3)$'
labels['tau_mu23_dZ'        ] = '$\Delta z (\mu_2, \mu_3)$'
labels['tau_Lxy_sign_BS'    ] = 'SV L/$\sigma$'
labels['tau_fit_vprob'      ] = 'SV prob'
labels['tau_cosAlpha_BS'    ] = 'SV cos($\\theta_{IP}$)'
labels['tau_mu1_TightID_PV' ] = '$\mu_1$ ID'
labels['tau_mu2_TightID_PV' ] = '$\mu_2$ ID'
labels['tau_mu3_TightID_PV' ] = '$\mu_3$ ID'
##labels['tau_fit_eta'        ] = '$\eta_{\\tau}$'
labels['tauEta'             ] = '$|\eta_{\\tau}|$'
##labels['bdt'                ] = 'BDT score'
labels['bdt_score'          ] = 'BDT score'
labels['tau_fit_mass'       ] = '$\\tau$ mass'

features = [
    'tau_fit_pt',
    'tau_fit_mt',
    'tau_relIso',
    'tau_met_Dphi',
    'tau_met_pt',
    'tau_met_ratio_pt',
    'W_pt',
    'miss_pz_min',
    'miss_pz_max',
    'tau_mu12_dZ',
    'tau_mu13_dZ',
    'tau_mu23_dZ',
    'tau_Lxy_sign_BS',
    'tau_fit_vprob',
    'tau_cosAlpha_BS',
    'tau_mu1_TightID_PV',
    'tau_mu2_TightID_PV',
    'tau_mu3_TightID_PV',
]

branches = features + [
    'tau_fit_charge',
    'tau_fit_mass', 'tau_fit_mass_err',
    'tau_fit_eta',
    'tau_mu12_M',
    'tau_mu23_M',
    'tau_mu13_M',
    'tau_mu1_SoftID_PV', 'tau_mu1_SoftID_BS', 'tau_mu1_LooseID',
    'tau_mu1_SoftID_PV', 'tau_mu2_SoftID_BS', 'tau_mu2_LooseID',
    'tau_mu1_SoftID_PV', 'tau_mu3_SoftID_BS', 'tau_mu3_LooseID',
]

###        ##
#  ETA BINS #
###        ##
@np.vectorize
def tauEta(eta):
   if   abs(eta) > 2.1 : return 7
   elif abs(eta) > 1.8 : return 6
   elif abs(eta) > 1.5 : return 5
   elif abs(eta) > 1.1 : return 4
   elif abs(eta) > 0.8 : return 3
   elif abs(eta) > 0.5 : return 2
   elif abs(eta) > 0.2 : return 1
   else                : return 0

### ----- features Nbins xlow xhigh ---- ###

features_NbinsXloXhiLabel = {
    'tau_fit_pt'        : [ 40, 0, 80,  'p_{T}(3 #mu) (GeV)'],
    'tau_fit_mt'        : [ 90, 0, 180, 'M_{T}(3 #mu)'],
    'tau_relIso'        : [ 50, 0, 0.5, 'rel. Isolation (3 #mu)'],
    'tau_met_Dphi'      : [ 63, 0, 6.3, '#Delta #phi (3 #mu, MET)'],
    'tau_met_pt'        : [ 75, 0, 150.,'MET (GeV)'],
    'tau_met_ratio_pt'  : [ 60, 0., 6., 'MET/p_{T}(3 #mu)'],
    'W_pt'              : [ 80, 0, 150, 'p_{T}(W) (GeV)'],
    'miss_pz_min'       : [100, -300, 300, 'min p_{z}^{#nu} (GeV)'],
    'miss_pz_max'       : [100,-1500, 1500,'max p_{z}^{#nu} (GeV)'],
    'tau_mu12_dZ'       : [ 30, 0, 0.3, '#Delta z (#mu_1, #mu_2)'],
    'tau_mu13_dZ'       : [ 30, 0, 0.3, '#Delta z (#mu_1, #mu_3)'],
    'tau_mu23_dZ'       : [ 30, 0, 0.3, '#Delta z (#mu_2, #mu_3)'],
    'tau_Lxy_sign_BS'   : [ 40, 0, 30,  'SV L_{xy}/#sigma'],
    'tau_fit_vprob'     : [ 20, 0,  1,  'SV probability'],
    'tau_cosAlpha_BS'   : [ 50,-1,  1,  'cos_{#alpha}(SV, BS)'],
    'tau_mu1_TightID_PV': [  2,-0.5,1.5, '#mu_1 ID'],
    'tau_mu2_TightID_PV': [  2,-0.5,1.5, '#mu_2 ID'],
    'tau_mu3_TightID_PV': [  2,-0.5,1.5, '#mu_3 ID'],
    'tauEta'            : [  8,-0.5,7.5, '3#mu #eta bins'],
    'tau_fit_eta'       : [ 70, -3.5, 3.5,'#eta (3 #mu)'],
    'tau_fit_mass'      : [ 40,1.6, 2.0, 'M(3 #mu)'],
    'bdt_score'         : [ 50, 0, 1,    'BDT score'],
}

###                ###
#  Ds->Phi(MuMu) Pi  #
###                ###
Ds_mass_range_lo  = 1.70 # GeV
Ds_mass_range_hi  = 2.10 # GeV

# -- translate features -- #
features_DsPhiPi = [
    'Ds_fit_pt',
    'Ds_fit_mt',
    'Ds_relIso',
    'tau_met_Dphi',
    'tau_met_pt',
    'tau_met_ratio_pt',
    'W_pt',
    'miss_pz_min',
    'miss_pz_max',
    'phi_mu12_dZ',
    'Ds_mu1pi_dZ',
    'Ds_mu2pi_dZ',
    'Ds_Lxy_sign_BS',
    'Ds_fit_vprob',
    'Ds_cosAlpha_BS',
    'phi_mu1_TightID_PV',
    'phi_mu2_TightID_PV',
    'pi_TightID',
]
features_DsPhiPi_to_Tau3Mu = dict(zip(features_DsPhiPi,features))


###                                   ###
#  TRANSLATE RUN2 <--> RUN3 VARIAVLES   #
###                                   ###
branches_Run2 = [
    'cand_refit_tau_pt',
    'cand_refit_tau_eta',
    'cand_refit_mttau',
    'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'cand_refit_dPhitauMET',
    'cand_refit_met_pt',
    'cand_refit_w_pt',
    'cand_refit_mez_1',
    'cand_refit_mez_2',
    'mu1_z',
    'mu2_z',
    'mu3_z',
    'tau_sv_ls',
    'tau_sv_prob',
    'tau_sv_cos',
    'mu1_refit_muonid_tight',
    'mu2_refit_muonid_tight',
    'mu3_refit_muonid_tight',
    'cand_refit_tau_mass',
]

features_Run2 = [
    'cand_refit_tau_pt',
    'cand_refit_mttau',
    'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'abs(cand_refit_dPhitauMET)',
    'cand_refit_met_pt',
    'cand_refit_tau_pt*(cand_refit_met_pt**-1)',
    'cand_refit_w_pt',
    'cand_refit_mez_1',
    'cand_refit_mez_2',
    'abs(mu1_z-mu2_z)',
    'abs(mu1_z-mu3_z)',
    'abs(mu2_z-mu3_z)',
    'tau_sv_ls',
    'tau_sv_prob',
    'tau_sv_cos',
    'mu1_refit_muonid_tight',
    'mu2_refit_muonid_tight',
    'mu3_refit_muonid_tight',
]

# [(key, value)
#          for i, (key, value) in enumerate(zip(test_keys, test_values))]

features_Run2toRun3 = dict(zip(features_Run2,features))

features_Run3toRun2 = {
    'tau_fit_pt'        :'cand_refit_tau_pt',
    'tau_fit_mt'        :'cand_refit_mttau',
    'tau_relIso'        :'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'tau_met_Dphi'      :'abs(cand_refit_dPhitauMET)',
    'tau_met_pt'        :'cand_refit_met_pt',
    'tau_met_ratio_pt'  :'cand_refit_tau_pt*(cand_refit_met_pt**-1)',
    'W_pt'              :'cand_refit_w_pt',
    'miss_pz_max'       :'cand_refit_mez_1',
    'miss_pz_min'       :'cand_refit_mez_2',
    'tau_mu12_dZ'       :'abs(mu1_z-mu2_z)',
    'tau_mu13_dZ'       :'abs(mu1_z-mu3_z)',
    'tau_mu23_dZ'       :'abs(mu2_z-mu3_z)',
    'tau_Lxy_sign_BS'   :'tau_sv_ls',
    'tau_fit_vprob'     :'tau_sv_prob',
    'tau_cosAlpha_BS'   :'tau_sv_cos',
    'tau_mu1_TightID_PV':'mu1ID',
    'tau_mu2_TightID_PV':'mu2ID',
    'tau_mu3_TightID_PV':'mu3ID',
    'tau_mu3_TightID_PV':'mu3ID',
}
