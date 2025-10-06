# WTau3Mu Run3 developement
# useful global variables for python code
from collections import OrderedDict
import numpy  as np
import os
import ROOT

###                ###
#    W->tau(3mu)nu   #
###                ###
tau_mass       = 1.777 #GeV
mass_range_lo  = 1.40 # GeV
mass_range_hi  = 2.05 # GeV
blind_range_lo = 1.72 # GeV
blind_range_hi = 1.84 # GeV

###                ###
#  Ds->Phi(MuMu) Pi  #
###                ###
Ds_mass = 1.9678 # GeV
D_mass  = 1.8693 # GeV
Ds_mass_range_lo  = 1.75 # GeV
Ds_mass_range_hi  = 2.05 # GeV

###                ###
#   EVENT SELECTION  #
###  at mva level  ###
Phi_mass_, Phi_window_ = 1.019, 6*0.013
Omega_mass_, Omega_window_ = 0.780, 6*0.012
LxySign_cut    = 2.0
Ds_phi_mass_lo, Ds_phi_mass_hi = 0.98, 1.06
Ds_minSVprob = 0.001

# tau->3mu
base_selection      = f'(tau_fit_mass > {mass_range_lo} & tau_fit_mass < {mass_range_hi} ) & (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu)'
phi_veto            = '''(fabs(tau_mu12_fitM- {mass:.3f})> {window:.3f} & fabs(tau_mu23_fitM - {mass:.3f})> {window:.3f} & fabs(tau_mu13_fitM -  {mass:.3f})>{window:.3f})'''.format(mass =Phi_mass_ , window = Phi_window_/2. )
omega_veto          = '''(fabs(tau_mu12_fitM- {mass:.3f})> {window:.3f} & fabs(tau_mu23_fitM - {mass:.3f})> {window:.3f} & fabs(tau_mu13_fitM -  {mass:.3f})>{window:.3f})'''.format(mass =Omega_mass_ , window = Omega_window_/2. )
sidebands_selection = f'((tau_fit_mass < {blind_range_lo} )|| (tau_fit_mass > {blind_range_hi}))'
displacement_selection = f'(tau_Lxy_sign_BS > {LxySign_cut})'

# Ds->Phi(MuMu)Pi
Ds_base_selection   = f'(Ds_fit_mass > {Ds_mass_range_lo} & Ds_fit_mass < {Ds_mass_range_hi} )' #& (HLT_isfired_Tau3Mu || HLT_isfired_DoubleMu)'
Ds_phi_selection    = f'(fabs(phi_fit_mass - {Phi_mass_}) < {Phi_window_/2.:.3f})'#f'(phi_fit_mass > {Ds_phi_mass_lo} & phi_fit_mass < {Ds_phi_mass_hi} )'
Ds_sv_selection     = f'(Ds_Lxy_sign_BS > 0.0 & Ds_fit_vprob > {Ds_minSVprob} )'
Tau_sv_selection    = f'(tau_Lxy_sign_BS > 0. & tau_fit_vprob > {Ds_minSVprob} )'

# peaking background
peakB_mass_lo = 1.70
peakB_mass_hi = 2.02
peakB_base_selection = f'(tau_MuMuPi_mass > {peakB_mass_lo} & tau_MuMuPi_mass < {peakB_mass_hi})'
peakB_phi_selection  = f'(tau_phiMuMu_mass > {Ds_phi_mass_lo} & tau_phiMuMu_mass < {Ds_phi_mass_hi} )'#f'fabs(tau_phiMuMu_mass - {Phi_mass_}) < {Phi_window_/2.0}'
peakB_phi_veto       = f'fabs(tau_phiMuMu_mass - {Phi_mass_}) > {Phi_window_/2.0}'
peakB_sv_selection   = f'(tau_Lxy_sign_BS > {5.0} & tau_fit_vprob > {0.10} )'

###              ###
#   DATASET INFO   #
###              ###

# filetr level number of events
Nmc_WTau3Mu = {
    '2022preEE'  :  197789,
    '2022EE'     :  792640,
    '2023preBPix':  662000,
    '2023BPix'   :  330000,
    '2024'       :  3894160,
}
Nmc_DsPhiPi = {
    '2022preEE' :  1000000,
    '2022EE'    :  1000000,
    '2023preBPix':  1000000,
    '2023BPix'  :  1000000,
}
Nmc_W3MuNu = {
    '2022preEE'  :  9963904,
    '2022EE'     :  9978946,
    '2023preBPix':  9924000,
    '2023BPix'   :  9864000,
    '2024'       :  1000000,
}
Nmc_ZTau3Mu = {
    '2022preEE' :  195001,
    '2022EE'    :  786411,
    '2023preBPix':  677882,
    '2023BPix'  :  317554,
    '2024'      :  4103413,
}
Nmc_TTbar_WTau3Mu = {
    '2022preEE'  :  47680,
    '2022EE'     :  -1,
    '2023preBPix':  -1,
    '2023BPix'   :  -1,
}
Nmc_process = {
    'WTau3Mu'   : Nmc_WTau3Mu,
    'DsPhiMuMuPi': Nmc_DsPhiPi,
    'W3MuNu'    : Nmc_W3MuNu,
    'ZTau3Mu'   : Nmc_ZTau3Mu,
    'TTbar_WTau3Mu': Nmc_TTbar_WTau3Mu,
}

# xsec W -> Tau Nu [fb]
eff_filterW = 1.0
xsec_ppWxMuNu_SMP_Run3 = 20928000  # Cross-section for W -> Mu Nu in fb
Br_WtoMuNu = 0.1063  # Branching ratio for W -> Mu Nu
Br_WtoTauNu = 0.1138  # Branching ratio for W -> Tau Nu

xsec_ppWxTauNu = xsec_ppWxMuNu_SMP_Run3 * Br_WtoTauNu / Br_WtoMuNu

# xsec Z -> Tau Tau [fb]
eff_filterZ = 0.2444  # Filter efficiency for 60 GeV < Mtautau < 120 GeV
xsec_ppZxMuMu_SMP_Run3 = 2026000  # Cross-section for Z -> Mu Mu in fb
Br_ZtoTauTau = 0.0337  # Branching ratio for Z -> Tau Tau
Br_ZtoMuMu = 0.0337  # Branching ratio for Z -> Mu Mu

xsec_ppZxTauTau = xsec_ppZxMuMu_SMP_Run3 * Br_ZtoTauTau / Br_ZtoMuMu



year_selection = {
    '2022preEE'     : '((year_id == 220) | ((year_id > 222) & (year_id < 225))) ', # era CD
    '2022EE'        : '((year_id == 221) | ((year_id > 224) & (year_id < 230))) ', # era EFG
    '2022'          : '((year_id >  219) & (year_id <  230))',
    '2023preBPix'   : '((year_id == 230) | ((year_id > 231) & (year_id < 234))) ', # era BC
    '2023BPix'      : '((year_id == 231) | ((year_id > 233) & (year_id < 240))) ', # era D
    '2023'          : '((year_id >  229) & (year_id < 240))',
    '2024'          : '((year_id >  239) & (year_id < 250))',
    '2024B'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 241) & (year_id <= 242)) ', # era B
    '2024C'         : '(((year_id > 239) & (year_id < 241)) | ((year_id > 242) & (year_id <= 243)))', # era C
    '2024D'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 243) & (year_id <= 244)) ', # era D
    '2024E'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 244) & (year_id <= 245)) ', # era E
    '2024F'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 245) & (year_id <= 246)) ', # era F
    '2024G'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 246) & (year_id <= 247)) ', # era G
    '2024H'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 247) & (year_id <= 248)) ', # era H
    '2024I'         : '((year_id > 239) & (year_id < 241)) | ((year_id > 248) & (year_id <= 249)) ', # era I
    'Run3'          : '((year_id >  219) & (year_id < 260))',
}
LumiVal_plots = {
    '2022preEE'     : "13.6",
    '2022EE'        : "20.8",
    '2022'          : "34.5", 
    '2023preBPix'   : "18.1",
    '2023BPix'      : "9.7",
    '2023'          : "27.7",
    'Run3'          : "62.2", # 2022 + 2023
    '2022+2023'     : "62.2", # 2022 + 2023
    '2024'          : "108.4",
    '2024B'         : "0.13",
    '2024C'         : "7.24",
    '2024D'         : "7.96",
    '2024E'         : "11.32",
    '2024F'         : "29.45",
    '2024G'         : "40.08",
    '2024H'         : "5.79",
    '2024I'         : "12.07",
}
###             ###
#   SYSTEMATICS   #
###             ###
Lumi_systematics = {
    '2022'          : 1.014,
    '2023'          : 1.013,
    '2024'          : 1.000, # fixme : put the correct value
}
# W channel normalization
xsec_ppW_sys  = 1.0166
Br_Wmunu_sys  = 1.0141
Br_Wtaunu_sys = 1.0185
Br_Wtaunu_munu_sys = 1.0200
# Z channel normalization
xsec_ppZ_sys  = 1.0157
Br_Zmumu_sys  = 1.0020
Br_Ztautau_sys= 1.0025
Br_Ztautau_mumu_sys = 1.0026
# signal shape systematics
shape_systematics = {
    '2022'         : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/signal_model/signal_shape_comparison_2022_ANv9.json'),
    '2023'         : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/signal_model/signal_shape_comparison_2023_ANv9.json'),
    '2024'         : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/signal_model/signal_shape_comparison_2024_ANv9.json'), # fixme : it is just a copy of 2023
}
# LxyS efficiency systematics
LxySign_cut_systematics ={
   '2022' : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/LxyS_efficiency/LxyS_efficiency_2022.json'),
   '2023' : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/LxyS_efficiency/LxyS_efficiency_2023.json'),
   '2024' : os.path.join(os.path.dirname(__file__), os.pardir + '/corrections/LxyS_efficiency/LxyS_efficiency_2023.json'), # fixme : use 2023 sys for the moment
}

###                     ###
#  CATEGORIES DEFINITION  #
###                     ###
# mass resolution
cat_selection_dict = {
    'A' : '(tau_fit_mass_err/tau_fit_mass < 0.007)',
    'B' : '(tau_fit_mass_err/tau_fit_mass >= 0.007 & tau_fit_mass_err/tau_fit_mass < 0.012)',
    'C' : '(tau_fit_mass_err/tau_fit_mass >= 0.012)'
}
cat_color_dict = {
    'A' : ROOT.kRed,
    'B' : ROOT.kBlue,
    'C' : ROOT.kGreen + 2
}
# pseudo-rapidity
eta_thAB = 0.9
eta_thBC = 1.8

cat_eta_selection_dict = {
    'ABC': f'(tau_fit_absEta > 0.)',
    'A' : f'(tau_fit_absEta < {eta_thAB})',
    'B' : f'(tau_fit_absEta > {eta_thAB} & tau_fit_absEta < {eta_thBC})', 
    'C' : f'(tau_fit_absEta > {eta_thBC})',
}
cat_eta_selection_dict_fit = {
    'ABC': f'(fabs(tau_fit_eta) > 0.)',
    'A'  : f'(fabs(tau_fit_eta) < {eta_thAB})',
    'B'  : f'(fabs(tau_fit_eta) > {eta_thAB} & fabs(tau_fit_eta) < {eta_thBC})', 
    'C'  : f'(fabs(tau_fit_eta) > {eta_thBC})',
}
Ds_category_selection = {
    'ABC': f'(fabs(Ds_fit_eta) > 0.)',
    'A'  : f'(fabs(Ds_fit_eta) < {eta_thAB})',
    'B'  : f'(fabs(Ds_fit_eta) > {eta_thAB} & fabs(Ds_fit_eta) < {eta_thBC})', 
    'C'  : f'(fabs(Ds_fit_eta) > {eta_thBC})',
}

#########################
#  BDT working points   #
#########################
year_list=['22', '23', '24']
cat_list=['A', 'B', 'C', 'comb']
bdt_cuts_22 = [0.991, 0.994, 0.995, -1]#[0.997, 0.996, 0.995, -1]
bdt_cuts_23 = [0.993, 0.993, 0.988, -1]#[0.987, 0.996, 0.992, -1]
bdt_cuts_23tight = [0.994, 0.996, 0.992, -1]
bdt_cuts_24 = [0.997, 0.996, 0.996, -1]
cat_sensitivity_22 = [-1., -1., -1., -1.]#[1.5, 1.7, 4.2, 1.0]
cat_sensitivity_23 = [-1., -1., -1., -1.]#[1.6, 2.1, 6.0, 1.2]
cat_sensitivity_24 = [-1., -1., -1., -1.]

wp_dict = dict(zip(year_list, [
   dict(zip(cat_list, bdt_cuts_22)), 
   dict(zip(cat_list, bdt_cuts_23)),
   dict(zip(cat_list, bdt_cuts_24))
   ]))
sensitivity_dict = dict(zip(year_list, [
   dict(zip(cat_list, cat_sensitivity_22)),
   dict(zip(cat_list, cat_sensitivity_23)),
   dict(zip(cat_list, cat_sensitivity_24))
   ]))

#########################
#   STYLE per PROCESS   #
#########################
process_name = ['WTau3Mu', 'W3MuNu', 'DsPhiPi', 'ZTau3Mu', 'invMedID', 'DataSB']
color_process = {
    'WTau3Mu' : ROOT.kRed - 7,
    'W3MuNu' : ROOT.kGreen+2,
    'DsPhiPi': ROOT.kViolet,
    'DataSB' : ROOT.kBlue,
    'ZTau3Mu': ROOT.kCyan+2,
    'invMedID': ROOT.kOrange+ 2,
}
legend_process = {
    'WTau3Mu' : 'W#rightarrow #tau (3#mu)#nu',
    'W3MuNu'  : 'W#rightarrow 3#mu#nu',
    'DsPhiPi' : 'D_{s}#rightarrow#phi#pi',
    'DataSB'  : 'data SB',
    'ZTau3Mu' : 'Z#rightarrow #tau (3#mu)#tau',
    'invMedID': 'inv-#mu ID',
    'MTauX'   : 'W#rightarrow #tau (3#mu) #nu',
}
bdt_label_process ={
   'WTau3Mu' : 0,
   'DataSB' : 1,
   'W3MuNu' : 2,
}

#########################
#        DATASETS       #
#########################

mc_path     = '/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/'
data_path   = '/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/'
invid_path  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/'

WTau3Mu_signals  = [
    # 2022
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onTau3Mu.root',
    # 2023
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onTau3Mu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onTau3Mu.root',
    # 2024
    #mc_path + 'outRoot/WTau3Mu_MCanalyzer_2024_HLT_overlap_onTau3Mu.root',
]

DsPhiPi_signals = [
    # 2022
    mc_path + 'outRoot/DsPhiMuMuPi_MCanalyzer_2022preEE_HLT_overlap_onDsPhiPi.root',
    mc_path + 'outRoot/DsPhiMuMuPi_MCanalyzer_2022EE_HLT_overlap_onDsPhiPi.root',
    # 2023
    mc_path + 'outRoot/DsPhiMuMuPi_MCanalyzer_2023preBPix_HLT_overlap_onDsPhiPi.root',
    mc_path + 'outRoot/DsPhiMuMuPi_MCanalyzer_2023BPix_HLT_overlap_onDsPhiPi.root',
    # 2024
    #mc_path + 'outRoot/DsPhiMuMuPi_MCanalyzer_2024_HLT_overlap_onDsPhiPi.root',
]

ZTau3Mu_signals = [
    # 2022
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onZTau3Mu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onZTau3Mu.root',
    # 2023
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onZTau3Mu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onZTau3Mu.root',
]

DsPhiPi_data = [
    #2022
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_overlap.root',
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_overlap.root',
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_overlap.root',
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_overlap.root',
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_overlap.root',
    data_path + 'reMini2022/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root',
    #2023
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Bv1_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv4_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root',
    data_path + 'reMini2023/DsPhiMuMuPi_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv2_HLT_overlap.root',
]

data_background  = [
    #2022
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_overlap.root',
    data_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root',
    #2023
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Bv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv4_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root',
    data_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv2_HLT_overlap.root',
]
W3MuNu_background = [
    #2022
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onW3MuNu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onW3MuNu.root',
    #2023
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onW3MuNu.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onW3MuNu.root', 
]

Peaking_background = [
    #2022
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onDsPhiPi.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onDsPhiPi.root',
    #2023
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onDsPhiPi.root',
    mc_path + 'outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onDsPhiPi.root',
]

invID_background = [
    #2022
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Cv1_HLT_overlap.root',
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv1_HLT_overlap.root',
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Dv2_HLT_overlap.root',
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Ev1_HLT_overlap.root',
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_overlap.root',
    #invid_path + 'reMini2022/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root',
    #2023
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Bv1_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv1_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv2_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv3_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv4_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root',
    invid_path + 'reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv2_HLT_overlap.root',
]


mc_samples = {
    'WTau3Mu'       : WTau3Mu_signals,
    'DsPhiMuMuPi'   : DsPhiPi_signals,
    'W3MuNu'        : W3MuNu_background,
    'peakingBkg'    : Peaking_background,
    'ZTau3Mu'       : ZTau3Mu_signals,
    'TTbar_WTau3Mu' : [mc_path+'outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu_TTbar.root']
}
data_samples = {
    'WTau3Mu'       : data_background,
    'DsPhiMuMuPi'   : DsPhiPi_data,
    'W3MuNu'        : data_background,
    'ZTau3Mu'       : data_background,
    'invMedID'      : invID_background,
}

##############
#    BDT     #
##############

# samples processed with BDT
bdt_output_path = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/'
mc_bdt_samples = {
    'WTau3Mu'       : bdt_output_path+'XGBout_signal_kFold_ANv8_2025Jul28.root', 
    'DsPhiMuMuPi'   : bdt_output_path+'XGBout_DsPhiMuMuPi_MC_noSVp-ANv9.root',#'XGBout_DsPhiMuMuPi_MC_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root', 
    'W3MuNu'        : bdt_output_path+'XGBout_W3MuNu_MC_noLxyScut.root',#'XGBout_W3MuNu_MC_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root', 
    'peakingBkg'    : bdt_output_path+'XGBout_peakingBkg_MC_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root', 
    'ZTau3Mu'       : bdt_output_path+'XGBout_ZTau3Mu_MC_ANv8_2025Jul28.root', 
    'TTbar_WTau3Mu' : bdt_output_path+'XGBout_WTau3Mu_MC_TTbar-2022preEE.root',
}
data_bdt_samples = {
    'WTau3Mu'       : bdt_output_path+'XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root',
    'DsPhiMuMuPi'   : bdt_output_path+'XGBout_DsPhiMuMuPi_DATA_noSVp-ANv9.root',#'XGBout_DsPhiMuMuPi_DATA_Optuna_HLT_overlap_LxyS2.0_2024Jul16.root',
    'W3MuNu'        : bdt_output_path+'XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root',
    'ZTau3Mu'       : bdt_output_path+'XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root',
    'peakingBkg'    : bdt_output_path+'XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root',
}


# give labels human readable names
# IMPORTANT : same order as features!!!
#labels = OrderedDict()
labels = {}
labels['tau_fit_pt'         ] = '$p_{T} (3\mu)$'
labels['tau_fit_mt'         ] = '$m_{T}(\\tau, MET)$'
labels['tau_relIso'         ] = '$I_{rel}(3\mu)$'
labels['tau_met_Dphi'       ] = '$\Delta\phi(\\tau, MET)$'
labels['tau_met_pt'         ] = 'MET'
labels['tau_met_ratio_pt'   ] = '$p_{T}(\\tau)$/MET' # only for >= v2
labels['W_pt'               ] = '$p_{T}$(W)'
labels['miss_pz_min'        ] = 'min $p_{z}^{\\nu}$'
labels['miss_pz_max'        ] = 'max $p_{z}^{\\nu}$'
labels['tau_mu12_dZ'        ] = '$\Delta z (\mu_{1}, \mu_{2})$'
labels['tau_mu13_dZ'        ] = '$\Delta z (\mu_{1}, \mu_{3})$'
labels['tau_mu23_dZ'        ] = '$\Delta z (\mu_{2}, \mu_{3})$'
labels['tau_Lxy_sign_BS'    ] = 'SV L/$\sigma$'
labels['tau_fit_vprob'      ] = 'SV prob.'
labels['tau_cosAlpha_BS'    ] = 'SV cos($\\alpha$)'
labels['tau_mu1_TightID_PV' ] = 'Tight-ID $\mu_1$'
labels['tau_mu2_TightID_PV' ] = 'Tight-ID $\mu_2$'
labels['tau_mu3_TightID_PV' ] = 'Tight-ID $\mu_3$'
labels['tau_fit_eta'        ] = '$\eta_{\\tau}$'
labels['tauEta'             ] = '$|\eta_{\\tau}|$'
##labels['bdt'                ] = 'BDT score'
labels['bdt_score'          ] = 'BDT score'
#labels['bdt_score_t3m'      ] = 'BDT $\\tau 3\\mu$ '
#labels['bdt_score_b'        ] = 'BDT bkg'
#labels['bdt_score_w3m'      ] = 'BDT W3$\\mu$'
labels['tau_fit_mass'       ] = 'm_{3\mu}'
labels['tau_fit_charge'     ] = 'q$_{3\mu}$'

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

features_NbinsXloXhiLabelLog = {
    'tau_fit_pt'        : [ 20, 10, 50,     'p_{T}(3 #mu) (GeV)',      0],
    'tau_fit_mt'        : [ 30, 0, 120,     'M_{T}(3 #mu) (GeV)',           0],
    'tau_relIso'        : [ 50, 0, 3.0,     'rel. Isolation (3 #mu)',  1],
    'tau_met_Dphi'      : [ 32, 0, 6.4,     '#Delta #phi (3 #mu, MET)',0],
    'tau_met_pt'        : [ 20, 0, 100.,    'MET (GeV)',               0],
    'tau_met_ratio_pt'  : [ 30, 0., 3.,     'MET/p_{T}(3 #mu)',        0],
    'W_pt'              : [ 20, 0, 100,     'p_{T}(W) (GeV)',          0],
    'miss_pz_min'       : [40, -200, 200,   'min p_{z}^{#nu} (GeV)',  0],
    'miss_pz_max'       : [40,-1500, 1500,  'max p_{z}^{#nu} (GeV)',  0],
    'tau_mu12_dZ'       : [ 20, 0, 0.2,     '#Delta z (#mu_{1}, #mu_{2})',  0],
    'tau_mu13_dZ'       : [ 20, 0, 0.2,     '#Delta z (#mu_{1}, #mu_{3})',  0],
    'tau_mu23_dZ'       : [ 20, 0, 0.2,     '#Delta z (#mu_{2}, #mu_{3})',  0],
    'tau_Lxy_sign_BS'   : [50, 0, 50,      'SV L_{xy}/#sigma',         0],
    #'tau_Lxy_sign_BS'   : [ 40, 0, 10,      'SV L_{xy}/#sigma',         0],
    'tau_Lxy_val_BS'    : [ 40, 0,1.0,      'SV L_{xy} (cm)',           0],
    'tau_Lxy_err_BS'    : [ 20, 0.01,0.03,  'SV #sigma_{L_{xy}} (cm)',  0],
    'Ds_Lxy_val_BS'     : [ 40, 0,1.0,      'SV L_{xy} (cm)',           0],
    'Ds_Lxy_err_BS'     : [ 30, 0,0.03,     'SV #sigma_{L_{xy}} (cm)',  0],
    'tau_fit_vprob'     : [ 50, 0,  1,      'SV probability',           1],
    'tau_cosAlpha_BS'   : [ 50, 0.995, 1, 'cos_{#alpha}(SV, BS)',     1],
    'tau_mu1_TightID_PV': [  2,-0.5,1.5,    'Tight-ID #mu_{1}',        0],
    'tau_mu2_TightID_PV': [  2,-0.5,1.5,    'Tight-ID #mu_{2}',        0],
    'tau_mu3_TightID_PV': [  2,-0.5,1.5,    'Tight-ID #mu_{3}',        0],
    'tri_muonID'        : [  4,-0.5,3.5,    'Medium ID_{#mu_1}+ID_{#mu_2}+ID_{#mu_3}',                0],
    'tauEta'            : [  8,-0.5,7.5,    '3#mu #eta bins',          0],
    'tau_fit_eta'       : [ 25, -2.5, 2.5,  '#eta (3 #mu)',           0],
    'Ds_fit_eta'        : [ 25, -2.5, 2.5,  '#eta (3 #mu)',           0],
    'tau_fit_mass'      : [ 65, 1.40, 2.05, 'm_{3#mu}',                0],
    'bdt_score'         : [ 50, 0, 1,       'BDT score',               1],
    'bdt_score_t3m'     : [ 50, 0, 1,       'BDT_{#tau 3 #mu} score',  1],
    'tau_mu12_fitM'     : [ 100, 0.30, 1.60,  'M(#mu_{1}#mu_{2})',       0],
    'tau_mu13_fitM'     : [ 100, 0.30, 1.6,  'M(#mu_{1}#mu_{3})',       0],
    'tau_mu23_fitM'     : [ 100, 0.30, 1.6,  'M(#mu_{2}#mu_{3})',       0],
    'tau_mu12_M'        : [ 100, 0.30, 1.60,  'M(#mu_{1}#mu_{2})',       0],
    'tau_mu13_M'        : [ 100, 0.30, 1.6,  'M(#mu_{1}#mu_{3})',       0],
    'tau_mu23_M'        : [ 100, 0.30, 1.6,  'M(#mu_{2}#mu_{3})',       0],
    'tau_mu1_pt'        : [ 45, 5, 50,      'p_{T}(#mu_{1}) (GeV)',    0],
    'tau_mu2_pt'        : [ 30, 0, 30,      'p_{T}(#mu_{2}) (GeV)',    0],
    'tau_mu3_pt'        : [ 30, 0, 30,      'p_{T}(#mu_{3}) (GeV)',    0],
    'tau_mu1_eta'       : [ 50, -2.5, 2.5,  '#eta(#mu_{1})',           0],
    'tau_mu2_eta'       : [ 50, -2.5, 2.5,  '#eta(#mu_{2})',           0],
    'tau_mu3_eta'       : [ 50, -2.5, 2.5,  '#eta(#mu_{3})',           0],
    'tau_fit_charge'    : [  2, -2.0, 2.0,    'q(3#mu)',        0],
}



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
