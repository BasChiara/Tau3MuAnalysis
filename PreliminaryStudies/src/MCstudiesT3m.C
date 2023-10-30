#include "../include/MCstudiesT3m.h"

MCstudiesT3m::MCstudiesT3m(TTree *tree, const TString & tags) : MCTau3Mu_base(tree, tags){

    outFilePath_ = "./outRoot/MCstudiesT3m_"+ tags_ + ".root";
    
}

MCstudiesT3m::~MCstudiesT3m(){
    delete outFile_;
}// ~MCstudiesT3m()

void MCstudiesT3m::Loop(){

    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t nbytes = 0, nb = 0;
    const Long64_t Nbreak = nentries + 10; 
    const Long64_t Nprint = (int)(nentries/20.);

    unsigned int nTriggerBit = 0, nEvTriggerFired_Tau3Mu = 0, nEvTriggerFired_DoubleMu = 0, nTriggerFired3Mu = 0, nTauDiMuonVeto = 0, nTauMCmatched = 0;
    bool flag_HLT_Tau3mu = false, flag_HLT_DoubleMu = false;

    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0 || jentry == Nbreak) break;
        if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
        nb = fChain->GetEntry(jentry);   nbytes += nb;

        // --- TRIGGER BIT
        if((HLTconf_ == HLT_paths::HLT_Tau3Mu) &&
            !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15)) continue;
        if((HLTconf_ == HLT_paths::HLT_DoubleMu) &&
            !HLT_DoubleMu4_3_LowMass) continue;
        if((HLTconf_ == HLT_paths::HLT_overlap) &&
	   !(HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 || HLT_DoubleMu4_3_LowMass)) continue;

        nTriggerBit++;
        // --- MC truth & matching
        GenPartFillP4();
        TauTo3Mu_MCmatch_idx = MCtruthMatching();

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
                if(!flag_HLT_Tau3mu)   flag_HLT_Tau3mu   = TriggerMatching(t,HLT_paths::HLT_Tau3Mu);
                if(!flag_HLT_DoubleMu) flag_HLT_DoubleMu = TriggerMatching(t,HLT_paths::HLT_DoubleMu);
            }
            nTriggerFired3Mu++;
            h_nTau->Fill(nTauTo3Mu);

            // veto diMuonResonances
            if (TauTo3Mu_diMuVtxFit_bestProb[t] > 0) h_diMuon_Mass->Fill(TauTo3Mu_diMuVtxFit_bestMass[t]);
            if (TauTo3Mu_diMuVtxFit_toVeto[t]) continue;
            nTauDiMuonVeto++;

            if( t != TauTo3Mu_MCmatch_idx) continue;
            nTauMCmatched++;

            // GENERATOR-LEVEL
            h_gen_MuLeading_pT->Fill(GenMu1_P4.Pt());
            h_gen_MuSubLeading_pT->Fill(GenMu2_P4.Pt());
            h_gen_MuTrailing_pT->Fill(GenMu3_P4.Pt());

            h_gen_Tau_M->Fill(GenTau_P4.M());
            h_gen_Tau_pT->Fill(GenTau_P4.Pt());
            h_gen_Tau_eta->Fill(GenTau_P4.Eta());
            h_gen_Tau_phi->Fill(GenTau_P4.Phi());

            h_gen_W_pT->Fill(GenW_P4.Pt());

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
            h_Tau_raw_M->Fill( (RecoMu1_P4+RecoMu2_P4+RecoMu3_P4).M() );
            h_Tau_fit_MrelErr->Fill(sqrt(TauTo3Mu_fitted_mass_err2[t])/TauTo3Mu_fitted_mass[t]);
            h_Tau_fit_pT->Fill(RecoTau_P4.Pt());
            h_Tau_fit_eta->Fill(RecoTau_P4.Eta());
            h_Tau_fit_phi->Fill(RecoTau_P4.Phi());
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
            h_DPhi_TauPuppiMET->Fill(Dphi_MET);
            h_TauPt_DeepMET->Fill(RecoTau_P4.Pt()/DeepMETResolutionTune_pt);
            h_TauPt_PuppiMET->Fill(RecoTau_P4.Pt()/PuppiMET_pt);
            if (TauPlusMET_PuppiMETminPz[t]!=-999){
               h_missPz_min->Fill(TauPlusMET_PuppiMETminPz[t]);
               h_missPz_max->Fill(TauPlusMET_PuppiMETmaxPz[t]);
            }

            // W
            h_W_pT->Fill(TauPlusMET_pt[t]);
            
        
        }// loop on tau cands

        // HLT superposition
        h_HLT_T3MvsDM4->Fill(flag_HLT_DoubleMu, flag_HLT_Tau3mu);
        if(flag_HLT_Tau3mu) nEvTriggerFired_Tau3Mu++;
        if(flag_HLT_DoubleMu) nEvTriggerFired_DoubleMu++;

        // MET - Puppi correction
        h_diffGenPuppiMET->Fill(GenMET_pt-PuppiMET_pt);
        float PuppiMET_Nu_Dphi = PuppiMET_phi - GenNu_P4.Phi();
        float LongMET_Puppi = PuppiMET_pt*cos(PuppiMET_Nu_Dphi);
        float PerpMET_Puppi = PuppiMET_pt*sin(PuppiMET_Nu_Dphi);
        h_diffLongGenPuppiMET->Fill(LongMET_Puppi - GenNu_P4.Pt());
        h_ratioLongGenPuppiMET->Fill(LongMET_Puppi/GenNu_P4.Pt());
        h_ratioPerpGenPuppiMET->Fill(PerpMET_Puppi/GenNu_P4.Pt());
        // MET - DeepMET correction
        h_diffGenDeepMET->Fill(GenMET_pt-DeepMETResolutionTune_pt);
        float DeepMET_Nu_Dphi = DeepMETResolutionTune_phi - GenNu_P4.Phi();
        float LongMET_Deep = DeepMETResolutionTune_pt*cos(DeepMET_Nu_Dphi);
        float PerpMET_Deep = DeepMETResolutionTune_pt*sin(DeepMET_Nu_Dphi);
        h_diffLongGenDeepMET->Fill(LongMET_Deep-GenNu_P4.Pt());
        h_ratioLongGenDeepMET->Fill(LongMET_Deep/GenNu_P4.Pt());
        h_ratioPerpGenDeepMET->Fill(PerpMET_Deep/GenNu_P4.Pt());
        

    }// loop on events

    h_HLT_T3MvsDM4->Scale(1./nentries);
    saveOutput();

    std::cout << " == summary == " << std::endl;
    std::cout << " Events " << nentries << std::endl;
    std::cout << " Events whith HLT-bit ON " << nTriggerBit << std::endl;
    std::cout << " Events which fully fired HLT_Tau3Mu " << nEvTriggerFired_Tau3Mu << std::endl;
    std::cout << " Events which fully fired HLT_DoubleMu " << nEvTriggerFired_DoubleMu << std::endl;
    std::cout << " Tau candidates with 3 fired muons " << nTriggerFired3Mu << std::endl;
    std::cout << " Tau candidates after diMu veto " << nTauDiMuonVeto << std::endl;
    std::cout << " Tau candidates MC matched " << nTauMCmatched << std::endl;


} //Loop()


bool  MCstudiesT3m::RecoPartFillP4(const int TauIdx){

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

    return muonsTrksQualityCheck;
}// RecoPartFillP4

int   MCstudiesT3m::MCtruthMatching(const bool verbose){
    
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

bool MCstudiesT3m::TriggerMatching(const int TauIdx, const int config){
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
}//TriggerMatching()


bool MCstudiesT3m::HLT_Tau3Mu_emulator(const int TauIdx){

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

bool MCstudiesT3m::HLT_DoubleMu_emulator(const int TauIdx){
  
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


void MCstudiesT3m::saveOutput(){

    outFile_ = new TFile(outFilePath_, "RECREATE");
    outFile_->cd();
    
    h_HLT_T3MvsDM4->Write();

    h_gen_MuLeading_pT->Write();
    h_gen_MuSubLeading_pT->Write();
    h_gen_MuTrailing_pT->Write();
    h_gen_Tau_M->Write();
    h_gen_Tau_pT->Write();
    h_gen_Tau_eta->Write();
    h_gen_Tau_phi->Write();
    h_gen_W_pT->Write();


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
    h_Tau_fit_MrelErr->Write();
    h_Tau_raw_M->Write();
    h_Tau_fit_pT->Write();
    h_Tau_fit_eta->Write();
    h_Tau_fit_phi->Write();
    h_Tau_relIso->Write();
    h_LxySign_BSvtx->Write();
    h_diMuon_Mass->Write();
    h_Tau_Mt->Write();
    h_Tau_Pvtx->Write();
    h_Tau_cosAlpha_BS->Write();

    h_diffGenPuppiMET->Write();
    h_diffLongGenPuppiMET->Write();
    h_ratioLongGenPuppiMET->Write();
    h_ratioPerpGenPuppiMET->Write();
    h_diffGenDeepMET->Write();
    h_diffLongGenDeepMET->Write();
    h_ratioLongGenDeepMET->Write();
    h_ratioPerpGenDeepMET->Write();
    h_DPhi_TauDeepMET->Write();
    h_DPhi_TauPuppiMET->Write();
    h_TauPt_DeepMET->Write();
    h_TauPt_PuppiMET->Write();
    h_missPz_min->Write();
    h_missPz_max->Write();

    h_W_pT->Write();


    outFile_->Close();

    std::cout << " [OUTPUT] root file saved in " << outFilePath_ << std::endl;

}//saveOutput()
