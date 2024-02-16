{
   gSystem->Load("./plotter_fromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);
   gStyle->SetLineWidth(2);

   SetIO("../outRoot/MCstudiesT3m_MC_2022EE_reMini_HLT_Tau3Mu.root", "MCmatching_tree", "/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022reMini/");
   
   // MET vs PU
   ProfileVsPU({"fabs(tau_met_pt-gen_met_pt)/gen_met_pt", "fabs(tau_DeepMet_pt-gen_met_pt)/gen_met_pt"},{"PuppiMET", "DeepMET"}, "# PV", "|MET^{reco}-MET^{gen}|/MET^{gen}", 14, 0, 70, 0, 1, "diff_GenMET_vs_PU"); 
   ProfileVsPU({"tau_met_pt", "tau_DeepMet_pt"},{"PuppiMET", "DeepMET"}, "# PV", "MET^{reco}", 14, 0, 70, 0, 100, "METreco_vs_PU"); 
   ProfileVsPU({"METlongNu/gen_met_pt"},{"PuppiMET"}, "# PV", "longMET/pT(#nu)", 14, 0, 70,   0,  3, "ratio_GenLongMET_vs_PU");
   ProfileVsPU({"METlongNu-gen_met_pt"},{"PuppiMET"}, "# PV", "longMET-pT(#nu)", 14, 0, 70, -10, 10, "diff_GenLongMET_vs_PU");


}
