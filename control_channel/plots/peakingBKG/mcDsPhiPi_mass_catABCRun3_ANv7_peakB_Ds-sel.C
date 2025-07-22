#ifdef __CLING__
#pragma cling optimize(0)
#endif
void mcDsPhiPi_mass_catABCRun3_ANv7_peakB_Ds-sel()
{
//=========Macro generated from canvas: c/c
//=========  (Mon Jul 14 13:14:57 2025) by ROOT version 6.26/11
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
   up_pad->Range(1.636,0,2.062667,81.49511);
   up_pad->SetFillColor(0);
   up_pad->SetBorderMode(0);
   up_pad->SetBorderSize(2);
   up_pad->SetLeftMargin(0.15);
   up_pad->SetBottomMargin(0);
   up_pad->SetFrameBorderMode(0);
   up_pad->SetFrameBorderMode(0);
   
   TH1D *frame_a85c3a0__1 = new TH1D("frame_a85c3a0__1","D_{s} -> #phi(1020)#pi signal",100,1.7,2.02);
   frame_a85c3a0__1->SetBinContent(1,73.3456);
   frame_a85c3a0__1->SetMaximum(73.3456);
   frame_a85c3a0__1->SetEntries(1);
   frame_a85c3a0__1->SetDirectory(0);
   frame_a85c3a0__1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   frame_a85c3a0__1->SetLineColor(ci);
   frame_a85c3a0__1->GetXaxis()->SetTitle("#mu#mu #pi mass (GeV)");
   frame_a85c3a0__1->GetXaxis()->SetLabelFont(42);
   frame_a85c3a0__1->GetXaxis()->SetTitleOffset(1);
   frame_a85c3a0__1->GetXaxis()->SetTitleFont(42);
   frame_a85c3a0__1->GetYaxis()->SetTitle("Events / ( 0.00969697 GeV )");
   frame_a85c3a0__1->GetYaxis()->SetLabelFont(42);
   frame_a85c3a0__1->GetYaxis()->SetTitleFont(42);
   frame_a85c3a0__1->GetZaxis()->SetLabelFont(42);
   frame_a85c3a0__1->GetZaxis()->SetTitleOffset(1);
   frame_a85c3a0__1->GetZaxis()->SetTitleFont(42);
   frame_a85c3a0__1->Draw("FUNC");
   
   Double_t extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx1[122] = {
   1.7,
   1.7032,
   1.7064,
   1.7096,
   1.7128,
   1.716,
   1.7192,
   1.7224,
   1.7256,
   1.7288,
   1.732,
   1.7352,
   1.7384,
   1.7416,
   1.7448,
   1.748,
   1.7512,
   1.7544,
   1.7576,
   1.7608,
   1.764,
   1.7672,
   1.7704,
   1.7736,
   1.7768,
   1.78,
   1.7832,
   1.7864,
   1.7896,
   1.7928,
   1.796,
   1.7992,
   1.8024,
   1.8056,
   1.8088,
   1.812,
   1.8152,
   1.8184,
   1.8216,
   1.8248,
   1.828,
   1.8312,
   1.8344,
   1.8376,
   1.8408,
   1.844,
   1.8472,
   1.8504,
   1.8536,
   1.8568,
   1.86,
   1.8632,
   1.8664,
   1.8696,
   1.8728,
   1.876,
   1.8792,
   1.8824,
   1.8856,
   1.8888,
   1.892,
   1.8952,
   1.8984,
   1.9016,
   1.9048,
   1.908,
   1.9112,
   1.9144,
   1.9176,
   1.9208,
   1.924,
   1.9256,
   1.9272,
   1.9288,
   1.9304,
   1.932,
   1.9336,
   1.9352,
   1.9368,
   1.9384,
   1.94,
   1.9432,
   1.9464,
   1.9496,
   1.9528,
   1.9544,
   1.956,
   1.9576,
   1.9592,
   1.9608,
   1.9624,
   1.964,
   1.9656,
   1.9672,
   1.9688,
   1.9704,
   1.972,
   1.9736,
   1.9752,
   1.9768,
   1.9784,
   1.98,
   1.9816,
   1.9848,
   1.988,
   1.9912,
   1.9944,
   1.996,
   1.9976,
   1.9992,
   2.0008,
   2.0024,
   2.004,
   2.0056,
   2.0072,
   2.0088,
   2.0104,
   2.012,
   2.0136,
   2.0168,
   2.02,
   2.02};
   Double_t extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy1[122] = {
   3.6577,
   3.656185,
   3.65467,
   3.653157,
   3.651644,
   3.650132,
   3.648621,
   3.647112,
   3.645603,
   3.644095,
   3.642589,
   3.641084,
   3.63958,
   3.638079,
   3.636579,
   3.635082,
   3.633588,
   3.632096,
   3.630609,
   3.629126,
   3.627649,
   3.626178,
   3.624715,
   3.623262,
   3.62182,
   3.620392,
   3.618981,
   3.617591,
   3.616227,
   3.614894,
   3.6136,
   3.612353,
   3.611164,
   3.610048,
   3.60902,
   3.608102,
   3.60732,
   3.606705,
   3.606299,
   3.60615,
   3.606321,
   3.606889,
   3.60795,
   3.609625,
   3.612062,
   3.615449,
   3.62002,
   3.626068,
   3.633957,
   3.644147,
   3.657213,
   3.673874,
   3.695037,
   3.721838,
   3.755706,
   3.79844,
   3.852303,
   3.92015,
   4.005578,
   4.113129,
   4.248539,
   4.419058,
   4.633859,
   4.904555,
   5.245859,
   5.676433,
   6.219959,
   6.906519,
   7.774352,
   8.872116,
   10.26176,
   11.08994,
   12.02226,
   13.07204,
   14.25432,
   15.58608,
   17.08652,
   18.77736,
   20.6558,
   22.65614,
   24.7632,
   29.23511,
   33.9145,
   38.59759,
   43.0463,
   45.10349,
   47.00702,
   48.7266,
   50.23401,
   51.50389,
   52.5144,
   53.24789,
   53.69137,
   53.83693,
   53.68195,
   53.2292,
   52.48672,
   51.46763,
   50.1897,
   48.67485,
   46.94857,
   45.03911,
   42.9768,
   38.52041,
   33.83294,
   29.15213,
   24.6812,
   22.57533,
   20.57653,
   18.69615,
   16.94233,
   15.32018,
   13.83196,
   12.47742,
   11.25411,
   10.15772,
   9.182427,
   8.321243,
   7.566333,
   6.341558,
   5.439159,
   5.439159};
   TGraph *graph = new TGraph(122,extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx1,extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy1);
   graph->SetName("extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   graph->SetTitle("Projection of extMCmodel_DsPhiMuMuPi");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   
   TH1F *Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1 = new TH1F("Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1","Projection of extMCmodel_DsPhiMuMuPi",122,1.668,2.052);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMinimum(3.245535);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMaximum(58.86001);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetDirectory(0);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetLineColor(ci);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetTitleOffset(1);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetXaxis()->SetTitleFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetYaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetYaxis()->SetTitleFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetLabelFont(42);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetTitleOffset(1);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]1);
   
   graph->Draw("l");
   
   Double_t h_mc_DsPhiMuMuPi_fx3001[33] = {
   1.704848,
   1.714545,
   1.724242,
   1.733939,
   1.743636,
   1.753333,
   1.76303,
   1.772727,
   1.782424,
   1.792121,
   1.801818,
   1.811515,
   1.821212,
   1.830909,
   1.840606,
   1.850303,
   1.86,
   1.869697,
   1.879394,
   1.889091,
   1.898788,
   1.908485,
   1.918182,
   1.927879,
   1.937576,
   1.947273,
   1.95697,
   1.966667,
   1.976364,
   1.986061,
   1.995758,
   2.005455,
   2.015152};
   Double_t h_mc_DsPhiMuMuPi_fy3001[33] = {
   4,
   2,
   1,
   4,
   3,
   9,
   2,
   6,
   6,
   0,
   4,
   5,
   5,
   1,
   5,
   3,
   3,
   1,
   5,
   5,
   3,
   6,
   11,
   8,
   24,
   38,
   43,
   61,
   44,
   37,
   19,
   15,
   8};
   Double_t h_mc_DsPhiMuMuPi_felx3001[33] = {
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
   0,
   0,
   0,
   0};
   Double_t h_mc_DsPhiMuMuPi_fely3001[33] = {
   1.914339,
   1.291815,
   0.8272462,
   1.914339,
   1.632705,
   2.943461,
   1.291815,
   2.379931,
   2.379931,
   0,
   1.914339,
   2.159691,
   2.159691,
   0.8272462,
   2.159691,
   1.632705,
   1.632705,
   0.8272462,
   2.159691,
   2.159691,
   1.632705,
   2.379931,
   3.265579,
   2.768386,
   4.864612,
   6.137163,
   6.531834,
   7.788779,
   6.60794,
   6.055143,
   4.320219,
   3.82938,
   2.768386};
   Double_t h_mc_DsPhiMuMuPi_fehx3001[33] = {
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
   0,
   0,
   0,
   0};
   Double_t h_mc_DsPhiMuMuPi_fehy3001[33] = {
   3.162753,
   2.63786,
   2.299527,
   3.162753,
   2.918186,
   4.110204,
   2.63786,
   3.583642,
   3.583642,
   1.147874,
   3.162753,
   3.382473,
   3.382473,
   2.299527,
   3.382473,
   2.918186,
   2.918186,
   2.299527,
   3.382473,
   3.382473,
   2.918186,
   3.583642,
   4.416521,
   3.945142,
   5.966932,
   7.218484,
   7.608278,
   8.852952,
   7.68351,
   7.137555,
   5.435196,
   4.958738,
   3.945142};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(33,h_mc_DsPhiMuMuPi_fx3001,h_mc_DsPhiMuMuPi_fy3001,h_mc_DsPhiMuMuPi_felx3001,h_mc_DsPhiMuMuPi_fehx3001,h_mc_DsPhiMuMuPi_fely3001,h_mc_DsPhiMuMuPi_fehy3001);
   grae->SetName("h_mc_DsPhiMuMuPi");
   grae->SetTitle("Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass");

   ci = TColor::GetColor("#ff0000");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);
   grae->SetLineWidth(2);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_h_mc_DsPhiMuMuPi3001 = new TH1F("Graph_h_mc_DsPhiMuMuPi3001","Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass",100,1.673818,2.046182);
   Graph_h_mc_DsPhiMuMuPi3001->SetMinimum(0);
   Graph_h_mc_DsPhiMuMuPi3001->SetMaximum(76.83825);
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
   TText *pt_LaTex = pt->AddText("alpha = -0.1 +/- 2");
   pt_LaTex = pt->AddText("alphaCB_mc =  1.5 +/- 0.9");
   pt_LaTex = pt->AddText("dM_mc = -0.0006 +/- 0.002");
   pt_LaTex = pt->AddText("nCB_mc =  66 +/- 1524");
   pt_LaTex = pt->AddText("nCombMC =  118 +/- 24");
   pt_LaTex = pt->AddText("nMC =  273 +/- 27");
   pt_LaTex = pt->AddText("width_mc =  0.021 +/- 0.002");
   pt->Draw();
   
   TH1D *frame_a85c3a0__2 = new TH1D("frame_a85c3a0__2","D_{s} -> #phi(1020)#pi signal",100,1.7,2.02);
   frame_a85c3a0__2->SetBinContent(1,73.3456);
   frame_a85c3a0__2->SetMaximum(73.3456);
   frame_a85c3a0__2->SetEntries(1);
   frame_a85c3a0__2->SetDirectory(0);
   frame_a85c3a0__2->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_a85c3a0__2->SetLineColor(ci);
   frame_a85c3a0__2->GetXaxis()->SetTitle("#mu#mu #pi mass (GeV)");
   frame_a85c3a0__2->GetXaxis()->SetLabelFont(42);
   frame_a85c3a0__2->GetXaxis()->SetTitleOffset(1);
   frame_a85c3a0__2->GetXaxis()->SetTitleFont(42);
   frame_a85c3a0__2->GetYaxis()->SetTitle("Events / ( 0.00969697 GeV )");
   frame_a85c3a0__2->GetYaxis()->SetLabelFont(42);
   frame_a85c3a0__2->GetYaxis()->SetTitleFont(42);
   frame_a85c3a0__2->GetZaxis()->SetLabelFont(42);
   frame_a85c3a0__2->GetZaxis()->SetTitleOffset(1);
   frame_a85c3a0__2->GetZaxis()->SetTitleFont(42);
   frame_a85c3a0__2->Draw("AXISSAME");
   
   pt = new TPaveText(0.3184314,0.9330379,0.6815686,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   pt_LaTex = pt->AddText("D_{s} -> #phi(1020)#pi signal");
   pt->Draw();
   up_pad->Modified();
   c->cd();
  
// ------------>Primitives in pad: ratio_pad
   TPad *ratio_pad = new TPad("ratio_pad", "",0,0,1,0.28);
   ratio_pad->Draw();
   ratio_pad->cd();
   ratio_pad->Range(1.636,-12.83333,2.062667,5.5);
   ratio_pad->SetFillColor(0);
   ratio_pad->SetBorderMode(0);
   ratio_pad->SetBorderSize(2);
   ratio_pad->SetLeftMargin(0.15);
   ratio_pad->SetTopMargin(0);
   ratio_pad->SetBottomMargin(0.4);
   ratio_pad->SetFrameBorderMode(0);
   ratio_pad->SetFrameBorderMode(0);
   
   TH1D *frame_adfef60__3 = new TH1D("frame_adfef60__3"," ",100,1.7,2.02);
   frame_adfef60__3->SetBinContent(1,5.5);
   frame_adfef60__3->SetMinimum(-5.5);
   frame_adfef60__3->SetMaximum(5.5);
   frame_adfef60__3->SetEntries(1);
   frame_adfef60__3->SetDirectory(0);
   frame_adfef60__3->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_adfef60__3->SetLineColor(ci);
   frame_adfef60__3->GetXaxis()->SetTitle("#mu#mu #pi mass (GeV)");
   frame_adfef60__3->GetXaxis()->SetLabelFont(42);
   frame_adfef60__3->GetXaxis()->SetLabelSize(0.1);
   frame_adfef60__3->GetXaxis()->SetTitleSize(0.1);
   frame_adfef60__3->GetXaxis()->SetTitleOffset(1);
   frame_adfef60__3->GetXaxis()->SetTitleFont(42);
   frame_adfef60__3->GetYaxis()->SetTitle("Pull");
   frame_adfef60__3->GetYaxis()->SetLabelFont(42);
   frame_adfef60__3->GetYaxis()->SetLabelSize(0.1);
   frame_adfef60__3->GetYaxis()->SetTitleSize(0.1);
   frame_adfef60__3->GetYaxis()->SetTitleFont(42);
   frame_adfef60__3->GetZaxis()->SetLabelFont(42);
   frame_adfef60__3->GetZaxis()->SetTitleOffset(1);
   frame_adfef60__3->GetZaxis()->SetTitleFont(42);
   frame_adfef60__3->Draw("FUNC");
   
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002[33] = {
   1.704848,
   1.714545,
   1.724242,
   1.733939,
   1.743636,
   1.753333,
   1.76303,
   1.772727,
   1.782424,
   1.792121,
   1.801818,
   1.811515,
   1.821212,
   1.830909,
   1.840606,
   1.850303,
   1.86,
   1.869697,
   1.879394,
   1.889091,
   1.898788,
   1.908485,
   1.918182,
   1.927879,
   1.937576,
   1.947273,
   1.95697,
   1.966667,
   1.976364,
   1.986061,
   1.995758,
   2.005455,
   2.015152};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002[33] = {
   0.1800074,
   -0.6258179,
   -1.150777,
   0.1871784,
   -0.2183292,
   1.823501,
   -0.6172045,
   0.99849,
   1.00031,
   -3.149465,
   0.2029903,
   0.6444003,
   0.645253,
   -1.133731,
   0.6425326,
   -0.2147623,
   -0.2257903,
   -1.1855,
   0.526632,
   0.3993403,
   -0.5792786,
   0.08156607,
   0.8978161,
   -1.179796,
   0.4496619,
   0.4610189,
   -0.6241895,
   0.9833527,
   -0.6194313,
   0.06176512,
   -0.7472292,
   0.5729453,
   0.3303304};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002[33] = {
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
   0,
   0,
   0,
   0};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002[33] = {
   1,
   0.4897207,
   0.3597463,
   1,
   0.559493,
   1,
   0.4897207,
   1,
   1,
   0,
   1,
   1,
   1,
   0.3597463,
   1,
   0.559493,
   0.559493,
   0.3597463,
   1,
   1,
   0.559493,
   1,
   1,
   0.7017203,
   1,
   1,
   0.8585167,
   1,
   0.8600158,
   1,
   0.7948599,
   1,
   1};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002[33] = {
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
   0,
   0,
   0,
   0};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002[33] = {
   1.652138,
   1,
   1,
   1.652138,
   1,
   1.396385,
   1,
   1.505775,
   1.505775,
   1,
   1.652138,
   1.566184,
   1.566184,
   1,
   1.566184,
   1,
   1,
   1,
   1.566184,
   1.566184,
   1,
   1.505775,
   1.352446,
   1,
   1.2266,
   1.176192,
   1,
   1.136629,
   1,
   1.178759,
   1,
   1.294919,
   1.425069};
   grae = new TGraphAsymmErrors(33,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002);
   grae->SetName("pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   grae->SetTitle("Pull of Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass and Projection of extMCmodel_DsPhiMuMuPi");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002 = new TH1F("Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002","Pull of Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass and Projection of extMCmodel_DsPhiMuMuPi",100,1.673818,2.046182);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMinimum(-3.786401);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMaximum(3.856821);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetDirectory(0);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetLineColor(ci);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitle("#mu#mu #pi mass (GeV)");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetRange(8,93);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitleOffset(1);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitleFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetTitle("(Data - curve) / #sigma_{data}");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetYaxis()->SetTitleFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetLabelFont(42);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetTitleOffset(1);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]3002);
   
   grae->Draw("p");
   
   TH1D *frame_adfef60__4 = new TH1D("frame_adfef60__4"," ",100,1.7,2.02);
   frame_adfef60__4->SetBinContent(1,5.5);
   frame_adfef60__4->SetMinimum(-5.5);
   frame_adfef60__4->SetMaximum(5.5);
   frame_adfef60__4->SetEntries(1);
   frame_adfef60__4->SetDirectory(0);
   frame_adfef60__4->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_adfef60__4->SetLineColor(ci);
   frame_adfef60__4->GetXaxis()->SetTitle("#mu#mu #pi mass (GeV)");
   frame_adfef60__4->GetXaxis()->SetLabelFont(42);
   frame_adfef60__4->GetXaxis()->SetLabelSize(0.1);
   frame_adfef60__4->GetXaxis()->SetTitleSize(0.1);
   frame_adfef60__4->GetXaxis()->SetTitleOffset(1);
   frame_adfef60__4->GetXaxis()->SetTitleFont(42);
   frame_adfef60__4->GetYaxis()->SetTitle("Pull");
   frame_adfef60__4->GetYaxis()->SetLabelFont(42);
   frame_adfef60__4->GetYaxis()->SetLabelSize(0.1);
   frame_adfef60__4->GetYaxis()->SetTitleSize(0.1);
   frame_adfef60__4->GetYaxis()->SetTitleFont(42);
   frame_adfef60__4->GetZaxis()->SetLabelFont(42);
   frame_adfef60__4->GetZaxis()->SetTitleOffset(1);
   frame_adfef60__4->GetZaxis()->SetTitleFont(42);
   frame_adfef60__4->Draw("AXISSAME");
   
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
