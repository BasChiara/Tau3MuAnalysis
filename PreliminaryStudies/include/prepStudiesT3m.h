#ifndef prepStudiesT3m_h
#define prepStudiesT3m_h

#include "../include/Tau3Mu_base.h"

class prepStudiesT3m : public Tau3Mu_base{

public:
 prepStudiesT3m(TTree *tree=0, const TString & tags = "2022_preEE");
 virtual ~prepStudiesT3m(){}

 void    Loop();
 void    saveOutput();

private:
 TString tags_;

 TString outFilePath_;
 TFile*  outFile_;

   // TH1
   // muond ID
   TH1F* h_Mu_MediumID = new TH1F("Mu_MediumID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_SoftID   = new TH1F("Mu_SoftID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_SoftID_BS= new TH1F("Mu_SoftID_BS", "", 2, -0.5, 1.5);
   TH1F* h_Mu_TightID  = new TH1F("Mu_TightID", "", 2, -0.5, 1.5);
   TH1F* h_Mu_TightID_BS= new TH1F("Mu_TightID_BS", "", 2, -0.5, 1.5);

   // muons kinematics
   TH1F* h_MuLeading_pT = new TH1F("MuLeading_pT", "", 25, 0, 50);
   TH1F* h_MuSubLeading_pT = new TH1F("MuSubLeading_pT", "", 25, 0, 50);
   TH1F* h_MuTrailing_pT = new TH1F("MuTrailing_pT", "", 25, 0, 50);

   TH1F* h_MuLeading_eta = new TH1F("MuLeading_eta", "", 14, -3.5, 3.5);
   TH1F* h_MuSubLeading_eta = new TH1F("MuSubLeading_eta", "", 14, -3.5, 3.5);
   TH1F* h_MuTrailing_eta = new TH1F("MuTrailing_eta", "", 14, -3.5, 3.5);

  // Tau
   TH1F* h_nTau = new TH1F("nTau", "", 10, -0.5, 9.5);
   TH1F* h_Tau_fit_M = new TH1F("Tau_fit_M", "", 40, 1.6, 2.0);
   TH1F* h_Tau_fit_pT = new TH1F("Tau_fit_pT", "", 90, 10, 100);
   TH1F* h_Tau_relIso = new TH1F("Tau_relIso", "", 30, 0, 3);
   TH1F* h_Tau_fitNoVtx_M = new TH1F("Tau_fitNoVtx_M", "", 40, 1.6, 2.0);
   TH1F* h_LxySign_BSvtx = new TH1F("LxySign_BSvtx", "", 60, 0, 30);
   TH1F* h_diMuon_Mass = new TH1F("diMuon_Mass", "", 200, 0., 95);


};


#endif