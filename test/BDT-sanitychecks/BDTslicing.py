import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import argparse
import os   
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config

import cmsstyle as CMS
CMS.setCMSStyle()
cmsStyle = CMS.getCMSStyle()
cmsStyle.SetErrorX(0)
cmsStyle.SetPalette(ROOT.kCMYK)
CMS.SetEnergy(13.6)
CMS.cmsGrid(False)
CMS.SetLumi(f'{config.LumiVal_plots["2022+2023"]}', run='2022+2023')

argparser = argparse.ArgumentParser(description='BDT slicing sanity check.')
argparser.add_argument('--process', choices=['WTau3Mu', 'W3MuNu', 'MTauX'], required=True, help='Process to analyze')
argparser.add_argument('--isMC', action='store_true', help='Flag to indicate if the sample is MC')
argparser.add_argument('--category', choices=['A', 'B', 'C', 'ABC'], default='ABC', help='Eta category for selection')
args = argparser.parse_args()


process = args.process
isMC = args.isMC
category = args.category
base_selection = '&'.join([
    config.base_selection,
    #config.phi_veto,
    config.cat_eta_selection_dict[category],
])
CMS.SetExtraText('Preliminary' if not isMC else 'Simulation Preliminary')
CMS.ResetAdditionalInfo()
if isMC: 
    CMS.AppendAdditionalInfo(config.legend_process[process])
    CMS.SetLumi('', run = '2022+2023')
if category != 'ABC': CMS.AppendAdditionalInfo(f'CAT {category}')
    

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

bdt_cuts = [0.0, 0.500, 0.600, 0.800, 0.900, 0.950, 0.990]
mass_range_lo = config.mass_range_lo if (not isMC and process!='W3MuNu') else 1.6
mass_range_hi = 2.0
nbins = int((mass_range_hi-mass_range_lo)/0.010)
h_bdtSel = []
for cut in bdt_cuts:
    selection = f'bdt_score>{cut}'
    tag = 'BDT' + str(cut).replace('.', 'p')
    h_bdtSel.append(rdf.Filter(selection).Histo1D((f'h_mass_{tag}', '', nbins,mass_range_lo,mass_range_hi), 'tau_fit_mass').GetPtr())

canv = CMS.cmsCanvas(
    'canv',
    x_min=mass_range_lo, x_max=mass_range_hi,
    y_min=0. if isMC else 1e-5, y_max=2.0 if isMC else 1.2,
    nameXaxis='m_{3#mu} (GeV)',
    nameYaxis='efficiency',
    square=False,
    extraSpace=0.05,
    yTitOffset=1.1,
)
canv.SetLogy(not isMC)

legend = CMS.cmsLeg(0.50, 0.70, 0.95, 0.90, columns=2)
for i in range(len(bdt_cuts)) :
    if i ==0 : continue
    h_bdtSel[i].Sumw2()
    h_bdtSel[i].Divide(h_bdtSel[0])
    h_bdtSel[i].SetLineWidth(2)
    h_bdtSel[i].SetMarkerStyle(20)
    legend.AddEntry(h_bdtSel[i], 'BDT > %.3f'%bdt_cuts[i], 'lp')
    canv.cd()
    h_bdtSel[i].Draw('EP same plc pmc')
legend.Draw()
currentPlot_name = os.path.join(os.path.expandvars('$WWW/Tau3Mu_Run3/BDTtraining/validations'), f'BDT_efficiency_vs_tau_mass_{process}' + ('_MC' if isMC else '_Data') + f'_{category}')
CMS.SaveCanvas(canv, currentPlot_name+'.png', False)
CMS.SaveCanvas(canv, currentPlot_name+'.pdf', True)
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)