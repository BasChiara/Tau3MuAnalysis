#ifndef DsPhiMuMuPi_tools_h
#define DsPhiMuMuPi_tools_h

#include "DsPhiMuMuPi_base.h"
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

#include "../corrections/HLT_DoubleMu4_3_LowMass/trigger_SFs_2022.h"

class DsPhiMuMuPi_tools : public DsPhiMuMuPi_base{

   public:
   DsPhiMuMuPi_tools(TTree *tree=0, const bool& isMC = true) : DsPhiMuMuPi_base(tree, isMC){}
   virtual ~DsPhiMuMuPi_tools(){
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
   bool    GenPartFillP4();
   bool    RecoPartFillP4(const int idx);
   // trigger tools
   bool    TriggerMatching(const int idx, const int config = -1);
   bool    HLT_Tau3Mu_emulator(const int idx);
   bool    HLT_DoubleMu_emulator(const int idx);
   bool    HLT_DoubleMu_reinforcement(const int idx);
   // MET filters
   bool    applyMETfilters(const int& TauIdx);
   // sort candidates by transverse mass
   std::vector<unsigned int> sorted_cand_mT();
   // scale factors
   // muon ID
   int    parseMuonSF(const TString & era = "2022preEE", const TString & pTrange = "low" );
   int    applyMuonSF(const int& TauIdx);
   // HLT DoubleMu4_3_LowMass
   int    parseHLT_SF();
   int    applyHLT_SF(const TString & era = "2022preEE");
   // PU re-weight
   int    parsePUweights(const TString & era = "2022preEE");
   int    applyPUreweight();


   const std::string muons_IDsf_set_ = "NUM_MediumID_DEN_TrackerMuons";



   // gen particle P4 
   ROOT::Math::PtEtaPhiMVector GenDs_P4;
   ROOT::Math::PtEtaPhiMVector GenPhi_P4, GenPi_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4;
   // reco particle P4 
   ROOT::Math::PtEtaPhiMVector RecoDs_P4;
   ROOT::Math::PtEtaPhiMVector RecoPhi_P4, RecoPi_P4;
   ROOT::Math::PtEtaPhiMVector RecoMu1_P4, RecoMu2_P4;

   // offline muon sf MUON-POG
   TH2Poly* h_muonSF_lowpT          = 0;
   TH2Poly* h_muonSF_lowpT_sysUP    = 0;
   TH2Poly* h_muonSF_lowpT_sysDOWN  = 0;
   TH2Poly* h_muonSF_medpT          = 0; // NOT used 
   TH2Poly* h_muonSF_medpT_sysUP    = 0; //  " 
   TH2Poly* h_muonSF_medpT_sysDOWN  = 0; //  "
   float Ds_mu1_IDrecoSF, Ds_mu2_IDrecoSF;
   float Ds_mu1_IDrecoSF_sysUP, Ds_mu2_IDrecoSF_sysUP;
   float Ds_mu1_IDrecoSF_sysDOWN, Ds_mu2_IDrecoSF_sysDOWN;

   // HLT
   float Ds_DoubleMu4_3_LowMass_SF, Ds_DoubleMu4_3_LowMass_SF_sysUP, Ds_DoubleMu4_3_LowMass_SF_sysDOWN;

   // PU weights
   TH1D* h_PUweights             =0;
   TH1D* h_PUweights_sysUP       =0;
   TH1D* h_PUweights_sysDOWN     =0;

   float PU_weight, PU_weight_up, PU_weight_down; 

   private:
   bool debug = false;
   

};//DsPhiMuMuPi_tools

#endif
