import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import cmsstyle as CMS

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import mva.config as cfg

def drawCMSstyle(observable, histo_list, colors, names, output, y_max=None, additional_text=None, name_tag= None):
    if len(histo_list) != len(colors):
        raise ValueError("Number of histograms and colors must match.")
        return
    if not isinstance(histo_list, list):
        raise TypeError("histo_list must be a list of ROOT histograms.")
        return
    CMS.ResetAdditionalInfo()
    if additional_text:
        CMS.AppendAdditionalInfo(additional_text)
    minima = min([h.GetMinimum() for h in histo_list])
    SETLOGY = cfg.features_NbinsXloXhiLabelLog[observable][4]
    c = CMS.cmsCanvas(f'c_{observable}', 
        x_min = cfg.features_NbinsXloXhiLabelLog[observable][1], 
        x_max = cfg.features_NbinsXloXhiLabelLog[observable][2], 
        y_min = max( minima, 1e-4) if SETLOGY else 0.0,
        y_max = 1.4*max([h.GetMaximum() for h in histo_list]) if not y_max else y_max,
        nameXaxis = cfg.features_NbinsXloXhiLabelLog[observable][3], 
        nameYaxis = 'Events', 
        square = CMS.kSquare, 
        extraSpace=0.02, 
        iPos=11
    ) 
    c.cd()
    c.SetLogy(cfg.features_NbinsXloXhiLabelLog[observable][4])
    for i, h in enumerate(histo_list):
        if i == 0:
            CMS.cmsDraw(h, 
                'pe',
                lwidth = 2,
                lcolor = colors[i],
                marker = 20,
                mcolor = colors[i],
                fcolor = colors[i],
            )
        else:
            CMS.cmsDraw(h, 
                'PE same',
                lwidth = 2,
                lcolor = colors[i],
                marker = 20,
                mcolor = colors[i],
                fcolor = 0,
                fstyle = 0,
            )
    legend = ROOT.TLegend(0.55, 0.70, 0.90, 0.90)
    legend.SetTextSize(0.04)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    for i, h in enumerate(histo_list):
        legend.AddEntry(h, f'{names[i]}', 'pe')
    if len(legend.GetListOfPrimitives()) > 0:
        legend.Draw()
    ROOT.gPad.RedrawAxis()
    plot_name = os.path.join(output, f'{observable}'+(f'_{name_tag}' if name_tag else ''))
    CMS.SaveCanvas(c, plot_name+'.png', False)


# ---- INPUT SAMPLES ---- #
data_file = cfg.data_bdt_samples['WTau3Mu']
#invID_file  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples//XGBout_invMedIDandSideBands_DATA_2022_invID-mu3_reweight.root'
invID_file  = '/eos/user/c/cbasile/Tau3MuRun3/data/bkg_samples/XGBout_invMedIDandSideBands_DATA_2022_invID-mu3_nT15k_invIDopen_reweight.root'
if not os.path.exists(invID_file):
    raise FileNotFoundError(f"Proxy sample not found: {invID_file}")
if not os.path.exists(data_file):
    raise FileNotFoundError(f"Target sample not found: {data_file}")

# ---- OUTPUT ---- #
output_dir = os.path.join(
    os.path.expandvars('$WWW'),
    'Tau3Mu_Run3/BDTtraining/features/invertedID-mu3/reweight',
)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"[i] created directory for output plots : {output_dir}")
else:
    print(f"[i] already existing directory for output plots : {output_dir}")

# ---- SELECTION ---- #
base_selection = '&'.join([
    cfg.base_selection,
    cfg.displacement_selection,
    #cfg.sidebands_selection,
    cfg.year_selection['2022'], #FIXME: 2022 only to try
])
CMS.SetLumi(f'2022, {cfg.LumiVal_plots["2022"]}')
CMS.SetEnergy(13.6)

# ---- LOAD DATA ---- #
treename = 'tree_w_BDT'
#data_rdf = ROOT.RDataFrame(treename, data_file).Filter(base_selection)
data_rdf = ROOT.RDataFrame(treename, invID_file).Filter(base_selection).Filter('is_dataSB == 1').Define('w_invID', 'p_data/(1-p_data)') # weight for data sidebands
invID_rdf = ROOT.RDataFrame(treename, invID_file).Filter(base_selection).Filter('is_dataSB == 0').Define('w_invID', 'p_data/(1-p_data)') # weight for inverted ID sidebands



observables = cfg.features + ['tau_fit_eta', 'tauEta', 'bdt_score', 'tau_fit_mass']
observables = []
#, 'tau_mu12_fitM', 'tau_mu23_fitM', 'tau_mu13_fitM']
#observables = observables + ['tau_mu1_pt', 'tau_mu2_pt', 'tau_mu3_pt', 'tau_mu1_eta', 'tau_mu2_eta', 'tau_mu3_eta']
#observables = ['bdt_score', 'tau_fit_eta']
legend = ROOT.TLegend(0.55, 0.70, 0.90, 0.90)
legend.SetTextSize(0.04)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
for i,obs in enumerate(observables):
    # --- data sidebands
    h_data     = data_rdf.Histo1D(('h_data_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
    h_data.Scale(1./h_data.Integral())
    
    # --- inverted ID sidebands
    h_invID     = invID_rdf.Histo1D(('h_invID_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
    h_invID.Scale(1./h_invID.Integral())

    # --- inverted ID sidebands weighted
    h_invID_w   = invID_rdf.Histo1D(('h_invID_w_%s'%obs, '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs, 'w_invID').GetPtr()
    h_invID_w.Scale(1./h_invID_w.Integral())

    drawCMSstyle(
        obs, 
        [h_data, h_invID, h_invID_w], 
        [ROOT.kBlack, ROOT.kOrange+1 ,ROOT.kRed], 
        ['data sidebands', 'inv-ID', 'inv-ID (weighted)'],
        output_dir,
    )

    # --- Ratio histograms
    h_invID_ratio = h_invID.Clone(f'h_invID_ratio_{obs}')
    h_invID_ratio.Divide(h_data)

    h_invID_w_ratio = h_invID_w.Clone(f'h_invID_w_ratio_{obs}')
    h_invID_w_ratio.Divide(h_data)
  
    c_ratio = CMS.cmsDiCanvas(f'c_ratio_{obs}',                           
        x_min=cfg.features_NbinsXloXhiLabelLog[obs][1], 
        x_max=cfg.features_NbinsXloXhiLabelLog[obs][2], 
        y_min=max(min(h_data.GetMinimum(),h_invID.GetMinimum()), 1e-4) if cfg.features_NbinsXloXhiLabelLog[obs][4] else 0.0,
        y_max=1.4*max(h_data.GetMaximum(),h_invID.GetMaximum()), 
        nameXaxis=cfg.features_NbinsXloXhiLabelLog[obs][3],
        nameYaxis='Events',
        r_min = 0.5,
        r_max = 1.5,
        nameRatio = 'inv-ID/data SB',
        square=True,
        iPos=11,
        extraSpace=0,
        scaleLumi=1,
    )
    c_ratio.cd(1)
    CMS.cmsDraw(h_data, 
        'pe',
        lwidth = 2,
        lcolor = ROOT.kBlack,
        marker = 20,
        mcolor = ROOT.kBlack,
        fcolor = ROOT.kBlack,
    )
    CMS.cmsDraw(h_invID, 
        'PE same',
        lwidth = 2,
        lcolor = ROOT.kOrange+1,
        marker = 20, 
        mcolor = ROOT.kOrange+1,
        fcolor = 0,
        fstyle = 0,
    )
    CMS.cmsDraw(h_invID_w, 
        'PE same',
        lwidth = 2,
        lcolor = ROOT.kRed,
        marker = 21, 
        mcolor = ROOT.kRed,
        fcolor = 0,
        fstyle = 0,
    )
    legend.Draw()
    ROOT.gPad.RedrawAxis()
    c_ratio.cd(2)
    CMS.cmsDraw(h_invID_ratio, 
        'PE',
        lwidth = 2,
        lcolor = ROOT.kOrange+1,
        marker = 20, 
        mcolor = ROOT.kOrange+1,
        fcolor = ROOT.kOrange+1,
    )
    CMS.cmsDraw(h_invID_w_ratio, 
        'PE same',
        lwidth = 2,
        lcolor = ROOT.kRed,
        marker = 21, 
        mcolor = ROOT.kRed,
        fcolor = ROOT.kRed,
    )
    ref_line = ROOT.TLine(cfg.features_NbinsXloXhiLabelLog[obs][1], 1.0, cfg.features_NbinsXloXhiLabelLog[obs][2], 1.0)
    CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lwidth=2, lstyle=ROOT.kDotted)
    CMS.SaveCanvas(c_ratio, os.path.join(output_dir, f'{obs}_ratio')+'.png', False)

# post BDT only for mass
var = 'tau_fit_mass'
# -- bdt-cut
bdt_cut = 0.900
bdt_cut_list = [0.500, 0.700, 0.900, 0.950, 0.975, 0.990, 0.995]
for bdt_cut in bdt_cut_list:
    selection = '&'.join([
        '(bdt_score > %f)' % bdt_cut,
        cfg.phi_veto,
    ])
    data_rdf_bdt  = data_rdf.Filter(selection)
    invID_rdf_bdt = invID_rdf.Filter(selection)

    h_data_bdt  = data_rdf_bdt.Histo1D(('h_data_bdt', '', cfg.features_NbinsXloXhiLabelLog[var][0], cfg.features_NbinsXloXhiLabelLog[var][1], cfg.features_NbinsXloXhiLabelLog[var][2]), var).GetPtr()
    h_invID_bdt  = invID_rdf_bdt.Histo1D(('h_invID_bdt', '', cfg.features_NbinsXloXhiLabelLog[var][0], cfg.features_NbinsXloXhiLabelLog[var][1], cfg.features_NbinsXloXhiLabelLog[var][2]), var).GetPtr()
    h_invID_w_bdt = invID_rdf_bdt.Histo1D(('h_invID_bdt', '', cfg.features_NbinsXloXhiLabelLog[var][0], cfg.features_NbinsXloXhiLabelLog[var][1], cfg.features_NbinsXloXhiLabelLog[var][2]), var, 'w_invID').GetPtr()

    drawCMSstyle(
        var, 
        [h_data_bdt, h_invID_bdt, h_invID_w_bdt], 
        [ROOT.kBlack, ROOT.kOrange+1 ,ROOT.kRed], 
        ['data sidebands', 'inv-ID', 'inv-ID (weighted)'],
        output_dir,
        #y_max = 50,
        additional_text = 'BDT > %.3f' % bdt_cut,
        name_tag = 'BDT'+str(bdt_cut).replace('.', 'p'), 
    )

