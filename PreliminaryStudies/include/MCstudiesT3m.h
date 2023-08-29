#ifndef MCstudiesT3m_h
#define MCstudiesT3m_h

#include "include/MCTau3Mu_base.h"

#define _USE_MATH_DEFINES
#include <cmath>
#include "TH1F.h"


class MCstudiesT3m : public MCTau3Mu_base{

  public:
   MCstudiesT3m(TTree *tree=0, const TString & tags = "2022_preEE");
   virtual ~MCstudiesT3m();

   void    Loop();
   int     MCtruthMatching(const bool verbose = false);
   bool    RecoPartFillP4(const int TauIdx);

   void    saveOutput();
    
   private:
   
   // particle P4 
   ROOT::Math::PtEtaPhiMVector RecoW_P4;
   ROOT::Math::PtEtaPhiMVector RecoTau_P4, RecoMET_P4;
   ROOT::Math::PtEtaPhiMVector RecoMu1_P4, RecoMu2_P4, RecoMu3_P4;

   // MC matching tau candidate
   int TauTo3Mu_MCmatch_idx;

   // [OUTPUT]
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
   TH1F* h_gen_MuLeading_pT = new TH1F("gen_MuLeading_pT", "", 50, 0, 50);
   TH1F* h_gen_MuSubLeading_pT = new TH1F("gen_MuSubLeading_pT", "", 50, 0, 50);
   TH1F* h_gen_MuTrailing_pT = new TH1F("gen_MuTrailing_pT", "", 50, 0, 50);

   TH1F* h_MuLeading_pT = new TH1F("MuLeading_pT", "", 50, 0, 50);
   TH1F* h_MuSubLeading_pT = new TH1F("MuSubLeading_pT", "", 50, 0, 50);
   TH1F* h_MuTrailing_pT = new TH1F("MuTrailing_pT", "", 50, 0, 50);

   TH1F* h_MuLeading_eta = new TH1F("MuLeading_eta", "", 35, -3.5, 3.5);
   TH1F* h_MuSubLeading_eta = new TH1F("MuSubLeading_eta", "", 35, -3.5, 3.5);
   TH1F* h_MuTrailing_eta = new TH1F("MuTrailing_eta", "", 35, -3.5, 3.5);

   TH1F* h_Mu_Dz12 = new TH1F("Mu_Dz12", "", 40, 0, 0.4);
   TH1F* h_Mu_Dz23 = new TH1F("Mu_Dz23", "", 40, 0, 0.4);
   TH1F* h_Mu_Dz13 = new TH1F("Mu_Dz13", "", 40, 0, 0.4);

  // Tau
   TH1F* h_gen_Tau_M = new TH1F("gen_Tau_M", "", 50, 1.6, 2.0);
   TH1F* h_gen_Tau_pT = new TH1F("gen_Tau_pT", "", 40, 10, 100);
   TH1F* h_gen_Tau_eta = new TH1F("gen_Tau_eta", "", 70, -3.5, 3.5);

   TH1F* h_nTau = new TH1F("nTau", "", 10, -0.5, 9.5);
   TH1F* h_Tau_fit_M = new TH1F("Tau_fit_M", "", 50, 1.6, 2.0);
   TH1F* h_Tau_fit_pT = new TH1F("Tau_fit_pT", "", 40, 10, 100);
   TH1F* h_Tau_fit_eta = new TH1F("Tau_fit_eta", "", 70, -3.5, 3.5);
   TH1F* h_Tau_relIso = new TH1F("Tau_relIso", "", 60, 0, 3);
   TH1F* h_Tau_fitNoVtx_M = new TH1F("Tau_fitNoVtx_M", "", 50, 1.6, 2.0);
   TH1F* h_diMuon_Mass = new TH1F("diMuon_Mass", "", 200, 0., 95);

   TH1F* h_LxySign_BSvtx = new TH1F("LxySign_BSvtx", "", 40, 0, 30);
   TH1F* h_Tau_Mt = new TH1F("Tau_Mt", "", 50, 0, 200);
   TH1F* h_Tau_Pvtx = new TH1F("Tau_Pvtx", "", 40, 0., 1.);
   TH1F* h_Tau_cosAlpha_BS = new TH1F("Tau_cosAlpha_BS", "", 100, -1, 1);

   // MET
   TH1F* h_diffGenPuppiMET = new TH1F("diffGenPuppiMET", "", 50, -50, 50);
   TH1F* h_diffLongGenPuppiMET = new TH1F("diffLongGenPuppiMET", "", 50, -50, 50);
   TH1F* h_ratioLongGenPuppiMET = new TH1F("ratioLongGenPuppiMET", "", 50, -2.0, 3);
   TH1F* h_ratioPerpGenPuppiMET = new TH1F("ratioPerpGenPuppiMET", "", 50, 0., 2);
   
   TH1F* h_diffGenDeepMET = new TH1F("diffGenDeepMET", "", 50, -50, 50);
   TH1F* h_diffLongGenDeepMET = new TH1F("diffLongGenDeepMET", "", 50, -50, 50);
   TH1F* h_ratioLongGenDeepMET = new TH1F("ratioLongGenDeepMET", "", 50, -2.0, 3);
   TH1F* h_ratioPerpGenDeepMET = new TH1F("ratioPerpGenDeepMET", "", 50, 0., 2);

   TH1F* h_DPhi_TauDeepMET = new TH1F("DPhi_TauDeepMET", "", 50, 0, 3.14);
   TH1F* h_TauPt_DeepMET = new TH1F("TauPt_DeepMET", "", 60, 0, 6.);
   TH1F* h_DPhi_TauPunziMET = new TH1F("DPhi_TauPunziMET", "", 50, 0, 3.14);
   TH1F* h_TauPt_PunziMET = new TH1F("TauPt_PunziMET", "", 60, 0, 6.);

   TH1F* h_missPz_min = new TH1F("missPz_min", "", 100, -300, 300);
   TH1F* h_missPz_max = new TH1F("missPz_max", "", 100, 0, 4000);


  // W cand
  TH1F* h_W_pT = new TH1F("W_pT", "", 40, 0, 150);
  TH1F* h_gen_W_pT = new TH1F("gen_W_pT", "", 40, 0, 150);



};
#endif
