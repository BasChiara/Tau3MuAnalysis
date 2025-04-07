import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import correctionlib


# apply weights to nTrueInt in MC --> should get the 62.9mb PU profile
era = '2023preBPix'

# central corrections in correctionlib format
#       --> from https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration
base_cJson = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/LUM/"
json_file_list = {
   "2022preEE" : base_cJson +  "2022_Summer22/puWeights.json.gz",
   "2022EE" : base_cJson +  "2022_Summer22EE/puWeights.json.gz",
   "2023preBPix" : base_cJson +  "2023_Summer23/puWeights.json.gz",
   "2023BPix" : base_cJson +  "2023_Summer23BPix/puWeights.json.gz",
}
value_list = ["nominal", "up", "down"]

pu_corr = correctionlib.CorrectionSet.from_file(json_file_list[era])
corr_name = list(pu_corr.keys())[0]
print(f'[+] PU weights from {json_file_list[era]}')
pu_weights = pu_corr[corr_name]
print(f' [test] nTrueInt = 10, nominal = {pu_weights.evaluate(10.0, "nominal")}')


#get mc tree
# nanoAOD files with tau3mu preselection
nano_base = '/eos/cms/store/group/phys_bphys/cbasile/Tau3MuNano_2024Aug03/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/'
t3m_nano_files ={
    "2022preEE"     : nano_base + "crab_WnuTau3Mu_2022/240803_095729/0000/",
    "2022EE"        : nano_base + "crab_WnuTau3Mu_2022EE/240803_095719/0000/",
    "2023preBPix"   : nano_base + "crab_WnuTau3Mu_2023preBPix/240803_095748/0000/", 
    "2023BPix"      : nano_base + "crab_WnuTau3Mu_2023BPix/240803_095801/0000/" 
}
tree_name = 'Events'
chain = ROOT.TChain(tree_name)
chain.Add(t3m_nano_files[era] + '*.root')
rdf_nano = ROOT.RDataFrame(chain)
print('[+]entries nanoAOD : ', rdf_nano.Count().GetValue())

h_nTrueInt = rdf_nano.Histo1D(('nTrueInt', 'nTrueInt', 100, 0, 100), 'Pileup_nTrueInt').GetPtr()
h_nTrueInt.SetLineColor(ROOT.kBlue)
h_nTrueInt.SetLineStyle(ROOT.kDashed)
h_nTrueInt.SetLineWidth(2)
h_nTrueInt.SetMarkerColor(ROOT.kBlue)
h_nTrueInt.GetXaxis().SetTitle('nTrueInt')
h_nTrueInt.Scale(1./h_nTrueInt.Integral())
# re weight nTrueInt
h_nTrueInt_rw = h_nTrueInt.Clone('nTrueInt_rw')
for i in range(h_nTrueInt_rw.GetNbinsX()):
    nTrueInt = h_nTrueInt_rw.GetBinCenter(i)
    weight = pu_weights.evaluate(nTrueInt, "nominal")
    h_nTrueInt_rw.SetBinContent(i, h_nTrueInt_rw.GetBinContent(i) * weight)
    h_nTrueInt_rw.SetBinError(i, 0)
h_nTrueInt_rw.SetLineColor(ROOT.kBlue)
h_nTrueInt.SetLineStyle(ROOT.kSolid)
h_nTrueInt_rw.SetLineWidth(2)
h_nTrueInt_rw.SetMarkerColor(ROOT.kBlue)
h_nTrueInt_rw.Scale(1./h_nTrueInt_rw.Integral())
# get PU profile from configuration
file_central = ROOT.TFile.Open(f'pileup_histograms/pileupMC_central_MinBxsec69p2mb_{era}.root')
h_central = file_central.Get('h_mc_PU')
h_central.SetDirectory(0)
file_central.Close()
h_central.SetLineColor(ROOT.kBlack)
h_central.SetLineWidth(2)
h_central.GetXaxis().SetTitle('nTrueInt')
# get PU from DATA
file_data = ROOT.TFile.Open(f'pileup_histograms/pileupDATA_{era}.root')
h_data = file_data.Get('pileup')
h_data.SetDirectory(0)
file_data.Close()
h_data.SetLineColor(ROOT.kGreen+2)
h_data.SetLineWidth(2)
h_data.Scale(1./h_data.Integral())


c = ROOT.TCanvas('c', 'c', 800, 600)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h_nTrueInt, 'MC', 'l')
legend.AddEntry(h_nTrueInt_rw, 'MC reweighted', 'l')
legend.AddEntry(h_central, 'PU profile 69.2mb', 'l')
legend.AddEntry(h_data, 'DATA', 'l')
h_central.Draw('hist')
h_data.Draw('hist same')
h_nTrueInt.Draw('hist same')
h_nTrueInt_rw.Draw('hist same')
legend.Draw()
c.Draw()
c.SaveAs(f'./plots/nTrueInt_{era}.png')
c.SaveAs(f'./plots/nTrueInt_{era}.pdf')
