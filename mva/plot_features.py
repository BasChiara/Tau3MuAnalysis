import ROOT
ROOT.EnableImplicitMT()
import cmsstyle as CMS
import argparse
import os
import pandas as pd

# from my config
import config as cfg


def add_overunderflow(histo):
    """
    Add overflow and underflow bins to the histogram.
    """
    histo.SetBinContent(1, histo.GetBinContent(0)+ histo.GetBinContent(1))  # underflow
    histo.SetBinContent(histo.GetNbinsX(), histo.GetBinContent(histo.GetNbinsX())+histo.GetBinContent(histo.GetNbinsX()+1))  # overflow
    #nbins = histo.GetNbinsX()
    #xlow  = histo.GetXaxis().GetXmin()
    #xhigh = histo.GetXaxis().GetXmax()
    #bin_width = (xhigh - xlow) / nbins

    ## new histogram with N+2 bins to include underflow and overflow
    #h_with_extra = ROOT.TH1F(histo.GetName()+"_extra", histo.GetTitle(), nbins + 2, xlow - bin_width, xhigh + bin_width)

    ## Fill bin contents: shift everything by 1 to make room for underflow at bin 1
    #for i in range(nbins + 2):  # bins 0 to nbins+1 in original
    #    content = histo.GetBinContent(i)
    #    error = histo.GetBinError(i)
    #    h_with_extra.SetBinContent(i + 1, content)
    #    h_with_extra.SetBinError(i + 1, error)
    
    return histo

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/features', help=' output directory for plots')
parser.add_argument('--category'   ,                                                                 help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',            default= 'app_emulateRun2',                                  help='tag to the training')
parser.add_argument('--bdt_cut',        default= 0.995, type= float,                                 help='bdt threshold')
parser.add_argument('--debug',          action = 'store_true' ,                                      help='set it to have useful printout')
parser.add_argument('--isMulticlass',   action = 'store_true',                                       help='set to use teh multiclass setting')
parser.add_argument('--LxySign_cut',    default=  0.0,  type = float,                                help='set random state for reproducible results')
parser.add_argument('-p', '--process',  choices = ['WTau3Mu', 'W3MuNu', 'DsPhiPi', 'ZTau3Mu', 'invMedID'], default = 'WTau3Mu',help='which process in the simulation')
parser.add_argument('-s', '--signal',   action = 'append',                                           help='file with signal events with BDT applied')
parser.add_argument('-d', '--data',     action = 'append',                                           help='file with data events with BDT applied')
parser.add_argument('-y', '--year',     choices= ['2022', '2023', 'Run3'],   default= '2022',                 help='data-taking year to process')

args = parser.parse_args()
tag = args.tag + '_%s'%args.year
removeNaN = False

# ------------ INPUT/OUTPUT ------------ # 
if not os.path.isdir(args.plot_outdir):
    os.makedirs(args.plot_outdir)
    os.system(f'cp ~/public/index.php {args.plot_outdir}')
    print(f'[i] created directory for output plots : {args.plot_outdir}')
else:
    print(f'[i] already existing directory for output plots : {args.plot_outdir}')

# ------------ APPLY SELECTIONS ------------ #
base_selection = ' & '.join([
    cfg.base_selection,
    cfg.phi_veto,
    cfg.year_selection[args.year],
    f' (tau_Lxy_sign_BS > {args.LxySign_cut})',

])
sig_selection  = base_selection 
#if (args.process == 'invMedID') : 
#    sig_selection = base_selection + f' & (tau_mu1_MediumID & tau_mu2_MediumID & !tau_mu3_MediumID)'
bkg_selection  = base_selection + f'& {cfg.sidebands_selection}'
if (args.process == 'W3MuNu') : 
    sig_selection = bkg_selection

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

#  ------------ PICK SIGNAL & BACKGROUND -------------- #
if(args.signal is None):
    signals     = [
        cfg.mc_bdt_samples[args.process]
    ]
else :
    signals = args.signal 
if(args.data is None):
    backgrounds  = [
        cfg.data_bdt_samples[args.process]
    ]
else :
    backgrounds = args.data 

print('[+] signal events read from \n', signals)
print('[+] data events read from \n', backgrounds)

tree_name = 'tree_w_BDT'
bdt_score = 'bdt_score' if not args.isMulticlass else 'bdt_score_t3m'

sig_rdf = ROOT.RDataFrame(tree_name, signals).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy() )
if(args.debug):print(bkg)
    
##             ##
#    PLOTTING   #
##             ##
CMS.setCMSStyle()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.1)
CMS.SetExtraText("Preliminary")
if args.year == 'Run3':
    lumitext = f'2022+2023, {cfg.LumiVal_plots[args.year]}'
else:
    lumitext = f'{args.year}, {cfg.LumiVal_plots[args.year]}'
CMS.SetLumi(lumitext)
CMS.SetEnergy(13.6)

observables = cfg.features + ['tau_fit_eta', 'tauEta', bdt_score, 'tau_fit_mass', 'tau_mu12_fitM', 'tau_mu23_fitM', 'tau_mu13_fitM']
observables = observables + ['tau_mu1_pt', 'tau_mu2_pt', 'tau_mu3_pt', 'tau_mu1_eta', 'tau_mu2_eta', 'tau_mu3_eta']
#observables = [cfg.features[0], cfg.features[1], cfg.features[2], cfg.features[3]]
no_overunderflow = ['tauEta', 'tau_mu1_TightID_PV', 'tau_mu2_TightID_PV', 'tau_mu3_TightID_PV', 'tau_mu1_MediumID', 'tau_mu2_MediumID', 'tau_mu3_MediumID', 'tau_fit_vprob', 'bdt_score']
#observables = ['tau_Lxy_sign_BS']
legend = ROOT.TLegend(0.55, 0.70, 0.90, 0.90)
legend.SetTextSize(0.04)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend_cut = ROOT.TLegend(0.40, 0.75, 0.90, 0.90)
legend_cut.SetTextSize(0.03)
legend_cut.SetBorderSize(0)
legend_cut.SetFillStyle(0)
for i,obs in enumerate(observables):
    if obs not in cfg.features_NbinsXloXhiLabelLog:
        print(f'[!] {obs} not in features_NbinsXloXhiLabelLog')
        continue
    nbins, xlo, xhi, xlabel, logscale = cfg.features_NbinsXloXhiLabelLog[obs]

    ### signal MC
    h_sig     = sig_rdf.Histo1D(('h_sig_%s'%obs, '', nbins, xlo, xhi), obs).GetPtr()
    if not (obs in no_overunderflow) : h_sig = add_overunderflow(h_sig)
    h_sig.Scale(1./h_sig.Integral())
    h_sig.GetXaxis().SetMaxDigits(3)
    ### background
    h_bkg = bkg_rdf.Histo1D(('h_bkg_%s'%obs, '', nbins, xlo, xhi), obs).GetPtr()
    if not (obs in no_overunderflow) : h_bkg = add_overunderflow(h_bkg)
    h_bkg.Scale(1./h_bkg.Integral())
    h_bkg.GetXaxis().SetMaxDigits(3)


    if(i == 0):
        legend.AddEntry(h_bkg, 'data sidebands', 'pe')
        legend.AddEntry(h_sig, f'{cfg.legend_process[args.process]}' + (' MC' if args.process != 'invMedID' else ''), 'f')
    xlo = h_sig.GetXaxis().GetXmin()
    xhi = h_sig.GetXaxis().GetXmax()
    c = CMS.cmsCanvas(f'c_{obs}', 
        xlo, xhi, 
        max(min(h_bkg.GetMinimum(),h_sig.GetMinimum()), 1e-4) if logscale else 0.0,
        1.4*max(h_bkg.GetMaximum(),h_sig.GetMaximum()) if not logscale else 5., 
        xlabel, 'Events', 
        square = CMS.kSquare, 
        extraSpace=0.02, 
        iPos=11
    ) 
    c.cd()
    c.SetLogy(logscale)
    CMS.cmsDraw(h_sig, 
        'hist',
        lwidth = 2,
        marker = 0,
        mcolor = 0,
        fcolor = cfg.color_process[args.process],
    )
    CMS.cmsDraw(h_bkg, 
        'PE same',
        lwidth = 2,
        marker = 20, 
        mcolor = ROOT.kBlack,
        fcolor = 0,
        fstyle = 0,
    )
    legend.Draw()
    ROOT.gPad.RedrawAxis()
    plot_name = os.path.join(args.plot_outdir, f'BDTinput_{obs}')
    CMS.SaveCanvas(c, plot_name+'.png', False)
    CMS.SaveCanvas(c, plot_name+'.pdf', False)
    
    if args.bdt_cut < 0.0: continue
    nbins, xlo, xhi, xlabel, logscale = cfg.features_NbinsXloXhiLabelLog[obs]
    #  after BDT selection
    sig_amplify = None
    if    args.process == 'Tau3Mu' : sig_amplify = 10.0
    elif  args.process == 'ZTau3Mu': sig_amplify = 20.0
    
    h_sig_cut = sig_rdf.Filter('%s>%f'%( bdt_score, args.bdt_cut)).Histo1D(('h_sig_%s'%obs, '', nbins, xlo, xhi), obs, 'weight').GetPtr()
    if not (obs in no_overunderflow) : h_sig_cut = add_overunderflow(h_sig_cut)
    if sig_amplify : h_sig_cut.Scale(sig_amplify)
    
    h_bkg_cut = bkg_rdf.Filter('%s>%f'%( bdt_score, args.bdt_cut)).Histo1D(('h_bkg_%s'%obs, '', nbins, xlo, xhi), obs).GetPtr()
    if not (obs in no_overunderflow) : h_bkg_cut = add_overunderflow(h_bkg_cut)
    
    if i ==0:
        legend_cut.AddEntry(h_bkg_cut, 'data sidebands', 'pe')
        legend_cut.AddEntry(h_sig_cut, f'{cfg.legend_process[args.process]}' + (' MC' if args.process != 'invMedID' else '') + (f' #times {sig_amplify:.1f} ' if sig_amplify else '') +  f'(BDT>{args.bdt_cut:.3f})', 'f') 
    
    c_cut = CMS.cmsCanvas(f'c_cut_{obs}', 
        xlo, xhi,
        max(min(h_bkg.GetMinimum(),h_sig.GetMinimum()), 1e-4) if logscale else 0.0,
        1.4*max(h_bkg_cut.GetMaximum(),h_sig_cut.GetMaximum()), 
        xlabel, 
        'Events', 
        square = CMS.kSquare, 
        extraSpace=0.02, 
        iPos=11
    ) 
    c_cut.cd()
    CMS.cmsDraw(h_sig_cut, 
        'hist',
        lwidth = 2,
        marker = 0,
        mcolor = 0,
        fcolor = cfg.color_process[args.process],
    )
    CMS.cmsDraw(h_bkg_cut, 
        'PE same',
        lwidth = 2,
        marker = 20, 
        mcolor = ROOT.kBlack,
        fcolor = 0,
        fstyle = 0,
    )
    c_cut.SetLogy(logscale)
    legend_cut.Draw()
    ROOT.gPad.RedrawAxis()
    plot_name = os.path.join(args.plot_outdir, os.path.basename(plot_name).replace('BDTinput', 'BDTinput_cut'))
    #plot_name = plot_name.replace('input', 'cut'+str(args.bdt_cut).replace('.', 'p'))
    CMS.SaveCanvas(c_cut, plot_name+'.png', False)
    CMS.SaveCanvas(c_cut, plot_name+'.pdf', False)

