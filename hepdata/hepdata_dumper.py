# hepdata_dumper.py
import os 
import numpy as np

import hepdata_lib as hepd

_TOPUB_ = ["limits"] #["massfit", "limits"]
_QUANTILES_ = [0.025, 0.16, 0.5, 0.84, 0.975, -1.0]
_NDEC_ = 2

def read_csv_limit(fname):
    t = np.genfromtxt(fname, delimiter=",", names=True, autostrip=True)
    row = [t["mh"][0]]
    for q in _QUANTILES_:
        sel = np.isclose(t["quantileExpected"], q, atol=1e-3)
        if sel.sum() != 1:
            raise ValueError(f"{fname}: found {sel.sum()} rows for quantile {q}")
        row.append(t["limit"][sel][0])
    return np.array(row, dtype=float)

def read_limits(filenames, factor = 10):
    rows = []
    for fname in filenames:
        if fname.endswith(".csv"):
            d = read_csv_limit(fname)
        else:
            d = d = np.array(hepd.RootFileReader(fname).read_limit_tree()[0], dtype=float)
        d[1:] *= factor
        rows.append(d)
        print(f" > {fname}\n\t{d}")

    return np.array(rows)


if __name__ == "__main__":
    
    submission = hepd.Submission()
    submission_name = "CMS-BPH-24-010"
    submission.read_abstract("inputs/abstract.txt")
    submission.add_link("Public CMS page with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/BPH-24-010/index.html") # not working yet
    #submission.add_link("arXiv", "")
    #submission.add_record_id(1111111, "inspire")

    print(f"\n---- submission {submission_name} with {_TOPUB_} tables ----\n")

    #####################
    #      MASS FIT     #
    #####################
    if "massfit" in _TOPUB_:
    
        # ---- W CHANNEL ----
        # read root file 
        reader = hepd.RootFileReader("inputs/massfit_SB_A22_ANv11_bdt0p991.root")
        data_reader = reader.read_graph("data")
        bkg_model   = reader.read_hist_1d("bkg_model")
        sig_w_model = reader.read_hist_1d("sig_0_model")
        sig_z_model = reader.read_hist_1d("sig_1_model")

        # define the variables 
        m3m = hepd.Variable("m$_{3\\mu}$", is_independent=True, is_binned=True, units="GeV")
        m3m.values = sig_w_model["x_edges"]

        sig_w_y = hepd.Variable("Number of expected signal events from W decay", is_independent=False, is_binned=False, units="")
        sig_w_y.values = sig_w_model["y"]

        sig_z_y = hepd.Variable("Number of expected signal events from Z decay", is_independent=False, is_binned=False, units="")
        sig_z_y.values = sig_z_model["y"]

        bkg_y = hepd.Variable("Number of expected background events", is_independent=False, is_binned=False, units="")
        bkg_y.values = bkg_model["y"]

        data = hepd.Variable("Number of observed events", is_independent=False, is_binned=False, units="")
        data.values = data_reader["y"]

        table = hepd.Table("test-A22")
        table.description = "Caption"
        table.location = ""
        table.keywords["observables"] = ["N"]
        #table.add_image("example_inputs/CMS-B2G-17-009_Figure_004-a.pdf")

        table.add_variable(m3m)
        table.add_variable(sig_w_y)
        table.add_variable(sig_z_y)
        table.add_variable(bkg_y)
        table.add_variable(data)

        submission.add_table(table)
        
    #############################
    #      EXCLUSION LIMITS     #
    #############################
    if "limits" in _TOPUB_:

        _pos_mass, _pos_minus2sigma, _pos_minus1sigma, _pos_exp, _pos_plus1sigma, _pos_plus2sigma, _pos_obs  = 0, 1, 2, 3, 4, 5, 6
        _factor = 10 # to convert from 10^-7 to 10^-8
        combine_results ={
            #'HF 2022'              : './inputs/higgsCombine.HFTau3Mu_22Combined.HybridNew.mH1.777.root',
            #'HF 2023'              : './inputs/higgsCombine.HFTau3Mu_23Combined.HybridNew.mH1.777.root', 
            'Heavy-flavor 2022+2023'         : './inputs/higgsCombine.HFTau3Mu_Run3_2223.HybridNew.mH1.777.root',  
            #'V 2022 A'             : './inputs/higgsCombine.W_22A_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2022 B'             : './inputs/higgsCombine.W_22B_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2022 C'             : './inputs/higgsCombine.W_22C_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2022'               : './inputs/higgsCombine.W_22Combined_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2023 A'             : './inputs/higgsCombine.W_23A_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2023 B'             : './inputs/higgsCombine.W_23B_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2023 C'             : './inputs/higgsCombine.W_23C_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            #'V 2023'               : './inputs/higgsCombine.W_23Combined_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            'V 2022+2023'          : './inputs/higgsCombine.W_Run3_2223Combined_ANv11_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            'Heavy-flavor+V 2022'            : './inputs/higgsCombine.HFW_22Combined_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            'Heavy-flavor+V 2023'            : './inputs/higgsCombine.HFW_23Combined_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            'Heavy-flavor+V 2022+2023'       : './inputs/higgsCombine.HFW_Run3_2223Combined_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
            'Heavy-flavor+W 2016-2018'       : './inputs/higgsCombine.HFW_CombinedRun2.Extrapolation.mH1.777.csv',
            'Heavy-flavor+V 2016-2023'       : './inputs/higgsCombine.HFV_Run2_Run3_2223_mar18_limitResults_CL0.90_expectedFromGrid_all.HybridNew.mH1.777.UNBLIND.root',
        }
        _table_paper_ = combine_results.keys()
        
        lim_table = hepd.Table("Table_5")
        lim_table.description = r"Expected and observed upper limits at 90% CL on $\tau \to 3\mu$, in units of 10$^{-8}$, for the individual channels and data taking periods of this analysis and their combinations. The last row reports the combination with the previous CMS results based on 2016--2018 data."
        lim_table.location = "Data from Table 5 and Figure 7 of the paper draft BPH-24-010_v7."
        lim_table.add_image("/eos/user/c/cbasile/www/Tau3Mu_Run3/paper/plots/limit_results_HFVTau3Mu-Run2-Run3.pdf")
        lim_table.add_image("/eos/user/c/cbasile/www/Tau3Mu_Run3/paper/plots/limit_results_HFVTau3Mu-Run3.pdf")

        # keywords TBD
        lim_table.keywords["observables"] = ["CLS", "WIDTH"]
        lim_table.keywords["reactions"]   = [
            "P P --> W+ X --> TAU+ NUTAU X --> MU+ MU- MU+ NUTAU X", 
            "P P --> Z0 X --> TAU+ TAU-  X --> MU+ MU- MU+ TAU- X",
            "P P --> B0 X --> TAU+ NUTAU X   X --> MU+ MU- MU+ MU- X",
            "P P --> B+ X --> TAU+ NUTAU X   X --> MU+ MU- MU+ MU- X",
            "P P --> D/S+ X --> TAU+ NUTAU X --> MU+ MU- MU+ MU- X",
        ]
        lim_table.keywords["phrases"] = ["Lepton Flavour Violation", "Tau", "Branching Fraction", "Upper Limit", "CL"]

        # categories
        cat = hepd.Variable("Category", is_independent=True, is_binned=False)
        cat.values = _table_paper_

        # limits
        lim_values = read_limits([combine_results[name] for name in _table_paper_], factor=_factor)

        br  = r"90% CL upper limit on $\mathcal{B}(\tau \to 3\mu)$"
        obs = hepd.Variable(f"Observed {br}",        is_independent=False, is_binned=False, units=r"$10^{-8}$")
        exp = hepd.Variable(f"Median expected {br}", is_independent=False, is_binned=False, units=r"$10^{-8}$")
        obs.values = np.round(lim_values[:, _pos_obs], _NDEC_).tolist()
        exp.values = np.round(lim_values[:, _pos_exp], _NDEC_).tolist()


        for band in zip([("68% expected", _pos_minus1sigma, _pos_plus1sigma), ("95% expected", _pos_minus2sigma, _pos_plus2sigma)]):
            label, lo, hi = band[0]
            print(f" > {label}")
            unc = hepd.Uncertainty(label, is_symmetric=False)

            unc.set_values_from_intervals(zip(
                (np.round(lim_values[:,lo], _NDEC_)), 
                (np.round(lim_values[:,hi], _NDEC_))), 
                nominal=exp.values)
            exp.add_uncertainty(unc)
        
        
        lim_table.add_variable(cat)
        lim_table.add_variable(obs)
        lim_table.add_variable(exp)

        submission.add_table(lim_table)
    
    
    # ---- FINAL SUBMISSION ----
    # common keywords for all tables
    for table in submission.tables: # FIXME : to be checked
        table.keywords["cmenergies"]    = [13000, 13600]
    
    submission.create_files(submission_name,remove_old=True)
