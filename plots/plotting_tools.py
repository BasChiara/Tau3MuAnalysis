import ROOT
import cmsstyle as CMS
CMS.SetEnergy(13.6)

import numpy as np
# custom configuration
import sys
sys.path.append('..')
from mva.config import LumiVal_plots

def ratio_plot( histo_num = [], histo_den = [], to_ploton = [], file_name = 'ratio_plot', **kwargs):

    # parse argument
    ratio_w         = kwargs['ratio_w'] if 'ratio_w' in kwargs else 0.5
    ratio_yname     = kwargs['ratio_yname'] if 'ratio_yname' in kwargs else 'Data/MC' 
    x_lim           = kwargs['x_lim'] if 'x_lim' in kwargs else [histo_den.GetBinLowEdge(histo_den.FindFirstBinAbove(0.)), histo_den.GetBinLowEdge(histo_den.FindLastBinAbove(0.)+1)] 
    y_lim           = kwargs['y_lim'] if 'y_lim' in kwargs else [histo_den.GetMinimum(), 1.3*histo_den.GetMaximum()]
    draw_opt_num    = kwargs['draw_opt_num'] if 'draw_opt_num' in kwargs else 'histe'
    draw_opt_den    = kwargs['draw_opt_den'] if 'draw_opt_den' in kwargs else 'PE0'
    log_y           = kwargs['log_y'] if 'log_y' in kwargs else False
    log_x           = kwargs['log_x'] if 'log_x' in kwargs else False
    
    
    c = ROOT.TCanvas("c", "", 1024, 1248)

    #create upper TPad
    c.cd()
    up_pad = ROOT.TPad("up_pad", "", 0., 0.30, 1.0,1.0) #xlow, ylow, xup, yup (mother pad reference system)
    up_pad.SetMargin(0.15, 0.1,0.0,0.1) # left, right, bottom, top
    if log_x: up_pad.SetLogx()
    if log_y: up_pad.SetLogy()
    up_pad.SetGridy() # vertical grid 
    up_pad.Draw()
    #create lower TPad
    c.cd()
    ratio_pad = ROOT.TPad("ratio_pad", "", 0., 0., 1.,0.30)
    ratio_pad.SetMargin(0.15,0.1,0.4,0.0)
    ratio_pad.SetGridy() # vertical grid
    if log_x: ratio_pad.SetLogx()
    ratio_pad.Draw()

    # - histo manipulations
    # remove title
    [h_num.SetTitle("") for h_num in histo_num]
    histo_den.SetTitle("")
    # ... avoid the first label (0) to be clipped.
    #histo_den.GetYaxis().ChangeLabel(1, -1, -1, -1, -1, -1, " ") 
    histo_den.GetYaxis().SetLabelSize(0.045)
    histo_den.GetYaxis().SetTitleFont(43)
    histo_den.GetYaxis().SetTitleOffset(1.75)
    histo_den.GetYaxis().SetTitleSize(40)
    histo_den.GetXaxis().SetRangeUser(x_lim[0], x_lim[1])
    histo_den.GetYaxis().SetRangeUser(y_lim[0], y_lim[1])
    # create ratio plot
    h_ratio_den  = histo_den.Clone("h_ratio_den")
    h_ratio_den.Sumw2()
    h_ratio_den.Divide(histo_den)
    h_ratio_den.SetFillColorAlpha(h_ratio_den.GetLineColor(), 0.3)
    h_ratio_den.SetStats(0)
    h_ratio_den.GetYaxis().SetRangeUser(np.max([1 - ratio_w, 0]), 1 + ratio_w)
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
    h_ratio_den.GetXaxis().SetRangeUser(x_lim[0], x_lim[1])

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
    histo_den.Draw(draw_opt_den)               
    for h_num in histo_num:
        h_num.SetStats(0)          # No statistics on upper plot
        h_num.Draw(draw_opt_num+"same") 
    [obj.Draw() for obj in to_ploton]
    # draw in the ratio pad 
    ratio_pad.cd()
    h_ratio_den.Draw("PE2")
    [h_ratio.Draw("PE same") for h_ratio in h_ratio_list]
    
    
    c.cd()
    c.SaveAs(file_name+'.png')
    c.SaveAs(file_name+'.pdf')
    return c

def ratio_plot_CMSstyle(histo_num = [], histo_den = [], to_ploton = [], file_name = 'ratio_plot', **kwargs):
    # parse argument
    #for key, value in kwargs.items():
    #    print(f'{key} : {value}')
    ratio_w      = kwargs['ratio_w'] if 'ratio_w' in kwargs else 0.5
    ratio_yname  = kwargs['ratio_yname'] if 'ratio_yname' in kwargs else 'Data/MC'
    draw_opt_num = kwargs['draw_opt_num'] if 'draw_opt_num' in kwargs else 'hist'
    draw_opt_den = kwargs['draw_opt_den'] if 'draw_opt_den' in kwargs else 'hist'
    CMSextraText = kwargs['CMSextraText'] if 'CMSextraText' in kwargs else 'Preliminary'
    isMC         = kwargs['isMC'] if 'isMC' in kwargs else False
    year         = kwargs['year'] if 'year' in kwargs else 2022
    x_lim        = kwargs['x_lim'] if 'x_lim' in kwargs else [histo_den.GetBinLowEdge(histo_den.FindFirstBinAbove(0.)), histo_den.GetBinLowEdge(histo_den.FindLastBinAbove(0.)+1)] 
    y_lim        = kwargs['y_lim'] if 'y_lim' in kwargs else [histo_den.GetMinimum(), 1.3*histo_den.GetMaximum()]
    log_y        = kwargs['log_y'] if 'log_y' in kwargs else False
    
    # CMS style setting
    if isMC :
        CMS.SetLumi('')
        CMSextraText = 'Simulation ' + CMSextraText
    else: CMS.SetLumi(LumiVal_plots[str(year)])
    CMS.SetExtraText(CMSextraText)
    CMS.SetEnergy(13.6)

    
    # CMS style canva
    x_min = x_lim[0]
    x_max = x_lim[1]
    y_min = y_lim[0]
    y_max = y_lim[1]
    r_min = np.max([0.0, 1 - ratio_w])
    r_max = 1 + ratio_w
    #c = ROOT.TCanvas("c", "", 1024, 1248)
    c = CMS.cmsDiCanvas('c', 
                    x_min, 
                    x_max, 
                    y_min, 
                    y_max,
                    r_min,
                    r_max,
                    histo_den.GetXaxis().GetTitle(),
                    histo_den.GetYaxis().GetTitle(),
                    ratio_yname,
                    square = CMS.kSquare, 
                    extraSpace=0, 
                    iPos=11
    ) 
    
    # - histo manipulations
    # remove title
    [h_num.SetTitle("") for h_num in histo_num]
    histo_den.SetTitle("")
    # create ratio plot
    h_ratio_den  = histo_den.Clone("h_ratio_den")
    h_ratio_den.Sumw2()
    h_ratio_den.Divide(histo_den)
    h_ratio_den.SetFillColorAlpha(h_ratio_den.GetLineColor(), 0.3)
    h_ratio_den.SetMarkerStyle(0)
    # ratio plot style ...
    

    h_ratio_list = []
    for h_num in histo_num:
        h_ratio = h_num.Clone("h_ratio")
        h_ratio.Sumw2()
        h_ratio.Divide(histo_den)
        h_ratio.SetMarkerStyle(20) 
        h_ratio_list.append(h_ratio)

    
    # draw in the upper pad
    c.cd(1)
    #histo_den.Draw("HISTE")
    CMS.cmsDraw(histo_den,
        f'{draw_opt_den}',
        lwidth = histo_den.GetLineWidth(), 
        mcolor = histo_den.GetLineColor(),
        marker = histo_den.GetMarkerStyle(),
        fcolor = histo_den.GetFillColor(),
        fstyle = histo_den.GetFillStyle(),
    )           
    for h_num in histo_num:
        h_num.SetStats(0)          # No statistics on upper plot
        CMS.cmsDraw(h_num, 
        f'{draw_opt_num} same',
        lwidth = h_num.GetLineWidth(), 
        mcolor = h_num.GetLineColor(), 
        marker = h_num.GetMarkerStyle(),
        fcolor = h_num.GetFillColor(),
        fstyle = h_num.GetFillStyle(),
        ) 
    [obj.Draw() for obj in to_ploton]
    c.SetLogy(log_y)
    CMS.fixOverlay()
    # draw in the ratio pad 
    c.cd(2)
    CMS.cmsDraw(h_ratio_den, 
    'E2',
    marker = 0,
    lwidth = h_ratio_den.GetLineWidth(),
    mcolor = h_ratio_den.GetLineColor(), 
    fcolor = h_ratio_den.GetFillColor(),
    )
    [CMS.cmsDraw(h_ratio, f'{draw_opt_num} same', lwidth = h_ratio.GetLineWidth(),mcolor = h_ratio.GetLineColor(), fcolor = h_ratio.GetFillColor(), ) for h_ratio in h_ratio_list]
    c.cd()
    c.SaveAs(file_name + '.png')
    c.SaveAs(file_name + '.pdf')
    c.SaveAs(file_name + '.root')

    c.Close()
    return 1