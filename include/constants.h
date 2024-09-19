#ifndef Tau3MuAnalysis_constants
#define Tau3MuAnalysis_constants

#include "TString.h"
#include <string>
#include <map>

// PDG IDs
constexpr int isW       = 24;
constexpr int isTau     = 15;
constexpr int isNuTau   = 16;
constexpr int isMuon    = 13;
constexpr int isDs_p    = 431;
constexpr int isPion_p  = 211;
constexpr int isPhi1020 = 333;

// PDG mass & width [GeV]
constexpr float W_MASS       = 80.377;
constexpr float W_WIDTH      =  2.085;
constexpr float Ds_MASS      = 1.96834;
constexpr float Ds_WIDTH     = 0.02791; // ?
constexpr float Tau_MASS     = 1.776;
constexpr float Tau_WIDTH    = 0.00000001;
constexpr float Phi_MASS     = 1.019455;
constexpr float Phi_WIDTH    = 0.00426;
constexpr float NuTau_MASS   = 0.0;
constexpr float Muon_MASS    = 0.10565837;
constexpr float Muon_WIDTH   = 0.00000001;
constexpr float Pion_MASS    = 0.13957061;
constexpr float Pion_WIDTH   = 0.00000023;


// HLT-path enumerator
enum HLT_paths {
    HLT_Tau3Mu = 1,
    HLT_DoubleMu = 2,
    HLT_overlap = 3
};

enum MCsignals {
    MC_Tau3Mu,
    MC_DsPhiPi,
    MC_W3MuNu
};

namespace yearID
{
    inline std::map<TString, UInt_t> year_era_code{
        {"2022preEE"      , 220}, 
        {"2022EE"         , 221}, 
        {"ParkingDoubleMuonLowMass0_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass1_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass2_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass3_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass4_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass5_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass6_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass7_2022Cv1"       , 223},
        {"ParkingDoubleMuonLowMass0_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass1_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass2_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass3_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass4_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass5_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass6_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass7_2022Dv1"       , 224},
        {"ParkingDoubleMuonLowMass0_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass1_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass2_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass3_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass4_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass5_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass6_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass7_2022Dv2"       , 224},
        {"ParkingDoubleMuonLowMass0_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass1_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass2_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass3_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass4_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass5_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass6_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass7_2022Ev1"       , 225},
        {"ParkingDoubleMuonLowMass0_2022Fv1"       , 226},
        {"ParkingDoubleMuonLowMass1_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass2_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass3_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass4_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass5_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass6_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass7_2022Fv1"       , 225},
        {"ParkingDoubleMuonLowMass0_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass1_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass2_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass3_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass4_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass5_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass6_2022Gv1"       , 227},
        {"ParkingDoubleMuonLowMass7_2022Gv1"       , 227},
        {"2023preBPix"    , 230}, 
        {"2023BPix"       , 231},
        {"ParkingDoubleMuonLowMass0_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass1_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass2_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass3_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass4_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass5_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass6_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass7_2023Bv1"       , 232},
        {"ParkingDoubleMuonLowMass0_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass1_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass2_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass3_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass4_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass5_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass6_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass7_2023Cv1"       , 233},
        {"ParkingDoubleMuonLowMass0_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass1_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass2_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass3_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass4_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass5_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass6_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass7_2023Cv2"       , 233},
        {"ParkingDoubleMuonLowMass0_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass1_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass2_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass3_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass4_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass5_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass6_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass7_2023Cv3"       , 233},
        {"ParkingDoubleMuonLowMass0_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass1_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass2_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass3_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass4_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass5_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass6_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass7_2023Cv4"       , 233},
        {"ParkingDoubleMuonLowMass0_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass1_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass2_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass3_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass4_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass5_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass6_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass7_2023Dv1"       , 234},
        {"ParkingDoubleMuonLowMass0_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass1_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass2_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass3_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass4_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass5_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass6_2023Dv2"       , 234},
        {"ParkingDoubleMuonLowMass7_2023Dv2"       , 234},
    };
}

// Lumi-normalization
namespace LumiRun3
{
    inline std::map<TString, float> LumiFactor{
        {"DEFAULT"        , 1.0}, 
        {"2022preEE"      , 0.0001452},			 
        {"2022EE"         , 0.0000554},	
        {"2023preBPix"    , 0.0000574}, 
        {"2023BPix"       , 0.0000619}, 
    };
    inline std::map<TString, float> LumiFactor_W3MuNu{
        {"DEFAULT"        , 1.0}, 
        {"2022preEE"      , 0.001791}, 
        {"2022EE"         , 0.086435}, 
        {"2023preBPix"    , 0.002380}, 
        {"2023BPix"       , 0.001286}, 
    };
}

//*******************
//*  SCALE FACTORS  *
//*******************

namespace scale_factor_src
{
    // muon ID
    inline std::string base_dir = "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/";
    inline std::map<TString, std::string> IDsf_jsonfile_Jpsi{
        {"2022preEE"      , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2022_schemaV2.json"}, 
        {"2022EE"         , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2022_EE_schemaV2.json"}, 
        {"2023preBPix"    , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2023_schemaV2.json"}, 
        {"2023BPix"       , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2023_schemaV2.json"}, 
    };
    inline std::map<TString, std::string> IDsf_jsonfile_Z{
        {"2022preEE"      , base_dir + "/include/scale_factors/ScaleFactors_Muon_Z_ID_ISO_2022_schemaV2.json"}, 
        {"2022EE"         , base_dir + "/include/scale_factors/"}, 
        {"2023preBPix"    , base_dir + "/include/scale_factors/ScaleFactors_Muon_Z_ID_ISO_2023_schemaV2.json"}, 
        {"2023BPix"       , base_dir + "/include/scale_factors/"}, 
    };
    // HLT_DoubleMu
    inline std::string HLTeff_rootfile = base_dir + "corrections/HLT_DoubleMu4_3_LowMass/HLT_DoubleMu_efficiency2022.root";
    // PU weights
    // - central weights
    inline TString PUweight_rootfile = base_dir + "corrections/pileup/weights/puWeights_CollisionsRun3_GoldenJson_2024Aug26.root"; 
    inline std::map<TString, TString> centralPUweights_hist{
        {"2022preEE"      , "Collisions2022_355100_357900_eraBCD_GoldenJson"},
        {"2022EE"         , "Collisions2022_359022_362760_eraEFG_GoldenJson"},
        {"2023preBPix"    , "Collisions2023_366403_369802_eraBC_GoldenJson"},
        {"2023BPix"       , "Collisions2023_369803_370790_eraD_GoldenJson"},
    };
    // - recalc with Tau3Mu_nanoAOD
    inline TString myPUweight_rootfile = base_dir + "corrections/pileup/weights/PUweights_Run3_WTau3MuNanoAOD.root"; 
    inline std::map<TString, TString> myPUweights_hist{
        {"2022preEE"      , "myPUweights_GoldenJson_2022preEE_nomina"},
        {"2022EE"         , "myPUweights_GoldenJson_2022EE"},
        {"2023preBPix"    , "myPUweights_GoldenJson_2023preBPix"},
        {"2023BPix"       , "myPUweights_GoldenJson_2023BPix"},
    };
    // NLO weights
    inline TString NLOweight_rootfile = base_dir + "corrections/NLO_W/SF_source/W_NLOvsT3m_Run3.root";
    inline std::map<TString, TString> NLOweights_hist{ 
        {"2022preEE"      , "h_Wgen_2022preEE_ratio_pTeta"},
        {"2022EE"         , "h_Wgen_2022EE_ratio_pTeta"},
        {"2023preBPix"    , "h_Wgen_2023preBPix_ratio_pTeta"},
        {"2023BPix"       , "h_Wgen_2023BPix_ratio_pTeta"},
    };
}
#endif
