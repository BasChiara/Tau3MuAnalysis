#ifndef DsPhiMuMuPi_analyzer_h
#define DsPhiMuMuPi_analyzer_h
#include "DsPhiMuMuPi_tools.h"
#include <cstdlib>
#include <iostream>

class DsPhiMuMuPi_analyzer : public DsPhiMuMuPi_tools{

   public :
      DsPhiMuMuPi_analyzer(TTree *tree=0, const TString & outdir = "./outRoot", const TString& year = "2022preEE", const TString process = "DsPhiPi", const TString & tag="", const bool isMC = false) : DsPhiMuMuPi_tools(tree, isMC){
         // running on DATA or MC ?
         isMC_ = isMC;
         TString DATA_MC_tag = "DATA";
         if (isMC_) DATA_MC_tag = "MC";
         // which era is processed
         year_ = year;
         auto search_id = yearID::year_era_code.find(year_);
         if (search_id != yearID::year_era_code.end()) year_id_ = search_id->second;
         else year_id_ = 0;
         // set simulated process
         process_ = process;
         TString process_tag = "";
         if (process_ != "data" ) process_tag = "on" + process_;
         // normalization --> data driven next steps
         lumi_factor = 1.0; 
         // set the HLT tag
         TString HLT_tag = "";
         if(HLTconf_ == HLT_paths::HLT_Tau3Mu)   HLT_tag = "HLT_Tau3Mu"; 
         if(HLTconf_ == HLT_paths::HLT_DoubleMu) HLT_tag = "HLT_DoubleMu"; 
         if(HLTconf_ == HLT_paths::HLT_overlap)  HLT_tag = "HLT_overlap";

         //final tag
         tag_ = DATA_MC_tag + "analyzer_" + year_ + "_"+ HLT_tag;
         if (!process_tag.IsNull()) tag_ = tag_ + "_" + process_tag;
         if (!tag.IsNull()) tag_ = tag_ + "_" + tag;

         // parse the SF file for MonteCarlo
         if (isMC_){
            parseMuonSF(year_, "low"); 
            parsePUweights(year_);
         }

         // name and setup the output
         outFilePath_ = outdir + "/DsPhiMuMuPi_"+ tag_ + ".root";
         std::cout << "[o] output file is " << outFilePath_ << std::endl; 
         outTreeSetUp();

         srand(123456);

         std::cout << "-------------------------------------------" << std::endl;
         std::cout << "[ Ds -> Phi(MuMu)Pi analyzer ]"<< std::endl;
         std::cout << "> year/era  " << year_ << " [" << year_id_ << "]" << std::endl;
         std::cout << "> HLT path : " << HLT_tag << std::endl;
         std::cout << "> running on " << DATA_MC_tag << std::endl;
         std::cout << "-------------------------------------------" << std::endl;

      } 
      virtual ~DsPhiMuMuPi_analyzer() override {}

      virtual void Loop();
      void    outTreeSetUp();
      void    saveOutput();

   private :

      TString tag_;
      TString year_;
      UInt_t  year_id_;
      TString process_;

      // DATA or MC
      bool isMC_;
      // MC matching tau candidate
      int DsPhiPi_MCmatch_idx;
      // HLT paths
      HLT_paths HLTconf_ = HLT_overlap; // HLT_DoubleMu, HLT_Tau3Mu, HLT_overlap

      // [OUTPUT]
      TString outFilePath_;
      TFile*  outFile_;
      TTree*  outTree_;
      const TString outTree_name_ = "DsPhiMuMuPi_tree";

      // TTree branches
      UInt_t LumiBlock, Run;
      ULong64_t Event;
      int nGoodPV;
      float Rho_Fj;
      // total weight : lumi and scale factor
      float weight;
      float lumi_factor = 1.0;
      // HLT_bit
      int HLT_isfired_Tau3Mu, HLT_isfired_DoubleMu;
      // MC matching bool
      int isMCmatching;
      // * muons
      int   phi_mu1_MediumID,  phi_mu2_MediumID;
      int   phi_mu1_LooseID,  phi_mu2_LooseID;
      int   phi_mu1_SoftID_PV, phi_mu2_SoftID_PV;
      int   phi_mu1_SoftID_BS, phi_mu2_SoftID_BS;
      int   phi_mu1_TightID_PV,phi_mu2_TightID_PV;
      int   phi_mu1_TightID_BS,phi_mu2_TightID_BS;
      float phi_mu1_pt, phi_mu2_pt;
      float phi_mu1_gen_pt = -1, phi_mu2_gen_pt = -1;
      float phi_mu1_eta, phi_mu2_eta;
      float phi_mu1_gen_eta = -1, phi_mu2_gen_eta = -1;
      float phi_mu12_dZ;
      // * phi(1020) candidates
      float phi_gen_mass = -1;
      float phi_gen_pt = -1, phi_gen_eta = -1, phi_gen_phi = -1;
      float phi_fit_mass, phi_fit_mass_err;
      float phi_fit_pt, phi_fit_eta, phi_fit_phi, phi_fit_charge;
      // * pion kinematics
      float pi_gen_pt = -1, pi_gen_eta = -1, pi_gen_phi = -1;
      float pi_pt, pi_eta, pi_phi;
      int   pi_TightID;
      // *  Ds candidates
      float Ds_gen_pt = -1, Ds_gen_eta = -1, Ds_gen_phi = -1;
      int n_Ds;
      float Ds_fit_mass, Ds_fit_mass_err;
      float Ds_fit_pt, Ds_fit_eta, Ds_fit_phi, Ds_fit_charge;
      float Ds_relIso, Ds_relIso_pT05; 
      float Ds_Iso_chargedDR04, Ds_Iso_photonDR04, Ds_Iso_puDR08; 
      float Ds_Iso_chargedDR04_pT05, Ds_Iso_photonDR04_pT05, Ds_Iso_puDR08_pT05; 
      float Ds_Lxy_val_BS, Ds_Lxy_err_BS, Ds_Lxy_sign_BS;
      float Ds_fit_mt, Ds_fit_vprob, Ds_cosAlpha_BS;
      float Ds_mu1pi_dZ, Ds_mu2pi_dZ;
      // * Ds + MET
      float gen_met_pt = -1, gen_met_phi = -1;
      float tau_met_pt, tau_met_phi; //PuppiMET
      float tau_rawMet_pt, tau_rawMet_phi; // rawPuppiMET
      float tau_DeepMet_pt, tau_DeepMet_phi;
      float tau_met_Dphi, tau_met_ratio_pt;
      float miss_pz_min, miss_pz_max;
      float METlongNu, METperpNu;
      float W_pt, W_eta_min, W_eta_max, W_phi;
      float W_Deep_pt, W_Deep_eta_min, W_Deep_eta_max, W_Deep_phi;
      float W_mass_nominal, W_mass_min, W_mass_max;

};// DsPhiMuMuPi_analyzer

#endif
