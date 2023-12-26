{
   gROOT->SetBatch(true);
  
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
  
   SetInputFile( {"/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022/recoKinematicsT3m_open_ParkingDoubleMuonLowMass_2022F.root","/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root"});
   SetInputTree({"Tau3Mu_HLTemul_tree", "Tau3Mu_HLTemul_tree"});
   SetSelection({"tau_fit_mass < 1.72 || tau_fit_mass > 1.84","tau_fit_mass < 1.72 || tau_fit_mass > 1.84"});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/DataRun3_promptVSreMini/");
   
   //Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},  {"Run3_prompt","Run3_reMini"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "Run3promptVSreMini_fitTauMass",false, false);
   draw_branches({"n_tau","n_tau"},                {"Run3_prompt","Run3_reMini"}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., "Run3promptVSreMini_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},     {"Run3_prompt","Run3_reMini"}, "p_{T}(3 #mu) (GeV)", 40, 10, 100, "Run3promptVSreMini_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},    {"Run3_prompt","Run3_reMini"}, "#eta (3 #mu)", 70, -3.5, 3.5, "Run3promptVSreMini_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},    {"Run3_prompt","Run3_reMini"}, "#phi (3 #mu)", 62, -3.1, 3.1, "Run3promptVSreMini_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},     {"Run3_prompt","Run3_reMini"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "Run3promptVSreMini_Tau_relIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},{"Run3_prompt","Run3_reMini"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "Run3promptVSreMini_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},         {"Run3_prompt","Run3_reMini"}, "M_{T}(3 #mu)", 50, 0., 200., "Run3promptVSreMini_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},    {"Run3_prompt","Run3_reMini"}, "vtx-probability(3 #mu)", 20, 0., 1., "Run3promptVSreMini_Tau_Vprob");
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"}, {"Run3_prompt","Run3_reMini"}, "cos_{#alpha}(3#mu vtx, BS)", 100, -1., 1., "Run3promptVSreMini_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"}, {"Run3_prompt","Run3_reMini"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "Run3promptVSreMini_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt"    }, {"Run3_prompt","Run3_reMini"}, " p_{T}(MET) (GeV)", 40, 0., 100., "Run3promptVSreMini_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" }, {"Run3_prompt","Run3_reMini"}, " #phi (MET) ", 62, -3.1, 3.1, "Run3promptVSreMini_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},{"Run3_prompt","Run3_reMini"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 100, 0., 40., "Run3promptVSreMini_pTratio_PuppiMET", true);
   draw_branches({"miss_pz_min", "miss_pz_min"},{"Run3_prompt","Run3_reMini"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "Run3promptVSreMini_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},{"Run3_prompt","Run3_reMini"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "Run3promptVSreMini_miss_pz_max");

   // W
   draw_branches({"W_pt","W_pt"}, {"Run3_prompt","Run3_reMini"}, "W p_{T} (GeV)", 50, 0.0, 150.0, "Run3promptVSreMini_WpT");
  
}
