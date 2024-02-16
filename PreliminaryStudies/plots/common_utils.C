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
  
  PtlColor["mu"]    = kPink + 4;
  PtlColor["mu1"]   = kBlue + 2;
  PtlColor["mu2"]  = kGreen + 2;
  PtlColor["mu3"]   = kOrange + 1;
  PtlColor["pi"]   = kOrange + 1;

  PtlColor["tau_fit"]   = kRed - 7;
  PtlColor["phi_fit"]   = kViolet;
  PtlColor["tau_gen"]  = kBlack;
  PtlColor["tau_raw"] = kBlue;
  PtlColor["Ds_fit"]   = kRed - 7;

  PtlColor["PuppiMET"] = kViolet + 2;
  PtlColor["rawPuppiMET"] = kOrange +2;
  PtlColor["DeepMET"] = kCyan +2;

  PtlColor["W"] = kOrange;
  PtlColor["W_gen"] = kBlack;
  
  PtlColor["Run2"] = kBlue;
  PtlColor["Run3_prompt"] = kOrange;
  PtlColor["Run3_reMini"] = kGreen +2;

  PtlColor["data22"] = kBlue;
  PtlColor["mc"] = kRed;

  return PtlColor[particle];
}

TString CategoryLegend(const TString& category){

  std::map <TString , TString> Leg_entry{};
  Leg_entry["mu"] = "#mu";
  Leg_entry["mu1"] = "leading #mu";
  Leg_entry["mu2"] = "sub-leading #mu";
  Leg_entry["mu3"] = "trailing #mu";
  Leg_entry["pi"] = "track";

  Leg_entry["tau_fit"] = "3 #mu refit";
  Leg_entry["Ds_fit"] = "#mu #mu #pi refit";
  Leg_entry["tau_fit"] = "#phi #to #mu #mu refit";
  Leg_entry["tau_gen"] = "#tau gen-level";
  Leg_entry["tau_raw"] = "3 #mu raw";

  Leg_entry["PuppiMET"] = "PuppiMET (Run3)";
  Leg_entry["rawPuppiMET"] = "raw PuppiMET (Run3)";
  Leg_entry["DeepMET"] = "DeepMET (Run2)";
  Leg_entry["W"] = "W reco-level";
  Leg_entry["W_gen"] = "W gen-level";

  Leg_entry["Run2"] = "Run2";
  Leg_entry["Run3_prompt"] = "Run3 prompt";
  Leg_entry["Run3_reMini"] = "Run3 reMini";

  Leg_entry["data22"] = "data 2022";
  Leg_entry["mc"] = "signal";
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
    histo->SetFillColorAlpha(PtlColorMap(category), 0.3);
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
