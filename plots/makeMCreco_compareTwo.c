{
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gROOT->SetBatch(true);
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   
   bool is_MC = true;
   //SetInputFile( {"/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_fulltrainUnBalanced_emulateRun2_kFold_2024Apr17.root", "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_fulltrainReBalanced_emulateRun2_kFold_2024Apr17.root"});
   //SetInputFile( {"../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu.root", "../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu.root"});
   //SetInputFile( {"../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onTau3Mu.root", "../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onZTau3Mu.root"});
   SetInputFile( {"../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onTau3Mu.root", "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_W3MuNu_MC_noLxyScut.root"});
   //SetInputTree( {"WTau3Mu_tree", "WTau3Mu_tree"});
   SetInputTree( {"WTau3Mu_tree", "tree_w_BDT"});
   SetSelection( {"(tau_fit_mass>1.6) && (tau_fit_mass<2.0)","(tau_fit_mass>1.6) && (tau_fit_mass<2.0)"});
   TString cat_1 = "Tau3Mu";
   TString cat_2 = "W3MuNu";
   TString out_tag = "T3MvsW3Mu";
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/WTau3MuVSW3MuNu/");

   // W vs Z
   draw_2D_branches({"tau_met_pt","tau_met_Dphi"},             {cat_1,cat_2}, "MET (GeV)", 20, 0., 100., "#Delta #phi (3 #mu, MET)", 15, 0., 6., out_tag + "_METvsDphi");

   // Muons
   draw_branches({"tau_mu1_TightID_PV","tau_mu1_TightID_PV"},  {cat_1,cat_2}, "#mu1 Tight ID (PV)", 2, -0.5, 1.5, out_tag + "_Mu_TightID");
   draw_branches({"tau_mu1_SoftID_PV","tau_mu1_SoftID_PV"},    {cat_1,cat_2}, "#mu1 Soft ID (PV)", 2, -0.5, 1.5, out_tag + "_Mu_SoftID");
   draw_branches({"tau_mu1_pt", "tau_mu1_pt"},                 {cat_1,cat_2}, "p_{T}(#mu_{1}) (GeV)", 50, 0.,50., out_tag + "_LeadingMuon_pT");
   draw_branches({"tau_mu2_pt", "tau_mu2_pt"},                 {cat_1,cat_2}, "p_{T}(#mu_{2}) (GeV)", 50, 0.,50., out_tag + "_SubleadingMuon_pT");
   draw_branches({"tau_mu3_pt", "tau_mu3_pt"},                 {cat_1,cat_2}, "p_{T}(#mu_{3}) (GeV)", 50, 0.,50., out_tag + "_TrailingMuon_pT");
   draw_branches({"tau_mu1_eta", "tau_mu1_eta"},               {cat_1,cat_2}, "#eta (#mu_{1})", 25, -2.5, 2.5, out_tag + "_LeadingMuon_eta");
   draw_branches({"tau_mu2_eta", "tau_mu2_eta"},               {cat_1,cat_2}, "#eta (#mu_{2})", 25, -2.5, 2.5, out_tag + "_SubleadingMuon_eta");
   draw_branches({"tau_mu3_eta", "tau_mu3_eta"},               {cat_1,cat_2}, "#eta (#mu_{3})", 25, -2.5, 2.5, out_tag + "_TrailingMuon_eta");
   draw_branches({"tau_mu12_dZ", "tau_mu12_dZ"},               {cat_1,cat_2}, "#Delta z(#mu_{1}, #mu_{2}) (cm)", 50, 0., .5, out_tag + "_tau_mu12_dZ", true);
   draw_branches({"tau_mu23_dZ", "tau_mu23_dZ"},               {cat_1,cat_2}, "#Delta z(#mu_{2}, #mu_{3}) (cm)", 50, 0., .5, out_tag + "_tau_mu23_dZ", true);
   draw_branches({"tau_mu13_dZ", "tau_mu13_dZ"},               {cat_1,cat_2}, "#Delta z(#mu_{1}, #mu_{3}) (cm)", 50, 0., .5, out_tag + "_tau_mu13_dZ", true);
   draw_branches({"tau_mu12_fitM","tau_mu12_fitM"},            {cat_1,cat_2}, "M(#mu_{1},#mu_{2}) (GeV)", 80, 0., 2.0, out_tag + "_Mu12mass");
   draw_branches({"tau_mu13_fitM","tau_mu13_fitM"},            {cat_1,cat_2}, "M(#mu_{1},#mu_{3}) (GeV)", 80, 0., 2.0, out_tag + "_Mu13mass");
   draw_branches({"tau_mu23_fitM","tau_mu23_fitM"},            {cat_1,cat_2}, "M(#mu_{2},#mu_{3}) (GeV)", 80, 0., 2.0, out_tag + "_Mu23mass");
   // DR mu-tau
   //TString DR_tau_mu1 = "sqrt( (tau_mu1_eta-tau_fit_eta)*(tau_mu1_eta-tau_fit_eta) + (tau_mu1_phi-tau_fit_phi)*(tau_mu1_phi-tau_fit_phi) )";
   //draw_branches({DR_tau_mu1, DR_tau_mu1},  {cat_1,cat_2}, "#Delta R(#mu_{1},3#mu)", 30, 0.0, 0.9, out_tag + "_DRTauMu1",true);
   
   // Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},              {cat_1,cat_2}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, out_tag + "_fitTauMass");
   draw_branches({"tau_fit_mass_resol","tau_fit_mass_resol"},  {cat_1,cat_2}, "#sigma/M(3 #mu)", 50, 0., 0.025, out_tag + "_fitTauMass_resol");
   draw_branches({"n_tau","n_tau"},                            {cat_1,cat_2}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., out_tag + "_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},                 {cat_1,cat_2}, "p_{T}(3 #mu) (GeV)", 40, 0, 80, out_tag + "_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},                {cat_1,cat_2}, "#eta (3 #mu)", 25, -2.5, 2.5, out_tag + "_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},                {cat_1,cat_2}, "#phi (3 #mu)", 63, -3.15, 3.15, out_tag + "_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},                 {cat_1,cat_2}, "rel. isolation (3 #mu)", 100, 0, 0.5, out_tag + "_Tau_relIso", true);
   draw_branches({"tau_relIso*tau_fit_pt", "tau_relIso*tau_fit_pt"},{cat_1,cat_2}, "abs isolation (3 #mu)", 80, 0, 20.0, out_tag + "_Tau_absIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},        {cat_1,cat_2}, "L_{xy}(SV)/#sigma", 80, 0, 20, out_tag + "_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},                 {cat_1,cat_2}, "M_{T}(3 #mu)", 50, 0., 200., out_tag + "_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},            {cat_1,cat_2}, "vtx-probability(3 #mu)", 40, 0., 1., out_tag + "_Tau_Vprob");
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"},        {cat_1,cat_2}, "cos #alpha(SV,BS)", 40, 0., 1., out_tag + "_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"},             {cat_1,cat_2}, "#Delta #phi (3 #mu, MET)", 63, 0., 6.3, out_tag + "_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt" },                {cat_1,cat_2}, " MET (GeV)", 30, 0., 150., out_tag + "_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" },              {cat_1,cat_2}, " #phi (MET) ", 63, -3.15, 3.15, out_tag + "_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},     {cat_1,cat_2}, " p_{T}^{3 #mu}/MET", 50, 0., 4., out_tag + "_pTratio_PuppiMET");
   draw_branches({"miss_pz_min", "miss_pz_min"},               {cat_1,cat_2}, " min p_{z}^{#nu} (GeV)", 50, -300., 300., out_tag + "_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},               {cat_1,cat_2}, " max p_{z}^{#nu} (GeV)", 50, -1000., 1000., out_tag + "_miss_pz_max");

   /// W
   draw_branches({"W_pt","W_pt"},                              {cat_1,cat_2}, "W p_{T} (GeV)",     50, 0.0, 150.0, out_tag + "_WpT_rIso0p2");
   draw_branches({"W_phi","W_phi"},                            {cat_1,cat_2}, "W #phi",            63, -3.15, 3.15, out_tag + "_Wphi");
   draw_branches({"W_eta_min","W_eta_min"},                    {cat_1,cat_2}, "W #eta(min)",       35, -3.5, 3.5, out_tag + "_Wetamin");
   draw_branches({"W_eta_max","W_eta_max"},                    {cat_1,cat_2}, "W #eta (max)",      50, -5, 5, out_tag + "_Wetamax");
   draw_branches({"W_mass_min","W_mass_min"},                  {cat_1,cat_2}, "M(W)_{min} (GeV)",  20, 70, 90, out_tag + "_Wmassmin", true);
   draw_branches({"W_mass_max","W_mass_max"},                  {cat_1,cat_2}, "M(W)_{max} (GeV)",  20, 70, 90, out_tag + "_Wmassmax", true);
  
}
