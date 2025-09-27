import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)

import pandas as pd
import numpy as np

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import mva.config as cfg

def get_pdDataset(file, tree, branches, selection='(1)'):
    
    sig_rdf = ROOT.RDataFrame(tree, file).Filter(selection)
    df = pd.DataFrame(sig_rdf.AsNumpy(branches))

    df['min_mumu_fitM'] = df[['tau_mu12_fitM', 'tau_mu13_fitM', 'tau_mu23_fitM']].min(axis=1)
    cols = ['tau_mu12_M', 'tau_mu13_M', 'tau_mu23_M']
    df['min_mumu_M'] = df[cols].mask(df[cols] < 0).min(axis=1)

    return df

if __name__ == '__main__':

    selection = cfg.base_selection
    branches_to_load = ['tau_mu12_fitM', 'tau_mu13_fitM', 'tau_mu23_fitM', 'tau_mu12_M', 'tau_mu13_M', 'tau_mu23_M']

    # signal
    df_t3m = get_pdDataset(cfg.mc_samples['WTau3Mu'], 'WTau3Mu_tree', branches_to_load, selection)
    # W3munu
    df_w3m = get_pdDataset(cfg.mc_samples['W3MuNu'], 'WTau3Mu_tree', branches_to_load, selection)

    lo, hi, nbins = 0.0, 1.5, 100
    mass_var = 'min_mumu_fitM'

    eff_w3m_ref = np.array([0.85], dtype='float64')
    eff_t3m_ref = 0.80

    h_t3m_minM = ROOT.TH1F('h_t3m_minM', '', nbins, lo, hi)
    [h_t3m_minM.Fill(x) for x in df_t3m[mass_var]]
    
    h_w3m_minM = ROOT.TH1F('h_w3m_minM', '', nbins, lo, hi)
    [h_w3m_minM.Fill(x) for x in df_w3m[mass_var]]
    h_t3m_minM.Scale(1./h_t3m_minM.Integral())
    h_w3m_minM.Scale(1./h_w3m_minM.Integral())

    q = np.zeros(1, dtype='float64')
    h_w3m_minM.GetQuantiles(len(eff_w3m_ref), q, eff_w3m_ref)
    q = q[0]

    print(f'W3MuNu: {eff_w3m_ref[0]*100:.1f}% quantile at {q:.3f} GeV')
    bin_cut = h_t3m_minM.FindBin(q)
    eff_t3m = 1. - h_t3m_minM.Integral(1, bin_cut)/h_t3m_minM.Integral()
    print(f'WTau3Mu efficiency at the same cut: {eff_t3m*100:.1f}% (ref: {eff_t3m_ref*100:.1f}%)')
    

    h_t3m_minM.SetLineColor(cfg.color_process['WTau3Mu'])   
    h_t3m_minM.SetLineWidth(2)
    h_t3m_minM.GetXaxis().SetTitle('min m_{#mu#mu} [GeV]')
    h_t3m_minM.GetYaxis().SetTitle(f'Events / { (hi-lo)/nbins :.2f} GeV')
    h_t3m_minM.GetYaxis().SetTitleOffset(1.4)

    h_w3m_minM.SetLineColor(cfg.color_process['W3MuNu'])
    h_w3m_minM.SetLineWidth(2)
    h_w3m_minM.GetXaxis().SetTitle('min m_{#mu#mu} [GeV]')
    h_w3m_minM.GetYaxis().SetTitle(f'Events / { (hi-lo)/nbins :.2f} GeV')
    h_w3m_minM.GetYaxis().SetTitleOffset(1.4)

    h_t3m_minM.SetMaximum(1.2*max(h_t3m_minM.GetMaximum(), h_w3m_minM.GetMaximum()))
    
    legend = ROOT.TLegend(0.65, 0.75, 0.85, 0.85)   
    legend.AddEntry(h_t3m_minM, cfg.legend_process['WTau3Mu'], 'l')
    legend.AddEntry(h_w3m_minM, cfg.legend_process['W3MuNu'], 'l')
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)

    # vertical line at quantile
    line = ROOT.TLine(q, 0, q, h_t3m_minM.GetMaximum())
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.SetLineStyle(ROOT.kDashed)
    

    c = ROOT.TCanvas('c', 'c', 800, 600)
    c.SetLeftMargin(0.15)
    h_t3m_minM.Draw('HIST')
    h_w3m_minM.Draw('HIST same')
    line.Draw('same')
    legend.Draw()
    c.SaveAs(f'signal_{mass_var}.png')
    c.SaveAs(f'signal_{mass_var}.pdf')