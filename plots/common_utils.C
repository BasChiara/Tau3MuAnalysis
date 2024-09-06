#include <iostream>

#include <TFile.h>
#include <TString.h>

TFile* open_file(TString& inRootFile_){
    TFile* input_file = new TFile(inRootFile_);
    std::cout << "[+] opening file "<< inRootFile_ << std::endl;

    if ( !input_file->IsOpen() ) {
       std::cout << "ERROR IN OPENING FILE "<< inRootFile_ << std::endl;
       exit(-1);
    }

    return input_file;
}

Color_t PtlColorMap(const TString& particle){

  std::map <TString , Color_t> PtlColor{};
  // final satte particles 
  PtlColor["mu"]    = kPink + 4;
  PtlColor["mu1"]   = kBlue + 2;
  PtlColor["mu2"]  = kGreen + 2;
  PtlColor["mu3"]   = kOrange + 1;
  PtlColor["pi"]   = kOrange + 1;
  // intermediate resonances
  PtlColor["tau_fit"]   = kRed - 7;
  PtlColor["phi_fit"]   = kViolet;
  PtlColor["tau_gen"]  = kBlack;
  PtlColor["tau_raw"] = kBlue;
  // initial state particle
  PtlColor["W"] = kOrange;
  PtlColor["W_gen"] = kBlack;
  PtlColor["Ds_fit"]   = kRed - 7;
  // MET algos
  PtlColor["PuppiMET"] = kViolet + 2;
  PtlColor["rawPuppiMET"] = kOrange +2;
  PtlColor["DeepMET"] = kCyan +2;
  // dataset 
  PtlColor["Run2"] = kBlue;
  PtlColor["Run3_prompt"] = kOrange;
  PtlColor["Run3_reMini"] = kGreen +2;

  PtlColor["data22"] = kBlue;
  PtlColor["mc"] = kRed;
  PtlColor["Run3_HLT_Tau3Mu"] = kRed-7;
  PtlColor["Run3_HLT_DoubleMu"] = kGreen+2;
  PtlColor["2022preEE"]   = kAzure +1; 
  PtlColor["2022EE"]      = kAzure +1;
  PtlColor["Tau3Mu"]      = kRed;
  PtlColor["W3MuNu"]      = kGreen+1; 
  PtlColor["2023preBPix"] = kAzure +1; 
  PtlColor["2023BPix"]    = kOrange +1;

  PtlColor["unbalanced"] = kBlue;
  PtlColor["rebalanced"] = kRed;

  PtlColor["MCno_weight"] = kBlack;
  PtlColor["MC_weight"]   = kRed;


  return PtlColor[particle];
}

TString CategoryLegend(const TString& category){

  std::map <TString , TString> Leg_entry{};
  //final state particles
  Leg_entry["mu"] = "#mu";
  Leg_entry["mu1"] = "leading #mu";
  Leg_entry["mu2"] = "sub-leading #mu";
  Leg_entry["mu3"] = "trailing #mu";
  Leg_entry["pi"] = "track";
  // intermediate resonances
  Leg_entry["tau_fit"] = "3 #mu refit";
  Leg_entry["tau_fit"] = "#phi #to #mu #mu refit";
  Leg_entry["tau_gen"] = "#tau gen-level";
  Leg_entry["tau_raw"] = "3 #mu raw";
  // initial state particles
  Leg_entry["W"] = "W reco-level";
  Leg_entry["W_gen"] = "W gen-level";
  Leg_entry["Ds_fit"] = "#mu #mu #pi refit";
  // MET algos
  Leg_entry["PuppiMET"] = "PuppiMET (Run3)";
  Leg_entry["rawPuppiMET"] = "raw PuppiMET (Run3)";
  Leg_entry["DeepMET"] = "DeepMET (Run2)";
  //dataset
  Leg_entry["Run2"] = "Run2";
  Leg_entry["Run3_prompt"] = "Run3 prompt";
  Leg_entry["Run3_reMini"] = "Run3 reMini";

  Leg_entry["data22"]             = "data 2022";
  Leg_entry["mc"]                 = "signal";
  Leg_entry["Run3_HLT_Tau3Mu"]    = "HLT_Tau3Mu";
  Leg_entry["Run3_HLT_DoubleMu"]  = "HLT_DoubleMu";
  Leg_entry["2022preEE"]   = "2022preEE"; 
  Leg_entry["2022EE"]      = "2022EE";
  Leg_entry["Tau3Mu"]      = "W#tau(3#mu)#nu MC"; 
  Leg_entry["W3MuNu"]      = "W3#mu#nu MC"; 
  Leg_entry["2023preBPix"] = "2023 pre-BPix";
  Leg_entry["2023BPix"] = "2023 post-BPix";
  Leg_entry["unbalanced"] = "original";
  Leg_entry["rebalanced"] = "resampled";

  Leg_entry["MCno_weight"] = "MC no weight";
  Leg_entry["MC_weight"]   = "MC with weight";

  return Leg_entry[category];
}

void histoSetUp(TH1* histo, const TString& category, const TString& x_name, bool fill = true , bool norm = true){

  //AXIS LABEL 
  histo->GetXaxis()->SetTitle(x_name);
  histo->GetYaxis()->SetTitleOffset(2.0);
  histo->GetXaxis()->SetTitleSize(0.045);
  histo->GetXaxis()->SetLabelSize(0.035);
  histo->GetYaxis()->SetTitle(Form("Events/ %.3f", histo->GetXaxis()->GetBinWidth(1)));
  histo->GetYaxis()->SetTitleOffset(1.6);
  histo->GetYaxis()->SetTitleSize(0.04);
  histo->GetYaxis()->SetLabelSize(0.035);

  //WIDTH & COLOR
  histo->SetLineWidth(3);
  histo->SetLineColor(PtlColorMap(category));
  if (fill){
    histo->SetFillColorAlpha(PtlColorMap(category), 0.75);
    histo->SetFillStyle(3004);
  }
  //NORMALIZATION
  if(norm )histo->Scale(1./histo->Integral());
}

void CMSxxx(TCanvas* c){
	c->cd();
	TLatex RunDetails; RunDetails.SetNDC(); 
	RunDetails.SetTextFont(61);
	RunDetails.SetTextAlign(10);
	RunDetails.SetTextSize(0.03);
	RunDetails.DrawLatex(.10, .91, "CMS");
	RunDetails.SetTextFont(52);
	RunDetails.DrawLatex(.17, .91, "Simulation");
	RunDetails.SetTextFont(42);
	RunDetails.SetTextSize(0.025);
	//RunDetails.DrawLatex(.70, .91, "41 fb^{-1} (13 TeV)");

}
