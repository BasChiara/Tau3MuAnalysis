#include "../include/prepStudiesT3m.h"

prepStudiesT3m::prepStudiesT3m(TTree *tree, const TString & tags) : Tau3Mu_base(tree){

    tags_ = tags;
    outFilePath_ = "./outRoot/DATAstudiesT3m_"+ tags_ + ".root";

}//prepStudiesT3m()

void prepStudiesT3m::Loop(){

    if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   int Nevents = 0;
   std::cout << "...in the Loop()"<< std::endl;
   const Long64_t Nbreak = nentries + 10; 
   const Long64_t Nprint = 1;//(int)(nentries/20.);
   unsigned int nTriggerBit = 0, nTriggerFired3Mu = 0, nTauDiMuonVeto = 0;


   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {

        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0 || jentry == Nbreak) break;
        if ((jentry+1) % Nprint == 0) std::cout << "--> " << Form("%3.0f",(float)(jentry+1)/nentries* 100.) << " \%"<< std::endl;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        Nevents++;

        // --- TRIGGER BIT
        if(!HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1) continue;
        nTriggerBit++;

        // --- loop on TAU candidates
        for(unsigned int t = 0; t < nTauTo3Mu; t++){

            if(!RecoPartFillP4(t)) continue;
            // check if the 3 muons fired the trigger
            if( !(TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                    TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 &&
                    TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1) ) continue;
            nTriggerFired3Mu++;

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

            // Tau -> 3mu
            h_nTau->Fill(nTauTo3Mu);
            h_Tau_fit_M->Fill(TauTo3Mu_fitted_vc_mass[t]);
            h_Tau_fit_pT->Fill(TauTo3Mu_fitted_vc_pt[t]);
            h_Tau_relIso->Fill(TauTo3Mu_absIsolation[t]/TauTo3Mu_fitted_vc_pt[t]);
            h_Tau_fitNoVtx_M->Fill(TauTo3Mu_fitted_wovc_mass[t]);
            h_LxySign_BSvtx->Fill(TauTo3Mu_sigLxy_3muVtxBS[t]);
            
        }// loop on tau cands
    }// loop on events

    saveOutput();
    std::cout << "...processed " << Nevents << " events" << std::endl;
    std::cout << " == summary == " << std::endl;
    std::cout << " Events wich fired HLT " << nTriggerBit << std::endl;
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

    h_nTau->Write();
    h_Tau_fit_M->Write();
    h_Tau_fit_pT->Write();
    h_Tau_fitNoVtx_M->Write();
    h_Tau_relIso->Write();
    h_LxySign_BSvtx->Write();
    h_diMuon_Mass->Write();

    outFile_->Close();
    std::cout << " [OUTPUT] root file saved in " << outFilePath_ << std::endl;

}//saveOutput()