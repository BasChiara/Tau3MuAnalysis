{
   gROOT->SetBatch(true);
  
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
  
   SetInputFile( {"../outRoot/recoKinematicsT3m_MC_2022EE_reMini_HLT_Tau3Mu.root ","/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/recoKinematicsT3m_ParkingDoubleMuonLowMass_2022F.root"});
   SetInputTree({"Tau3Mu_HLTemul_tree", "Tau3Mu_HLTemul_tree"});
   SetSelection({"","(tau_fit_mass > 1.6 && tau_fit_mass < 1.72) || (tau_fit_mass > 1.84 && tau_fit_mass < 2.0)"});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/DataVsMC/2022/reMini/");

   // Muons
   draw_branches({"Mu_TightID","Mu_TightID"},  {"mc","data22"}, "#mu Tight ID (PV)", 2, -0.5, 1.5, "DataVsMC_reMini_Mu_TightID");
   draw_branches({"tau_mu12_fitM","tau_mu12_fitM"},  {"mc","data22"}, "M(#mu_{1},#mu_{2}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu12mass");
   draw_branches({"tau_mu13_fitM","tau_mu13_fitM"},  {"mc","data22"}, "M(#mu_{1},#mu_{3}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu13mass");
   draw_branches({"tau_mu23_fitM","tau_mu23_fitM"},  {"mc","data22"}, "M(#mu_{2},#mu_{3}) (GeV)", 100, 0.5, 1.5, "DataVsMC_reMini_Mu23mass");
   
   // Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},  {"mc","data22"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "DataVsMC_reMini_fitTauMass");
   draw_branches({"n_tau","n_tau"},                {"mc","data22"}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., "DataVsMC_reMini_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},     {"mc","data22"}, "p_{T}(3 #mu) (GeV)", 40, 0, 80, "DataVsMC_reMini_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},    {"mc","data22"}, "#eta (3 #mu)", 70, -3.5, 3.5, "DataVsMC_reMini_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},    {"mc","data22"}, "#phi (3 #mu)", 31, -3.1, 3.1, "DataVsMC_reMini_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},     {"mc","data22"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "DataVsMC_reMini_Tau_relIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},{"mc","data22"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "DataVsMC_reMini_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},         {"mc","data22"}, "M_{T}(3 #mu)", 50, 0., 200., "DataVsMC_reMini_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},    {"mc","data22"}, "vtx-probability(3 #mu)", 40, 0., 1., "DataVsMC_reMini_Tau_Vprob");
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"}, {"mc","data22"}, "cos_{#alpha}(3#mu vtx, BS)", 50, 0., 1., "DataVsMC_reMini_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"}, {"mc","data22"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "DataVsMC_reMini_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt"    }, {"mc","data22"}, " p_{T}(MET) (GeV)", 75, 0., 150., "DataVsMC_reMini_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" }, {"mc","data22"}, " #phi (MET) ", 31, -3.1, 3.1, "DataVsMC_reMini_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},{"mc","data22"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 60, 0., 6., "DataVsMC_reMini_pTratio_PuppiMET");
   draw_branches({"miss_pz_min", "miss_pz_min"},{"mc","data22"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "DataVsMC_reMini_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},{"mc","data22"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "DataVsMC_reMini_miss_pz_max");

   // W
   draw_branches({"W_pt","W_pt"}, {"mc","data22"}, "W p_{T} (GeV)", 80, 0.0, 150.0, "DataVsMC_reMini_WpT");
   draw_branches({"W_phi","W_phi"}, {"mc","data22"}, " W #phi", 31, -3.1, 3.1, "DataVsMC_reMini_Wphi");
   draw_branches({"W_eta_min","W_eta_min"}, {"mc","data22"}, "W #eta(min)", 70, -3.5, 3.5, "DataVsMC_reMini_Wetamin");
   draw_branches({"W_eta_max","W_eta_max"}, {"mc","data22"}, "W #eta (max)", 70, -3.5, 3.5, "DataVsMC_reMini_Wetamax");
   draw_branches({"W_mass_min","W_mass_min"}, {"mc","data22"}, "W mass min", 100, 70, 90, "DataVsMC_reMini_Wmassmin");
  
}
