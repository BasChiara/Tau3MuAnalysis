{
    TString period = "2023BPix";
    gStyle->SetOptStat(0);
    TFile *f = new TFile("../../outRoot/WTau3Mu_MCanalyzer_"+period+"_HLT_overlap_onTau3Mu.root");
    TH2Poly *h = (TH2Poly*)f->Get("h_NUM_MediumID_DEN_TrackerMuons_"+period+"_low_val");
    h->SetTitle("");
    h->GetYaxis()->SetRangeUser(0,30);
    h->GetXaxis()->SetTitle("muon |#eta|");
    h->GetYaxis()->SetTitle("muon p_{T} (GeV)");
    h->GetZaxis()->SetTitle("SF");
    h->GetZaxis()->SetTitleOffset(1.5);
    TCanvas *c = new TCanvas("c","c",800,800);
    gPad->SetMargin(0.12, 0.15, 0.12, 0.12);
    h->Draw("colz text0");
    c->SaveAs("MuonMediumID_SFmap_"+period+".png");
    c->SaveAs("MuonMediumID_SFmap_"+period+".pdf");



}