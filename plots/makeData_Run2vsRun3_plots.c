{
   gROOT->SetBatch(true);
  
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
  
   SetInputFile( {"/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/DoubleMuonLowMass_2017E.root","/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_reMini_2024Jan04_open.root"});
   SetInputTree({"tree","tree_w_BDT"});
   SetSelection({" (mu1_refit_muonid_medium==1 && mu2_refit_muonid_medium==1 && mu3_refit_muonid_medium==1) && (HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Charge1_matched || HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_matched) && (abs(cand_refit_charge) == 1) && ((mu1_refit_pt>3.5 && abs(mu1_refit_eta)<1.2) || (mu1_refit_pt>2.0 && abs(mu1_refit_eta)<2.5 && abs(mu1_refit_eta)>1.2)) && ((mu2_refit_pt>3.5 && abs(mu2_refit_eta)<1.2) || (mu2_refit_pt>2.0 && abs(mu2_refit_eta)<2.5 && abs(mu2_refit_eta)>1.2))&&((mu3_refit_pt>3.5 && abs(mu3_refit_eta)<1.2) || (mu3_refit_pt>2.0 && abs(mu3_refit_eta)<2.5 && abs(mu3_refit_eta)>1.2)) && (mu1_refit_pt > 7 & mu2_refit_pt > 1 & mu3_refit_pt > 1) && (cand_refit_dR12 < 0.5 || cand_refit_dR13 < 0.5 || cand_refit_dR23 < 0.5)&& (cand_refit_mass12 < 1.9 || cand_refit_mass13 < 1.9 || cand_refit_mass23 < 1.9) && (cand_refit_tau_pt > 15) && (abs(cand_refit_tau_eta) < 2.5) && (cand_refit_tau_mass < 1.72 || cand_refit_tau_mass > 1.84)","(tau_fit_mass < 1.72|| tau_fit_mass> 1.84)"});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/Run2/DataRun2vsRun3reMini/");
   
   //Tau
   draw_branches({"cand_refit_tau_mass","tau_fit_mass"},  {"Run2","Run3_reMini"}, "M(3 #mu) (GeV)", 80, 1.6, 2.0, "DataRun2vsRun3_fitTauMass");
   draw_branches({"n_candidates","n_tau"},                {"Run2","Run3_reMini"}, "#(#tau -> 3 #mu) candidates", 10, 0., 10., "DataRun2vsRun3_Ntau_cand", true);
   draw_branches({"cand_refit_tau_pt", "tau_fit_pt"},     {"Run2","Run3_reMini"}, "p_{T}(3 #mu) (GeV)", 40, 10, 100, "DataRun2vsRun3_Tau_fit_pT");
   draw_branches({"cand_refit_tau_eta","tau_fit_eta"},    {"Run2","Run3_reMini"}, "#eta (3 #mu)", 70, -3.5, 3.5, "DataRun2vsRun3_Tau_fit_eta");
   draw_branches({"cand_refit_tau_phi","tau_fit_phi"},    {"Run2","Run3_reMini"}, "#phi (3 #mu)", 62, -3.1, 3.1, "DataRun2vsRun3_Tau_fit_phi");
   draw_branches({"tau_sv_ls","tau_Lxy_sign_BS"},         {"Run2","Run3_reMini"}, "L_{xy}(BS;3#mu-vtx)/#sigma", 40, 0, 30, "DataRun2vsRun3_Tau_Lxysign");
   draw_branches({"cand_refit_mttau","tau_fit_mt"},       {"Run2","Run3_reMini"}, "M_{T}(3 #mu)", 50, 0., 200., "DataRun2vsRun3_Tau_Mt");
   draw_branches({"tau_sv_prob","tau_fit_vprob"},         {"Run2","Run3_reMini"}, "vtx-probability(3 #mu)", 20, 0., 1., "DataRun2vsRun3_Tau_Vprob");
   draw_branches({"tau_sv_cos","tau_cosAlpha_BS"},        {"Run2","Run3_reMini"}, "cos_{#alpha}(3#mu vtx, BS)", 100, -1., 1., "DataRun2vsRun3_Tau_cosAlpha_BS", true);
   draw_branches({"cand_refit_tau_dBetaIsoCone0p8strength0p2_rel","tau_relIso"},     {"Run2","Run3_reMini"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "DataRun2vsRun3_Tau_relIso", true);
   draw_branches({"cand_refit_tau_dBetaIsoCone0p8strength0p2_abs","tau_relIso*tau_fit_pt"},     {"Run2","Run3_reMini"}, "abs. isolation (3 #mu)", 30, 0, 30, "DataRun2vsRun3_Tau_absIso", true);

   // Tau + MET
   //draw_branches({"fabs(cand_refit_dPhitauMET)","tau_met_Dphi", "tau_met_Dphi"}, {"Run2","Run3_prompt","Run3_reMini"}, "#Delta #phi (3 #mu, MET)", 30, 0., 6., "DataRun2vsRun3_Dphi_PuppiMET");
   draw_branches({"cand_refit_met_pt","tau_met_pt", }, {"Run2","Run3_reMini"}, " p_{T}(MET) (GeV)", 40, 0., 100., "DataRun2vsRun3_pT_PuppiMET");
   draw_branches({"cand_refit_met_phi","tau_met_phi"}, {"Run2","Run3_reMini"}, " #phi (MET) ", 62, -3.1, 3.1, "DataRun2vsRun3_phi_PuppiMET");
   draw_branches({"cand_refit_mez_1","miss_pz_min"},   {"Run2","Run3_reMini"}, " min p_{z}^{#nu} (GeV)", 100, -400., 400., "DataRun2vsRun3_miss_pz_min");
   draw_branches({"cand_refit_mez_2","miss_pz_max"},   {"Run2","Run3_reMini"}, " max p_{z}^{#nu} (GeV)", 100, -1500., 1500., "DataRun2vsRun3_miss_pz_max");
   draw_branches({"cand_refit_tau_pt/cand_refit_met_pt","tau_met_ratio_pt"},{"Run2","Run3_reMini"}, " p_{T}^{3 #mu}/p_{T}^{MET} ", 100, 0., 40., "DataRun2vsRun3_pTratio_PuppiMET", true);

   // W
   draw_branches({"cand_refit_w_pt","W_pt"}, {"Run2","Run3_reMini"}, "W p_{T} (GeV)", 50, 0.0, 150.0, "DataRun2vsRun3_WpT");
   
   // PU
   draw_branches({"n_vtx","nGoodPV"}, {"Run2","Run3_reMini"}, "number vertices", 100, 0., 100., "DataRun2vsRun3_nPVs");
   
   // check with non-ISO HLT
   SetSelection({" (mu1_refit_muonid_medium==1 && mu2_refit_muonid_medium==1 && mu3_refit_muonid_medium==1) && (HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_matched) && (abs(cand_refit_charge) == 1) && ((mu1_refit_pt>3.5 && abs(mu1_refit_eta)<1.2) || (mu1_refit_pt>2.0 && abs(mu1_refit_eta)<2.5 && abs(mu1_refit_eta)>1.2)) && ((mu2_refit_pt>3.5 && abs(mu2_refit_eta)<1.2) || (mu2_refit_pt>2.0 && abs(mu2_refit_eta)<2.5 && abs(mu2_refit_eta)>1.2))&&((mu3_refit_pt>3.5 && abs(mu3_refit_eta)<1.2) || (mu3_refit_pt>2.0 && abs(mu3_refit_eta)<2.5 && abs(mu3_refit_eta)>1.2)) && (mu1_refit_pt > 7 & mu2_refit_pt > 1 & mu3_refit_pt > 1) && (cand_refit_dR12 < 0.5 || cand_refit_dR13 < 0.5 || cand_refit_dR23 < 0.5)&& (cand_refit_mass12 < 1.9 || cand_refit_mass13 < 1.9 || cand_refit_mass23 < 1.9) && (cand_refit_tau_pt > 15) && (abs(cand_refit_tau_eta) < 2.5) && (cand_refit_tau_mass < 1.72 || cand_refit_tau_mass > 1.84)","(tau_fit_mass < 1.72|| tau_fit_mass> 1.84)"});
   
   draw_branches({"cand_refit_tau_dBetaIsoCone0p8strength0p2_rel","tau_relIso"},     {"Run2","Run3_reMini"}, "rel. isolation (3 #mu)", 50, 0, 0.5, "DataRun2vsRun3_Tau_relIsoNonIsoHLT", true);
   draw_branches({"cand_refit_tau_dBetaIsoCone0p8strength0p2_abs","tau_relIso*tau_fit_pt"},     {"Run2","Run3_reMini"}, "abs. isolation (3 #mu)", 30, 0, 30, "DataRun2vsRun3_Tau_absIsoNonIsoHLT", true);
}
