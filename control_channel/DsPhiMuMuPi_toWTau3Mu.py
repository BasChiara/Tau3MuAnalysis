import ROOT
ROOT.gROOT.SetBatch(True)
import numpy as np
import pandas as pd
from array import array

import argparse

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import mva.config as config
import plots.plotting_tools as pt
from plots.color_text import color_text as ct



def get_arguments():
    parser = argparse.ArgumentParser(
        description="Script to plot DsPhiMuMuPi to WTau3Mu control channel histograms",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-i', '--input',
        type=str,
        required=True,
        help="Path to the input ROOT file containing the DsPhiMuMuPi sWeighted data.",
    )
    parser.add_argument('--plot_outdir',
        type=str,
        default='plots',
        help="Directory where the output plots will be saved.",
    )
    parser.add_argument('-y','--year',   
        type=str,
        choices=['2022', '2023'],
        default='2022'
    )
    parser.add_argument('--tag',
        type=str,
        default='',
        help="Additional tag to append to output filenames.",
    )

    
    args = parser.parse_args()
    return args

def add_overunderflow(histo):
    """
    Add overflow and underflow bins to the histogram.
    """
    histo.SetBinContent(1, histo.GetBinContent(0)+ histo.GetBinContent(1))  # underflow
    histo.SetBinContent(histo.GetNbinsX(), histo.GetBinContent(histo.GetNbinsX())+histo.GetBinContent(histo.GetNbinsX()+1))

def define_reweighting_histogram(rdf_num, rdf_den, var_settings):
    # 2D kinematic reweighting
    x_settings = var_settings['var_1']
    y_settings = var_settings['var_2']
    
    h_den = rdf_den.Histo2D(
        ('h_Ds_mc_2d', f';{x_settings["var"]};{y_settings["var"]}', len(x_settings['bins']) -1, x_settings['bins'], len(y_settings['bins'])-1, y_settings['bins']), 
        x_settings['var'], y_settings['var'], 'total_weight'
    ).GetPtr()
    h_den.Scale(1./h_den.Integral())
    h_den.Sumw2()
    # normalize to bin area
    #[h_Ds_mc_2d.SetBinContent(ix, iy, h_Ds_mc_2d.GetBinContent(ix, iy)/(h_Ds_mc_2d.GetXaxis().GetBinWidth(ix)*h_Ds_mc_2d.GetYaxis().GetBinWidth(iy))) for ix in range(1, h_Ds_mc_2d.GetNbinsX()+1) for iy in range(1, h_Ds_mc_2d.GetNbinsY()+1)]
    h_num = rdf_num.Histo2D(
        ('h_w_mc_2d', f';{x_settings["var"]};{y_settings["var"]}', len(x_settings['bins']) -1, x_settings['bins'], len(y_settings['bins'])-1, y_settings['bins']), 
        x_settings['var'], y_settings['var'], 'weight'
    ).GetPtr()
    h_num.Scale(1./h_num.Integral())
    h_num.Sumw2()
    # normalize to bin area
    #[h_w_mc_2d.SetBinContent(ix, iy, h_w_mc_2d.GetBinContent(ix, iy)/(h_w_mc_2d.GetXaxis().GetBinWidth(ix)*h_w_mc_2d.GetYaxis().GetBinWidth(iy))) for ix in range(1, h_w_mc_2d.GetNbinsX()+1) for iy in range(1, h_w_mc_2d.GetNbinsY()+1)]
    # reweighting histogram
    h_ratio = h_num.Clone('h_ratio')
    h_ratio.Divide(h_den)
    h_ratio.Sumw2()

    for i in range(1, h_ratio.GetNbinsX()+1):
        for j in range(1, h_ratio.GetNbinsY()+1):
            bin_content = h_ratio.GetBinContent(i, j)
            bin_error   = h_ratio.GetBinError(i, j)
            xi, yi = h_ratio.GetXaxis().GetBinCenter(i), h_ratio.GetYaxis().GetBinCenter(j)
            #if bin_content < 1e6 and yi>15.0 and h_den.GetBinContent(i, j) < 1e-6 :
            #    print(f'[WARNING]: bin ({i}, {j}) = ({xi:.2f}, {yi:.2f}) has zero content in reweighting histogram, setting weight to 1.0')
            #    h_ratio.SetBinContent(i, j, 1.0)
            #    h_ratio.SetBinError(i, j, 0.0)
            #if bin_content > 20.0:
            #    print(f'[WARNING]: bin ({i}, {j}) = ({xi:.2f}, {yi:.2f}) has large weight {bin_content:.2f} +/- {bin_error:.2f} in reweighting histogram, setting weight to 20.0')
                #h_ratio.SetBinContent(i, j, 20.0)
                #h_ratio.SetBinError(i, j, 0.0)

    return h_ratio

def styleHisto(h, lcolor=ROOT.kBlack, lwidth=2, lstyle=1, mcolor=ROOT.kBlack, mstyle=20, msize=1.0, normalize=False):
    if normalize:
        h.Scale(1./h.Integral())
        [h.SetBinContent(bin_idx, h.GetBinContent(bin_idx)/h.GetBinWidth(bin_idx)) for bin_idx in range(1, h.GetNbinsX()+1)]
    h.SetLineColor(lcolor)
    h.SetLineWidth(lwidth)
    h.SetLineStyle(lstyle)
    h.SetMarkerColor(mcolor)
    h.SetMarkerStyle(mstyle)
    h.SetMarkerSize(msize)
    

def apply_reweighting(h_weights, df, handles = ['tau_fit_eta', 'tau_fit_pt'], wname = 'w_byW'):

    this_df = df.copy()
    this_df[wname] = np.ones(len(this_df))
    x = handles[0]
    y = handles[1]
    for binx in range(1, h_weights.GetNbinsX() + 1):
        bin_lox = h_weights.GetXaxis().GetBinLowEdge(binx)
        bin_hix = h_weights.GetXaxis().GetBinUpEdge(binx)
        
        for biny in range(1, h_weights.GetNbinsY() + 1):
            bin_loy = h_weights.GetYaxis().GetBinLowEdge(biny)
            bin_hiy = h_weights.GetYaxis().GetBinUpEdge(biny)

            bin_weight = h_weights.GetBinContent(binx, biny)
            mask = (df[x] >= bin_lox) & (df[x] < bin_hix) & (df[y] >= bin_loy) & (df[y] < bin_hiy)
            this_df.loc[mask, wname] = bin_weight

    return this_df

if __name__ == '__main__':

    args = get_arguments()
    plot_outdir = args.plot_outdir
    tag = '_'.join([args.year, args.tag]) if args.tag != '' else args.year
    
    # -- I/O setup 
    if not os.path.exists(plot_outdir):
        os.makedirs(plot_outdir)
        os.system(f'cp ~/public/index.php {plot_outdir}')
        print(f'[+] created output directory {plot_outdir}')
    else:
        print(f'[+] output directory {plot_outdir} already exists')

    # selection of samples to plot
    base_selection = '(' + ' & '.join([
        config.year_selection[args.year],
        config.Tau_sv_selection,
    ]) + ')'
    # Ds->PhiPi MC & data 
    Ds_mc_rdf = ROOT.RDataFrame('mc_tree', args.input).Define('total_weight', 'weight*norm_factor*w_byEta').Define('tau_fit_eta_abs', 'fabs(Ds_fit_eta)').Filter(base_selection)
    if not Ds_mc_rdf:
        print(f'[ERROR]: tree not found in file {args.input}')
        sys.exit(1)
    Ds_mc_df = pd.DataFrame(Ds_mc_rdf.AsNumpy())
    Ds_sData_rdf = ROOT.RDataFrame('data_tree', args.input).Define('total_weight', 'nDs_sw').Define('tau_fit_eta_abs', 'fabs(Ds_fit_eta)').Filter(base_selection)
    Ds_sData_df = pd.DataFrame(Ds_sData_rdf.AsNumpy())
    
    if Ds_sData_rdf.Count().GetValue() == 0 or Ds_mc_rdf.Count().GetValue() == 0:
        print(f'[ERROR]: No entries found after applying base selection in data or MC!')
        sys.exit(1)

    # W->Tau(3Mu) MC
    w_mc_rdf = ROOT.RDataFrame('tree_w_BDT', config.mc_bdt_samples['WTau3Mu']).Define('tau_fit_eta_abs', 'fabs(tau_fit_eta)').Filter(base_selection)

    # -- match the kinematics of DsPhiMuMuPi to WTau3Mu
    rew_settings = {
        'var_1': {
            'var': 'tau_fit_eta_abs',
            'bins': array('d', np.linspace(0, 2.5, 26)),
            'xlabel': '|#eta|',
        },
        'var_2': {
            'var': 'tau_fit_pt',
            'bins': array('d', np.linspace(4, 30, 15).tolist() + np.linspace(35, 50, 4).tolist()+ [100]),
            'xlabel': 'p_{T} (GeV)',
        },
    }
    
    # -- REWEIGHTING
    h_mc_rew_2d         = define_reweighting_histogram(w_mc_rdf, Ds_mc_rdf, rew_settings)
    Ds_mc_df_rew        = apply_reweighting(h_mc_rew_2d, Ds_mc_df, handles=[rew_settings['var_1']['var'], rew_settings['var_2']['var']], wname='w_byW')
    
    h_sData_rew_2d      = define_reweighting_histogram(w_mc_rdf, Ds_sData_rdf, rew_settings)
    Ds_sData_df_rew     = apply_reweighting(h_sData_rew_2d, Ds_sData_df, handles=[rew_settings['var_1']['var'], rew_settings['var_2']['var']], wname='w_byW')
    
    # save reweighted dataframe to new ROOT file
    rew_output_file = os.path.join(os.path.expandvars('$EOS/Tau3MuRun3/data/control_channel/sWeight_toWtau3mu'), f'DsPhiMuMuPi_to_WTau3Mu_reweighted{tag}')
    Ds_mc_rdf_rew = ROOT.RDF.MakeNumpyDataFrame({col: Ds_mc_df_rew[col].values for col in Ds_mc_df_rew.columns}).Define('total_weight_toW', 'weight*norm_factor*w_byEta*w_byW')
    Ds_mc_rdf_rew.Snapshot('mc_tree', rew_output_file+'MC.root')
    Ds_sData_rdf_rew = ROOT.RDF.MakeNumpyDataFrame({col: Ds_sData_df_rew[col].values for col in Ds_sData_df_rew.columns}).Define('total_weight_toW', 'nDs_sw*w_byW')
    Ds_sData_rdf_rew.Snapshot('data_tree', rew_output_file+'Data.root')

    # merge MC and data files
    os.system(f'hadd -f {rew_output_file}.root {rew_output_file}MC.root {rew_output_file}Data.root')
    os.system(f'rm {rew_output_file}MC.root {rew_output_file}Data.root')
    print(f'[+] saved reweighted DsPhiMuMuPi to WTau3Mu data and MC to {rew_output_file}.root')

    # plot reweighting histogram
    canv = ROOT.TCanvas('canv_rew_2d', 'canv_rew_2d', 1200, 800)
    canv.Divide(2)
    canv.cd(1)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)
    h_mc_rew_2d.SetTitle('MC;|#eta|;p_{T}(GeV);')
    h_mc_rew_2d.GetZaxis().SetRangeUser(0.0, 50.0)
    h_mc_rew_2d.Draw('COLZ')
    canv.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)
    h_sData_rew_2d.SetTitle('sWeighted Data;|#eta|;p_{T}(GeV);')
    h_sData_rew_2d.GetZaxis().SetRangeUser(0.0, 50.0)
    h_sData_rew_2d.Draw('COLZ')
    canv.SaveAs(os.path.join(plot_outdir, f'2D_reweighting_histogram{tag}'))

    # comparison pre/post-weighting
    #Ds_mc_rdf_rew = ROOT.RDataFrame('mc_tree', rew_output_file)
    leg_coordinates_ = (0.50, 0.60, 0.9, 0.9)
    for var_key, var_cfg in rew_settings.items():
        var = var_cfg['var']
        xlabel = var_cfg['xlabel']
        # Ds MC
        h_Ds_mc_pre = Ds_mc_rdf.Histo1D((f'h_Ds_mc_preweight_{var}', f';{xlabel};Events',      len(var_cfg['bins']) -1, var_cfg['bins']), var, 'total_weight').GetPtr()
        styleHisto(h_Ds_mc_pre, lcolor=ROOT.kGreen+1, lwidth=2, normalize=True)
        h_Ds_mc     = Ds_mc_rdf_rew.Histo1D((f'h_Ds_mc_postweight_{var}', f';{xlabel};Events', len(var_cfg['bins']) -1, var_cfg['bins']), var, 'total_weight_toW').GetPtr()
        styleHisto(h_Ds_mc, lcolor=ROOT.kBlue, lwidth=2, normalize=True)
        
        # sData
        h_Ds_data_pre = Ds_sData_rdf_rew.Histo1D((f'h_Ds_data_preweight_{var}', f';{xlabel};Events', len(var_cfg['bins'])         -1, var_cfg['bins']), var, 'nDs_sw').GetPtr()
        styleHisto(h_Ds_data_pre, lcolor=ROOT.kBlack, lwidth=2, mcolor=ROOT.kBlack, mstyle=20, msize=1.0, normalize=True)
        h_Ds_data     = Ds_sData_rdf_rew.Histo1D((f'h_Ds_data_postweight_{var}', f';{xlabel};Events', len(var_cfg['bins'])        -1, var_cfg['bins']), var, 'total_weight_toW').GetPtr()
        styleHisto(h_Ds_data, lcolor=ROOT.kBlack, lwidth=2, mcolor=ROOT.kBlack, mstyle=20, msize=1.0, normalize=True)
        
        # W MC
        h_w_mc = w_mc_rdf.Histo1D((f'h_w_mc_postweight_{var}', f';{xlabel};Events', len(var_cfg['bins'])         -1, var_cfg['bins']), var, 'weight').GetPtr()
        styleHisto(h_w_mc, lcolor=ROOT.kRed, lwidth=2, normalize=True)
        

        # sPlot as cross-check pre-weighting
        pt.ratio_plot_CMSstyle(
            histo_num=[h_Ds_mc_pre, h_Ds_data_pre],
            draw_opt_num='p',
            histo_den=h_w_mc,
            ratio_yname = "D_{s}/#tau(3#mu)",
            draw_opt_den = 'histe',
            description=['D_{s}#rightarrow#phi#pi MC (pre-weight)', 'D_{s}#rightarrow#phi#pi sData', 'W#rightarrow#tau(3#mu)#nu MC'],
            file_name=os.path.join(plot_outdir, f'preweight_{var}_DsTau3Mu_{tag}'),
            x_lim = (var_cfg['bins'][0], var_cfg['bins'][-1]),
            y_lim = (0.0, 1.5 * max(h_Ds_mc_pre.GetMaximum(), h_w_mc.GetMaximum(), h_Ds_data_pre.GetMaximum())),
            leg_coords = leg_coordinates_,
            year = args.year,
        )

        # post-weighting comparisons
        pt.ratio_plot_CMSstyle(
            histo_num=[h_Ds_mc, h_Ds_data],
            draw_opt_num='histe',
            histo_den=h_w_mc,
            draw_opt_den = 'histe',
            ratio_yname = "D_{s}/#tau(3#mu)",
            description=['D_{s}#rightarrow#phi#pi MC (post-weight)', 'D_{s}#rightarrow#phi#pi Data (post-weight)','W#rightarrow#tau(3#mu)#nu MC'],
            file_name=os.path.join(plot_outdir, f'postweight_{var}_DsTau3muMC_{tag}'),
            x_lim = (var_cfg['bins'][0], var_cfg['bins'][-1]),
            y_lim = (0.0, 1.5 * max(h_Ds_mc.GetMaximum(), h_w_mc.GetMaximum(), h_Ds_data.GetMaximum())),
            leg_coords = leg_coordinates_,
            year = args.year,
        )
        
        pt.ratio_plot_CMSstyle(
            histo_num=[h_Ds_data],
            draw_opt_num='p',
            histo_den=h_Ds_mc,
            draw_opt_den = 'histe',
            description=['D_{s}#rightarrow#phi#pi sData (post-weight)', 'D_{s}#rightarrow#phi#pi MC (post-weight)'],
            file_name=os.path.join(plot_outdir, f'postweight_{var}_DsDataMC_{tag}{tag}'),
            x_lim = (var_cfg['bins'][0], var_cfg['bins'][-1]),
            y_lim = (0.0, 1.5 * max(h_Ds_data.GetMaximum(), h_Ds_mc.GetMaximum())),
            leg_coords = leg_coordinates_,
            ratio_w = 1.0
        )

    # BDT score comparison pre/post-weighting
    var = 'bdt_score'
    bins = array('d', np.linspace(0.0, 1.0, 26))
    h_Ds_mc_bdt_pre = Ds_mc_rdf.Histo1D(('h_Ds_mc_bdt_preweight', ';BDT score;Events', len(bins) -1, bins),         var, 'total_weight').GetPtr()
    styleHisto(h_Ds_mc_bdt_pre, lcolor=ROOT.kGreen+1, lwidth=2, normalize=False)
    h_Ds_mc_bdt     = Ds_mc_rdf_rew.Histo1D(('h_Ds_mc_bdt_postweight', ';BDT score;Events', len(bins) -1, bins),    var, 'total_weight_toW').GetPtr()
    styleHisto(h_Ds_mc_bdt, lcolor=ROOT.kBlue, lwidth=2, normalize=False)
    h_Ds_data_bdt_pre = Ds_sData_rdf.Histo1D(('h_Ds_data_bdt_preweight', ';BDT score;Events', len(bins) -1, bins),      var, 'nDs_sw').GetPtr()
    styleHisto(h_Ds_data_bdt_pre, lcolor=ROOT.kBlack, lwidth=2, mcolor=ROOT.kBlack, mstyle=20, msize=1.0, normalize=False)
    h_Ds_data_bdt     = Ds_sData_rdf_rew.Histo1D(('h_Ds_data_bdt_postweight', ';BDT score;Events', len(bins) -1, bins),  var, 'total_weight_toW').GetPtr()
    styleHisto(h_Ds_data_bdt, lcolor=ROOT.kBlack, lwidth=2, mcolor=ROOT.kBlack, mstyle=20, msize=1.0, normalize=False)

    pt.ratio_plot_CMSstyle(
        histo_num=[h_Ds_data_bdt_pre],
        draw_opt_num='p',
        histo_den=h_Ds_mc_bdt_pre,
        draw_opt_den = 'histe',
        description=['D_{s}#rightarrow#phi#pi sData', 'D_{s}#rightarrow#phi#pi MC (pre-weight)'],
        file_name=os.path.join(plot_outdir, f'preweight_BDTscore_DsDataMC_{tag}'),
        x_lim = (0.0, 1.0),
        ratio_w = 2.0,
        log_y = True,
        y_lim = (1e-4, 4*1e3),
        year = args.year,
    )
    pt.ratio_plot_CMSstyle(
        histo_num=[h_Ds_data_bdt],
        draw_opt_num='p',
        histo_den=h_Ds_mc_bdt,
        draw_opt_den = 'histe',
        description=['D_{s}#rightarrow#phi#pi Data (post-weight)', 'D_{s}#rightarrow#phi#pi MC (post-weight)'],
        file_name=os.path.join(plot_outdir, f'postweight_BDTscore_DsDataMC_{tag}'),
        x_lim = (0.0, 1.0),
        log_y = True,
        y_lim = (-100.0, 3.5*1e3),
        ratio_w = 2.0,
        year = args.year,
    )
    # efficiency discrepancy check
    bdt_th = 0.993
    N_sData_pre = Ds_sData_rdf.Sum('nDs_sw').GetValue()
    N_sData_BDT_pre = Ds_sData_rdf.Filter(f'bdt_score > {bdt_th}').Sum('nDs_sw').GetValue()
    N_sData_rew = Ds_sData_rdf_rew.Sum('total_weight_toW').GetValue()
    N_sData_BDT_rew = Ds_sData_rdf_rew.Filter(f'bdt_score > {bdt_th}').Sum('total_weight_toW').GetValue()
    print(f'[INFO]: Ds sWeighted data efficiency before reweighting: {N_sData_BDT_pre/N_sData_pre:.2e}')
    print(f'[INFO]: Ds sWeighted data efficiency after reweighting: {N_sData_BDT_rew/N_sData_rew:.2e}') 
    N_MC_pre  = Ds_mc_rdf.Sum('total_weight').GetValue()
    N_MC_BDT_pre = Ds_mc_rdf.Filter(f'bdt_score > {bdt_th}').Sum('total_weight').GetValue()
    N_MC_rew  = Ds_mc_rdf_rew.Sum('total_weight_toW').GetValue()
    N_MC_BDT_rew = Ds_mc_rdf_rew.Filter(f'bdt_score > {bdt_th}').Sum('total_weight_toW').GetValue()
    print(f'[INFO]: Ds MC efficiency before reweighting: {N_MC_BDT_pre/N_MC_pre:.2e}')
    print(f'[INFO]: Ds MC efficiency after reweighting: {N_MC_BDT_rew/N_MC_rew:.2e}')
    
    # check normalization of Ds data after reweighting
    print(f'[INFO]: Ds MC normalization after/before reweighting: {N_MC_rew/N_MC_pre:.2e}')
    print(f'[INFO]: Ds sWeighted data normalization after/before reweighting: {N_sData_rew/N_sData_pre:.2e}')
