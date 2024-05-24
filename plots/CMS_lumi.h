#include "TPad.h"
#include "TLatex.h"
#include "TLine.h"
#include "TBox.h"
#include "TASImage.h"

//
// Global variables
//

TString cmsText     = "CMS";
float cmsTextFont   = 61;  // default is helvetic-bold

bool writeExtraText = true;
TString extraText   = "Preliminary";
float extraTextFont = 52;  // default is helvetica-italics

// text sizes and text offsets with respect to the top frame
// in unit of the top margin size
float lumiTextSize     = 0.6;
float lumiTextOffset   = 0.2;
float cmsTextSize      = 1.0;
float cmsTextOffset    = 0.1;  // only used in outOfFrame version

float relPosX    = 0.05; //0.15 (out of frame) in [0, 1] rispetto pad interno
float relPosY    = 0.10;
float relExtraDY = 1.0;

// ratio of "CMS" and extra text size
float extraOverCmsTextSize  = .75;

TString lumi_13TeV = "20.1 fb^{-1}";
TString lumi_8TeV  = "19.7 fb^{-1}";
TString lumi_7TeV  = "5.1 fb^{-1}";
TString lumi_sqrtS = "";
TString lumi_2022  = "34.7 fb^{-1} ";
TString lumi_2023  = "27.9 fb^{-1} ";

bool drawLogo      = false;

void CMS_lumi( TPad* pad, int iPeriod=3, int iPosX=10 );

