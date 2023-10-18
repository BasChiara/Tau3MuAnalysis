#include <iostream>
#include <vector>

#include <TFile.h>
#include <TString.h>

#include <TH1.h>
#include <TH2.h>
#include <TH1F.h>
#include <THStack.h>
#include <TTree.h>
#include <TGraph.h>
#include <TMultiGraph.h>

#include <TStyle.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TLatex.h>

#include "common_utils.C"

TString inRootFile_  = "../outRoot/MCstudiesT3m_MC_2022preEE.root"; 
TString outPath_     = "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/";
TString treeName_    = "Tau3Mu_HLTemul_tree";




void SetInputFile(const TString& inFile = ""){

  inRootFile_ = inFile;

}//SetInputFile()
void SetOutputFile(const TString& outPath = ""){

  outPath_ = outPath;

}//SetOutputFile()
void SetIO(const TString& inFile = "", const TString& tree_name = "", const TString& outPath = ""){
  
  inRootFile_ = inFile;
  treeName_ = tree_name;
  outPath_ = outPath;

}//SetOutputFile()

int draw_one_histo(const TString& branch_name, const TString& category, const TString& x_name, const int Nbins, const float x_low, const float x_high, TString out_name = "", bool logY = false, bool norm = true, bool fill = true )
{

  TFile* input_file = open_file(inRootFile_);
  TTree* inTree = (TTree*)input_file->Get(treeName_);
  if ( !inTree ){
    std::cout<< "null pointer to the TTree " << treeName_ << std::endl;
    exit(-1);
  }

  // draw the branch variable
  TH1F* h = new TH1F("h", "", Nbins, x_low, x_high);
  inTree->Draw(branch_name+">>h");
  histoSetUp(h, category, x_name, fill, norm);
  // canva
  TCanvas* c1 = new TCanvas("c1","canvas", 800,800);
  c1->DrawFrame(0,0,1,1);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.13);
  gStyle->SetOptStat(0);

  h->Draw("HIST");

  c1->Update();
  
  // semi log scale
  if (logY) c1->SetLogy();
  else c1->SetLogy(0);

  // save
  if (out_name == "") out_name = branch_name;
  TString outName = outPath_ + out_name;
  c1->SaveAs(outName+".png");
  c1->SaveAs(outName+".pdf");

  input_file->Close();

  return 0;

}// draw_one_histo()

int draw_many_histos(std::vector<TString> branches, std::vector<TString> categories,const TString& x_name, const int Nbins, const float x_low, const float x_high, TString out_name, bool logY = false, bool norm = true, bool fill = true)
{

  TFile* input_file = open_file(inRootFile_);
  TTree* inTree = (TTree*)input_file->Get(treeName_);
  if ( !inTree ){
    std::cout<< "null pointer to the TTree " << treeName_ << std::endl;
    exit(-1);
  }

  // TCanvas
  TCanvas* c = new TCanvas("c","canvas", 800,800);
  c->DrawFrame(0,0,1,1);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.13);
  gStyle->SetOptStat(0);
  // TLegend
  float leg_entry_dy = 0.3
  auto legend = new TLegend(0.60,0.80-branches.size()*leg_entry_dy,0.80,0.80);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.035);

  
  TH1F* h0 = new TH1F("h0", "", Nbins, x_low, x_high);
  inTree->Draw(branches[0]+">>h0");
  histoSetUp(h0, categories[0], x_name, fill, norm);
  legend->AddEntry(h0, CategoryLegend(categories[0]),"f");
  float maxY = h0->GetBinContent(h0->GetMaximumBin());
  
  TString y_name = Form("Events / %.2f", h0->GetXaxis()->GetBinWidth(1));
  THStack* stk = new THStack("hStack",";" + x_name + ";" + y_name);
  stk->Add(h0);
  
  c->cd();
  for(unsigned int i = 1; i < branches.size(); i++){
    TH1F* h = new TH1F(Form("h_%d",i), "", Nbins, x_low, x_high);
    inTree->Draw(branches[i]+Form(">>h_%d",i));
    histoSetUp(h, categories[i], x_name, fill, norm);
    std::cout << " max : " << h->GetBinContent(h->GetMaximumBin()) << std::endl;
    legend->AddEntry(h, CategoryLegend(categories[i]),"f");
    maxY = (h->GetBinContent(h->GetMaximumBin()) > maxY ? h->GetBinContent(h->GetMaximumBin()) : maxY);
    stk->Add(h);
  }
  stk->SetMaximum(1.4*maxY);
  stk->Draw("nostack HIST");
  legend->Draw();
  // semi-log scale
  if (logY) c->SetLogy();
  else c->SetLogy(0);

  // save
  if (out_name == "") out_name = branches[0];
  TString outName = outPath_ + out_name;
  c->SaveAs(outName+".png");
  c->SaveAs(outName+".pdf");

  input_file->Close();

  return 0;

}// draw_many_histos()