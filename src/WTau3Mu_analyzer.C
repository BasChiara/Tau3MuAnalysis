#include "../include/WTau3Mu_analyzer.h"


void WTau3Mu_analyzer::Loop(){ 

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   unsigned int Nevents = 0;
   const Long64_t Nbreak = nentries + 10; 
   const Long64_t Nprint = (int)(nentries/20.);

   unsigned int nEvTau3Mu =0, nTriggerBit = 0, nEvTriggerFired_Tau3Mu = 0, nEvTriggerFired_DoubleMu = 0, nEvTriggerFired_Total = 0, nEvReinforcedHLT = 0, nEvDiMuResVeto = 0;
   unsigned int nTauFired3Mu = 0, nTauReinforcedHLT = 0, nTauDiMuonVeto = 0, nTauMCmatched = 0;
   bool flag_HLT_Tau3mu = false, flag_HLT_DoubleMu = false, flag_reinfHLT = true, flag_diMuResVeto =true;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {

      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0 || jentry == Nbreak) break;
      if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      Nevents++;

      // analyze only W Tau -> 3 Mui passing MET filters
      if(nTauTo3Mu == 0) continue;
      if(!applyMETfilters(0)) continue;
      if(debug && nTauTo3Mu > 1) std::cout << "++ new event with multiple cands" << std::endl;
      nEvTau3Mu++;

      // --- HL TRIGGER BIT
      if((HLTconf_ == HLT_paths::HLT_Tau3Mu) &&
            !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15)) continue;
      if((HLTconf_ == HLT_paths::HLT_DoubleMu) &&
            !HLT_DoubleMu4_3_LowMass) continue;
      if((HLTconf_ == HLT_paths::HLT_overlap) &&
            !(HLT_DoubleMu4_3_LowMass|| HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15)) continue;
      nTriggerBit++;

      LumiBlock = luminosityBlock;
      Run = run;
      Event = event;
      nGoodPV = PV_npvsGood;

      if(isMC_){
         // --- MC truth & matching
         GenPartFillP4();
         TauTo3Mu_MCmatch_idx = MCtruthMatching();
 
         tau_mu1_gen_pt  = GenMu1_P4.Pt();  tau_mu2_gen_pt  = GenMu2_P4.Pt();  tau_mu3_gen_pt  = GenMu3_P4.Pt();
         tau_mu1_gen_eta = GenMu1_P4.Eta(); tau_mu2_gen_eta = GenMu2_P4.Eta(); tau_mu3_gen_eta = GenMu3_P4.Eta();
         tau_gen_mass = GenTau_P4.M(); tau_gen_pt = GenTau_P4.Pt(); tau_gen_eta = GenTau_P4.Eta(); tau_gen_phi = GenTau_P4.Phi();    
         W_gen_pt = GenW_P4.Pt(); W_gen_eta = GenW_P4.Eta(); W_gen_phi = GenW_P4.Phi();
         Nu_gen_pt = GenNu_P4.Pt(); Nu_gen_eta = GenNu_P4.Eta(); Nu_gen_phi = GenNu_P4.Phi();
         gen_met_pt = GenMET_pt; gen_met_phi = GenMET_phi;
      }
      // --- loop on TAU candidates
      flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false;
      flag_reinfHLT = true; flag_diMuResVeto = true;
      tau_mu12_M = -1.0; tau_mu23_M = -1.0; tau_mu13_M = -1.0;
      // sort candidates by transverse mass
      std::vector<unsigned int> tau_idxs = sorted_cand_mT(); 
      //for(unsigned int t = 0; t < nTauTo3Mu; t++){
      for(unsigned int t: tau_idxs){ 

         if(debug && nTauTo3Mu > 1) std::cout << " + tau cand with mT " << TauPlusMET_Tau_Puppi_mT[t] << std::endl; 
         // check muons MediumID
         if(!RecoPartFillP4(t)) continue;

         // trigger matching
         //if(!TriggerMatching(t, HLTconf_)) continue;
         flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false; 
         if(HLTconf_ == HLT_paths::HLT_Tau3Mu)   flag_HLT_Tau3mu = TriggerMatching(t, HLTconf_);
         if(HLTconf_ == HLT_paths::HLT_DoubleMu) flag_HLT_DoubleMu = TriggerMatching(t, HLTconf_);
         if(HLTconf_ == HLT_paths::HLT_overlap){
            flag_HLT_Tau3mu   = TriggerMatching(t,HLT_paths::HLT_Tau3Mu);
            flag_HLT_DoubleMu = TriggerMatching(t,HLT_paths::HLT_DoubleMu);
         }
         if(!(flag_HLT_Tau3mu || flag_HLT_DoubleMu)) continue;
         nTauFired3Mu++;
         HLT_isfired_DoubleMu = (int)flag_HLT_DoubleMu; HLT_isfired_Tau3Mu = (int)flag_HLT_Tau3mu; 

         n_tau = nTauTo3Mu;

         // blind tau mass if needed
         if(isBlind_ && RecoTau_P4.M() > blindTauMass_low && RecoTau_P4.M() < blindTauMass_high ) continue;

         // veto diMuonResonances
         if (TauTo3Mu_diMuVtxFit_toVeto[t]) continue;
         if (flag_diMuResVeto) nEvDiMuResVeto++;
         flag_diMuResVeto = false;
         nTauDiMuonVeto++;
         tau_dimuon_mass = ( TauTo3Mu_diMuVtxFit_bestProb[t] > 0 ? TauTo3Mu_diMuVtxFit_bestMass[t] : -1 );

         // HLT_DoubleMuon reinforcement
         //if (HLTconf_ == HLT_paths::HLT_DoubleMu && !HLT_DoubleMu_reinforcement(t)) continue;
         if (flag_HLT_DoubleMu && !HLT_DoubleMu_reinforcement(t)) continue;
         if (flag_reinfHLT) nEvReinforcedHLT++;
         nTauReinforcedHLT++; 

         // muonsID
         tau_mu1_MediumID   = Muon_isMedium[TauTo3Mu_mu1_idx[t]];   tau_mu2_MediumID   = Muon_isMedium[TauTo3Mu_mu2_idx[t]];   tau_mu3_MediumID   = Muon_isMedium[TauTo3Mu_mu2_idx[t]];
         tau_mu1_LooseID    = Muon_isLoose[TauTo3Mu_mu1_idx[t]];    tau_mu2_LooseID    = Muon_isLoose[TauTo3Mu_mu2_idx[t]];    tau_mu3_LooseID    = Muon_isLoose[TauTo3Mu_mu2_idx[t]];
         tau_mu1_SoftID_PV  = Muon_isSoft[TauTo3Mu_mu1_idx[t]];     tau_mu2_SoftID_PV  = Muon_isSoft[TauTo3Mu_mu2_idx[t]];     tau_mu3_SoftID_PV  = Muon_isSoft[TauTo3Mu_mu3_idx[t]];
         tau_mu1_SoftID_BS  = Muon_isSoft_BS[TauTo3Mu_mu1_idx[t]];  tau_mu2_SoftID_BS  = Muon_isSoft_BS[TauTo3Mu_mu2_idx[t]];  tau_mu3_SoftID_BS  = Muon_isSoft_BS[TauTo3Mu_mu3_idx[t]];
         tau_mu1_TightID_PV = Muon_isTight[TauTo3Mu_mu1_idx[t]];    tau_mu2_TightID_PV = Muon_isTight[TauTo3Mu_mu2_idx[t]];    tau_mu3_TightID_PV = Muon_isTight[TauTo3Mu_mu3_idx[t]];
         tau_mu1_TightID_BS = Muon_isTight_BS[TauTo3Mu_mu1_idx[t]]; tau_mu2_TightID_BS = Muon_isTight_BS[TauTo3Mu_mu2_idx[t]]; tau_mu3_TightID_BS = Muon_isTight_BS[TauTo3Mu_mu3_idx[t]];
         // muons SF in MC
         tau_mu1_IDrecoSF=1.; tau_mu2_IDrecoSF=1.; tau_mu3_IDrecoSF=1.;
         tau_mu1_IDrecoSF_sysUP = -1.; tau_mu1_IDrecoSF_sysDOWN = -1.;  
         tau_mu2_IDrecoSF_sysUP = -1.; tau_mu2_IDrecoSF_sysDOWN = -1.;  
         tau_mu3_IDrecoSF_sysUP = -1.; tau_mu3_IDrecoSF_sysDOWN = -1.;  
         if(isMC_){
            applyMuonSF(t);
         }
         weight = lumi_factor * tau_mu1_IDrecoSF * tau_mu2_IDrecoSF * tau_mu3_IDrecoSF; 

         // muons kinematics
         tau_mu1_pt  = TauTo3Mu_mu1_pt[t];   tau_mu2_pt  = TauTo3Mu_mu2_pt[t];   tau_mu3_pt  = TauTo3Mu_mu3_pt[t];
         tau_mu1_eta = TauTo3Mu_mu1_eta[t];  tau_mu2_eta = TauTo3Mu_mu2_eta[t];  tau_mu3_eta = TauTo3Mu_mu3_eta[t];
         tau_mu1_z   = Muon_z[TauTo3Mu_mu1_idx[t]]; tau_mu2_z   = Muon_z[TauTo3Mu_mu2_idx[t]]; tau_mu3_z   = Muon_z[TauTo3Mu_mu3_idx[t]];
         tau_mu12_dZ = TauTo3Mu_dZmu12[t];   tau_mu23_dZ = TauTo3Mu_dZmu23[t];   tau_mu13_dZ = TauTo3Mu_dZmu13[t];
         if ( Muon_charge[TauTo3Mu_mu1_idx[t]]*Muon_charge[TauTo3Mu_mu2_idx[t]] < 0. ) tau_mu12_M = (RecoMu1_P4+RecoMu2_P4).M();
         tau_mu12_fitM = TauTo3Mu_mu12_fit_mass[t];
         if ( Muon_charge[TauTo3Mu_mu2_idx[t]]*Muon_charge[TauTo3Mu_mu3_idx[t]] < 0. ) tau_mu23_M = (RecoMu2_P4+RecoMu3_P4).M();
         tau_mu23_fitM = TauTo3Mu_mu23_fit_mass[t];
         if ( Muon_charge[TauTo3Mu_mu1_idx[t]]*Muon_charge[TauTo3Mu_mu3_idx[t]] < 0. ) tau_mu13_M = (RecoMu1_P4+RecoMu3_P4).M();
         tau_mu13_fitM = TauTo3Mu_mu13_fit_mass[t];

         // Tau -> 3mu
         tau_fit_charge = TauTo3Mu_charge[t]; 
         tau_raw_mass = (RecoMu1_P4+RecoMu2_P4+RecoMu3_P4).M(); 
         tau_fit_mass = TauTo3Mu_fitted_mass[t];
         tau_fit_mass_err =  sqrt(TauTo3Mu_fitted_mass_err2[t]);
         tau_fit_mass_resol =  sqrt(TauTo3Mu_fitted_mass_err2[t])/TauTo3Mu_fitted_mass[t];
         tau_fit_pt = TauTo3Mu_fitted_pt[t]; 
         tau_fit_eta = TauTo3Mu_fitted_eta[t], tau_fit_phi = TauTo3Mu_fitted_phi[t];
         tau_relIso = TauTo3Mu_absIsolation[t]/TauTo3Mu_fitted_pt[t];
         tau_Iso_chargedDR04 = TauTo3Mu_iso_ptChargedFromPV[t];
         tau_Iso_photonDR04 = TauTo3Mu_iso_ptPhotons[t]; 
         tau_Iso_puDR08 = TauTo3Mu_iso_ptChargedFromPU[t]; 
         tau_relIso_pT05 = TauTo3Mu_absIsolation_pT05[t]/TauTo3Mu_fitted_pt[t];
         tau_Iso_chargedDR04_pT05 = TauTo3Mu_iso_ptChargedFromPV_pT05[t]; 
         tau_Iso_photonDR04_pT05 = TauTo3Mu_iso_ptPhotons_pT05[t]; 
         tau_Iso_puDR08_pT05 = TauTo3Mu_iso_ptChargedFromPU_pT05[t];
         tau_Lxy_val_BS = TauTo3Mu_Lxy_3muVtxBS[t];
         tau_Lxy_err_BS = TauTo3Mu_errLxy_3muVtxBS[t];
         tau_Lxy_sign_BS = TauTo3Mu_sigLxy_3muVtxBS[t];
         tau_fit_mt = TauPlusMET_Tau_Puppi_mT[t];
         tau_fit_vprob = TauTo3Mu_vtx_prob[t];
         tau_cosAlpha_BS = TauTo3Mu_CosAlpha2D_LxyP3mu[t];
         // tau + MET (Puppi)
         float Dphi_MET = fabs(RecoTau_P4.Phi()- DeepMETResolutionTune_phi);
         if (Dphi_MET > 2*M_PI) Dphi_MET = 2*M_PI - Dphi_MET;
         Dphi_MET = fabs(RecoTau_P4.Phi()- PuppiMET_phi);
         if (Dphi_MET > 2*M_PI){
            std::cout << " Dphi PuppiMET " << Dphi_MET << std::endl;
            float full_angle = 2*M_PI;
            Dphi_MET = Dphi_MET - full_angle;
            std::cout << " Dphi PuppiMET corrected " << Dphi_MET << std::endl;
         }

         //---
         tau_met_pt = PuppiMET_pt; tau_met_phi = PuppiMET_phi;
         tau_rawMet_pt = RawPuppiMET_pt; tau_rawMet_phi = RawPuppiMET_phi;
         tau_DeepMet_pt = TauPlusMET_DeepMET_pt[t]; tau_DeepMet_phi = 0;//TauPlusMET_DeepMET_phi[t];
         tau_met_ratio_pt = RecoTau_P4.Pt()/PuppiMET_pt;
         tau_met_Dphi = Dphi_MET;            
         miss_pz_min = TauPlusMET_PuppiMETminPz[t], miss_pz_max = TauPlusMET_PuppiMETmaxPz[t];

         // W
         W_pt = TauPlusMET_Puppi_pt[t]; W_phi = TauPlusMET_Puppi_phi[t]; 
         W_eta_min =  TauPlusMET_Puppi_eta_min[t];  W_eta_max =  TauPlusMET_Puppi_eta_max[t]; 
         W_mass_min = TauPlusMET_Puppi_mass_min[t]; W_mass_max = TauPlusMET_Puppi_mass_max[t]; 
         W_Deep_pt = TauPlusMET_Deep_pt[t]; W_Deep_phi = TauPlusMET_Deep_phi[t]; 
         W_Deep_eta_min =  TauPlusMET_Deep_eta_min[t];  W_Deep_eta_max =  TauPlusMET_Deep_eta_max[t]; 

         // Ds-> phi(mumu) pi fake 
         fakeDs_mass(t);
         // MC maching
         if(process_ == "Tau3Mu"){
           isMCmatching = (t == TauTo3Mu_MCmatch_idx);
           if(isMCmatching) nTauMCmatched++;
         }

         outTree_->Fill();
         break;
      }// loop on tau cands

      // HLT summary
      if(flag_HLT_Tau3mu) nEvTriggerFired_Tau3Mu++;
      if(flag_HLT_DoubleMu) nEvTriggerFired_DoubleMu++;
      if(flag_HLT_DoubleMu || flag_HLT_Tau3mu) nEvTriggerFired_Total++;

   }// loop on events

   saveOutput();
   std::cout << " == summary == " << std::endl;
   std::cout << " Events processed " << Nevents << std::endl;
   std::cout << " Events whith Tau3Mu candidates " << nEvTau3Mu << std::endl;
   std::cout << " Events whith HLT-bit ON " << nTriggerBit << std::endl;
   std::cout << " Events which fully fired HLT_Tau3Mu " << nEvTriggerFired_Tau3Mu << std::endl;
   std::cout << " Events which fully fired HLT_DoubleMu " << nEvTriggerFired_DoubleMu << std::endl;
   std::cout << " Events which fully fired TOTAL " << nEvTriggerFired_Total << std::endl;
   std::cout << " Events after di-muon resonance veto " << nEvDiMuResVeto << std::endl;
   std::cout << " Events after HLT_DoubleMu reinforcement " << nEvReinforcedHLT << std::endl;
   std::cout << " Tau candidates with 3 fired muons " << nTauFired3Mu << std::endl;
   std::cout << " Tau candidates after diMu veto " << nTauDiMuonVeto << std::endl;
   std::cout << " Tau candidates after HLT_DoubleMu reinforcement " << nTauReinforcedHLT << std::endl;
   if(isMC_){
      std::cout << " Tau candidates MC-matching " << nTauMCmatched << std::endl;
   }


}//Loop()

void WTau3Mu_analyzer::fakeDs_mass(const int& cand_idx){
   ROOT::Math::PtEtaPhiMVector RecoFake_cand;
   ROOT::Math::PtEtaPhiMVector RecoFake_pi, RecoFake_phi;

   // get the di-muonpair closest to phi(1020) mass
   std::vector<double> dimuon_mass = {fabs(TauTo3Mu_mu12_fit_mass[cand_idx] - Phi_MASS),
                                       fabs(TauTo3Mu_mu23_fit_mass[cand_idx] - Phi_MASS),
                                       fabs(TauTo3Mu_mu13_fit_mass[cand_idx] - Phi_MASS)};
   auto phiMuMu_pair_iter = std::min_element(dimuon_mass.begin(), dimuon_mass.end());
   int phiMuMu_pair = std::distance(dimuon_mass.begin(), phiMuMu_pair_iter);
   if ( phiMuMu_pair == 0 ){
      RecoFake_phi = RecoMu1_P4 + RecoMu2_P4;
      RecoFake_pi = RecoMu3_P4;
      tau_phiMuMu_mass = TauTo3Mu_mu12_fit_mass[cand_idx]; 
   }else if (phiMuMu_pair == 1){
      RecoFake_phi = RecoMu2_P4 + RecoMu3_P4;
      RecoFake_pi = RecoMu1_P4; 
      tau_phiMuMu_mass = TauTo3Mu_mu23_fit_mass[cand_idx]; 
   }else if (phiMuMu_pair == 2){
      RecoFake_phi = RecoMu1_P4 + RecoMu3_P4;
      RecoFake_pi = RecoMu2_P4;  
      tau_phiMuMu_mass = TauTo3Mu_mu13_fit_mass[cand_idx]; 
   }
   RecoFake_pi.SetM(Pion_MASS);
   RecoFake_cand = RecoFake_phi + RecoFake_pi; 

   tau_MuMuPi_mass = RecoFake_cand.M(); 
   
}//fakeDs_mass()

void WTau3Mu_analyzer::saveOutput(){

   outFile_ = new TFile(outFilePath_, "RECREATE");
   outFile_->cd();

   outTree_->Write();
   if(isMC_){
      h_muonSF_lowpT->Write();
      h_muonSF_lowpT_sysUP->Write();
      h_muonSF_lowpT_sysDOWN->Write();
      //make h_muonSF_medpT->Write();
   }
   outFile_->Close();
   std::cout << " [OUTPUT] root file saved in " << outFilePath_ << std::endl;


}//saveOutput()

void WTau3Mu_analyzer::outTreeSetUp(){
    
   outTree_ = new TTree(outTree_name_, "Tau3Mu candidates with HLT implemented");
   std::cout << " out tree setting up ... " << std::endl;

   outTree_->Branch("run", &Run, "run/i");
   outTree_->Branch("LumiBlock", &LumiBlock, "LumiBlock/i");
   outTree_->Branch("event", &Event, "Event/l");
   //outTree_->Branch("year", &year_num, "year/i");
   outTree_->Branch("year_id", &year_id_, "year_id/i"); 
   outTree_->Branch("nGoodPV", &nGoodPV, "nGoodPV/i");
   // lumi & scale factors
   outTree_->Branch("weight",                   &weight,                   "weight/F");
   outTree_->Branch("lumi_factor",              &lumi_factor,              "lumi_factor/F");
   outTree_->Branch("tau_mu1_IDrecoSF",         &tau_mu1_IDrecoSF,         "tau_mu1_IDrecoSF/F");
   outTree_->Branch("tau_mu1_IDrecoSF_sysUP",   &tau_mu1_IDrecoSF_sysUP,   "tau_mu1_IDrecoSF_sysUP/F");
   outTree_->Branch("tau_mu1_IDrecoSF_sysDOWN", &tau_mu1_IDrecoSF_sysDOWN, "tau_mu1_IDrecoSF_sysDOWN/F");
   outTree_->Branch("tau_mu2_IDrecoSF",         &tau_mu2_IDrecoSF,         "tau_mu2_IDrecoSF/F");
   outTree_->Branch("tau_mu2_IDrecoSF_sysUP",   &tau_mu2_IDrecoSF_sysUP,   "tau_mu2_IDrecoSF_sysUP/F");
   outTree_->Branch("tau_mu2_IDrecoSF_sysDOWN", &tau_mu2_IDrecoSF_sysDOWN, "tau_mu2_IDrecoSF_sysDOWN/F");
   outTree_->Branch("tau_mu3_IDrecoSF",         &tau_mu3_IDrecoSF,         "tau_mu3_IDrecoSF/F");
   outTree_->Branch("tau_mu3_IDrecoSF_sysUP",   &tau_mu3_IDrecoSF_sysUP,   "tau_mu3_IDrecoSF_sysUP/F");
   outTree_->Branch("tau_mu3_IDrecoSF_sysDOWN", &tau_mu3_IDrecoSF_sysDOWN, "tau_mu3_IDrecoSF_sysDOWN/F");
   outTree_->Branch("isMCmatching",             &isMCmatching,             "isMCmatching/I");
   // * HLT
   outTree_->Branch("HLT_isfired_Tau3Mu",     &HLT_isfired_Tau3Mu,   "HLT_isfired_Tau3Mu/I");
   outTree_->Branch("HLT_isfired_DoubleMu",   &HLT_isfired_DoubleMu, "HLT_isfired_DoubleMu/I");
   // * muons
   // ** IDs
   outTree_->Branch("tau_mu1_MediumID",     &tau_mu1_MediumID,   "tau_mu1_MediumID/I");
   outTree_->Branch("tau_mu2_MediumID",     &tau_mu2_MediumID,   "tau_mu2_MediumID/I");
   outTree_->Branch("tau_mu3_MediumID",     &tau_mu3_MediumID,   "tau_mu3_MediumID/I");
   outTree_->Branch("tau_mu1_LooseID",      &tau_mu1_LooseID,    "tau_mu1_LooseID/I");
   outTree_->Branch("tau_mu2_LooseID",      &tau_mu2_LooseID,    "tau_mu2_LooseID/I");
   outTree_->Branch("tau_mu3_LooseID",      &tau_mu3_LooseID,    "tau_mu3_LooseID/I");
   outTree_->Branch("tau_mu1_SoftID_PV",    &tau_mu1_SoftID_PV,  "tau_mu1_SoftID_PV/I");
   outTree_->Branch("tau_mu2_SoftID_PV",    &tau_mu2_SoftID_PV,  "tau_mu2_SoftID_PV/I");
   outTree_->Branch("tau_mu3_SoftID_PV",    &tau_mu3_SoftID_PV,  "tau_mu3_SoftID_PV/I");
   outTree_->Branch("tau_mu1_SoftID_BS",    &tau_mu1_SoftID_BS,  "tau_mu1_SoftID_BS/I");
   outTree_->Branch("tau_mu2_SoftID_BS",    &tau_mu2_SoftID_BS,  "tau_mu2_SoftID_BS/I");
   outTree_->Branch("tau_mu3_SoftID_BS",    &tau_mu3_SoftID_BS,  "tau_mu3_SoftID_BS/I");
   outTree_->Branch("tau_mu1_TightID_PV",   &tau_mu1_TightID_PV, "tau_mu1_TightID_PV/I");
   outTree_->Branch("tau_mu2_TightID_PV",   &tau_mu2_TightID_PV, "tau_mu2_TightID_PV/I");
   outTree_->Branch("tau_mu3_TightID_PV",   &tau_mu3_TightID_PV, "tau_mu3_TightID_PV/I");
   outTree_->Branch("tau_mu1_TightID_BS",   &tau_mu1_TightID_BS, "tau_mu1_TightID_BS/I");
   outTree_->Branch("tau_mu2_TightID_BS",   &tau_mu2_TightID_BS, "tau_mu2_TightID_BS/I");
   outTree_->Branch("tau_mu3_TightID_BS",   &tau_mu3_TightID_BS, "tau_mu3_TightID_BS/I");
   // ** kinematics
   outTree_->Branch("tau_mu1_gen_pt",      &tau_mu1_gen_pt,   "tau_mu1_gen_pt/F");
   outTree_->Branch("tau_mu2_gen_pt",      &tau_mu2_gen_pt,   "tau_mu2_gen_pt/F");
   outTree_->Branch("tau_mu3_gen_pt",      &tau_mu3_gen_pt,   "tau_mu3_gen_pt/F");
   outTree_->Branch("tau_mu1_gen_eta",     &tau_mu1_gen_eta,  "tau_mu1_gen_eta/F");
   outTree_->Branch("tau_mu2_gen_eta",     &tau_mu2_gen_eta,  "tau_mu2_gen_eta/F");
   outTree_->Branch("tau_mu3_gen_eta",     &tau_mu3_gen_eta,  "tau_mu3_gen_eta/F");
   outTree_->Branch("tau_mu1_pt",      &tau_mu1_pt,   "tau_mu1_pt/F");
   outTree_->Branch("tau_mu2_pt",      &tau_mu2_pt,   "tau_mu2_pt/F");
   outTree_->Branch("tau_mu3_pt",      &tau_mu3_pt,   "tau_mu3_pt/F");
   outTree_->Branch("tau_mu1_eta",     &tau_mu1_eta,  "tau_mu1_eta/F");
   outTree_->Branch("tau_mu2_eta",     &tau_mu2_eta,  "tau_mu2_eta/F");
   outTree_->Branch("tau_mu3_eta",     &tau_mu3_eta,  "tau_mu3_eta/F");
   outTree_->Branch("tau_mu1_z",       &tau_mu1_z,    "tau_mu1_z/F");
   outTree_->Branch("tau_mu2_z",       &tau_mu2_z,    "tau_mu2_z/F");
   outTree_->Branch("tau_mu3_z",       &tau_mu3_z,    "tau_mu3_z/F");
   outTree_->Branch("tau_mu12_dZ",     &tau_mu12_dZ,  "tau_mu12_dZ/F");
   outTree_->Branch("tau_mu13_dZ",     &tau_mu13_dZ,  "tau_mu13_dZ/F");
   outTree_->Branch("tau_mu23_dZ",     &tau_mu23_dZ,  "tau_mu23_dZ/F");
   outTree_->Branch("tau_mu12_M",      &tau_mu12_M,   "tau_mu12_M/F");
   outTree_->Branch("tau_mu12_fitM",      &tau_mu12_fitM,   "tau_mu12_fitM/F");
   outTree_->Branch("tau_mu13_M",      &tau_mu13_M,   "tau_mu13_M/F");
   outTree_->Branch("tau_mu13_fitM",      &tau_mu13_fitM,   "tau_mu13_fitM/F");
   outTree_->Branch("tau_mu23_M",      &tau_mu23_M,   "tau_mu23_M/F");
   outTree_->Branch("tau_mu23_fitM",      &tau_mu23_fitM,   "tau_mu23_fitM/F");
   // * tau canditates
   outTree_->Branch("n_tau",            &n_tau,            "n_tau/I");
   outTree_->Branch("tau_gen_mass",     &tau_gen_mass,     "tau_gen_mass/F");
   outTree_->Branch("tau_gen_pt",       &tau_gen_pt,      "tau_gen_pt/F");
   outTree_->Branch("tau_gen_eta",      &tau_gen_eta,     "tau_gen_eta/F");
   outTree_->Branch("tau_gen_phi",      &tau_gen_phi,     "tau_gen_phi/F");
   outTree_->Branch("tau_raw_mass",     &tau_raw_mass,     "tau_raw_mass/F");
   outTree_->Branch("tau_fit_mass",     &tau_fit_mass,     "tau_fit_mass/F");
   outTree_->Branch("tau_fit_mass_err", &tau_fit_mass_err,"tau_fit_mass_err/F");
   outTree_->Branch("tau_fit_mass_resol", &tau_fit_mass_resol,"tau_fit_mass_resol/F");
   outTree_->Branch("tau_fit_charge",   &tau_fit_charge,   "tau_fit_charge/F");
   outTree_->Branch("tau_fit_pt",       &tau_fit_pt,      "tau_fit_pt/F");
   outTree_->Branch("tau_fit_eta",      &tau_fit_eta,     "tau_fit_eta/F");
   outTree_->Branch("tau_fit_phi",      &tau_fit_phi,     "tau_fit_phi/F");
   outTree_->Branch("tau_relIso",       &tau_relIso,      "tau_relIso/F");
   outTree_->Branch("tau_Iso_chargedDR04",       &tau_Iso_chargedDR04,      "tau_Iso_chargedDR04/F");
   outTree_->Branch("tau_Iso_photonDR04",       &tau_Iso_photonDR04,      "tau_Iso_photonDR04/F");
   outTree_->Branch("tau_Iso_puDR08",       &tau_Iso_puDR08,      "tau_Iso_puDR08/F");
   outTree_->Branch("tau_relIso_pT05",  &tau_relIso_pT05, "tau_relIso_pT05/F");
   outTree_->Branch("tau_Iso_chargedDR04_pT05",  &tau_Iso_chargedDR04_pT05, "tau_Iso_chargedDR04_pT05/F");
   outTree_->Branch("tau_Iso_photonDR04_pT05",  &tau_Iso_photonDR04_pT05, "tau_Iso_photonDR04_pT05/F");
   outTree_->Branch("tau_Iso_puDR08_pT05",  &tau_Iso_puDR08_pT05, "tau_Iso_puDR08_pT05/F");
   outTree_->Branch("tau_dimuon_mass",  &tau_dimuon_mass, "tau_dimuon_mass/F");
   outTree_->Branch("tau_Lxy_sign_BS",  &tau_Lxy_sign_BS, "tau_Lxy_sign_BS/F");
   outTree_->Branch("tau_Lxy_err_BS",   &tau_Lxy_err_BS, "tau_Lxy_err_BS/F");
   outTree_->Branch("tau_Lxy_val_BS",   &tau_Lxy_val_BS, "tau_Lxy_val_BS/F");
   outTree_->Branch("tau_fit_mt",       &tau_fit_mt,      "tau_fit_mt/F");
   outTree_->Branch("tau_fit_vprob",    &tau_fit_vprob,   "tau_fit_vprob/F");
   outTree_->Branch("tau_cosAlpha_BS",  &tau_cosAlpha_BS, "tau_cosAlpha_BS/F");
   // * tau + MET
   outTree_->Branch("gen_met_pt",       &gen_met_pt,       "gen_met_pt/F");
   outTree_->Branch("gen_met_phi",      &gen_met_phi,      "gen_met_phi/F");
   outTree_->Branch("Nu_gen_pt",        &Nu_gen_pt,        "Nu_gen_pt/F");
   outTree_->Branch("Nu_gen_eta",       &Nu_gen_eta,       "Nu_gen_eta/F");
   outTree_->Branch("Nu_gen_phi",       &Nu_gen_phi,       "Nu_gen_phi/F");
   outTree_->Branch("W_gen_pt",         &W_gen_pt,         "W_gen_pt/F");
   outTree_->Branch("W_gen_eta",        &W_gen_eta,        "W_gen_eta/F");
   outTree_->Branch("W_gen_phi",        &W_gen_phi,        "W_gen_phi/F");
   outTree_->Branch("tau_met_Dphi",     &tau_met_Dphi,     "tau_met_Dphi/F");
   outTree_->Branch("tau_met_ratio_pt", &tau_met_ratio_pt, "tau_met_ratio_pt/F");
   outTree_->Branch("tau_met_pt",       &tau_met_pt,       "tau_met_pt/F");
   outTree_->Branch("tau_met_phi",      &tau_met_phi,      "tau_met_phi/F");
   outTree_->Branch("tau_rawMet_pt",    &tau_rawMet_pt,    "tau_rawMet_pt/F");
   outTree_->Branch("tau_rawMet_phi",   &tau_rawMet_phi,   "tau_rawMet_phi/F");
   outTree_->Branch("tau_DeepMet_pt",   &tau_DeepMet_pt,   "tau_DeepMet_pt/F");
   outTree_->Branch("tau_DeepMet_phi",  &tau_DeepMet_phi,  "tau_DeepMet_phi/F");
   outTree_->Branch("miss_pz_min",      &miss_pz_min,      "miss_pz_min/F");
   outTree_->Branch("miss_pz_max",      &miss_pz_max,      "miss_pz_max/F");
   outTree_->Branch("W_pt",             &W_pt,             "W_pt/F");
   outTree_->Branch("W_eta_min",        &W_eta_min,        "W_eta_min/F");
   outTree_->Branch("W_eta_max",        &W_eta_max,        "W_eta_max/F");
   outTree_->Branch("W_phi",            &W_phi,            "W_phi/F");
   outTree_->Branch("W_mass_min",       &W_mass_min,       "W_mass_min/F");
   outTree_->Branch("W_mass_max",       &W_mass_max,       "W_mass_max/F");
   outTree_->Branch("W_Deep_pt",        &W_Deep_pt,        "W_Deep_pt/F");
   outTree_->Branch("W_Deep_eta_min",   &W_Deep_eta_min,   "W_Deep_eta_min/F");
   outTree_->Branch("W_Deep_eta_max",   &W_Deep_eta_max,   "W_Deep_eta_max/F");
   outTree_->Branch("W_Deep_phi",       &W_Deep_phi,       "W_Deep_phi/F");
   // * fake rate *
   outTree_->Branch("tau_phiMuMu_mass", &tau_phiMuMu_mass, "tau_phiMuMu_mass/F"); 
   outTree_->Branch("tau_MuMuPi_mass",  &tau_MuMuPi_mass,  "tau_MuMuPi_mass/F"); 


    //outTree_->Branch("", &, "/")


}// outTreeSetUp()
