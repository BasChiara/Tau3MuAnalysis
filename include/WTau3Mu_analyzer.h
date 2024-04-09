#ifndef WTau3Mu_analyzer_h
#define WTau3Mu_analyzer_h

#include "WTau3Mu_tools.h"
#include <cmath>

class WTau3Mu_analyzer : public WTau3Mu_tools{

   public:
      WTau3Mu_analyzer(TTree *tree=0, const TString & outdir = "./outRoot", const TString& year = "2022preEE", const TString & tag="", const bool isMC = false) : WTau3Mu_tools(tree, isMC){
         // running on DATA or MC ?
         isMC_ = isMC;
         TString DATA_MC_tag = "DATA";
         if (isMC_) DATA_MC_tag = "MC";
         // set the year
         year_ = year;

         if (auto search = LumiRun3::LumiFactor.find(year_); isMC_ && search != LumiRun3::LumiFactor.end()){
            if(debug) std::cout << "> found year tag " << search->first << std::endl;
            lumi_factor = search->second;
         }else lumi_factor =LumiRun3::LumiFactor["DEFAULT"];
         // set the HLT tag
         TString HLT_tag = "";
         if(HLTconf_ == HLT_paths::HLT_Tau3Mu)   HLT_tag = "HLT_Tau3Mu"; 
         if(HLTconf_ == HLT_paths::HLT_DoubleMu) HLT_tag = "HLT_DoubleMu"; 
         if(HLTconf_ == HLT_paths::HLT_overlap)  HLT_tag = "HLT_overlap"; 
         // final tag
         tag_ = DATA_MC_tag +"analyzer_"+ year_ + "_" + HLT_tag;
         if (!tag.IsNull()) tag_ = tag_ + "_" + tag;     

         // parse the SF file
         if (isMC_){
            parseMuonSF(year_, "low");         
            //parseMuonSF(year_, "medium");         
         }

         // name and setup the output
         outFilePath_ = outdir + "/WTau3Mu_"+ tag_ + ".root";
         std::cout << "[o] output file is " << outFilePath_ << std::endl; 
         outTreeSetUp();

         std::cout << "-------------------------------------------" << std::endl;
         std::cout << "[ Tau 3 Mu analyzer ]"<< std::endl;
         std::cout << "> Lumi weight for " << year_ << " = " << lumi_factor << std::endl;
         std::cout << "> HLT path : " << HLT_tag << std::endl;
         std::cout << "> running on " << DATA_MC_tag << std::endl;
         std::cout << "-------------------------------------------" << std::endl;
      }
      virtual ~WTau3Mu_analyzer(){}

      virtual void Loop();
      void   fakeDs_mass(const int& cand_idx);
      void    outTreeSetUp();
      void    saveOutput();

   private:
      bool debug = false;

      // MC related vars
      bool isMC_;
      int TauTo3Mu_MCmatch_idx;
      // HLT paths
      HLT_paths HLTconf_ = HLT_overlap;  // HLT_DoubleMu, HLT_Tau3Mu, HLT_overlap

      // blinding parameters
      bool isBlind_ = false;
      const float blindTauMass_low = 1.74;
      const float blindTauMass_high = 1.82;

      TString tag_;
      TString year_;

      TString outFilePath_;
      TFile*  outFile_;
      TTree*  outTree_;
      const TString outTree_name_ = "WTau3Mu_tree";

      // TTree branches
      UInt_t LumiBlock, Run;
      ULong64_t Event;
      int nGoodPV;
      int isMCmatching;
      // lumi and scale facors
      float lumi_factor;
      // HLT_bit
      int HLT_isfired_Tau3Mu, HLT_isfired_DoubleMu;
      // * muons
      int   tau_mu1_MediumID,  tau_mu2_MediumID,  tau_mu3_MediumID;
      int   tau_mu1_LooseID,  tau_mu2_LooseID,  tau_mu3_LooseID;
      int   tau_mu1_SoftID_PV, tau_mu2_SoftID_PV, tau_mu3_SoftID_PV;
      int   tau_mu1_SoftID_BS, tau_mu2_SoftID_BS, tau_mu3_SoftID_BS;
      int   tau_mu1_TightID_PV,tau_mu2_TightID_PV,tau_mu3_TightID_PV;
      int   tau_mu1_TightID_BS,tau_mu2_TightID_BS,tau_mu3_TightID_BS;
      float tau_mu1_pt, tau_mu2_pt, tau_mu3_pt;
      float tau_mu1_eta, tau_mu2_eta, tau_mu3_eta;
      float tau_mu1_z, tau_mu2_z, tau_mu3_z;
      float tau_mu12_dZ, tau_mu23_dZ, tau_mu13_dZ;
      float tau_mu12_M, tau_mu23_M, tau_mu13_M;
      float tau_mu12_fitM, tau_mu23_fitM, tau_mu13_fitM;
      float tau_mu1_gen_pt, tau_mu2_gen_pt, tau_mu3_gen_pt;
      float tau_mu1_gen_eta, tau_mu2_gen_eta, tau_mu3_gen_eta;
      // * tau candidates
      int n_tau;
      float tau_gen_mass;
      float tau_gen_pt, tau_gen_eta, tau_gen_phi;
      float tau_raw_mass;
      float tau_fit_mass, tau_fit_mass_err, tau_fit_mass_resol;
      float tau_fit_pt, tau_fit_eta, tau_fit_phi, tau_fit_charge;
      float tau_relIso, tau_relIso_pT05; 
      float tau_Iso_chargedDR04, tau_Iso_photonDR04, tau_Iso_puDR08; 
      float tau_Iso_chargedDR04_pT05, tau_Iso_photonDR04_pT05, tau_Iso_puDR08_pT05; 
      float tau_dimuon_mass;
      float tau_Lxy_val_BS, tau_Lxy_err_BS, tau_Lxy_sign_BS;
      float tau_fit_mt, tau_fit_vprob, tau_cosAlpha_BS;
      // * tau + MET
      float gen_met_pt, gen_met_phi;
      float Nu_gen_pt, Nu_gen_eta, Nu_gen_phi;
      float METlongNu, METperpNu;
      float W_gen_pt, W_gen_eta, W_gen_phi;
      float tau_met_pt, tau_met_phi; //PuppiMET
      float tau_rawMet_pt, tau_rawMet_phi; // rawPuppiMET
      float tau_DeepMet_pt, tau_DeepMet_phi;
      float tau_met_Dphi, tau_met_ratio_pt;
      float miss_pz_min, miss_pz_max;
      float W_pt, W_eta_min, W_eta_max, W_phi;
      float W_Deep_pt, W_Deep_eta_min, W_Deep_eta_max, W_Deep_phi;
      float W_mass_nominal, W_mass_min, W_mass_max;
      // * fake rate *
      float tau_phiMuMu_mass, tau_MuMuPi_mass;

};


#endif
