import ROOT

def ratio_plot( histo_num = [], histo_den = [], to_ploton = [], file_name = 'ratio_plot', **kwargs):

    # parse argument
    for key, value in kwargs.items():
        print(f'{key} : {value}')
    ratio_w = kwargs['ratio_w'] if 'ratio_w' in kwargs else 0.5
    ratio_yname = kwargs['ratio_yname'] if 'ratio_yname' in kwargs else 'Data/MC' 

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

    # - histo manipulations
    # remove title
    [h_num.SetTitle("") for h_num in histo_num]
    histo_den.SetTitle("")
    # ... avoid the first label (0) to be clipped.
    histo_den.GetYaxis().ChangeLabel(1, -1, -1, -1, -1, -1, " ")
    histo_den.SetMaximum(histo_den.GetMaximum())
    histo_den.GetYaxis().SetLabelSize(0.045)
    histo_den.GetYaxis().SetTitleFont(43)
    histo_den.GetYaxis().SetTitleOffset(1.75)
    histo_den.GetYaxis().SetTitleSize(40)
    # create ratio plot
    h_ratio_den  = histo_den.Clone("h_ratio_den")
    h_ratio_den.Sumw2()
    h_ratio_den.Divide(histo_den)
    h_ratio_den.SetFillColorAlpha(h_ratio_den.GetLineColor(), 0.3)
    h_ratio_den.SetStats(0)
    h_ratio_den.SetMinimum(1 - ratio_w)
    h_ratio_den.SetMaximum(1 + ratio_w)
    # ratio plot style ...
    h_ratio_den.GetYaxis().SetTitle(ratio_yname)
    h_ratio_den.GetYaxis().ChangeLabel(1, -1, -1, -1, -1, -1, " ")
    h_ratio_den.GetYaxis().ChangeLabel(-1, -1, -1, -1, -1, -1, " ")
    h_ratio_den.GetYaxis().SetNdivisions(-504)
    h_ratio_den.GetYaxis().SetTitleFont(43)
    h_ratio_den.GetYaxis().SetTitleSize(40)
    h_ratio_den.GetYaxis().SetTitleOffset(2.0)
    h_ratio_den.GetYaxis().SetLabelSize(0.1)
    h_ratio_den.GetXaxis().SetTitle(histo_den.GetXaxis().GetTitle())
    h_ratio_den.GetXaxis().SetLabelSize(0.1)
    h_ratio_den.GetXaxis().SetTitleFont(43)
    h_ratio_den.GetXaxis().SetTitleSize(40)
    h_ratio_den.GetXaxis().SetTitleOffset(1.5)

    h_ratio_list = []
    for h_num in histo_num:
        h_ratio = h_num.Clone("h_ratio")
        #h_ratio.SetLineColor(ROOT.kBlack)
        h_ratio.Sumw2()
        h_ratio.Divide(histo_den)
        h_ratio.SetMarkerStyle(20) 
        h_ratio_list.append(h_ratio)

    
    # draw in the upper pad
    up_pad.cd()
    histo_den.Draw("HISTE")               
    for h_num in histo_num:
        h_num.SetStats(0)          # No statistics on upper plot
        h_num.Draw("PE0 same") 
    [obj.Draw() for obj in to_ploton]
    # draw in the ratio pad 
    ratio_pad.cd()
    h_ratio_den.Draw("PE2")
    [h_ratio.Draw("PE same") for h_ratio in h_ratio_list]
    
    c.cd()
    c.Update()
    c.SaveAs(file_name+'.png')
    c.SaveAs(file_name+'.pdf')
    return c

