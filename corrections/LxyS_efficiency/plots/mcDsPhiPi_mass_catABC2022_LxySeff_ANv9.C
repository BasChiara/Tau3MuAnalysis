#ifdef __CLING__
#pragma cling optimize(0)
#endif
void mcDsPhiPi_mass_catABC2022_LxySeff_ANv9()
{
//=========Macro generated from canvas: c/c
//=========  (Fri Sep 26 16:24:12 2025) by ROOT version 6.26/11
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
   up_pad->Range(1.69,0,2.09,981.3487);
   up_pad->SetFillColor(0);
   up_pad->SetBorderMode(0);
   up_pad->SetBorderSize(2);
   up_pad->SetLeftMargin(0.15);
   up_pad->SetBottomMargin(0);
   up_pad->SetFrameBorderMode(0);
   up_pad->SetFrameBorderMode(0);
   
   TH1D *frame_9c59160__1 = new TH1D("frame_9c59160__1"," ",100,1.75,2.05);
   frame_9c59160__1->SetBinContent(1,883.2138);
   frame_9c59160__1->SetMaximum(883.2138);
   frame_9c59160__1->SetEntries(1);
   frame_9c59160__1->SetDirectory(0);
   frame_9c59160__1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   frame_9c59160__1->SetLineColor(ci);
   frame_9c59160__1->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_9c59160__1->GetXaxis()->SetLabelFont(42);
   frame_9c59160__1->GetXaxis()->SetTitleOffset(1);
   frame_9c59160__1->GetXaxis()->SetTitleFont(42);
   frame_9c59160__1->GetYaxis()->SetTitle("Events / ( 0.01 GeV )");
   frame_9c59160__1->GetYaxis()->SetLabelFont(42);
   frame_9c59160__1->GetYaxis()->SetTitleFont(42);
   frame_9c59160__1->GetZaxis()->SetLabelFont(42);
   frame_9c59160__1->GetZaxis()->SetTitleOffset(1);
   frame_9c59160__1->GetZaxis()->SetTitleFont(42);
   frame_9c59160__1->Draw("FUNC");
   
   Double_t extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx1[123] = {
   1.75,
   1.753,
   1.756,
   1.759,
   1.762,
   1.765,
   1.768,
   1.771,
   1.774,
   1.777,
   1.78,
   1.783,
   1.786,
   1.789,
   1.792,
   1.795,
   1.798,
   1.801,
   1.804,
   1.807,
   1.81,
   1.813,
   1.816,
   1.819,
   1.822,
   1.825,
   1.828,
   1.831,
   1.834,
   1.837,
   1.84,
   1.843,
   1.846,
   1.849,
   1.852,
   1.855,
   1.858,
   1.861,
   1.864,
   1.867,
   1.87,
   1.873,
   1.876,
   1.879,
   1.882,
   1.885,
   1.888,
   1.891,
   1.894,
   1.897,
   1.9,
   1.903,
   1.906,
   1.909,
   1.912,
   1.915,
   1.918,
   1.921,
   1.924,
   1.927,
   1.93,
   1.933,
   1.9345,
   1.936,
   1.9375,
   1.939,
   1.9405,
   1.942,
   1.9435,
   1.945,
   1.9465,
   1.948,
   1.951,
   1.954,
   1.9555,
   1.957,
   1.9585,
   1.96,
   1.9615,
   1.963,
   1.9645,
   1.966,
   1.9675,
   1.969,
   1.9705,
   1.972,
   1.9735,
   1.975,
   1.9765,
   1.978,
   1.9795,
   1.981,
   1.984,
   1.987,
   1.99,
   1.9915,
   1.993,
   1.9945,
   1.996,
   1.9975,
   1.999,
   2.0005,
   2.002,
   2.0035,
   2.005,
   2.0065,
   2.008,
   2.0095,
   2.011,
   2.014,
   2.017,
   2.02,
   2.023,
   2.026,
   2.029,
   2.032,
   2.035,
   2.038,
   2.041,
   2.044,
   2.047,
   2.05,
   2.05};
   Double_t extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy1[123] = {
   8.393065,
   8.498839,
   8.605961,
   8.714455,
   8.82434,
   8.935641,
   9.048383,
   9.162592,
   9.278298,
   9.395532,
   9.514331,
   9.634732,
   9.756782,
   9.880529,
   10.00603,
   10.13336,
   10.26259,
   10.39381,
   10.52714,
   10.6627,
   10.80064,
   10.94117,
   11.08449,
   11.23089,
   11.38069,
   11.53431,
   11.69225,
   11.85511,
   12.02364,
   12.19877,
   12.38162,
   12.57361,
   12.77645,
   12.99228,
   13.22375,
   13.47413,
   13.74747,
   14.04879,
   14.38433,
   14.76183,
   15.19091,
   15.68351,
   16.25449,
   16.92236,
   17.71013,
   18.64648,
   19.76714,
   21.11669,
   22.7507,
   24.73858,
   27.16697,
   30.14412,
   33.80535,
   38.3199,
   43.89954,
   50.80934,
   59.38133,
   70.03159,
   83.28175,
   99.78615,
   120.366,
   146.0524,
   161.2033,
   178.1409,
   197.0794,
   218.2595,
   241.9508,
   268.4559,
   298.1142,
   331.3065,
   368.4157,
   407.9535,
   490.0241,
   572.2661,
   611.8129,
   649.3715,
   684.2315,
   715.7035,
   743.1419,
   765.9665,
   783.6835,
   795.9029,
   802.3531,
   802.8911,
   797.5074,
   786.3272,
   769.605,
   747.7151,
   721.1383,
   690.4439,
   656.27,
   619.3012,
   539.8166,
   457.5614,
   377.526,
   339.6254,
   303.6664,
   269.9433,
   238.6679,
   209.9742,
   183.9236,
   160.5136,
   139.6866,
   121.3393,
   105.3331,
   91.50309,
   79.66738,
   69.63473,
   61.2116,
   48.44125,
   39.94958,
   34.54048,
   31.26246,
   29.40084,
   28.44572,
   28.0502,
   27.98851,
   28.11984,
   28.35983,
   28.65993,
   28.99323,
   29.34539,
   29.34539};
   TGraph *graph = new TGraph(123,extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx1,extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy1);
   graph->SetName("extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   graph->SetTitle("Projection of extMCmodel_DsPhiMuMuPi");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   
   TH1F *Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1 = new TH1F("Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1","Projection of extMCmodel_DsPhiMuMuPi",123,1.72,2.08);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMinimum(7.553759);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMaximum(882.3409);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetDirectory(0);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetLineColor(ci);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetTitleOffset(1);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetTitleFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetYaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetYaxis()->SetTitleFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetTitleOffset(1);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]1);
   
   graph->Draw("l");
   
   Double_t h_mc_DsPhiMuMuPi_fx3001[30] = {
   1.755,
   1.765,
   1.775,
   1.785,
   1.795,
   1.805,
   1.815,
   1.825,
   1.835,
   1.845,
   1.855,
   1.865,
   1.875,
   1.885,
   1.895,
   1.905,
   1.915,
   1.925,
   1.935,
   1.945,
   1.955,
   1.965,
   1.975,
   1.985,
   1.995,
   2.005,
   2.015,
   2.025,
   2.035,
   2.045};
   Double_t h_mc_DsPhiMuMuPi_fy3001[30] = {
   8.598516,
   9.545742,
   7.406982,
   10.86823,
   8.780316,
   15.57831,
   10.51305,
   14.43867,
   9.110548,
   5.042244,
   16.99336,
   15.20051,
   16.70588,
   12.58832,
   26.99913,
   31.58981,
   53.22081,
   87.89341,
   173.3259,
   319.1943,
   588.5915,
   815.0211,
   754.5215,
   479.1606,
   250.4626,
   123.3103,
   59.50827,
   37.58398,
   22.1602,
   21.19049};
   Double_t h_mc_DsPhiMuMuPi_felx3001[30] = {
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005};
   Double_t h_mc_DsPhiMuMuPi_fely3001[30] = {
   2.592335,
   2.926118,
   2.357561,
   3.189729,
   2.756654,
   4.156015,
   3.013286,
   3.738278,
   2.673472,
   1.575754,
   4.114028,
   3.788258,
   4.017112,
   3.12433,
   4.911352,
   5.249869,
   6.487046,
   8.763051,
   12.23071,
   16.63663,
   22.56151,
   26.13491,
   25.14775,
   20.2719,
   14.69878,
   10.2525,
   6.863471,
   5.954087,
   4.81853,
   4.343223};
   Double_t h_mc_DsPhiMuMuPi_fehx3001[30] = {
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005,
   0.005};
   Double_t h_mc_DsPhiMuMuPi_fehy3001[30] = {
   2.592335,
   2.926118,
   2.357561,
   3.189729,
   2.756654,
   4.156015,
   3.013286,
   3.738278,
   2.673472,
   1.575754,
   4.114028,
   3.788258,
   4.017112,
   3.12433,
   4.911352,
   5.249869,
   6.487046,
   8.763051,
   12.23071,
   16.63663,
   22.56151,
   26.13491,
   25.14775,
   20.2719,
   14.69878,
   10.2525,
   6.863471,
   5.954087,
   4.81853,
   4.343223};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(30,h_mc_DsPhiMuMuPi_fx3001,h_mc_DsPhiMuMuPi_fy3001,h_mc_DsPhiMuMuPi_felx3001,h_mc_DsPhiMuMuPi_fehx3001,h_mc_DsPhiMuMuPi_fely3001,h_mc_DsPhiMuMuPi_fehy3001);
   grae->SetName("h_mc_DsPhiMuMuPi");
   grae->SetTitle("Histogram of mc_DsPhiMuMuPi_plot__Ds_fit_mass");

   ci = TColor::GetColor("#ff0000");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);
   grae->SetLineWidth(2);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_h_mc_DsPhiMuMuPi3001 = new TH1F("Graph_h_mc_DsPhiMuMuPi3001","Histogram of mc_DsPhiMuMuPi_plot__Ds_fit_mass",100,1.72,2.08);
   Graph_h_mc_DsPhiMuMuPi3001->SetMinimum(3.119841);
   Graph_h_mc_DsPhiMuMuPi3001->SetMaximum(924.925);
   Graph_h_mc_DsPhiMuMuPi3001->SetDirectory(0);
   Graph_h_mc_DsPhiMuMuPi3001->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_h_mc_DsPhiMuMuPi3001->SetLineColor(ci);
   Graph_h_mc_DsPhiMuMuPi3001->GetXaxis()->SetLabelFont(42);
   Graph_h_mc_DsPhiMuMuPi3001->GetXaxis()->SetTitleOffset(1);
   Graph_h_mc_DsPhiMuMuPi3001->GetXaxis()->SetTitleFont(42);
   Graph_h_mc_DsPhiMuMuPi3001->GetYaxis()->SetLabelFont(42);
   Graph_h_mc_DsPhiMuMuPi3001->GetYaxis()->SetTitleFont(42);
   Graph_h_mc_DsPhiMuMuPi3001->GetZaxis()->SetLabelFont(42);
   Graph_h_mc_DsPhiMuMuPi3001->GetZaxis()->SetTitleOffset(1);
   Graph_h_mc_DsPhiMuMuPi3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_h_mc_DsPhiMuMuPi3001);
   
   grae->Draw("p");
   
   TPaveText *pt = new TPaveText(0.2,0.43,0.5,0.85,"BRNDC");
   pt->SetName("extMCmodel_DsPhiMuMuPi_paramBox");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextAlign(12);
   pt->SetTextSize(0.03);
   TText *pt_LaTex = pt->AddText("alpha =  4.2 +/- 0.6");
   pt_LaTex = pt->AddText("alphaCB_mc =  1.3 +/- 0.1");
   pt_LaTex = pt->AddText("dM_mc =  0.0006 +/- 0.0004");
   pt_LaTex = pt->AddText("nCB_mc =  100 +/- 198");
   pt_LaTex = pt->AddText("nCombMC =  502 +/- 36");
   pt_LaTex = pt->AddText("nMC =  3503 +/- 62");
   pt_LaTex = pt->AddText("width_mc =  0.0172 +/- 0.0004");
   pt->Draw();
   
   TH1D *frame_9c59160__2 = new TH1D("frame_9c59160__2"," ",100,1.75,2.05);
   frame_9c59160__2->SetBinContent(1,883.2138);
   frame_9c59160__2->SetMaximum(883.2138);
   frame_9c59160__2->SetEntries(1);
   frame_9c59160__2->SetDirectory(0);
   frame_9c59160__2->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_9c59160__2->SetLineColor(ci);
   frame_9c59160__2->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_9c59160__2->GetXaxis()->SetLabelFont(42);
   frame_9c59160__2->GetXaxis()->SetTitleOffset(1);
   frame_9c59160__2->GetXaxis()->SetTitleFont(42);
   frame_9c59160__2->GetYaxis()->SetTitle("Events / ( 0.01 GeV )");
   frame_9c59160__2->GetYaxis()->SetLabelFont(42);
   frame_9c59160__2->GetYaxis()->SetTitleFont(42);
   frame_9c59160__2->GetZaxis()->SetLabelFont(42);
   frame_9c59160__2->GetZaxis()->SetTitleOffset(1);
   frame_9c59160__2->GetZaxis()->SetTitleFont(42);
   frame_9c59160__2->Draw("AXISSAME");
   
   pt = new TPaveText(0.4816667,0.94,0.5183333,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   pt_LaTex = pt->AddText(" ");
   pt->Draw();
   up_pad->Modified();
   c->cd();
  
// ------------>Primitives in pad: ratio_pad
   TPad *ratio_pad = new TPad("ratio_pad", "",0,0,1,0.28);
   ratio_pad->Draw();
   ratio_pad->cd();
   ratio_pad->Range(1.69,-12.83333,2.09,5.5);
   ratio_pad->SetFillColor(0);
   ratio_pad->SetBorderMode(0);
   ratio_pad->SetBorderSize(2);
   ratio_pad->SetLeftMargin(0.15);
   ratio_pad->SetTopMargin(0);
   ratio_pad->SetBottomMargin(0.4);
   ratio_pad->SetFrameBorderMode(0);
   ratio_pad->SetFrameBorderMode(0);
   
   TH1D *frame_a0d5a50__3 = new TH1D("frame_a0d5a50__3"," ",100,1.75,2.05);
   frame_a0d5a50__3->SetBinContent(1,5.5);
   frame_a0d5a50__3->SetMinimum(-5.5);
   frame_a0d5a50__3->SetMaximum(5.5);
   frame_a0d5a50__3->SetEntries(1);
   frame_a0d5a50__3->SetDirectory(0);
   frame_a0d5a50__3->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a0d5a50__3->SetLineColor(ci);
   frame_a0d5a50__3->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_a0d5a50__3->GetXaxis()->SetLabelFont(42);
   frame_a0d5a50__3->GetXaxis()->SetLabelSize(0.1);
   frame_a0d5a50__3->GetXaxis()->SetTitleSize(0.1);
   frame_a0d5a50__3->GetXaxis()->SetTitleOffset(1);
   frame_a0d5a50__3->GetXaxis()->SetTitleFont(42);
   frame_a0d5a50__3->GetYaxis()->SetTitle("Pull");
   frame_a0d5a50__3->GetYaxis()->SetLabelFont(42);
   frame_a0d5a50__3->GetYaxis()->SetLabelSize(0.1);
   frame_a0d5a50__3->GetYaxis()->SetTitleSize(0.1);
   frame_a0d5a50__3->GetYaxis()->SetTitleFont(42);
   frame_a0d5a50__3->GetZaxis()->SetLabelFont(42);
   frame_a0d5a50__3->GetZaxis()->SetTitleOffset(1);
   frame_a0d5a50__3->GetZaxis()->SetTitleFont(42);
   frame_a0d5a50__3->Draw("FUNC");
   
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002[30] = {
   1.755,
   1.765,
   1.775,
   1.785,
   1.795,
   1.805,
   1.815,
   1.825,
   1.835,
   1.845,
   1.855,
   1.865,
   1.875,
   1.885,
   1.895,
   1.905,
   1.915,
   1.925,
   1.935,
   1.945,
   1.955,
   1.965,
   1.975,
   1.985,
   1.995,
   2.005,
   2.015,
   2.025,
   2.035,
   2.045};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002[30] = {
   0.01067401,
   0.2082309,
   -0.8106094,
   0.3609705,
   -0.4912083,
   1.204278,
   -0.1742163,
   0.7762857,
   -1.112591,
   -4.868746,
   0.8523359,
   0.1770872,
   0.1498909,
   -1.971662,
   0.6964715,
   -0.2558248,
   0.2299444,
   -0.2752754,
   0.2420552,
   -1.10927,
   -0.3012538,
   1.429494,
   0.6274158,
   -1.615006,
   -0.9211465,
   1.344789,
   1.781355,
   1.192303,
   -1.232374,
   -1.748291};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002[30] = {
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
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002[30] = {
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002[30] = {
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
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002[30] = {
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1};
   grae = new TGraphAsymmErrors(30,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002);
   grae->SetName("pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   grae->SetTitle("Pull of Histogram of mc_DsPhiMuMuPi_plot__Ds_fit_mass and Projection of extMCmodel_DsPhiMuMuPi");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002 = new TH1F("Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002","Pull of Histogram of mc_DsPhiMuMuPi_plot__Ds_fit_mass and Projection of extMCmodel_DsPhiMuMuPi",100,1.726,2.074);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMinimum(-6.733756);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMaximum(3.646365);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetDirectory(0);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetLineColor(ci);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetRange(7,94);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitleOffset(1);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitleFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetTitle("(Data - curve) / #sigma_{data}");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetTitleFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetTitleOffset(1);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBDs_fit_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[Ds_fit_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]3002);
   
   grae->Draw("p");
   
   TH1D *frame_a0d5a50__4 = new TH1D("frame_a0d5a50__4"," ",100,1.75,2.05);
   frame_a0d5a50__4->SetBinContent(1,5.5);
   frame_a0d5a50__4->SetMinimum(-5.5);
   frame_a0d5a50__4->SetMaximum(5.5);
   frame_a0d5a50__4->SetEntries(1);
   frame_a0d5a50__4->SetDirectory(0);
   frame_a0d5a50__4->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a0d5a50__4->SetLineColor(ci);
   frame_a0d5a50__4->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_a0d5a50__4->GetXaxis()->SetLabelFont(42);
   frame_a0d5a50__4->GetXaxis()->SetLabelSize(0.1);
   frame_a0d5a50__4->GetXaxis()->SetTitleSize(0.1);
   frame_a0d5a50__4->GetXaxis()->SetTitleOffset(1);
   frame_a0d5a50__4->GetXaxis()->SetTitleFont(42);
   frame_a0d5a50__4->GetYaxis()->SetTitle("Pull");
   frame_a0d5a50__4->GetYaxis()->SetLabelFont(42);
   frame_a0d5a50__4->GetYaxis()->SetLabelSize(0.1);
   frame_a0d5a50__4->GetYaxis()->SetTitleSize(0.1);
   frame_a0d5a50__4->GetYaxis()->SetTitleFont(42);
   frame_a0d5a50__4->GetZaxis()->SetLabelFont(42);
   frame_a0d5a50__4->GetZaxis()->SetTitleOffset(1);
   frame_a0d5a50__4->GetZaxis()->SetTitleFont(42);
   frame_a0d5a50__4->Draw("AXISSAME");
   
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
