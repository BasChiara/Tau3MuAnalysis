#include "../include/DsPhiMuMuPi_analyzer.h"

void DsPhiMuMuPi_analyzer::Loop(){

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;
   const Long64_t Nbreak = nentries + 10; 
   const Long64_t Nprint = (int)(nentries/20.);
   
   unsigned int Nevents =0;
   unsigned int nEvDsPhiPi =0, nEvTriggerBit = 0, nEvTriggerFired_Tau3Mu = 0, nEvTriggerFired_DoubleMu = 0, nEvTriggerFired_Total = 0, nEvReinforcedHLT = 0, nEvDiMuResVeto = 0, nEvMETfilters =0;
   unsigned int nDsFired3Mu = 0, nDsReinforcedHLT = 0, nDsDiMuonVeto = 0, nDsMCmatched = 0;
   bool flag_HLT_Tau3mu = false, flag_HLT_DoubleMu = false, flag_reinfHLT = true, flag_diMuResVeto =true;


   for (Long64_t jentry=0; jentry<nentries;jentry++) {
   
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0 || jentry == Nbreak) break;
      if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      Nevents++;
      
      // analyze only Ds->Phi Pi passing MET filters
      if (nDsPhiPi == 0) continue;
      if (!applyMETfilters(0)) continue; 
      nEvDsPhiPi++;
      
      // --- TRIGGER BIT
      if((HLTconf_ == HLT_paths::HLT_Tau3Mu) &&
            !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15)) continue;
      if((HLTconf_ == HLT_paths::HLT_DoubleMu) &&
            !HLT_DoubleMu4_3_LowMass) continue;
      if((HLTconf_ == HLT_paths::HLT_overlap) &&
            !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 || HLT_DoubleMu4_3_LowMass)) continue;
      nEvTriggerBit++;

      LumiBlock = luminosityBlock;
      Run = run;
      Event = event;
      nGoodPV = PV_npvsGood;
      Rho_Fj = Rho_fixedGridRhoFastjetAll;
      // --- MC truth & matching
      if(isMC_) {
         GenPartFillP4();
         DsPhiPi_MCmatch_idx = MCtruthMatching();
         // save GENERATOR-LEVEL info
         phi_mu1_gen_pt  = GenMu1_P4.Pt();  phi_mu2_gen_pt  = GenMu2_P4.Pt();
         phi_mu1_gen_eta = GenMu1_P4.Eta(); phi_mu2_gen_eta = GenMu2_P4.Eta();
         phi_gen_mass    = GenPhi_P4.M(); phi_gen_pt = GenPhi_P4.Pt(); phi_gen_eta = GenPhi_P4.Eta(); phi_gen_phi = GenPhi_P4.Phi();    
         pi_gen_pt       = GenPi_P4.Pt(); pi_gen_eta = GenPi_P4.Eta(); pi_gen_phi = GenPi_P4.Phi();
         Ds_gen_pt       = GenDs_P4.Pt(); Ds_gen_eta = GenDs_P4.Eta(); Ds_gen_phi = GenDs_P4.Phi();
         gen_met_pt = GenMET_pt; gen_met_phi = GenMET_phi;
      }
      // --- loop on TAU candidates
      flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false;
      flag_reinfHLT = true; flag_diMuResVeto = true;
      // sort candidates by transverse mass
      std::vector<unsigned int> Ds_idxs = sorted_cand_mT();
      //for(unsigned int t = 0; t < nDsPhiPi; t++){
      for(unsigned int t: Ds_idxs){
         // check muons MediumID
         if(!RecoPartFillP4(t)) continue;
            
         // trigger matching
         //if(!TriggerMatching(t, HLTconf_)) continue;
         flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false;
         if(HLTconf_ == HLT_paths::HLT_Tau3Mu)   flag_HLT_Tau3mu   = TriggerMatching(t, HLTconf_);
         if(HLTconf_ == HLT_paths::HLT_DoubleMu) flag_HLT_DoubleMu = TriggerMatching(t, HLTconf_);
         if(HLTconf_ == HLT_paths::HLT_overlap){
            flag_HLT_Tau3mu   = TriggerMatching(t,HLT_paths::HLT_Tau3Mu);
            flag_HLT_DoubleMu = TriggerMatching(t,HLT_paths::HLT_DoubleMu);
         }
         if(!(flag_HLT_DoubleMu||flag_HLT_Tau3mu)) continue;
         nDsFired3Mu++;
         HLT_isfired_DoubleMu= (int)flag_HLT_DoubleMu; HLT_isfired_Tau3Mu = (int)flag_HLT_Tau3mu; 
         
         n_Ds = nDsPhiPi;
         // do not veto other resonances around the event -> (are we sure ?)
         if (flag_diMuResVeto) nEvDiMuResVeto++;
         flag_diMuResVeto = false;
         nDsDiMuonVeto++;
         // HLT_DoubleMuon reinforcement
         if (flag_HLT_DoubleMu && !HLT_DoubleMu_reinforcement(t)) continue;
         if (flag_reinfHLT) nEvReinforcedHLT++;
         flag_reinfHLT = false;
         nDsReinforcedHLT++;

         // muonsID
         phi_mu1_MediumID   = Muon_isMedium[DsPhiPi_mu1_idx[t]];   phi_mu2_MediumID   = Muon_isMedium[DsPhiPi_mu2_idx[t]];
         phi_mu1_LooseID    = Muon_isLoose[DsPhiPi_mu1_idx[t]];    phi_mu2_LooseID    = Muon_isLoose[DsPhiPi_mu2_idx[t]];
         phi_mu1_SoftID_PV  = Muon_isSoft[DsPhiPi_mu1_idx[t]];     phi_mu2_SoftID_PV  = Muon_isSoft[DsPhiPi_mu2_idx[t]];
         phi_mu1_SoftID_BS  = Muon_isSoft_BS[DsPhiPi_mu1_idx[t]];  phi_mu2_SoftID_BS  = Muon_isSoft_BS[DsPhiPi_mu2_idx[t]];
         phi_mu1_TightID_PV = Muon_isTight[DsPhiPi_mu1_idx[t]];    phi_mu2_TightID_PV = Muon_isTight[DsPhiPi_mu2_idx[t]]; 
         phi_mu1_TightID_BS = Muon_isTight_BS[DsPhiPi_mu1_idx[t]]; phi_mu2_TightID_BS = Muon_isTight_BS[DsPhiPi_mu2_idx[t]];
         // muons SF in MC
         Ds_mu1_IDrecoSF= 1.; Ds_mu2_IDrecoSF= 1.;
         Ds_mu1_IDrecoSF_sysUP = -1.; Ds_mu1_IDrecoSF_sysDOWN = -1.;  
         Ds_mu2_IDrecoSF_sysUP = -1.; Ds_mu2_IDrecoSF_sysDOWN = -1.;
         PU_weight = 1.; PU_weight_up = -1.; PU_weight_down = -1.;
         if(isMC_){
            applyMuonSF(t);
            applyPUreweight();
         }
         weight = lumi_factor * PU_weight * Ds_mu1_IDrecoSF * Ds_mu2_IDrecoSF; // PU weights to be understood !!
         //weight = lumi_factor * Ds_mu1_IDrecoSF * Ds_mu2_IDrecoSF;

         // muons kinematics
         phi_mu1_pt  = DsPhiPi_mu1_pt[t];   phi_mu2_pt  = DsPhiPi_mu2_pt[t];
         phi_mu1_eta = DsPhiPi_mu1_eta[t];  phi_mu2_eta = DsPhiPi_mu2_eta[t];
         phi_mu12_dZ = DsPhiPi_dZmu12[t];
         // pion kinematics
         pi_pt = DsPhiPi_trk_pt[t]; pi_eta = DsPhiPi_trk_eta[t]; pi_phi = DsPhiPi_trk_phi[t];
         pi_TightID = ( (double)std::rand()/RAND_MAX > 0.17 ? 1 : 0); 
         // phi(1020) kinematics
         phi_fit_charge = DsPhiPi_mu1_charge[t] + DsPhiPi_mu2_charge[t]; 
         phi_fit_mass = DsPhiPi_MuMu_fitted_mass[t];
         phi_fit_mass_err =  sqrt(DsPhiPi_MuMu_fitted_mass_err2[t]);
         phi_fit_pt = DsPhiPi_MuMu_fitted_pt[t]; 
         phi_fit_eta = DsPhiPi_MuMu_fitted_eta[t], phi_fit_phi = DsPhiPi_MuMu_fitted_phi[t];

         // Ds -> Phi(MuMu) Pi
         Ds_fit_charge = DsPhiPi_charge[t]; 
         Ds_fit_mass = DsPhiPi_fitted_mass[t];
         Ds_fit_mass_err =  sqrt(DsPhiPi_fitted_mass_err2[t]);
         Ds_fit_pt = DsPhiPi_fitted_pt[t]; 
         Ds_fit_eta = DsPhiPi_fitted_eta[t], Ds_fit_phi = DsPhiPi_fitted_phi[t];
         Ds_relIso = DsPhiPi_absIsolation[t]/DsPhiPi_fitted_pt[t];
         Ds_Iso_chargedDR04 = DsPhiPi_iso_ptChargedFromPV[t];
         Ds_Iso_photonDR04 = DsPhiPi_iso_ptPhotons[t]; 
         Ds_Iso_puDR08 = DsPhiPi_iso_ptChargedFromPU[t]; 
         Ds_relIso_pT05 = DsPhiPi_absIsolation_pT05[t]/DsPhiPi_fitted_pt[t];
         Ds_Iso_chargedDR04_pT05 = DsPhiPi_iso_ptChargedFromPV_pT05[t]; 
         Ds_Iso_photonDR04_pT05 = DsPhiPi_iso_ptPhotons_pT05[t]; 
         Ds_Iso_puDR08_pT05 = DsPhiPi_iso_ptChargedFromPU_pT05[t];
         Ds_Lxy_val_BS = DsPhiPi_Lxy_3muVtxBS[t];
         Ds_Lxy_err_BS = DsPhiPi_errLxy_3muVtxBS[t];
         Ds_Lxy_sign_BS = DsPhiPi_sigLxy_3muVtxBS[t];
         Ds_fit_vprob = DsPhiPi_vtx_prob[t];
         Ds_cosAlpha_BS = DsPhiPi_CosAlpha2D_LxyP3mu[t];
         Ds_mu1pi_dZ = DsPhiPi_dZmu13[t]; Ds_mu2pi_dZ = DsPhiPi_dZmu23[t]; 
         
         Ds_fit_mt = DsPlusMET_Tau_Puppi_mT[t];
   
         // Ds + MET (Puppi)
         float Dphi_MET = fabs(RecoDs_P4.Phi()- PuppiMET_phi);
         if (Dphi_MET > 2*M_PI){
            std::cout << " Dphi PuppiMET " << Dphi_MET << std::endl;
            float full_angle = 2*M_PI;
            Dphi_MET = Dphi_MET - full_angle;
            std::cout << " Dphi PuppiMET corrected " << Dphi_MET << std::endl;
         }

         tau_met_pt = PuppiMET_pt; tau_met_phi = PuppiMET_phi;
         tau_rawMet_pt = RawPuppiMET_pt; tau_rawMet_phi = RawPuppiMET_phi;
         tau_DeepMet_pt = DsPlusMET_DeepMET_pt[t]; tau_DeepMet_phi = 0;//DsPlusMET_DeepMET_phi[t];
         tau_met_ratio_pt = RecoDs_P4.Pt()/PuppiMET_pt;
         tau_met_Dphi = Dphi_MET;            
         miss_pz_min = DsPlusMET_PuppiMETminPz[t], miss_pz_max = DsPlusMET_PuppiMETmaxPz[t];

         // W
         W_pt = DsPlusMET_Puppi_pt[t]; W_phi = DsPlusMET_Puppi_phi[t]; 
         W_eta_min =  DsPlusMET_Puppi_eta_min[t];  W_eta_max =  DsPlusMET_Puppi_eta_max[t]; 
         W_mass_min = DsPlusMET_Puppi_mass_min[t]; W_mass_max = DsPlusMET_Puppi_mass_max[t]; 
         W_Deep_pt = DsPlusMET_Deep_pt[t]; W_Deep_phi = DsPlusMET_Deep_phi[t]; 
         W_Deep_eta_min =  DsPlusMET_Deep_eta_min[t];  W_Deep_eta_max =  DsPlusMET_Deep_eta_max[t]; 

         // MC matching
         if(isMC_){
            isMCmatching = (t == DsPhiPi_MCmatch_idx); 
            if(isMCmatching) nDsMCmatched++;
         }

         // fill tree
         outTree_->Fill();
         break;
      }// loop on Ds candidates

      // HLT report 
      if(flag_HLT_Tau3mu)   nEvTriggerFired_Tau3Mu++;
      if(flag_HLT_DoubleMu) nEvTriggerFired_DoubleMu++;
      if(flag_HLT_DoubleMu||flag_HLT_Tau3mu) nEvTriggerFired_Total++;

   }// loop on events

   saveOutput();

   std::cout << " == summary == " << std::endl;
   std::cout << " Events processed "                               << Nevents << std::endl;
   std::cout << " Events whith DsPhiPi candidates "                << nEvDsPhiPi << std::endl;
   //std::cout << " Events passing MET-filters "                   << nEvMETfilters << std::endl;
   std::cout << " Events with HLT-bit ON "                         << nEvTriggerBit << std::endl;
   std::cout << " Events which fully fired HLT_Tau3Mu "            << nEvTriggerFired_Tau3Mu << std::endl;
   std::cout << " Events which fully fired HLT_DoubleMu "          << nEvTriggerFired_DoubleMu << std::endl;
   std::cout << " Events which fully fired HLT_TOTAL "             << nEvTriggerFired_Total << std::endl;
   std::cout << " Events after di-muon resonance veto "            << nEvDiMuResVeto << std::endl;
   std::cout << " Events after HLT_DoubleMu reinforcement "        << nEvReinforcedHLT << std::endl;
   std::cout << " Ds candidates with 3 fired muons "               << nDsFired3Mu << std::endl;
   std::cout << " Ds candidates after diMu veto "                  << nDsDiMuonVeto << std::endl;
   std::cout << " Ds candidates after HLT_DoubleMu reinforcement " << nDsReinforcedHLT << std::endl;
   if(isMC_) std::cout << " Ds candidates MC matched "             << nDsMCmatched << std::endl;

} // Loop


void DsPhiMuMuPi_analyzer::saveOutput(){
   
   outFile_ = new TFile(outFilePath_, "RECREATE");
   outFile_->cd();
   outTree_->Write();
   if(isMC_)
  { h_muonSF_lowpT->Write();
   h_muonSF_lowpT_sysDOWN->Write();
   h_muonSF_lowpT_sysUP->Write();}
   outFile_->Close();

   std::cout << " [OUTPUT] root file saved in " << outFilePath_ << "\n" << std::endl;

}//saveOutput()

void DsPhiMuMuPi_analyzer::outTreeSetUp(){

   outTree_ = new TTree(outTree_name_, "DsPhiMuMuPi candidates with HLT matching and preselction");
   std::cout << "[->] out tree setting up ... " << std::endl;

   outTree_->Branch("run",       &Run,       "run/i");
   outTree_->Branch("LumiBlock", &LumiBlock, "LumiBlock/i");
   outTree_->Branch("event",     &Event,     "Event/l");
   outTree_->Branch("year_id",   &year_id_,  "year_id/i");
   outTree_->Branch("nGoodPV",   &nGoodPV,   "nGoodPV/i");
   outTree_->Branch("Rho_Fj",    &Rho_Fj,    "Rho_Fj/F");
   // lumi & scale factors
   outTree_->Branch("weight",                   &weight,                   "weight/F");
   outTree_->Branch("lumi_factor",              &lumi_factor,              "lumi_factor/F");
   outTree_->Branch("Ds_mu1_IDrecoSF",          &Ds_mu1_IDrecoSF,          "Ds_mu1_IDrecoSF/F");
   outTree_->Branch("Ds_mu1_IDrecoSF_sysUP",    &Ds_mu1_IDrecoSF_sysUP,    "Ds_mu1_IDrecoSF_sysUP/F");
   outTree_->Branch("Ds_mu1_IDrecoSF_sysDOWN",  &Ds_mu1_IDrecoSF_sysDOWN,  "Ds_mu1_IDrecoSF_sysDOWN/F");
   outTree_->Branch("Ds_mu2_IDrecoSF",          &Ds_mu2_IDrecoSF,          "Ds_mu2_IDrecoSF/F");
   outTree_->Branch("Ds_mu2_IDrecoSF_sysUP",    &Ds_mu2_IDrecoSF_sysUP,    "Ds_mu2_IDrecoSF_sysUP/F");
   outTree_->Branch("Ds_mu2_IDrecoSF_sysDOWN",  &Ds_mu2_IDrecoSF_sysDOWN,  "Ds_mu2_IDrecoSF_sysDOWN/F");
   outTree_->Branch("PU_weight",                &PU_weight,                "PU_weight/F");
   outTree_->Branch("PU_weight_up",             &PU_weight_up,             "PU_weight_up/F");
   outTree_->Branch("PU_weight_down",           &PU_weight_down,           "PU_weight_down/F");
   outTree_->Branch("isMCmatching",             &isMCmatching,             "isMCmatching/I");
   // * HLT
   outTree_->Branch("HLT_isfired_Tau3Mu",     &HLT_isfired_Tau3Mu,   "HLT_isfired_Tau3Mu/I");
   outTree_->Branch("HLT_isfired_DoubleMu",   &HLT_isfired_DoubleMu, "HLT_isfired_DoubleMu/I");
   // * muons
   // ** IDs
   outTree_->Branch("phi_mu1_MediumID",     &phi_mu1_MediumID,   "phi_mu1_MediumID/I");
   outTree_->Branch("phi_mu2_MediumID",     &phi_mu2_MediumID,   "phi_mu2_MediumID/I");
   outTree_->Branch("phi_mu1_LooseID",      &phi_mu1_LooseID,    "phi_mu1_LooseID/I");
   outTree_->Branch("phi_mu2_LooseID",      &phi_mu2_LooseID,    "phi_mu2_LooseID/I");
   outTree_->Branch("phi_mu1_SoftID_PV",    &phi_mu1_SoftID_PV,  "phi_mu1_SoftID_PV/I");
   outTree_->Branch("phi_mu2_SoftID_PV",    &phi_mu2_SoftID_PV,  "phi_mu2_SoftID_PV/I");
   outTree_->Branch("phi_mu1_SoftID_BS",    &phi_mu1_SoftID_BS,  "phi_mu1_SoftID_BS/I");
   outTree_->Branch("phi_mu2_SoftID_BS",    &phi_mu2_SoftID_BS,  "phi_mu2_SoftID_BS/I");
   outTree_->Branch("phi_mu1_TightID_PV",   &phi_mu1_TightID_PV, "phi_mu1_TightID_PV/I");
   outTree_->Branch("phi_mu2_TightID_PV",   &phi_mu2_TightID_PV, "phi_mu2_TightID_PV/I");
   outTree_->Branch("phi_mu1_TightID_BS",   &phi_mu1_TightID_BS, "phi_mu1_TightID_BS/I");
   outTree_->Branch("phi_mu2_TightID_BS",   &phi_mu2_TightID_BS, "phi_mu2_TightID_BS/I");
   // ** kinematics
   outTree_->Branch("phi_mu1_pt",      &phi_mu1_pt,     "phi_mu1_pt/F");
   outTree_->Branch("phi_mu2_pt",      &phi_mu2_pt,     "phi_mu2_pt/F");
   outTree_->Branch("phi_mu1_gen_pt",  &phi_mu1_gen_pt, "phi_mu1_gen_pt/F");
   outTree_->Branch("phi_mu2_gen_pt",  &phi_mu2_gen_pt, "phi_mu2_gen_pt/F");
   outTree_->Branch("phi_mu1_eta",     &phi_mu1_eta,    "phi_mu1_eta/F");
   outTree_->Branch("phi_mu2_eta",     &phi_mu2_eta,    "phi_mu2_eta/F");
   outTree_->Branch("phi_mu1_gen_eta", &phi_mu1_gen_eta,"phi_mu1_gen_eta/F");
   outTree_->Branch("phi_mu2_gen_eta", &phi_mu2_gen_eta,"phi_mu2_gen_eta/F");
   outTree_->Branch("phi_mu12_dZ",     &phi_mu12_dZ,    "phi_mu12_dZ/F");
   // * pion kinematics
   outTree_->Branch("pi_gen_pt",            &pi_gen_pt,         "pi_gen_pt/F");
   outTree_->Branch("pi_gen_eta",           &pi_gen_eta,        "pi_gen_eta/F");
   outTree_->Branch("pi_gen_phi",           &pi_gen_phi,        "pi_gen_phi/F");
   outTree_->Branch("pi_pt",                &pi_pt,             "pi_pt/F");
   outTree_->Branch("pi_eta",               &pi_eta,            "pi_eta/F");
   outTree_->Branch("pi_phi",               &pi_phi,            "pi_phi/F");
   outTree_->Branch("pi_TightID",           &pi_TightID,       "pi_TightID/I");
   // * phi(1020) candidates
   outTree_->Branch("phi_gen_mass",     &phi_gen_mass,     "phi_gen_mass/F");
   outTree_->Branch("phi_gen_pt",       &phi_gen_pt,      "phi_gen_pt/F");
   outTree_->Branch("phi_gen_eta",      &phi_gen_eta,     "phi_gen_eta/F");
   outTree_->Branch("phi_gen_phi",      &phi_gen_phi,     "phi_gen_phi/F");
   outTree_->Branch("phi_fit_mass",     &phi_fit_mass,     "phi_fit_mass/F");
   outTree_->Branch("phi_fit_mass_err", &phi_fit_mass_err,"phi_fit_mass_err/F");
   outTree_->Branch("phi_fit_charge",   &phi_fit_charge,   "phi_fit_charge/F");
   outTree_->Branch("phi_fit_pt",       &phi_fit_pt,      "phi_fit_pt/F");
   outTree_->Branch("phi_fit_eta",      &phi_fit_eta,     "phi_fit_eta/F");
   outTree_->Branch("phi_fit_phi",      &phi_fit_phi,     "phi_fit_phi/F");
   // * tau canditates
   outTree_->Branch("n_Ds",            &n_Ds,            "n_Ds/I");
   outTree_->Branch("Ds_fit_mass",     &Ds_fit_mass,     "Ds_fit_mass/F");
   outTree_->Branch("Ds_fit_mass_err", &Ds_fit_mass_err,"Ds_fit_mass_err/F");
   outTree_->Branch("Ds_fit_charge",   &Ds_fit_charge,   "Ds_fit_charge/F");
   outTree_->Branch("Ds_fit_pt",       &Ds_fit_pt,      "Ds_fit_pt/F");
   outTree_->Branch("Ds_fit_eta",      &Ds_fit_eta,     "Ds_fit_eta/F");
   outTree_->Branch("Ds_fit_phi",      &Ds_fit_phi,     "Ds_fit_phi/F");
   outTree_->Branch("Ds_relIso",       &Ds_relIso,      "Ds_relIso/F");
   outTree_->Branch("Ds_Iso_chargedDR04",       &Ds_Iso_chargedDR04,      "Ds_Iso_chargedDR04/F");
   outTree_->Branch("Ds_Iso_photonDR04",       &Ds_Iso_photonDR04,      "Ds_Iso_photonDR04/F");
   outTree_->Branch("Ds_Iso_puDR08",       &Ds_Iso_puDR08,      "Ds_Iso_puDR08/F");
   outTree_->Branch("Ds_relIso_pT05",  &Ds_relIso_pT05, "Ds_relIso_pT05/F");
   outTree_->Branch("Ds_Iso_chargedDR04_pT05",  &Ds_Iso_chargedDR04_pT05, "Ds_Iso_chargedDR04_pT05/F");
   outTree_->Branch("Ds_Iso_photonDR04_pT05",  &Ds_Iso_photonDR04_pT05, "Ds_Iso_photonDR04_pT05/F");
   outTree_->Branch("Ds_Iso_puDR08_pT05",  &Ds_Iso_puDR08_pT05, "Ds_Iso_puDR08_pT05/F");
   outTree_->Branch("Ds_Lxy_sign_BS",  &Ds_Lxy_sign_BS, "Ds_Lxy_sign_BS/F");
   outTree_->Branch("Ds_Lxy_err_BS",   &Ds_Lxy_err_BS, "Ds_Lxy_err_BS/F");
   outTree_->Branch("Ds_Lxy_val_BS",   &Ds_Lxy_val_BS, "Ds_Lxy_val_BS/F");
   outTree_->Branch("Ds_cosAlpha_BS",   &Ds_cosAlpha_BS, "Ds_cosAlpha_BS/F");
   outTree_->Branch("Ds_fit_mt",       &Ds_fit_mt,      "Ds_fit_mt/F");
   outTree_->Branch("Ds_fit_vprob",    &Ds_fit_vprob,   "Ds_fit_vprob/F");
   outTree_->Branch("Ds_mu1pi_dZ",  &Ds_mu1pi_dZ, "Ds_mu1pi_dZ/F");
   outTree_->Branch("Ds_mu2pi_dZ",  &Ds_mu2pi_dZ, "Ds_mu2pi_dZ/F");
   // * tau + MET
   outTree_->Branch("tau_met_Dphi",     &tau_met_Dphi,     "tau_met_Dphi/F");
   outTree_->Branch("tau_met_ratio_pt", &tau_met_ratio_pt, "tau_met_ratio_pt/F");
   outTree_->Branch("tau_met_pt",       &tau_met_pt,       "tau_met_pt/F");
   outTree_->Branch("gen_met_pt",       &gen_met_pt,       "gen_met_pt/F");
   outTree_->Branch("tau_met_phi",       &tau_met_phi,       "tau_met_phi/F");
   outTree_->Branch("gen_met_phi",       &gen_met_phi,       "gen_met_phi/F");
   outTree_->Branch("tau_rawMet_pt",    &tau_rawMet_pt,    "tau_rawMet_pt/F");
   outTree_->Branch("tau_rawMet_phi",    &tau_rawMet_phi,    "tau_rawMet_phi/F");
   outTree_->Branch("tau_DeepMet_pt",    &tau_DeepMet_pt,    "tau_DeepMet_pt/F");
   outTree_->Branch("tau_DeepMet_phi",    &tau_DeepMet_phi,    "tau_DeepMet_phi/F");
   outTree_->Branch("miss_pz_min",      &miss_pz_min,      "miss_pz_min/F");
   outTree_->Branch("miss_pz_max",      &miss_pz_max,      "miss_pz_max/F");
   outTree_->Branch("METlongNu",             &METlongNu,             "METlongNu/F");
   outTree_->Branch("METperpNu",             &METperpNu,             "METperpNu/F");
   outTree_->Branch("Ds_gen_pt",             &Ds_gen_pt,             "Ds_gen_pt/F");
   outTree_->Branch("Ds_gen_eta",             &Ds_gen_eta,             "Ds_gen_eta/F");
   outTree_->Branch("Ds_gen_phi",             &Ds_gen_phi,             "Ds_gen_phi/F");
   outTree_->Branch("W_pt",             &W_pt,             "W_pt/F");
   outTree_->Branch("W_eta_min",             &W_eta_min,             "W_eta_min/F");
   outTree_->Branch("W_eta_max",             &W_eta_max,             "W_eta_max/F");
   outTree_->Branch("W_phi",             &W_phi,             "W_phi/F");
   outTree_->Branch("W_mass_min",             &W_mass_min,             "W_mass_min/F");
   outTree_->Branch("W_mass_max",             &W_mass_max,             "W_mass_max/F");
   outTree_->Branch("W_Deep_pt",             &W_Deep_pt,             "W_Deep_pt/F");
   outTree_->Branch("W_Deep_eta_min",             &W_Deep_eta_min,             "W_Deep_eta_min/F");
   outTree_->Branch("W_Deep_eta_max",             &W_Deep_eta_max,             "W_Deep_eta_max/F");
   outTree_->Branch("W_Deep_phi",             &W_Deep_phi,             "W_Deep_phi/F");


   //outTree_->Branch("", &, "/")


}// outTreeSetUp()

