#ifndef Tau3MuAnalysis_constants
#define Tau3MuAnalysis_constants

#include "TString.h"
#include <string>
#include <map>

// PDG IDs
constexpr int isZ       = 23;
constexpr int isW       = 24;
constexpr int isEle     = 11;
constexpr int isNuEle   = 12;
constexpr int isMuon    = 13;
constexpr int isNuMuon  = 14;
constexpr int isTau     = 15;
constexpr int isNuTau   = 16;
constexpr int isDs_p    = 431;
constexpr int isPion_p  = 211;
constexpr int isPion_0  = 111;
constexpr int isPhi1020 = 333;

// PDG mass & width [GeV]
constexpr float Z_MASS       = 91.1876;
constexpr float Z_WIDTH      =  2.4952;
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

enum TauDecayMode {
    UNDEFINED  = -1,
    ELECTRONIC = 1,
    MUONIC     = 2,
    HADRONIC   = 3,
    TRIMUON    = 10,
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
        {"2024"    , 240}, 
        {"ParkingDoubleMuonLowMass0_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass1_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass2_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass3_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass4_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass5_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass6_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass7_2024Bv1"       , 242},
        {"ParkingDoubleMuonLowMass0_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass1_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass2_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass3_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass4_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass5_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass6_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass7_2024Cv1"       , 243},
        {"ParkingDoubleMuonLowMass0_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass1_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass2_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass3_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass4_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass5_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass6_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass7_2024Dv1"       , 244},
        {"ParkingDoubleMuonLowMass0_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass1_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass2_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass3_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass4_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass5_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass6_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass7_2024Ev1"       , 245},
        {"ParkingDoubleMuonLowMass0_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass1_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass2_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass3_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass4_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass5_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass6_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass7_2024Ev2"       , 245},
        {"ParkingDoubleMuonLowMass0_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass1_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass2_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass3_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass4_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass5_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass6_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass7_2024Fv1"       , 246},
        {"ParkingDoubleMuonLowMass0_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass1_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass2_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass3_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass4_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass5_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass6_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass7_2024Gv1"       , 247},
        {"ParkingDoubleMuonLowMass0_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass1_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass2_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass3_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass4_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass5_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass6_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass7_2024Hv1"       , 248},
        {"ParkingDoubleMuonLowMass0_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass1_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass2_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass3_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass4_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass5_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass6_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass7_2024Iv1"       , 249},
        {"ParkingDoubleMuonLowMass0_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass1_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass2_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass3_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass4_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass5_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass6_2024Iv2"       , 249},
        {"ParkingDoubleMuonLowMass7_2024Iv2"       , 249},
    };
}

// Lumi-normalization
namespace LumiRun3
{
    // xsec W -> Tau Nu [fb]
    inline float eff_filterW = 1.0;
    inline float xsec_ppWxMuNu_SMP_Run3 = 20928000;
    inline float Br_WtoMuNu  = 0.1063;
    inline float Br_WtoTauNu = 0.1138;
    inline float xsec_ppWxTauNu = xsec_ppWxMuNu_SMP_Run3 * Br_WtoTauNu / Br_WtoMuNu;

    // xsec Z -> Tau Tau [fb]
    inline float eff_filterZ = 0.2444; // 60 GeV < Mtautau < 120 GeV
    inline float xsec_ppZxMuMu_SMP_Run3 = 2026000;
    inline float Br_ZtoTauTau = 0.0337;
    inline float Br_ZtoMuMu  = 0.0337;
    inline float xsec_ppZxTauTau = xsec_ppZxMuMu_SMP_Run3 * Br_ZtoTauTau / Br_ZtoMuMu;
    // processed luminosity [/fb]
    inline std::map<TString, float> Lumi{
        {"2022preEE"      , 4.990+2.961+5.684}, 
        {"2022EE"         , 17.755+3.078}, 
        {"2023preBPix"    , 0.601+17.516}, 
        {"2023BPix"       , 9.690}, 
        {"2024"           , 0.12+7.14+7.88+11.22+27.72+37.57+5.43+11.28},
    };
    // Nmc @ filter level
    inline std::map<TString, float> Nmc{
        {"2022preEE"      , 197789}, 
        {"2022EE"         , 792640}, 
        {"2023preBPix"    , 662000}, 
        {"2023BPix"       , 330000}, 
        {"2024"           , 3894160},
    };
    // Br (tau -> 3mu)
    inline float Br_t3m = 1e-7;
    // Lumi normalization factor
    inline std::map<TString, float> LumiFactor{
        {"DEFAULT"        , 1.0}, 
        {"2022preEE"      , (Lumi["2022preEE"]*xsec_ppWxTauNu*Br_t3m)/Nmc["2022preEE"]},//0.0001452},			 
        {"2022EE"         , (Lumi["2022EE"]*xsec_ppWxTauNu*Br_t3m)/Nmc["2022EE"]},//0.0000554},	
        {"2023preBPix"    , (Lumi["2023preBPix"]*xsec_ppWxTauNu*Br_t3m)/Nmc["2023preBPix"]},//0.0000574}, 
        {"2023BPix"       , (Lumi["2023BPix"]*xsec_ppWxTauNu*Br_t3m)/Nmc["2023BPix"]},//0.0000619},
        {"2024"           , (Lumi["2024"]*xsec_ppWxTauNu*Br_t3m)/Nmc["2024"]},//0.0000619},
    };
    inline std::map<TString, float> LumiFactor_W3MuNu{
        {"DEFAULT"        , 1.0}, 
        {"2022preEE"      , 0.001791}, 
        {"2022EE"         , 0.086435}, 
        {"2023preBPix"    , 0.002380}, 
        {"2023BPix"       , 0.001286}, 
    };

    inline std::map<TString, float> LumiFactor_ZTau3Mu{
        {"DEFAULT"        , 1.0}, 
        {"2022preEE"      , Lumi["2022preEE"]*xsec_ppZxTauTau*2.*Br_t3m/195001}, 
        {"2022EE"         , Lumi["2022EE"]*xsec_ppZxTauTau*2.*Br_t3m/786411}, 
        {"2023preBPix"    , Lumi["2023preBPix"]*xsec_ppZxTauTau*2.*Br_t3m/677882}, 
        {"2023BPix"       , Lumi["2023BPix"]*xsec_ppZxTauTau*2.*Br_t3m/317554},
        {"2024"           , Lumi["2024"]*xsec_ppZxTauTau*2.*Br_t3m/4103413},
    };
}

//*******************
//*  SCALE FACTORS  *
//*******************

namespace scale_factor_src
{
    inline std::string base_dir = "/afs/cern.ch/user/c/cbasile/WTau3MuRun3_Analysis/CMSSW_13_0_13/src/Tau3MuAnalysis/";
    // muon ID
    inline std::map<TString, std::string> IDsf_jsonfile_Jpsi{
        {"2022preEE"      , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2022_schemaV2.json"}, 
        {"2022EE"         , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2022_EE_schemaV2.json"}, 
        {"2023preBPix"    , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2023_schemaV2.json"}, 
        {"2023BPix"       , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2023_schemaV2.json"},
        {"2024"           , base_dir + "/include/scale_factors/ScaleFactors_Muon_Jpsi_ID_2023_schemaV2.json"}, // fixme : to be updated
    };
    inline std::map<TString, std::string> IDsf_jsonfile_Z{
        {"2022preEE"      , base_dir + "/include/scale_factors/ScaleFactors_Muon_Z_ID_ISO_2022_schemaV2.json"}, 
        {"2022EE"         , base_dir + "/include/scale_factors/"}, 
        {"2023preBPix"    , base_dir + "/include/scale_factors/ScaleFactors_Muon_Z_ID_ISO_2023_schemaV2.json"}, 
        {"2023BPix"       , base_dir + "/include/scale_factors/"},
    };
    // HLT_DoubleMu
    inline std::string HLTeff_rootfile = base_dir + "corrections/HLT_DoubleMu4_3_LowMass/HLT_DoubleMu_efficiency2022.root";
    inline std::map<TString, TString> L1_HLT_mPOG_eff_files{
        {"2022preEE"      , base_dir + "corrections/HLT_DoubleMu4_3_LowMass/muonPOG/Run2022/HLT_L1_efficiency_abseta_pt.root"},
        {"2022EE"         , base_dir + "corrections/HLT_DoubleMu4_3_LowMass/muonPOG/Run2022/HLT_L1_efficiency_abseta_pt.root"},
        {"2023preBPix"    , base_dir + "corrections/HLT_DoubleMu4_3_LowMass/muonPOG/Run2023/HLT_L1_efficiency_abseta_pt.root"},
        {"2023BPix"       , base_dir + "corrections/HLT_DoubleMu4_3_LowMass/muonPOG/Run2023/HLT_L1_efficiency_abseta_pt.root"},
        {"2024"           , base_dir + "corrections/HLT_DoubleMu4_3_LowMass/muonPOG/Run2023/HLT_L1_efficiency_abseta_pt.root"}, // fixme : to be updated
    };
    inline std::string L1_mPOG_eff_MC    = "L1_MCefficiency";
    inline std::string L1_mPOG_eff_DATA  = "L1_DATAefficiency";
    inline std::string HLT_mPOG_eff_MC   = "HLT_MCefficiency";
    inline std::string HLT_mPOG_eff_DATA = "HLT_DATAefficiency";


    // PU weights
    // - central weights + my weights for 2024
    //inline TString PUweight_rootfile = base_dir + "corrections/pileup/weights/puWeights_CollisionsRun3_GoldenJson_2024Aug26.root"; 
    inline TString PUweight_rootfile = base_dir + "corrections/pileup/weights/puWeights_Collisions22_23_24_GoldenJson_2025Mar25.root";
    inline std::map<TString, TString> centralPUweights_hist{
        {"2022preEE"      , "Collisions2022_355100_357900_eraBCD_GoldenJson"},
        {"2022EE"         , "Collisions2022_359022_362760_eraEFG_GoldenJson"},
        {"2023preBPix"    , "Collisions2023_366403_369802_eraBC_GoldenJson"},
        {"2023BPix"       , "Collisions2023_369803_370790_eraD_GoldenJson"},
        {"2024"           , "myPUweights_GoldenJson_2024"},
    };
    // - recalc with Tau3Mu_nanoAOD
    inline TString myPUweight_rootfile = base_dir + "corrections/pileup/weights/PUweights_Run3_WTau3MuNanoAOD.root"; 
    inline std::map<TString, TString> myPUweights_hist{
        {"2022preEE"      , "myPUweights_GoldenJson_2022preEE"},
        {"2022EE"         , "myPUweights_GoldenJson_2022EE"},
        {"2023preBPix"    , "myPUweights_GoldenJson_2023preBPix"},
        {"2023BPix"       , "myPUweights_GoldenJson_2023BPix"},
    };
    // NLO weights 
    // - W channel
    inline TString NLOweight_W_rootfile = base_dir + "corrections/NLO_W/SF_source/W_NLOvsT3m_Run3.root";
    // - Z channel
    inline TString NLOweight_Z_rootfile = base_dir + "corrections/NLO_W/SF_source/Z_NLOvsT3m_Run3.root";
    inline std::map<TString, TString> NLOweights_hist{ 
        {"2022preEE"      , "h_Wgen_2022preEE_ratio_pTeta"},
        {"2022EE"         , "h_Wgen_2022EE_ratio_pTeta"},
        {"2023preBPix"    , "h_Wgen_2023preBPix_ratio_pTeta"},
        {"2023BPix"       , "h_Wgen_2023BPix_ratio_pTeta"},
        {"2024"           , "h_Wgen_2023BPix_ratio_pTeta"}, // fixme : to be updated
    }; 

    // pT Z and W from data [SMP]
    inline TString pTVweight_rootfile = base_dir + "corrections/pT_W/SMPinput/pTV_weightsSMP.root";
    inline TString pTVweights_hist = "pTV_weights";
}
#endif
