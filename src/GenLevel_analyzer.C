#include "../include/GenLevel_analyzer.h"
#include <TH1F.h>
#include <TStyle.h>
#include <TCanvas.h>

void GenLevel_analyzer::Loop()
{

   fChain->SetBranchStatus("*",0);  // disable all branches
   fChain->SetBranchStatus("*GenPart*",1);  // activate branchname
   fChain->SetBranchStatus("HLT_*",1);  // activate branchname

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;
   Long64_t print_freq = 1e5;
   ULong64_t break_loop = 1e10;

   Long64_t Nevents = 0, Npassed = 0;

   // setup binning for pT
   bool muon_triggers = false;
   bool electron_triggers = false;
   float bins[] = {0.3,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,20,22,25,28,32,37,43,52,65,85,150,160,190,220,250,300,400,500,800,1500};
   TH1F* h_V_pT    = new TH1F("h_V_pT", "V->ll pT", sizeof(bins)/sizeof(bins[0])-1, bins);
   TH1F* h_V_absY  = new TH1F("h_V_absY", "V->ll |y|", 30, 0, 3.0);
   for (Long64_t jentry=0; jentry<nentries; jentry++) {
      
      Long64_t ientry = LoadTree(jentry);
      
      if (ientry < 0) break;
      if (debug_ && jentry > break_loop) break;
      if (jentry % print_freq == 0) std::cout << "# ---- entry " << jentry << std::endl;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      Nevents++;

      // trigger selection
      //muon_triggers = true; electron_triggers = true;
      muon_triggers = HLT_IsoMu24 || HLT_IsoTkMu24 || HLT_IsoMu22 || HLT_IsoTkMu22 || HLT_Mu50;
      electron_triggers = HLT_Ele105_CaloIdVT_GsfTrkIdT || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Ele25_eta2p1_WPTight_Gsf || HLT_Ele27_WPTight_Gsf || HLT_Ele27_eta2p1_WPTight_Gsf || HLT_Ele27_eta2p1_WPLoose_Gsf;
      if (!(muon_triggers || electron_triggers)) continue;
   
      if (!genZll_selection()) continue;
      h_V_pT->Fill(GenV_P4.Pt());
      h_V_absY->Fill(fabs(GenV_P4.Rapidity()));
      Npassed++;
      

   }
   // Save on file
   TFile* file = new TFile("GenLevel_analyzer_MiniAODv2.root", "RECREATE");
   h_V_pT->Write();
   h_V_absY->Write();
   file->Close();
   std::cout << "Nevents = " << Nevents << " Npassed = " << Npassed << std::endl;
}

bool GenLevel_analyzer::genZll_selection()
{

   int lepton_flav = -1;
   int n_leptons = 0;
   int V_idx_temp = -1;
   int V_idx = -1, lep1_idx = -1, lep2_idx = -1;
   
   // loop on GenPart and pick up the Z->ll events
   for (int i = 0; (i < nGenPart); i++){
      if(debug_) std::cout << "GenPart_pdgId[" << i << "] = " << GenPart_pdgId[i] << "   MotherIdx["<< i<<"] = " << GenPart_genPartIdxMother[i] << std::endl;
      // search for 2 electrons or 2 muons from the Z decay
      if (!(fabs(GenPart_pdgId[i]) == isEle || fabs(GenPart_pdgId[i]) == isMuon) || GenPart_pdgId[GenPart_genPartIdxMother[i]] != isZ) continue;
      lepton_flav = GenPart_pdgId[i];
      V_idx_temp = GenPart_genPartIdxMother[i];
      // check if the lepton is in the acceptance
      if (debug_) std::cout << "l1 pT = " << GenPart_pt[i] << " l1 eta = " << GenPart_eta[i] << std::endl;
      if (GenPart_pt[i] < minLepton_pT_ || fabs(GenPart_eta[i]) > maxLepton_eta_) continue;
      // check if there is another lepton from the Z decay
      for (int j = i+1; (j < nGenPart); j++){
         if (GenPart_pdgId[j] != -lepton_flav || GenPart_pdgId[GenPart_genPartIdxMother[j]] != isZ || GenPart_genPartIdxMother[j] != V_idx_temp) continue;
         if (debug_) std::cout << "l2 pT = " << GenPart_pt[j] << " l2 eta = " << GenPart_eta[j] << std::endl;
         if (GenPart_pt[j] < minLepton_pT_ || fabs(GenPart_eta[j]) > maxLepton_eta_) continue;
         if (fabs( GenPart_mass[GenPart_genPartIdxMother[j]] - Z_MASS) > Vmass_tolerance) continue;
         if (GenPart_pt[V_idx_temp] > maxZ_pT_) continue;
         lep1_idx = i;
         lep2_idx = j;
         V_idx = V_idx_temp;
         
         if (V_idx > 0) break;
      }
      if (V_idx > 0) break;
      V_idx_temp = -1;
      if (debug_) std::cout << "lepton_flav 1 = " << lepton_flav << " lep1_idx = " << lep1_idx << " lep2_idx = " << lep2_idx << " V_idx = " << V_idx << std::endl;
   }// loop on GenPart
   if (lep1_idx != -1 && lep2_idx != -1 && V_idx != -1){

      GenV_P4.SetPt(GenPart_pt[V_idx]); GenV_P4.SetEta(GenPart_eta[V_idx]); GenV_P4.SetPhi(GenPart_phi[V_idx]); GenV_P4.SetM(GenPart_mass[V_idx]);
      if (GenPart_pt[lep2_idx] > GenPart_pt[lep1_idx]){
         int tmp = lep1_idx;
         lep1_idx = lep2_idx;
         lep2_idx = tmp;
      }
      Genl1_P4.SetPt(GenPart_pt[lep1_idx]); Genl1_P4.SetEta(GenPart_eta[lep1_idx]); Genl1_P4.SetPhi(GenPart_phi[lep1_idx]); Genl1_P4.SetM(GenPart_mass[lep1_idx]);
      Genl2_P4.SetPt(GenPart_pt[lep2_idx]); Genl2_P4.SetEta(GenPart_eta[lep2_idx]); Genl2_P4.SetPhi(GenPart_phi[lep2_idx]); Genl2_P4.SetM(GenPart_mass[lep2_idx]);
   }

   return (lep1_idx != -1 && lep2_idx != -1 && V_idx != -1); 
}
