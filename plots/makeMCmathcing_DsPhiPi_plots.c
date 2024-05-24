{
   gSystem->Load("./plotter_fromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   gStyle->SetLineWidth(2);
   SetIO("../outRoot/DsPhiMuMuPi_MCanalyzer_2022_HLT_Tau3Mu.root", "DsPhiMuMuPi_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/DsPhiMuMuPi/MC_2022/");

   // muons ID
   draw_many_histos({"phi_mu1_MediumID",  "phi_mu2_MediumID"},    {"mu1", "mu2"}, "#mu medium ID", 2, -0.5,1.5, "Muons_MediumID", true);
   draw_many_histos({"phi_mu1_SoftID_PV", "phi_mu2_SoftID_PV"},   {"mu1", "mu2"}, "#mu soft ID",   2, -0.5,1.5, "Muons_SoftID_PV", true);
   draw_many_histos({"phi_mu1_TightID_PV","phi_mu2_TightID_PV"},  {"mu1", "mu2"}, "#mu tight ID",  2, -0.5,1.5, "Muons_TightID_PV", true);
   draw_many_histos({"phi_mu1_MediumID",  "phi_mu1_SoftID_PV"},   {"mu1", "mu2"}, "#mu_{1} ID",    2, -0.5,1.5, "Muon1_IDs", true);
   // muons kinematics
   draw_many_histos({"phi_mu1_pt", "phi_mu2_pt", "pi_pt"},    {"mu1", "mu2", "pi"},"p_{T}(#mu) (GeV)", 50, 0.,50., "Muons_pT");
   draw_many_histos({"phi_mu1_eta", "phi_mu2_eta", "pi_eta"}, {"mu1", "mu2", "pi"},"#eta (#mu)", 70, -3.5, 3.5, "Muons_eta");
   //draw_one_histo("tau_mu12_dZ", "mu","#Delta z(#mu_{1}, #mu_{2}) (cm)", 40, 0., 5., "tau_mu12_dZ", true);
   //draw_one_histo("tau_mu23_dZ", "mu","#Delta z(#mu_{2}, #mu_{3}) (cm)", 40, 0., 5., "tau_mu23_dZ", true);
   //draw_one_histo("tau_mu13_dZ", "mu","#Delta z(#mu_{1}, #mu_{3}) (cm)", 40, 0., 5., "tau_mu13_dZ", true);
   // phi(1020) kinematics
   draw_one_histo("phi_fit_mass", "phi_fit", "M(#mu #mu) (GeV)", 50, 0.9, 1.1, "Phi1020_fit_M");
   draw_one_histo("phi_fit_eta", "phi_fit", "#eta (3 #mu)", 70, -3.5, 3.5, "Phi1020_fit_eta");
   draw_one_histo("phi_fit_phi", "phi_fit", "#phi (3 #mu)", 62, -3.1, 3.1, "Phi1020_fit_phi");

   // Tau
   draw_one_histo("n_Ds", "Ds_fit", "#(D_{s}-> #phi(#mu #mu) #pi) candidates", 10, 0., 10., "NDs_cand", true);
   draw_one_histo("Ds_fit_mass", "Ds_fit", "M(#mu #mu #pi) (GeV)", 100, 1.6, 2.4, "Ds_fit_M");
   draw_one_histo("Ds_fit_pt", "Ds_fit", "p_{T}(#mu #mu #pi) (GeV)", 40, 10, 100, "Ds_fit_pT");
   draw_one_histo("Ds_fit_eta", "Ds_fit", "#eta (#mu #mu #pi)", 70, -3.5, 3.5, "Ds_fit_eta");
   draw_one_histo("Ds_fit_phi", "Ds_fit", "#phi (#mu #mu #pi)", 62, -3.1, 3.1, "Ds_fit_phi");
   draw_one_histo("Ds_relIso", "Ds_fit", "rel. isolation (#mu #mu #pi)", 50, 0, 0.5, "Ds_relIso", true);
   draw_one_histo("Ds_Lxy_sign_BS", "Ds_fit", "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "Ds_Lxysign");
   draw_one_histo("Ds_fit_mt", "Ds_fit", "M_{T}(#mu #mu #pi)", 50, 0., 200., "Ds_Mt");
   draw_one_histo("Ds_fit_vprob", "Ds_fit", "vtx-probability(#mu #mu #pi)", 20, 0., 1., "Ds_Vprob");
   draw_one_histo("Ds_cosAlpha_BS", "Ds_fit", "cos_{#alpha}(3#mu vtx, BS)", 100, -1., 1., "Ds_cosAlpha_BS", true);

   // Ds + MET
   draw_one_histo("tau_met_Dphi", "PuppiMET", "#Delta #phi (3 #mu, MET)", 30, 0., 6., "Dphi_PuppiMET");
   draw_one_histo("tau_met_pt", "PuppiMET", " p_{T}(MET) (GeV)", 100, 0., 300., "pT_PuppiMET");
   draw_one_histo("tau_met_ratio_pt", "PuppiMET", " p_{T}^{3 #mu}/p_{T}^{MET} ", 100, 0., 40., "pTratio_PuppiMET", true);
   draw_one_histo("miss_pz_min", "PuppiMET", " min p_{z}^{#nu} (GeV)", 100, -400., 400., "miss_pz_min");
   draw_one_histo("miss_pz_max", "PuppiMET", " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "miss_pz_max");

   // W
   draw_one_histo("W_pt", "W", "p_{T}(W) (GeV)", 100, 0., 200., "W_pt");
   
}
