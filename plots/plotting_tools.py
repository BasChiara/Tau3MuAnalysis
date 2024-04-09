import ROOT

def ratio_plot( histo_num, histo_den, to_ploton = [], file_name = 'ratio_plot'):
   
    histo_num.SetTitle("") 
    histo_den.SetTitle("") 
    # ... avoid the first label (0) to be clipped.
    histo_den.GetYaxis().ChangeLabel(1, -1, -1, -1, -1, -1, " ")
    histo_den.GetYaxis().SetLabelSize(0.045)
    histo_den.GetYaxis().SetTitleFont(43)
    histo_den.GetYaxis().SetTitleOffset(1.75)
    histo_den.GetYaxis().SetTitleSize(40)
    # create ratio plot
    h_ratio = histo_num.Clone("h_ratio")
    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.Sumw2()
    h_ratio.SetStats(0)
    h_ratio.Divide(histo_den)
    h_ratio.SetMinimum(0.5)
    h_ratio.SetMaximum(1.5)
    # ratio plot style ...
    h_ratio.SetMarkerStyle(20)
    h_ratio.GetYaxis().SetTitle("Data/MC ratio")
    h_ratio.GetYaxis().ChangeLabel(1, -1, -1, -1, -1, -1, " ")
    h_ratio.GetYaxis().ChangeLabel(-1, -1, -1, -1, -1, -1, " ")
    h_ratio.GetYaxis().SetNdivisions(-504)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleSize(40)
    h_ratio.GetYaxis().SetTitleOffset(2.0)
    h_ratio.GetYaxis().SetLabelSize(0.1)
    h_ratio.GetXaxis().SetTitle(histo_den.GetXaxis().GetTitle())
    h_ratio.GetXaxis().SetLabelSize(0.1)
    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetTitleSize(40)
    h_ratio.GetXaxis().SetTitleOffset(1.5)

    c = ROOT.TCanvas("c", "", 1024, 1248)
    #create upper TPad
    c.cd()
    up_pad = ROOT.TPad("up_pad", "", 0., 0.30, 1.0,1.0) #xlow, ylow, xup, yup (mother pad reference system)
    up_pad.SetMargin(0.15, 0.1,0.0,0.1) # left, right, bottom, top 
    up_pad.Draw()
    #create lower TPad
    c.cd()
    ratio_pad = ROOT.TPad("ratio_pad", "", 0., 0., 1.,0.30)
    ratio_pad.SetMargin(0.15,0.1,0.4,0.0)
    ratio_pad.SetGridy() # vertical grid
    ratio_pad.Draw()
    
    # draw in the upper pad
    up_pad.cd()
    histo_num.SetStats(0)          # No statistics on upper plot
    histo_den.Draw("HISTE")               
    histo_num.Draw("PE0 same") 
    [obj.Draw() for obj in to_ploton]
    ratio_pad.cd()
    h_ratio.Draw("PE")
    
    c.cd()
    c.Update()
    c.SaveAs(file_name+'.png')
    c.SaveAs(file_name+'.pdf')
    return c

