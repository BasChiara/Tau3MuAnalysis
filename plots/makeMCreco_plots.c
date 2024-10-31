{
   gSystem->Load("./plotter_fromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   gStyle->SetLineWidth(2);

   //SetIO("../outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu.root", "WTau3Mu_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022preEE/");
   //SetIO("../outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onTau3Mu.root", "WTau3Mu_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022EE/");
   //SetIO("../outRoot/WTau3Mu_MCanalyzer_2023preBPix_HLT_overlap_onTau3Mu.root", "WTau3Mu_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2023preBPix/");
   SetIO("../outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onTau3Mu.root", "WTau3Mu_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2023BPix/");

   // muons ID
   draw_many_histos({"tau_mu1_MediumID", "tau_mu2_MediumID", "tau_mu3_MediumID"}, {"mu1", "mu2", "mu3"},"#mu medium ID", 2, -0.5,1.5, "Muons_MediumID", true);
   draw_many_histos({"tau_mu1_SoftID_PV", "tau_mu2_SoftID_PV", "tau_mu3_SoftID_PV"}, {"mu1", "mu2", "mu3"},"#mu soft ID", 2, -0.5,1.5, "Muons_SoftID_PV", true);
   draw_many_histos({"tau_mu1_TightID_PV", "tau_mu2_TightID_PV", "tau_mu3_TightID_PV"}, {"mu1", "mu2", "mu3"},"#mu tight ID", 2, -0.5,1.5, "Muons_TightID_PV", true);
   draw_many_histos({"tau_mu1_MediumID", "tau_mu1_SoftID_PV", "tau_mu1_TightID_PV" }, {"mu1", "mu2", "mu3"},"#mu_{1} ID", 2, -0.5,1.5, "Muon1_IDs", true);
   // muons kinematics
   draw_many_histos({"tau_mu1_pt", "tau_mu2_pt", "tau_mu3_pt"}, {"mu1", "mu2", "mu3"},"p_{T}(#mu) (GeV)", 50, 0.,50., "Muons_pT");
   draw_many_histos({"tau_mu1_eta", "tau_mu2_eta", "tau_mu3_eta"}, {"mu1", "mu2", "mu3"},"#eta (#mu)", 70, -3.5, 3.5, "Muons_eta");
   draw_one_histo("tau_mu12_dZ", "mu","#Delta z(#mu_{1}, #mu_{2}) (cm)", 40, 0., 2., "tau_mu12_dZ", true);
   draw_one_histo("tau_mu23_dZ", "mu","#Delta z(#mu_{2}, #mu_{3}) (cm)", 40, 0., 2., "tau_mu23_dZ", true);
   draw_one_histo("tau_mu13_dZ", "mu","#Delta z(#mu_{1}, #mu_{3}) (cm)", 40, 0., 2., "tau_mu13_dZ", true);

   // Tau
   draw_one_histo("n_tau", "tau_fit", "#(#tau -> 3 #mu) candidates", 10, 0., 10., "Ntau_cand", true);
   draw_one_histo("tau_fit_mass", "tau_fit", "M(3 #mu) (GeV)", 50, 1.6, 2.0, "Tau_fit_M");
   draw_one_histo("tau_fit_mass_resol", "tau_fit", "#sigma/M(3 #mu)", 50, 0.0, 0.025, "Tau_fit_resolM");
   draw_many_histos({"tau_fit_mass","tau_raw_mass"}, {"tau_fit","tau_raw"}, "M(3 #mu) (GeV)", 50, 1.6, 2.0, "Tau_prepostfit_M");
   draw_one_histo("tau_fit_pt", "tau_fit", "p_{T}(3 #mu) (GeV)", 40, 10, 100, "Tau_fit_pT");
   draw_one_histo("tau_fit_eta", "tau_fit", "#eta (3 #mu)", 70, -3.5, 3.5, "Tau_fit_eta");
   draw_one_histo("tau_fit_phi", "tau_fit", "#phi (3 #mu)", 62, -3.1, 3.1, "Tau_fit_phi");
   draw_one_histo("tau_relIso", "tau_fit", "rel. isolation (3 #mu)", 50, 0, 0.5, "Tau_relIso", true);
   draw_one_histo("tau_dimuon_mass", "tau_fit", "di-muon fit mass", 100, 0, 95., "Tau_dimuon_mass");
   draw_one_histo("tau_Lxy_sign_BS", "tau_fit", "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "Tau_Lxysign");
   draw_one_histo("tau_fit_mt", "tau_fit", "M_{T}(3 #mu)", 50, 0., 200., "Tau_Mt");
   draw_one_histo("tau_fit_vprob", "tau_fit", "vtx-probability(3 #mu)", 20, 0., 1., "Tau_Vprob");
   draw_one_histo("tau_cosAlpha_BS", "tau_fit", "cos_{#alpha}(3#mu vtx, BS)", 50, -1., 1., "Tau_cosAlpha_BS", true);

   // Tau + MET
   draw_one_histo("tau_met_Dphi", "PuppiMET", "#Delta #phi (3 #mu, MET)", 30, 0., 6., "Dphi_PuppiMET");
   draw_one_histo("tau_met_pt", "PuppiMET", " MET (GeV)", 50, 0., 100., "pT_PuppiMET");
   draw_one_histo("tau_met_ratio_pt", "PuppiMET", " p_{T}^{3 #mu}/p_{T}^{MET} ", 50, 0., 40., "pTratio_PuppiMET", true);
   draw_one_histo("miss_pz_min", "PuppiMET", " min p_{z}^{#nu} (GeV)", 100, -400., 400., "miss_pz_min");
   draw_one_histo("miss_pz_max", "PuppiMET", " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "miss_pz_max");

   // W
   draw_one_histo("W_pt", "W", "p_{T}(W) (GeV)", 100, 0., 200., "W_pt");
   
   // versus PU
   ProfileVsPU({"tau_relIso*tau_fit_pt","tau_Iso_chargedDR04", "tau_Iso_photonDR04", "tau_Iso_puDR08"}, {"Isolation", "#sum pT^{ch}(dz<0.2 cm)", "#sum pT^{#gamma}", "#sum pT^{ch}(dz>0.2 cm)"}, "# good PV","", 28, 0, 70, 0, 150, "TauIsoVsPUwPUcomponent");
   ProfileVsPU({"tau_relIso*tau_fit_pt","tau_Iso_chargedDR04", "tau_Iso_photonDR04", "tau_Iso_puDR08"}, {"Isolation", "#sum pT^{ch}(dz<0.2 cm)", "#sum pT^{#gamma}", "#sum pT^{ch}(dz>0.2 cm)"}, "# good PV","", 28, 0, 70, 0, 10, "TauIsoVsPU");
   ProfileVsPU({"tau_met_pt"},{"PuppiMET"}, "# good PV", "", 35, 0, 70, 0, 100, "PuppiMETvsPU");
   efficiencyVsPU({"tau_relIso < 0.2", "tau_relIso_pT05 < 0.2"}, {"I_{rel}", "I_{rel}(pT>0.5 GeV)"},"# PV", "efficiency", 7, 0, 70, "effTauIso02_VS_PU");
   // check on Dbeta isolation
   drawProfile2D({"tau_Iso_photonDR04", "tau_Iso_photonDR04_pT05"}, {"no pT th.", "pT > 0.5 GeV"}, {"tau_Iso_puDR08", "tau_Iso_puDR08_pT05"}, "","PU iso component", "#gamma iso component", 25, 0, 50, 0, 5, "ProfilePhotonVsPU_iso")

}
