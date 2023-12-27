#include "../include/prepStudiesT3m.h"

prepStudiesT3m::prepStudiesT3m(TTree *tree, const TString & outdir, const TString & tags) : Tau3Mu_base(tree){

    tags_ = tags;
    //if (tags_.Contains("data",TString::kIgnoreCase ) || tags_.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase )) isBlind_ = true;
    //else isBlind_ = false;
    isBlind_ = false;
    if(isBlind_) std::cout << " > running analysis blind" << std::endl;
    else std::cout << " > running analysis open!!" << std::endl;
    
    // output
    outFilePath_ = outdir + "/recoKinematicsT3m_"+ tags_ + ".root";
    outTreeSetUp();

}//prepStudiesT3m()

void prepStudiesT3m::Loop(){

    if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   int Nevents = 0;
   const Long64_t Nbreak = nentries + 10; 
   const Long64_t Nprint = (int)(nentries/20.);
   
   unsigned int nTriggerBit = 0, nEvTriggerFired_Tau3Mu = 0, nEvTriggerFired_DoubleMu = 0, nEvDiMuResVeto = 0;
   unsigned int nTauFired3Mu = 0, nTauDiMuonVeto = 0, nTauMCmatched = 0;
   bool flag_HLT_Tau3mu = false, flag_HLT_DoubleMu = false, flag_diMuResVeto =true;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {

        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0 || jentry == Nbreak) break;
        if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        Nevents++;

        // --- TRIGGER BIT
        if((HLTconf_ == HLT_paths::HLT_Tau3Mu) &&
            !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15)) continue;
        if((HLTconf_ == HLT_paths::HLT_DoubleMu) &&
            !HLT_DoubleMu4_3_LowMass) continue;
        nTriggerBit++;

        LumiBlock = luminosityBlock;
        Run = run;
        Event = event;
        nGoodPV = PV_npvsGood;

        // --- loop on TAU candidates
        flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false;
        flag_diMuResVeto = true;
        tau_mu12_M = -1.0; tau_mu23_M = -1.0; tau_mu13_M = -1.0;
        for(unsigned int t = 0; t < nTauTo3Mu; t++){
            // check muons MediumID
            if(!RecoPartFillP4(t)) continue;

            
            // trigger matching
            if(!TriggerMatching(t)) continue;
            if(HLTconf_ == HLT_paths::HLT_Tau3Mu)   flag_HLT_Tau3mu = true;
            if(HLTconf_ == HLT_paths::HLT_DoubleMu) flag_HLT_DoubleMu = true;
            if(HLTconf_ == HLT_paths::HLT_overlap){
                flag_HLT_Tau3mu   = TriggerMatching(t,HLT_paths::HLT_Tau3Mu);
                flag_HLT_DoubleMu = TriggerMatching(t,HLT_paths::HLT_DoubleMu);
            }
            nTauFired3Mu++;
            HLT_isfired_DoubleMu= (int)flag_HLT_DoubleMu; HLT_isfired_Tau3Mu = (int)flag_HLT_Tau3mu; 

            n_tau = nTauTo3Mu;
            h_nTau->Fill(nTauTo3Mu);

            // blind if needed
            if(isBlind_ && RecoTau_P4.M() > blindTauMass_low && RecoTau_P4.M() < blindTauMass_high ) continue;
            // veto diMuonResonances
            if (TauTo3Mu_diMuVtxFit_bestProb[t] > 0){
                h_diMuon_Mass->Fill(TauTo3Mu_diMuVtxFit_bestMass[t]);
                tau_dimuon_mass = TauTo3Mu_diMuVtxFit_bestMass[t];
            }
            if (TauTo3Mu_diMuVtxFit_toVeto[t]) continue;
            if (flag_diMuResVeto) { nEvDiMuResVeto++; flag_diMuResVeto = false;}
            nTauDiMuonVeto++;

            // muonsID
            tau_mu1_MediumID    = Muon_isMedium[TauTo3Mu_mu1_idx[t]];   tau_mu2_MediumID   = Muon_isMedium[TauTo3Mu_mu2_idx[t]];    tau_mu3_MediumID   = Muon_isMedium[TauTo3Mu_mu2_idx[t]];
            tau_mu1_LooseID     = Muon_isLoose[TauTo3Mu_mu1_idx[t]];    tau_mu2_LooseID    = Muon_isLoose[TauTo3Mu_mu2_idx[t]];     tau_mu3_LooseID    = Muon_isLoose[TauTo3Mu_mu2_idx[t]];
            tau_mu1_SoftID_PV   = Muon_isSoft[TauTo3Mu_mu1_idx[t]];     tau_mu2_SoftID_PV  = Muon_isSoft[TauTo3Mu_mu2_idx[t]];      tau_mu3_SoftID_PV  = Muon_isSoft[TauTo3Mu_mu3_idx[t]];
            tau_mu1_SoftID_BS   = Muon_isSoft_BS[TauTo3Mu_mu1_idx[t]];  tau_mu2_SoftID_BS  = Muon_isSoft_BS[TauTo3Mu_mu2_idx[t]];   tau_mu3_SoftID_BS  = Muon_isSoft_BS[TauTo3Mu_mu3_idx[t]];
            tau_mu1_TightID_PV  = Muon_isTight[TauTo3Mu_mu1_idx[t]];    tau_mu2_TightID_PV = Muon_isTight[TauTo3Mu_mu2_idx[t]];     tau_mu3_TightID_PV = Muon_isTight[TauTo3Mu_mu3_idx[t]];
            tau_mu1_TightID_BS  = Muon_isTight_BS[TauTo3Mu_mu1_idx[t]]; tau_mu2_TightID_BS = Muon_isTight_BS[TauTo3Mu_mu2_idx[t]];  tau_mu3_TightID_BS = Muon_isTight_BS[TauTo3Mu_mu3_idx[t]];


            //-------
            h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu1_idx[t]]); h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu2_idx[t]]); h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu3_idx[t]]);
            h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu1_idx[t]]); h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu2_idx[t]]); h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu3_idx[t]]);
            h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu1_idx[t]]); h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu2_idx[t]]); h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu3_idx[t]]);
            h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu1_idx[t]]); h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu2_idx[t]]); h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu3_idx[t]]);
            h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu1_idx[t]]); h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu2_idx[t]]); h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu3_idx[t]]);
            
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
           
            //----
            h_MuLeading_pT->Fill(TauTo3Mu_mu1_pt[t]);
            h_MuSubLeading_pT->Fill(TauTo3Mu_mu2_pt[t]);
            h_MuTrailing_pT->Fill(TauTo3Mu_mu3_pt[t]);
            h_MuLeading_eta->Fill(TauTo3Mu_mu1_eta[t]);
            h_MuSubLeading_eta->Fill(TauTo3Mu_mu2_eta[t]);
            h_MuTrailing_eta->Fill(TauTo3Mu_mu3_eta[t]);
            h_Mu_Dz12->Fill(TauTo3Mu_dZmu12[t]);
            h_Mu_Dz23->Fill(TauTo3Mu_dZmu23[t]);
            h_Mu_Dz13->Fill(TauTo3Mu_dZmu13[t]);

            // Tau -> 3mu
            tau_fit_charge = TauTo3Mu_charge[t]; 
            tau_raw_mass = (RecoMu1_P4+RecoMu2_P4+RecoMu3_P4).M(); 
            tau_fit_mass = TauTo3Mu_fitted_mass[t];
            tau_fit_mass_err =  sqrt(TauTo3Mu_fitted_mass_err2[t]);
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
            //---
            h_Tau_fit_M->Fill(TauTo3Mu_fitted_mass[t]);
            h_Tau_fit_pT->Fill(TauTo3Mu_fitted_pt[t]);
            h_Tau_fit_eta->Fill(RecoTau_P4.Eta());
            h_Tau_relIso->Fill(TauTo3Mu_absIsolation[t]/TauTo3Mu_fitted_pt[t]);
            h_LxySign_BSvtx->Fill(TauTo3Mu_sigLxy_3muVtxBS[t]);
            h_Tau_Mt->Fill(TauPlusMET_Tau_Puppi_mT[t]);
            h_Tau_Pvtx->Fill(TauTo3Mu_vtx_prob[t]);
            h_Tau_cosAlpha_BS->Fill(TauTo3Mu_CosAlpha2D_LxyP3mu[t]);
            // tau + MET (Puppi)
            float Dphi_MET = fabs(RecoTau_P4.Phi()- DeepMETResolutionTune_phi);
            if (Dphi_MET > 2*M_PI) Dphi_MET = 2*M_PI - Dphi_MET;
            h_DPhi_TauDeepMET->Fill(Dphi_MET);
            Dphi_MET = fabs(RecoTau_P4.Phi()- PuppiMET_phi);
            if (Dphi_MET > 2*M_PI){
               std::cout << " Dphi PuppiMET " << Dphi_MET << std::endl;
               float full_angle = 2*M_PI;
               Dphi_MET = Dphi_MET - full_angle;
               std::cout << " Dphi PuppiMET corrected " << Dphi_MET << std::endl;
            }
            h_DPhi_TauPuppiMET->Fill(Dphi_MET);
            h_TauPt_DeepMET->Fill(RecoTau_P4.Pt()/DeepMETResolutionTune_pt);
            h_TauPt_PuppiMET->Fill(RecoTau_P4.Pt()/PuppiMET_pt);
            h_missPz_min->Fill(TauPlusMET_DeepMETminPz[t]);
            h_missPz_max->Fill(TauPlusMET_DeepMETmaxPz[t]);

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
            h_W_pT->Fill(TauPlusMET_pt[t]);

            outTree_->Fill();
        }// loop on tau cands

        // HLT summary
        if(flag_HLT_Tau3mu) nEvTriggerFired_Tau3Mu++;
        if(flag_HLT_DoubleMu) nEvTriggerFired_DoubleMu++;
        
    }// loop on events

    saveOutput();
    std::cout << "...processed " << Nevents << " events" << std::endl;
    std::cout << " == summary == " << std::endl;
    std::cout << " Events whith HLT-bit ON " << nTriggerBit << std::endl;
    std::cout << " Events which fully fired HLT_Tau3Mu " << nEvTriggerFired_Tau3Mu << std::endl;
    std::cout << " Events which fully fired HLT_DoubleMu " << nEvTriggerFired_DoubleMu << std::endl;
    std::cout << " Events after di-muon resonance veto " << nEvDiMuResVeto << std::endl;
    std::cout << " Tau candidates with 3 fired muons " << nTauFired3Mu << std::endl;
    std::cout << " Tau candidates after diMu veto " << nTauDiMuonVeto << std::endl;
    

}//Loop()

void prepStudiesT3m::saveOutput(){

    outFile_ = new TFile(outFilePath_, "RECREATE");
    outFile_->cd();

    h_Mu_MediumID->Write();
    h_Mu_SoftID->Write();
    h_Mu_SoftID_BS->Write();
    h_Mu_TightID->Write();
    h_Mu_TightID_BS->Write();

    h_MuLeading_pT->Write();
    h_MuSubLeading_pT->Write();
    h_MuTrailing_pT->Write();
    h_MuLeading_eta->Write();
    h_MuSubLeading_eta->Write();
    h_MuTrailing_eta->Write();
    h_Mu_Dz12->Write();
    h_Mu_Dz23->Write();
    h_Mu_Dz13->Write();
    h_nTau->Write();
    h_Tau_fit_M->Write();
    h_Tau_fit_pT->Write();
    h_Tau_fit_eta->Write();
    h_Tau_fitNoVtx_M->Write();
    h_Tau_relIso->Write();
    h_LxySign_BSvtx->Write();
    h_diMuon_Mass->Write();
    h_Tau_Mt->Write();
    h_Tau_Pvtx->Write();
    h_Tau_cosAlpha_BS->Write();

    h_DPhi_TauDeepMET->Write();
    h_DPhi_TauPuppiMET->Write();
    h_TauPt_DeepMET->Write();
    h_TauPt_PuppiMET->Write();
    h_missPz_min->Write();
    h_missPz_max->Write();

    h_W_pT->Write();

    outTree_->Write();

    outFile_->Close();
    std::cout << " [OUTPUT] root file saved in " << outFilePath_ << std::endl;

}//saveOutput()

bool prepStudiesT3m::TriggerMatching(const int TauIdx, const int config){
    int trigger_configuration = (config == -1 ? HLTconf_ : config);
    bool is_fired_trigger = false;
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
        is_fired_trigger = (is_fired_1 || is_fired_2) && HLT_Tau3Mu_emulator(TauIdx);
    }
    if(trigger_configuration == HLT_paths::HLT_DoubleMu){
        is_fired_trigger = HLT_DoubleMu4_3_LowMass &&
	  (
	   (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx]) ||
	   (TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx]) ||
	   (TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx] && TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx])
	   ) && 
	  HLT_DoubleMu_emulator(TauIdx);
    }
    if(trigger_configuration == HLT_paths::HLT_overlap) is_fired_trigger = true;
    return is_fired_trigger;
}// TriggerMatching()

bool prepStudiesT3m::HLT_DoubleMu_emulator(const int TauIdx){
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

bool prepStudiesT3m::HLT_Tau3Mu_emulator(const int TauIdx){

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

}//HLT_Tau3Mu_emulator()

void prepStudiesT3m::outTreeSetUp(){
    
    outTree_ = new TTree(outTree_name_, "Tau3Mu candidates with HLT implemented");
    std::cout << " out tree setting up ... " << std::endl;

    outTree_->Branch("run", &Run, "run/i");
    outTree_->Branch("LumiBlock", &LumiBlock, "LumiBlock/i");
    outTree_->Branch("event", &Event, "Event/l");
    outTree_->Branch("nGoodPV", &nGoodPV, "nGoodPV/i");
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
    outTree_->Branch("tau_raw_mass",     &tau_raw_mass,     "tau_raw_mass/F");
    outTree_->Branch("tau_fit_mass",     &tau_fit_mass,     "tau_fit_mass/F");
    outTree_->Branch("tau_fit_mass_err", &tau_fit_mass_err,"tau_fit_mass_err/F");
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
    outTree_->Branch("tau_met_Dphi",     &tau_met_Dphi,     "tau_met_Dphi/F");
    outTree_->Branch("tau_met_ratio_pt", &tau_met_ratio_pt, "tau_met_ratio_pt/F");
    outTree_->Branch("tau_met_pt",       &tau_met_pt,       "tau_met_pt/F");
    outTree_->Branch("tau_met_phi",       &tau_met_phi,       "tau_met_phi/F");
    outTree_->Branch("tau_rawMet_pt",    &tau_rawMet_pt,    "tau_rawMet_pt/F");
    outTree_->Branch("tau_rawMet_phi",    &tau_rawMet_phi,    "tau_rawMet_phi/F");
    outTree_->Branch("tau_DeepMet_pt",    &tau_DeepMet_pt,    "tau_DeepMet_pt/F");
    outTree_->Branch("tau_DeepMet_phi",    &tau_DeepMet_phi,    "tau_DeepMet_phi/F");
    outTree_->Branch("miss_pz_min",      &miss_pz_min,      "miss_pz_min/F");
    outTree_->Branch("miss_pz_max",      &miss_pz_max,      "miss_pz_max/F");
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
