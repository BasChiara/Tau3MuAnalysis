import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetHistMinimumZero()
import cmsstyle as CMS
CMS.setCMSStyle()
CMS.SetEnergy(13.6)

import argparse

import numpy as np
import pandas as pd
import array as array 

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import style.color_text as ct
import plots.plotting_tools as plt
import mva.config as config

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate BDT selection efficiency.')
    parser.add_argument('--input',  required=True, 
                        help='Input ROOT file with sWeighted data.')
    parser.add_argument('--bdt_cut', type=float,
                        default=0., help='BDT cut value for selection.')
    parser.add_argument('--method', type=str,
                        choices=['ratio', 'difference', 'reldiff', 'pull'],
                        default='ratio', help='Comparison method: ratio, difference, reldiff, pull.')
    parser.add_argument('--year', type=int,
                        default=2022, help='Data taking year.')
    parser.add_argument('--output', required=True, help='Output ROOT file to save efficiency histogram.')
    return parser.parse_args()

def get_binning(rdf, handle = 'bdt_score', weight= 'total_weight', xlo = 0, xhi = 1, threshold = 0.993):
    """Get the binning for <handle> as every bin has the same stat as <handle> > <threshold>"""
    if not rdf :
        ct.print_error("RDataFrame is None!")
        return None
    elif not(rdf.HasColumn(handle) or rdf.HasColumn(weight)):
        ct.print_error(f"RDataFrame has no column named {handle}!")
        return None
    binning = [threshold, xhi]   
    nevents = rdf.Filter(f'{handle} > {threshold}').Sum(weight).GetValue()
    print(f"Number of events with {handle} > {threshold} : {nevents:.1f}")
    
    # get the remaining events below threshold
    df = pd.DataFrame(rdf.Filter(f'{handle} <= {threshold}').AsNumpy(columns=[handle, weight]))
    df.sort_values(by=handle, ascending=False, inplace=True, ignore_index=True)
    #print(df.head())
    sumevents = 0.0
    for index, row in df.iterrows():
        sumevents += row[weight]
        if sumevents >= nevents:
            bin_edge = np.round(row[handle], 6) 
            binning.insert(0, bin_edge)
            sumevents = 0.0
    
    binning = array.array('d', [xlo] + binning)
    ct.print_success(f"Found {len(binning)-1} bins for {handle} with stat ~ {nevents:.1f} per bin.")
    return binning

def get_comparison(histo1, histo2, method = 'ratio'):

    label = {
        'ratio'     : 'Data/MC',
        'difference': 'Data-MC',
        'reldiff'   : '(Data-MC)/MC',
        'pull'      : '(Data-MC)/#sigma',
    }

    h_out = histo1.Clone(f"{histo1.GetName()}_{method}_{histo2.GetName()}")
    if method == 'ratio':
        h_out.Divide(histo2)
    elif method == 'difference':
        h_out.Add(histo2, -1)
    elif method == 'reldiff':
        h_out.Add(histo2, -1)
        h_out.Divide(histo2)
    elif method == 'pull':
        h_out.Add(histo2, -1)
        for i in range(h_out.GetNbinsX()):
            err = max( 0. , np.sqrt(histo1.GetBinError(i+1)**2 + histo2.GetBinError(i+1)**2))
            h_out.SetBinContent(i+1, h_out.GetBinContent(i+1)/err if err > 0 else 0.0)
            h_out.SetBinError(i+1, 1.0)
    else :
        ct.print_error(f"Comparison method {method} not recognized!")
        return None
    
    return h_out, label[method]

def flatten_histo(histo, xlo =0, xhi=1, ybins = 25, ylo=0, yhi=2):
    """Flatten the ratio histogram based on x slices."""
    ilo = histo.GetXaxis().FindBin(xlo)
    ihi = histo.GetXaxis().FindBin(xhi)
    flat_histo = ROOT.TH1F(f"flat_histo_{ilo}_{ihi}", "", ybins, ylo, yhi)
    for i in range(ilo, ihi):
        #print(f"bin {i} [{histo.GetBinLowEdge(i):.3f}, {histo.GetBinLowEdge(i+1):.3f}] = {histo.GetBinContent(i):.1f} ± {histo.GetBinError(i):.1f}")
        flat_histo.Fill(histo.GetBinContent(i))
    
    return flat_histo

if __name__ == '__main__' :

    args = parse_arguments()
    input_file = args.input
    bdt_cut = args.bdt_cut
    output_dir = args.output
    year = str(args.year)
    method = args.method
    tag = '_'.join([method, year])
    CMS.SetLumi(config.LumiVal_plots[year], run = year)
    
    
    mc_w    = 'total_weight'  # MC weight branch name
    data_w  = 'total_weight'  # Data weight branch name

    # --- I/O ---
    mc_rdf   = ROOT.RDataFrame("mc_tree", input_file)
    data_rdf = ROOT.RDataFrame("data_tree", input_file)
    if not mc_rdf or not data_rdf:
        print("Error: Unable to open input file or find trees.")
        sys.exit(1)
    
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        ct.print_info(f"Created output directory: {output_dir}")
    output_file = os.path.join(output_dir, f"BDTefficiency_{tag}.root")

    logfile = os.path.join(output_dir, f'BDTefficiency_{tag}.log')
    log = open(logfile, 'w')
    log.write("--- BDT efficiency tes "+"--"*20 + "\n")
    log.write(f"[+] Input file: {input_file}\n")


    # --- Efficiency calculation ---
    var = 'bdt_score'

    N_mc = mc_rdf.Sum(mc_w).GetValue()
    N_mc_pass = mc_rdf.Filter(f'{var} > {bdt_cut}').Sum(mc_w).GetValue()
    eff_mc = N_mc_pass / N_mc if N_mc > 0 else 0.0
    eff_mc_err = np.sqrt(eff_mc * (1 - eff_mc) / N_mc) if N_mc > 0 else 0.0

    N_data = data_rdf.Sum(data_w).GetValue()
    N_data_pass = data_rdf.Filter(f'{var} > {bdt_cut}').Sum(data_w).GetValue()
    eff_data = N_data_pass / N_data if N_data > 0 else 0.0
    eff_data_err = np.sqrt(eff_data * (1 - eff_data) / N_data) if N_data > 0 else 0.0

    eff_sys = eff_data/eff_mc if eff_mc > 0 else 0.0
    eff_sys_err = eff_sys * np.sqrt( (eff_data_err/eff_data)**2 + (eff_mc_err/eff_mc)**2 ) if eff_data > 0 and eff_mc > 0 else 0.0 

    ct.print_info(f"BDT cut at {bdt_cut}:", logger=log)
    ct.print_info(f"  Data Efficiency = {eff_data:.4f} ± {eff_data_err:.4f} (N={N_data_pass:.1f}/{N_data:.1f})", logger=log)
    ct.print_info(f"  MC Efficiency   = {eff_mc:.4f} ± {eff_mc_err:.4f} (N={N_mc_pass:.1f}/{N_mc:.1f})", logger=log)
    ct.print_info(f"  Efficiency Scale Factor (Data/MC) = {eff_sys:.4f} ± {eff_sys_err:.4f}", logger=log)
    
    # --- STATISTICAL COMPATIBILITY TEST ---
    # get the optimal binning for statistically equivalent bins
    bins = np.linspace(0, 1, 51)  # 20 bins from -1 to 1
    bins = get_binning(mc_rdf, handle=var, weight=mc_w, xlo=0, xhi=1, threshold=bdt_cut)
    log.write(f"BDT binning: {list(bins)}\n")
    pull_lo, pull_hi = -1.0, 1.0

    h_mc = mc_rdf.Histo1D(('h_mc', ';BDT score;Events', len(bins)-1, bins), var, mc_w).GetValue()
    h_mc.Sumw2()
    h_data = data_rdf.Histo1D(('h_data', ';BDT score;Events', len(bins)-1, bins), var, data_w).GetValue()
    h_data.Sumw2()

    h_pull, pull_label = get_comparison(h_data, h_mc, method=method)
    #h_data.Clone("h_pull")
    #h_pull.Add(h_mc, -1)
    #h_pull.Divide(h_mc)

    canv = CMS.cmsDiCanvas(
        'cbdt',
        x_min = bins[0], x_max=bins[-1],
        y_min = 0.0, y_max=2.0*max(h_data.GetMaximum(), h_mc.GetMaximum()),
        r_min = pull_lo, r_max = pull_hi,
        nameXaxis='BDT score',
        nameYaxis='Events',
        nameRatio=pull_label,
        square=False
    )
    canv.cd()
    leg = CMS.cmsLeg(0.6, 0.70, 0.9, 0.9)
    leg.AddEntry(h_mc,   'D_{s}#rightarrow #phi#pi MC', 'lf')
    leg.AddEntry(h_data, 'sData', 'lep')
    canv.cd(1)
    CMS.cmsDraw(
        h_mc, 'HIST',
        marker=0,
        msize=0,
        lcolor=ROOT.kGreen+1,
        lwidth=2,
        fstyle=3004,
        fcolor=ROOT.kGreen+1,
    )
    CMS.cmsDraw(
        h_data, 'E1 SAME',
        marker=20,
        msize=1,
        lcolor=ROOT.kBlack,
        lwidth=2,
    )
    canv.cd(2)
    CMS.cmsDraw(
        h_pull, 'E1',
        marker=20,
        msize=1,
        lcolor=ROOT.kBlack,
        lwidth=2,
    )
    canv.cd()
    
    CMS.SaveCanvas(canv, os.path.join(output_dir, f'BDT_dataMC-{tag}.png'), False)
    CMS.SaveCanvas(canv, os.path.join(output_dir, f'BDT_dataMC-{tag}.pdf'), True)

    # 
    pull_dist = flatten_histo(h_pull, xlo=0, xhi=1, ybins=25, ylo=pull_lo, yhi=pull_hi)
    obs = h_pull.GetBinContent(h_pull.FindBin(bdt_cut+0.001))
    gausfit_res = pull_dist.Fit("gaus", "s")
    mean = gausfit_res.Parameter(1)
    mean_err = gausfit_res.ParError(1)
    sigma = gausfit_res.Parameter(2)
    sigma_err = gausfit_res.ParError(2)
    ct.print_info(f"Pull distribution fit results:", logger=log)
    ct.print_info(f"  Mean  = {mean:.4f} ± {mean_err:.4f}", logger=log)
    ct.print_info(f"  Sigma = {sigma:.4f} ± {sigma_err:.4f}", logger=log)
    fitfunc = pull_dist.GetFunction("gaus")

    cpull = CMS.cmsCanvas(
        'cpull',
        x_min = pull_lo, x_max = pull_hi+1.0,
        y_min = 0.0,  y_max = 1.4*pull_dist.GetMaximum(),
        nameXaxis=pull_label,
        nameYaxis='Events',
        square=False
    )
    cpull.cd()
    legpull = CMS.cmsLeg(0.6, 0.70, 0.9, 0.9)
    CMS.cmsDraw(
        pull_dist, 'hist',
        marker=20,
        msize=1,
        lcolor=ROOT.kBlue,
        fcolor=0,
        fstyle=1,
        lwidth=2,
    )
    legpull.AddEntry(pull_dist, f'{method} distribution', 'l')
    CMS.cmsObjectDraw(fitfunc, '', LineWidth=2, LineColor=ROOT.kRed, MarkerStyle=0)
    legpull.AddEntry(fitfunc, 'Gaussian fit', 'l')
    
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.DrawLatex(0.6, 0.65, f"Mean = {mean:.3f} #pm {mean_err:.3f}")
    text.DrawLatex(0.6, 0.60, f"#sigma = {sigma:.3f} #pm {sigma_err:.3f}")
    
    observed_pull = ROOT.TLine(obs, 0, obs, 0.7*pull_dist.GetMaximum())
    CMS.UpdatePad()
    CMS.cmsDrawLine(observed_pull, lcolor=ROOT.kBlack, lstyle=1, lwidth=5)
    legpull.AddEntry(observed_pull, f'obs BDT > {bdt_cut}', 'l')
    CMS.SaveCanvas(cpull, os.path.join(output_dir, f'BDT_distribution-{tag}.png'), False)
    CMS.SaveCanvas(cpull, os.path.join(output_dir, f'BDT_distribution-{tag}.pdf'), True)

    p_value = pull_dist.Integral(pull_dist.FindBin(obs), pull_dist.GetNbinsX()+1) / pull_dist.Integral()
    ct.print_info(f"P-value from integral for observed pull {obs:.4f} at BDT cut {bdt_cut}: p = {p_value:.4f}", logger=log)
    tobs = (obs - mean) / sigma if sigma > 0 else 0.0
    ct.print_info(f"P-value from fit Gaussian P(μ={mean:.3f}, σ={sigma:.3f}) = {(ROOT.TMath.Erfc(tobs)/np.sqrt(2.)):.4f} ({tobs:.1f}σ)", logger=log)

    log.close()
    # save in root file
    output_root = ROOT.TFile.Open(output_file, "RECREATE")
    output_root.cd()
    h_mc.Write()
    h_data.Write()
    h_pull.Write()
    pull_dist.Write()
    output_root.Close()
    
    

    #bdt_slices = [0.0, 0.5, 0.7, 0.9, 0.990, 1.0]
    ##bdt_slices = [0.9, 1.0]
    #histo_list = []
    #legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    #legend.SetBorderSize(0)
    #legend.SetFillStyle(0)
    #legend.SetTextFont(42)
    #legend.SetTextSize(0.04)
    ## inclusive
    ##flat_histo = flatten_ratio(ratio_histo, bdt_slices[0], bdt_slices[-1])
    ##ct.print_info(f"Inclusive BDT slice [{bdt_slices[0]}, {bdt_slices[-1]}]: Mean efficiency = {flat_histo.GetMean():.4f} ± {flat_histo.GetMeanError():.4f}")
    ##flat_histo.SetDirectory(0)
    ##histo_list.append(flat_histo)
    ##canv.SaveAs(os.path.join(output_dir, f'BDT_efficiency_inclusive.png'))
    #for i in range(len(bdt_slices)-1):
    #    xlo = bdt_slices[i]
    #    xhi = bdt_slices[-1]
    #    flat_histo = flatten_ratio(ratio_histo, xlo, xhi)
    #    flat_histo.SetDirectory(0)
    #    ct.print_info(f"BDT slice [{xlo}, {xhi}]: Mean efficiency = {flat_histo.GetMean():.4f} ± {flat_histo.GetMeanError():.4f}")
    #    histo_list.append(flat_histo)
    #canv = ROOT.TCanvas("canv", "canv", 800, 600)
    #canv.cd()
    #for i, histo in enumerate(histo_list):
    #    histo.GetYaxis().SetRangeUser(0, 60)
    #    histo.SetLineColor(i+1)
    #    histo.SetLineWidth(2)
    #    histo.SetFillColor(i+1)
    #    histo.SetFillStyle(3004)
    #    histo.SetMarkerColor(0)
    #    histo.SetMarkerStyle(0)
    #    histo.SetTitle(f"BDT efficiency slices")
    #    legend.AddEntry(histo, f'BDT > {bdt_slices[i]:.3f}', 'l')
    #    histo.Draw("HIST same" if i>0 else "HIST")
    #legend.Draw("same")
    #canv.SaveAs(os.path.join(output_dir, f'BDT_efficiency_slice.png'))