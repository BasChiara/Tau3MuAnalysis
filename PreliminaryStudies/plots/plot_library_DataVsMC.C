#include <iostream>
#include<stdlib.h>
#include<string.h>

#include <TFile.h>
#include <TString.h>

#include <TH1.h>
#include <TH1F.h>
#include <TTree.h>
#include <TGraph.h>
#include <TMultiGraph.h>

#include <TStyle.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TLatex.h>

using namespace std;

TString inRootFileMC_  = "../outRoot/MCstudiesT3m_MC_2022.root"; 
TString inRootFileDATA_  = "/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/ParkingDoubleMuonLowMass_2022E.root"; 
TString outPath_     = "/eos/user/c/cbasile/www/Tau3Mu_Run3/DataVsMC/";


void SetInputFile_DataMC(const TString& inFileDATA = "", const TString& inFileMC = ""){

  inRootFileMC_ = inFileMC;
  inRootFileDATA_ = inFileDATA;

}//SetInputFile()

void SetOutputFile(const TString& outPath = ""){

  outPath_ = outPath;


}//SetOutputFile()

TFile* open_file(const TString& dataset = "MC"){
    TString toOpen = "";
    if (dataset == "MC") toOpen = inRootFileMC_;
    else if (dataset == "Data") toOpen = inRootFileDATA_;
    TFile* input_file = new TFile(toOpen);

    if ( !input_file->IsOpen() ) {
       std::cout << "ERROR IN OPENING FILE "<< toOpen << std::endl;
       exit(-1);
    }

    return input_file;
}


Color_t PtlColorMap(const TString& particle){

  std::map <TString , Color_t> PtlColor{};
  PtlColor["MC"] = kRed;
  PtlColor["Data"] = kBlue;
  PtlColor["mu"]    = kPink + 4;
  PtlColor["muL"]   = kBlue + 2;
  PtlColor["muSL"]  = kGreen + 2;
  PtlColor["muT"]   = kOrange + 1;

  PtlColor["Tau_vc"]   = kRed - 7;
  PtlColor["Tau_gen"]  = kBlack;
  PtlColor["Tau_wovc"] = kBlue;

  PtlColor["PuppiMET"] = kViolet + 2;
  PtlColor["DeepMET"] = kCyan +2;

  PtlColor["W"] = kOrange;
  PtlColor["W_gen"] = kBlack;

  return PtlColor[particle];
}


TString CategoryLegend(const TString& category){

  std::map <TString , TString> Leg_entry{};
  Leg_entry["MC"] = "sgn (MC)";
  Leg_entry["Data"] = "bkg (data)";

  Leg_entry["mu"] = "#mu";
  Leg_entry["muL"] = "leading #mu";
  Leg_entry["muSL"] = "sub-leading #mu";
  Leg_entry["muT"] = "trailing #mu";

  Leg_entry["Tau_vc"] = "3 #mu refit";
  Leg_entry["Tau_gen"] = "#tau gen-level";
  Leg_entry["Tau_wovc"] = "3 #mu pre-refit";

  Leg_entry["PuppiMET"] = "PuppiMET";
  Leg_entry["DeepMET"] = "DeepMET";
  Leg_entry["W"] = "W reco-level";
  Leg_entry["W_gen"] = "W gen-level";


  return Leg_entry[category];
}

void histoSetUp(TH1* histo, const TString& category, const TString& x_name, bool fill = true , bool norm = true){

  //AXIS LABEL 
  histo->GetXaxis()->SetTitle(x_name);
  histo->GetXaxis()->SetTitleSize(0.04);
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

TString pngName(TString histo_name){

	TString pngName = outPath_ + histo_name + ".png";
	return pngName;
}
TString pdfName(TString histo_name){

	TString pdfName = outPath_ + histo_name + ".pdf";
	return pdfName;
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

int draw_one_histo(const TString& histo_name, const TString& dataset, const TString& x_name, TString out_name = "", bool LogY = false, bool fill = false){
    
    TFile* input_file = open_file(dataset);

    TH1F* h = (TH1F*)input_file->Get(histo_name);
    if ( !h ){
    std::cout<< "null pointer for histogram named " << histo_name << std::endl;
    exit(-1);
    }
    if (out_name == "") out_name = histo_name;

    histoSetUp(h, dataset, x_name, fill);
    h->SetMaximum(1.3*h->GetBinContent(h->GetMaximumBin()));

    auto legend = new TLegend(0.60,0.75,.80,.80);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.035);
    legend->AddEntry(h,CategoryLegend(dataset),"f");

    //STATISTICS
    gStyle->SetOptStat(0);

    //TEXT

    TCanvas* c1 = new TCanvas("c1","canvas", 1024,1024);
    c1->DrawFrame(0,0,1,1);
    h->Draw("HIST");
    legend->Draw();
    gPad->SetLeftMargin(0.13);
    gPad->SetBottomMargin(0.13);
    c1->Update(); 
    if (out_name == "") out_name = histo_name;
    if (LogY) c1->SetLogy();
    else c1->SetLogy(0);
    c1->SaveAs(pngName(out_name));
    c1->SaveAs(pdfName(out_name));

    input_file->Close();
    return 0;

}//draw_pT()


int draw_DataVsMC(const TString h_name, const TString& x_name, TString out_name = "", bool fill = true, bool LogY = false){

    TFile* input_file_data = open_file("Data");
    TFile* input_file_mc = open_file("MC");
    TH1F* h_data = (TH1F*)input_file_data->Get(h_name);
    TH1F* h_mc = (TH1F*)input_file_mc->Get(h_name);
    if ( !h_data ){
    std::cout<< "null pointer data for histogram named " << h_name << std::endl;
    exit(-1);
    }    
    if ( !h_mc ){
    std::cout<< "null pointer mc for histogram named " << h_name << std::endl;
    exit(-1);
    } 
    if (out_name == "") out_name = h_name+"DataVsMC";

    histoSetUp(h_data, "Data", x_name, fill);
    histoSetUp(h_mc, "MC", x_name, fill);
    

    //STATISTICS
    gStyle->SetOptStat(0);

    //SETMAXIMUM                                                                                                                                                                  
    double M1 = h_data->GetBinContent(h_data->GetMaximumBin());
    double M2 = h_mc->GetBinContent(h_mc->GetMaximumBin());
    if (M1 > M2){ h_data->SetMaximum(1.4*M1);
    }else {h_data->SetMaximum(1.4*M2);}

    //LEGEND
    auto legend = new TLegend(0.60,0.70,.85,.80);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.035);
    legend->AddEntry(h_data, CategoryLegend("Data") ,"f");
    legend->AddEntry(h_mc, CategoryLegend("MC") ,"f");

    TString png_name = pngName(out_name);
    TString pdf_name = pdfName(out_name);
    TCanvas* c1 = new TCanvas("c1","canvas", 1024,1024);

    h_data->Draw("HIST");
    h_mc->Draw("HIST SAME");
    gPad->SetLeftMargin(0.13);
    gPad->SetBottomMargin(0.13);
    gPad->RedrawAxis();
    legend->Draw();
    if (LogY) c1->SetLogy();
    else c1->SetLogy(0);
    c1->SaveAs(png_name);
    c1->SaveAs(pdf_name);

    input_file_data->Close();
    input_file_mc->Close();

    return 0;
}

int draw_many_histos(const std::vector<TString> histo_names,const std::vector<TString> categories, const TString& x_name, TString out_name = "", bool fill = false, bool LogY = false){

    TFile* input_file = open_file();
    TH1F* h1 = (TH1F*)input_file->Get(histo_names[0]);
    if ( !h1 ){
    std::cout<< "null pointer for histogram named " << histo_names[0] << std::endl;
    exit(-1);
    }    

    // set canva
    if (out_name == "") out_name = histo_names[0];
    TString png_name = pngName(out_name);
    TString pdf_name = pdfName(out_name);
    TCanvas* c1 = new TCanvas("c1","canvas", 1024,1024);
    //STATISTICS
    gStyle->SetOptStat(0);
    //LEGEND
    auto legend = new TLegend(0.60,0.70,.90,.80);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.035);

    // draw the first histogram
    histoSetUp(h1, categories[0], x_name, fill);
    float thisMax = h1->GetBinContent(h1->GetMaximumBin());
    legend->AddEntry(h1, CategoryLegend(categories[0]) ,"f");
    float globalMax = thisMax;
    h1->Draw("HIST");
    TH1F* h;
    
    for (unsigned int i = 1; i < histo_names.size(); i++){
        h = (TH1F*)input_file->Get(histo_names[i]);
        if ( !h ){
        std::cout<< "null pointer for histogram named " << histo_names[i] << std::endl;
        exit(-1);
        } 
        histoSetUp(h, categories[i], x_name, fill);
        //h1->GetYaxis()->SetTitle(Form("1/N dN/%.2f GeV", h1->GetXaxis()->GetBinWidth(1)));
        thisMax = h->GetBinContent(h->GetMaximumBin()); 
        if(thisMax>globalMax) globalMax = thisMax;                                                                                                                                                           
        
        legend->AddEntry(h, CategoryLegend(categories[i]) ,"f");
        h->Draw("HIST SAME");
    }
    h1->SetMaximum(1.4*globalMax);
    gPad->SetLeftMargin(0.13);
    gPad->SetBottomMargin(0.13);
    gPad->RedrawAxis();
    legend->Draw();
    if (LogY) c1->SetLogy();
    else c1->SetLogy(0);
    c1->Update();
    c1->SaveAs(png_name);
    c1->SaveAs(pdf_name);

    input_file->Close();

    return 0;
}


int draw_binary_histo(const TString h_MCmatch, const TString MC_category, const TString& title,TString out_name){

    TFile* input_file = open_file();

    TH1F* h1 = (TH1F*)input_file->Get(h_MCmatch);
    
    if ( !h1 ){
        std::cout<< "null pointer for histogram named " << h_MCmatch << std::endl;
        exit(-1);
    }
    

    TString category1 = MC_category; //, category2 = Fk_category;
    //SETUP
    histoSetUp(h1, category1, title);
    h1->GetYaxis()->SetRangeUser(0.01, 3.);
    h1->GetXaxis()->SetBinLabel(1, "FALSE"); h1->GetXaxis()->SetBinLabel(2, "TRUE");

    //STATISTICS
    gStyle->SetOptStat(0);
    gStyle->SetPaintTextFormat("1.2f");


    //LEGEND
    auto legend = new TLegend(0.62,0.8,.89,.89);
    legend->SetBorderSize(0);
    legend->AddEntry(h1, CategoryLegend(category1) ,"f");
    //legend->AddEntry(h2, CategoryLegend(category2) ,"f");

    TCanvas* c1 = new TCanvas("c1","canvas", 1024, 1024);
    gPad->SetLogy();
    h1->Draw("HIST TEXT0");
    gPad->RedrawAxis();
    gPad->SetMargin(0.12, 0.12, 0.1, 0.1);
    //legend->Draw();

    if (out_name == "") out_name = h_MCmatch;
    c1->SaveAs(pngName(out_name));
    c1->SaveAs(pdfName(out_name));
    input_file->Close();

    return 0;

}


void makeROCcurve(std::vector<TString> SGNhistos, std::vector<TString> BKGhistos, const TString out_name){

  TFile* input_file = open_file();
  TH1F* sigHist = new TH1F();
  TH1F* bkgHist = new TH1F();
  
  int Nobservables = SGNhistos.size();
  int nbins;  
  float sig_integral = 0, bkg_integral = 0;
  
  TCanvas* c1 = new TCanvas("c1","canvas", 1024, 1024);
  TGraph* vec_graph[Nobservables]; 
  TMultiGraph *mg = new TMultiGraph();

  //LEGEND
  auto legend = new TLegend(0.50,0.15,.80,.30);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.03);

  for (int j = 0; j < Nobservables; j++){

    sigHist = (TH1F*)input_file->Get(SGNhistos[j]);
    bkgHist = (TH1F*)input_file->Get(BKGhistos[j]);

    nbins = sigHist->GetNbinsX();
    sig_integral = sigHist->Integral(1,nbins);
    bkg_integral = bkgHist->Integral(1,nbins);
    std::cout << "Histo number " << j << std::endl;
    std::cout<<" total int  sig: "<<sig_integral<<" bkg: "<<bkg_integral<<std::endl;
    std::vector<float> sigPoints(nbins);
    std::vector<float> bkgPoints(nbins);
    for ( int i = nbins; i > 0; i-- ) {
      float sig_slice_integral = sigHist->Integral(i,nbins);
      float bkg_slice_integral = bkgHist->Integral(i,nbins);
      sigPoints.push_back(sig_slice_integral/sig_integral);
      bkgPoints.push_back(bkg_slice_integral/bkg_integral);

      std::cout<<i<<" "<<sig_slice_integral<<" "<<sig_slice_integral/sig_integral<<" "<<bkg_slice_integral<<" "<<bkg_slice_integral/bkg_integral<<std::endl;
    }
    
    vec_graph[j] = new TGraph(sigPoints.size(),&bkgPoints[0], &sigPoints[0]);
    vec_graph[j]->SetLineWidth(4);
    vec_graph[j]->SetLineColor(2+j);
    legend->AddEntry(vec_graph[j], SGNhistos[j], "l");
    mg->Add(vec_graph[j]);
    
    std::cout <<"\n -------------------------\n" << std::endl;
  } // on observables
  //g->GetXaxis()->SetTitle("signal efficiency"); g->GetYaxis()->SetTitle("background efficiency");

    c1->cd();
    mg->Draw("AL");
    mg->SetTitle("; background efficiency; signal efficiency");
    legend->Draw();
    c1->SaveAs(pngName(out_name));
    c1->SaveAs(pdfName(out_name));
  
  input_file->Close();

}




void compare_years(const TString& tree_name, const TString branch_name, const TString& selection, const int Nbins = 100, const float xlow = 0., const float xhigh = 100, TString x_name = " ", TString out_name = " "){

    //TFile* file_16preVFP = new TFile("outRoot/.root"); 
    TFile* file_16       = new TFile("/eos/user/c/cbasile/B0toX3872K0s/data/CharmoniumUL_2016_blind.root");
    TFile* file_17       = new TFile("/eos/user/c/cbasile/B0toX3872K0s/data/CharmoniumUL_2017_blind.root");
    TFile* file_18       = new TFile("/eos/user/c/cbasile/B0toX3872K0s/data/CharmoniumUL_2018_blind.root");

    //TTree* h_16preVFP = (TTree*)file_16preVFP->Get(tree_name);
    TTree* t_16= (TTree*)file_16->Get(tree_name);
    TH1F*  h_16= new TH1F("h_16", "", Nbins, xlow, xhigh);
    t_16->Draw(branch_name+">>h_16", selection);
    TTree* t_17= (TTree*)file_17->Get(tree_name);
    TH1F*  h_17= new TH1F("h_17", "", Nbins, xlow, xhigh);
    t_17->Draw(branch_name+">>h_17", selection);
    TTree* t_18= (TTree*)file_18->Get(tree_name);
    TH1F*  h_18= new TH1F("h_18", "", Nbins, xlow, xhigh);
    t_18->Draw(branch_name+">>h_18", selection);

    
    //histoSetUp(TH1* histo, const TString& category, const TString& x_name, bool fill = true , bool norm = true)
    //histoSetUp(h_16preVFP, "16preVFP", x_name, false, true);
    if(x_name == " ") x_name = branch_name;
    histoSetUp(h_16      , "16"      , x_name, false, true);
    histoSetUp(h_17      , "17"      , x_name, false, true);
    histoSetUp(h_18      , "18"      , x_name, false, true);

    gStyle->SetOptStat(0);
    gStyle->SetLineWidth(2);

    //LEGEND                                                                                                                                                                    
    auto legend = new TLegend(0.15,0.65,.40,.80);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.035);
    //legend->AddEntry(h_16preVFP,CategoryLegend("16preVFP"),"f");
    legend->AddEntry(h_16,CategoryLegend("16"),"f");
    legend->AddEntry(h_17,CategoryLegend("17"),"f");
    legend->AddEntry(h_18,CategoryLegend("18"),"f");

    TCanvas* c = new TCanvas("c", "", 800, 600);
    gPad->SetLeftMargin(0.13);
    gPad->SetBottomMargin(0.13);
    //h_16preVFP->Draw("hist");
    //h_16->SetMaximum(1.5*std::max( std::max(h_16preVFP->GetBinContent(h_16preVFP->GetMaximumBin()), h_16->GetBinContent(h_16->GetMaximumBin())) , 
     //                                       std::max(h_17->GetBinContent(h_17->GetMaximumBin()), h_18->GetBinContent(h_18->GetMaximumBin()) ) ) ); 
    h_16->SetMaximum(1.5*std::max( std::max(h_16->GetBinContent(h_16->GetMaximumBin()), h_17->GetBinContent(h_17->GetMaximumBin())) , 
                                            std::max(h_17->GetBinContent(h_17->GetMaximumBin()), h_18->GetBinContent(h_18->GetMaximumBin()) ) ) ); 
    h_16->Draw("hist");
    h_17->Draw("same hist");
    h_18->Draw("same hist");
    legend->Draw();
    if(out_name == " ") out_name = branch_name;
    c->SaveAs("/eos/user/c/cbasile/www/B0toX3872K0s/HLT-emulation/FullRun2_data/"+ out_name + ".png");
    c->SaveAs("/eos/user/c/cbasile/www/B0toX3872K0s/HLT-emulation/FullRun2_data/"+ out_name + ".pdf");


    //file_16preVFP->Close();
    file_16->Close();
    file_17->Close();
    file_18->Close();

}//compare_years()
