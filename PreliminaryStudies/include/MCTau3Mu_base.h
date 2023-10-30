//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Sep 20 11:50:18 2023 by ROOT version 6.24/07
// from TTree Events/Events
// found on file: /eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2023Sep16/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2022/230916_122436/0000/tau3muNANO_mc_2023Sep16_10.root
//////////////////////////////////////////////////////////

#ifndef MCTau3Mu_base_h
#define MCTau3Mu_base_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "Math/Vector4D.h"
#include "Math/GenVector/VectorUtil.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

// Header file for the classes stored in the TTree if any.

class MCTau3Mu_base {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   UInt_t          run;
   UInt_t          luminosityBlock;
   ULong64_t       event;
   UInt_t          bunchCrossing;
   UInt_t          nTauTo3Mu;
   Float_t         TauTo3Mu_CosAlpha2D_LxyP3mu[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_Lxy_3muVtxBS[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_absIsolation[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_dZmu12[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_dZmu13[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_dZmu23[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_diMuVtxFit_bestMass[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_diMuVtxFit_bestProb[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_errLxy_3muVtxBS[3];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_fitted_eta[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_fitted_mass[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_fitted_mass_err2[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_fitted_phi[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_fitted_pt[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_iso_ptChargedForHLT[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_iso_ptChargedFromPU[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_iso_ptChargedFromPV[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_iso_ptPhotons[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu12_DCA[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu12_vtxFitProb[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu13_DCA[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu13_vtxFitProb[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu1_dr[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu1_eta[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu1_phi[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu1_pt[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu23_DCA[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu23_vtxFitProb[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu2_dr[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu2_eta[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu2_phi[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu2_pt[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu3_dr[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu3_eta[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu3_phi[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_mu3_pt[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_sigLxy_3muVtxBS[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_vtx_Ndof[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_vtx_chi2[15];   //[nTauTo3Mu]
   Float_t         TauTo3Mu_vtx_prob[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_charge[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_diMuVtxFit_toVeto[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_charge[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_idx[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu1_trackQuality[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_charge[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_idx[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu2_trackQuality[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_charge[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_idx[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_mu3_trackQuality[15];   //[nTauTo3Mu]
   Int_t           TauTo3Mu_vtx_isValid[15];   //[nTauTo3Mu]
   UInt_t          nTauPlusMET;
   Float_t         TauPlusMET_DeepMET_pt[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_DeepMETmaxPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_DeepMETminPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Deep_eta[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Deep_phi[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Deep_pt[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_MET_pt[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_METmaxPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_METminPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_PuppiMET_pt[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_PuppiMETmaxPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_PuppiMETminPz[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Puppi_eta[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Puppi_phi[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Puppi_pt[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Tau_Deep_mT[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Tau_Puppi_mT[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_Tau_mT[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_eta[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_mass[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_phi[15];   //[nTauPlusMET]
   Float_t         TauPlusMET_pt[15];   //[nTauPlusMET]
   Int_t           TauPlusMET_charge[15];   //[nTauPlusMET]
   Float_t         BeamSpot_sigmaZ;
   Float_t         BeamSpot_sigmaZError;
   Float_t         BeamSpot_z;
   Float_t         BeamSpot_zError;
   Char_t          BeamSpot_type;
   Float_t         CaloMET_phi;
   Float_t         CaloMET_pt;
   Float_t         CaloMET_sumEt;
   Float_t         ChsMET_phi;
   Float_t         ChsMET_pt;
   Float_t         ChsMET_sumEt;
   Float_t         DeepMETResolutionTune_phi;
   Float_t         DeepMETResolutionTune_pt;
   Float_t         DeepMETResponseTune_phi;
   Float_t         DeepMETResponseTune_pt;
   UInt_t          nGenPart;
   Float_t         GenPart_eta[50];   //[nGenPart]
   Float_t         GenPart_mass[50];   //[nGenPart]
   Float_t         GenPart_phi[50];   //[nGenPart]
   Float_t         GenPart_pt[50];   //[nGenPart]
   Float_t         GenPart_vx[50];   //[nGenPart]
   Float_t         GenPart_vy[50];   //[nGenPart]
   Float_t         GenPart_vz[50];   //[nGenPart]
   Int_t           GenPart_genPartIdxMother[50];   //[nGenPart]
   Int_t           GenPart_pdgId[50];   //[nGenPart]
   Int_t           GenPart_status[50];   //[nGenPart]
   Int_t           GenPart_statusFlags[50];   //[nGenPart]
   Float_t         Generator_binvar;
   Float_t         Generator_scalePDF;
   Float_t         Generator_weight;
   Float_t         Generator_x1;
   Float_t         Generator_x2;
   Float_t         Generator_xpdf1;
   Float_t         Generator_xpdf2;
   Int_t           Generator_id1;
   Int_t           Generator_id2;
   Float_t         genWeight;
   UInt_t          nPSWeight;
   Float_t         PSWeight[10];   //[nPSWeight]
   Float_t         GenMET_phi;
   Float_t         GenMET_pt;
   Float_t         MET_MetUnclustEnUpDeltaX;
   Float_t         MET_MetUnclustEnUpDeltaY;
   Float_t         MET_covXX;
   Float_t         MET_covXY;
   Float_t         MET_covYY;
   Float_t         MET_phi;
   Float_t         MET_pt;
   Float_t         MET_significance;
   Float_t         MET_sumEt;
   Float_t         MET_sumPtUnclustered;
   UInt_t          nMuon;
   Float_t         Muon_dZpv[30];   //[nMuon]
   Float_t         Muon_err_dZpv[30];   //[nMuon]
   Float_t         Muon_phi[30];   //[nMuon]
   Float_t         Muon_pt[30];   //[nMuon]
   Float_t         Muon_z[30];   //[nMuon]
   Int_t           Muon_charge[30];   //[nMuon]
   Int_t           Muon_isSoft_BS[30];   //[nMuon]
   Int_t           Muon_isTight_BS[30];   //[nMuon]
   Int_t           Muon_trackQuality[30];   //[nMuon]
   Bool_t          Muon_isGlobal[30];   //[nMuon]
   Bool_t          Muon_isLoose[30];   //[nMuon]
   Bool_t          Muon_isMedium[30];   //[nMuon]
   Bool_t          Muon_isPFcand[30];   //[nMuon]
   Bool_t          Muon_isSoft[30];   //[nMuon]
   Bool_t          Muon_isTight[30];   //[nMuon]
   Bool_t          Muon_isTracker[30];   //[nMuon]
   Float_t         Pileup_nTrueInt;
   Float_t         Pileup_pudensity;
   Float_t         Pileup_gpudensity;
   Int_t           Pileup_nPU;
   Int_t           Pileup_sumEOOT;
   Int_t           Pileup_sumLOOT;
   Float_t         PuppiMET_phi;
   Float_t         PuppiMET_phiJERDown;
   Float_t         PuppiMET_phiJERUp;
   Float_t         PuppiMET_phiJESDown;
   Float_t         PuppiMET_phiJESUp;
   Float_t         PuppiMET_phiUnclusteredDown;
   Float_t         PuppiMET_phiUnclusteredUp;
   Float_t         PuppiMET_pt;
   Float_t         PuppiMET_ptJERDown;
   Float_t         PuppiMET_ptJERUp;
   Float_t         PuppiMET_ptJESDown;
   Float_t         PuppiMET_ptJESUp;
   Float_t         PuppiMET_ptUnclusteredDown;
   Float_t         PuppiMET_ptUnclusteredUp;
   Float_t         PuppiMET_sumEt;
   Float_t         RawMET_phi;
   Float_t         RawMET_pt;
   Float_t         RawMET_sumEt;
   Float_t         RawPuppiMET_phi;
   Float_t         RawPuppiMET_pt;
   Float_t         RawPuppiMET_sumEt;
   Float_t         Rho_fixedGridRhoAll;
   Float_t         Rho_fixedGridRhoFastjetAll;
   Float_t         Rho_fixedGridRhoFastjetCentral;
   Float_t         Rho_fixedGridRhoFastjetCentralCalo;
   Float_t         Rho_fixedGridRhoFastjetCentralChargedPileUp;
   Float_t         Rho_fixedGridRhoFastjetCentralNeutral;
   Float_t         TkMET_phi;
   Float_t         TkMET_pt;
   Float_t         TkMET_sumEt;
   Int_t           HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;
   Int_t           HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;
   Int_t           HLT_DoubleMu4_3_LowMass;
   UInt_t          nTrigObj;
   Float_t         TrigObj_pt[10];   //[nTrigObj]
   Float_t         TrigObj_eta[10];   //[nTrigObj]
   Float_t         TrigObj_phi[10];   //[nTrigObj]
   Int_t           TrigObj_id[10];   //[nTrigObj]
   UInt_t          nOtherPV;
   Float_t         OtherPV_z[3];   //[nOtherPV]
   Float_t         OtherPV_score[3];   //[nOtherPV]
   Float_t         PV_ndof;
   Float_t         PV_x;
   Float_t         PV_y;
   Float_t         PV_z;
   Float_t         PV_chi2;
   Float_t         PV_score;
   Int_t           PV_npvs;
   Int_t           PV_npvsGood;
   UInt_t          nSV;
   Float_t         SV_dlen[15];   //[nSV]
   Float_t         SV_dlenSig[15];   //[nSV]
   Float_t         SV_dxy[15];   //[nSV]
   Float_t         SV_dxySig[15];   //[nSV]
   Float_t         SV_pAngle[15];   //[nSV]
   Int_t           SV_charge[15];   //[nSV]
   Int_t           Muon_genPartIdx[30];   //[nMuon]
   Int_t           Muon_genPartFlav[30];   //[nMuon]
   Float_t         SV_chi2[15];   //[nSV]
   Float_t         SV_eta[15];   //[nSV]
   Float_t         SV_mass[15];   //[nSV]
   Float_t         SV_ndof[15];   //[nSV]
   Float_t         SV_phi[15];   //[nSV]
   Float_t         SV_pt[15];   //[nSV]
   Float_t         SV_x[15];   //[nSV]
   Float_t         SV_y[15];   //[nSV]
   Float_t         SV_z[15];   //[nSV]
   UChar_t         SV_ntracks[15];   //[nSV]

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_luminosityBlock;   //!
   TBranch        *b_event;   //!
   TBranch        *b_bunchCrossing;   //!
   TBranch        *b_nTauTo3Mu;   //!
   TBranch        *b_TauTo3Mu_CosAlpha2D_LxyP3mu;   //!
   TBranch        *b_TauTo3Mu_Lxy_3muVtxBS;   //!
   TBranch        *b_TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr;   //!
   TBranch        *b_TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr;   //!
   TBranch        *b_TauTo3Mu_absIsolation;   //!
   TBranch        *b_TauTo3Mu_dZmu12;   //!
   TBranch        *b_TauTo3Mu_dZmu13;   //!
   TBranch        *b_TauTo3Mu_dZmu23;   //!
   TBranch        *b_TauTo3Mu_diMuVtxFit_bestMass;   //!
   TBranch        *b_TauTo3Mu_diMuVtxFit_bestProb;   //!
   TBranch        *b_TauTo3Mu_errLxy_3muVtxBS;   //!
   TBranch        *b_TauTo3Mu_fitted_eta;   //!
   TBranch        *b_TauTo3Mu_fitted_mass;   //!
   TBranch        *b_TauTo3Mu_fitted_mass_err2;   //!
   TBranch        *b_TauTo3Mu_fitted_phi;   //!
   TBranch        *b_TauTo3Mu_fitted_pt;   //!
   TBranch        *b_TauTo3Mu_iso_ptChargedForHLT;   //!
   TBranch        *b_TauTo3Mu_iso_ptChargedFromPU;   //!
   TBranch        *b_TauTo3Mu_iso_ptChargedFromPV;   //!
   TBranch        *b_TauTo3Mu_iso_ptPhotons;   //!
   TBranch        *b_TauTo3Mu_mu12_DCA;   //!
   TBranch        *b_TauTo3Mu_mu12_vtxFitProb;   //!
   TBranch        *b_TauTo3Mu_mu13_DCA;   //!
   TBranch        *b_TauTo3Mu_mu13_vtxFitProb;   //!
   TBranch        *b_TauTo3Mu_mu1_dr;   //!
   TBranch        *b_TauTo3Mu_mu1_eta;   //!
   TBranch        *b_TauTo3Mu_mu1_phi;   //!
   TBranch        *b_TauTo3Mu_mu1_pt;   //!
   TBranch        *b_TauTo3Mu_mu23_DCA;   //!
   TBranch        *b_TauTo3Mu_mu23_vtxFitProb;   //!
   TBranch        *b_TauTo3Mu_mu2_dr;   //!
   TBranch        *b_TauTo3Mu_mu2_eta;   //!
   TBranch        *b_TauTo3Mu_mu2_phi;   //!
   TBranch        *b_TauTo3Mu_mu2_pt;   //!
   TBranch        *b_TauTo3Mu_mu3_dr;   //!
   TBranch        *b_TauTo3Mu_mu3_eta;   //!
   TBranch        *b_TauTo3Mu_mu3_phi;   //!
   TBranch        *b_TauTo3Mu_mu3_pt;   //!
   TBranch        *b_TauTo3Mu_sigLxy_3muVtxBS;   //!
   TBranch        *b_TauTo3Mu_vtx_Ndof;   //!
   TBranch        *b_TauTo3Mu_vtx_chi2;   //!
   TBranch        *b_TauTo3Mu_vtx_prob;   //!
   TBranch        *b_TauTo3Mu_charge;   //!
   TBranch        *b_TauTo3Mu_diMuVtxFit_toVeto;   //!
   TBranch        *b_TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;   //!
   TBranch        *b_TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;   //!
   TBranch        *b_TauTo3Mu_mu1_charge;   //!
   TBranch        *b_TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass;   //!
   TBranch        *b_TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;   //!
   TBranch        *b_TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;   //!
   TBranch        *b_TauTo3Mu_mu1_idx;   //!
   TBranch        *b_TauTo3Mu_mu1_trackQuality;   //!
   TBranch        *b_TauTo3Mu_mu2_charge;   //!
   TBranch        *b_TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass;   //!
   TBranch        *b_TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;   //!
   TBranch        *b_TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;   //!
   TBranch        *b_TauTo3Mu_mu2_idx;   //!
   TBranch        *b_TauTo3Mu_mu2_trackQuality;   //!
   TBranch        *b_TauTo3Mu_mu3_charge;   //!
   TBranch        *b_TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass;   //!
   TBranch        *b_TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;   //!
   TBranch        *b_TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;   //!
   TBranch        *b_TauTo3Mu_mu3_idx;   //!
   TBranch        *b_TauTo3Mu_mu3_trackQuality;   //!
   TBranch        *b_TauTo3Mu_vtx_isValid;   //!
   TBranch        *b_nTauPlusMET;   //!
   TBranch        *b_TauPlusMET_DeepMET_pt;   //!
   TBranch        *b_TauPlusMET_DeepMETmaxPz;   //!
   TBranch        *b_TauPlusMET_DeepMETminPz;   //!
   TBranch        *b_TauPlusMET_Deep_eta;   //!
   TBranch        *b_TauPlusMET_Deep_phi;   //!
   TBranch        *b_TauPlusMET_Deep_pt;   //!
   TBranch        *b_TauPlusMET_MET_pt;   //!
   TBranch        *b_TauPlusMET_METmaxPz;   //!
   TBranch        *b_TauPlusMET_METminPz;   //!
   TBranch        *b_TauPlusMET_PuppiMET_pt;   //!
   TBranch        *b_TauPlusMET_PuppiMETmaxPz;   //!
   TBranch        *b_TauPlusMET_PuppiMETminPz;   //!
   TBranch        *b_TauPlusMET_Puppi_eta;   //!
   TBranch        *b_TauPlusMET_Puppi_phi;   //!
   TBranch        *b_TauPlusMET_Puppi_pt;   //!
   TBranch        *b_TauPlusMET_Tau_Deep_mT;   //!
   TBranch        *b_TauPlusMET_Tau_Puppi_mT;   //!
   TBranch        *b_TauPlusMET_Tau_mT;   //!
   TBranch        *b_TauPlusMET_eta;   //!
   TBranch        *b_TauPlusMET_mass;   //!
   TBranch        *b_TauPlusMET_phi;   //!
   TBranch        *b_TauPlusMET_pt;   //!
   TBranch        *b_TauPlusMET_charge;   //!
   TBranch        *b_BeamSpot_sigmaZ;   //!
   TBranch        *b_BeamSpot_sigmaZError;   //!
   TBranch        *b_BeamSpot_z;   //!
   TBranch        *b_BeamSpot_zError;   //!
   TBranch        *b_BeamSpot_type;   //!
   TBranch        *b_CaloMET_phi;   //!
   TBranch        *b_CaloMET_pt;   //!
   TBranch        *b_CaloMET_sumEt;   //!
   TBranch        *b_ChsMET_phi;   //!
   TBranch        *b_ChsMET_pt;   //!
   TBranch        *b_ChsMET_sumEt;   //!
   TBranch        *b_DeepMETResolutionTune_phi;   //!
   TBranch        *b_DeepMETResolutionTune_pt;   //!
   TBranch        *b_DeepMETResponseTune_phi;   //!
   TBranch        *b_DeepMETResponseTune_pt;   //!
   TBranch        *b_nGenPart;   //!
   TBranch        *b_GenPart_eta;   //!
   TBranch        *b_GenPart_mass;   //!
   TBranch        *b_GenPart_phi;   //!
   TBranch        *b_GenPart_pt;   //!
   TBranch        *b_GenPart_vx;   //!
   TBranch        *b_GenPart_vy;   //!
   TBranch        *b_GenPart_vz;   //!
   TBranch        *b_GenPart_genPartIdxMother;   //!
   TBranch        *b_GenPart_pdgId;   //!
   TBranch        *b_GenPart_status;   //!
   TBranch        *b_GenPart_statusFlags;   //!
   TBranch        *b_Generator_binvar;   //!
   TBranch        *b_Generator_scalePDF;   //!
   TBranch        *b_Generator_weight;   //!
   TBranch        *b_Generator_x1;   //!
   TBranch        *b_Generator_x2;   //!
   TBranch        *b_Generator_xpdf1;   //!
   TBranch        *b_Generator_xpdf2;   //!
   TBranch        *b_Generator_id1;   //!
   TBranch        *b_Generator_id2;   //!
   TBranch        *b_genWeight;   //!
   TBranch        *b_nPSWeight;   //!
   TBranch        *b_PSWeight;   //!
   TBranch        *b_GenMET_phi;   //!
   TBranch        *b_GenMET_pt;   //!
   TBranch        *b_MET_MetUnclustEnUpDeltaX;   //!
   TBranch        *b_MET_MetUnclustEnUpDeltaY;   //!
   TBranch        *b_MET_covXX;   //!
   TBranch        *b_MET_covXY;   //!
   TBranch        *b_MET_covYY;   //!
   TBranch        *b_MET_phi;   //!
   TBranch        *b_MET_pt;   //!
   TBranch        *b_MET_significance;   //!
   TBranch        *b_MET_sumEt;   //!
   TBranch        *b_MET_sumPtUnclustered;   //!
   TBranch        *b_nMuon;   //!
   TBranch        *b_Muon_dZpv;   //!
   TBranch        *b_Muon_err_dZpv;   //!
   TBranch        *b_Muon_phi;   //!
   TBranch        *b_Muon_pt;   //!
   TBranch        *b_Muon_z;   //!
   TBranch        *b_Muon_charge;   //!
   TBranch        *b_Muon_isSoft_BS;   //!
   TBranch        *b_Muon_isTight_BS;   //!
   TBranch        *b_Muon_trackQuality;   //!
   TBranch        *b_Muon_isGlobal;   //!
   TBranch        *b_Muon_isLoose;   //!
   TBranch        *b_Muon_isMedium;   //!
   TBranch        *b_Muon_isPFcand;   //!
   TBranch        *b_Muon_isSoft;   //!
   TBranch        *b_Muon_isTight;   //!
   TBranch        *b_Muon_isTracker;   //!
   TBranch        *b_Pileup_nTrueInt;   //!
   TBranch        *b_Pileup_pudensity;   //!
   TBranch        *b_Pileup_gpudensity;   //!
   TBranch        *b_Pileup_nPU;   //!
   TBranch        *b_Pileup_sumEOOT;   //!
   TBranch        *b_Pileup_sumLOOT;   //!
   TBranch        *b_PuppiMET_phi;   //!
   TBranch        *b_PuppiMET_phiJERDown;   //!
   TBranch        *b_PuppiMET_phiJERUp;   //!
   TBranch        *b_PuppiMET_phiJESDown;   //!
   TBranch        *b_PuppiMET_phiJESUp;   //!
   TBranch        *b_PuppiMET_phiUnclusteredDown;   //!
   TBranch        *b_PuppiMET_phiUnclusteredUp;   //!
   TBranch        *b_PuppiMET_pt;   //!
   TBranch        *b_PuppiMET_ptJERDown;   //!
   TBranch        *b_PuppiMET_ptJERUp;   //!
   TBranch        *b_PuppiMET_ptJESDown;   //!
   TBranch        *b_PuppiMET_ptJESUp;   //!
   TBranch        *b_PuppiMET_ptUnclusteredDown;   //!
   TBranch        *b_PuppiMET_ptUnclusteredUp;   //!
   TBranch        *b_PuppiMET_sumEt;   //!
   TBranch        *b_RawMET_phi;   //!
   TBranch        *b_RawMET_pt;   //!
   TBranch        *b_RawMET_sumEt;   //!
   TBranch        *b_RawPuppiMET_phi;   //!
   TBranch        *b_RawPuppiMET_pt;   //!
   TBranch        *b_RawPuppiMET_sumEt;   //!
   TBranch        *b_Rho_fixedGridRhoAll;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetAll;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetCentral;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetCentralCalo;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetCentralChargedPileUp;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetCentralNeutral;   //!
   TBranch        *b_TkMET_phi;   //!
   TBranch        *b_TkMET_pt;   //!
   TBranch        *b_TkMET_sumEt;   //!
   TBranch        *b_HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1;   //!
   TBranch        *b_HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15;   //!
   TBranch        *b_HLT_DoubleMu4_3_LowMass;   //!
   TBranch        *b_nTrigObj;   //!
   TBranch        *b_TrigObj_pt;   //!
   TBranch        *b_TrigObj_eta;   //!
   TBranch        *b_TrigObj_phi;   //!
   TBranch        *b_TrigObj_id;   //!
   TBranch        *b_nOtherPV;   //!
   TBranch        *b_OtherPV_z;   //!
   TBranch        *b_OtherPV_score;   //!
   TBranch        *b_PV_ndof;   //!
   TBranch        *b_PV_x;   //!
   TBranch        *b_PV_y;   //!
   TBranch        *b_PV_z;   //!
   TBranch        *b_PV_chi2;   //!
   TBranch        *b_PV_score;   //!
   TBranch        *b_PV_npvs;   //!
   TBranch        *b_PV_npvsGood;   //!
   TBranch        *b_nSV;   //!
   TBranch        *b_SV_dlen;   //!
   TBranch        *b_SV_dlenSig;   //!
   TBranch        *b_SV_dxy;   //!
   TBranch        *b_SV_dxySig;   //!
   TBranch        *b_SV_pAngle;   //!
   TBranch        *b_SV_charge;   //!
   TBranch        *b_Muon_genPartIdx;   //!
   TBranch        *b_Muon_genPartFlav;   //!
   TBranch        *b_SV_chi2;   //!
   TBranch        *b_SV_eta;   //!
   TBranch        *b_SV_mass;   //!
   TBranch        *b_SV_ndof;   //!
   TBranch        *b_SV_phi;   //!
   TBranch        *b_SV_pt;   //!
   TBranch        *b_SV_x;   //!
   TBranch        *b_SV_y;   //!
   TBranch        *b_SV_z;   //!
   TBranch        *b_SV_ntracks;   //!

   MCTau3Mu_base(TTree *tree=0, const TString& tags = "MC_2022");
   virtual ~MCTau3Mu_base();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   // custom
   virtual void     GenPartFillP4();

   // I/O
   TString tags_;

   // particle P4 
   ROOT::Math::PtEtaPhiMVector GenW_P4;
   ROOT::Math::PtEtaPhiMVector GenTau_P4, GenNu_P4;
   ROOT::Math::PtEtaPhiMVector GenMu1_P4, GenMu2_P4, GenMu3_P4;
};

#endif

#ifdef MCTau3Mu_base_cxx
MCTau3Mu_base::MCTau3Mu_base(TTree *tree, const TString& tags) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2023Sep16/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2022/230916_122436/0000/tau3muNANO_mc_2023Sep16_10.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano2022_2023Sep16/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/crab_WnuTau3Mu_2022/230916_122436/0000/tau3muNANO_mc_2023Sep16_10.root");
      }
      f->GetObject("Events",tree);

   }
   tags_ = tags;
   Init(tree);
}

MCTau3Mu_base::~MCTau3Mu_base()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t MCTau3Mu_base::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MCTau3Mu_base::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void MCTau3Mu_base::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("luminosityBlock", &luminosityBlock, &b_luminosityBlock);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("bunchCrossing", &bunchCrossing, &b_bunchCrossing);
   fChain->SetBranchAddress("nTauTo3Mu", &nTauTo3Mu, &b_nTauTo3Mu);
   fChain->SetBranchAddress("TauTo3Mu_CosAlpha2D_LxyP3mu", TauTo3Mu_CosAlpha2D_LxyP3mu, &b_TauTo3Mu_CosAlpha2D_LxyP3mu);
   fChain->SetBranchAddress("TauTo3Mu_Lxy_3muVtxBS", TauTo3Mu_Lxy_3muVtxBS, &b_TauTo3Mu_Lxy_3muVtxBS);
   fChain->SetBranchAddress("TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr", TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr, &b_TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr);
   fChain->SetBranchAddress("TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr", TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr, &b_TauTo3Mu_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr);
   fChain->SetBranchAddress("TauTo3Mu_absIsolation", TauTo3Mu_absIsolation, &b_TauTo3Mu_absIsolation);
   fChain->SetBranchAddress("TauTo3Mu_dZmu12", TauTo3Mu_dZmu12, &b_TauTo3Mu_dZmu12);
   fChain->SetBranchAddress("TauTo3Mu_dZmu13", TauTo3Mu_dZmu13, &b_TauTo3Mu_dZmu13);
   fChain->SetBranchAddress("TauTo3Mu_dZmu23", TauTo3Mu_dZmu23, &b_TauTo3Mu_dZmu23);
   fChain->SetBranchAddress("TauTo3Mu_diMuVtxFit_bestMass", TauTo3Mu_diMuVtxFit_bestMass, &b_TauTo3Mu_diMuVtxFit_bestMass);
   fChain->SetBranchAddress("TauTo3Mu_diMuVtxFit_bestProb", TauTo3Mu_diMuVtxFit_bestProb, &b_TauTo3Mu_diMuVtxFit_bestProb);
   fChain->SetBranchAddress("TauTo3Mu_errLxy_3muVtxBS", TauTo3Mu_errLxy_3muVtxBS, &b_TauTo3Mu_errLxy_3muVtxBS);
   fChain->SetBranchAddress("TauTo3Mu_fitted_eta", TauTo3Mu_fitted_eta, &b_TauTo3Mu_fitted_eta);
   fChain->SetBranchAddress("TauTo3Mu_fitted_mass", TauTo3Mu_fitted_mass, &b_TauTo3Mu_fitted_mass);
   fChain->SetBranchAddress("TauTo3Mu_fitted_mass_err2", TauTo3Mu_fitted_mass_err2, &b_TauTo3Mu_fitted_mass_err2);
   fChain->SetBranchAddress("TauTo3Mu_fitted_phi", TauTo3Mu_fitted_phi, &b_TauTo3Mu_fitted_phi);
   fChain->SetBranchAddress("TauTo3Mu_fitted_pt", TauTo3Mu_fitted_pt, &b_TauTo3Mu_fitted_pt);
   fChain->SetBranchAddress("TauTo3Mu_iso_ptChargedForHLT", TauTo3Mu_iso_ptChargedForHLT, &b_TauTo3Mu_iso_ptChargedForHLT);
   fChain->SetBranchAddress("TauTo3Mu_iso_ptChargedFromPU", TauTo3Mu_iso_ptChargedFromPU, &b_TauTo3Mu_iso_ptChargedFromPU);
   fChain->SetBranchAddress("TauTo3Mu_iso_ptChargedFromPV", TauTo3Mu_iso_ptChargedFromPV, &b_TauTo3Mu_iso_ptChargedFromPV);
   fChain->SetBranchAddress("TauTo3Mu_iso_ptPhotons", TauTo3Mu_iso_ptPhotons, &b_TauTo3Mu_iso_ptPhotons);
   fChain->SetBranchAddress("TauTo3Mu_mu12_DCA", TauTo3Mu_mu12_DCA, &b_TauTo3Mu_mu12_DCA);
   fChain->SetBranchAddress("TauTo3Mu_mu12_vtxFitProb", TauTo3Mu_mu12_vtxFitProb, &b_TauTo3Mu_mu12_vtxFitProb);
   fChain->SetBranchAddress("TauTo3Mu_mu13_DCA", TauTo3Mu_mu13_DCA, &b_TauTo3Mu_mu13_DCA);
   fChain->SetBranchAddress("TauTo3Mu_mu13_vtxFitProb", TauTo3Mu_mu13_vtxFitProb, &b_TauTo3Mu_mu13_vtxFitProb);
   fChain->SetBranchAddress("TauTo3Mu_mu1_dr", TauTo3Mu_mu1_dr, &b_TauTo3Mu_mu1_dr);
   fChain->SetBranchAddress("TauTo3Mu_mu1_eta", TauTo3Mu_mu1_eta, &b_TauTo3Mu_mu1_eta);
   fChain->SetBranchAddress("TauTo3Mu_mu1_phi", TauTo3Mu_mu1_phi, &b_TauTo3Mu_mu1_phi);
   fChain->SetBranchAddress("TauTo3Mu_mu1_pt", TauTo3Mu_mu1_pt, &b_TauTo3Mu_mu1_pt);
   fChain->SetBranchAddress("TauTo3Mu_mu2_dr", TauTo3Mu_mu2_dr, &b_TauTo3Mu_mu2_dr);
   fChain->SetBranchAddress("TauTo3Mu_mu2_eta", TauTo3Mu_mu2_eta, &b_TauTo3Mu_mu2_eta);
   fChain->SetBranchAddress("TauTo3Mu_mu2_phi", TauTo3Mu_mu2_phi, &b_TauTo3Mu_mu2_phi);
   fChain->SetBranchAddress("TauTo3Mu_mu2_pt", TauTo3Mu_mu2_pt, &b_TauTo3Mu_mu2_pt);
   fChain->SetBranchAddress("TauTo3Mu_mu3_dr", TauTo3Mu_mu3_dr, &b_TauTo3Mu_mu3_dr);
   fChain->SetBranchAddress("TauTo3Mu_mu3_eta", TauTo3Mu_mu3_eta, &b_TauTo3Mu_mu3_eta);
   fChain->SetBranchAddress("TauTo3Mu_mu3_phi", TauTo3Mu_mu3_phi, &b_TauTo3Mu_mu3_phi);
   fChain->SetBranchAddress("TauTo3Mu_mu3_pt", TauTo3Mu_mu3_pt, &b_TauTo3Mu_mu3_pt);
   fChain->SetBranchAddress("TauTo3Mu_sigLxy_3muVtxBS", TauTo3Mu_sigLxy_3muVtxBS, &b_TauTo3Mu_sigLxy_3muVtxBS);
   fChain->SetBranchAddress("TauTo3Mu_vtx_Ndof", TauTo3Mu_vtx_Ndof, &b_TauTo3Mu_vtx_Ndof);
   fChain->SetBranchAddress("TauTo3Mu_vtx_chi2", TauTo3Mu_vtx_chi2, &b_TauTo3Mu_vtx_chi2);
   fChain->SetBranchAddress("TauTo3Mu_vtx_prob", TauTo3Mu_vtx_prob, &b_TauTo3Mu_vtx_prob);
   fChain->SetBranchAddress("TauTo3Mu_charge", TauTo3Mu_charge, &b_TauTo3Mu_charge);
   fChain->SetBranchAddress("TauTo3Mu_diMuVtxFit_toVeto", TauTo3Mu_diMuVtxFit_toVeto, &b_TauTo3Mu_diMuVtxFit_toVeto);
   fChain->SetBranchAddress("TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1", TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1, &b_TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1);
   fChain->SetBranchAddress("TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15", TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15, &b_TauTo3Mu_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15);
   fChain->SetBranchAddress("TauTo3Mu_mu1_charge", TauTo3Mu_mu1_charge, &b_TauTo3Mu_mu1_charge);
   fChain->SetBranchAddress("TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass", TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass, &b_TauTo3Mu_mu1_fired_DoubleMu4_3_LowMass);
   fChain->SetBranchAddress("TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15", TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15, &b_TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15);
   fChain->SetBranchAddress("TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1", TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1, &b_TauTo3Mu_mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1);
   fChain->SetBranchAddress("TauTo3Mu_mu1_idx", TauTo3Mu_mu1_idx, &b_TauTo3Mu_mu1_idx);
   fChain->SetBranchAddress("TauTo3Mu_mu1_trackQuality", TauTo3Mu_mu1_trackQuality, &b_TauTo3Mu_mu1_trackQuality);
   fChain->SetBranchAddress("TauTo3Mu_mu2_charge", TauTo3Mu_mu2_charge, &b_TauTo3Mu_mu2_charge);
   fChain->SetBranchAddress("TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass", TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass, &b_TauTo3Mu_mu2_fired_DoubleMu4_3_LowMass);
   fChain->SetBranchAddress("TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15", TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15, &b_TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15);
   fChain->SetBranchAddress("TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1", TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1, &b_TauTo3Mu_mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1);
   fChain->SetBranchAddress("TauTo3Mu_mu2_idx", TauTo3Mu_mu2_idx, &b_TauTo3Mu_mu2_idx);
   fChain->SetBranchAddress("TauTo3Mu_mu2_trackQuality", TauTo3Mu_mu2_trackQuality, &b_TauTo3Mu_mu2_trackQuality);
   fChain->SetBranchAddress("TauTo3Mu_mu3_charge", TauTo3Mu_mu3_charge, &b_TauTo3Mu_mu3_charge);
   fChain->SetBranchAddress("TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass", TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass, &b_TauTo3Mu_mu3_fired_DoubleMu4_3_LowMass);
   fChain->SetBranchAddress("TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15", TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15, &b_TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15);
   fChain->SetBranchAddress("TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1", TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1, &b_TauTo3Mu_mu3_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1);
   fChain->SetBranchAddress("TauTo3Mu_mu3_idx", TauTo3Mu_mu3_idx, &b_TauTo3Mu_mu3_idx);
   fChain->SetBranchAddress("TauTo3Mu_mu3_trackQuality", TauTo3Mu_mu3_trackQuality, &b_TauTo3Mu_mu3_trackQuality);
   fChain->SetBranchAddress("TauTo3Mu_vtx_isValid", TauTo3Mu_vtx_isValid, &b_TauTo3Mu_vtx_isValid);
   fChain->SetBranchAddress("nTauPlusMET", &nTauPlusMET, &b_nTauPlusMET);
   fChain->SetBranchAddress("TauPlusMET_DeepMET_pt", TauPlusMET_DeepMET_pt, &b_TauPlusMET_DeepMET_pt);
   fChain->SetBranchAddress("TauPlusMET_DeepMETmaxPz", TauPlusMET_DeepMETmaxPz, &b_TauPlusMET_DeepMETmaxPz);
   fChain->SetBranchAddress("TauPlusMET_DeepMETminPz", TauPlusMET_DeepMETminPz, &b_TauPlusMET_DeepMETminPz);
   fChain->SetBranchAddress("TauPlusMET_Deep_eta", TauPlusMET_Deep_eta, &b_TauPlusMET_Deep_eta);
   fChain->SetBranchAddress("TauPlusMET_Deep_phi", TauPlusMET_Deep_phi, &b_TauPlusMET_Deep_phi);
   fChain->SetBranchAddress("TauPlusMET_Deep_pt", TauPlusMET_Deep_pt, &b_TauPlusMET_Deep_pt);
   fChain->SetBranchAddress("TauPlusMET_MET_pt", TauPlusMET_MET_pt, &b_TauPlusMET_MET_pt);
   fChain->SetBranchAddress("TauPlusMET_METmaxPz", TauPlusMET_METmaxPz, &b_TauPlusMET_METmaxPz);
   fChain->SetBranchAddress("TauPlusMET_METminPz", TauPlusMET_METminPz, &b_TauPlusMET_METminPz);
   fChain->SetBranchAddress("TauPlusMET_PuppiMET_pt", TauPlusMET_PuppiMET_pt, &b_TauPlusMET_PuppiMET_pt);
   fChain->SetBranchAddress("TauPlusMET_PuppiMETmaxPz", TauPlusMET_PuppiMETmaxPz, &b_TauPlusMET_PuppiMETmaxPz);
   fChain->SetBranchAddress("TauPlusMET_PuppiMETminPz", TauPlusMET_PuppiMETminPz, &b_TauPlusMET_PuppiMETminPz);
   fChain->SetBranchAddress("TauPlusMET_Puppi_eta", TauPlusMET_Puppi_eta, &b_TauPlusMET_Puppi_eta);
   fChain->SetBranchAddress("TauPlusMET_Puppi_phi", TauPlusMET_Puppi_phi, &b_TauPlusMET_Puppi_phi);
   fChain->SetBranchAddress("TauPlusMET_Puppi_pt", TauPlusMET_Puppi_pt, &b_TauPlusMET_Puppi_pt);
   fChain->SetBranchAddress("TauPlusMET_Tau_Deep_mT", TauPlusMET_Tau_Deep_mT, &b_TauPlusMET_Tau_Deep_mT);
   fChain->SetBranchAddress("TauPlusMET_Tau_Puppi_mT", TauPlusMET_Tau_Puppi_mT, &b_TauPlusMET_Tau_Puppi_mT);
   fChain->SetBranchAddress("TauPlusMET_Tau_mT", TauPlusMET_Tau_mT, &b_TauPlusMET_Tau_mT);
   fChain->SetBranchAddress("TauPlusMET_eta", TauPlusMET_eta, &b_TauPlusMET_eta);
   fChain->SetBranchAddress("TauPlusMET_mass", TauPlusMET_mass, &b_TauPlusMET_mass);
   fChain->SetBranchAddress("TauPlusMET_phi", TauPlusMET_phi, &b_TauPlusMET_phi);
   fChain->SetBranchAddress("TauPlusMET_pt", TauPlusMET_pt, &b_TauPlusMET_pt);
   fChain->SetBranchAddress("TauPlusMET_charge", TauPlusMET_charge, &b_TauPlusMET_charge);
   fChain->SetBranchAddress("BeamSpot_sigmaZ", &BeamSpot_sigmaZ, &b_BeamSpot_sigmaZ);
   fChain->SetBranchAddress("BeamSpot_sigmaZError", &BeamSpot_sigmaZError, &b_BeamSpot_sigmaZError);
   fChain->SetBranchAddress("BeamSpot_z", &BeamSpot_z, &b_BeamSpot_z);
   fChain->SetBranchAddress("BeamSpot_zError", &BeamSpot_zError, &b_BeamSpot_zError);
   fChain->SetBranchAddress("BeamSpot_type", &BeamSpot_type, &b_BeamSpot_type);
   fChain->SetBranchAddress("CaloMET_phi", &CaloMET_phi, &b_CaloMET_phi);
   fChain->SetBranchAddress("CaloMET_pt", &CaloMET_pt, &b_CaloMET_pt);
   fChain->SetBranchAddress("CaloMET_sumEt", &CaloMET_sumEt, &b_CaloMET_sumEt);
   fChain->SetBranchAddress("ChsMET_phi", &ChsMET_phi, &b_ChsMET_phi);
   fChain->SetBranchAddress("ChsMET_pt", &ChsMET_pt, &b_ChsMET_pt);
   fChain->SetBranchAddress("ChsMET_sumEt", &ChsMET_sumEt, &b_ChsMET_sumEt);
   fChain->SetBranchAddress("DeepMETResolutionTune_phi", &DeepMETResolutionTune_phi, &b_DeepMETResolutionTune_phi);
   fChain->SetBranchAddress("DeepMETResolutionTune_pt", &DeepMETResolutionTune_pt, &b_DeepMETResolutionTune_pt);
   fChain->SetBranchAddress("DeepMETResponseTune_phi", &DeepMETResponseTune_phi, &b_DeepMETResponseTune_phi);
   fChain->SetBranchAddress("DeepMETResponseTune_pt", &DeepMETResponseTune_pt, &b_DeepMETResponseTune_pt);
   fChain->SetBranchAddress("nGenPart", &nGenPart, &b_nGenPart);
   fChain->SetBranchAddress("GenPart_eta", GenPart_eta, &b_GenPart_eta);
   fChain->SetBranchAddress("GenPart_mass", GenPart_mass, &b_GenPart_mass);
   fChain->SetBranchAddress("GenPart_phi", GenPart_phi, &b_GenPart_phi);
   fChain->SetBranchAddress("GenPart_pt", GenPart_pt, &b_GenPart_pt);
   fChain->SetBranchAddress("GenPart_vx", GenPart_vx, &b_GenPart_vx);
   fChain->SetBranchAddress("GenPart_vy", GenPart_vy, &b_GenPart_vy);
   fChain->SetBranchAddress("GenPart_vz", GenPart_vz, &b_GenPart_vz);
   fChain->SetBranchAddress("GenPart_genPartIdxMother", GenPart_genPartIdxMother, &b_GenPart_genPartIdxMother);
   fChain->SetBranchAddress("GenPart_pdgId", GenPart_pdgId, &b_GenPart_pdgId);
   fChain->SetBranchAddress("GenPart_status", GenPart_status, &b_GenPart_status);
   fChain->SetBranchAddress("GenPart_statusFlags", GenPart_statusFlags, &b_GenPart_statusFlags);
   fChain->SetBranchAddress("Generator_binvar", &Generator_binvar, &b_Generator_binvar);
   fChain->SetBranchAddress("Generator_scalePDF", &Generator_scalePDF, &b_Generator_scalePDF);
   fChain->SetBranchAddress("Generator_weight", &Generator_weight, &b_Generator_weight);
   fChain->SetBranchAddress("Generator_x1", &Generator_x1, &b_Generator_x1);
   fChain->SetBranchAddress("Generator_x2", &Generator_x2, &b_Generator_x2);
   fChain->SetBranchAddress("Generator_xpdf1", &Generator_xpdf1, &b_Generator_xpdf1);
   fChain->SetBranchAddress("Generator_xpdf2", &Generator_xpdf2, &b_Generator_xpdf2);
   fChain->SetBranchAddress("Generator_id1", &Generator_id1, &b_Generator_id1);
   fChain->SetBranchAddress("Generator_id2", &Generator_id2, &b_Generator_id2);
   fChain->SetBranchAddress("genWeight", &genWeight, &b_genWeight);
   fChain->SetBranchAddress("nPSWeight", &nPSWeight, &b_nPSWeight);
   fChain->SetBranchAddress("PSWeight", PSWeight, &b_PSWeight);
   fChain->SetBranchAddress("GenMET_phi", &GenMET_phi, &b_GenMET_phi);
   fChain->SetBranchAddress("GenMET_pt", &GenMET_pt, &b_GenMET_pt);
   fChain->SetBranchAddress("MET_MetUnclustEnUpDeltaX", &MET_MetUnclustEnUpDeltaX, &b_MET_MetUnclustEnUpDeltaX);
   fChain->SetBranchAddress("MET_MetUnclustEnUpDeltaY", &MET_MetUnclustEnUpDeltaY, &b_MET_MetUnclustEnUpDeltaY);
   fChain->SetBranchAddress("MET_covXX", &MET_covXX, &b_MET_covXX);
   fChain->SetBranchAddress("MET_covXY", &MET_covXY, &b_MET_covXY);
   fChain->SetBranchAddress("MET_covYY", &MET_covYY, &b_MET_covYY);
   fChain->SetBranchAddress("MET_phi", &MET_phi, &b_MET_phi);
   fChain->SetBranchAddress("MET_pt", &MET_pt, &b_MET_pt);
   fChain->SetBranchAddress("MET_significance", &MET_significance, &b_MET_significance);
   fChain->SetBranchAddress("MET_sumEt", &MET_sumEt, &b_MET_sumEt);
   fChain->SetBranchAddress("MET_sumPtUnclustered", &MET_sumPtUnclustered, &b_MET_sumPtUnclustered);
   fChain->SetBranchAddress("nMuon", &nMuon, &b_nMuon);
   fChain->SetBranchAddress("Muon_dZpv", Muon_dZpv, &b_Muon_dZpv);
   fChain->SetBranchAddress("Muon_err_dZpv", Muon_err_dZpv, &b_Muon_err_dZpv);
   fChain->SetBranchAddress("Muon_phi", Muon_phi, &b_Muon_phi);
   fChain->SetBranchAddress("Muon_pt", Muon_pt, &b_Muon_pt);
   fChain->SetBranchAddress("Muon_z", Muon_z, &b_Muon_z);
   fChain->SetBranchAddress("Muon_charge", Muon_charge, &b_Muon_charge);
   fChain->SetBranchAddress("Muon_isSoft_BS", Muon_isSoft_BS, &b_Muon_isSoft_BS);
   fChain->SetBranchAddress("Muon_isTight_BS", Muon_isTight_BS, &b_Muon_isTight_BS);
   fChain->SetBranchAddress("Muon_trackQuality", Muon_trackQuality, &b_Muon_trackQuality);
   fChain->SetBranchAddress("Muon_isGlobal", Muon_isGlobal, &b_Muon_isGlobal);
   fChain->SetBranchAddress("Muon_isLoose", Muon_isLoose, &b_Muon_isLoose);
   fChain->SetBranchAddress("Muon_isMedium", Muon_isMedium, &b_Muon_isMedium);
   fChain->SetBranchAddress("Muon_isPFcand", Muon_isPFcand, &b_Muon_isPFcand);
   fChain->SetBranchAddress("Muon_isSoft", Muon_isSoft, &b_Muon_isSoft);
   fChain->SetBranchAddress("Muon_isTight", Muon_isTight, &b_Muon_isTight);
   fChain->SetBranchAddress("Muon_isTracker", Muon_isTracker, &b_Muon_isTracker);
   fChain->SetBranchAddress("Pileup_nTrueInt", &Pileup_nTrueInt, &b_Pileup_nTrueInt);
   fChain->SetBranchAddress("Pileup_pudensity", &Pileup_pudensity, &b_Pileup_pudensity);
   fChain->SetBranchAddress("Pileup_gpudensity", &Pileup_gpudensity, &b_Pileup_gpudensity);
   fChain->SetBranchAddress("Pileup_nPU", &Pileup_nPU, &b_Pileup_nPU);
   fChain->SetBranchAddress("Pileup_sumEOOT", &Pileup_sumEOOT, &b_Pileup_sumEOOT);
   fChain->SetBranchAddress("Pileup_sumLOOT", &Pileup_sumLOOT, &b_Pileup_sumLOOT);
   fChain->SetBranchAddress("PuppiMET_phi", &PuppiMET_phi, &b_PuppiMET_phi);
   fChain->SetBranchAddress("PuppiMET_phiJERDown", &PuppiMET_phiJERDown, &b_PuppiMET_phiJERDown);
   fChain->SetBranchAddress("PuppiMET_phiJERUp", &PuppiMET_phiJERUp, &b_PuppiMET_phiJERUp);
   fChain->SetBranchAddress("PuppiMET_phiJESDown", &PuppiMET_phiJESDown, &b_PuppiMET_phiJESDown);
   fChain->SetBranchAddress("PuppiMET_phiJESUp", &PuppiMET_phiJESUp, &b_PuppiMET_phiJESUp);
   fChain->SetBranchAddress("PuppiMET_phiUnclusteredDown", &PuppiMET_phiUnclusteredDown, &b_PuppiMET_phiUnclusteredDown);
   fChain->SetBranchAddress("PuppiMET_phiUnclusteredUp", &PuppiMET_phiUnclusteredUp, &b_PuppiMET_phiUnclusteredUp);
   fChain->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt, &b_PuppiMET_pt);
   fChain->SetBranchAddress("PuppiMET_ptJERDown", &PuppiMET_ptJERDown, &b_PuppiMET_ptJERDown);
   fChain->SetBranchAddress("PuppiMET_ptJERUp", &PuppiMET_ptJERUp, &b_PuppiMET_ptJERUp);
   fChain->SetBranchAddress("PuppiMET_ptJESDown", &PuppiMET_ptJESDown, &b_PuppiMET_ptJESDown);
   fChain->SetBranchAddress("PuppiMET_ptJESUp", &PuppiMET_ptJESUp, &b_PuppiMET_ptJESUp);
   fChain->SetBranchAddress("PuppiMET_ptUnclusteredDown", &PuppiMET_ptUnclusteredDown, &b_PuppiMET_ptUnclusteredDown);
   fChain->SetBranchAddress("PuppiMET_ptUnclusteredUp", &PuppiMET_ptUnclusteredUp, &b_PuppiMET_ptUnclusteredUp);
   fChain->SetBranchAddress("PuppiMET_sumEt", &PuppiMET_sumEt, &b_PuppiMET_sumEt);
   fChain->SetBranchAddress("RawMET_phi", &RawMET_phi, &b_RawMET_phi);
   fChain->SetBranchAddress("RawMET_pt", &RawMET_pt, &b_RawMET_pt);
   fChain->SetBranchAddress("RawMET_sumEt", &RawMET_sumEt, &b_RawMET_sumEt);
   fChain->SetBranchAddress("RawPuppiMET_phi", &RawPuppiMET_phi, &b_RawPuppiMET_phi);
   fChain->SetBranchAddress("RawPuppiMET_pt", &RawPuppiMET_pt, &b_RawPuppiMET_pt);
   fChain->SetBranchAddress("RawPuppiMET_sumEt", &RawPuppiMET_sumEt, &b_RawPuppiMET_sumEt);
   fChain->SetBranchAddress("Rho_fixedGridRhoAll", &Rho_fixedGridRhoAll, &b_Rho_fixedGridRhoAll);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetAll", &Rho_fixedGridRhoFastjetAll, &b_Rho_fixedGridRhoFastjetAll);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetCentral", &Rho_fixedGridRhoFastjetCentral, &b_Rho_fixedGridRhoFastjetCentral);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetCentralCalo", &Rho_fixedGridRhoFastjetCentralCalo, &b_Rho_fixedGridRhoFastjetCentralCalo);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetCentralChargedPileUp", &Rho_fixedGridRhoFastjetCentralChargedPileUp, &b_Rho_fixedGridRhoFastjetCentralChargedPileUp);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetCentralNeutral", &Rho_fixedGridRhoFastjetCentralNeutral, &b_Rho_fixedGridRhoFastjetCentralNeutral);
   fChain->SetBranchAddress("TkMET_phi", &TkMET_phi, &b_TkMET_phi);
   fChain->SetBranchAddress("TkMET_pt", &TkMET_pt, &b_TkMET_pt);
   fChain->SetBranchAddress("TkMET_sumEt", &TkMET_sumEt, &b_TkMET_sumEt);
   fChain->SetBranchAddress("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1", &HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1, &b_HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1);
   fChain->SetBranchAddress("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15", &HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15, &b_HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15);
   fChain->SetBranchAddress("HLT_DoubleMu4_3_LowMass", &HLT_DoubleMu4_3_LowMass, &b_HLT_DoubleMu4_3_LowMass);
   fChain->SetBranchAddress("nTrigObj", &nTrigObj, &b_nTrigObj);
   fChain->SetBranchAddress("TrigObj_pt", TrigObj_pt, &b_TrigObj_pt);
   fChain->SetBranchAddress("TrigObj_eta", TrigObj_eta, &b_TrigObj_eta);
   fChain->SetBranchAddress("TrigObj_phi", TrigObj_phi, &b_TrigObj_phi);
   fChain->SetBranchAddress("TrigObj_id", TrigObj_id, &b_TrigObj_id);
   fChain->SetBranchAddress("nOtherPV", &nOtherPV, &b_nOtherPV);
   fChain->SetBranchAddress("OtherPV_z", OtherPV_z, &b_OtherPV_z);
   fChain->SetBranchAddress("OtherPV_score", OtherPV_score, &b_OtherPV_score);
   fChain->SetBranchAddress("PV_ndof", &PV_ndof, &b_PV_ndof);
   fChain->SetBranchAddress("PV_x", &PV_x, &b_PV_x);
   fChain->SetBranchAddress("PV_y", &PV_y, &b_PV_y);
   fChain->SetBranchAddress("PV_z", &PV_z, &b_PV_z);
   fChain->SetBranchAddress("PV_chi2", &PV_chi2, &b_PV_chi2);
   fChain->SetBranchAddress("PV_score", &PV_score, &b_PV_score);
   fChain->SetBranchAddress("PV_npvs", &PV_npvs, &b_PV_npvs);
   fChain->SetBranchAddress("PV_npvsGood", &PV_npvsGood, &b_PV_npvsGood);
   fChain->SetBranchAddress("nSV", &nSV, &b_nSV);
   fChain->SetBranchAddress("SV_dlen", SV_dlen, &b_SV_dlen);
   fChain->SetBranchAddress("SV_dlenSig", SV_dlenSig, &b_SV_dlenSig);
   fChain->SetBranchAddress("SV_dxy", SV_dxy, &b_SV_dxy);
   fChain->SetBranchAddress("SV_dxySig", SV_dxySig, &b_SV_dxySig);
   fChain->SetBranchAddress("SV_pAngle", SV_pAngle, &b_SV_pAngle);
   fChain->SetBranchAddress("SV_charge", SV_charge, &b_SV_charge);
   fChain->SetBranchAddress("Muon_genPartIdx", Muon_genPartIdx, &b_Muon_genPartIdx);
   fChain->SetBranchAddress("Muon_genPartFlav", Muon_genPartFlav, &b_Muon_genPartFlav);
   fChain->SetBranchAddress("SV_chi2", SV_chi2, &b_SV_chi2);
   fChain->SetBranchAddress("SV_eta", SV_eta, &b_SV_eta);
   fChain->SetBranchAddress("SV_mass", SV_mass, &b_SV_mass);
   fChain->SetBranchAddress("SV_ndof", SV_ndof, &b_SV_ndof);
   fChain->SetBranchAddress("SV_phi", SV_phi, &b_SV_phi);
   fChain->SetBranchAddress("SV_pt", SV_pt, &b_SV_pt);
   fChain->SetBranchAddress("SV_x", SV_x, &b_SV_x);
   fChain->SetBranchAddress("SV_y", SV_y, &b_SV_y);
   fChain->SetBranchAddress("SV_z", SV_z, &b_SV_z);
   fChain->SetBranchAddress("SV_ntracks", SV_ntracks, &b_SV_ntracks);
   Notify();
}

Bool_t MCTau3Mu_base::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void MCTau3Mu_base::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t MCTau3Mu_base::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef MCTau3Mu_base_cxx
