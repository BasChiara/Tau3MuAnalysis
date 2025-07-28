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

  // how many HLT matching pairs?
  int nMatch = (int)use12 + (int)use13 + (int)use23;
  //h_DiMuon_HLTcand->Fill(nMatch);
  if (use12) h_DiMuon_HLTcand->Fill(1);
  else if (use13) h_DiMuon_HLTcand->Fill(2);
  else if (use23) h_DiMuon_HLTcand->Fill(3);

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

std::vector<int> WTau3Mu_tools::Gen3Mu_FindSort(){
   
   std::vector<int> Muons_idxs;
   int mu1 = -1, mu2 = -1, mu3 = -1;
   bool tau3Mu_found = false, debug = false;
   for (UInt_t g = 0; g < nGenPart; g++){
      
      if (GenPart_genPartIdxMother[g] < 0 ) continue;
      
      if(abs(GenPart_pdgId[g]) == isMuon 
      && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isTau
      && !tau3Mu_found)
      { // mu1
         mu1 = g;
         int Tau_idx = GenPart_genPartIdxMother[g];
         if (debug) std::cout << " mu1 found @" << mu1 << std::endl;

         for(UInt_t gg = g+1; gg < nGenPart; gg++){
            if (GenPart_genPartIdxMother[gg] < 0) continue;
            
            if(abs(GenPart_pdgId[gg]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[gg]]) == isTau
            && GenPart_genPartIdxMother[gg] == Tau_idx
            && !tau3Mu_found)
            { // mu2
               if(mu1 == gg) continue;
               mu2 = gg;
               if (debug) std::cout << " mu2 found @" << mu2 << std::endl;
               
               for(UInt_t ggg = gg+1; ggg < nGenPart; ggg++){
                  if(GenPart_genPartIdxMother[ggg] < 0) continue;

                  if(abs(GenPart_pdgId[ggg]) == isMuon 
                  && abs(GenPart_pdgId[GenPart_genPartIdxMother[ggg]]) == isTau
                  && GenPart_genPartIdxMother[ggg] == Tau_idx
                  && !tau3Mu_found)
                  { // mu3
                     if(mu2 == ggg) continue;
                     mu3 = ggg;
                     if (debug) std::cout << " mu3 found @" << mu3 << std::endl;
                     tau3Mu_found = true;
                  }
               }// loop on mu3
            }
         }// loop on mu2
      } 
   }// loop on gen particles

   Muons_idxs.push_back(mu1); Muons_idxs.push_back(mu2); Muons_idxs.push_back(mu3);
   if ((mu1<0)||(mu2<0)||(mu3<0)) std::cerr << " [ERROR] tau->3mu not found" << std::endl;
   else Muons_idxs = sortMu_pT(Muons_idxs);
   
   return Muons_idxs;

}//Gen3Mu_FindSort()

std::vector<int> WTau3Mu_tools::sortMu_pT(const std::vector<int>& muons){
   std::vector<int> sorted_muons;
   
   if(muons.size() < 3){
      std::cout << " [ERROR] wrong number of gen-muons it is " << muons.size() << std::endl;
      exit(-1);
   }else if(muons.size() == 3){
      sorted_muons = muons;
      std::sort(sorted_muons.begin(),sorted_muons.end(), [this](int &a, int &b){ return GenPart_pt[a]>GenPart_pt[b]; }); 
   }else{
      std::cout << " [!!] number of gen-muons from taus is " << muons.size() << std::endl;
      exit(-1);
   }

   return sorted_muons;
}// sortMu_pT()

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
   
   GenW_P4.SetPt(GenPart_pt[W_idx]); GenW_P4.SetEta(GenPart_eta[W_idx]); GenW_P4.SetPhi(GenPart_phi[W_idx]); GenW_P4.SetM(GenPart_mass[W_idx]);
   GenTau_P4.SetPt(GenPart_pt[Tau_idx]); GenTau_P4.SetEta(GenPart_eta[Tau_idx]); GenTau_P4.SetPhi(GenPart_phi[Tau_idx]); GenTau_P4.SetM(Tau_MASS);
   GenNu_P4.SetPt(GenPart_pt[Nu_idx]); GenNu_P4.SetEta(GenPart_eta[Nu_idx]); GenNu_P4.SetPhi(GenPart_phi[Nu_idx]); GenNu_P4.SetM(NuTau_MASS);
   GenMu1_P4.SetPt(GenPart_pt[Mu1_idx]); GenMu1_P4.SetEta(GenPart_eta[Mu1_idx]); GenMu1_P4.SetPhi(GenPart_phi[Mu1_idx]); GenMu1_P4.SetM(Muon_MASS);
   GenMu2_P4.SetPt(GenPart_pt[Mu2_idx]); GenMu2_P4.SetEta(GenPart_eta[Mu2_idx]); GenMu2_P4.SetPhi(GenPart_phi[Mu2_idx]); GenMu2_P4.SetM(Muon_MASS);
   GenMu3_P4.SetPt(GenPart_pt[Mu3_idx]); GenMu3_P4.SetEta(GenPart_eta[Mu3_idx]); GenMu3_P4.SetPhi(GenPart_phi[Mu3_idx]); GenMu3_P4.SetM(Muon_MASS);

   gen_W_idx_ = W_idx;
   gen_tau_idx_ = Tau_idx;
   gen_mu1_idx_ = Mu1_idx; gen_mu2_idx_ = Mu2_idx; gen_mu3_idx_ = Mu3_idx;

   if(debug){
      std::cout << " W found @ "    << W_idx << std::endl;
      std::cout << " nu found @ "   << Nu_idx << std::endl;
      std::cout << " tau found @ "  << Tau_idx << std::endl;
      std::cout << " Mu found @ "   << Mu1_idx  << " " << Mu2_idx << " "<< Mu3_idx << std::endl;
      std::cout << " Mu pT "        << GenPart_pt[Mu1_idx] << " " << GenPart_pt[Mu2_idx] << " "<< GenPart_pt[Mu3_idx] << std::endl;
   }

} // GenPartFillP4()

int WTau3Mu_tools::search_radiativeDecay(const int prod_idx, const int Mother_pdgId, const int Daugh_pdgId){
   // check wether there is a radiative decay
   int first_part_idx = prod_idx;
   int mother_idx = GenPart_genPartIdxMother[prod_idx];
   
   bool found_daugh = abs(GenPart_pdgId[first_part_idx]) == Daugh_pdgId && abs(GenPart_pdgId[mother_idx]) == Mother_pdgId;
   while (!found_daugh){//(tau_idx < 0){
      first_part_idx = mother_idx;
      mother_idx = GenPart_genPartIdxMother[mother_idx];
      if (mother_idx < 0) break;
      found_daugh = abs(GenPart_pdgId[first_part_idx]) == Daugh_pdgId && abs(GenPart_pdgId[mother_idx]) == Mother_pdgId && (GenPart_statusFlags[mother_idx] & (1<<13));
   }
   return first_part_idx;
}//search_radiativeDecay()

int WTau3Mu_tools::GenTauDecayMode(const int tau_idx){
   int decay_mode = TauDecayMode::UNDEFINED, pdgId = -1;
   bool nu_found = false;
   int Nu_idx = -1;
   for (int g = 0; g < nGenPart; g++){
      
      if (GenPart_genPartIdxMother[g] != tau_idx) continue;
      pdgId = abs(GenPart_pdgId[g]);
      
      if (pdgId == isNuTau) {
         nu_found = true; Nu_idx = g;
      }
      else if (decay_mode > 0) continue;
      else if (abs(pdgId) == isEle)    decay_mode = TauDecayMode::ELECTRONIC;
      else if (abs(pdgId) == isMuon)   decay_mode = TauDecayMode::MUONIC;
      else if (abs(pdgId) >= isPion_0) decay_mode = TauDecayMode::HADRONIC;
   
   }// loop on gen particles
   if (!nu_found && decay_mode == TauDecayMode::MUONIC) decay_mode = 10;
   GenNu_P4.SetPt(GenPart_pt[Nu_idx]); GenNu_P4.SetEta(GenPart_eta[Nu_idx]); GenNu_P4.SetPhi(GenPart_phi[Nu_idx]); GenNu_P4.SetM(NuTau_MASS);
   return decay_mode;
}//GenTauDecayMode()

int WTau3Mu_tools::GenPartFillP4_Z(){
   int oppositeTau_mode = TauDecayMode::UNDEFINED;
   bool debug = false;
   int tau3mu_idx = -1, tau_opposite_idx = -1;
   int tau3mu_origin_idx = -1, tau_opposite_origin_idx = -1, Z_idx = -1;
   if (debug) std::cout << " #gen particles " << nGenPart << std::endl;
   
   // tau->3mu side
   std::vector<int> tau3muons_idxs = Gen3Mu_FindSort();
   if (tau3muons_idxs.size() < 3) return oppositeTau_mode;
   if (tau3muons_idxs[0] < 0 || tau3muons_idxs[1] < 0 || tau3muons_idxs[2] < 0) return oppositeTau_mode;

   tau3mu_idx = GenPart_genPartIdxMother[tau3muons_idxs[0]];
   tau3mu_origin_idx = search_radiativeDecay(tau3mu_idx, isZ);

   // opposite side tau
   if (debug) std::cout << "g \t PDGid \t mother_idx \t pT(GeV) " << std::endl;
   for (int g = 0; g < nGenPart; g++){
      if (debug) std::cout << g << " \t " << GenPart_pdgId[g] << " \t " << GenPart_genPartIdxMother[g] << " \t" << GenPart_pt[g] << std::endl;
      
      if (GenPart_statusFlags[g] & (1<<4)
         && GenPart_genPartIdxMother[g] != tau3mu_idx
         && (abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[g]]]) == isTau || abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[g]]]) == isZ)
      )
      { // isTauDecayProduct
         tau_opposite_idx = GenPart_genPartIdxMother[g];
         tau_opposite_origin_idx = search_radiativeDecay(tau_opposite_idx, isZ);
      }
   }// loop on gen particles
   oppositeTau_mode = GenTauDecayMode(tau_opposite_idx);
   Z_idx = (GenPart_genPartIdxMother[tau3mu_origin_idx] == GenPart_genPartIdxMother[tau_opposite_origin_idx]) ? GenPart_genPartIdxMother[tau3mu_origin_idx] : -1;
   
   // fill P4
   int Mu1_idx = tau3muons_idxs[0], Mu2_idx = tau3muons_idxs[1], Mu3_idx = tau3muons_idxs[2];
   GenZ_P4.SetPt(GenPart_pt[Z_idx]); GenZ_P4.SetEta(GenPart_eta[Z_idx]); GenZ_P4.SetPhi(GenPart_phi[Z_idx]); GenZ_P4.SetM((GenPart_mass[Z_idx] > 0 ? GenPart_mass[Z_idx] : Z_MASS));
   GenTau_P4.SetPt(GenPart_pt[tau3mu_idx]); GenTau_P4.SetEta(GenPart_eta[tau3mu_idx]); GenTau_P4.SetPhi(GenPart_phi[tau3mu_idx]); GenTau_P4.SetM(Tau_MASS);
   GenMu1_P4.SetPt(GenPart_pt[Mu1_idx]); GenMu1_P4.SetEta(GenPart_eta[Mu1_idx]); GenMu1_P4.SetPhi(GenPart_phi[Mu1_idx]); GenMu1_P4.SetM(Muon_MASS);
   GenMu2_P4.SetPt(GenPart_pt[Mu2_idx]); GenMu2_P4.SetEta(GenPart_eta[Mu2_idx]); GenMu2_P4.SetPhi(GenPart_phi[Mu2_idx]); GenMu2_P4.SetM(Muon_MASS);
   GenMu3_P4.SetPt(GenPart_pt[Mu3_idx]); GenMu3_P4.SetEta(GenPart_eta[Mu3_idx]); GenMu3_P4.SetPhi(GenPart_phi[Mu3_idx]); GenMu3_P4.SetM(Muon_MASS);
   
   if (debug){
      std::cout << " tau3mu found @ " << tau3mu_idx << " radiative decay from " << tau3mu_origin_idx << std::endl;
      std::cout << " mu1 @ "<< tau3muons_idxs[0] << " mu2 @ "<< tau3muons_idxs[1] << " mu3 @ "<< tau3muons_idxs[2] << std::endl;
      std::cout << " tau opposite found @ " << tau_opposite_idx << " radiative deacy from "<< tau_opposite_origin_idx  <<" --> decay mode "<< oppositeTau_mode << std::endl;
      std::cout << " Z found @ " << Z_idx << std::endl;
   }
   gen_Z_idx_   = Z_idx;
   gen_tau_idx_ = tau3mu_idx;
   gen_mu1_idx_ = Mu1_idx; gen_mu2_idx_ = Mu2_idx; gen_mu3_idx_ = Mu3_idx;

   return oppositeTau_mode;
}//GenPartFillP4_Z()

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

int WTau3Mu_tools::parseHLT_SF(const TString & era){

   //TFile * file_efficiency = new TFile(scale_factor_src::L1_HLT_mPOG_eff_files[era]);
   //std::cout << "[+] parse L1 and HLT SFs from \n " << file_efficiency->GetName() << std::endl;
   //// L1
   //h_L1_efficiency_MC     = (TH2F*)file_efficiency->Get(scale_factor_src::L1_mPOG_eff_MC.c_str());   h_L1_efficiency_MC->SetDirectory(0);
   //h_L1_efficiency_DATA   = (TH2F*)file_efficiency->Get(scale_factor_src::L1_mPOG_eff_DATA.c_str()); h_L1_efficiency_DATA->SetDirectory(0);
   //// HLT
   //h_HLT_efficiency_MC    = (TH2F*)file_efficiency->Get(scale_factor_src::HLT_mPOG_eff_MC.c_str());   h_HLT_efficiency_MC->SetDirectory(0);
   //h_HLT_efficiency_DATA  = (TH2F*)file_efficiency->Get(scale_factor_src::HLT_mPOG_eff_DATA.c_str()); h_HLT_efficiency_DATA->SetDirectory(0);
   // --- L1 
   TFile * file_efficiency_L1 = new TFile(scale_factor_src::L1_eff_files[era]);
   std::cout << "[+] parse L1 SFs from \n " << file_efficiency_L1->GetName() << std::endl;
   h_L1_efficiency_MC     = (TH2F*)file_efficiency_L1->Get(scale_factor_src::h_eff_MC_name.c_str());
   h_L1_efficiency_MC->SetDirectory(0); h_L1_efficiency_MC->SetName("h_HLT_DoubleMu_L1efficiency_MC");
   h_L1_efficiency_DATA   = (TH2F*)file_efficiency_L1->Get(scale_factor_src::h_eff_DATA_name.c_str());
   h_L1_efficiency_DATA->SetDirectory(0); h_L1_efficiency_DATA->SetName("h_HLT_DoubleMu_L1efficiency_DATA");
   file_efficiency_L1->Close();
   // --- HLT
   TFile * file_efficiency_HLT = new TFile(scale_factor_src::HLT_eff_files[era]);
   std::cout << "[+] parse HLT SFs from \n " << file_efficiency_HLT->GetName() << std::endl;
   h_HLT_efficiency_MC     = (TH2F*)file_efficiency_HLT->Get(scale_factor_src::h_eff_MC_name.c_str());
   h_HLT_efficiency_MC->SetDirectory(0); h_HLT_efficiency_MC->SetName("h_HLT_DoubleMu_HLT_efficiency_MC");
   h_HLT_efficiency_DATA   = (TH2F*)file_efficiency_HLT->Get(scale_factor_src::h_eff_DATA_name.c_str());
   h_HLT_efficiency_DATA->SetDirectory(0); h_HLT_efficiency_DATA->SetName("h_HLT_DoubleMu_HLT_efficiency_DATA");
   file_efficiency_HLT->Close();

   return 0;
}// parseHLT_SF()

float WTau3Mu_tools::get_dimuon_efficiency(const float& pt, const float& eta, const float& DR, const TString& trigger, const TString& dataset, float* error){
   
   float l1_efficiency = -99, hlt_efficiency = -99;
   float l1_efficiency_error = 0.0, hlt_efficiency_error = 0.0; 
   float pt_touse = (pt > 50.0 ? 45.0 : pt);
   float x = pt_touse, y = fabs(eta);
   if (debug) std::cout << Form(" [HLT] get dimuon efficiency for (pt, eta) = (%.2f, %.2f) ", pt, eta) << std::endl;
   if (dataset == "data"){
      l1_efficiency_error  = h_L1_efficiency_DATA->GetBinError(h_L1_efficiency_DATA->FindBin(x,y));
      hlt_efficiency_error = h_HLT_efficiency_DATA->GetBinError(h_HLT_efficiency_DATA->FindBin(x,y)); 
   
      l1_efficiency  = h_L1_efficiency_DATA->GetBinContent(h_L1_efficiency_DATA->FindBin(x,y));
      hlt_efficiency = h_HLT_efficiency_DATA->GetBinContent(h_HLT_efficiency_DATA->FindBin(x,y));
   } else if (dataset == "mc"){
      l1_efficiency_error  = h_L1_efficiency_MC->GetBinError(h_L1_efficiency_MC->FindBin(x,y));
      hlt_efficiency_error = h_HLT_efficiency_MC->GetBinError(h_HLT_efficiency_MC->FindBin(x,y));
   
      l1_efficiency = h_L1_efficiency_MC->GetBinContent(h_L1_efficiency_MC->FindBin(x,y));
      hlt_efficiency = h_HLT_efficiency_MC->GetBinContent(h_HLT_efficiency_MC->FindBin(x,y));
   }
   if (error != 0){ 
      if (debug) std::cout << Form(" [L1] efficiency = %.3f +/- %.3f \t [HLT] efficiency = %.3f +/- %.3f", l1_efficiency, l1_efficiency_error, hlt_efficiency, hlt_efficiency_error) << std::endl;
      //*error = (l1_efficiency*hlt_efficiency) * sqrt( (l1_efficiency_error/l1_efficiency)*(l1_efficiency_error/l1_efficiency) + (hlt_efficiency_error/hlt_efficiency)*(hlt_efficiency_error/hlt_efficiency) );
      *error = sqrt( (l1_efficiency_error*hlt_efficiency)*(l1_efficiency_error*hlt_efficiency) + (l1_efficiency*hlt_efficiency_error)*(l1_efficiency*hlt_efficiency_error) );
      if (debug) std::cout << Form(" [Dimuon] efficiency = %.3f +/- %.3f", l1_efficiency*hlt_efficiency, *error) << std::endl;
   }

   return l1_efficiency * hlt_efficiency;
} // get_dimuon_efficiency


float WTau3Mu_tools::get_trimuon_efficiency(const TString& dataset, float* error){

   float eff_mu12 = -99.0, eff_mu23 = -99.0, eff_mu13 = -99.0;
   float eff_mu12_err = 0.0, eff_mu23_err = 0.0, eff_mu13_err = 0.0;
   float trimuon_eff = -99.0, trimuon_eff_err = 0.0;
   eff_mu12 = get_dimuon_efficiency(RecoMu2_P4.Pt(), fabs(RecoMu2_P4.Eta()), -1.0 , "", dataset, &eff_mu12_err);
   eff_mu23 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), -1.0 , "", dataset, &eff_mu23_err); 
   eff_mu13 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), -1.0 , "", dataset, &eff_mu13_err);

   trimuon_eff      = 1 - (1 - eff_mu12) * (1 - eff_mu23) * (1 - eff_mu13);
   trimuon_eff_err  = (eff_mu12_err/(1-eff_mu12)) * (eff_mu12_err/(1-eff_mu12));
   trimuon_eff_err += (eff_mu23_err/(1-eff_mu23)) * (eff_mu23_err/(1-eff_mu23));
   trimuon_eff_err += (eff_mu13_err/(1-eff_mu13)) * (eff_mu13_err/(1-eff_mu13));
   trimuon_eff_err  = (1-trimuon_eff) * sqrt(trimuon_eff_err);

   *error = trimuon_eff_err;
   
   if (debug) std::cout << Form(" [Trimuon] efficiency = %.3f +/- %.3f", trimuon_eff, trimuon_eff_err) << std::endl;
   return trimuon_eff;

}// get_trimuon_efficiency

//int WTau3Mu_tools::parseHLT_SF(const TString & era){
//   TFile * file_weights = new TFile(scale_factor_src::HLTeff_rootfile.c_str());
//   std::cout << "[+] parse HLT SF from \n " << file_weights->GetName() << std::endl;
//   // L1 
//   h_mc_L1_efficiency_barrel     = (TH2Poly*)file_weights->Get("h_mc_L1eff_barrel");   h_mc_L1_efficiency_barrel->SetDirectory(0); 
//   h_data_L1_efficiency_barrel   = (TH2Poly*)file_weights->Get("h_data_L1eff_barrel"); h_data_L1_efficiency_barrel->SetDirectory(0);
//   h_mc_L1_efficiency_overlap    = (TH2Poly*)file_weights->Get("h_mc_L1eff_overlap");  h_mc_L1_efficiency_overlap->SetDirectory(0);
//   h_data_L1_efficiency_overlap  = (TH2Poly*)file_weights->Get("h_data_L1eff_overlap");h_data_L1_efficiency_overlap->SetDirectory(0);
//   h_mc_L1_efficiency_endcap     = (TH2Poly*)file_weights->Get("h_mc_L1eff_endcap");   h_mc_L1_efficiency_endcap->SetDirectory(0);
//   h_data_L1_efficiency_endcap   = (TH2Poly*)file_weights->Get("h_data_L1eff_endcap"); h_data_L1_efficiency_endcap->SetDirectory(0);
//   // HLT
//   h_mc_HLT_efficiency_barrel    = (TH2Poly*)file_weights->Get("h_mc_HLTeff_barrel");   h_mc_HLT_efficiency_barrel->SetDirectory(0); 
//   h_data_HLT_efficiency_barrel  = (TH2Poly*)file_weights->Get("h_data_HLTeff_barrel"); h_data_HLT_efficiency_barrel->SetDirectory(0);
//   h_mc_HLT_efficiency_overlap   = (TH2Poly*)file_weights->Get("h_mc_HLTeff_overlap");  h_mc_HLT_efficiency_overlap->SetDirectory(0);
//   h_data_HLT_efficiency_overlap = (TH2Poly*)file_weights->Get("h_data_HLTeff_overlap");h_data_HLT_efficiency_overlap->SetDirectory(0);
//   h_mc_HLT_efficiency_endcap    = (TH2Poly*)file_weights->Get("h_mc_HLTeff_endcap");   h_mc_HLT_efficiency_endcap->SetDirectory(0);
//   h_data_HLT_efficiency_endcap  = (TH2Poly*)file_weights->Get("h_data_HLTeff_endcap"); h_data_HLT_efficiency_endcap->SetDirectory(0);
//
//   return 0;
//}//parseHLT_SF
//
//float WTau3Mu_tools::get_dimuon_efficiency(const float& pt, const float& eta, const float& DR, const TString& trigger, const TString& dataset){
//   float efficiency = -1.0;
//   int bin = 0;
//   if (debug) std::cout << Form(" [HLT] get dimuon efficiency for (pt, eta, DR) = (%.2f, %.2f, %.2f) ", pt, eta, DR) << std::endl;
//   while (efficiency < 0.001 && bin > -1){
//      bin = h_data_HLT_efficiency_barrel->FindBin(pt, DR);
//      if (eta < 0.9 ){ //barrel
//         if (trigger == "HLT") {
//            if (dataset == "data")    efficiency = h_data_HLT_efficiency_barrel->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_HLT_efficiency_barrel->GetBinContent(bin);
//         } else if (trigger == "L1") {
//            if (dataset == "data")    efficiency = h_data_L1_efficiency_barrel->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_L1_efficiency_barrel->GetBinContent(bin);
//         }  
//      } else if (eta < 1.2 ){ //overlap
//         if (trigger == "HLT") {
//            if (dataset == "data")    efficiency = h_data_HLT_efficiency_overlap->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_HLT_efficiency_overlap->GetBinContent(bin);
//         } else if (trigger == "L1") {
//            if (dataset == "data")    efficiency = h_data_L1_efficiency_overlap->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_L1_efficiency_overlap->GetBinContent(bin);
//         }
//      } else { //endcap
//         if (trigger == "HLT") {
//            if (dataset == "data")    efficiency = h_data_HLT_efficiency_endcap->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_HLT_efficiency_endcap->GetBinContent(bin);
//         } else if (trigger == "L1") {
//            if (dataset == "data")    efficiency = h_data_L1_efficiency_endcap->GetBinContent(bin);
//            else if (dataset == "mc") efficiency = h_mc_L1_efficiency_endcap->GetBinContent(bin);
//         }
//      }
//      if (debug) std::cout << Form(" [+] efficiency = %.3f", efficiency) << std::endl;
//      // if empty bin take the closest one on the left (= lower pT bin)
//      bin =- 2;   
//   }
//   return efficiency;
//}//get_dimuon_efficiency
//
//float WTau3Mu_tools::get_trimuon_efficiency(const TString& dataset){
//   
//   //L1 efficiency
//   if (debug) std::cout << "[HLT-SF] get L1 trimuon efficiency in "<< dataset << std::endl;
//   float L1eff_mu12 = 1.0, L1eff_mu13 = 1.0, L1eff_mu23 = 1.0;
//   L1eff_mu12 = get_dimuon_efficiency(RecoMu2_P4.Pt(), fabs(RecoMu2_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoMu2_P4), "L1", dataset);
//   L1eff_mu13 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoMu3_P4), "L1", dataset);
//   L1eff_mu23 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu2_P4 ,RecoMu3_P4), "L1", dataset);
//   float L1_eff_3mu = 1.0 - (1. - L1eff_mu12)*(1.-L1eff_mu13)*(1.-L1eff_mu23);
//   // HLT efficiency
//   if (debug) std::cout << "[HLT-SF] get HLT trimuon efficiency in "<< dataset << std::endl;
//   float HLTeff_mu12 = 1.0, HLTeff_mu13 = 1.0, HLTeff_mu23 = 1.0;
//   HLTeff_mu12 = get_dimuon_efficiency(RecoMu2_P4.Pt(), fabs(RecoMu2_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoMu2_P4), "HLT", dataset);
//   HLTeff_mu13 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoMu3_P4), "HLT", dataset);
//   HLTeff_mu23 = get_dimuon_efficiency(RecoMu3_P4.Pt(), fabs(RecoMu3_P4.Eta()), ROOT::Math::VectorUtil::DeltaR( RecoMu2_P4 ,RecoMu3_P4), "HLT", dataset);
//   float HLT_eff_3mu = 1.0 - (1. - HLTeff_mu12)*(1.-HLTeff_mu13)*(1.-HLTeff_mu23);
//
//   return (L1_eff_3mu * HLT_eff_3mu);
//   
//}//get_trimuon_efficiency

int WTau3Mu_tools::applyHLT_SF(){
   float mc_eff = -99.0, data_eff = -99.0;
   float mc_eff_err = 0.0, data_eff_err = 0.0;

   // MC DATA efficiencies nominal
   mc_eff = get_trimuon_efficiency("mc", &mc_eff_err);
   data_eff = get_trimuon_efficiency("data", &data_eff_err);

   tau_DoubleMu4_3_LowMass_SF = data_eff/mc_eff;
   float SF_err = tau_DoubleMu4_3_LowMass_SF * sqrt( (mc_eff_err/mc_eff)*(mc_eff_err/mc_eff) + (data_eff_err/data_eff)*(data_eff_err/data_eff) );
   tau_DoubleMu4_3_LowMass_SF_sysUP   = (tau_DoubleMu4_3_LowMass_SF + SF_err > 0. ? tau_DoubleMu4_3_LowMass_SF + SF_err :  0.);
   tau_DoubleMu4_3_LowMass_SF_sysDOWN = (tau_DoubleMu4_3_LowMass_SF - SF_err > 0. ? tau_DoubleMu4_3_LowMass_SF - SF_err : 0.);
    
   if (debug) std::cout << Form("[HLT-SF] MC efficiency = %.3f +/- %.3f \t DATA efficiency = %.3f +/- %.3f", mc_eff, mc_eff_err, data_eff, data_eff_err) << std::endl;
   if (debug) std::cout << Form("[HLT-SF] tau_DoubleMu4_3_LowMass_SF = %.3f +/- %.3f", tau_DoubleMu4_3_LowMass_SF, SF_err) << std::endl;
   return 0;
}//applyHLT_SF


int WTau3Mu_tools::parsePUweights(const TString & era){

   TFile * file_weights = new TFile(scale_factor_src::PUweight_rootfile);
   if (debug) std::cout << "[+] parse PU weights from \n " << file_weights->GetName() << std::endl; 
   h_PUweights          = (TH1D*)((file_weights->Get(scale_factor_src::centralPUweights_hist[era]+"_nominal"))->Clone());
   h_PUweights->SetDirectory(0);
   h_PUweights_sysUP    = (TH1D*)((file_weights->Get(scale_factor_src::centralPUweights_hist[era]+"_up"))->Clone());
   h_PUweights_sysUP->SetDirectory(0);
   h_PUweights_sysDOWN  = (TH1D*)((file_weights->Get(scale_factor_src::centralPUweights_hist[era]+"_down"))->Clone());
   h_PUweights_sysDOWN->SetDirectory(0);

   file_weights->Close(); 
    
   return 0;
}//parsePUweights

int WTau3Mu_tools::applyPUreweight(){
   
   int bin = h_PUweights->FindBin(Pileup_nTrueInt); 
   if (bin < 0 ) std::cout << "[ERROR] Pileup_nTrueInt outside PU-weights range" << std::endl;
   PU_weight      = (bin > 0 ? h_PUweights->GetBinContent(bin) : 1.0 ); 
   PU_weight_up   = (bin > 0 ? h_PUweights_sysUP->GetBinContent(bin) : 0.0 ); 
   PU_weight_down = (bin > 0 ? h_PUweights_sysDOWN->GetBinContent(bin) : 0.0 ); 

   return 0;
}//applyPUreweight


int WTau3Mu_tools::parseNLOweights(const TString & era, const TString & process){
   TString in_file = scale_factor_src::NLOweight_W_rootfile;
   if (process == "ZTau3Mu") in_file = scale_factor_src::NLOweight_Z_rootfile;
   TFile * file_weights = new TFile(in_file);
   if (file_weights->IsZombie()) {
      std::cerr << "[ERROR] NLO weights file not found" << std::endl;
      return 1;
   }
   std::cout << "[+] parse NLO weights from \n " << file_weights->GetName() << std::endl; 
   h_NLOweights          = (TH2F*)((file_weights->Get(scale_factor_src::NLOweights_hist[era]+"_nominal"))->Clone());
   h_NLOweights->SetDirectory(0);
   h_NLOweights_sysUP    = (TH2F*)((file_weights->Get(scale_factor_src::NLOweights_hist[era]+"_up"))->Clone());
   h_NLOweights_sysUP->SetDirectory(0);
   h_NLOweights_sysDOWN  = (TH2F*)((file_weights->Get(scale_factor_src::NLOweights_hist[era]+"_down"))->Clone());
   h_NLOweights_sysDOWN->SetDirectory(0);

   file_weights->Close(); 
    
   return 0;
}//parseNLOweights

int WTau3Mu_tools::applyNLOreweight(const float& W_pt, const float& W_eta){
   
   int bin = h_NLOweights->FindBin(W_pt, std::abs(W_eta));
   // (pT, eta) outside NLO weight range -> SF = 1.0 +/- 0.0
   if (bin < 0 ) std::cout << "[INFO] GenW_P4.Pt() outside NLO-weights range" << std::endl;
   NLO_weight      = (bin > 0 ? h_NLOweights->GetBinContent(bin) : 1.0 ); 
   NLO_weight_up   = (bin > 0 ? h_NLOweights_sysUP->GetBinContent(bin) : 0.0 ); 
   NLO_weight_down = (bin > 0 ? h_NLOweights_sysDOWN->GetBinContent(bin) : 0.0 ); 

   return 0;
}//applyNLOreweight

int WTau3Mu_tools::parse_pTVweights(){
   TFile * file_weights = new TFile(scale_factor_src::pTVweight_rootfile);
   if (file_weights->IsZombie()) {
      std::cerr << "[ERROR] pTV weights file not found" << std::endl;
      return 1;
   }
   std::cout << "[+] parse pTV weights from \n " << file_weights->GetName() << std::endl;
   h_pTVweights          = (TH1D*)((file_weights->Get(scale_factor_src::pTVweights_hist+"_nominal"))->Clone());
   h_pTVweights->SetDirectory(0);

   file_weights->Close();
   delete file_weights;
   return 0;
}//parse_pTVweights

int WTau3Mu_tools::apply_pTVweights(const float& V_pt){

   int bin = h_pTVweights->FindBin(V_pt);
   if (bin < 0 ) std::cout << "[INFO] GenW_P4.Pt() outside pTV-weights range" << std::endl;
   pTV_weight = (bin > 0 ? h_pTVweights->GetBinContent(bin) : 1.0 );
   return 0;
}//apply_pTVweights

int WTau3Mu_tools::parse_SFfromTHist(const TString inFile, const TString hist_name, TH1* nominal, TH1* sys_up, TH1* sys_down, bool nominal_only){

   TFile* input_file = new TFile(inFile);
   if (input_file->IsZombie()) {
      std::cerr << "[ERROR] file not found" << std::endl;
      return 1;
   }
   std::cout << "[+] parse SF from " << input_file->GetName() << std::endl;
   nominal = (TH1*)((input_file->Get(hist_name+"_nominal"))->Clone());
   nominal->SetDirectory(0);
   if (nominal == nullptr) {
      std::cerr << "[ERROR] nominal histogram not found" << std::endl;
      return 1;
   }
   if (!nominal_only){
      sys_up = (TH1*)((input_file->Get(hist_name+"_up"))->Clone());
      sys_up->SetDirectory(0);
      sys_down = (TH1*)((input_file->Get(hist_name+"_down"))->Clone());
      sys_down->SetDirectory(0);
      if (sys_up == nullptr || sys_down == nullptr) {
         std::cerr << "[ERROR] sys-histograms not found" << std::endl;
         return 1;
      }
   }
   input_file->Close();
   delete input_file;

   return 0;

}//parse_SFfromTHist_1D

float  WTau3Mu_tools::apply_SFfromTHist1D(const double& x, TH1* histo){
   if (histo == nullptr) {
      std::cerr << "[ERROR] SF-histogram not provided" << std::endl;
      return 1;
   }
   int bin = histo->FindBin(x); 
   if (bin < 0) {
      std::cerr << "[ERROR] value outside histogram range for "<< histo->GetName() << std::endl;
      return 1;
   }
   return (bin > 0 ? histo->GetBinContent(bin) : 1.0);
   
}//apply_SFfromTHist

