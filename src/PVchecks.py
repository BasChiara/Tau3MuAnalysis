import ROOT
ROOT.gROOT.SetBatch(True)


file = "outRoot/WTau3Mu_MCanalyzer_2022preEE_HLT_overlap_onTau3Mu_PVstudies.root"
tree_name = "WTau3Mu_tree"

data = ROOT.RDataFrame(tree_name, file)
data = data.Define("dRxy_TauPV", "sqrt( (tau_gen_vx-PV_x)*(tau_gen_vx-PV_x) +(tau_gen_vy-PV_y)*(tau_gen_vy-PV_y) )").Define("dRz_TauPV", "tau_gen_vz-PV_z").Define("dR_TauPV", "sqrt(dRxy_TauPV*dRxy_TauPV + dRz_TauPV*dRz_TauPV)").Define("dRx_TauPV", "tau_gen_vx-PV_x").Define("dRy_TauPV", "tau_gen_vy-PV_y")

branches = {
    "dRxy_TauPV" : {
        "xaxis": "#sqrt{(x_{#tau}^{gen}-x_{PV})^{2} + (y_{#tau}^{gen}-y_{PV})^{2}} [cm]",
        "yaxis": "Events",
        'xmin' :0, 'xmax': 0.01,
    },
    "dRx_TauPV" : {
        "xaxis": "x_{#tau}^{gen}-x_{PV} [cm]",
        "yaxis": "Events",
        'xmin' : -0.01, 'xmax': 0.01,
    },
    "dRy_TauPV" : {
        "xaxis": "y_{#tau}^{gen}-y_{PV} [cm]",
        "yaxis": "Events",
        'xmin' : -0.01, 'xmax': 0.01,
    },
    "dRz_TauPV" : {
        "xaxis": "z_{#tau}^{gen}-z_{PV} [cm]",
        "yaxis": "Events",
        'xmin' : -0.1, 'xmax': 0.1,
    },
    "dR_TauPV" : {
        "xaxis": "#sqrt{(x_{#tau}^{gen}-x_{PV})^{2} + (y_{#tau}^{gen}-y_{PV})^{2} + (z_{#tau}^{gen}-z_{PV})^{2}} [cm]",
        "yaxis": "Events",
        'xmin' : 0, 'xmax': 5.0,
    }
}
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
for branch in branches:
    hist = data.Histo1D(( branch, "", 100, branches[branch]['xmin'], branches[branch]['xmax']), branch)
    hist.Scale(1.0 / hist.Integral())
    hist.GetXaxis().SetTitle(branches[branch]['xaxis'])
    hist.GetYaxis().SetTitle(branches[branch]['yaxis'])

    hist.SetLineColor(ROOT.kBlue)
    hist.SetLineWidth(2)

    hist.SetMaximum(1.0)

    hist.Draw("HIST")
    canvas.SetLogy()
    canvas.SaveAs(f"test/{branch}.png")
    canvas.Clear()
