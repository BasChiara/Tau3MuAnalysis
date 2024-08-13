import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import sys
sys.path.append('../../')
from plots.plotting_tools import ratio_plot_CMSstyle

xrootd_prefix = 'root://cms-xrd-global.cern.ch//'
isLastCopy_string = '(GenPart_statusFlags & (1<<13))'
W_pdgID = 24
Wgen_selection = f'(fabs(GenPart_pdgId) == {W_pdgID}) && {isLastCopy_string}'

# --- read NANOAOD files from txt file
input_t3m_file_list = open('WtoTauNu_Tauto3Mu_Run3Summer22EENanoAODv12_fileList_demo.txt', 'r').readlines()
tree_t3m = ROOT.TChain('Events')
# tau3mu
for file_name in input_t3m_file_list:
    tree_t3m.Add(xrootd_prefix + file_name.strip())
print(f'[+] LO file has {tree_t3m.GetEntries()} entries')
input_NLO_file_list = open('WtoLNu-2Jets_Run3Summer22EENanoAODv12_fileList_demo.txt', 'r').readlines()
tree_NLO = ROOT.TChain('Events')
# NLO
for file_name in input_NLO_file_list:
    tree_NLO.Add(xrootd_prefix + file_name.strip())
print(f'[+] NLO file has {tree_NLO.GetEntries()} entries')
print('\n')
# --- W kinematics
# pT
pT_bins, pT_lo, pT_hi = 50, 0, 150
tree_t3m.Draw(f'GenPart_pt>>h_Wgen_t3m_pT({pT_bins},{pT_lo}, {pT_hi})', Wgen_selection, 'goff')
h_Wgen_t3m_pT = ROOT.gDirectory.Get('h_Wgen_t3m_pT')
tree_NLO.Draw(f'GenPart_pt>>h_Wgen_NLO_pT({pT_bins},{pT_lo}, {pT_hi})', Wgen_selection, 'goff')
h_Wgen_NLO_pT = ROOT.gDirectory.Get('h_Wgen_NLO_pT')
print(f'... done with pT plots')
# eta
eta_bins, eta_lo, eta_hi = 35, -3.5, 3.5
tree_t3m.Draw(f'GenPart_eta>>h_Wgen_t3m_eta({eta_bins}, {eta_lo}, {eta_hi})', Wgen_selection, 'goff')
h_Wgen_t3m_eta = ROOT.gDirectory.Get('h_Wgen_t3m_eta')
tree_NLO.Draw(f'GenPart_eta>>h_Wgen_NLO_eta({eta_bins}, {eta_lo}, {eta_hi})', Wgen_selection, 'goff')
h_Wgen_NLO_eta = ROOT.gDirectory.Get('h_Wgen_NLO_eta')
print(f'... done with eta plots')
# pT vs eta
tree_t3m.Draw(f'GenPart_pt:GenPart_eta>>h_Wgen_t3m_pTeta({eta_bins}, {eta_lo}, {eta_hi}, {pT_bins}, {pT_lo}, {pT_hi})', Wgen_selection, 'goff')
h_Wgen_t3m_pTeta = ROOT.gDirectory.Get('h_Wgen_t3m_pTeta')
tree_NLO.Draw(f'GenPart_pt:GenPart_eta>>h_Wgen_NLO_pTeta({eta_bins}, {eta_lo}, {eta_hi}, {pT_bins}, {pT_lo}, {pT_hi})', Wgen_selection, 'goff')
h_Wgen_NLO_pTeta = ROOT.gDirectory.Get('h_Wgen_NLO_pTeta')
print(f'... done with pT vs eta plots\n')
# nomralize
h_Wgen_t3m_eta.Scale(1/h_Wgen_t3m_eta.Integral())
h_Wgen_NLO_eta.Scale(1/h_Wgen_NLO_eta.Integral())
h_Wgen_t3m_pT.Scale(1/h_Wgen_t3m_pT.Integral())
h_Wgen_NLO_pT.Scale(1/h_Wgen_NLO_pT.Integral())
h_Wgen_t3m_pTeta.Scale(1/h_Wgen_t3m_pTeta.Integral())
h_Wgen_NLO_pTeta.Scale(1/h_Wgen_NLO_pTeta.Integral())

h_Wgen_ratio = h_Wgen_NLO_pTeta.Clone('h_Wgen_ratio')
h_Wgen_ratio.Divide(h_Wgen_t3m_pTeta)

# --- save to file
output_file = ROOT.TFile('W_NLOvsT3m.root', 'RECREATE')
output_file.cd()
h_Wgen_t3m_pT.Write()
h_Wgen_NLO_pT.Write()
h_Wgen_t3m_eta.Write()
h_Wgen_NLO_eta.Write()
h_Wgen_t3m_pTeta.Write()
h_Wgen_NLO_pTeta.Write()
h_Wgen_ratio.Write()
output_file.Close()
print('[i] saved to W_NLOvsT3m.root')

# --- plot
print('[i] plotting ...')
c = ROOT.TCanvas('c', 'c', 1200, 800)
c.Divide(2, 1)
c.cd(1)
h_Wgen_t3m_pT.SetLineColor(ROOT.kRed)
h_Wgen_t3m_pT.SetLineWidth(2)
h_Wgen_t3m_pT.SetTitle('W pT')
h_Wgen_t3m_pT.Draw()
h_Wgen_NLO_pT.SetLineColor(ROOT.kBlue)
h_Wgen_NLO_pT.SetLineWidth(2)
h_Wgen_NLO_pT.Draw('same')
c.cd(2)
h_Wgen_t3m_eta.SetLineColor(ROOT.kRed)
h_Wgen_t3m_eta.SetLineWidth(2)
h_Wgen_t3m_eta.SetTitle('W eta')
h_Wgen_t3m_eta.Draw()
h_Wgen_NLO_eta.SetLineColor(ROOT.kBlue)
h_Wgen_NLO_eta.SetLineWidth(2)
h_Wgen_NLO_eta.Draw('same')

c.Draw()
c.SaveAs('W_NLOvsT3m_pTeta.pdf')

# --- ratio plot
print('[i] ratio plots ...')
ratio_plot_CMSstyle(
    histo_num = [h_Wgen_NLO_pT], 
    histo_den = h_Wgen_t3m_pT, 
    isMC = True,
    year = 2022,
    ratio_yname = 'NLO/LO',
    ratio_w = 0.5,
    file_name = 'W_NLOvsT3m_ratio_pT', 
)
ratio_plot_CMSstyle(
    histo_num = [h_Wgen_NLO_eta], 
    histo_den = h_Wgen_t3m_eta, 
    isMC = True,
    year = 2022,
    ratio_yname = 'NLO/LO',
    ratio_w = 0.5,
    file_name = 'W_NLOvsT3m_ratio_eta', 
)
