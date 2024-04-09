{
   gSystem->Load("./plotter_fromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   gStyle->SetLineWidth(2);
   gStyle->SetHistMinimumZero();

   SetIO("../outRoot/WTau3Mu_MCanalyzer_2022preEE_test_HLT_DoubleMu.root", "WTau3Mu_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022_HLT_DoubleMu/");
   
   // muons ID
   draw_many_histos({"tau_mu1_MediumID",  "tau_mu2_MediumID"  , "tau_mu3_MediumID" }, {"mu1", "mu2", "mu3"}, "#mu medium ID", 2, -0.5,1.5, "Muons_MediumID", true);
   draw_many_histos({"tau_mu1_SoftID_PV", "tau_mu2_SoftID_PV" , "tau_mu3_SoftID_PV" }, {"mu1", "mu2", "mu3"}, "#mu soft ID",   2, -0.5,1.5, "Muons_SoftID_PV", true);
   draw_many_histos({"tau_mu1_TightID_PV","tau_mu2_TightID_PV", "tau_mu3_TightID_PV" }, {"mu1", "mu2", "mu3"}, "#mu tight ID",  2, -0.5,1.5, "Muons_TightID_PV", true);
   //draw_many_histos({"tau_mu1_MediumID",  "tau_mu1_SoftID_PV" , "tau_mu1_TightID_PV" }, {"mu1", "mu2", "mu3"}, "#mu_{1} ID",    2, -0.5,1.5, "Muon1_Itau", true);
   // muons kinematics
   draw_many_histos({"tau_mu1_pt", "tau_mu2_pt", "tau_mu3_pt"},    {"mu1", "mu2", "mu3"},"p_{T}(#mu) (GeV)", 50, 0.,50., "Muons_pT");
   draw_many_histos({"tau_mu1_eta", "tau_mu2_eta", "tau_mu3_eta"}, {"mu1", "mu2", "mu3"},"#eta (#mu)", 35, -3.5, 3.5, "Muons_eta");
   draw_one_histo("tau_mu12_dZ", "mu","#Delta z(#mu_{1}, #mu_{2}) (cm)", 30, 0., 3., "tau_mu12_dZ", true);
   draw_one_histo("tau_mu23_dZ", "mu","#Delta z(#mu_{2}, #mu_{3}) (cm)", 30, 0., 3., "tau_mu23_dZ", true);
   draw_one_histo("tau_mu13_dZ", "mu","#Delta z(#mu_{1}, #mu_{3}) (cm)", 30, 0., 3., "tau_mu13_dZ", true);
   draw_one_histo("tau_mu12_fitM", "mu", "M(#mu_{1} #mu_{2}) (GeV)", 50, 0.9, 1.1, "Mu1Mu2_fit_M");
   draw_one_histo("tau_mu13_fitM", "mu", "M(#mu_{1} #mu_{3}) (GeV)", 50, 0.9, 1.1, "Mu1Mu3_fit_M");
   draw_one_histo("tau_mu23_fitM", "mu", "M(#mu_{2} #mu_{3}) (GeV)", 50, 0.9, 1.1, "Mu2Mu3_fit_M");

   // Tau
   draw_one_histo("n_tau", "tau_fit", "#(#tau -> #mu #mu #mu) candidates", 10, 0., 10., "Ntau_cand", true);
   draw_one_histo("tau_fit_mass", "tau_fit", "M(#mu #mu #mu) (GeV)", 40, 1.6, 2.0, "tau_fit_M");
   draw_one_histo("tau_fit_pt", "tau_fit", "p_{T}(#mu #mu #mu) (GeV)", 40, 10, 100, "tau_fit_pT");
   draw_one_histo("tau_fit_eta", "tau_fit", "#eta (#mu #mu #mu)", 35, -3.5, 3.5, "tau_fit_eta");
   draw_one_histo("tau_fit_phi", "tau_fit", "#phi (#mu #mu #mu)", 62, -3.1, 3.1, "tau_fit_phi");
   draw_one_histo("tau_relIso", "tau_fit", "rel. isolation (#mu #mu #mu)", 50, 0, 0.5, "tau_relIso", true);
   draw_one_histo("tau_Lxy_sign_BS", "tau_fit", "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "tau_Lxysign");
   draw_one_histo("tau_fit_mt", "tau_fit", "M_{T}(#mu #mu #mu)", 50, 0., 200., "tau_Mt");
   draw_one_histo("tau_fit_vprob", "tau_fit", "vtx-probability(#mu #mu #mu)", 20, 0., 1., "tau_Vprob");
   draw_one_histo("tau_cosAlpha_BS", "tau_fit", "cos_{#alpha}(3#mu vtx, BS)", 25, -1., 1., "tau_cosAlpha_BS", true);

   // tau + MET
   draw_one_histo("tau_met_Dphi", "PuppiMET", "#Delta #phi (3 #mu, MET)", 30, 0., 6., "Dphi_PuppiMET");
   draw_many_histos({"tau_met_pt", "tau_DeepMet_pt"}, {"PuppiMET", "DeepMET"}, " MET (GeV)", 30, 0., 150., "MET");
   draw_one_histo("tau_met_ratio_pt", "PuppiMET", " p_{T}^{3 #mu}/p_{T}^{MET} ", 100, 0., 40., "pTratio_PuppiMET", true);
   draw_one_histo("miss_pz_min", "PuppiMET", " min p_{z}^{#nu} (GeV)", 100, -400., 400., "miss_pz_min");
   draw_one_histo("miss_pz_max", "PuppiMET", " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "miss_pz_max");

   // W
   draw_one_histo("W_pt", "W", "p_{T}(W) (GeV)", 50, 0., 100., "W_pt");
   // MET vs PU
   ProfileVsPU({"fabs(tau_met_pt-gen_met_pt)/gen_met_pt", "fabs(tau_DeepMet_pt-gen_met_pt)/gen_met_pt"},{"PuppiMET", "DeepMET"}, "# PV", "|MET^{reco}-MET^{gen}|/MET^{gen}", 14, 0, 70, 0, 1, "diff_GenMET_vs_PU"); 
   ProfileVsPU({"tau_met_pt", "tau_DeepMet_pt"},{"PuppiMET", "DeepMET"}, "# PV", "MET^{reco}", 14, 0, 70, 0, 100, "METreco_vs_PU"); 
   ProfileVsPU({"METlongNu/gen_met_pt"},{"PuppiMET"}, "# PV", "longMET/pT(#nu)", 14, 0, 70,   0,  3, "ratio_GenLongMET_vs_PU");
   ProfileVsPU({"METlongNu-gen_met_pt"},{"PuppiMET"}, "# PV", "longMET-pT(#nu)", 14, 0, 70, -10, 10, "diff_GenLongMET_vs_PU");


}
