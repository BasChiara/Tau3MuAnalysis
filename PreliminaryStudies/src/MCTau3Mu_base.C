#define MCTau3Mu_base_cxx
#include "../include/MCTau3Mu_base.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

#include "../include/constants.h"

void MCTau3Mu_base::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      if(jentry > 10) break;
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
            

   }// loop on events
}// Loop()


void  MCTau3Mu_base::GenPartFillP4(){
    
   bool debug = false; 
   int Mu1_idx = -1, Mu2_idx = -1, Mu3_idx = -1, Tau_idx = -1, Nu_idx = -1, W_idx = -1;
   std::vector<int> Muons_idxs;
   std::vector<int> Taus_idxs;
   std::vector<float> Muons_pt;
   if (debug) {
      for (UInt_t g = 0; g < nGenPart; g++)std::cout << g << " \t " << GenPart_pdgId[g] << " \t " << GenPart_genPartIdxMother[g] << std::endl;
   }


   int mu1, mu2, mu3;
   bool tau3Mu_found = false;

   for (UInt_t g = 0; g < nGenPart; g++){

      // look for 3 muons from same Tau 
      if(abs(GenPart_pdgId[g]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isTau
            && !tau3Mu_found)
      {
         mu1 = g;
         int Tau_idx = GenPart_genPartIdxMother[g];
         if (debug) std::cout << " mu1 found @" << mu1 << std::endl;
         for(UInt_t gg = g+1; gg < nGenPart; gg++){ 
            if(abs(GenPart_pdgId[gg]) == isMuon 
            && abs(GenPart_pdgId[GenPart_genPartIdxMother[gg]]) == isTau
            && GenPart_genPartIdxMother[gg] == Tau_idx
            && !tau3Mu_found){
               if(mu1 == gg) continue;
               mu2 = gg;
               if (debug) std::cout << " mu2 found @" << mu2 << std::endl;
               for(UInt_t ggg = gg+1; ggg < nGenPart; ggg++){ 
                  if(abs(GenPart_pdgId[ggg]) == isMuon 
                     && abs(GenPart_pdgId[GenPart_genPartIdxMother[ggg]]) == isTau
                     && GenPart_genPartIdxMother[ggg] == Tau_idx
                     && !tau3Mu_found){
                     if(mu2 == ggg) continue;
                     mu3 = ggg;
                     if (debug) std::cout << " mu3 found @" << mu3 << std::endl;
                     tau3Mu_found = true;
                  }
               }
            }
         }
      }
      // look for tauonic neutrinos
      if(abs(GenPart_pdgId[g]) == isNuTau
         && abs(GenPart_pdgId[GenPart_genPartIdxMother[g]]) == isW) Nu_idx = g;
     
   }// loop on gen particles

         // save Muon and Tau idx
         Muons_idxs.push_back(mu1); Muons_idxs.push_back(mu2); Muons_idxs.push_back(mu3); 
         Taus_idxs.push_back(GenPart_genPartIdxMother[mu1]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu2]); Taus_idxs.push_back(GenPart_genPartIdxMother[mu3]);
         Muons_pt.push_back(GenPart_pt[mu1]); Muons_pt.push_back(GenPart_pt[mu2]); Muons_pt.push_back(GenPart_pt[mu3]);

     
      if(Muons_idxs.size() < 3){
         std::cout << " [ERROR] wrong number of gen-muons it is " << Muons_idxs.size() << std::endl;
         exit(-1);
      }else if(Muons_idxs.size() == 3){
         if (debug) std::cout << " [OK] 3 muons found" << std::endl;
         // Tau index & Tau's mother idx 
         Tau_idx = Taus_idxs[0];
         int motherTau_idx = GenPart_genPartIdxMother[Tau_idx];
            // Tau comes from W
         if (abs(GenPart_pdgId[motherTau_idx]) == isW)
         {
            W_idx = motherTau_idx;   
            // in case of tau radiative decays
         }else if( abs(GenPart_pdgId[motherTau_idx]) == isTau 
                && abs(GenPart_pdgId[GenPart_genPartIdxMother[motherTau_idx]]) == isW)
         {
            Tau_idx = motherTau_idx;
            W_idx = GenPart_genPartIdxMother[motherTau_idx]; 
         }  
      }else{
         std::cout << " [!!] number of gen-muons from taus is " << Muons_idxs.size() << std::endl;
         if(debug){
            for (int i=0; i < Taus_idxs.size(); i++) std::cout << Form("tau : %d\t mu: %d", Taus_idxs[i] , Muons_idxs[i])<< std::endl;
         }
         exit(-1);
      }
   

   // order muons in leading, sub-leading and trailing
   std::sort(Muons_idxs.begin(),Muons_idxs.end(), [this](int &a, int &b){ return GenPart_pt[a]>GenPart_pt[b]; });
   Mu1_idx = Muons_idxs[0]; 
   Mu2_idx = Muons_idxs[1]; 
   Mu3_idx = Muons_idxs[2]; 
   
   GenW_P4.SetPt(GenPart_pt[W_idx]); GenW_P4.SetEta(GenPart_eta[W_idx]); GenW_P4.SetPhi(GenPart_phi[W_idx]); GenW_P4.SetM(W_MASS);
   GenTau_P4.SetPt(GenPart_pt[Tau_idx]); GenTau_P4.SetEta(GenPart_eta[Tau_idx]); GenTau_P4.SetPhi(GenPart_phi[Tau_idx]); GenTau_P4.SetM(Tau_MASS);
   GenNu_P4.SetPt(GenPart_pt[Nu_idx]); GenNu_P4.SetEta(GenPart_eta[Nu_idx]); GenNu_P4.SetPhi(GenPart_phi[Nu_idx]); GenNu_P4.SetM(NuTau_MASS);
   GenMu1_P4.SetPt(GenPart_pt[Mu1_idx]); GenMu1_P4.SetEta(GenPart_eta[Mu1_idx]); GenMu1_P4.SetPhi(GenPart_phi[Mu1_idx]); GenMu1_P4.SetM(Muon_MASS);
   GenMu2_P4.SetPt(GenPart_pt[Mu2_idx]); GenMu2_P4.SetEta(GenPart_eta[Mu2_idx]); GenMu2_P4.SetPhi(GenPart_phi[Mu2_idx]); GenMu2_P4.SetM(Muon_MASS);
   GenMu3_P4.SetPt(GenPart_pt[Mu3_idx]); GenMu3_P4.SetEta(GenPart_eta[Mu3_idx]); GenMu3_P4.SetPhi(GenPart_phi[Mu3_idx]); GenMu3_P4.SetM(Muon_MASS);

   if(debug){
      std::cout << " W found @ " << W_idx << std::endl;
      std::cout << " nu found @ " << Nu_idx << std::endl;
      std::cout << " tau found @ " << Tau_idx << std::endl;
      std::cout << " Mu found @ " << Mu1_idx  << " " << Mu2_idx << " "<< Mu3_idx << std::endl;
      std::cout << " Mu pT " << GenPart_pt[Mu1_idx] << " " << GenPart_pt[Mu2_idx] << " "<< GenPart_pt[Mu3_idx] << std::endl;
   }

} // GenPartFillP4()
