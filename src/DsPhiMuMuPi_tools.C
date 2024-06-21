#include "../include/DsPhiMuMuPi_tools.h"

#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#include <boost/bind/bind.hpp>
#include "boost/property_tree/ptree.hpp"
#include "boost/property_tree/json_parser.hpp"
using namespace boost::placeholders;
namespace pt = boost::property_tree;

bool DsPhiMuMuPi_tools::GenPartFillP4(){
    
   bool debug = false; 
   int Mu1_idx = -1, Mu2_idx = -1, Pi_idx = -1, Phi_idx = -1, Ds_idx;
   std::vector<int> Muons_idxs;
   std::vector<int> Taus_idxs;
   std::vector<float> Muons_pt;
   if (debug) {
      for (UInt_t g = 0; g < nGenPart; g++)std::cout << g << " \t " << GenPart_pdgId[g] << " \t " << GenPart_genPartIdxMother[g] << std::endl;
   }

   bool DsPhiPi_found = false;
   bool PhiMuMu_found = false;

   // look for 2 muons from Phi(1020) 
   for (UInt_t g = 0; g < nGenPart; g++){

      if(abs(GenPart_pdgId[g]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isPhi1020
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[g]]]) == isDs_p
            && !PhiMuMu_found)
      {
         Mu1_idx = g;
         Phi_idx = GenPart_genPartIdxMother[g]; // Phi(1020) idx
         Ds_idx  = GenPart_genPartIdxMother[GenPart_genPartIdxMother[g]]; // Ds+ idx
         if (debug) std::cout << " mu1 found @" << Mu1_idx << std::endl;
         for(UInt_t gg = g+1; gg < nGenPart; gg++){ 
            if(abs(GenPart_pdgId[gg]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[gg]]) == isPhi1020
            && GenPart_genPartIdxMother[gg] == Phi_idx
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[g]]]) == isDs_p
            && !PhiMuMu_found){
               if(Mu1_idx == gg) continue;
               Mu2_idx = gg;
               if (debug) std::cout << " mu2 found @" << Mu2_idx << std::endl;
               PhiMuMu_found = true;
            }
         } // loop for Mu2
      }
      // look for Pi+ 
      if(abs(GenPart_pdgId[g]) == isPion_p
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isDs_p) Pi_idx = g;

   }// loop on gen particles

   //// save Muon and Tau idx
   //Muons_idxs.push_back(mu1); Muons_idxs.push_back(mu2); Muons_idxs.push_back(mu3); 
   //Taus_idxs.push_back(GenPart_genPartIdxMother[mu1]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu2]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu3]);
   //Muons_pt.push_back(GenPart_pt[mu1]); Muons_pt.push_back(GenPart_pt[mu2]); Muons_pt.push_back(GenPart_pt[mu3]);
   // check consistency
   if(Mu1_idx == -1 || Mu2_idx == -1){ 
      std::cout << " [ERROR] gen muons not found : mu1 idx is " << Mu1_idx << " mu2 idx is "<< Mu2_idx  << std::endl;
      exit(-1);
   }else if (Phi_idx == -1){
      std::cout << " [ERROR] gen Phi(1020) not found " << std::endl;
      exit(-1);
   }else if (Pi_idx == -1){
      std::cout << " [ERROR] gen Pi+/- not found " << std::endl;
      exit(-1);
   }else if (Ds_idx == -1){
      std::cout << " [ERROR] gen Ds+/- not found " << std::endl;
      exit(-1);
   }

     
   // if(Muons_idxs.size() < 3){
   //    std::cout << " [ERROR] wrong number of gen-muons it is " << Muons_idxs.size() << std::endl;
   //    exit(-1);
   // }else if(Muons_idxs.size() == 3){
   //    if (debug) std::cout << " [OK] 3 muons found" << std::endl;
   //    // Tau index & Tau's mother idx 
   //    Phi_idx = Taus_idxs[0];
   //    int motherPhi_idx = GenPart_genPartIdxMother[Phi_idx];
   //       // Tau comes from W
   //    if (abs(GenPart_pdgId[motherPhi_idx]) == isW)
   //    {
   //       W_idx = motherPhi_idx;   
   //       // in case of tau radiative decays
   //    }else if( abs(GenPart_pdgId[motherPhi_idx]) == isTau 
   //           && abs(GenPart_pdgId[GenPart_genPartIdxMother[motherPhi_idx]]) == isW)
   //    {
   //       Phi_idx = motherPhi_idx;
   //       W_idx = GenPart_genPartIdxMother[motherPhi_idx]; 
   //    }  
   // }else{
   //    std::cout << " [!!] number of gen-muons from taus is " << Muons_idxs.size() << std::endl;
   //    if(debug){
   //       for (int i=0; i < Taus_idxs.size(); i++) std::cout << Form("tau : %d\t mu: %d", Taus_idxs[i] , Muons_idxs[i])<< std::endl;
   //    }
   //    exit(-1);
   // }
   

   // order muons in leading, sub-leading and trailing
   //std::sort(Muons_idxs.begin(),Muons_idxs.end(), [this](int &a, int &b){ return GenPart_pt[a]>GenPart_pt[b]; });
   if(GenPart_pt[Mu1_idx] < GenPart_pt[Mu2_idx]){
      int tmp = Mu2_idx;
      Mu2_idx = Mu1_idx;
      Mu1_idx = tmp;
   }
   
   GenDs_P4.SetPt(GenPart_pt[Ds_idx]); GenDs_P4.SetEta(GenPart_eta[Ds_idx]); GenDs_P4.SetPhi(GenPart_phi[Ds_idx]); GenDs_P4.SetM(Ds_MASS);
   GenPhi_P4.SetPt(GenPart_pt[Phi_idx]); GenPhi_P4.SetEta(GenPart_eta[Phi_idx]); GenPhi_P4.SetPhi(GenPart_phi[Phi_idx]); GenPhi_P4.SetM(Phi_MASS);
   GenMu1_P4.SetPt(GenPart_pt[Mu1_idx]); GenMu1_P4.SetEta(GenPart_eta[Mu1_idx]); GenMu1_P4.SetPhi(GenPart_phi[Mu1_idx]); GenMu1_P4.SetM(Muon_MASS);
   GenMu2_P4.SetPt(GenPart_pt[Mu2_idx]); GenMu2_P4.SetEta(GenPart_eta[Mu2_idx]); GenMu2_P4.SetPhi(GenPart_phi[Mu2_idx]); GenMu2_P4.SetM(Muon_MASS);
   GenPi_P4.SetPt(GenPart_pt[Pi_idx]); GenPi_P4.SetEta(GenPart_eta[Pi_idx]); GenPi_P4.SetPhi(GenPart_phi[Pi_idx]); GenPi_P4.SetM(Pion_MASS);

   if(debug){
      std::cout << " Ds found @ " << Ds_idx << std::endl;
      std::cout << " Phi found @ " << Phi_idx << std::endl;
      std::cout << " Mu found @ " << Mu1_idx  << " " << Mu2_idx << std::endl;
      std::cout << " Mu pT " << GenPart_pt[Mu1_idx] << " " << GenPart_pt[Mu2_idx] << std::endl;
      std::cout << " Pi found @ " << Pi_idx  << std::endl;
   }
   return true;

} // GenPartFillP4()

bool  DsPhiMuMuPi_tools::RecoPartFillP4(const int idx){

    // require mediumID for all muons
    bool muonsTrksQualityCheck = Muon_isMedium[DsPhiPi_mu1_idx[idx]] && 
                                Muon_isMedium[DsPhiPi_mu2_idx[idx]]; 
    bool pionTrackQualityCheck = true; // add something if needed 

    // muons
    RecoMu1_P4.SetPt(DsPhiPi_mu1_pt[idx]); RecoMu1_P4.SetEta(DsPhiPi_mu1_eta[idx]); RecoMu1_P4.SetPhi(DsPhiPi_mu1_phi[idx]); RecoMu1_P4.SetM(Muon_MASS);
    RecoMu2_P4.SetPt(DsPhiPi_mu2_pt[idx]); RecoMu2_P4.SetEta(DsPhiPi_mu2_eta[idx]); RecoMu2_P4.SetPhi(DsPhiPi_mu2_phi[idx]); RecoMu2_P4.SetM(Muon_MASS);
    // pion
    RecoPi_P4.SetPt(DsPhiPi_trk_pt[idx]); RecoPi_P4.SetEta(DsPhiPi_trk_eta[idx]); RecoPi_P4.SetPhi(DsPhiPi_trk_phi[idx]); RecoPi_P4.SetM(Pion_MASS);
    // Phi(1020) 
    RecoPhi_P4.SetPt(DsPhiPi_MuMu_fitted_pt[idx]);  RecoPhi_P4.SetEta(DsPhiPi_MuMu_fitted_eta[idx]); RecoPhi_P4.SetPhi(DsPhiPi_MuMu_fitted_phi[idx]);  RecoPhi_P4.SetM(DsPhiPi_MuMu_fitted_mass[idx]);
    // Ds
    RecoDs_P4.SetPt(DsPhiPi_fitted_pt[idx]);  RecoDs_P4.SetEta(DsPhiPi_fitted_eta[idx]); RecoDs_P4.SetPhi(DsPhiPi_fitted_phi[idx]);  RecoDs_P4.SetM(DsPhiPi_fitted_mass[idx]);

    return (muonsTrksQualityCheck && pionTrackQualityCheck);
}// RecoPartFillP4

std::vector<unsigned int> DsPhiMuMuPi_tools::sorted_cand_mT(){

   if (debug) std::cout << " #cand " << nDsPhiPi << std::endl;
   // initialize cand-idx vector 
   std::vector<unsigned int> cand_idx(nDsPhiPi, 0);
   iota(cand_idx.begin(), cand_idx.end(), 0);
   // if more than one sort by mT
   if (cand_idx.size() > 1){
   
      if(debug) std::cout << " sort by mT..." << std::endl;
      std::vector<float> mT_v(DsPlusMET_Tau_mT, DsPlusMET_Tau_mT + nDsPhiPi); 
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

int   DsPhiMuMuPi_tools::MCtruthMatching(const bool verbose){
    
    int MCmatch_idx = -1;
    const float DR_threshold = 0.03;
    float DR_Mu1, DR_Mu2, DR_Pi;
    float DRmin_Mu1 = DR_threshold, DRmin_Mu2 = DR_threshold, DRmin_Pi = DR_threshold;
    float Dpt_Mu1, Dpt_Mu2, Dpt_Pi;

    
    for(unsigned int t = 0; t < nDsPhiPi; t++){
        
        RecoPartFillP4(t);         

        // mu 1
        //RecoMu1_P4.SetPt(DsPhiPi_mu1_pt[t]); RecoMu1_P4.SetEta(DsPhiPi_mu1_eta[t]); RecoMu1_P4.SetPhi(DsPhiPi_mu1_phi[t]);
        DR_Mu1 = ROOT::Math::VectorUtil::DeltaR(GenMu1_P4, RecoMu1_P4);
        // mu 2
        RecoMu2_P4.SetPt(DsPhiPi_mu2_pt[t]); RecoMu2_P4.SetEta(DsPhiPi_mu2_eta[t]); RecoMu2_P4.SetPhi(DsPhiPi_mu2_phi[t]);
        //DR_Mu2 = ROOT::Math::VectorUtil::DeltaR(GenMu2_P4, RecoMu2_P4);
        // Pi
        //RecoPi_P4.SetPt(DsPhiPi_mu3_pt[t]); RecoPi_P4.SetEta(DsPhiPi_mu3_eta[t]); RecoPi_P4.SetPhi(DsPhiPi_mu3_phi[t]);
        DR_Pi = ROOT::Math::VectorUtil::DeltaR(GenPi_P4, RecoPi_P4);

        if(verbose){
            std::cout << " - starting Ds cand number " << t << std::endl;
            std::cout << Form(" DR_1 = %.4f \t DR_2 = %.4f \t DR_3 = %.4f", DR_Mu1, DR_Mu2, DR_Pi ) << std::endl;
        }

        if(DR_Mu1 < DRmin_Mu1 && DR_Mu2 < DRmin_Mu2 && DR_Pi < DRmin_Pi ){
            DRmin_Mu1 = DR_Mu1; DRmin_Mu2 = DR_Mu2; DRmin_Pi = DR_Pi;
            Dpt_Mu1 = fabs(GenMu1_P4.Pt() - RecoMu1_P4.Pt())/GenMu1_P4.Pt(); 
            Dpt_Mu2 = fabs(GenMu2_P4.Pt() - RecoMu2_P4.Pt())/GenMu2_P4.Pt();
            Dpt_Pi = fabs(GenPi_P4.Pt() - RecoPi_P4.Pt())/GenPi_P4.Pt();
            MCmatch_idx = t;
        }

    }// loop on tau candidate

    if (verbose){
        std::cout << " MC-matching found w tau cand " << MCmatch_idx << std::endl;
        std::cout << Form(" DRmin_1 = %.4f \t DRmin_2 = %.4f \t DRmin_3 = %.4f", DRmin_Mu1, DRmin_Mu2, DRmin_Pi ) << std::endl;
        std::cout << Form(" Dpt_1 = %.4f \t Dpt_2 = %.4f \t Dpt_3 = %.4f", Dpt_Mu1, Dpt_Mu2, Dpt_Pi ) << std::endl;
    } 
    return MCmatch_idx;

}// MCtruthMatching

bool DsPhiMuMuPi_tools::TriggerMatching(const int idx, const int config){
   //int trigger_configuration = (config == -1 ? HLTconf_ : config);
   int trigger_configuration =config; 
   bool is_fired_trigger = false;
   bool is_fired_Tau3Mu = false, is_fired_DoubleMu = false;
   if(trigger_configuration == HLT_paths::HLT_Tau3Mu){
      // check if the 3 muons + tau fired the trigger
      bool is_fired_1 = HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                           DsPhiPi_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[idx] &&
                           DsPhiPi_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[idx] &&
                           DsPhiPi_trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[idx] &&
                           DsPhiPi_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[idx];
      bool is_fired_2 = HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 &&
                           DsPhiPi_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[idx] &&
                           DsPhiPi_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[idx] &&
                           DsPhiPi_trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[idx]&&
                           DsPhiPi_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[idx];
      is_fired_Tau3Mu = (is_fired_1 || is_fired_2) && HLT_Tau3Mu_emulator(idx);
   }
   if(trigger_configuration == HLT_paths::HLT_DoubleMu){
      is_fired_DoubleMu = HLT_DoubleMu4_3_LowMass &&
         (DsPhiPi_mu1_fired_DoubleMu4_3_LowMass[idx] && DsPhiPi_mu2_fired_DoubleMu4_3_LowMass[idx]) && 
         HLT_DoubleMu_emulator(idx);
   }
   is_fired_trigger = is_fired_Tau3Mu || is_fired_DoubleMu; 
   return is_fired_trigger;
}//TriggerMatching()

bool DsPhiMuMuPi_tools::HLT_Tau3Mu_emulator(const int idx){

   //** single muon
   const float minPT_mu1 = 7.0, minPT_mu2 = 1.0, minPT_mu3 = 1.0;
   const float maxEta_mu = 2.5;
   if(RecoMu1_P4.Pt() < minPT_mu1 || RecoMu2_P4.Pt() < minPT_mu2 || RecoPi_P4.Pt() < minPT_mu3 ) return false;
   if(fabs(RecoMu1_P4.Eta()) > maxEta_mu || fabs(RecoMu2_P4.Eta()) > maxEta_mu || fabs(RecoPi_P4.Eta()) > maxEta_mu ) return false;

   //** di-muon
   const float minM_mumu = 2*Muon_MASS, maxM_mumu = 1.9;
   const float maxDR_muBS = 0.5, maxDZ_mumu = 0.7;
   if(!((DsPhiPi_dZmu12[idx] < maxDZ_mumu && DsPhiPi_mu1_dr[idx] < maxDR_muBS && DsPhiPi_mu2_dr[idx] < maxDR_muBS && (RecoMu1_P4+RecoMu2_P4).M() > minM_mumu && (RecoMu1_P4+RecoMu2_P4).M() < maxM_mumu ) ||  // mu_1, mu_2
      (DsPhiPi_dZmu23[idx] < maxDZ_mumu && DsPhiPi_mu2_dr[idx] < maxDR_muBS && DsPhiPi_trk_dr[idx] < maxDR_muBS && (RecoMu2_P4+RecoPi_P4).M() > minM_mumu && (RecoMu2_P4+RecoPi_P4).M() < maxM_mumu ) ||  // mu_2, mu_3
      (DsPhiPi_dZmu13[idx] < maxDZ_mumu && DsPhiPi_mu1_dr[idx] < maxDR_muBS && DsPhiPi_trk_dr[idx] < maxDR_muBS && (RecoMu1_P4+RecoPi_P4).M() > minM_mumu && (RecoMu1_P4+RecoPi_P4).M() < maxM_mumu) )  // mu_1, mu_3
   ) return false;

   //** muon-Tau
   const float maxDZ_muTau = 0.3, maxDR_muTau = 0.3;
   //if(0) return false; // insert the selection on DZ(tau,mu)
   if( ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoDs_P4) > maxDR_muTau ||
      ROOT::Math::VectorUtil::DeltaR( RecoMu2_P4 ,RecoDs_P4) > maxDR_muTau || 
      ROOT::Math::VectorUtil::DeltaR( RecoPi_P4 ,RecoDs_P4) > maxDR_muTau) return false;

   //** TAU
   const float minPT_tau = 15.0, maxEta_tau = 2.5, minM_tau = 1.3, maxM_tau = 2.1;
   if(RecoDs_P4.Pt() < minPT_tau || RecoDs_P4.M() < minM_tau || RecoDs_P4.M() > maxM_tau || fabs(RecoDs_P4.Eta()) > maxEta_tau) return false;
   const float maxIsoCh_tau = 2.0, maxRelIsoCh_tau = 0.2;
   // --> Iso @ HLT level not comparable with reco isolation offline 
   //if(DsPhiPi_iso_ptChargedFromPV[idx] > maxIsoCh_tau || DsPhiPi_iso_ptChargedFromPV[idx]/RecoTau_P4.Pt() > maxRelIsoCh_tau) return false;
   
   return true;

}//HLT_emulator()


bool DsPhiMuMuPi_tools::HLT_DoubleMu_emulator(const int idx){
  
  if (!(DsPhiPi_mu1_fired_DoubleMu4_3_LowMass[idx] && DsPhiPi_mu2_fired_DoubleMu4_3_LowMass[idx])) return false;
  // single muon - eta
  const float maxEta_mu = 2.5;
  if ( (fabs(RecoMu1_P4.Eta()) > maxEta_mu) || (fabs(RecoMu2_P4.Eta()) > maxEta_mu) ) return false; 

  // single muon
  // * pT
  const float minPT_mu1 = 4.0, minPT_mu2 = 3.0;
  float minPt=-999.;
  float maxPt=-999.;
  minPt = std::min(RecoMu1_P4.Pt(), RecoMu2_P4.Pt());
  maxPt = std::max(RecoMu1_P4.Pt(), RecoMu2_P4.Pt());
  if( maxPt < minPT_mu1 || minPt < minPT_mu2) return false;

  // * compatibility with BS
  const float maxDR_mu = 2.0;
  if(DsPhiPi_mu1_dr[idx]>maxDR_mu || DsPhiPi_mu2_dr[idx]>maxDR_mu ) return false;

  // double muon
  float ptMM=-999.;
  float massMM=-999.;
  const float minPT_mumu = 4.9, minM_mumu = 0.2, maxM_mumu = 8.5;

  ptMM=(RecoMu1_P4+RecoMu2_P4).Pt();
  massMM=(RecoMu1_P4+RecoMu2_P4).M();
  if (!(massMM>minM_mumu && massMM< maxM_mumu && ptMM> minPT_mumu)) return false;

  const float maxDCA_mumu = 0.5;
  const float minVtx_prob = 0.005; // on MuMu vertex fit
  //if (DsPhiPi_mu12_DCA[idx] > maxDCA_mumu || DsPhiPi_mu12_vtxFitProb[idx] < minVtx_prob) return false;

  return true;

}//HLT_DoubleMu_emulator()

bool DsPhiMuMuPi_tools::HLT_DoubleMu_reinforcement(const int idx){

   const float minPT_mu1 = 7.0, minPT_mu3 = 1.0;
   if(RecoMu1_P4.Pt() < minPT_mu1 || RecoPi_P4.Pt() < minPT_mu3 ) return false;
   const float minPT_tau = 15.0;
   if(RecoDs_P4.Pt() < minPT_tau) return false;
   const float maxM_mumu  = 1.9;
   const float maxDZ_mumu = 0.7;
   if(!( DsPhiPi_dZmu12[idx] < maxDZ_mumu && (RecoMu1_P4+RecoMu2_P4).M() < maxM_mumu )) return false;

   return true;

}//HLT_DoubleMu_reinforcement()

bool DsPhiMuMuPi_tools::applyMETfilters(const int& TauIdx){
   
   bool passed_filter = DsPlusMET_Flag_BadPFMuonDzFilter[TauIdx] &&
                        DsPlusMET_Flag_BadPFMuonFilter[TauIdx] &&
                        DsPlusMET_Flag_EcalDeadCellTriggerPrimitiveFilter[TauIdx] &&
                        DsPlusMET_Flag_eeBadScFilter[TauIdx] &&
                        DsPlusMET_Flag_globalSuperTightHalo2016Filter[TauIdx] &&
                        DsPlusMET_Flag_goodVertices[TauIdx] &&
                        DsPlusMET_Flag_hfNoisyHitsFilter[TauIdx];

   return passed_filter;

}//applyMETfilters()

int DsPhiMuMuPi_tools::parseMuonSF(const TString & era, const TString & pTrange){
   
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

int DsPhiMuMuPi_tools::applyMuonSF(const int& idx){
   
   float cand_SF = 1.0;
   int bin = -5;
   // mu1
   bin = h_muonSF_lowpT->FindBin(fabs(DsPhiPi_mu1_eta[idx]), DsPhiPi_mu1_pt[idx]);
   Ds_mu1_IDrecoSF           = (bin > 0 ? h_muonSF_lowpT->GetBinContent(bin) : 1.0);
   Ds_mu1_IDrecoSF_sysUP     = (bin > 0 ? h_muonSF_lowpT_sysUP->GetBinContent(bin) : 1.0);
   Ds_mu1_IDrecoSF_sysDOWN   = (bin > 0 ? h_muonSF_lowpT_sysDOWN->GetBinContent(bin) : 1.0);
   if(debug) std::cout << Form("> mu1 (pT, eta) = (%.2f,%.2f ) \t SF = %.3f", DsPhiPi_mu1_pt[idx], DsPhiPi_mu1_eta[idx], Ds_mu1_IDrecoSF ) << std::endl;
   // mu2
   bin = h_muonSF_lowpT->FindBin(fabs(DsPhiPi_mu2_eta[idx]), DsPhiPi_mu2_pt[idx]);
   Ds_mu2_IDrecoSF           = (bin > 0 ? h_muonSF_lowpT->GetBinContent(bin) : 1.0);
   Ds_mu2_IDrecoSF_sysUP     = (bin > 0 ? h_muonSF_lowpT_sysUP->GetBinContent(bin) : 1.0);
   Ds_mu2_IDrecoSF_sysDOWN   = (bin > 0 ? h_muonSF_lowpT_sysDOWN->GetBinContent(bin) : 1.0);
   if(debug) std::cout << Form("> mu2 (pT, eta) = (%.2f,%.2f ) \t SF = %.3f", DsPhiPi_mu2_pt[idx], DsPhiPi_mu2_eta[idx], Ds_mu2_IDrecoSF ) << std::endl;


   return 0;
}//applyMuonSF