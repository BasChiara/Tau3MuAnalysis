{

   gROOT->SetBatch(true);
  
   gSystem->Load("./plotter_compareFilesFromTTree_C.so");
   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);

   SetInputFile( {"../outRoot/MCstudiesT3m_MC_2022EEreReco_HLT_Tau3Mu.root", "../outRoot/MCstudiesT3m_MC_2022_HLT_Tau3Mu.root "});
   SetOutputFile("/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2022reReco/");

  //draw_histos(vector<TString> histo_names, vector<TString> categories, const TString& x_name, TString out_name, bool logY = false, bool norm = true, bool fill = true) 
  draw_histos({"diffGenPuppiMET","diffGenPuppiMET"},{"Run3_prompt","Run3_reReco"},"genMET - recoMET (GeV)", "MC_Run3promptVSrereco_diffGenMET");
  draw_histos({"diffLongGenPuppiMET","diffLongGenPuppiMET"},{"Run3_prompt","Run3_reReco"},"longMET^{reco} - p_{T}(#nu) (GeV)", "MC_Run3promptVSrereco_diffLongGenPuppiMET");
  draw_histos({"ratioLongGenPuppiMET","ratioLongGenPuppiMET"},{"Run3_prompt","Run3_reReco"},"longMET^{reco} / p_{T}(#nu) (GeV)", "MC_Run3promptVSrereco_ratioLongGenPuppiMET");
  draw_histos({"ratioPerpGenPuppiMET","ratioPerpGenPuppiMET"},{"Run3_prompt","Run3_reReco"},"perpMET^{reco} / p_{T}(#nu) (GeV)", "MC_Run3promptVSrereco_ratioPerpGenPuppiMET");


}
