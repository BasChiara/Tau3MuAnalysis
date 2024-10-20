import ROOT
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mva.config as config

input_file = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
selection = '&'.join([
    config.base_selection,
    config.sidebands_selection,
    config.displacement_selection,
    config.peakB_phi_selection,
    '(bdt_score > 0.9950)'
])
rdf = ROOT.ROOT.RDataFrame('tree_w_BDT', input_file)
#plot tau_fit_mass

h = rdf.Filter(selection).Histo1D(('tau_fit_mass', 'tau_fit_mass', 45, 1.6, config.mass_range_hi), 'tau_fit_mass').GetValue()
h.SetMarkerColor(ROOT.kBlack)
h.GetXaxis().SetTitle('M_{3#mu} (GeV)')
h.GetYaxis().SetTitle('Events')
h.SetTitle('')
h.SetMarkerStyle(20)
h.SetMarkerSize(0.5)
h.SetLineColor(ROOT.kBlack)
c = ROOT.TCanvas('c', 'c', 800, 800)
h.Draw('pe')
c.Draw()
c.SaveAs('/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/peaking_bkg/Tau3Mu_mass_postBDT.png')
c.SaveAs('/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/peaking_bkg/Tau3Mu_mass_postBDT.pdf')
