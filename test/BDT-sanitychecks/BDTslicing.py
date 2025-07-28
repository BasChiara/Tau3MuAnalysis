import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kCMYK)
import os   
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config


process = 'WTau3Mu'
isMC = False
category = 'ABC'
base_selection = '&'.join([
    config.base_selection,
    config.phi_veto,
    config.cat_eta_selection_dict[category],
])

if process == 'WTau3Mu': sample = config.mc_bdt_samples[process] if isMC else config.data_bdt_samples[process]
elif process == 'W3MuNu': sample = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output//XGBout_W3MuNu_MC_noLxyScut.root'
elif process == 'MTauX':
    sample = [
        "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1650.root",
        "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1700.root",
        config.mc_bdt_samples['WTau3Mu'],
        "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1850.root",
        "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1900.root",
        "/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/MTauX//XGBout_WTau3Mu_MC_MTau1950.root",
    ]


if not isMC:
    base_selection += f'& {config.sidebands_selection}'
rdf = ROOT.RDataFrame("tree_w_BDT", sample)
rdf = rdf.Define('tau_fit_absEta', 'fabs(tau_fit_eta)').Filter(base_selection)


# ------------ EFFICIENCY vs Mtau ------------ # 

bdt_cuts = [0.0, 0.500, 0.600, 0.800, 0.900, 0.950, 0.990, 0.995]
mass_range_lo = config.mass_range_lo if not (isMC and process=='WTau3Mu') else 1.6
#mass_range_lo = 1.6
mass_range_hi = config.mass_range_hi
nbins = int((mass_range_hi-mass_range_lo)/0.01)
h_bdtSel = []
for cut in bdt_cuts:
    selection = f'bdt_score>{cut}'
    tag = 'BDT' + str(cut).replace('.', 'p')
    h_bdtSel.append(rdf.Filter(selection).Histo1D((f'h_mass_{tag}', '', nbins,mass_range_lo,mass_range_hi), 'tau_fit_mass').GetPtr())


c = ROOT.TCanvas('c', 'c', 800, 800)
c.SetLeftMargin(0.15)
legend = ROOT.TLegend(0.50, 0.60, 0.9, 0.9)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)
legend.SetTextFont(42)
h_bdtSel[0].Sumw2()
h_bdtSel[1].SetTitle(f'BDT efficiency vs #tau mass ({config.legend_process[process]})')
h_bdtSel[1].GetXaxis().SetTitle('m_{3#mu} (GeV)')
h_bdtSel[1].GetYaxis().SetTitle('efficiency')
h_bdtSel[1].GetYaxis().SetRangeUser(1e-4, 1.5)

for i in range(len(bdt_cuts)) :
    if i ==0 : continue
    h_bdtSel[i].Sumw2()
    h_bdtSel[i].Divide(h_bdtSel[0])
    h_bdtSel[i].SetLineWidth(2)
    h_bdtSel[i].SetMarkerStyle(0)
    legend.AddEntry(h_bdtSel[i], 'BDT > %.3f'%bdt_cuts[i], 'L')
    c.cd()
    h_bdtSel[i].Draw('EP same plc')
c.Update()
c.SetLogy(not isMC)
c.SetGridx()
c.SetGridy()
legend.Draw()
currentPlot_name = os.path.join('.', f'BDT_efficiency_vs_tau_mass_{process}' + ('_MC' if isMC else '_Data') + f'_{category}')
c.SaveAs(currentPlot_name + '.png')
c.SaveAs(currentPlot_name + '.pdf')
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)