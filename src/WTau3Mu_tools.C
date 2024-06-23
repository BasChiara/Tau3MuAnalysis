#include "../include/WTau3Mu_tools.h"

#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#include <boost/bind/bind.hpp>
#include "boost/property_tree/ptree.hpp"
#include "boost/property_tree/json_parser.hpp"
using namespace boost::placeholders;
namespace pt = boost::property_tree;

int   WTau3Mu_tools::MCtruthMatching(const bool verbose){
    
    int MCmatchTau_idx = -1;
    const float DR_threshold = 0.03;
    float DR_Mu1, DR_Mu2, DR_Mu3;
    float DRmin_Mu1 = DR_threshold, DRmin_Mu2 = DR_threshold, DRmin_Mu3 = DR_threshold;
    float Dpt_Mu1, Dpt_Mu2, Dpt_Mu3;

    
    for(unsigned int t = 0; t < nTauTo3Mu; t++){

        // mu 1
        RecoMu1_P4.SetPt(TauTo3Mu_mu1_pt[t]); RecoMu1_P4.SetEta(TauTo3Mu_mu1_eta[t]); RecoMu1_P4.SetPhi(TauTo3Mu_mu1_phi[t]);
        DR_Mu1 = ROOT::Math::VectorUtil::DeltaR(GenMu1_P4, RecoMu1_P4);
        // mu 2
        RecoMu2_P4.SetPt(TauTo3Mu_mu2_pt[t]); RecoMu2_P4.SetEta(TauTo3Mu_mu2_eta[t]); RecoMu2_P4.SetPhi(TauTo3Mu_mu2_phi[t]);
        DR_Mu2 = ROOT::Math::VectorUtil::DeltaR(GenMu2_P4, RecoMu2_P4);
        // mu 3
        RecoMu3_P4.SetPt(TauTo3Mu_mu3_pt[t]); RecoMu3_P4.SetEta(TauTo3Mu_mu3_eta[t]); RecoMu3_P4.SetPhi(TauTo3Mu_mu3_phi[t]);
        DR_Mu3 = ROOT::Math::VectorUtil::DeltaR(GenMu3_P4, RecoMu3_P4);

        if(verbose){
            std::cout << " - starting tau cand number " << t << std::endl;
            std::cout << Form(" DR_1 = %.4f \t DR_2 = %.4f \t DR_3 = %.4f", DR_Mu1, DR_Mu2, DR_Mu3 ) << std::endl;
        }

        if(DR_Mu1 < DRmin_Mu1 && DR_Mu2 < DRmin_Mu2 && DR_Mu3 < DRmin_Mu3 ){
            DRmin_Mu1 = DR_Mu1; DRmin_Mu2 = DR_Mu2; DRmin_Mu3 = DR_Mu3;
            Dpt_Mu1 = fabs(GenMu1_P4.Pt() - RecoMu1_P4.Pt())/GenMu1_P4.Pt(); 
            Dpt_Mu2 = fabs(GenMu2_P4.Pt() - RecoMu2_P4.Pt())/GenMu2_P4.Pt();
            Dpt_Mu3 = fabs(GenMu3_P4.Pt() - RecoMu3_P4.Pt())/GenMu3_P4.Pt();
            MCmatchTau_idx = t;
        }

    }// loop on tau candidate

    if (verbose){
        std::cout << " MC-matching found w tau cand " << MCmatchTau_idx << std::endl;
        std::cout << Form(" DRmin_1 = %.4f \t DRmin_2 = %.4f \t DRmin_3 = %.4f", DRmin_Mu1, DRmin_Mu2, DRmin_Mu3 ) << std::endl;
        std::cout << Form(" Dpt_1 = %.4f \t Dpt_2 = %.4f \t Dpt_3 = %.4f", Dpt_Mu1, Dpt_Mu2, Dpt_Mu3 ) << std::endl;
    } 
    return MCmatchTau_idx;

}// MCtruthMatching


std::vector<unsigned int> WTau3Mu_tools::sorted_cand_mT(){

   if (debug) std::cout << " #cand " << nTauTo3Mu << std::endl;
   // initialize cand-idx vector 
   std::vector<unsigned int> cand_idx(nTauTo3Mu, 0);
   iota(cand_idx.begin(), cand_idx.end(), 0);
   // if more than one sort by mT
   if (cand_idx.size() > 1){
   
      if(debug) std::cout << " sort by mT..." << std::endl;
      std::vector<float> mT_v(TauPlusMET_Tau_Puppi_mT, TauPlusMET_Tau_Puppi_mT + nTauTo3Mu); 
      stable_sort(cand_idx.begin(), cand_idx.end(), [&mT_v](size_t i1, size_t i2) {return mT_v[i1] >  mT_v[i2];});
      if(debug){
         std::cout << " unsorted mT "<< std::endl;
         for(float m : mT_v) std::cout << "\t" << m << std::endl;
         std::cout << " sorted mT "<< std::endl;
         for(float i : cand_idx) std::cout << "\t" << i << "\t" << mT_v[i] << std::endl;
      }
   }
   return cand_idx;

}//sorted_cand_mT()

bool WTau3Mu_tools::TriggerMatching(const int TauIdx, const int config){
   //int trigger_configuration = (config == -1 ? HLTconf_ : config);
   int trigger_configuration = config;
   bool is_fired_trigger = false;
   bool is_fired_Tau3Mu = false, is_fired_DoubleMu = false;
   if(trigger_configuration == HLT_paths::HLT_Tau3Mu){
      // check if the 3 muons + tau fired the trigger
      bool is_fired_1 = HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                           TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[TauIdx] &&
                           TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[TauIdx] &&
                           TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[TauIdx] &&
                           TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[TauIdx];
      bool is_fired_2 = HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 &&
                           TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[TauIdx] &&
                           TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[TauIdx] &&
                           TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[TauIdx]&&
                           TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[TauIdx];
      is_fired_Tau3Mu = (is_fired_1 || is_fired_2) && HLT_Tau3Mu_emulator(TauIdx);
   }
   if(trigger_configuration == HLT_paths::HLT_DoubleMu ){
      is_fired_DoubleMu = HLT_DoubleMu4_3_LowMass &&
	   (
	   (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx]) ||
	   (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx]) ||
	   (TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx])
	   ) && 
     HLT_DoubleMu_emulator(TauIdx);
    }
    //if(trigger_configuration == HLT_paths::HLT_overlap) is_fired_trigger = true;
    is_fired_trigger = is_fired_Tau3Mu || is_fired_DoubleMu;
    return is_fired_trigger;
}//TriggerMatching()


bool WTau3Mu_tools::HLT_Tau3Mu_emulator(const int TauIdx){

    //** single muon
    const float minPT_mu1 = 7.0, minPT_mu2 = 1.0, minPT_mu3 = 1.0;
    const float maxEta_mu = 2.5;
    if(RecoMu1_P4.Pt() < minPT_mu1 || RecoMu2_P4.Pt() < minPT_mu2 || RecoMu3_P4.Pt() < minPT_mu3 ) return false;
    if(fabs(RecoMu1_P4.Eta()) > maxEta_mu || fabs(RecoMu2_P4.Eta()) > maxEta_mu || fabs(RecoMu3_P4.Eta()) > maxEta_mu ) return false;

    //** di-muon
    const float minM_mumu = 2*Muon_MASS, maxM_mumu = 1.9;
    const float maxDR_muBS = 0.5, maxDZ_mumu = 0.7;
    if(!((TauTo3Mu_dZmu12[TauIdx] < maxDZ_mumu && TauTo3Mu_mu1_dr[TauIdx] < maxDR_muBS && TauTo3Mu_mu2_dr[TauIdx] < maxDR_muBS && (RecoMu1_P4+RecoMu2_P4).M() > minM_mumu && (RecoMu1_P4+RecoMu2_P4).M() < maxM_mumu ) ||  // mu_1, mu_2
         (TauTo3Mu_dZmu23[TauIdx] < maxDZ_mumu && TauTo3Mu_mu2_dr[TauIdx] < maxDR_muBS && TauTo3Mu_mu3_dr[TauIdx] < maxDR_muBS && (RecoMu2_P4+RecoMu3_P4).M() > minM_mumu && (RecoMu2_P4+RecoMu3_P4).M() < maxM_mumu ) ||  // mu_2, mu_3
         (TauTo3Mu_dZmu13[TauIdx] < maxDZ_mumu && TauTo3Mu_mu1_dr[TauIdx] < maxDR_muBS && TauTo3Mu_mu3_dr[TauIdx] < maxDR_muBS && (RecoMu1_P4+RecoMu3_P4).M() > minM_mumu && (RecoMu1_P4+RecoMu3_P4).M() < maxM_mumu) )  // mu_1, mu_3
    ) return false;

    //** muon-Tau
    const float maxDZ_muTau = 0.3, maxDR_muTau = 0.3;
    //if(0) return false; // insert the selection on DZ(tau,mu)
    if( ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoTau_P4) > maxDR_muTau ||
        ROOT::Math::VectorUtil::DeltaR( RecoMu2_P4 ,RecoTau_P4) > maxDR_muTau || 
        ROOT::Math::VectorUtil::DeltaR( RecoMu3_P4 ,RecoTau_P4) > maxDR_muTau) return false;

    //** TAU
    const float minPT_tau = 15.0, maxEta_tau = 2.5, minM_tau = 1.3, maxM_tau = 2.1;
    if(RecoTau_P4.Pt() < minPT_tau || RecoTau_P4.M() < minM_tau || RecoTau_P4.M() > maxM_tau || fabs(RecoTau_P4.Eta()) > maxEta_tau) return false;
    const float maxIsoCh_tau = 2.0, maxRelIsoCh_tau = 0.2;
    // --> Iso @ HLT level not comparable with reco isolation offline 
    //if(TauTo3Mu_iso_ptChargedFromPV[TauIdx] > maxIsoCh_tau || TauTo3Mu_iso_ptChargedFromPV[TauIdx]/RecoTau_P4.Pt() > maxRelIsoCh_tau) return false;
    
    return true;

}//HLT_emulator()

bool WTau3Mu_tools::HLT_DoubleMu_emulator(const int TauIdx){
  
  // which pair
  bool use12=false;
  bool use13=false;
  bool use23=false;
  if (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx]) use12=true;
  if (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx]) use13=true;
  if (TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx]) use23=true;

  // single muon - eta
  const float maxEta_mu = 2.5;
  if (use12 && ( (fabs(RecoMu1_P4.Eta()) > maxEta_mu) || (fabs(RecoMu2_P4.Eta()) > maxEta_mu) )) use12=false;
  if (use13 && ( (fabs(RecoMu1_P4.Eta()) > maxEta_mu) || (fabs(RecoMu3_P4.Eta()) > maxEta_mu) )) use12=false;
  if (use23 && ( (fabs(RecoMu2_P4.Eta()) > maxEta_mu) || (fabs(RecoMu3_P4.Eta()) > maxEta_mu) )) use23=false;
  if (!use12 && !use13 && !use23) return false;

  // single muon
  // * pT
  const float minPT_mu1 = 4.0, minPT_mu2 = 3.0;
  float minPt=-999.;
  float maxPt=-999.;
  if (use12) {
    if (RecoMu1_P4.Pt()>RecoMu2_P4.Pt()) { maxPt = RecoMu1_P4.Pt(); minPt = RecoMu2_P4.Pt(); }
    else { maxPt = RecoMu2_P4.Pt(); minPt = RecoMu1_P4.Pt(); }
    use12 = maxPt > minPT_mu1 && minPt > minPT_mu2;

  }
  if (use13) {
    if (RecoMu1_P4.Pt()>RecoMu3_P4.Pt()) { maxPt = RecoMu1_P4.Pt(); minPt = RecoMu3_P4.Pt(); }
    else { maxPt = RecoMu3_P4.Pt(); minPt = RecoMu1_P4.Pt(); }
    use13 = maxPt > minPT_mu1 && minPt > minPT_mu2;
  }
  if (use23) {
    if (RecoMu2_P4.Pt()>RecoMu3_P4.Pt()) { maxPt = RecoMu2_P4.Pt(); minPt = RecoMu3_P4.Pt(); }
    else { maxPt = RecoMu3_P4.Pt(); minPt = RecoMu2_P4.Pt(); }
    use23 = maxPt > minPT_mu1 && minPt > minPT_mu2;
  }
  if (!use12 && !use13 && !use23) return false;
  // * compatibility with BS
  const float maxDR_mu = 2.0;
  if(use12 && (TauTo3Mu_mu1_dr[TauIdx]>maxDR_mu || TauTo3Mu_mu2_dr[TauIdx]>maxDR_mu )) use12 = false;
  if(use13 && (TauTo3Mu_mu1_dr[TauIdx]>maxDR_mu || TauTo3Mu_mu3_dr[TauIdx]>maxDR_mu )) use13 = false;
  if(use23 && (TauTo3Mu_mu2_dr[TauIdx]>maxDR_mu || TauTo3Mu_mu3_dr[TauIdx]>maxDR_mu )) use23 = false;
  if (!use12 && !use13 && !use23) return false;

  // double muon
  float ptMM=-999.;
  float massMM=-999.;
  const float minPT_mumu = 4.9, minM_mumu = 0.2, maxM_mumu = 8.5;

  if (use12) {
    ptMM=(RecoMu1_P4+RecoMu2_P4).Pt();
    massMM=(RecoMu1_P4+RecoMu2_P4).M();
    use12 = massMM>minM_mumu && massMM< maxM_mumu && ptMM> minPT_mumu;
  }
  if (use13) {
    ptMM=(RecoMu1_P4+RecoMu3_P4).Pt();
    massMM=(RecoMu1_P4+RecoMu3_P4).M();
    use13 = massMM>minM_mumu && massMM< maxM_mumu && ptMM> minPT_mumu;
  }
  if (use23) {
    ptMM=(RecoMu2_P4+RecoMu3_P4).Pt();
    massMM=(RecoMu2_P4+RecoMu3_P4).M();
    use23 = massMM>minM_mumu && massMM< maxM_mumu && ptMM> minPT_mumu;
  }
  if (!use12 && !use13 && !use23) return false;

 
  const float maxDCA_mumu = 0.5;
  if(use12) use12 = TauTo3Mu_mu12_DCA[TauIdx] < maxDCA_mumu; 
  if(use13) use13 = TauTo3Mu_mu13_DCA[TauIdx] < maxDCA_mumu; 
  if(use23) use23 = TauTo3Mu_mu23_DCA[TauIdx] < maxDCA_mumu; 
  if (!use12 && !use13 && !use23) return false;
  const float minVtx_prob = 0.005; // on MuMu vertex fit
  if(use12) use12 = TauTo3Mu_mu12_vtxFitProb[TauIdx] > minVtx_prob;
  if(use13) use13 = TauTo3Mu_mu13_vtxFitProb[TauIdx] > minVtx_prob;
  if(use23) use23 = TauTo3Mu_mu23_vtxFitProb[TauIdx] > minVtx_prob;
  if (!use12 && !use13 && !use23) return false;

  return true;

}//HLT_DoubleMu_emulator()

bool WTau3Mu_tools::HLT_DoubleMu_reinforcement(const int TauIdx){
    

   const float minPT_mu1 = 7.0, minPT_mu3 = 1.0;
   if(RecoMu1_P4.Pt() < minPT_mu1 || RecoMu3_P4.Pt() < minPT_mu3 ) return false;
   const float minPT_tau = 15.0;
   if(RecoTau_P4.Pt() < minPT_tau) return false;
   const float maxM_mumu = 1.9;
   const float maxDZ_mumu = 0.7;
   if(!( (TauTo3Mu_dZmu12[TauIdx] < maxDZ_mumu && (RecoMu1_P4+RecoMu2_P4).M() < maxM_mumu ) ||  // mu_1, mu_2
         (TauTo3Mu_dZmu23[TauIdx] < maxDZ_mumu && (RecoMu2_P4+RecoMu3_P4).M() < maxM_mumu ) ||  // mu_2, mu_3
         (TauTo3Mu_dZmu13[TauIdx] < maxDZ_mumu && (RecoMu1_P4+RecoMu3_P4).M() < maxM_mumu) )  // mu_1, mu_3
    ) return false;

   return true;

}//HLT_DoubleMu_reinforcement()

void  WTau3Mu_tools::GenPartFillP4(){
    
   bool debug = false; 
   int Mu1_idx = -1, Mu2_idx = -1, Mu3_idx = -1, Tau_idx = -1, Nu_idx = -1, W_idx = -1;
   std::vector<int> Muons_idxs;
   std::vector<int> Taus_idxs;
   std::vector<float> Muons_pt;
   if (debug) {
      for (UInt_t g = 0; g < nGenPart; g++)std::cout << g << " \t " << GenPart_pdgId[g] << " \t " << GenPart_genPartIdxMother[g] << std::endl;
   }


   int mu1 = -1, mu2 = -1, mu3 = -1;
   bool tau3Mu_found = false;

   for (UInt_t g = 0; g < nGenPart; g++){

      // look for 3 muons from same Tau 
      if (GenPart_genPartIdxMother[g] < 0 ) continue;
      if(abs(GenPart_pdgId[g]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isTau
            && !tau3Mu_found)
      {
         mu1 = g;
         int Tau_idx = GenPart_genPartIdxMother[g];
         if (debug) std::cout << " mu1 found @" << mu1 << std::endl;
         for(UInt_t gg = g+1; gg < nGenPart; gg++){
            if (GenPart_genPartIdxMother[gg] < 0) continue;
            if(abs(GenPart_pdgId[gg]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[gg]]) == isTau
            && GenPart_genPartIdxMother[gg] == Tau_idx
            && !tau3Mu_found){
               if(mu1 == gg) continue;
               mu2 = gg;
               if (debug) std::cout << " mu2 found @" << mu2 << std::endl;
               for(UInt_t ggg = gg+1; ggg < nGenPart; ggg++){ 
                  if(GenPart_genPartIdxMother[ggg] < 0) continue;
                  if(abs(GenPart_pdgId[ggg]) == isMuon 
                     && abs(GenPart_pdgId[GenPart_genPartIdxMother[ggg]]) == isTau
                     && GenPart_genPartIdxMother[ggg] == Tau_idx
                     && !tau3Mu_found){
                     if(mu2 == ggg) continue;
                     mu3 = ggg;
                     if (debug) std::cout << " mu3 found @" << mu3 << std::endl;
                     tau3Mu_found = true;
                  }
               }
            }
         }
      }
      // look for tauonic neutrinos
      if(abs(GenPart_pdgId[g]) == isNuTau
         && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isW) Nu_idx = g;
     
   }// loop on gen particles

   if ((mu1<0)||(mu2<0)||(mu3<0)) return;

   // save Muon and Tau idx
   Muons_idxs.push_back(mu1); Muons_idxs.push_back(mu2); Muons_idxs.push_back(mu3); 
   Taus_idxs.push_back(GenPart_genPartIdxMother[mu1]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu2]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu3]);
   Muons_pt.push_back(GenPart_pt[mu1]); Muons_pt.push_back(GenPart_pt[mu2]); Muons_pt.push_back(GenPart_pt[mu3]);

   
   if(Muons_idxs.size() < 3){
      std::cout << " [ERROR] wrong number of gen-muons it is " << Muons_idxs.size() << std::endl;
      exit(-1);
   }else if(Muons_idxs.size() == 3){
      if (debug) std::cout << " [OK] 3 muons found" << std::endl;
      // Tau index & Tau's mother idx 
      Tau_idx = Taus_idxs[0];
      int motherTau_idx = GenPart_genPartIdxMother[Tau_idx];
         // Tau comes from W
      if (abs(GenPart_pdgId[motherTau_idx]) == isW)
      {
         W_idx = motherTau_idx;   
         // in case of tau radiative decays
      }else if( abs(GenPart_pdgId[motherTau_idx]) == isTau 
               && abs(GenPart_pdgId[GenPart_genPartIdxMother[motherTau_idx]]) == isW)
      {
         Tau_idx = motherTau_idx;
         W_idx = GenPart_genPartIdxMother[motherTau_idx]; 
      }  
   }else{
      std::cout << " [!!] number of gen-muons from taus is " << Muons_idxs.size() << std::endl;
      if(debug){
         for (int i=0; i < Taus_idxs.size(); i++) std::cout << Form("tau : %d\t mu: %d", Taus_idxs[i] , Muons_idxs[i])<< std::endl;
      }
      exit(-1);
   }


   // order muons in leading, sub-leading and trailing
   std::sort(Muons_idxs.begin(),Muons_idxs.end(), [this](int &a, int &b){ return GenPart_pt[a]>GenPart_pt[b]; });
   Mu1_idx = Muons_idxs[0]; 
   Mu2_idx = Muons_idxs[1]; 
   Mu3_idx = Muons_idxs[2]; 
   
   GenW_P4.SetPt(GenPart_pt[W_idx]); GenW_P4.SetEta(GenPart_eta[W_idx]); GenW_P4.SetPhi(GenPart_phi[W_idx]); GenW_P4.SetM(W_MASS);
   GenTau_P4.SetPt(GenPart_pt[Tau_idx]); GenTau_P4.SetEta(GenPart_eta[Tau_idx]); GenTau_P4.SetPhi(GenPart_phi[Tau_idx]); GenTau_P4.SetM(Tau_MASS);
   GenNu_P4.SetPt(GenPart_pt[Nu_idx]); GenNu_P4.SetEta(GenPart_eta[Nu_idx]); GenNu_P4.SetPhi(GenPart_phi[Nu_idx]); GenNu_P4.SetM(NuTau_MASS);
   GenMu1_P4.SetPt(GenPart_pt[Mu1_idx]); GenMu1_P4.SetEta(GenPart_eta[Mu1_idx]); GenMu1_P4.SetPhi(GenPart_phi[Mu1_idx]); GenMu1_P4.SetM(Muon_MASS);
   GenMu2_P4.SetPt(GenPart_pt[Mu2_idx]); GenMu2_P4.SetEta(GenPart_eta[Mu2_idx]); GenMu2_P4.SetPhi(GenPart_phi[Mu2_idx]); GenMu2_P4.SetM(Muon_MASS);
   GenMu3_P4.SetPt(GenPart_pt[Mu3_idx]); GenMu3_P4.SetEta(GenPart_eta[Mu3_idx]); GenMu3_P4.SetPhi(GenPart_phi[Mu3_idx]); GenMu3_P4.SetM(Muon_MASS);

   if(debug){
      std::cout << " W found @ "    << W_idx << std::endl;
      std::cout << " nu found @ "   << Nu_idx << std::endl;
      std::cout << " tau found @ "  << Tau_idx << std::endl;
      std::cout << " Mu found @ "   << Mu1_idx  << " " << Mu2_idx << " "<< Mu3_idx << std::endl;
      std::cout << " Mu pT "        << GenPart_pt[Mu1_idx] << " " << GenPart_pt[Mu2_idx] << " "<< GenPart_pt[Mu3_idx] << std::endl;
   }

} // GenPartFillP4()

bool  WTau3Mu_tools::RecoPartFillP4(const int TauIdx){

    // require mediumID for all muons
    bool muonsTrksQualityCheck = Muon_isMedium[TauTo3Mu_mu1_idx[TauIdx]] && 
                                Muon_isMedium[TauTo3Mu_mu2_idx[TauIdx]] && 
                                Muon_isMedium[TauTo3Mu_mu3_idx[TauIdx]];

    // muons
    RecoMu1_P4.SetPt(TauTo3Mu_mu1_pt[TauIdx]); RecoMu1_P4.SetEta(TauTo3Mu_mu1_eta[TauIdx]); RecoMu1_P4.SetPhi(TauTo3Mu_mu1_phi[TauIdx]); RecoMu1_P4.SetM(Muon_MASS);
    RecoMu2_P4.SetPt(TauTo3Mu_mu2_pt[TauIdx]); RecoMu2_P4.SetEta(TauTo3Mu_mu2_eta[TauIdx]); RecoMu2_P4.SetPhi(TauTo3Mu_mu2_phi[TauIdx]); RecoMu2_P4.SetM(Muon_MASS);
    RecoMu3_P4.SetPt(TauTo3Mu_mu3_pt[TauIdx]); RecoMu3_P4.SetEta(TauTo3Mu_mu3_eta[TauIdx]); RecoMu3_P4.SetPhi(TauTo3Mu_mu3_phi[TauIdx]); RecoMu3_P4.SetM(Muon_MASS);

    // tau
    RecoTau_P4.SetPt(TauTo3Mu_fitted_pt[TauIdx]);  RecoTau_P4.SetEta(TauTo3Mu_fitted_eta[TauIdx]); RecoTau_P4.SetPhi(TauTo3Mu_fitted_phi[TauIdx]);  RecoTau_P4.SetM(TauTo3Mu_fitted_mass[TauIdx]);

    // met in the transverse plane

    // W in the transverse plane

    return muonsTrksQualityCheck;
}// RecoPartFillP4

bool WTau3Mu_tools::applyMETfilters(const int& TauIdx){
   
   bool passed_filter = TauPlusMET_Flag_BadPFMuonDzFilter[TauIdx] &&
                        TauPlusMET_Flag_BadPFMuonFilter[TauIdx] &&
                        TauPlusMET_Flag_EcalDeadCellTriggerPrimitiveFilter[TauIdx] &&
                        TauPlusMET_Flag_eeBadScFilter[TauIdx] &&
                        TauPlusMET_Flag_globalSuperTightHalo2016Filter[TauIdx] &&
                        TauPlusMET_Flag_goodVertices[TauIdx] &&
                        TauPlusMET_Flag_hfNoisyHitsFilter[TauIdx];

   return passed_filter;

}//applyMETfilters()

int WTau3Mu_tools::parseMuonSF(const TString & era, const TString & pTrange){
   
   // retrive json file from constants.h
   std::string sf_json_name;
   if (pTrange == "low") sf_json_name = scale_factor_src::IDsf_jsonfile_Jpsi[era]; 
   if (pTrange == "medium") sf_json_name = scale_factor_src::IDsf_jsonfile_Z[era]; 
   std::cout << "[+] parse Muon SF from \n " << sf_json_name << std::endl; 

   // Load the JSON file
   pt::ptree sf_json;
   try {
      pt::read_json(sf_json_name, sf_json);
   } catch (pt::json_parser_error &e) {
        std::cerr << " JSON parsing error: " << e.what() << std::endl;
        return 1;
   } catch (std::exception &e) {
        std::cerr << " Error reading JSON file: " << e.what() << std::endl;
        return 1;
   }

   // Accessing data
   pt::ptree data_content; 
   for (const auto& corr : sf_json.get_child("corrections")){
      // look for the needed corrections-set
      std::string current_sf_set = corr.second.get_child("name").data(); 
      if(debug) std::cout <<  current_sf_set << std::endl;
      if (current_sf_set != muons_IDsf_set_) continue;
      // pick the desired SF set
      data_content = corr.second.get_child("data");
   }
   // define eta-bins
   std::vector<float> eta_edges;
   for (const auto& edge : data_content.get_child("edges")) {
      eta_edges.push_back(edge.second.get_value<float>());
   }
   int N_eta_bins = eta_edges.size() - 1;
   if(debug) std::cout<< "> found " << N_eta_bins << " bins for eta " << std::endl; 
   //define pT bins in each eta-bin
   int ieta = 0;
   // ** TH2F with SF
   TH2Poly* h_muonSF_      = new TH2Poly();
   TH2Poly* h_muonSF_sUP   = new TH2Poly(); 
   TH2Poly* h_muonSF_sDOWN = new TH2Poly(); 
   TString h_muonSF_name = "h_" + TString(muons_IDsf_set_) + "_" + era +"_" +pTrange;
   h_muonSF_->SetNameTitle(h_muonSF_name + "_val", "ID/reco muon SF value");
   h_muonSF_sUP->SetNameTitle(h_muonSF_name + "_sUP", "ID/reco muon SF +sys");
   h_muonSF_sDOWN->SetNameTitle(h_muonSF_name + "_sDOWN", "ID/reco muon SF -sys");
   float deta = 0.01, dpt = 0.01;
   for (const auto& pT_binning : data_content.get_child("content")){
      std::vector<float> pt_edges;
      for(const auto& edge : pT_binning.second.get_child("edges")) pt_edges.push_back(edge.second.get_value<float>());
      // if low-pT lower pT bin has edge at 0 GeV
      if (pTrange == "low") pt_edges.front() = 0.0; 
      int N_pt_bins = pt_edges.size() - 1;
      if(debug) std::cout<< Form("> eta [%.1f, %.1f] with %d pT bins", eta_edges.at(ieta), eta_edges.at(ieta+1), N_pt_bins ) << std::endl; 
      int ipT = 0;
      // retrive SF in each bin
      for (const auto& category : pT_binning.second.get_child("content")){
         for (const auto& sf_val : category.second.get_child("content")){
            float xlo = eta_edges.at(ieta), xhi = eta_edges.at(ieta+1), ylo = pt_edges.at(ipT), yhi =  pt_edges.at(ipT + 1); 
            // SF nominal value
            if (sf_val.second.get_child("key").data() == "nominal"){
               if(debug) std::cout<< Form("> eta [%.1f, %.1f] pT [%.1f, %.1f] -> SF : %.3f", eta_edges.at(ieta), eta_edges.at(ieta+1),pt_edges.at(ipT), pt_edges.at(ipT + 1), sf_val.second.get<double>("value") ) << std::endl; 
               h_muonSF_->AddBin(xlo, ylo, xhi, yhi); 
               h_muonSF_->Fill(xlo+ deta, ylo + dpt, sf_val.second.get<double>("value"));
            // SF nominal value + sys-err
            } else if (sf_val.second.get_child("key").data() == "systup"){
               h_muonSF_sUP->AddBin(xlo, ylo, xhi, yhi); 
               h_muonSF_sUP->Fill(xlo+ deta, ylo + dpt, sf_val.second.get<double>("value"));
            // SF nominal value - sys-err
            } else if (sf_val.second.get_child("key").data() == "systdown"){
               h_muonSF_sDOWN->AddBin(xlo, ylo, xhi, yhi); 
               h_muonSF_sDOWN->Fill(xlo+ deta, ylo + dpt, sf_val.second.get<double>("value"));
            }
           
         } 
         ipT++;
      }
      ieta++;
   }

   // save histogram in the correct pointer
   if (pTrange == "low"){
      h_muonSF_lowpT = h_muonSF_;
      h_muonSF_lowpT_sysUP = h_muonSF_sUP;
      h_muonSF_lowpT_sysDOWN = h_muonSF_sDOWN;
   }
   else if (pTrange == "medium"){
      h_muonSF_medpT = h_muonSF_;
      h_muonSF_medpT_sysUP = h_muonSF_sUP;
      h_muonSF_lowpT_sysDOWN = h_muonSF_sDOWN;
   }
   return 0;

}// parseMuonSF()

int WTau3Mu_tools::applyMuonSF(const int& TauIdx){
   
   float cand_SF = 1.0;
   int bin = -5;
   // mu1
   bin = h_muonSF_lowpT->FindBin(fabs(TauTo3Mu_mu1_eta[TauIdx]), TauTo3Mu_mu1_pt[TauIdx]);
   tau_mu1_IDrecoSF           = (bin > 0 ? h_muonSF_lowpT->GetBinContent(bin) : 1.0);
   tau_mu1_IDrecoSF_sysUP     = (bin > 0 ? h_muonSF_lowpT_sysUP->GetBinContent(bin) : 1.0);
   tau_mu1_IDrecoSF_sysDOWN   = (bin > 0 ? h_muonSF_lowpT_sysDOWN->GetBinContent(bin) : 1.0);
   if(debug) std::cout << Form("> mu1 (pT, eta) = (%.2f,%.2f ) \t SF = %.3f", TauTo3Mu_mu1_pt[TauIdx], TauTo3Mu_mu1_eta[TauIdx], tau_mu1_IDrecoSF ) << std::endl;
   // mu2
   bin = h_muonSF_lowpT->FindBin(fabs(TauTo3Mu_mu2_eta[TauIdx]), TauTo3Mu_mu2_pt[TauIdx]);
   tau_mu2_IDrecoSF           = (bin > 0 ? h_muonSF_lowpT->GetBinContent(bin) : 1.0);
   tau_mu2_IDrecoSF_sysUP     = (bin > 0 ? h_muonSF_lowpT_sysUP->GetBinContent(bin) : 1.0);
   tau_mu2_IDrecoSF_sysDOWN   = (bin > 0 ? h_muonSF_lowpT_sysDOWN->GetBinContent(bin) : 1.0);
   if(debug) std::cout << Form("> mu2 (pT, eta) = (%.2f,%.2f ) \t SF = %.3f", TauTo3Mu_mu2_pt[TauIdx], TauTo3Mu_mu2_eta[TauIdx], tau_mu2_IDrecoSF ) << std::endl;
   // mu3
   bin = h_muonSF_lowpT->FindBin(fabs(TauTo3Mu_mu3_eta[TauIdx]), TauTo3Mu_mu3_pt[TauIdx]);
   tau_mu3_IDrecoSF           = (bin > 0 ? h_muonSF_lowpT->GetBinContent(bin) : 1.0);
   tau_mu3_IDrecoSF_sysUP     = (bin > 0 ? h_muonSF_lowpT_sysUP->GetBinContent(bin) : 1.0);
   tau_mu3_IDrecoSF_sysDOWN   = (bin > 0 ? h_muonSF_lowpT_sysDOWN->GetBinContent(bin) : 1.0);
   if(debug) std::cout << Form("> mu3 (pT, eta) = (%.2f,%.2f ) \t SF = %.3f", TauTo3Mu_mu3_pt[TauIdx], TauTo3Mu_mu3_eta[TauIdx], tau_mu3_IDrecoSF ) << std::endl;

   return 0;
}//applyMuonSF

int WTau3Mu_tools::parsePUweights(const TString & era){

   TFile * file_weights = new TFile(scale_factor_src::PUweight_rootfile);
   std::cout << "[+] parse PU weights from \n " << file_weights->GetName() << std::endl; 
   h_PUweights          = (TH1D*)((file_weights->Get(scale_factor_src::PUweights_hist[era]+"_nominal"))->Clone());
   h_PUweights->SetDirectory(0);
   h_PUweights_sysUP    = (TH1D*)((file_weights->Get(scale_factor_src::PUweights_hist[era]+"_up"))->Clone());
   h_PUweights_sysUP->SetDirectory(0);
   h_PUweights_sysDOWN  = (TH1D*)((file_weights->Get(scale_factor_src::PUweights_hist[era]+"_down"))->Clone());
   h_PUweights_sysDOWN->SetDirectory(0);

   file_weights->Close(); 
    
   return 0;
}//parsePUweights

int WTau3Mu_tools::applyPUreweight(){
   
   int bin = h_PUweights->FindBin(Pileup_nTrueInt); 
   if (bin < 0 ) std::cout << "[ERROR] Pileup_nTrueInt outside PU-weights range" << std::endl;
   PU_weight      = (bin > 0 ? h_PUweights->GetBinContent(bin) : 1.0 ); 
   PU_weight_up   = (bin > 0 ? h_PUweights_sysUP->GetBinContent(bin) : 1.0 ); 
   PU_weight_down = (bin > 0 ? h_PUweights_sysDOWN->GetBinContent(bin) : 1.0 ); 

   return 0;
}//applyPUreweight