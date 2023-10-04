{
   // TO USE THE SCRIPT...
   // root -l -b
   // root[0] .L plots/plot_library.C++
   // root[1] .x makeMCstudies_plots.c 
   
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);

    SetInputFile_DataMC("/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/ParkingDoubleMuonLowMass_2022E.root","../outRoot/MCstudiesT3m_MC_2022.root");
    SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/DataVsMC/2022/");

    draw_DataVsMC("Mu_MediumID", "#mu mediumID", "", true, true);
    draw_DataVsMC("Mu_SoftID", "#mu softID", "", true, true);
    draw_DataVsMC("Mu_SoftID_BS", "#mu softID wrt BS", "", true, true);
    draw_DataVsMC("Mu_TightID", "#mu tightID", "", true, true);
    draw_DataVsMC("Mu_TightID_BS", "#mu tightID wrt BS", "", true, true);

    draw_DataVsMC("MuLeading_pT", "p_{T}(#mu_{1}) (GeV)");
    draw_DataVsMC("MuSubLeading_pT", "p_{T}(#mu_{2}) (GeV)");
    draw_DataVsMC("MuTrailing_pT", "p_{T}(#mu_{3}) (GeV)");
    draw_DataVsMC("MuLeading_eta", "#eta(#mu_{1}) (GeV)");
    draw_DataVsMC("MuSubLeading_eta", "#eta(#mu_{2}) (GeV)");
    draw_DataVsMC("MuTrailing_eta", "#eta(#mu_{3}) (GeV)");
    draw_DataVsMC("Mu_Dz12", "#Delta z (#mu_{1},#mu_{2}) (cm)"); 
    draw_DataVsMC("Mu_Dz23", "#Delta z (#mu_{2},#mu_{3}) (cm)"); 
    draw_DataVsMC("Mu_Dz13", "#Delta z (#mu_{1},#mu_{3}) (cm)");

    // TAU PLOTS
    draw_DataVsMC("Tau_fit_pT", "p_{T}(3#mu) (GeV)");
    draw_DataVsMC("Tau_fit_eta","#eta (3#mu)");
    draw_DataVsMC("Tau_fit_M","M(3#mu) (GeV)");
    draw_DataVsMC("Tau_Mt", "m_{T}(3#mu)", "Tau_Mt");
    draw_DataVsMC("Tau_relIso", "rel-iso 3#mu");
    draw_DataVsMC("LxySign_BSvtx", "L_{xy}(BS;3#mu-vtx)/#sigma");
    draw_DataVsMC("nTau", "3#mu candidates per event", "", true, true);
    
    draw_DataVsMC("Tau_Pvtx", "3#mu vtx probability");
    draw_DataVsMC("Tau_cosAlpha_BS", "cos_{#alpha}(3#mu vtx, BS)", "Tau_cosAlpha_BS", true, true);

    // MET PLOTS

    draw_DataVsMC("DPhi_TauPunziMET","#Delta #phi (3 #mu, MET)");
    draw_DataVsMC("TauPt_PunziMET", "p_{T}(3 #mu)/MET");
    //draw_DataVsMC("missPz_min", "min p_{z} (GeV)");
    //draw_DataVsMC("missPz_max", "max #n p_{z} (GeV)");


    draw_DataVsMC("W_pT", "p_{T}(W) (GeV)");

}
