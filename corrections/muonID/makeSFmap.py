import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kViridis)
import cmsstyle as CMS
CMS.SetExtraText("Preliminary")
CMS.SetLumi("")
CMS.SetEnergy("13.6")


if __name__ == "__main__":
    periods = [ '2022preEE', '2022EE', '2023preBPix', '2023BPix']
    dZ = 0.07
    for period in periods:
        file_path = "../../outRoot/WTau3Mu_MCanalyzer_"+period+"_HLT_overlap_onTau3Mu.root"
        input_file = ROOT.TFile(file_path)
        SF_map = input_file.Get("h_NUM_MediumID_DEN_TrackerMuons_"+period+"_low_val")
        SF_map.SetDirectory(0)
        SF_map.SetTitle("")
        SF_map.GetXaxis().SetTitle("|#eta(#mu)|")
        SF_map.GetXaxis().SetTitleSize(0.05)
        SF_map.GetYaxis().SetTitle("p_{T}(#mu) (GeV)")
        SF_map.GetYaxis().SetTitleSize(0.05)
        SF_map.GetYaxis().SetRangeUser(0, 30)
        SF_map.GetZaxis().SetTitle("Medium-ID SF")
        SF_map.GetZaxis().SetTitleSize(0.05)
        SF_map.GetZaxis().SetTitleOffset(1.5) 
        SF_map.GetZaxis().SetRangeUser(1.-dZ, 1.+dZ)

        text = ROOT.TLatex(0.75, 0.94, f"{period}")
        text.SetNDC()
        text.SetTextSize(0.05)
        text.SetTextFont(42)
        text.SetTextAlign(31)

        c = CMS.cmsstylec = CMS.cmsCanvas(
                canvName = 'c',
                x_min = 0, x_max = 2.4, y_min = 0, y_max = 30,
                nameXaxis = "|#eta(#mu)|", nameYaxis = "p_{T}(#mu) (GeV)",
                square=False, extraSpace=0.03,
                iPos=0,
                with_z_axis=True,
                )
        c.SetRightMargin(0.20)
        CMS.SetCMSPalette()
        CMS.cmsDraw(SF_map, 'colz', mcolor = ROOT.kWhite)
        CMS.UpdatePalettePosition(SF_map, c)
        text.Draw("same")
        c.SaveAs(f'muonID_SFmap_{period}_restyle.png')
        c.SaveAs(f'muonID_SFmap_{period}_restyle.pdf')
        continue
        c = ROOT.TCanvas(f'c_SFmap_{period}', f'SFmap_{period}', 800, 800)
        ROOT.gPad.SetLeftMargin(0.12)
        ROOT.gPad.SetRightMargin(0.20)
        ROOT.gPad.SetBottomMargin(0.12)
        SF_map.Draw("COLZ")
        
        c.SaveAs(f'muonID_SFmap_{period}.png')
        c.SaveAs(f'muonID_SFmap_{period}.pdf')