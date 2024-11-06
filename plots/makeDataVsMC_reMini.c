{
   gROOT->SetBatch(true);
  
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
  
   //SetInputFile( {"/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Cv4_HLT_overlap.root", "../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onTau3Mu.root "});
   SetInputFile( {"/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root", "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_signal_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root"});
   SetInputTree({"tree_w_BDT", "tree_w_BDT"});
   SetSelection({"(tau_fit_mass > 1.4 && tau_fit_mass < 1.72) || (tau_fit_mass > 1.84 && tau_fit_mass < 2.05) && (year_id < 230)", "(year_id < 230)"});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/DataVsMC/2022/");
   

   // Muons
   draw_branches({"tau_mu1_TightID_PV","tau_mu1_TightID_PV"}, {"data", "mc"}, "#mu_1 Tight ID (PV)", 2, -0.5, 1.5, "DataVsMC_reMini_Mu_TightID");
   draw_branches({"tau_mu12_fitM","tau_mu12_fitM"},  {"data", "mc"}, "M(#mu_{1},#mu_{2}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu12mass");
   draw_branches({"tau_mu13_fitM","tau_mu13_fitM"},  {"data", "mc"}, "M(#mu_{1},#mu_{3}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu13mass");
   draw_branches({"tau_mu23_fitM","tau_mu23_fitM"},  {"data", "mc"}, "M(#mu_{2},#mu_{3}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu23mass");
   
   // Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},  {"data", "mc"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "DataVsMC_reMini_fitTauMass");
   draw_branches({"tau_fit_mass_resol","tau_fit_mass_resol"},  {"data", "mc"}, "#sigma/M(3 #mu)", 50, 0.0, 0.025, "DataVsMC_reMini_fitTauMassResol");
   draw_branches({"n_tau","n_tau"},                {"data", "mc"}, "(#tau -> 3 #mu) candidates", 10, 0., 10., "DataVsMC_reMini_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},     {"data", "mc"}, "p_{T}(3 #mu) (GeV)", 40, 0, 80, "DataVsMC_reMini_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},    {"data", "mc"}, "#eta (3 #mu)", 70, -3.5, 3.5, "DataVsMC_reMini_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},    {"data", "mc"}, "#phi (3 #mu)", 31, -3.1, 3.1, "DataVsMC_reMini_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},     {"data", "mc"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "DataVsMC_reMini_Tau_relIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},{"data", "mc"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "DataVsMC_reMini_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},         {"data", "mc"}, "M_{T}(3 #mu)", 50, 0., 200., "DataVsMC_reMini_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},    {"data", "mc"}, "vtx-probability(3 #mu)", 40, 0., 1., "DataVsMC_reMini_Tau_Vprob", true);
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"}, {"data", "mc"}, "cos_{#alpha}(3#mu vtx, BS)", 50, 0., 1., "DataVsMC_reMini_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"}, {"data", "mc"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "DataVsMC_reMini_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt"    }, {"data", "mc"}, " p_{T}(MET) (GeV)", 75, 0., 150., "DataVsMC_reMini_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" }, {"data", "mc"}, " #phi (MET) ", 31, -3.1, 3.1, "DataVsMC_reMini_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},{"data", "mc"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 60, 0., 6., "DataVsMC_reMini_pTratio_PuppiMET");
   draw_branches({"miss_pz_min", "miss_pz_min"},{"data", "mc"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "DataVsMC_reMini_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},{"data", "mc"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "DataVsMC_reMini_miss_pz_max");

   // W
   draw_branches({"W_pt","W_pt"}, {"data", "mc"}, "W p_{T} (GeV)", 80, 0.0, 150.0, "DataVsMC_reMini_WpT");
   draw_branches({"W_phi","W_phi"}, {"data", "mc"}, " W #phi", 31, -3.1, 3.1, "DataVsMC_reMini_Wphi");
   draw_branches({"W_eta_min","W_eta_min"}, {"data", "mc"}, "W #eta(min)", 70, -3.5, 3.5, "DataVsMC_reMini_Wetamin");
   draw_branches({"W_eta_max","W_eta_max"}, {"data", "mc"}, "W #eta (max)", 70, -3.5, 3.5, "DataVsMC_reMini_Wetamax");
   draw_branches({"W_mass_min","W_mass_min"}, {"data", "mc"}, "W mass min", 100, 70, 90, "DataVsMC_reMini_Wmassmin", true);
   draw_branches({"W_mass_max","W_mass_max"}, {"data", "mc"}, "W mass max", 100, 70, 90, "DataVsMC_reMini_Wmassmax", true);
  
}
