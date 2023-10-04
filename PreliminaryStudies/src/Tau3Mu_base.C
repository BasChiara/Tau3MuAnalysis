#define Tau3Mu_base_cxx
#include "../include/Tau3Mu_base.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void Tau3Mu_base::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t Nevents = 0;
   std::cout << "...in the Loop()"<< std::endl;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      Nevents++;
   }

   std::cout << "...processed " << Nevents << " events" << std::endl;
}

bool  Tau3Mu_base::RecoPartFillP4(const int TauIdx){

    // require mediumID for all muons
    bool muonsTrksQualityCheck = Muon_isMedium[TauTo3Mu_mu1_idx[TauIdx]] && 
                                Muon_isMedium[TauTo3Mu_mu2_idx[TauIdx]] && 
                                Muon_isMedium[TauTo3Mu_mu3_idx[TauIdx]];

    // muons
    RecoMu1_P4.SetPt(TauTo3Mu_mu1_pt[TauIdx]); RecoMu1_P4.SetEta(TauTo3Mu_mu1_eta[TauIdx]); RecoMu1_P4.SetPhi(TauTo3Mu_mu1_phi[TauIdx]); RecoMu1_P4.SetM(Muon_MASS);
    RecoMu2_P4.SetPt(TauTo3Mu_mu2_pt[TauIdx]); RecoMu2_P4.SetEta(TauTo3Mu_mu2_eta[TauIdx]); RecoMu2_P4.SetPhi(TauTo3Mu_mu2_phi[TauIdx]); RecoMu1_P4.SetM(Muon_MASS);
    RecoMu3_P4.SetPt(TauTo3Mu_mu3_pt[TauIdx]); RecoMu3_P4.SetEta(TauTo3Mu_mu3_eta[TauIdx]); RecoMu3_P4.SetPhi(TauTo3Mu_mu3_phi[TauIdx]); RecoMu1_P4.SetM(Muon_MASS);

    // tau
    RecoTau_P4.SetPt(TauTo3Mu_fitted_pt[TauIdx]);  RecoTau_P4.SetEta(TauTo3Mu_fitted_eta[TauIdx]); RecoTau_P4.SetPhi(TauTo3Mu_fitted_phi[TauIdx]);  RecoTau_P4.SetM(TauTo3Mu_fitted_mass[TauIdx]);

    // met in the transverse plane

    // W in the transverse plane

    return muonsTrksQualityCheck;
}// RecoPartFillP4
