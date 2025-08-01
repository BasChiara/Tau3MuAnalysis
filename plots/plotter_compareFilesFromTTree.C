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
#include "tdrstyle.C"
#include "CMS_lumi.C"

std::vector<TString> inRootFile_;//  = {"/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/WTau3Mu_MC2017.root","../outRoot/recoKinematicsT3m_MC_2022EE_HLT_Tau3Mu.root", "../outRoot/recoKinematicsT3m_MC_2022EEreReco_HLT_Tau3Mu.root"}; 
std::vector<TString> treeName_;//    = {"tree","Tau3Mu_HLTemul_tree","Tau3Mu_HLTemul_tree"};
std::vector<TString> selections; 
TString outPath_     = "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/";

void SetInputFile(const std::vector<TString>& inFile){
  inRootFile_.erase(inRootFile_.begin(),inRootFile_.end());
  for(auto it = inFile.begin(); it != inFile.end(); it++){
     inRootFile_.push_back(*it);
  }
  setTDRStyle();
  extraText = "Preliminary";

}//SetInputFile()
void SetInputTree(const std::vector<TString>& inTree){
  treeName_.erase(treeName_.begin(),treeName_.end());
  for(auto it = inTree.begin(); it != inTree.end(); it++){
     treeName_.push_back(*it);
  }

}//SetInputTree()
void SetSelection(const std::vector<TString>& inSelection){
  selections.erase(selections.begin(),selections.end());
  for(auto it = inSelection.begin(); it != inSelection.end(); it++){
     selections.push_back(*it);
  }

}//SetSelection()
void SetOutputFile(const TString& outPath = ""){

  outPath_ = outPath;

}//SetOutputFile()

int draw_one_histo(const TString& branch_name, const TString& category, const TString& x_name, const int Nbins, const float x_low, const float x_high, TString out_name = "", bool logY = false, bool norm = true, bool fill = true )
{

  TFile* input_file = open_file(inRootFile_[0]);
  TTree* inTree = (TTree*)input_file->Get(treeName_[0]);
  if ( !inTree ){
    std::cout<< "null pointer to the TTree " << treeName_[0] << std::endl;
    exit(-1);
  }

  // draw the branch variable
  TH1F* h = new TH1F("h", "", Nbins, x_low, x_high);
  inTree->Draw(branch_name+">>h");
  histoSetUp(h, category, x_name, fill, norm);
  h->SetMaximum(1.4*h->GetBinContent(h->GetMaximumBin()));
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
  CMS_lumi( c1, 0 );
  c1->Update();
  gPad->Update();
  gPad->RedrawAxis();
  if (out_name == "") out_name = branch_name;
  TString outName = outPath_ + out_name;
  c1->SaveAs(outName+".png");
  c1->SaveAs(outName+".pdf");

  input_file->Close();

  return 0;

}// draw_one_histo()

int draw_branches(std::vector<TString> branches, std::vector<TString> categories,const TString& x_name, const int Nbins, const float x_low, const float x_high, TString out_name, bool logY = false, bool norm = true, bool fill = true)
{
  
   int Nfiles = inRootFile_.size(); 
   if (Nfiles != branches.size()){
      std::cout<< Form("[ERROR] files vector has %d elements while branches vector has %zu... they must have the same size!",Nfiles,branches.size()) << std::endl;
      exit(-1);
   }
   std::vector<TFile*> input_files(Nfiles, NULL);
   std::vector<TTree*> input_trees(Nfiles, NULL);
   std::vector<TH1F*>  histos(Nfiles, NULL);

   for (int i = 0; i < Nfiles; i++){
      input_files[i] = open_file(inRootFile_[i]);
      std::cout<< "[+] get TTree from file(s) : " << treeName_[i] << std::endl;
      input_trees[i] = (TTree*)input_files[i]->Get(treeName_[i]);
      if ( !input_trees[i]){
         std::cout<< "null pointer to the TTree " << treeName_[i] << std::endl;
         exit(-1);
      }
      histos[i] = new TH1F(Form("h_%d_"+branches[i],i), "", Nbins, x_low, x_high);
      input_trees[i]->Draw(Form(branches[i]+">>h_%d_"+branches[i],i), selections[i]);
      std::cout << Form(" histo %d with %.0f entries ", i, histos[i]->GetEntries() )<< std::endl;
   }
  
  // TCanvas
  TCanvas* c = new TCanvas("c","canvas", 800,800);
  c->DrawFrame(0,0,1,1);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.13);
  gStyle->SetOptStat(0);
  // TLegend
  float leg_entry_dy = 0.04;
  auto legend = new TLegend(0.50,0.80-branches.size()*leg_entry_dy,0.90,0.80);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.035);

  TString y_name = Form("Events / %.2f", histos[0]->GetXaxis()->GetBinWidth(1));
  THStack* stk = new THStack("hStack",";" + x_name + ";" + y_name);
  stk->GetXaxis()->SetTitleOffset(2.0);
  stk->GetYaxis()->SetTitleOffset(1.5);
  stk->GetXaxis()->SetTitleSize(0.045);
  stk->GetYaxis()->SetTitleSize(0.040);
  
  histoSetUp(histos[0], categories[0], x_name, fill, norm);
  legend->AddEntry(histos[0], CategoryLegend(categories[0]),"f");
  
  stk->Add(histos[0]);
  float maxY = histos[0]->GetBinContent(histos[0]->GetMaximumBin());
  for (int i = 1; i < Nfiles; i++){  
     histoSetUp(histos[i], categories[i], x_name, fill, norm);
     maxY = (histos[i]->GetBinContent(histos[i]->GetMaximumBin()) > maxY ? histos[i]->GetBinContent(histos[i]->GetMaximumBin()) : maxY);
     legend->AddEntry(histos[i], CategoryLegend(categories[i]),"f");
     //histos[i]->Draw("hist same");
     stk->Add(histos[i]);
  }
  stk->SetMaximum(1.4*maxY);
  stk->Draw("nostack HIST");
  legend->Draw();
  // semi-log scale
  if (logY) {
      c->SetLogy();
      stk->SetMaximum(2.0); 
   } else c->SetLogy(0);

  // save
  gPad->Modified(); gPad->Update();
  CMS_lumi( c, 0 );
  c->Update();
  gPad->Update();
  gPad->RedrawAxis();
  if (out_name == "") out_name = branches[0];
  TString outName = outPath_ + out_name;
  c->Update();
  c->SaveAs(outName+".png");
  c->SaveAs(outName+".pdf");

  for(int i = 0; i< Nfiles; i++)  input_files[i]->Close();

  return 0;

}// draw_branches()

int draw_2D_branches(std::vector<TString> branches_xy, std::vector<TString> categories,const TString& x_name, const int xNbins, const float x_low, const float x_high, const TString& y_name, const int yNbins, const float y_low, const float y_high, TString out_name, bool norm = true, bool fill = true)
{
   int Nfiles  = inRootFile_.size(); 
   if (Nfiles != categories.size()){
      std::cout<< Form("[ERROR] files vector has %d elements while categories vector has %zu... they must have the same size!",Nfiles,categories.size()) << std::endl;
      exit(-1);
   }

   std::vector<TFile*> input_files(Nfiles, NULL);
   std::vector<TTree*> input_trees(Nfiles, NULL);
   std::vector<TH2F*>  histos(Nfiles, NULL);

   for (int i = 0; i < Nfiles; i++){
      input_files[i] = open_file(inRootFile_[i]);
      std::cout<< "[+] get TTree from file(s) : " << treeName_[i] << std::endl;
      input_trees[i] = (TTree*)input_files[i]->Get(treeName_[i]);
      if ( !input_trees[i]){
         std::cout<< "null pointer to the TTree " << treeName_[i] << std::endl;
         exit(-1);
      }
      TString hist_name = Form("h_%d_"+branches_xy[0]+"VS"+branches_xy[1],i);
      histos[i] = new TH2F(hist_name, "", xNbins, x_low, x_high, yNbins, y_low, y_high);
      input_trees[i]->Draw(branches_xy[1]+":"+branches_xy[0]+">>"+hist_name, selections[i]);
      std::cout << Form(" histo %d with %.0f entries ", i, histos[i]->GetEntries() )<< std::endl;
   }
   // TCanvas
   TCanvas* c = new TCanvas("c","canvas", 800,800);
   c->DrawFrame(0,0,1,1);
   gPad->SetLeftMargin(0.13);
   gPad->SetBottomMargin(0.13);
   gStyle->SetOptStat(0);
   // TLegend
   float leg_entry_dy = 0.04;
   auto legend = new TLegend(0.50,0.80-categories.size()*leg_entry_dy,0.90,0.80);
   legend->SetBorderSize(0);
   legend->SetTextSize(0.035);

   histoSetUp(histos[0], categories[0], x_name, fill, norm);
   legend->AddEntry(histos[0], CategoryLegend(categories[0]),"f");
   histos[0]->GetYaxis()->SetTitle(y_name);
   
   //stk->GetXaxis()->SetTitleOffset(2.0);stk->GetYaxis()->SetTitleOffset(1.5);
   //stk->GetXaxis()->SetTitleSize(0.045); stk->GetYaxis()->SetTitleSize(0.040);
   gPad->Modified(); gPad->Update();
   //stk->Add(histos[0]);
   
   float maxY = histos[0]->GetBinContent(histos[0]->GetMaximumBin());
   histos[0]->Draw("box");
   for (int i = 1; i < Nfiles; i++){  
      histoSetUp(histos[i], categories[i], x_name, fill, norm);
      maxY = (histos[i]->GetBinContent(histos[i]->GetMaximumBin()) > maxY ? histos[i]->GetBinContent(histos[i]->GetMaximumBin()) : maxY);
      legend->AddEntry(histos[i], CategoryLegend(categories[i]),"f");
      histos[i]->Draw("box same");
      //stk->Add(histos[i]);
   }
   legend->Draw();

   // save
   CMS_lumi( c, 0 );
   c->Update();
   gPad->Update();
   gPad->RedrawAxis();
   if (out_name == "") out_name = branches_xy[0]+"VS"+branches_xy[1];
   TString outName = outPath_ + out_name;
   c->Update();
   c->SaveAs(outName+".png");
   c->SaveAs(outName+".pdf");

   for(int i = 0; i< Nfiles; i++)  input_files[i]->Close();

   return 0;
}// draw_2D_braches()

int draw_histos(std::vector<TString> histo_names, std::vector<TString> categories,const TString& x_name, TString out_name, bool logY = false, bool norm = true, bool fill = true)
{
  
   int Nfiles = inRootFile_.size(); 
   if (Nfiles != histo_names.size()){
      std::cout<< Form("[ERROR] files vector has %d elements while histos vector has %d... they must have the same size!",Nfiles,histo_names.size()) << std::endl;
      exit(-1);
   }
   std::vector<TFile*> input_files(Nfiles, NULL);
   std::vector<TH1F*>  histos(Nfiles, NULL);

   for (int i = 0; i < Nfiles; i++){
      input_files[i] = open_file(inRootFile_[i]);
      histos[i] = (TH1F*)input_files[i]->Get(histo_names[i]); 
      std::cout << Form(" histo %d with %.0f entries ", i, histos[i]->GetEntries() )<< std::endl;
   }
  
  // TCanvas
  TCanvas* c = new TCanvas("c","canvas", 800,800);
  c->DrawFrame(0,0,1,1);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.13);
  gStyle->SetOptStat(0);
  // TLegend
  float leg_entry_dy = 0.04;
  auto legend = new TLegend(0.60,.80-histos.size()*leg_entry_dy,0.85,0.80);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.035);

  TString y_name = Form("Events / %.2f", histos[0]->GetXaxis()->GetBinWidth(1));
  THStack* stk = new THStack("hStack",";" + x_name + ";" + y_name);
  histoSetUp(histos[0], categories[0], x_name, fill, norm);
  legend->AddEntry(histos[0], CategoryLegend(categories[0]),"f");
  stk->Add(histos[0]);
  float maxY = histos[0]->GetBinContent(histos[0]->GetMaximumBin());
  for (int i = 1; i < Nfiles; i++){  
     histoSetUp(histos[i], categories[i], x_name, fill, norm);
     maxY = (histos[i]->GetBinContent(histos[i]->GetMaximumBin()) > maxY ? histos[i]->GetBinContent(histos[i]->GetMaximumBin()) : maxY);
     legend->AddEntry(histos[i], CategoryLegend(categories[i]),"f");
     stk->Add(histos[i]);
  }
  stk->SetMaximum(1.4*maxY);
  stk->Draw("nostack HIST");
  legend->Draw();
  // semi-log scale
  if (logY) c->SetLogy();
  else c->SetLogy(0);

  // save
  CMS_lumi( c, 0 );
  c->Update();
  gPad->Update();
  gPad->RedrawAxis();
  if (out_name == "") out_name = histo_names[0];
  TString outName = outPath_ + out_name;
  c->Update();
  c->SaveAs(outName+".png");
  c->SaveAs(outName+".pdf");

  for(int i = 0; i< Nfiles; i++)  input_files[i]->Close();

  return 0;

}// draw_histos()

