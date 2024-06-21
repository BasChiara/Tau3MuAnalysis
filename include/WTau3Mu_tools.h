#ifndef WTau3Mu_tools_h
#define WTau3Mu_tools_h

#include "../include/WTau3Mu_base.h"
#include "include/constants.h"

#include <vector>
#include <numeric>
#include <algorithm>
#define _USE_MATH_DEFINES
#include <cmath>

#include "Math/Vector4D.h"
#include "Math/GenVector/VectorUtil.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TH2Poly.h"

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
   }

   virtual void     Loop(){}
   // gen/reco tools
   int     MCtruthMatching(const bool verbose = false);
   void    GenPartFillP4();
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
   int    parseMuonSF(const TString & era = "2022preEE", const TString & pTrange = "low" );
   int    applyMuonSF(const int& TauIdx);

   const std::string muons_IDsf_set_ = "NUM_MediumID_DEN_TrackerMuons";


   // gen particle P4 
   ROOT::Math::PtEtaPhiMVector GenW_P4;
   ROOT::Math::PtEtaPhiMVector GenTau_P4, GenNu_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4, GenMu3_P4;
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

   private:
   bool debug = false; 
   


};//WTau3Mu_tools

#endif
