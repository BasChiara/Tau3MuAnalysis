#ifndef DsPhiMuMuPi_tools_h
#define DsPhiMuMuPi_tools_h

#include "DsPhiMuMuPi_base.h"
#include "include/constants.h"
#define _USE_MATH_DEFINES
#include <cmath>
#include "Math/Vector4D.h"
#include "Math/GenVector/VectorUtil.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

class DsPhiMuMuPi_tools : public DsPhiMuMuPi_base{

   public:
   DsPhiMuMuPi_tools(TTree *tree=0, const bool& isMC = true) : DsPhiMuMuPi_base(tree, isMC){}
   virtual ~DsPhiMuMuPi_tools(){}

   virtual void     Loop(){}
   bool    TriggerMatching(const int TauIdx, const int config = -1);
   int     MCtruthMatching(const bool verbose = false);
   bool    GenPartFillP4();
   bool    RecoPartFillP4(const int idx);
   bool    HLT_Tau3Mu_emulator(const int TauIdx);
   bool    HLT_DoubleMu_emulator(const int TauIdx);


   // gen particle P4 
   ROOT::Math::PtEtaPhiMVector GenDs_P4;
   ROOT::Math::PtEtaPhiMVector GenPhi_P4, GenPi_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4;
   // reco particle P4 
   ROOT::Math::PtEtaPhiMVector RecoDs_P4;
   ROOT::Math::PtEtaPhiMVector RecoPhi_P4, RecoPi_P4;
   ROOT::Math::PtEtaPhiMVector RecoMu1_P4, RecoMu2_P4;
   
   private:
   

};//DsPhiMuMuPi_tools

#endif
