#ifndef Tau3MuAnalysis_constants
#define Tau3MuAnalysis_constants

// PDG IDs
constexpr int isW       = 24;
constexpr int isTau     = 15;
constexpr int isNuTau   = 16;
constexpr int isMuon    = 13;

// PDG mass & width [GeV]
constexpr float W_MASS       = 80.377;
constexpr float W_WIDTH      =  2.085;
constexpr float Tau_MASS     = 1.776;
constexpr float Tau_WIDTH    = 0.00000001;
constexpr float NuTau_MASS   = 0.0;
constexpr float Muon_MASS    = 0.10565837;
constexpr float Muon_WIDTH   = 0.00000001;


// HLT-path enumerator
enum HLT_paths {
    HLT_Tau3Mu = 1,
    HLT_DoubleMu = 2,
    HLT_overlap = 3
};



#endif
