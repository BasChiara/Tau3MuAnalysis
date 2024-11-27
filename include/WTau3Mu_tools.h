#ifndef WTau3Mu_tools_h
#define WTau3Mu_tools_h

#include "../include/WTau3Mu_base.h"
#include "include/constants.h"
#include "corrections/HLT_DoubleMu4_3_LowMass/trigger_SFs_2022.h"

#include <vector>
#include <numeric>
#include <algorithm>
#define _USE_MATH_DEFINES
#include <cmath>

#include "Math/Vector4D.h"
#include "Math/GenVector/VectorUtil.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TH2Poly.h"
#include "TH1D.h"


class WTau3Mu_tools : public WTau3Mu_base{

   public:
   WTau3Mu_tools(TTree *tree=0, const bool& isMC = true) : WTau3Mu_base(tree, isMC){}
   virtual ~WTau3Mu_tools(){

      delete h_muonSF_lowpT;
      delete h_muonSF_lowpT_sysUP;
      delete h_muonSF_lowpT_sysDOWN;
      delete h_muonSF_medpT;
      delete h_muonSF_medpT_sysUP;
      delete h_muonSF_medpT_sysDOWN;
      delete h_PUweights;
      delete h_PUweights_sysUP;
      delete h_PUweights_sysDOWN;

   }

   virtual void     Loop(){}
   // gen/reco tools
   int     MCtruthMatching(const bool verbose = false);
   void    GenPartFillP4();
   int     GenPartFillP4_Z();
   int     TauIdx_radiative(const int prod_idx, const int VpdgId=24);
   int     GenTauDecayMode(const int tau_idx);
   std::vector<int> Gen3Mu_FindSort();
   std::vector<int> sortMu_pT(const std::vector<int>& muons);
   
   bool    RecoPartFillP4(const int idx);
   // trigger tools
   bool    TriggerMatching(const int TauIdx, const int config = -1);
   bool    HLT_Tau3Mu_emulator(const int TauIdx);
   bool    HLT_DoubleMu_emulator(const int TauIdx);
   bool    HLT_DoubleMu_reinforcement(const int TauIdx);
   // MET filters
   bool    applyMETfilters(const int& TauIdx);
   // sort candidates by transverse mass
   std::vector<unsigned int> sorted_cand_mT();
   // scale factors
   // muon ID
   int    parseMuonSF(const TString & era = "2022preEE", const TString & pTrange = "low");
   int    applyMuonSF(const int& TauIdx);
   // HLT DoubleMu4_3_LowMass
   int    parseHLT_SF(const TString & era = "2022preEE");
   float  get_dimuon_efficiency(const float& pt, const float& eta, const float& DR, const TString& trigger = "L1", const TString& dataset = "mc");
   float  get_trimuon_efficiency(const TString& dataset = "mc");
   int    applyHLT_SF();
   // PU re-weight
   int    parsePUweights(const TString & era = "2022preEE");
   int    applyPUreweight();
   // NLO re-weight
   int    parseNLOweights(const TString & era = "2022preEE");
   int    applyNLOreweight(const float& W_pt, const float& W_eta);

   const std::string muons_IDsf_set_ = "NUM_MediumID_DEN_TrackerMuons";


   // gen particle P4 
   ROOT::Math::PtEtaPhiMVector GenW_P4, GenZ_P4;
   ROOT::Math::PtEtaPhiMVector GenTau_P4, GenNu_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4, GenMu3_P4;
   // opposite side (for Ztautau)
   ROOT::Math::PtEtaPhiMVector GenTauOp_P4;
   TauDecayMode opposite_side_ = TauDecayMode::UNDEFINED;
   int opposite_side_tag_;
   // reco  particle P4 
   ROOT::Math::PtEtaPhiMVector RecoW_P4;
   ROOT::Math::PtEtaPhiMVector RecoTau_P4, RecoMET_P4;
   ROOT::Math::PtEtaPhiMVector RecoMu1_P4, RecoMu2_P4, RecoMu3_P4;

   // offline muon sf MUON-POG
   TH2Poly* h_muonSF_lowpT          = 0;
   TH2Poly* h_muonSF_lowpT_sysUP    = 0;
   TH2Poly* h_muonSF_lowpT_sysDOWN  = 0;
   TH2Poly* h_muonSF_medpT          = 0; // NOT used 
   TH2Poly* h_muonSF_medpT_sysUP    = 0; //  " 
   TH2Poly* h_muonSF_medpT_sysDOWN  = 0; //  "

   float tau_mu1_IDrecoSF, tau_mu2_IDrecoSF, tau_mu3_IDrecoSF;
   float tau_mu1_IDrecoSF_sysUP, tau_mu2_IDrecoSF_sysUP, tau_mu3_IDrecoSF_sysUP;
   float tau_mu1_IDrecoSF_sysDOWN, tau_mu2_IDrecoSF_sysDOWN, tau_mu3_IDrecoSF_sysDOWN;

   // HLT_DoubleMu4_3_LowMass SF
   // L1
   TH2Poly* h_mc_L1_efficiency_barrel = 0;
   TH2Poly* h_mc_L1_efficiency_overlap = 0;
   TH2Poly* h_mc_L1_efficiency_endcap = 0;
   TH2Poly* h_data_L1_efficiency_barrel = 0;
   TH2Poly* h_data_L1_efficiency_overlap = 0;
   TH2Poly* h_data_L1_efficiency_endcap = 0;

   // HLT
   TH2Poly* h_mc_HLT_efficiency_barrel = 0;
   TH2Poly* h_mc_HLT_efficiency_overlap = 0;
   TH2Poly* h_mc_HLT_efficiency_endcap = 0;
   TH2Poly* h_data_HLT_efficiency_barrel = 0;
   TH2Poly* h_data_HLT_efficiency_overlap = 0;
   TH2Poly* h_data_HLT_efficiency_endcap = 0;

   float tau_DoubleMu4_3_LowMass_SF, tau_DoubleMu4_3_LowMass_SF_sysUP, tau_DoubleMu4_3_LowMass_SF_sysDOWN;
   TH1F* h_DiMuon_HLTcand = new TH1F("h_DiMuon_HLTcand", "DiMuon HLT cand", 4, -0.5, 3.5);

   // PU weights
   TH1D* h_PUweights             =0;
   TH1D* h_PUweights_sysUP       =0;
   TH1D* h_PUweights_sysDOWN     =0;

   float PU_weight, PU_weight_up, PU_weight_down;

   // NLO weights
   TH2F* h_NLOweights            =0;
   TH2F* h_NLOweights_sysUP      =0;
   TH2F* h_NLOweights_sysDOWN    =0;

   float NLO_weight, NLO_weight_up, NLO_weight_down;

   private:
   bool debug = false;
   


};//WTau3Mu_tools

#endif
