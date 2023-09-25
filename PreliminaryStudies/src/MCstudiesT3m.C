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

    unsigned int nTriggerBit = 0, nTriggerFired3Mu = 0, nTauDiMuonVeto = 0, nTauMCmatched = 0;

    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0 || jentry == Nbreak) break;
        if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
        nb = fChain->GetEntry(jentry);   nbytes += nb;

        // --- TRIGGER BIT
        if(!HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1) continue;
        nTriggerBit++;
        // --- MC truth & matching
        GenPartFillP4();
        TauTo3Mu_MCmatch_idx = MCtruthMatching();

        // --- loop on TAU candidates
        for(unsigned int t = 0; t < nTauTo3Mu; t++){

            if(!RecoPartFillP4(t)) continue;
            // check if the 3 muons fired the trigger
            if( !(TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                    TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                    TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1) ) continue;
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

    saveOutput();

    std::cout << " == summary == " << std::endl;
    std::cout << " Events wich fired HLT " << nTriggerBit << std::endl;
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


void MCstudiesT3m::saveOutput(){

    outFile_ = new TFile(outFilePath_, "RECREATE");
    outFile_->cd();

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
