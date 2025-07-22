import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import os
import sys

import cmsstyle as CMS
CMS.SetEnergy(13.6)
CMS.SetExtraText('Preliminary')
CMS.ResetAdditionalInfo()


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mva.config as config
CMS.SetLumi(f'2022+2023, {config.LumiVal_plots["Run3"]}')
#CMS.AppendAdditionalInfo(f'm_{{\mu\mu}} \in [{config.Phi_mass_ - config.Phi_window_/2.:.2f}, {config.Phi_mass_ + config.Phi_window_/2.:.2f}] GeV')
CMS.AppendAdditionalInfo(f'm_{{\mu\mu}} \in [{config.Ds_phi_mass_lo:.2f}, {config.Ds_phi_mass_hi:.2f}] GeV')

input_file =  config.data_bdt_samples['WTau3Mu'] #'/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_data_kFold_Optuna_HLT_overlap_apply_LxyS2.0_2024Oct10.root'
selection = '&'.join([
    config.base_selection,
    config.sidebands_selection,
    config.displacement_selection,
    config.peakB_phi_selection,
    '(bdt_score > 0.9950)'
])
rdf = ROOT.ROOT.RDataFrame('tree_w_BDT', input_file)
rdf = rdf.Filter(selection)
#full mass range
h = rdf.Histo1D(('tau_fit_mass', 'tau_fit_mass', 45, 1.6, config.mass_range_hi), 'tau_fit_mass').GetValue()
# highlits Ds mass region
hh = rdf.Filter('(tau_fit_mass > 1.95) && (tau_fit_mass < 2.00)').Histo1D(('tau_fit_mass', 'tau_fit_mass', 45, 1.6, config.mass_range_hi), 'tau_fit_mass')

c = CMS.cmsCanvas(
    'c',
    x_min = 1.6, x_max = config.mass_range_hi,
    y_min = 0, y_max = 10,
    nameXaxis = 'm_{3#mu} (GeV)',
    nameYaxis = f'Events/{h.GetXaxis().GetBinWidth(1)*1000.0:.0f} MeV',
    square=True,
    iPos=11,
    extraSpace=0.02,
    with_z_axis=False,
    scaleLumi=1
)
CMS.cmsDraw(
    h, 'PE',
    marker=ROOT.kFullCircle,
    msize=1.0,
    mcolor=ROOT.kBlack,
    lstyle=ROOT.kSolid,
    lwidth=1,
    lcolor=ROOT.kBlack,
    fstyle=0,
    fcolor=0,
    alpha=-1,
)
CMS.cmsDraw(
    hh, 'PE same',
    marker=ROOT.kFullCircle,
    msize=1.0,
    mcolor=ROOT.kRed,
    lstyle=ROOT.kSolid,
    lwidth=2,
    lcolor=ROOT.kRed,
    fstyle=0,
    fcolor=0,
    alpha=-1,
)




#c = ROOT.TCanvas('c', 'c', 800, 800)
#h.Draw('pe')
#hh.Draw('same pe')
#c.Draw()
c.SaveAs('./plots/peakingBKG/Tau3Mu_mass_postBDT.png')
c.SaveAs('./plots/peakingBKG/Tau3Mu_mass_postBDT.pdf')
#c.SaveAs('/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/peaking_bkg/Tau3Mu_mass_postBDT.png')
#c.SaveAs('/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/AN_v2/Training_kFold_Optuna_HLT_overlap_LxyS2.0_2024Jul16/peaking_bkg/Tau3Mu_mass_postBDT.pdf')
