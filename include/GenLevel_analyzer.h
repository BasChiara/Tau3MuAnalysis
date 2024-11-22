#pragma once
#include "GenLevel_base.h"

#include "constants.h"

#include "Math/Vector4D.h"
#include "Math/GenVector/VectorUtil.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

class GenLevel_analyzer : public GenLevel_base{
    public:
        GenLevel_analyzer(TTree *tree=0, const TString & outdir = "./outRoot", const TString& year = "2016", const TString process = "Zll", const TString & tag="", const bool isMC = false) : GenLevel_base(tree){}
    virtual ~GenLevel_analyzer(){}
    
    virtual void Loop() override;
    virtual bool genZll_selection();
    //virtual void genWlnu_selection();

    private:
        bool debug_ = false;
    
        const double minLepton_pT_  = 25.0; // GeV
        const double maxLepton_eta_ = 2.4;
        const double Vmass_tolerance = 15.0; // GeV

        // gen particle P4 
        ROOT::Math::PtEtaPhiMVector GenV_P4;
        ROOT::Math::PtEtaPhiMVector Genl1_P4, Genl2_P4, GenNu_P4;
};
