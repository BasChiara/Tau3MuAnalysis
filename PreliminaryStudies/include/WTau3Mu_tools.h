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

class WTau3Mu_tools : public WTau3Mu_base{

   public:
   WTau3Mu_tools(TTree *tree=0, const bool& isMC = true) : WTau3Mu_base(tree, isMC){}
   virtual ~WTau3Mu_tools(){}

   virtual void     Loop(){}
   bool    TriggerMatching(const int TauIdx, const int config = -1);
   int     MCtruthMatching(const bool verbose = false);
   void    GenPartFillP4();
   bool    RecoPartFillP4(const int idx);
   bool    HLT_Tau3Mu_emulator(const int TauIdx);
   bool    HLT_DoubleMu_emulator(const int TauIdx);
   bool    HLT_DoubleMu_reinforcement(const int TauIdx);
   std::vector<unsigned int> sorted_cand_mT();


   // gen particle P4 
   ROOT::Math::PtEtaPhiMVector GenW_P4;
   ROOT::Math::PtEtaPhiMVector GenTau_P4, GenNu_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4, GenMu3_P4;
   // reco  particle P4 
   ROOT::Math::PtEtaPhiMVector RecoW_P4;
   ROOT::Math::PtEtaPhiMVector RecoTau_P4, RecoMET_P4;
   ROOT::Math::PtEtaPhiMVector RecoMu1_P4, RecoMu2_P4, RecoMu3_P4;
   
   private:
   bool debug = false; 

};//WTau3Mu_tools

#endif
