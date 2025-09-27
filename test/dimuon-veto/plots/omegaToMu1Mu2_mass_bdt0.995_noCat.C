#ifdef __CLING__
#pragma cling optimize(0)
#endif
void omegaToMu1Mu2_mass_bdt0.995_noCat()
{
//=========Macro generated from canvas: c/c
//=========  (Tue Sep 23 16:56:28 2025) by ROOT version 6.26/11
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
   up_pad->Range(0.67,0,0.87,6.90455);
   up_pad->SetFillColor(0);
   up_pad->SetBorderMode(0);
   up_pad->SetBorderSize(2);
   up_pad->SetLeftMargin(0.15);
   up_pad->SetBottomMargin(0);
   up_pad->SetFrameBorderMode(0);
   up_pad->SetFrameBorderMode(0);
   
   TH1D *frame_a0c20a0__1 = new TH1D("frame_a0c20a0__1","#omega#rightarrow#mu#mu",100,0.7,0.85);
   frame_a0c20a0__1->SetBinContent(1,6.214095);
   frame_a0c20a0__1->SetMaximum(6.214095);
   frame_a0c20a0__1->SetEntries(1);
   frame_a0c20a0__1->SetDirectory(0);
   frame_a0c20a0__1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   frame_a0c20a0__1->SetLineColor(ci);
   frame_a0c20a0__1->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_a0c20a0__1->GetXaxis()->SetLabelFont(42);
   frame_a0c20a0__1->GetXaxis()->SetTitleOffset(1);
   frame_a0c20a0__1->GetXaxis()->SetTitleFont(42);
   frame_a0c20a0__1->GetYaxis()->SetTitle("Events / ( 0.005 GeV )");
   frame_a0c20a0__1->GetYaxis()->SetLabelFont(42);
   frame_a0c20a0__1->GetYaxis()->SetTitleFont(42);
   frame_a0c20a0__1->GetZaxis()->SetLabelFont(42);
   frame_a0c20a0__1->GetZaxis()->SetTitleOffset(1);
   frame_a0c20a0__1->GetZaxis()->SetTitleFont(42);
   frame_a0c20a0__1->Draw("FUNC");
   
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
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   1,
   1,
   1,
   1,
   0,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   2,
   2,
   1,
   1,
   3,
   0,
   2};
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
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   0.8272462,
   1.291815,
   1.291815,
   0.8272462,
   0.8272462,
   1.632705,
   0,
   1.291815};
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
   1.147874,
   1.147874,
   1.147874,
   1.147874,
   1.147874,
   1.147874,
   1.147874,
   1.147874,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   1.147874,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.299527,
   2.63786,
   2.63786,
   2.299527,
   2.299527,
   2.918186,
   1.147874,
   2.63786};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(30,data_fx3001,data_fy3001,data_felx3001,data_fehx3001,data_fely3001,data_fehy3001);
   grae->SetName("data");
   grae->SetTitle("Histogram of data_plot__tau_mu12_fitM");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_data3001 = new TH1F("Graph_data3001","Histogram of data_plot__tau_mu12_fitM",100,0.685,0.865);
   Graph_data3001->SetMinimum(0);
   Graph_data3001->SetMaximum(6.510004);
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
   5.314173e-08,
   0.01666671,
   0.03333336,
   0.05000002,
   0.06666667,
   0.08333333,
   0.09999998,
   0.1166666,
   0.1333333,
   0.1499999,
   0.1666666,
   0.1833333,
   0.1999999,
   0.2166666,
   0.2333332,
   0.2499999,
   0.2666665,
   0.2833332,
   0.2999998,
   0.3166665,
   0.3333332,
   0.3499998,
   0.3666665,
   0.3833331,
   0.3999998,
   0.4166664,
   0.4333331,
   0.4499997,
   0.4666664,
   0.4833331,
   0.4999997,
   0.5166664,
   0.533333,
   0.5499997,
   0.5666663,
   0.583333,
   0.5999997,
   0.6166664,
   0.6333331,
   0.6499998,
   0.6666665,
   0.6833332,
   0.7,
   0.7166668,
   0.7333336,
   0.7500005,
   0.7666674,
   0.7833343,
   0.8000012,
   0.8166682,
   0.8333351,
   0.850002,
   0.8666689,
   0.8833357,
   0.9000025,
   0.9166692,
   0.9333359,
   0.9500024,
   0.9666689,
   0.9833354,
   1.000002,
   1.016668,
   1.033335,
   1.050001,
   1.066667,
   1.083334,
   1.1,
   1.116667,
   1.133333,
   1.15,
   1.166666,
   1.183333,
   1.199999,
   1.216666,
   1.233333,
   1.249999,
   1.266666,
   1.283333,
   1.299999,
   1.316666,
   1.333332,
   1.349999,
   1.366666,
   1.383332,
   1.399999,
   1.416666,
   1.433332,
   1.449999,
   1.466666,
   1.483332,
   1.499999,
   1.516666,
   1.533332,
   1.549999,
   1.566666,
   1.583332,
   1.599999,
   1.616666,
   1.633332,
   1.649999,
   1.666666,
   1.666666};
   TGraph *graph = new TGraph(102,full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx1,full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy1);
   graph->SetName("full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]");
   graph->SetTitle("Projection of full_model");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff0000");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   
   TH1F *Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1 = new TH1F("Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1","Projection of full_model",102,0.685,0.865);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetMinimum(4.782755e-08);
   Graph_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB1->SetMaximum(1.833332);
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
   TLatex *   tex = new TLatex(0.71,1.242819,"#sigma = (10.0 #pm 0.0) MeV");
   tex->SetTextFont(42);
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.71,-498.7572,"#chi^{2}/nDoF = 0.15");
   tex->SetTextFont(42);
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
   
   TH1D *frame_a0c20a0__2 = new TH1D("frame_a0c20a0__2","#omega#rightarrow#mu#mu",100,0.7,0.85);
   frame_a0c20a0__2->SetBinContent(1,6.214095);
   frame_a0c20a0__2->SetMaximum(6.214095);
   frame_a0c20a0__2->SetEntries(1);
   frame_a0c20a0__2->SetDirectory(0);
   frame_a0c20a0__2->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a0c20a0__2->SetLineColor(ci);
   frame_a0c20a0__2->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_a0c20a0__2->GetXaxis()->SetLabelFont(42);
   frame_a0c20a0__2->GetXaxis()->SetTitleOffset(1);
   frame_a0c20a0__2->GetXaxis()->SetTitleFont(42);
   frame_a0c20a0__2->GetYaxis()->SetTitle("Events / ( 0.005 GeV )");
   frame_a0c20a0__2->GetYaxis()->SetLabelFont(42);
   frame_a0c20a0__2->GetYaxis()->SetTitleFont(42);
   frame_a0c20a0__2->GetZaxis()->SetLabelFont(42);
   frame_a0c20a0__2->GetZaxis()->SetTitleOffset(1);
   frame_a0c20a0__2->GetZaxis()->SetTitleFont(42);
   frame_a0c20a0__2->Draw("AXISSAME");
   
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
   
   TH1D *frame_a6599e0__3 = new TH1D("frame_a6599e0__3"," ",100,0.7,0.85);
   frame_a6599e0__3->SetBinContent(1,5.5);
   frame_a6599e0__3->SetMinimum(-5.5);
   frame_a6599e0__3->SetMaximum(5.5);
   frame_a6599e0__3->SetEntries(1);
   frame_a6599e0__3->SetDirectory(0);
   frame_a6599e0__3->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a6599e0__3->SetLineColor(ci);
   frame_a6599e0__3->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_a6599e0__3->GetXaxis()->SetLabelFont(42);
   frame_a6599e0__3->GetXaxis()->SetLabelSize(0.1);
   frame_a6599e0__3->GetXaxis()->SetTitleSize(0.1);
   frame_a6599e0__3->GetXaxis()->SetTitleOffset(1);
   frame_a6599e0__3->GetXaxis()->SetTitleFont(42);
   frame_a6599e0__3->GetYaxis()->SetTitle("Pull");
   frame_a6599e0__3->GetYaxis()->SetLabelFont(42);
   frame_a6599e0__3->GetYaxis()->SetLabelSize(0.1);
   frame_a6599e0__3->GetYaxis()->SetTitleSize(0.1);
   frame_a6599e0__3->GetYaxis()->SetTitleFont(42);
   frame_a6599e0__3->GetZaxis()->SetLabelFont(42);
   frame_a6599e0__3->GetZaxis()->SetTitleOffset(1);
   frame_a6599e0__3->GetZaxis()->SetTitleFont(42);
   frame_a6599e0__3->Draw("FUNC");
   
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
   -0.02419935,
   -0.07259795,
   -0.1209965,
   -0.1693951,
   -0.2177937,
   -0.2661923,
   -0.3145909,
   -0.3629895,
   0.6379939,
   0.5708367,
   0.5036795,
   0.4365222,
   0.3693647,
   0.3022069,
   -0.7017813,
   0.1678905,
   0.1007328,
   0.03357596,
   -0.01208036,
   -0.03623952,
   -0.0603988,
   -0.0845582,
   -0.1087177,
   0.5375735,
   0.4945677,
   -0.1811963,
   -0.2053559,
   0.9017082,
   -1.37936,
   0.2795387};
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
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   1,
   1,
   1,
   1,
   0,
   1,
   1,
   1,
   0.3597463,
   0.3597463,
   0.3597463,
   0.3597463,
   0.3597463,
   1,
   1,
   0.3597463,
   0.3597463,
   1,
   0,
   1};
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
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   2.779737,
   2.779737,
   2.779737,
   2.779737,
   2.779737,
   2.779737,
   1,
   2.779737,
   2.779737,
   2.779737,
   1,
   1,
   1,
   1,
   1,
   2.04198,
   2.04198,
   1,
   1,
   1.787332,
   1,
   2.04198};
   grae = new TGraphAsymmErrors(30,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fy3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_felx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehx3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fely3002,pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]_fehy3002);
   grae->SetName("pull_data_full_model_Norm[tau_mu12_fitM]_Range[fit_range]_NormRange[fit_range]");
   grae->SetTitle("Pull of Histogram of data_plot__tau_mu12_fitM and Projection of full_model");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002 = new TH1F("Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002","Pull of Histogram of data_plot__tau_mu12_fitM and Projection of full_model",100,0.688,0.862);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetMinimum(-1.859069);
   Graph_pull_data_full_model_NormoBtau_mu12_fitMcB_RangeoBfit_rangecB_NormRangeoBfit_rangecB3002->SetMaximum(3.89744);
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
   
   TH1D *frame_a6599e0__4 = new TH1D("frame_a6599e0__4"," ",100,0.7,0.85);
   frame_a6599e0__4->SetBinContent(1,5.5);
   frame_a6599e0__4->SetMinimum(-5.5);
   frame_a6599e0__4->SetMaximum(5.5);
   frame_a6599e0__4->SetEntries(1);
   frame_a6599e0__4->SetDirectory(0);
   frame_a6599e0__4->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a6599e0__4->SetLineColor(ci);
   frame_a6599e0__4->GetXaxis()->SetTitle("M(#mu_{1}#mu_{2}) (GeV)");
   frame_a6599e0__4->GetXaxis()->SetLabelFont(42);
   frame_a6599e0__4->GetXaxis()->SetLabelSize(0.1);
   frame_a6599e0__4->GetXaxis()->SetTitleSize(0.1);
   frame_a6599e0__4->GetXaxis()->SetTitleOffset(1);
   frame_a6599e0__4->GetXaxis()->SetTitleFont(42);
   frame_a6599e0__4->GetYaxis()->SetTitle("Pull");
   frame_a6599e0__4->GetYaxis()->SetLabelFont(42);
   frame_a6599e0__4->GetYaxis()->SetLabelSize(0.1);
   frame_a6599e0__4->GetYaxis()->SetTitleSize(0.1);
   frame_a6599e0__4->GetYaxis()->SetTitleFont(42);
   frame_a6599e0__4->GetZaxis()->SetLabelFont(42);
   frame_a6599e0__4->GetZaxis()->SetTitleOffset(1);
   frame_a6599e0__4->GetZaxis()->SetTitleFont(42);
   frame_a6599e0__4->Draw("AXISSAME");
   
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
