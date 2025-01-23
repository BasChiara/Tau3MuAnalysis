import ROOT 

in_wspace_file = "input_combine/wspace_bdt0.9970_WTau3Mu_A22_apply_LxyS2.0_pTVreweight_expo.root"
wspace_name = "wspace_WTau3Mu_A22_apply_LxyS2.0_pTVreweight_expo_bdt0.9970"

f = ROOT.TFile.Open(in_wspace_file)
w = f.Get(wspace_name)
w.Print()

x = w.var("tau_fit_mass")
x.setBins(65)
data_asimov = w.data("data_obs")
data_fit = w.data("data_fit")

print(f' - Asimov: {data_asimov.numEntries()} ({data_asimov.sumEntries()})')
print(f' - Fit: {data_fit.numEntries()} ({data_fit.sumEntries()})')

bkg_model = w.pdf("model_bkg_WTau3Mu_A22")

frame = x.frame()
plot_asimov = data_asimov.plotOn(frame,
                   ROOT.RooFit.MarkerColor(ROOT.kRed),
                   ROOT.RooFit.LineColor(ROOT.kRed),
                   ROOT.RooFit.Name("plot_asimov"),
)
plot_fit = data_fit.plotOn(frame,
                ROOT.RooFit.MarkerColor(ROOT.kBlack),
                ROOT.RooFit.LineColor(ROOT.kBlack),
                ROOT.RooFit.Name("plot_fit"),
)
bkg_fit = bkg_model.plotOn(frame, 
                           ROOT.RooFit.LineColor(ROOT.kBlue),
                           ROOT.RooFit.Name("bkg_fit"),
)

frame.Draw()
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry('plot_asimov', "Asimov", "pe")
legend.AddEntry('plot_fit', "Data sidebands", "pe")
legend.AddEntry('bkg_fit', "Fit sidebands", "l")


c = ROOT.TCanvas("c", "c", 800, 600)

frame.SetTitle("M(3#mu) (GeV)")
frame.SetXTitle("tau_fit_mass")
frame.SetYTitle("Events")
frame.SetMinimum(1e-5)
frame.SetTitleOffset(1.2, "Y")
frame.SetTitleOffset(1.2, "X")
frame.SetTitleSize(0.04, "Y")
frame.SetTitleSize(0.04, "X")
frame.Draw()
legend.Draw()

c.SaveAs("plots/test.png")
