import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
import mva.config as config
import plots.plotting_tools as plt

signal = config.mc_bdt_samples['WTau3Mu']
data   = config.data_bdt_samples['WTau3Mu']


sig_rdf  = ROOT.RDataFrame("tree_w_BDT",  'mc_mumuOS.root').Define('tau_fit_absEta', 'fabs(tau_fit_eta)')#.Filter(config.base_selection)
data_rdf = ROOT.RDataFrame("tree_w_BDT",  'data_mumuOS.root').Define('tau_fit_absEta', 'fabs(tau_fit_eta)')#.Filter('&'.join([config.base_selection, config.sidebands_selection]))
if sig_rdf.Count().GetValue() == 0 or data_rdf.Count().GetValue() == 0:
    print("No events found after selection")
    sys.exit(0)

BDT_th = [0.0, 0.985, 0.990, 0.995]
BDT_th = [0.0, 0.980]
n_slices = len(BDT_th)
vars = ['tau_mumuOS_fitM']#['tau_mu12_fitM', 'tau_mu13_fitM', 'tau_mu23_fitM']
ref_vars = ['tau_mu12_M', 'tau_mu13_M', 'tau_mu23_M']
categories = ['ABC', 'A', 'B', 'C']
#Phi_veto = config.phi_veto
#Omega_veto = config.omega_veto
Phi_veto            = '''(fabs(tau_mu12_M- {mass:.3f})> {window:.3f} & fabs(tau_mu23_M - {mass:.3f})> {window:.3f} & fabs(tau_mu13_M -  {mass:.3f})>{window:.3f})'''.format(mass =config.Phi_mass_ , window = config.Phi_window_/2. )
Omega_veto          = '''(fabs(tau_mu12_M- {mass:.3f})> {window:.3f} & fabs(tau_mu23_M - {mass:.3f})> {window:.3f} & fabs(tau_mu13_M -  {mass:.3f})>{window:.3f})'''.format(mass =config.Omega_mass_ , window = config.Omega_window_/2. )



min_val, max_val, n_bins = 0.4, 1.4, 100

for bdt in BDT_th:
    N_MC   = sig_rdf.Filter(f'(bdt_score> {bdt})').Count().GetValue()
    N_data = data_rdf.Filter(f'(bdt_score> {bdt})').Count().GetValue()

    for cat in categories:
        selection = '&'.join([
            f'(bdt_score> {bdt})',
            config.cat_eta_selection_dict[cat],
            ])
        for i, var in enumerate(vars):
            label = "m(#mu^{+}#mu^{-})" if "mumuOS" in var else "m(#mu#mu)"
            bin_w = (max_val - min_val) / n_bins * 1000 # in MeV

            h_data = data_rdf.Filter(selection).Histo1D(("h_data", f";{label}(GeV);Events/{bin_w:.0f} MeV", n_bins, min_val, max_val), var).GetValue()
            h_sig  = sig_rdf.Filter(selection).Histo1D(("h_sig", f";{label}(GeV;Events/{bin_w:.0f} MeV",   n_bins, min_val, max_val), var).GetValue()

            h_data.SetMarkerStyle(20)
            h_data.SetMarkerSize(0.8)
            h_data.SetLineColor(ROOT.kBlack)
            h_data.SetLineWidth(2)
            h_data.SetMarkerColor(ROOT.kBlack)
            
            h_sig.SetLineColor(ROOT.kRed)
            h_sig.SetLineWidth(2)
            h_sig.SetMarkerColor(ROOT.kRed)
            h_sig.SetMarkerStyle(0)
            h_sig.SetMarkerSize(0)

            # -- inclusive histograms --
            if i == 0:
                h_data_total = h_data.Clone("h_data_total")
                h_sig_total  = h_sig.Clone("h_sig_total")
            else:
                h_data_total.Add(h_data)
                h_sig_total.Add(h_sig)

            h_data.Scale(1.0 / h_data.Integral())
            h_sig.Scale(1.0 / h_sig.Integral())

            y_max = 1.5*max(h_data.GetMaximum(), h_sig.GetMaximum())
            
            # draw veto boxes
            box_Phi = ROOT.TBox(config.Phi_mass_ - config.Phi_window_/2., 0, config.Phi_mass_ + config.Phi_window_/2., 1.1*h_data.GetMaximum())
            box_Phi.SetFillColorAlpha(ROOT.kGray+2, 0.4)
            box_Omega = ROOT.TBox(config.Omega_mass_ - config.Omega_window_/2., 0, config.Omega_mass_ + config.Omega_window_/2., 1.1*h_data.GetMaximum())
            box_Omega.SetFillColorAlpha(ROOT.kGray+2, 0.4)
            

            plt.ratio_plot_CMSstyle(
                [h_data], 
                h_sig,
                description=["Data sidebands", f"W#rightarrow#tau(3#mu)#nu MC"],
                file_name=f"BDT_slice_{bdt}_cat{cat}_{var}",
                ratio_w = 8 if bdt > 0.5 else 2.0,
                draw_opt_num = "PE",
                draw_opt_den = "HIST",
                y_lim = (0, y_max),
                CMSadditionalText = [
                    '',
                    f'BDT score > {bdt:.3f}' if bdt > 0.0 else "No BDT selection",
                    f'CAT {cat}',
                    ],
                year = "2022+2023"
            )
            print("--------------------------------------------------\n")
        continue    
        
        h_data_total.Scale(1.0 / h_data_total.Integral())
        h_sig_total.Scale(1.0 / h_sig_total.Integral())
        h_sig_total.GetXaxis().SetTitle("m(#mu^{+}#mu^{-}) (GeV)") 
        plt.ratio_plot([h_data_total], h_sig_total,
                    file_name=f"BDT_slice_{bdt}_mumuOS",
                    title=f"BDT score > {bdt}",
                    ratio_w = 8 if bdt > 0.5 else 2.0,
                    draw_opt_num = "PE",
                    draw_opt_den = "HIST",
                    y_lim = (0, 1.5*max(h_data_total.GetMaximum(), h_sig_total.GetMaximum())),
                    to_ploton=[text, box_Phi, box_Omega]
        )

            

        # apply the Phi veto
        print(f"BDT > {bdt:.3f}")
        N_mc_phi_veto   = sig_rdf.Filter('&'.join([f'(bdt_score> {bdt})', Phi_veto])).Count().GetValue()
        N_data_phi_veto = data_rdf.Filter('&'.join([f'(bdt_score> {bdt})', Phi_veto])).Count().GetValue()
        print(f" + Phi veto: MC efficiency = {N_mc_phi_veto/N_MC:.4f} ({N_mc_phi_veto}/{N_MC}), Data efficiency = {N_data_phi_veto/N_data:.4f} ({N_data_phi_veto}/{N_data})")
        # apply the Omega veto
        N_mc_omega_veto   = sig_rdf.Filter('&'.join([f'(bdt_score> {bdt})', Phi_veto, Omega_veto])).Count().GetValue()
        N_data_omega_veto = data_rdf.Filter('&'.join([f'(bdt_score> {bdt})', Phi_veto, Omega_veto])).Count().GetValue()
        print(f" + Phi & Omega veto: MC efficiency = {N_mc_omega_veto/N_MC:.4f} ({N_mc_omega_veto}/{N_MC}), Data efficiency = {N_data_omega_veto/N_data:.4f} ({N_data_omega_veto}/{N_data})")