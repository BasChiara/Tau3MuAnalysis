#ifdef __CLING__
#pragma cling optimize(0)
#endif
void mcDsPhiPi_mass_catABCRun3_ANv7_peakB()
{
//=========Macro generated from canvas: c/c
//=========  (Mon Aug 11 19:44:05 2025) by ROOT version 6.26/11
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
   up_pad->Range(1.636,0,2.062667,76.52634);
   up_pad->SetFillColor(0);
   up_pad->SetBorderMode(0);
   up_pad->SetBorderSize(2);
   up_pad->SetLeftMargin(0.15);
   up_pad->SetBottomMargin(0);
   up_pad->SetFrameBorderMode(0);
   up_pad->SetFrameBorderMode(0);
   
   TH1D *frame_b40c010__1 = new TH1D("frame_b40c010__1"," ",100,1.7,2.02);
   frame_b40c010__1->SetBinContent(1,68.87371);
   frame_b40c010__1->SetMaximum(68.87371);
   frame_b40c010__1->SetEntries(1);
   frame_b40c010__1->SetDirectory(0);
   frame_b40c010__1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   frame_b40c010__1->SetLineColor(ci);
   frame_b40c010__1->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_b40c010__1->GetXaxis()->SetLabelFont(42);
   frame_b40c010__1->GetXaxis()->SetTitleOffset(1);
   frame_b40c010__1->GetXaxis()->SetTitleFont(42);
   frame_b40c010__1->GetYaxis()->SetTitle("Events / ( 0.01 GeV )");
   frame_b40c010__1->GetYaxis()->SetLabelFont(42);
   frame_b40c010__1->GetYaxis()->SetTitleFont(42);
   frame_b40c010__1->GetZaxis()->SetLabelFont(42);
   frame_b40c010__1->GetZaxis()->SetTitleOffset(1);
   frame_b40c010__1->GetZaxis()->SetTitleFont(42);
   frame_b40c010__1->Draw("FUNC");
   
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
   3.898015,
   3.890834,
   3.883668,
   3.876517,
   3.869379,
   3.862257,
   3.855149,
   3.848057,
   3.840981,
   3.83392,
   3.826876,
   3.819848,
   3.812838,
   3.805847,
   3.798874,
   3.791922,
   3.784991,
   3.778083,
   3.7712,
   3.764342,
   3.757514,
   3.750718,
   3.743956,
   3.737234,
   3.730555,
   3.723925,
   3.717352,
   3.710842,
   3.704406,
   3.698055,
   3.691802,
   3.685664,
   3.679661,
   3.673815,
   3.668155,
   3.662715,
   3.657537,
   3.652669,
   3.648171,
   3.644116,
   3.640591,
   3.637703,
   3.635582,
   3.634385,
   3.634305,
   3.635575,
   3.638484,
   3.643382,
   3.650701,
   3.660971,
   3.674844,
   3.693125,
   3.716806,
   3.747115,
   3.785576,
   3.834078,
   3.894971,
   3.971184,
   4.066372,
   4.185107,
   4.333118,
   4.517597,
   4.747593,
   5.034515,
   5.392772,
   5.840606,
   6.401162,
   7.103863,
   7.986205,
   9.096077,
   10.49478,
   11.32622,
   12.26098,
   13.31245,
   14.49585,
   15.82843,
   17.32984,
   19.02243,
   20.93134,
   23.0112,
   25.20444,
   29.86483,
   34.74507,
   39.62714,
   44.25602,
   46.39069,
   48.36041,
   50.13296,
   51.67841,
   52.97,
   53.9849,
   54.70485,
   55.11675,
   55.21301,
   54.9918,
   54.45712,
   53.61867,
   52.49154,
   51.09577,
   49.45574,
   47.59951,
   45.55794,
   43.36393,
   38.6548,
   33.74219,
   28.87559,
   24.26434,
   22.10577,
   20.06551,
   18.15432,
   16.37951,
   14.74521,
   13.25263,
   11.9004,
   10.68491,
   9.60074,
   8.641016,
   7.797765,
   7.062272,
   5.877816,
   5.013935,
   5.013935};
   TGraph *graph = new TGraph(122,extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx1,extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy1);
   graph->SetName("extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   graph->SetTitle("Projection of extMCmodel_DsPhiMuMuPi");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   
   TH1F *Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1 = new TH1F("Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1","Projection of extMCmodel_DsPhiMuMuPi",122,1.668,2.052);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMinimum(3.270874);
   Graph_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB1->SetMaximum(60.37088);
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
   
   Double_t h_mc_DsPhiMuMuPi_fx3001[32] = {
   1.705,
   1.715,
   1.725,
   1.735,
   1.745,
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
   2.015};
   Double_t h_mc_DsPhiMuMuPi_fy3001[32] = {
   4,
   2,
   1,
   5,
   2,
   10,
   3,
   5,
   5,
   1,
   5,
   4,
   5,
   2,
   4,
   3,
   2,
   4,
   5,
   2,
   8,
   7,
   10,
   17,
   39,
   43,
   57,
   51,
   37,
   21,
   15,
   6};
   Double_t h_mc_DsPhiMuMuPi_felx3001[32] = {
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
   Double_t h_mc_DsPhiMuMuPi_fely3001[32] = {
   1.914339,
   1.291815,
   0.8272462,
   2.159691,
   1.291815,
   3.108694,
   1.632705,
   2.159691,
   2.159691,
   0.8272462,
   2.159691,
   1.914339,
   2.159691,
   1.291815,
   1.914339,
   1.632705,
   1.291815,
   1.914339,
   2.159691,
   1.291815,
   2.768386,
   2.58147,
   3.108694,
   4.082184,
   6.218102,
   6.531834,
   7.527619,
   7.117933,
   6.055143,
   4.545807,
   3.82938,
   2.379931};
   Double_t h_mc_DsPhiMuMuPi_fehx3001[32] = {
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
   Double_t h_mc_DsPhiMuMuPi_fehy3001[32] = {
   3.162753,
   2.63786,
   2.299527,
   3.382473,
   2.63786,
   4.26695,
   2.918186,
   3.382473,
   3.382473,
   2.299527,
   3.382473,
   3.162753,
   3.382473,
   2.63786,
   3.162753,
   2.918186,
   2.63786,
   3.162753,
   3.382473,
   2.63786,
   3.945142,
   3.770281,
   4.26695,
   5.203719,
   7.298372,
   7.608278,
   8.594007,
   8.188122,
   7.137555,
   5.655182,
   4.958738,
   3.583642};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(32,h_mc_DsPhiMuMuPi_fx3001,h_mc_DsPhiMuMuPi_fy3001,h_mc_DsPhiMuMuPi_felx3001,h_mc_DsPhiMuMuPi_fehx3001,h_mc_DsPhiMuMuPi_fely3001,h_mc_DsPhiMuMuPi_fehy3001);
   grae->SetName("h_mc_DsPhiMuMuPi");
   grae->SetTitle("Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass");

   ci = TColor::GetColor("#ff0000");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);
   grae->SetLineWidth(2);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_h_mc_DsPhiMuMuPi3001 = new TH1F("Graph_h_mc_DsPhiMuMuPi3001","Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass",100,1.674,2.046);
   Graph_h_mc_DsPhiMuMuPi3001->SetMinimum(0.1554784);
   Graph_h_mc_DsPhiMuMuPi3001->SetMaximum(72.13613);
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
   TText *pt_LaTex = pt->AddText("alpha = -0.6 +/- 2");
   pt_LaTex = pt->AddText("alphaCB_mc =  1.5 +/- 0.5");
   pt_LaTex = pt->AddText("dM_mc = -0.0009 +/- 0.002");
   pt_LaTex = pt->AddText("nCB_mc =  23 +/- 238");
   pt_LaTex = pt->AddText("nCombMC =  114 +/- 24");
   pt_LaTex = pt->AddText("nMC =  271 +/- 27");
   pt_LaTex = pt->AddText("width_mc =  0.020 +/- 0.002");
   pt->Draw();
   
   TH1D *frame_b40c010__2 = new TH1D("frame_b40c010__2"," ",100,1.7,2.02);
   frame_b40c010__2->SetBinContent(1,68.87371);
   frame_b40c010__2->SetMaximum(68.87371);
   frame_b40c010__2->SetEntries(1);
   frame_b40c010__2->SetDirectory(0);
   frame_b40c010__2->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_b40c010__2->SetLineColor(ci);
   frame_b40c010__2->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_b40c010__2->GetXaxis()->SetLabelFont(42);
   frame_b40c010__2->GetXaxis()->SetTitleOffset(1);
   frame_b40c010__2->GetXaxis()->SetTitleFont(42);
   frame_b40c010__2->GetYaxis()->SetTitle("Events / ( 0.01 GeV )");
   frame_b40c010__2->GetYaxis()->SetLabelFont(42);
   frame_b40c010__2->GetYaxis()->SetTitleFont(42);
   frame_b40c010__2->GetZaxis()->SetLabelFont(42);
   frame_b40c010__2->GetZaxis()->SetTitleOffset(1);
   frame_b40c010__2->GetZaxis()->SetTitleFont(42);
   frame_b40c010__2->Draw("AXISSAME");
   
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
   ratio_pad->Range(1.636,-12.83333,2.062667,5.5);
   ratio_pad->SetFillColor(0);
   ratio_pad->SetBorderMode(0);
   ratio_pad->SetBorderSize(2);
   ratio_pad->SetLeftMargin(0.15);
   ratio_pad->SetTopMargin(0);
   ratio_pad->SetBottomMargin(0.4);
   ratio_pad->SetFrameBorderMode(0);
   ratio_pad->SetFrameBorderMode(0);
   
   TH1D *frame_b9a4b50__3 = new TH1D("frame_b9a4b50__3"," ",100,1.7,2.02);
   frame_b9a4b50__3->SetBinContent(1,5.5);
   frame_b9a4b50__3->SetMinimum(-5.5);
   frame_b9a4b50__3->SetMaximum(5.5);
   frame_b9a4b50__3->SetEntries(1);
   frame_b9a4b50__3->SetDirectory(0);
   frame_b9a4b50__3->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_b9a4b50__3->SetLineColor(ci);
   frame_b9a4b50__3->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_b9a4b50__3->GetXaxis()->SetLabelFont(42);
   frame_b9a4b50__3->GetXaxis()->SetLabelSize(0.1);
   frame_b9a4b50__3->GetXaxis()->SetTitleSize(0.1);
   frame_b9a4b50__3->GetXaxis()->SetTitleOffset(1);
   frame_b9a4b50__3->GetXaxis()->SetTitleFont(42);
   frame_b9a4b50__3->GetYaxis()->SetTitle("Pull");
   frame_b9a4b50__3->GetYaxis()->SetLabelFont(42);
   frame_b9a4b50__3->GetYaxis()->SetLabelSize(0.1);
   frame_b9a4b50__3->GetYaxis()->SetTitleSize(0.1);
   frame_b9a4b50__3->GetYaxis()->SetTitleFont(42);
   frame_b9a4b50__3->GetZaxis()->SetLabelFont(42);
   frame_b9a4b50__3->GetZaxis()->SetTitleOffset(1);
   frame_b9a4b50__3->GetZaxis()->SetTitleFont(42);
   frame_b9a4b50__3->Draw("FUNC");
   
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002[32] = {
   1.705,
   1.715,
   1.725,
   1.735,
   1.745,
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
   2.015};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002[32] = {
   0.05912814,
   -0.7068186,
   -1.236043,
   0.5462376,
   -0.6817835,
   2.001868,
   -0.2588604,
   0.5860428,
   0.5955872,
   -1.171458,
   0.6135199,
   0.17865,
   0.627801,
   -0.620107,
   0.1895428,
   -0.2249255,
   -0.6477494,
   0.09225003,
   0.4361672,
   -0.9579772,
   0.9164518,
   -0.09212033,
   -0.2766384,
   -0.4092572,
   1.022036,
   -0.504839,
   0.3365222,
   0.01911217,
   -0.1771672,
   -0.4658922,
   0.6198176,
   -0.186246};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002[32] = {
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
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002[32] = {
   1,
   0.4897207,
   0.3597463,
   1,
   0.4897207,
   1,
   0.559493,
   1,
   1,
   0.3597463,
   1,
   1,
   1,
   0.4897207,
   1,
   0.559493,
   0.4897207,
   1,
   1,
   0.4897207,
   1,
   0.6846892,
   0.7285519,
   0.7844743,
   1,
   0.8585167,
   1,
   1,
   0.8483497,
   0.8038304,
   1,
   0.6641098};
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002[32] = {
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
   Double_t pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002[32] = {
   1.652138,
   1,
   1,
   1.566184,
   1,
   1.372586,
   1,
   1.566184,
   1.566184,
   1,
   1.566184,
   1.652138,
   1.566184,
   1,
   1.652138,
   1,
   1,
   1.652138,
   1.566184,
   1,
   1.425069,
   1,
   1,
   1,
   1.17373,
   1,
   1.141663,
   1.150351,
   1,
   1,
   1.294919,
   1};
   grae = new TGraphAsymmErrors(32,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fy3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_felx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehx3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fely3002,pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_fehy3002);
   grae->SetName("pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_Norm[tau_MuMuPi_mass]_Range[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]_NormRange[fit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPi]");
   grae->SetTitle("Pull of Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass and Projection of extMCmodel_DsPhiMuMuPi");
   grae->SetFillStyle(1000);
   grae->SetMarkerStyle(8);
   
   TH1F *Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002 = new TH1F("Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002","Pull of Histogram of mc_DsPhiMuMuPi_plot__tau_MuMuPi_mass and Projection of extMCmodel_DsPhiMuMuPi",100,1.674,2.046);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMinimum(-2.092814);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetMaximum(3.871479);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetDirectory(0);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->SetLineColor(ci);
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   Graph_pull_h_mc_DsPhiMuMuPi_extMCmodel_DsPhiMuMuPi_NormoBtau_MuMuPi_masscB_RangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB_NormRangeoBfit_nll_extMCmodel_DsPhiMuMuPi_mc_DsPhiMuMuPicB3002->GetXaxis()->SetRange(7,94);
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
   
   TH1D *frame_b9a4b50__4 = new TH1D("frame_b9a4b50__4"," ",100,1.7,2.02);
   frame_b9a4b50__4->SetBinContent(1,5.5);
   frame_b9a4b50__4->SetMinimum(-5.5);
   frame_b9a4b50__4->SetMaximum(5.5);
   frame_b9a4b50__4->SetEntries(1);
   frame_b9a4b50__4->SetDirectory(0);
   frame_b9a4b50__4->SetStats(0);

   ci = TColor::GetColor("#000099");
   frame_b9a4b50__4->SetLineColor(ci);
   frame_b9a4b50__4->GetXaxis()->SetTitle("m_{#mu#mu#pi} (GeV)");
   frame_b9a4b50__4->GetXaxis()->SetLabelFont(42);
   frame_b9a4b50__4->GetXaxis()->SetLabelSize(0.1);
   frame_b9a4b50__4->GetXaxis()->SetTitleSize(0.1);
   frame_b9a4b50__4->GetXaxis()->SetTitleOffset(1);
   frame_b9a4b50__4->GetXaxis()->SetTitleFont(42);
   frame_b9a4b50__4->GetYaxis()->SetTitle("Pull");
   frame_b9a4b50__4->GetYaxis()->SetLabelFont(42);
   frame_b9a4b50__4->GetYaxis()->SetLabelSize(0.1);
   frame_b9a4b50__4->GetYaxis()->SetTitleSize(0.1);
   frame_b9a4b50__4->GetYaxis()->SetTitleFont(42);
   frame_b9a4b50__4->GetZaxis()->SetLabelFont(42);
   frame_b9a4b50__4->GetZaxis()->SetTitleOffset(1);
   frame_b9a4b50__4->GetZaxis()->SetTitleFont(42);
   frame_b9a4b50__4->Draw("AXISSAME");
   
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
