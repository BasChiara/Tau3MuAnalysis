#ifndef prepStudiesT3m_h
#define prepStudiesT3m_h

#include "Tau3Mu_base.h"
#include <cmath>
#include "constants.h"
class prepStudiesT3m : public Tau3Mu_base{

public:
 prepStudiesT3m(TTree *tree=0, const TString & outdir = "./outRoot", const TString & tags = "2022_preEE");
 virtual ~prepStudiesT3m(){}

 void    Loop();
 void    outTreeSetUp();
 void    saveOutput();

 // HLT trigger methods
 bool    TriggerMatching(const int TauIdx, const int config = -1);
 bool    HLT_Tau3Mu_emulator(const int TauIdx);
 bool    HLT_DoubleMu_emulator(const int TauIdx);

private:
  // HLT paths
  HLT_paths HLTconf_ = HLT_Tau3Mu;  // HLT_DoubleMu, HLT_Tau3Mu, HLT_overlap

  // blinding parameters
  bool isBlind_;
  const float blindTauMass_low = 1.74;
  const float blindTauMass_high = 1.82;

 TString tags_;

 TString outFilePath_;
 TFile*  outFile_;
 TTree*  outTree_;
 const TString outTree_name_ = "Tau3Mu_HLTemul_tree";

 // TTree branches
  UInt_t LumiBlock, Run;
  ULong64_t Event;
  // HLT_bit
  int HLT_isfired_Tau3Mu, HLT_isfired_DoubleMu;
 // * muons
  int   tau_mu1_MediumID,  tau_mu2_MediumID,  tau_mu3_MediumID;
  int   tau_mu1_LooseID,  tau_mu2_LooseID,  tau_mu3_LooseID;
  int   tau_mu1_SoftID_PV, tau_mu2_SoftID_PV, tau_mu3_SoftID_PV;
  int   tau_mu1_SoftID_BS, tau_mu2_SoftID_BS, tau_mu3_SoftID_BS;
  int   tau_mu1_TightID_PV,tau_mu2_TightID_PV,tau_mu3_TightID_PV;
  int   tau_mu1_TightID_BS,tau_mu2_TightID_BS,tau_mu3_TightID_BS;
  float tau_mu1_pt, tau_mu2_pt, tau_mu3_pt;
  float tau_mu1_eta, tau_mu2_eta, tau_mu3_eta;
  float tau_mu1_z, tau_mu2_z, tau_mu3_z;
  float tau_mu12_dZ, tau_mu23_dZ, tau_mu13_dZ;
 // * tau candidates
  int n_tau;
  float tau_raw_mass;
  float tau_fit_mass, tau_fit_mass_err;
  float tau_fit_pt, tau_fit_eta, tau_fit_phi;
  float tau_relIso, tau_dimuon_mass;
  float tau_Lxy_val_BS, tau_Lxy_err_BS, tau_Lxy_sign_BS;
  float tau_fit_mt, tau_fit_vprob, tau_cosAlpha_BS;
// * tau + MET
  float tau_met_pt, tau_met_phi;
  float tau_met_Dphi, tau_met_ratio_pt;
  float miss_pz_min, miss_pz_max;
  float W_pt;
  


  // TH1
  // muond ID
   TH1F* h_Mu_MediumID = new TH1F("Mu_MediumID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_SoftID   = new TH1F("Mu_SoftID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_SoftID_BS= new TH1F("Mu_SoftID_BS", "", 2, -0.5, 1.5);
   TH1F* h_Mu_TightID  = new TH1F("Mu_TightID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_TightID_BS= new TH1F("Mu_TightID_BS", "", 2, -0.5, 1.5);

   // muons kinematics
   TH1F* h_MuLeading_pT = new TH1F("MuLeading_pT", "", 50, 0, 50);
   TH1F* h_MuSubLeading_pT = new TH1F("MuSubLeading_pT", "", 50, 0, 50);
   TH1F* h_MuTrailing_pT = new TH1F("MuTrailing_pT", "", 50, 0, 50);

   TH1F* h_MuLeading_eta = new TH1F("MuLeading_eta", "", 35, -3.5, 3.5);
   TH1F* h_MuSubLeading_eta = new TH1F("MuSubLeading_eta", "", 35, -3.5, 3.5);
   TH1F* h_MuTrailing_eta = new TH1F("MuTrailing_eta", "", 35, -3.5, 3.5);

   TH1F* h_Mu_Dz12 = new TH1F("Mu_Dz12", "", 40, 0, 0.4);
   TH1F* h_Mu_Dz23 = new TH1F("Mu_Dz23", "", 40, 0, 0.4);
   TH1F* h_Mu_Dz13 = new TH1F("Mu_Dz13", "", 40, 0, 0.4);

  // Tau
   TH1F* h_nTau = new TH1F("nTau", "", 10, -0.5, 9.5);
   TH1F* h_Tau_fit_M = new TH1F("Tau_fit_M", "", 50, 1.6, 2.0);
   TH1F* h_Tau_fit_pT = new TH1F("Tau_fit_pT", "", 40, 10, 100);
   TH1F* h_Tau_fit_eta = new TH1F("Tau_fit_eta", "", 70, -3.5, 3.5);
   TH1F* h_Tau_relIso = new TH1F("Tau_relIso", "", 60, 0, 3);
   TH1F* h_Tau_fitNoVtx_M = new TH1F("Tau_fitNoVtx_M", "", 50, 1.6, 2.0);
   TH1F* h_diMuon_Mass = new TH1F("diMuon_Mass", "", 200, 0., 95);

   TH1F* h_LxySign_BSvtx = new TH1F("LxySign_BSvtx", "", 40, 0, 30);
   TH1F* h_Tau_Mt = new TH1F("Tau_Mt", "", 50, 0, 200);
   TH1F* h_Tau_Pvtx = new TH1F("Tau_Pvtx", "", 40, 0., 1.);
   TH1F* h_Tau_cosAlpha_BS = new TH1F("Tau_cosAlpha_BS", "", 100, -1, 1);

  // Tau + MET
  TH1F* h_DPhi_TauDeepMET = new TH1F("DPhi_TauDeepMET", "", 50, 0, 3.14);
  TH1F* h_TauPt_DeepMET = new TH1F("TauPt_DeepMET", "", 60, 0, 6.);
  TH1F* h_DPhi_TauPuppiMET = new TH1F("DPhi_TauPuppiMET", "", 50, 0, 3.14);
  TH1F* h_TauPt_PuppiMET = new TH1F("TauPt_PuppiMET", "", 60, 0, 6.);

  TH1F* h_missPz_min = new TH1F("missPz_min", "", 100, -300, 300);
  TH1F* h_missPz_max = new TH1F("missPz_max", "", 100, 0, 4000);  

  // W cand
  TH1F* h_W_pT = new TH1F("W_pT", "", 40, 0, 150);

};


#endif
