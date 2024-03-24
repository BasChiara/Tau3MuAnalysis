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
constexpr int isDs_p   = 431;
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

// Lumi-normalization
namespace LumiRun3
{
inline std::map<TString, float> LumiFactor{
   {"DEFAULT"        , 1.0}, 
   {"2022preEE"      , 0.00014111}, 
   {"2022EE"         , 0.00005537}, 
   {"2023preBPix"    , 0.00004177}, 
   {"2023BPix"       , 0.00004821}, 
};
}

#endif
