import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

MET_variables =[
    'PuppiMET_pt',
    'PuppiMET_phi',
    'TauPlusMET_Tau_Puppi_mT',
    'TauPlusMET_pt',
    'TauPlusMET_PuppiMETminPz',
    'TauPlusMET_PuppiMETmaxPz',
    'TauTo3Mu_fitted_pt',
    'TauTo3Mu_fitted_eta',
    'TauTo3Mu_fitted_phi',
    'TauTo3Mu_fitted_mass',
]
MET_variables_reco =[
    'tau_met_pt',
    'tau_fit_mt',
    'W_pt',
    'miss_pz_min',
    'miss_pz_max'
]
MET_variables_Run2map = {
    'PuppiMET_pt'   : 'cand_refit_met_pt',
    'tau_met_pt'   : 'cand_refit_met_pt',
    'PuppiMET_phi'   : 'cand_refit_met_phi',
    'TauPlusMET_Tau_Puppi_mT'   : 'cand_refit_mttau',
    'tau_fit_mt'   : 'cand_refit_mttau',
    'TauPlusMET_pt'         : 'cand_refit_w_pt',
    'W_pt'         : 'cand_refit_w_pt',
    'TauPlusMET_PuppiMETminPz'  : 'cand_refit_mez_1',
    'miss_pz_min'  : 'cand_refit_mez_1',
    'TauPlusMET_PuppiMETmaxPz'  : ' cand_refit_mez_2',
    'miss_pz_max'  : ' cand_refit_mez_2',
    'TauTo3Mu_fitted_pt' : 'cand_refit_tau_pt',
    'TauTo3Mu_fitted_eta' : 'cand_refit_tau_eta',
    'TauTo3Mu_fitted_phi' : 'cand_refit_tau_phi',
    'TauTo3Mu_fitted_mass': 'cand_refit_tau_mass',
}

MET_vars_settings = {# Nbins, xlow, xhigh
   'PuppiMET_pt'   : [80, 0, 100],
   'tau_met_pt'   : [80, 0, 100],
   'PuppiMET_phi'  : [30, -4, 4],
   'TauPlusMET_Tau_Puppi_mT' : [50, 0, 200],
   'tau_fit_mt' : [50, 0, 200],
   'TauPlusMET_pt' : [50, 0, 150],
   'W_pt' : [50, 0, 150],
   'TauPlusMET_PuppiMETminPz': [100, -300, 300],
   'miss_pz_min': [100, -300, 300],
   'TauPlusMET_PuppiMETmaxPz': [100, -1000, 1000], 
   'miss_pz_max': [100, -1000, 1000], 
   'TauTo3Mu_fitted_pt' : [25, 0, 50],
   'TauTo3Mu_fitted_eta': [60, -3.5,3.5],
   'TauTo3Mu_fitted_phi': [60, -3.5,3.5],
   'TauTo3Mu_fitted_mass': [80, 1.6, 2.0],
}

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_R2', default='/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/WTau3Mu_MC2017.root')
parser.add_argument('--input_R3', default='/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano2017_retry_2023Nov19/W_ToTau_ToMuMuMu_TuneCP5_13TeV-pythia8/crab_WnuTau3Mu_2017/231119_174852/0000/tau3muNANO_mc_2023Nov19_*.root')
parser.add_argument('--tree_R3', default='Events')
parser.add_argument('--outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')

args = parser.parse_args()
tag = args.tag

# -- read inputs
try:
    file_R2 = ROOT.TFile.Open(args.input_R2)
except:
    print(f' [+] error cannot open {args.input_R2}')
else:
    tree_R2 = file_R2.Get('tree')
    print(f' [+] get tree from {args.input_R2} with {tree_R2.GetEntries()} events')

selection_Run2 = ' && '.join([
  'abs(cand_refit_charge) == 1',
  'abs(cand_refit_tau_mass - 1.8) < 0.2',
  '(HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Charge1_matched || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_matched)',
  '(mu1_muonid_medium==1)',
  '(mu2_muonid_medium==1)',
  '(mu3_muonid_medium==1)',
  '((mu1_refit_pt>3.5 && abs(mu1_refit_eta)<1.2) || (mu1_refit_pt>2.0 && abs(mu1_refit_eta)<2.5 && abs(mu1_refit_eta)>1.2))',
  '((mu2_refit_pt>3.5 && abs(mu2_refit_eta)<1.2) || (mu2_refit_pt>2.0 && abs(mu2_refit_eta)<2.5 && abs(mu2_refit_eta)>1.2))',
  '((mu3_refit_pt>3.5 && abs(mu3_refit_eta)<1.2) || (mu3_refit_pt>2.0 && abs(mu3_refit_eta)<2.5 && abs(mu3_refit_eta)>1.2))',
  '(mu1_refit_pt > 7 & mu2_refit_pt > 1 & mu3_refit_pt > 1)',
  '(cand_refit_dR12 < 0.5 || cand_refit_dR13 < 0.5 || cand_refit_dR23 < 0.5)',
  '(cand_refit_mass12 < 1.9 || cand_refit_mass13 < 1.9 || cand_refit_mass23 < 1.9)',
  '(cand_refit_tau_pt > 15)',
  '(abs(cand_refit_tau_eta) < 2.5)',
  '(mu1_refit_muonid_medium==1 && mu2_refit_muonid_medium==1 && mu3_refit_muonid_medium==1)',])

print(f'  Run2 selection : {selection_Run2}')

chain_R3= ROOT.TChain(args.tree_R3)
chain_R3.Add(args.input_R3)
print(f' [+] get tree from {args.input_R3} with {chain_R3.GetEntries()} events')

# -- loop on variables
c = ROOT.TCanvas("c", "", 800, 800)
legend = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
legend.SetBorderSize(0)
legend.SetTextSize(0.035)
for var in MET_variables:
#var = MET_variables[0]
    print(f' [...] plotting {var} from R3 and {MET_variables_Run2map[var]} from R2 ')

    h_R2 = ROOT.TH1F("h_%s_R2"%var, "", MET_vars_settings[var][0], MET_vars_settings[var][1], MET_vars_settings[var][2])
    h_R2.SetLineWidth(2); h_R2.SetLineColor(ROOT.kOrange+7)
    h_R3 = ROOT.TH1F("h_%s_R3"%var, "", MET_vars_settings[var][0], MET_vars_settings[var][1], MET_vars_settings[var][2])
    h_R3.SetLineWidth(2); h_R3.SetLineColor(ROOT.kCyan+2)


    chain_R3.Draw("%s>>h_%s_R3"%(var,var))
    h_R3.Scale(1./h_R3.Integral())
    tree_R2.Draw("%s>>h_%s_R2"%(MET_variables_Run2map[var],var))
    h_R2.Scale(1./h_R2.Integral())
    h_R3.SetMaximum(1.3*np.max([h_R2.GetMaximum(), h_R3.GetMaximum()]))
    if(var == MET_variables[0]):
        legend.AddEntry(h_R2, "Run2 ntuplizer", 'f')
        legend.AddEntry(h_R3, "Run3 ntuplizer", 'f')

    h_R3.Draw('hist')
    h_R2.Draw('hist same')
    legend.Draw()


    c.SaveAs('%s/%s_2017.png'%(args.outdir, var))
