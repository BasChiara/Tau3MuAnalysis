{
   // TO USE THE SCRIPT...
   // root -l -b
   // root[0] .L plots/plot_library.C++
   // root[1] .x makeMCstudies_plots.c 
   
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);

    SetInputFile("../outRoot/MCstudiesT3m_MC_2022.root");
    SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022/");

    draw_binary_histo("Mu_MediumID", "mu", "#mu mediumID", "Mu_MediumID");
    draw_binary_histo("Mu_SoftID", "mu", "#mu softID", "Mu_SoftID");
    draw_binary_histo("Mu_SoftID_BS", "mu", "#mu softID wrt BS", "Mu_SoftID_BS");
    draw_binary_histo("Mu_TightID", "mu", "#mu tightID", "Mu_TightID");
    draw_binary_histo("Mu_TightID_BS", "mu", "#mu tightID wrt BS", "Mu_TightID_BS");

    draw_many_histos({"MuLeading_pT", "MuSubLeading_pT", "MuTrailing_pT"}, 
                     {"muL", "muSL", "muT"},
                     "p_{T}(#mu) (GeV)", "Muons_pT", true);
    draw_many_histos({"gen_MuLeading_pT", "gen_MuSubLeading_pT", "gen_MuTrailing_pT"}, 
                     {"muL", "muSL", "muT"},
                     "p_{T}(#mu) (GeV)", "GenMuons_pT", true);                 
    draw_many_histos({"MuLeading_eta", "MuSubLeading_eta", "MuTrailing_eta"}, 
                     {"muL", "muSL", "muT"},
                     "#eta(#mu)", "Muons_eta", true);   
    draw_one_histo("Mu_Dz12", "mu", "#Delta z (#mu_{1},#mu_{2}) (cm)"); 
    draw_one_histo("Mu_Dz23", "mu", "#Delta z (#mu_{2},#mu_{3}) (cm)"); 
    draw_one_histo("Mu_Dz13", "mu", "#Delta z (#mu_{1},#mu_{3}) (cm)");

    // TAU PLOTS
    draw_two_histos("Tau_raw_M", "Tau_wovc", "Tau_fit_M", "Tau_vc", "M(3#mu) (GeV)", "Tau_mass");
    draw_one_histo("Tau_fit_MrelErr", "Tau_vc", "M(3#mu) relative resolution", "Tau_massRelErr");
    draw_two_histos("Tau_fit_pT", "Tau_vc", "gen_Tau_pT", "Tau_gen","p_{T}(3#mu) (GeV)", "Tau_pT");
    draw_two_histos("Tau_fit_eta", "Tau_vc", "gen_Tau_eta", "Tau_gen", "#eta (3#mu)", "Tau_eta");
    draw_two_histos("Tau_fit_phi", "Tau_vc", "gen_Tau_phi", "Tau_gen", "#phi (3#mu)", "Tau_phi");
    draw_one_histo("Tau_relIso","Tau_vc", "rel-iso 3#mu");
    draw_one_histo("LxySign_BSvtx", "Tau_vc", "L_{xy}(BS;3#mu-vtx)/#sigma");
    draw_one_histo("nTau", "Tau_vc", "3#mu candidates per event", "nTau", true, true);
    draw_one_histo("Tau_Mt", "Tau_vc", "m_{T}(3#mu)", "Tau_Mt");
    draw_one_histo("Tau_Pvtx", "Tau_vc", "3#mu vtx probability");
    draw_one_histo("Tau_cosAlpha_BS", "Tau_vc", "cos_{#alpha}(3#mu vtx, BS)", "Tau_cosAlpha_BS", true);

    // MET PLOTS
    draw_two_histos("diffGenPuppiMET", "PuppiMET", "diffGenDeepMET", "DeepMET", "genMET - recoMET (GeV)", "diffGenMET");
    draw_two_histos("diffLongGenPuppiMET", "PuppiMET", "diffLongGenDeepMET", "DeepMET", "longitudinal-recoMET - p_{T}(#nu) (GeV)", "diffLongGenMET");
    draw_two_histos("ratioLongGenPuppiMET", "PuppiMET", "ratioLongGenDeepMET", "DeepMET", "longitudinal-recoMET/p_{T}(#nu)", "ratioLongGenMET");
    draw_two_histos("ratioPerpGenPuppiMET", "PuppiMET", "ratioPerpGenDeepMET", "DeepMET", "transverse-recoMET/p_{T}(#nu)", "ratioPerpGenMET", false, true);
    
    draw_one_histo("DPhi_TauDeepMET", "DeepMET", "#Delta #phi (3 #mu, MET)");
    draw_one_histo("DPhi_TauPuppiMET", "PuppiMET", "#Delta #phi (3 #mu, MET)");
    draw_one_histo("TauPt_DeepMET", "DeepMET", "p_{T}(3 #mu)/MET");
    draw_one_histo("TauPt_PuppiMET", "PuppiMET", "p_{T}(3 #mu)/MET");
    draw_one_histo("missPz_min", "DeepMET", "min p_{z}^{#nu} (GeV)");
    draw_one_histo("missPz_max", "DeepMET", "max p_{z}^{#nu} (GeV)");


    draw_two_histos("W_pT", "W", "gen_W_pT", "W_gen", "p_{T}(W) (GeV)");

}
