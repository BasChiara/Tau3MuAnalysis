#include "../include/prepStudiesT3m.h"

prepStudiesT3m::prepStudiesT3m(TTree *tree, const TString & outdir, const TString & tags) : Tau3Mu_base(tree){

    tags_ = tags;
    if (tags_.Contains("data",TString::kIgnoreCase ) || tags_.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase )) isBlind_ = true;
    else isBlind_ = false;
    if(isBlind_) std::cout << " > running analysis blind" << std::endl;
    outFilePath_ = outdir + "/recoKinematicsT3m_"+ tags_ + ".root";


}//prepStudiesT3m()

void prepStudiesT3m::Loop(){

    if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   int Nevents = 0;
   const Long64_t Nbreak = nentries + 10; 
   const Long64_t Nprint = (int)(nentries/20.);
   
   unsigned int nTriggerBit = 0, nEvTriggerFired_Tau3Mu = 0, nEvTriggerFired_DoubleMu = 0, nTriggerFired3Mu = 0, nTauDiMuonVeto = 0, nTauMCmatched = 0;
   bool flag_HLT_Tau3mu = false, flag_HLT_DoubleMu = false;

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

        // --- loop on TAU candidates
        flag_HLT_Tau3mu = false; flag_HLT_DoubleMu = false;
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
            nTriggerFired3Mu++;
            h_nTau->Fill(nTauTo3Mu);

            // blind if needed
            if(isBlind_ && RecoTau_P4.M() > blindTauMass_low && RecoTau_P4.M() < blindTauMass_high ) continue;
            // veto diMuonResonances
            if (TauTo3Mu_diMuVtxFit_bestProb[t] > 0) h_diMuon_Mass->Fill(TauTo3Mu_diMuVtxFit_bestMass[t]);
            if (TauTo3Mu_diMuVtxFit_toVeto[t]) continue;
            nTauDiMuonVeto++;

            // muonsID
            h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu1_idx[t]]); h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu2_idx[t]]); h_Mu_MediumID->Fill(Muon_isMedium[TauTo3Mu_mu3_idx[t]]);
            h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu1_idx[t]]); h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu2_idx[t]]); h_Mu_SoftID->Fill(Muon_isSoft[TauTo3Mu_mu3_idx[t]]);
            h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu1_idx[t]]); h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu2_idx[t]]); h_Mu_SoftID_BS->Fill(Muon_isSoft_BS[TauTo3Mu_mu3_idx[t]]);
            h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu1_idx[t]]); h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu2_idx[t]]); h_Mu_TightID->Fill(Muon_isTight[TauTo3Mu_mu3_idx[t]]);
            h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu1_idx[t]]); h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu2_idx[t]]); h_Mu_TightID_BS->Fill(Muon_isTight_BS[TauTo3Mu_mu3_idx[t]]);
            // muons kinematics
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
            h_Tau_fit_M->Fill(TauTo3Mu_fitted_mass[t]);
            h_Tau_fit_pT->Fill(TauTo3Mu_fitted_pt[t]);
            h_Tau_fit_eta->Fill(RecoTau_P4.Eta());
            h_Tau_relIso->Fill(TauTo3Mu_absIsolation[t]/TauTo3Mu_fitted_pt[t]);
            h_LxySign_BSvtx->Fill(TauTo3Mu_sigLxy_3muVtxBS[t]);
            h_Tau_Mt->Fill(TauPlusMET_Tau_Puppi_mT[t]);
            h_Tau_Pvtx->Fill(TauTo3Mu_vtx_prob[t]);
            h_Tau_cosAlpha_BS->Fill(TauTo3Mu_CosAlpha2D_LxyP3mu[t]);

            float Dphi_MET = fabs(RecoTau_P4.Phi()- DeepMETResolutionTune_phi);
            if (Dphi_MET > 2*M_PI) Dphi_MET = 2*M_PI - Dphi_MET;
            h_DPhi_TauDeepMET->Fill(Dphi_MET);
            Dphi_MET = fabs(RecoTau_P4.Phi()- PuppiMET_phi);
            if (Dphi_MET > 2*M_PI) Dphi_MET = 2*M_PI - Dphi_MET;
            h_DPhi_TauPunziMET->Fill(Dphi_MET);
            h_TauPt_DeepMET->Fill(RecoTau_P4.Pt()/DeepMETResolutionTune_pt);
            h_TauPt_PunziMET->Fill(RecoTau_P4.Pt()/PuppiMET_pt);
            h_missPz_min->Fill(TauPlusMET_DeepMETminPz[t]);
            h_missPz_max->Fill(TauPlusMET_DeepMETmaxPz[t]);

            // W
            h_W_pT->Fill(TauPlusMET_pt[t]);
            
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
    std::cout << " Tau candidates with 3 fired muons " << nTriggerFired3Mu << std::endl;
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
    h_DPhi_TauPunziMET->Write();
    h_TauPt_DeepMET->Write();
    h_TauPt_PunziMET->Write();
    h_missPz_min->Write();
    h_missPz_max->Write();

    h_W_pT->Write();

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
                            TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[TauIdx]&&
                            TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[TauIdx]&&
                            TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[TauIdx]&&
                            HLT_DoubleMu_emulator(TauIdx);
    }
    if(trigger_configuration == HLT_paths::HLT_overlap) is_fired_trigger = true;
    return is_fired_trigger;

}// TriggerMatching()

bool prepStudiesT3m::HLT_DoubleMu_emulator(const int TauIdx){
    // single muon
    const float minPT_mu1 = 3.0, minPT_mu2 = 4.0;
    const float maxEta_mu = 2.5;
    if(RecoMu1_P4.Pt() < minPT_mu1 || RecoMu3_P4.Pt() < minPT_mu2) return false;
    if(fabs(RecoMu1_P4.Eta()) > maxEta_mu || fabs(RecoMu2_P4.Eta()) > maxEta_mu || fabs(RecoMu3_P4.Eta()) > maxEta_mu ) return false;
    const float minPT_mumu = 4.9, minM_mumu = 0.2, maxM_mumu = 8.5;
    if(!(( (RecoMu1_P4+RecoMu2_P4).M() > minM_mumu && (RecoMu1_P4+RecoMu2_P4).M() < maxM_mumu && (RecoMu1_P4+RecoMu2_P4).Pt() > minPT_mumu ) ||
         ( (RecoMu2_P4+RecoMu3_P4).M() > minM_mumu && (RecoMu2_P4+RecoMu3_P4).M() < maxM_mumu && (RecoMu2_P4+RecoMu3_P4).Pt() > minPT_mumu ) ||
         ( (RecoMu1_P4+RecoMu3_P4).M() > minM_mumu && (RecoMu1_P4+RecoMu3_P4).M() < maxM_mumu && (RecoMu1_P4+RecoMu3_P4).Pt() > minPT_mumu ) )
    ) return false;
    const float minVtx_prob = 0.005; // on MuMu vertex fit
    const float maxDCA_mumu = 0.5;

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
    //if(0) return false; // insert the selection on DZ(tau,mu)
    if( ROOT::Math::VectorUtil::DeltaR( RecoMu1_P4 ,RecoTau_P4) > maxDR_muTau ||
        ROOT::Math::VectorUtil::DeltaR( RecoMu2_P4 ,RecoTau_P4) > maxDR_muTau || 
        ROOT::Math::VectorUtil::DeltaR( RecoMu3_P4 ,RecoTau_P4) > maxDR_muTau) return false;
    //** TAU
    const float minPT_tau = 15.0, maxEta_tau = 2.5, minM_tau = 1.3, maxM_tau = 2.1;
    const float maxIsoCh_tau = 2.0, maxRelIsoCh_tau = 0.2;
    if(RecoTau_P4.Pt() < minPT_tau || RecoTau_P4.M() < minM_tau || RecoTau_P4.M() > maxM_tau || fabs(RecoTau_P4.Eta()) > maxEta_tau) return false;
    if(TauTo3Mu_iso_ptChargedFromPV[TauIdx] > maxIsoCh_tau || TauTo3Mu_iso_ptChargedFromPV[TauIdx]/RecoTau_P4.Pt() > maxRelIsoCh_tau) return false;
    
    return true;

}//HLT_Tau3Mu_emulator()