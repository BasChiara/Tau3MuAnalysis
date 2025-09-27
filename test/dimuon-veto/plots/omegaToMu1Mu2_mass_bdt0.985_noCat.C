#ifdef __CLING__
#pragma cling optimize(0)
#endif
void omegaToMu1Mu2_mass_bdt0.985_noCat()
{
//=========Macro generated from canvas: c/c
//=========  (Tue Sep 23 16:55:51 2025) by ROOT version 6.26/11
   TCanvas *c = new TCanvas("c", "c",0,0,1024,1024);
   c->SetHighLightColor(2);
   c->Range(0,0,1,1);
   c->SetFillColor(0);
   c->SetBorderMode(0);
   c->SetBorderSize(2);
   c->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: up_pad
   TPad *up_pad = new TPad("up_pad", "",0,0.3,1,1);
   up_pad->Draw();
   up_pad->cd();
   up_pad->Range(0.67,0,0.87,12.56533);
   up_pad->SetFillColor(0);
   up_pad->SetBorderMode(0);
   up_pad->SetBorderSize(2);
   up_pad->SetLeftMargin(0.15);
   up_pad->SetBottomMargin(0);
   up_pad->SetFrameBorderMode(0);
   up_pad->SetFrameBorderMode(0);
   
   TH1D *frame_95392f0__1 = new TH1D("frame_95392f0__1","#omega#rightarrow#mu#mu",100,0.7,0.85);
   frame_95392f0__1->SetBinContent(1,11.30879);
   frame_95392f0__1->SetMaximum(11.30879);
   frame_95392f0__1->SetEntries(1);
   frame_95392f0__1->SetDirectory(0);
   frame_95392f0__1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   frame_95392f0__1->SetLineColor(ci);
   frame_95392f0__1->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_95392f0__1->GetXaxis()->SetLabelFont(42);
   frame_95392f0__1->GetXaxis()->SetTitleOffset(1);
   frame_95392f0__1->GetXaxis()->SetTitleFont(42);
   frame_95392f0__1->GetYaxis()->SetTitle("Events / ( 0.005 GeV )");
   frame_95392f0__1->GetYaxis()->SetLabelFont(42);
   frame_95392f0__1->GetYaxis()->SetTitleFont(42);
   frame_95392f0__1->GetZaxis()->SetLabelFont(42);
   frame_95392f0__1->GetZaxis()->SetTitleOffset(1);
   frame_95392f0__1->GetZaxis()->SetTitleFont(42);
   frame_95392f0__1->Draw("FUNC");
   
   Double_t data_fx3001[30] = {
   0.7025,
   0.7075,
   0.7125,
   0.7175,
   0.7225,
   0.7275,
   0.7325,
   0.7375,
   0.7425,
   0.7475,
   0.7525,
   0.7575,
   0.7625,
   0.7675,
   0.7725,
   0.7775,
   0.7825,
   0.7875,
   0.7925,
   0.7975,
   0.8025,
   0.8075,
   0.8125,
   0.8175,
   0.8225,
   0.8275,
   0.8325,
   0.8375,
   0.8425,
   0.8475};
   Double_t data_fy3001[30] = {
   3,
   3,
   2,
   4,
   1,
   2,
   3,
   2,
   3,
   2,
   3,
   5,
   4,
   4,
   1,
   6,
   4,
   3,
   5,
   5,
   2,
   4,
   7,
   7,
   3,
   4,
   3,
   5,
   4,
   4};
   Double_t data_felx3001[30] = {
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025};
   Double_t data_fely3001[30] = {
   1.632705,
   1.632705,
   1.291815,
   1.914339,
   0.8272462,
   1.291815,
   1.632705,
   1.291815,
   1.632705,
   1.291815,
   1.632705,
   2.159691,
   1.914339,
   1.914339,
   0.8272462,
   2.379931,
   1.914339,
   1.632705,
   2.159691,
   2.159691,
   1.291815,
   1.914339,
   2.58147,
   2.58147,
   1.632705,
   1.914339,
   1.632705,
   2.159691,
   1.914339,
   1.914339};
   Double_t data_fehx3001[30] = {
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025,
   0.0025};
   Double_t data_fehy3001[30] = {
   2.918186,
   2.918186,
   2.63786,
   3.162753,
   2.299527,
   2.63786,
   2.918186,
   2.63786,
   2.918186,
   2.63786,
   2.918186,
   3.382473,
   3.162753,
   3.162753,
   2.299527,
   3.583642,
   3.162753,
   2.918186,
   3.382473,
   3.382473,
   2.63786,
   3.162753,
   3.770281,
   3.770281,
   2.918186,
   3.162753,
   2.918186,
   3.382473,
   3.162753,
   3.162753};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(30,data_fx3001,data_fy3001,data_felx3001,data_fehx3001,data_fely3001,data_fehy3001);
   grae->SetName("data");
   grae->SetTitle("Histogram of data_plot__tau_mu12_fitM");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_data3001 = new TH1F("Graph_data3001","Histogram of data_plot__tau_mu12_fitM",100,0.685,0.865);
   Graph_data3001->SetMinimum(0.1554784);
   Graph_data3001->SetMaximum(11.83003);
   Graph_data3001->SetDirectory(0);
   Graph_data3001->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_data3001->SetLineColor(ci);
   Graph_data3001->GetXaxis()->SetLabelFont(42);
   Graph_data3001->GetXaxis()->SetTitleOffset(1);
   Graph_data3001->GetXaxis()->SetTitleFont(42);
   Graph_data3001->GetYaxis()->SetLabelFont(42);
   Graph_data3001->GetYaxis()->SetTitleFont(42);
   Graph_data3001->GetZaxis()->SetLabelFont(42);
   Graph_data3001->GetZaxis()->SetTitleOffset(1);
   Graph_data3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_data3001);
   
   grae->Draw("p");
   
   Double_t full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx1[102] = {
   0.7,
   0.7015,
   0.703,
   0.7045,
   0.706,
   0.7075,
   0.709,
   0.7105,
   0.712,
   0.7135,
   0.715,
   0.7165,
   0.718,
   0.7195,
   0.721,
   0.7225,
   0.724,
   0.7255,
   0.727,
   0.7285,
   0.73,
   0.7315,
   0.733,
   0.7345,
   0.736,
   0.7375,
   0.739,
   0.7405,
   0.742,
   0.7435,
   0.745,
   0.7465,
   0.748,
   0.7495,
   0.751,
   0.7525,
   0.754,
   0.7555,
   0.757,
   0.7585,
   0.76,
   0.7615,
   0.763,
   0.7645,
   0.766,
   0.7675,
   0.769,
   0.7705,
   0.772,
   0.7735,
   0.775,
   0.7765,
   0.778,
   0.7795,
   0.781,
   0.7825,
   0.784,
   0.7855,
   0.787,
   0.7885,
   0.79,
   0.7915,
   0.793,
   0.7945,
   0.796,
   0.7975,
   0.799,
   0.8005,
   0.802,
   0.8035,
   0.805,
   0.8065,
   0.808,
   0.8095,
   0.811,
   0.8125,
   0.814,
   0.8155,
   0.817,
   0.8185,
   0.82,
   0.8215,
   0.823,
   0.8245,
   0.826,
   0.8275,
   0.829,
   0.8305,
   0.832,
   0.8335,
   0.835,
   0.8365,
   0.838,
   0.8395,
   0.841,
   0.8425,
   0.844,
   0.8455,
   0.847,
   0.8485,
   0.85,
   0.85};
   Double_t full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy1[102] = {
   2.349172,
   2.372855,
   2.396539,
   2.420223,
   2.443906,
   2.46759,
   2.491274,
   2.514957,
   2.538641,
   2.562325,
   2.586008,
   2.609692,
   2.633376,
   2.657059,
   2.680743,
   2.704426,
   2.72811,
   2.751794,
   2.775477,
   2.799161,
   2.822845,
   2.846529,
   2.870213,
   2.893899,
   2.917586,
   2.941276,
   2.964971,
   2.988678,
   3.012403,
   3.036161,
   3.059973,
   3.083875,
   3.107921,
   3.13219,
   3.156799,
   3.181908,
   3.207734,
   3.234557,
   3.262729,
   3.292665,
   3.324836,
   3.359739,
   3.397859,
   3.439611,
   3.485272,
   3.534908,
   3.5883,
   3.644896,
   3.703771,
   3.763651,
   3.822956,
   3.87991,
   3.932677,
   3.979529,
   4.01901,
   4.050093,
   4.072285,
   4.085688,
   4.090979,
   4.089344,
   4.082348,
   4.071773,
   4.059453,
   4.047114,
   4.03624,
   4.027996,
   4.023179,
   4.022227,
   4.025255,
   4.03212,
   4.04249,
   4.055921,
   4.071917,
   4.089986,
   4.109674,
   4.130586,
   4.152395,
   4.174841,
   4.197728,
   4.220911,
   4.244288,
   4.267788,
   4.291364,
   4.314987,
   4.338636,
   4.362302,
   4.385975,
   4.409654,
   4.433335,
   4.457017,
   4.4807,
   4.504384,
   4.528067,
   4.551751,
   4.575434,
   4.599118,
   4.622802,
   4.646485,
   4.670169,
   4.693853,
   4.717536,
   4.717536};
   TGraph *graph = new TGraph(102,full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx1,full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy1);
   graph->SetName("full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]");
   graph->SetTitle("Projection of full_model");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff0000");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   
   TH1F *Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1 = new TH1F("Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1","Projection of full_model",102,0.685,0.865);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetMinimum(2.112335);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetMaximum(4.954373);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetDirectory(0);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetLineColor(ci);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetXaxis()->SetLabelFont(42);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetXaxis()->SetTitleOffset(1);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetXaxis()->SetTitleFont(42);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetYaxis()->SetLabelFont(42);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetYaxis()->SetTitleFont(42);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetZaxis()->SetLabelFont(42);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetZaxis()->SetTitleOffset(1);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]1);
   
   graph->Draw("l");
   TLatex *   tex = new TLatex(0.71,2.261759,"#sigma = (10.0 #pm 0.0) MeV");
   tex->SetTextFont(42);
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.71,-497.7382,"#chi^{2}/nDoF = 0.29");
   tex->SetTextFont(42);
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
   
   TH1D *frame_95392f0__2 = new TH1D("frame_95392f0__2","#omega#rightarrow#mu#mu",100,0.7,0.85);
   frame_95392f0__2->SetBinContent(1,11.30879);
   frame_95392f0__2->SetMaximum(11.30879);
   frame_95392f0__2->SetEntries(1);
   frame_95392f0__2->SetDirectory(0);
   frame_95392f0__2->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_95392f0__2->SetLineColor(ci);
   frame_95392f0__2->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_95392f0__2->GetXaxis()->SetLabelFont(42);
   frame_95392f0__2->GetXaxis()->SetTitleOffset(1);
   frame_95392f0__2->GetXaxis()->SetTitleFont(42);
   frame_95392f0__2->GetYaxis()->SetTitle("Events / ( 0.005 GeV )");
   frame_95392f0__2->GetYaxis()->SetLabelFont(42);
   frame_95392f0__2->GetYaxis()->SetTitleFont(42);
   frame_95392f0__2->GetZaxis()->SetLabelFont(42);
   frame_95392f0__2->GetZaxis()->SetTitleOffset(1);
   frame_95392f0__2->GetZaxis()->SetTitleFont(42);
   frame_95392f0__2->Draw("AXISSAME");
   
   TPaveText *pt = new TPaveText(0.44,0.94,0.56,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   TText *pt_LaTex = pt->AddText("#omega#rightarrow#mu#mu");
   pt->Draw();
   up_pad->Modified();
   c->cd();
  
// ------------>Primitives in pad: ratio_pad
   TPad *ratio_pad = new TPad("ratio_pad", "",0,0,1,0.28);
   ratio_pad->Draw();
   ratio_pad->cd();
   ratio_pad->Range(0.67,-12.83333,0.87,5.5);
   ratio_pad->SetFillColor(0);
   ratio_pad->SetBorderMode(0);
   ratio_pad->SetBorderSize(2);
   ratio_pad->SetLeftMargin(0.15);
   ratio_pad->SetTopMargin(0);
   ratio_pad->SetBottomMargin(0.4);
   ratio_pad->SetFrameBorderMode(0);
   ratio_pad->SetFrameBorderMode(0);
   
   TH1D *frame_9e8c8f0__3 = new TH1D("frame_9e8c8f0__3"," ",100,0.7,0.85);
   frame_9e8c8f0__3->SetBinContent(1,5.5);
   frame_9e8c8f0__3->SetMinimum(-5.5);
   frame_9e8c8f0__3->SetMaximum(5.5);
   frame_9e8c8f0__3->SetEntries(1);
   frame_9e8c8f0__3->SetDirectory(0);
   frame_9e8c8f0__3->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_9e8c8f0__3->SetLineColor(ci);
   frame_9e8c8f0__3->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_9e8c8f0__3->GetXaxis()->SetLabelFont(42);
   frame_9e8c8f0__3->GetXaxis()->SetLabelSize(0.1);
   frame_9e8c8f0__3->GetXaxis()->SetTitleSize(0.1);
   frame_9e8c8f0__3->GetXaxis()->SetTitleOffset(1);
   frame_9e8c8f0__3->GetXaxis()->SetTitleFont(42);
   frame_9e8c8f0__3->GetYaxis()->SetTitle("Pull");
   frame_9e8c8f0__3->GetYaxis()->SetLabelFont(42);
   frame_9e8c8f0__3->GetYaxis()->SetLabelSize(0.1);
   frame_9e8c8f0__3->GetYaxis()->SetTitleSize(0.1);
   frame_9e8c8f0__3->GetYaxis()->SetTitleFont(42);
   frame_9e8c8f0__3->GetZaxis()->SetLabelFont(42);
   frame_9e8c8f0__3->GetZaxis()->SetTitleOffset(1);
   frame_9e8c8f0__3->GetZaxis()->SetTitleFont(42);
   frame_9e8c8f0__3->Draw("FUNC");
   
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx3002[30] = {
   0.7025,
   0.7075,
   0.7125,
   0.7175,
   0.7225,
   0.7275,
   0.7325,
   0.7375,
   0.7425,
   0.7475,
   0.7525,
   0.7575,
   0.7625,
   0.7675,
   0.7725,
   0.7775,
   0.7825,
   0.7875,
   0.7925,
   0.7975,
   0.8025,
   0.8075,
   0.8125,
   0.8175,
   0.8225,
   0.8275,
   0.8325,
   0.8375,
   0.8425,
   0.8475};
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy3002[30] = {
   0.3744434,
   0.3260908,
   -0.207189,
   0.7180123,
   -0.7412076,
   -0.2969726,
   0.08432698,
   -0.3568344,
   -0.006969889,
   -0.4170019,
   -0.06247254,
   0.7994032,
   0.3203881,
   0.2418842,
   -1.18457,
   0.877017,
   -0.0143048,
   -0.3727137,
   0.4337115,
   0.4492045,
   -0.7692444,
   -0.02135788,
   1.11135,
   1.082495,
   -0.4398383,
   -0.1145542,
   -0.4938786,
   0.222174,
   -0.1894293,
   -0.2143903};
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_felx3002[30] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fely3002[30] = {
   1,
   1,
   0.4897207,
   1,
   0.3597463,
   0.4897207,
   1,
   0.4897207,
   0.559493,
   0.4897207,
   0.559493,
   1,
   1,
   1,
   0.3597463,
   1,
   0.6052762,
   0.559493,
   1,
   1,
   0.4897207,
   0.6052762,
   1,
   1,
   0.559493,
   0.6052762,
   0.559493,
   1,
   0.6052762,
   0.6052762};
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehx3002[30] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehy3002[30] = {
   1.787332,
   1.787332,
   1,
   1.652138,
   1,
   1,
   1.787332,
   1,
   1,
   1,
   1,
   1.566184,
   1.652138,
   1.652138,
   1,
   1.505775,
   1,
   1,
   1.566184,
   1.566184,
   1,
   1,
   1.460517,
   1.460517,
   1,
   1,
   1,
   1.566184,
   1,
   1};
   grae = new TGraphAsymmErrors(30,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_felx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fely3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehy3002);
   grae->SetName("pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]");
   grae->SetTitle("Pull of Histogram of data_plot__tau_mu12_fitM and Projection of full_model");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002 = new TH1F("Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002","Pull of Histogram of data_plot__tau_mu12_fitM and Projection of full_model",100,0.688,0.862);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetMinimum(-1.955935);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetMaximum(2.983485);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetDirectory(0);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetLineColor(ci);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetXaxis()->SetRange(7,94);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetXaxis()->SetLabelFont(42);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetXaxis()->SetTitleOffset(1);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetXaxis()->SetTitleFont(42);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetYaxis()->SetTitle("(Data - curve) / #sigma_{data}");
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetYaxis()->SetLabelFont(42);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetYaxis()->SetTitleFont(42);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetZaxis()->SetLabelFont(42);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetZaxis()->SetTitleOffset(1);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]3002);
   
   grae->Draw("p");
   
   TH1D *frame_9e8c8f0__4 = new TH1D("frame_9e8c8f0__4"," ",100,0.7,0.85);
   frame_9e8c8f0__4->SetBinContent(1,5.5);
   frame_9e8c8f0__4->SetMinimum(-5.5);
   frame_9e8c8f0__4->SetMaximum(5.5);
   frame_9e8c8f0__4->SetEntries(1);
   frame_9e8c8f0__4->SetDirectory(0);
   frame_9e8c8f0__4->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_9e8c8f0__4->SetLineColor(ci);
   frame_9e8c8f0__4->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_9e8c8f0__4->GetXaxis()->SetLabelFont(42);
   frame_9e8c8f0__4->GetXaxis()->SetLabelSize(0.1);
   frame_9e8c8f0__4->GetXaxis()->SetTitleSize(0.1);
   frame_9e8c8f0__4->GetXaxis()->SetTitleOffset(1);
   frame_9e8c8f0__4->GetXaxis()->SetTitleFont(42);
   frame_9e8c8f0__4->GetYaxis()->SetTitle("Pull");
   frame_9e8c8f0__4->GetYaxis()->SetLabelFont(42);
   frame_9e8c8f0__4->GetYaxis()->SetLabelSize(0.1);
   frame_9e8c8f0__4->GetYaxis()->SetTitleSize(0.1);
   frame_9e8c8f0__4->GetYaxis()->SetTitleFont(42);
   frame_9e8c8f0__4->GetZaxis()->SetLabelFont(42);
   frame_9e8c8f0__4->GetZaxis()->SetTitleOffset(1);
   frame_9e8c8f0__4->GetZaxis()->SetTitleFont(42);
   frame_9e8c8f0__4->Draw("AXISSAME");
   
   pt = new TPaveText(0.4870588,0.94,0.5129412,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   pt_LaTex = pt->AddText(" ");
   pt->Draw();
   ratio_pad->Modified();
   c->cd();
   c->Modified();
   c->cd();
   c->SetSelected(c);
}
