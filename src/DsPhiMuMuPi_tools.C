#include "../include/DsPhiMuMuPi_tools.h"


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
        is_fired_trigger = (is_fired_1 || is_fired_2) && HLT_Tau3Mu_emulator(idx);
    }
    if(trigger_configuration == HLT_paths::HLT_DoubleMu){
       is_fired_trigger = HLT_DoubleMu4_3_LowMass &&
          (DsPhiPi_mu1_fired_DoubleMu4_3_LowMass[idx] && DsPhiPi_mu2_fired_DoubleMu4_3_LowMass[idx]) && 
          HLT_DoubleMu_emulator(idx);
    }
    if(trigger_configuration == HLT_paths::HLT_overlap) is_fired_trigger = true;
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
