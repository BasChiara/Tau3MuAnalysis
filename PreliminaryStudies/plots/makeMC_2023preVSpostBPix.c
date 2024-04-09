{
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gROOT->SetBatch(true);
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   
   bool is_MC = true;
   SetInputFile( {"../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_Tau3Mu.root","../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_Tau3Mu.root"});
   SetInputTree( {"WTau3Mu_tree", "WTau3Mu_tree"});
   SetSelection( {"", ""});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2023_preVSpostBPix/");

   // Muons
   draw_branches({"tau_mu1_TightID_PV","tau_mu1_TightID_PV"}, {"2023preBPix","2023BPix"}, "#mu1 Tight ID (PV)", 2, -0.5, 1.5, "BPixComp_Mu_TightID");
   draw_branches({"tau_mu1_SoftID_PV","tau_mu1_SoftID_PV"}, {"2023preBPix","2023BPix"}, "#mu1 Tight ID (PV)", 2, -0.5, 1.5, "BPixComp_Mu_SoftID");
   draw_branches({"tau_mu1_pt", "tau_mu1_pt"},   {"2023preBPix","2023BPix"}, "p_{T}(#mu_{1}) (GeV)", 50, 0.,50., "BPixComp_LeadingMuon_pT");
   draw_branches({"tau_mu2_pt", "tau_mu2_pt"},   {"2023preBPix","2023BPix"}, "p_{T}(#mu_{2}) (GeV)", 50, 0.,50., "BPixComp_SubleadingMuon_pT");
   draw_branches({"tau_mu3_pt", "tau_mu3_pt"},   {"2023preBPix","2023BPix"}, "p_{T}(#mu_{3}) (GeV)", 50, 0.,50., "BPixComp_TrailingMuon_pT");
   draw_branches({"tau_mu1_eta", "tau_mu1_eta"}, {"2023preBPix","2023BPix"},"#eta (#mu_{1})", 35, -3.5, 3.5, "BPixComp_    LeadingMuon_eta");
   draw_branches({"tau_mu2_eta", "tau_mu2_eta"}, {"2023preBPix","2023BPix"},"#eta (#mu_{2})", 35, -3.5, 3.5, "BPixComp_    SubleadingMuon_eta");
   draw_branches({"tau_mu3_eta", "tau_mu3_eta"}, {"2023preBPix","2023BPix"},"#eta (#mu_{3})", 35, -3.5, 3.5, "BPixComp_    TrailingMuon_eta");
   draw_branches({"tau_mu12_dZ", "tau_mu12_dZ"}, {"2023preBPix","2023BPix"},"#Delta z(#mu_{1}, #mu_{2}) (cm)", 30, 0., 3., "BPixComp_tau_mu12_dZ", true);
   draw_branches({"tau_mu23_dZ", "tau_mu23_dZ"}, {"2023preBPix","2023BPix"},"#Delta z(#mu_{2}, #mu_{3}) (cm)", 30, 0., 3., "BPixComp_tau_mu23_dZ", true);
   draw_branches({"tau_mu13_dZ", "tau_mu13_dZ"}, {"2023preBPix","2023BPix"},"#Delta z(#mu_{1}, #mu_{3}) (cm)", 30, 0., 3., "BPixComp_tau_mu13_dZ", true);
   draw_branches({"tau_mu12_fitM","tau_mu12_fitM"},  {"2023preBPix","2023BPix"}, "M(#mu_{1},#mu_{2}) (GeV)", 80, 0., 2.0, "BPixComp_Mu12mass");
   draw_branches({"tau_mu13_fitM","tau_mu13_fitM"},  {"2023preBPix","2023BPix"}, "M(#mu_{1},#mu_{3}) (GeV)", 80, 0., 2.0, "BPixComp_Mu13mass");
   draw_branches({"tau_mu23_fitM","tau_mu23_fitM"},  {"2023preBPix","2023BPix"}, "M(#mu_{2},#mu_{3}) (GeV)", 80, 0., 2.0, "BPixComp_Mu23mass");
   // DR mu-tau
   TString DR_tau_mu1 = "sqrt( (tau_mu1_eta-tau_fit_eta)*(tau_mu1_eta-tau_fit_eta) + (tau_mu1_phi-tau_fit_phi)*(tau_mu1_phi-tau_fit_phi) )";
   //draw_branches({DR_tau_mu1, DR_tau_mu1},  {"2023preBPix","2023BPix"}, "#Delta R(#mu_{1},3#mu)", 30, 0.0, 0.9, "BPixComp_DRTauMu1",true);
   
   // Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},  {"2023preBPix","2023BPix"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "BPixComp_fitTauMass");
   draw_branches({"tau_fit_mass_resol","tau_fit_mass_resol"},  {"2023preBPix","2023BPix"}, "#sigma/M(3 #mu)", 50, 0., 0.025, "BPixComp_fitTauMass_resol");
   draw_branches({"n_tau","n_tau"},                {"2023preBPix","2023BPix"}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., "BPixComp_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},     {"2023preBPix","2023BPix"}, "p_{T}(3 #mu) (GeV)", 40, 0, 80, "BPixComp_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},    {"2023preBPix","2023BPix"}, "#eta (3 #mu)", 35, -3.5, 3.5, "BPixComp_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},    {"2023preBPix","2023BPix"}, "#phi (3 #mu)", 31, -3.1, 3.1, "BPixComp_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},     {"2023preBPix","2023BPix"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "BPixComp_Tau_relIso", true);
   draw_branches({"tau_relIso*tau_fit_pt", "tau_relIso*tau_fit_pt"},     {"2023preBPix","2023BPix"}, "abs isolation (3 #mu)", 80, 0, 20.0, "BPixComp_Tau_absIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},{"2023preBPix","2023BPix"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "BPixComp_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},         {"2023preBPix","2023BPix"}, "M_{T}(3 #mu)", 50, 0., 200., "BPixComp_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},    {"2023preBPix","2023BPix"}, "vtx-probability(3 #mu)", 40, 0., 1., "BPixComp_Tau_Vprob");
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"}, {"2023preBPix","2023BPix"}, "cos_{#alpha}(3#mu vtx, BS)", 40, 0., 1., "BPixComp_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"}, {"2023preBPix","2023BPix"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "BPixComp_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt"    }, {"2023preBPix","2023BPix"}, " MET (GeV)", 75, 0., 150., "BPixComp_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" }, {"2023preBPix","2023BPix"}, " #phi (MET) ", 31, -3.1, 3.1, "BPixComp_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},{"2023preBPix","2023BPix"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 60, 0., 6., "BPixComp_pTratio_PuppiMET");
   draw_branches({"miss_pz_min", "miss_pz_min"},{"2023preBPix","2023BPix"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "BPixComp_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},{"2023preBPix","2023BPix"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "BPixComp_miss_pz_max");

   /// W
   draw_branches({"W_pt","W_pt"}, {"2023preBPix","2023BPix"}, "W p_{T} (GeV)", 50, 0.0, 150.0, "BPixComp_WpT_rIso0p2");
   draw_branches({"W_phi","W_phi"}, {"2023preBPix","2023BPix"}, " W #phi", 31, -3.1, 3.1, "BPixComp_Wphi");
   draw_branches({"W_eta_min","W_eta_min"}, {"2023preBPix","2023BPix"}, "W #eta(min)", 35, -3.5, 3.5, "BPixComp_Wetamin");
   draw_branches({"W_eta_max","W_eta_max"}, {"2023preBPix","2023BPix"}, "W #eta (max)", 35, -3.5, 3.5, "BPixComp_Wetamax");
   draw_branches({"W_mass_min","W_mass_min"}, {"2023preBPix","2023BPix"}, "M(W)_{min} (GeV)", 20, 70, 90, "BPixComp_Wmassmin");
   draw_branches({"W_mass_max","W_mass_max"}, {"2023preBPix","2023BPix"}, "M(W)_{max} (GeV)", 20, 70, 90, "BPixComp_Wmassmax");
  
}
