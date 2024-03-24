{
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gROOT->SetBatch(true);
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   
   bool is_MC = false;
   TString HLT_DoubleMu_plus = "(tau_fit_pt > 10.0) && (tau_mu3_pt > 1.0) && (tau_mu12_fitM < 1.9 && tau_mu12_dZ < 0.7) && (tau_mu13_fitM < 1.9 && tau_mu13_dZ < 0.7) && (tau_mu23_fitM < 1.9 && tau_mu23_dZ < 0.7)";
   if(is_MC) {
      SetInputFile( {"../outRoot/WTau3Mu_MCanalyzer_2022_HLT_DoubleMu.root","../outRoot/WTau3Mu_MCanalyzer_2022_HLT_Tau3Mu.root"});
      SetInputTree( {"WTau3Mu_tree", "WTau3Mu_tree"});
      SetSelection( {"", ""});
      SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022_HLTstudies/");
   } else {
      TString data_path = "/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022/"; 
      TString selection = "((tau_fit_mass > 1.6 && tau_fit_mass < 1.72) || (tau_fit_mass > 1.84 && tau_fit_mass < 2.0))";
      SetInputFile( {data_path + "WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Fv1_HLT_DoubleMu.root", data_path + "recoKinematicsT3m_ParkingDoubleMuonLowMass_2022Fv1.root"}); 
      SetInputTree( {"WTau3Mu_tree", "Tau3Mu_HLTemul_tree"});
      //SetSelection( {selection + "&&" + HLT_DoubleMu_plus, selection});
      SetSelection( {selection , selection});
      SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/DataVsMC/2022_HLT_DoubleMu/");
   }

   // Muons
   draw_branches({"tau_mu1_TightID_PV","tau_mu1_TightID_PV"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#mu1 Tight ID (PV)", 2, -0.5, 1.5, "HLTcomp_Mu_TightID");
   draw_branches({"tau_mu1_SoftID_PV","tau_mu1_SoftID_PV"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#mu1 Tight ID (PV)", 2, -0.5, 1.5, "HLTcomp_Mu_SoftID");
   draw_branches({"tau_mu1_pt", "tau_mu1_pt"},   {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "p_{T}(#mu_{1}) (GeV)", 50, 0.,50., "HLTcomp_LeadingMuon_pT");
   draw_branches({"tau_mu2_pt", "tau_mu2_pt"},   {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "p_{T}(#mu_{2}) (GeV)", 50, 0.,50., "HLTcomp_SubleadingMuon_pT");
   draw_branches({"tau_mu3_pt", "tau_mu3_pt"},   {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "p_{T}(#mu_{3}) (GeV)", 50, 0.,50., "HLTcomp_TrailingMuon_pT");
   draw_branches({"tau_mu1_eta", "tau_mu1_eta"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#eta (#mu_{1})", 35, -3.5, 3.5, "HLTcomp_    LeadingMuon_eta");
   draw_branches({"tau_mu2_eta", "tau_mu2_eta"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#eta (#mu_{2})", 35, -3.5, 3.5, "HLTcomp_    SubleadingMuon_eta");
   draw_branches({"tau_mu3_eta", "tau_mu3_eta"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#eta (#mu_{3})", 35, -3.5, 3.5, "HLTcomp_    TrailingMuon_eta");
   draw_branches({"tau_mu12_dZ", "tau_mu12_dZ"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#Delta z(#mu_{1}, #mu_{2}) (cm)", 40, 0., 2., "HLTcomp_tau_mu12_dZ", true);
   draw_branches({"tau_mu23_dZ", "tau_mu23_dZ"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#Delta z(#mu_{2}, #mu_{3}) (cm)", 40, 0., 2., "HLTcomp_tau_mu23_dZ", true);
   draw_branches({"tau_mu13_dZ", "tau_mu13_dZ"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"},"#Delta z(#mu_{1}, #mu_{3}) (cm)", 40, 0., 2., "HLTcomp_tau_mu13_dZ", true);
   draw_branches({"tau_mu12_fitM","tau_mu12_fitM"},  {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(#mu_{1},#mu_{2}) (GeV)", 40, 0., 2.0, "HLTcomp_Mu12mass");
   draw_branches({"tau_mu13_fitM","tau_mu13_fitM"},  {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(#mu_{1},#mu_{3}) (GeV)", 40, 0., 2.0, "HLTcomp_Mu13mass");
   draw_branches({"tau_mu23_fitM","tau_mu23_fitM"},  {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(#mu_{2},#mu_{3}) (GeV)", 40, 0., 2.0, "HLTcomp_Mu23mass");
   // DR mu-tau
   TString DR_tau_mu1 = "sqrt( (tau_mu1_eta-tau_fit_eta)*(tau_mu1_eta-tau_fit_eta) + (tau_mu1_phi-tau_fit_phi)*(tau_mu1_phi-tau_fit_phi) )";
   //draw_branches({DR_tau_mu1, DR_tau_mu1},  {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#Delta R(#mu_{1},3#mu)", 30, 0.0, 0.9, "HLTcomp_DRTauMu1",true);
   
   // Tau
   draw_branches({"tau_fit_mass","tau_fit_mass"},  {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "HLTcomp_fitTauMass");
   draw_branches({"n_tau","n_tau"},                {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., "HLTcomp_Ntau_cand", true);
   draw_branches({"tau_fit_pt", "tau_fit_pt"},     {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "p_{T}(3 #mu) (GeV)", 40, 0, 80, "HLTcomp_Tau_fit_pT");
   draw_branches({"tau_fit_eta","tau_fit_eta"},    {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#eta (3 #mu)", 35, -3.5, 3.5, "HLTcomp_Tau_fit_eta");
   draw_branches({"tau_fit_phi","tau_fit_phi"},    {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#phi (3 #mu)", 31, -3.1, 3.1, "HLTcomp_Tau_fit_phi");
   draw_branches({"tau_relIso", "tau_relIso"},     {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "HLTcomp_Tau_relIso", true);
   draw_branches({"tau_relIso*tau_fit_pt", "tau_relIso*tau_fit_pt"},     {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "abs isolation (3 #mu)", 80, 0, 20.0, "HLTcomp_Tau_absIso", true);
   draw_branches({"tau_Lxy_sign_BS","tau_Lxy_sign_BS"},{"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "HLTcomp_Tau_Lxysign");
   draw_branches({"tau_fit_mt", "tau_fit_mt"},         {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M_{T}(3 #mu)", 50, 0., 200., "HLTcomp_Tau_Mt");
   draw_branches({"tau_fit_vprob","tau_fit_vprob"},    {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "vtx-probability(3 #mu)", 40, 0., 1., "HLTcomp_Tau_Vprob", true);
   draw_branches({"tau_cosAlpha_BS","tau_cosAlpha_BS"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "cos_{#alpha}(3#mu vtx, BS)", 40, 0., 1., "HLTcomp_Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_branches({"tau_met_Dphi", "tau_met_Dphi"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "HLTcomp_Dphi_PuppiMET");
   draw_branches({"tau_met_pt", "tau_met_pt"    }, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " MET (GeV)", 75, 0., 150., "HLTcomp_pT_PuppiMET");
   draw_branches({"tau_met_phi", "tau_met_phi" }, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " #phi (MET) ", 31, -3.1, 3.1, "HLTcomp_phi_PuppiMET");
   draw_branches({"tau_met_ratio_pt", "tau_met_ratio_pt"},{"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 60, 0., 6., "HLTcomp_pTratio_PuppiMET");
   draw_branches({"miss_pz_min", "miss_pz_min"},{"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "HLTcomp_miss_pz_min");
   draw_branches({"miss_pz_max", "miss_pz_max"},{"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "HLTcomp_miss_pz_max");

   // W
   draw_branches({"W_pt","W_pt"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "W p_{T} (GeV)", 50, 0.0, 150.0, "HLTcomp_WpT");
   draw_branches({"W_phi","W_phi"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, " W #phi", 31, -3.1, 3.1, "HLTcomp_Wphi");
   draw_branches({"W_eta_min","W_eta_min"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "W #eta(min)", 35, -3.5, 3.5, "HLTcomp_Wetamin");
   draw_branches({"W_eta_max","W_eta_max"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "W #eta (max)", 35, -3.5, 3.5, "HLTcomp_Wetamax");
   draw_branches({"W_mass_min","W_mass_min"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(W)_{min} (GeV)", 20, 70, 90, "HLTcomp_Wmassmin");
   draw_branches({"W_mass_max","W_mass_max"}, {"Run3_HLT_DoubleMu","Run3_HLT_Tau3Mu"}, "M(W)_{max} (GeV)", 20, 70, 90, "HLTcomp_Wmassmax");
  
}
