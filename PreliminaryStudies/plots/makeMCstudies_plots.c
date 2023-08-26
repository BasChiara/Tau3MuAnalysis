{
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);

    SetInputFile("../outRoot/MCstudiesT3m_2022_preEE.root");
    SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/");

    draw_binary_histo("Mu_MediumID", "mu", "#mu mediumID", "Mu_MediumID");
    draw_binary_histo("Mu_SoftID", "mu", "#mu softID", "Mu_SoftID");
    draw_binary_histo("Mu_SoftID_BS", "mu", "#mu softID wrt BS", "Mu_SoftID_BS");
    draw_binary_histo("Mu_TightID", "mu", "#mu tightID", "Mu_TightID");
    draw_binary_histo("Mu_TightID_BS", "mu", "#mu tightID wrt BS", "Mu_TightID_BS");

    draw_many_histos({"MuLeading_pT", "MuSubLeading_pT", "MuTrailing_pT"}, 
                     {"muL", "muSL", "muT"},
                     "p_{T}(#mu) (GeV)");    

    // TAU PLOTS
    draw_two_histos("Tau_fitNoVtx_M", "Tau_wovc", "Tau_fit_M", "Tau_vc", "M(#tau}) (GeV)", "Tau_mass");
    draw_one_histo("Tau_fit_pT", "Tau_vc", "p_{T}(#tau}) (GeV)", "Tau_fitted_mass");
    draw_one_histo("Tau_relIso","Tau_vc", "rel-iso #tau");
    draw_one_histo("LxySign_BSvtx", "Tau_vc", "L_{xy}(BS;#tau-vtx)/#sigma");
    draw_one_histo("nTau", "Tau_vc", "#tau candidates per event", "nTau", true);

    // MET PLOTS
    draw_two_histos("diffGenPuppiMET", "PuppiMET", "diffGenDeepMET", "DeepMET", "genMET - recoMET (GeV)", "diffGenMET");
    draw_two_histos("diffLongGenPuppiMET", "PuppiMET", "diffLongGenDeepMET", "DeepMET", "longitudinal-recoMET - p_{T}(#nu) (GeV)", "diffLongGenMET");
    draw_two_histos("ratioLongGenPuppiMET", "PuppiMET", "ratioLongGenDeepMET", "DeepMET", "longitudinal-recoMET/p_{T}(#nu)", "ratioLongGenMET");
    draw_two_histos("ratioPerpGenPuppiMET", "PuppiMET", "ratioPerpGenDeepMET", "DeepMET", "transverse-recoMET/p_{T}(#nu)", "ratioPerpGenMET", false, true);
    


}
