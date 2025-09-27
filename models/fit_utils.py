import ROOT
ROOT.gROOT.SetBatch(True)
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mva.config as config
from style.color_text import color_text as ct
import models.CMSStyle as CMS

 # *** RooFit Variables ***
def load_data(mass_window_lo, mass_window_hi, blind_region_lo, blind_region_hi, fit_range_lo, fit_range_hi, reduced = False):
    # tau mass
    mass = ROOT.RooRealVar('tau_fit_mass', 'm_{3#mu}'  , mass_window_lo,  mass_window_hi, 'GeV' )
    mass.setRange('left_SB', mass_window_lo, blind_region_lo)
    mass.setRange('right_SB', blind_region_hi, mass_window_hi)
    mass.setRange('fit_range', fit_range_lo,fit_range_hi)
    mass.setRange('sig_range', blind_region_lo,blind_region_hi)
    mass.setRange('full_range', mass_window_lo, mass_window_hi)

    # tau mass resolution
    eta = ROOT.RooRealVar('tau_fit_eta', '#eta_{3 #mu}'  , -4.0,  4.0)
    # BDT score
    bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
    # data weights
    weight = ROOT.RooRealVar('weight', 'weight', -np.inf, np.inf, '')
    # di-muon mass
    mu12_mass = ROOT.RooRealVar('tau_mu12_fitM', 'tau_mu12_fitM'  , -10.0,  10.0, 'GeV' )
    mu23_mass = ROOT.RooRealVar('tau_mu23_fitM', 'tau_mu23_fitM'  , -10.0,  10.0, 'GeV' )
    mu13_mass = ROOT.RooRealVar('tau_mu13_fitM', 'tau_mu13_fitM'  , -10.0,  10.0, 'GeV' )
    #displacement
    Lsign = ROOT.RooRealVar('tau_Lxy_sign_BS', 'tau_Lxy_sign_BS', 0, np.inf)
    # year/era tag
    year_id = ROOT.RooRealVar('year_id', 'year_id', 0, 500, '')
    
    if reduced:
        return [mass, eta, bdt, weight, year_id], mass
    else:
        return [mass, eta, bdt, weight, mu12_mass, mu23_mass, mu13_mass, Lsign, year_id], mass


def breakdown_efficiency(data, base_cut, full_cut, isTree = False):
    if isTree:
        nentries = data.GetEntries(base_cut)
        efficiency = data.GetEntries(full_cut)/nentries
    else:
        nentries = data.sumEntries(base_cut)
        efficiency = data.sumEntries(full_cut)/nentries
    return efficiency, nentries

def get_tree_from_file(root_file, tree_name = 'tree_w_BDT'):
    tree = ROOT.TChain(tree_name)
    tree.Add(root_file)
    return tree

def import_data_from_file(root_file, thevars, tree_name = 'tree_w_BDT', dataset_name = 'data', base_cut = '1', full_cut = '1', weight = 'weight', verbose = False):
    # import data from tree
    tree = get_tree_from_file(root_file, tree_name)
    efficiency, nentries = breakdown_efficiency(tree, base_cut, full_cut, isTree = True)
    # create RooDataSet
    data = ROOT.RooDataSet(dataset_name, dataset_name, tree, thevars, full_cut, weight)
    if verbose: 
        print(f'{ct.BOLD}==')
        data.Print()
        print(f'=={ct.END}')
        print(f' full selection      : {full_cut}')
        print(f' sel events (w)      : {data.sumEntries():.2f}')
        print(f' efficiency          : {data.numEntries()}/{nentries} = {efficiency*100:.2f}%')
        
    
    return data, efficiency, nentries

def import_data_from_tree(tree, thevars, dataset_name = 'data', base_cut = '1', full_cut = '1', weight = 'weight', verbose = False):
    # import data from tree
    efficiency, nentries = breakdown_efficiency(tree, base_cut, full_cut, isTree = True)
    # create RooDataSet
    data = ROOT.RooDataSet(dataset_name, dataset_name, tree, thevars, full_cut, weight)
    if verbose: 
        print(f'{ct.BOLD}==')
        data.Print()
        print(f'=={ct.END}')
        print(f' full selection      : {full_cut}')
        print(f' sel events (w)      : {data.sumEntries():.2f}')
        print(f' efficiency          : {data.numEntries()}/{nentries} = {efficiency*100:.2f}%')
        
    
    return data, efficiency, nentries

def get_pull(fit_var, frame, pull_range = 5.0, curve_name= '', title = 'Pull Distribution'):

    h_pull = frame.residHist('', curve_name, True) # (histo_name, curve_name, normalize, average)
    #h_pull = frame.pullHist()
    h_pull.setYAxisLimits(-pull_range, pull_range)
    
    f_pull = fit_var.frame(ROOT.RooFit.Title(title))
    f_pull.addPlotable(h_pull, 'P')
    return f_pull

def draw_fit_pull(frame_fit, frame_pull= None, fitvar = None, out_name = 'Pull Distribution', logy = False):
    # create canvas
    c = ROOT.TCanvas('c', 'c', 1024, 1024)
    c.cd()
    up_pad = ROOT.TPad("up_pad", "", 0., 0.30, 1.0,1.0) #xlow, ylow, xup, yup (mother pad reference system)
    up_pad.SetMargin(0.15, 0.1,0.0,0.1) # left, right, bottom, top
    up_pad.Draw()
    c.cd()
    ratio_pad = ROOT.TPad("ratio_pad", "", 0., 0., 1.,0.28)
    ratio_pad.SetMargin(0.15,0.1,0.4,0.0)
    ratio_pad.Draw()

    # upper pad
    up_pad.cd()
    frame_fit.Draw()
    # lower pad
    if not frame_pull:
        if not fitvar:
            print('Error: no fit variable provided')
            return False
        frame_pull = get_pull(fitvar, frame_fit, title=' ')
    frame_pull.GetYaxis().SetTitle('Pull')
    frame_pull.GetYaxis().SetTitleSize(0.1)
    frame_pull.GetYaxis().SetLabelSize(0.1)
    frame_pull.GetXaxis().SetTitle(frame_fit.GetXaxis().GetTitle())
    frame_pull.GetXaxis().SetTitleSize(0.1)
    frame_pull.GetXaxis().SetLabelSize(0.1)

    ratio_pad.cd()
    frame_pull.Draw()
    c.SaveAs(out_name+'.png')
    c.SaveAs(out_name+'.pdf')
    c.SaveAs(out_name+'.C')
    if logy:
        up_pad.SetLogy()
        c.SaveAs(out_name+'_log.png')
        c.SaveAs(out_name+'_log.pdf')
        c.SaveAs(out_name+'_log.C')
    c.Close()
    return True

def draw_full_fit(fitvar, sig_data, sig_func, data, bkg_func, nbins = 65, title = 'fit', CMSstyle = False, toMeV = True):
    
    
    frame = fitvar.frame(ROOT.RooFit.Title(title))
    # bacground model
    data.plotOn(
        frame, 
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.MarkerSize(1.),
        ROOT.RooFit.LineWidth(2),
        ROOT.RooFit.Name("data")
    )
    binwidth = (fitvar.getMax() - fitvar.getMin()) / nbins * 1000
    if toMeV : frame.GetYaxis().SetTitle(f'Events / {binwidth:.0f} MeV')
    bkg_func.plotOn(
        frame,
        ROOT.RooFit.LineColor(ROOT.kBlue),
        ROOT.RooFit.LineWidth(2),
        ROOT.RooFit.Range('full_range'),
        ROOT.RooFit.NormRange('left_SB,right_SB'),
        ROOT.RooFit.MoveToBack(),
        ROOT.RooFit.Name('bkg_func'),
    )
    # signal model(s)
    colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange, ROOT.kCyan, ROOT.kYellow]
    for i, sig in enumerate(sig_func):
        sig_data[i].plotOn(
            frame, 
            ROOT.RooFit.Binning(nbins), 
            ROOT.RooFit.DrawOption('B'), 
            ROOT.RooFit.DataError(ROOT.RooAbsData.ErrorType(2)), 
            ROOT.RooFit.XErrorSize(0), 
            ROOT.RooFit.LineWidth(2),
            ROOT.RooFit.FillColor(ROOT.kWhite),
            ROOT.RooFit.FillStyle(4000),
            #ROOT.RooFit.MoveToBack(),
        )
        sig.plotOn(
            frame,
            ROOT.RooFit.LineColor(colors[i]),
            ROOT.RooFit.Range('full_range'),
            ROOT.RooFit.NormRange('full_range'),
            ROOT.RooFit.Name(f'sig_func_{i}'),
        )
    
    return frame

def apply_cms_style(frame, outfile, cat, year, Preliminary = True, margin = 0.12, ymax = 10):
    CMS.setTDRStyle()
    x_txt = 0.50
    # LaTeX for text
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    latex.SetTextColor(ROOT.kBlack)

    #legend
    legend = ROOT.TLegend(x_txt, 0.60, 0.90, 0.80)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.SetTextFont(42)
    
    legend.AddEntry(frame.findObject('data'), 'Data', 'lep')
    legend.AddEntry(frame.findObject('bkg_func'), 'Background-only fit', 'l')
    legend.AddEntry(frame.findObject('sig_func_0'), 'W#rightarrow #tau(3#mu)#nu (Br=10^{-7})', 'l')
    legend.AddEntry(frame.findObject('sig_func_1'), 'Z#rightarrow #tau(3#mu)#tau (Br=10^{-7})', 'l')

    # frame settings
    frame.SetMaximum(ymax)
    frame.SetMinimum(1e-5)
    #frame.GetYaxis().SetTitleOffset(1.4)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.045)
    #frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)

    
    canv  = ROOT.TCanvas("c2", "c2", 800, 800)
    ROOT.gPad.SetMargin(margin,0.05,margin,0.07) # left, right, bottom, top
    frame.Draw()
    latex.DrawLatex(x_txt, 0.85, f'#bf{{V Category {cat}}}')
    CMS.setCMSLumiStyle(canv, 
                        iPosX=11, 
                        era=year, 
                        extra='Preliminary' if Preliminary else '')
    
    if legend: legend.Draw()
    ROOT.gPad.Update()        # Ensure the pad is updated
    ROOT.gPad.RedrawAxis()    # Redraw the axes on top
    canv.SaveAs(outfile + '.png')
    canv.SaveAs(outfile + '.pdf')


def add_summary_text(frame, text = '', x = 0.2, y = 0.8, size = 0.04):
    # add text to the plot
    #text = ROOT.TText(x, y, text)
    text = ROOT.TLatex(x, y, text)
    text.SetTextSize(size)
    text.SetTextFont(42)
    
    frame.addObject(text)
    return True
