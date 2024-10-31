import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
import numpy as np

def SF_2DmapTo1Dgraph(h_2Dmap) :
    x_pt  = []
    x_lim = []
    y_vec = []
    y_err = []
    sf_vec = []
    y_vec_tmp = []
    y_err_tmp = []
    sf_vec_tmp = []

    min_x = -1.
    max_x = -1.
    for bin in h_2Dmap.GetBins() :
        if (False) : 
            print(" > bin %d eta [%.1f, %.1f] pT [%.1f, %.1f] sf = %.3f "%( bin.GetBinNumber(), bin.GetXMin(), bin.GetXMax(), bin.GetYMin(), bin.GetYMax(), bin.GetContent()))

        is_new_Xbin = ( bin.GetXMin() != min_x) or (bin.GetXMax() != max_x)
        if is_new_Xbin :
            # relese the previous set, if any
            if sf_vec_tmp:
                y_vec.append(y_vec_tmp)
                y_err.append(y_err_tmp)
                sf_vec.append(sf_vec_tmp)
                x_lim.append([min_x, max_x])
                x_pt.append( (min_x + max_x)/2. )

            # start new set
            min_x   = bin.GetXMin() 
            max_x   = bin.GetXMax()
            y_vec_tmp = []
            y_err_tmp = []
            sf_vec_tmp = []


        #update the already existing set
        y_vec_tmp.append((bin.GetYMax() + bin.GetYMin())/2) 
        y_err_tmp.append((bin.GetYMax() - bin.GetYMin())/2)
        sf_vec_tmp.append(bin.GetContent())
    y_vec.append(y_vec_tmp)
    y_err.append(y_err_tmp)
    sf_vec.append(sf_vec_tmp)
    x_lim.append([min_x, max_x])
    x_pt.append( (min_x + max_x)/2. )
    return x_pt, x_lim, y_vec, y_err, sf_vec

def SF_2Dmap_with_sys(h_2Dval, h_2Dup, h_2Ddown, output_file):
    h_2Dmap_error = ROOT.TH2Poly()#= h_2Dval.Clone('h_2Dmap_error')
    h_2Dmap_error.ClearBinContents()
    #h_2Dmap_error.GetYaxis().SetRangeUser(0,20)
    for bin in h_2Dval.GetBins() :
        if (True) : 
            print(" > bin %d eta [%.1f, %.1f] pT [%.1f, %.1f] sf = %.3f "%( bin.GetBinNumber(), bin.GetXMin(), bin.GetXMax(), bin.GetYMin(), bin.GetYMax(), bin.GetContent()))
        h_2Dmap_error.AddBin(
            bin.GetXMin(), bin.GetYMin(),
            bin.GetXMax(), min(15, bin.GetYMax()),
        )
        bin_number = bin.GetBinNumber()
        h_2Dmap_error.SetBinContent(bin_number, h_2Dval.GetBinContent(bin_number))
        error = max(abs(h_2Dup.GetBinContent(bin_number) - h_2Dval.GetBinContent(bin_number)), abs(h_2Ddown.GetBinContent(bin_number) - h_2Dval.GetBinContent(bin_number)))
        h_2Dmap_error.SetBinError(bin_number, error)
        ROOT.gStyle.SetPaintTextFormat('.3f')
        h_2Dmap_error.GetYaxis().SetTitle('p_{T} [GeV]')
        h_2Dmap_error.GetXaxis().SetTitle('|#eta|')
        h_2Dmap_error.GetZaxis().SetRangeUser(0.9, 1.1)
    
    #draw the 2D map
    c = ROOT.TCanvas("c", "", 800, 800)
    c.cd()
    ROOT.gPad.SetMargin(0.15, 0.15, 0.15, 0.15)
    h_2Dmap_error.SetTitle('')
    h_2Dmap_error.Draw('colz texte')
    c.SaveAs(output_file+'.png')
    c.SaveAs(output_file+'.pdf')


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_root', default='/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/Run2_ntuples/WTau3Mu_MC2017.root')
#parser.add_argument('--tree',       default='WTau3Mu_tree')
parser.add_argument('--outdir',     default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/MCstudies/2017/', help=' output directory for plots')
parser.add_argument('--tag',        default= 'medium vs low pT ', help='tag to the training')
parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
parser.add_argument('--category',   default = 'noCat')

args = parser.parse_args()
tag  = args.tag

# -- read inputs
try:
    infile = ROOT.TFile.Open(args.input_root)
except:
    print(f' [+] error cannot open {args.input_root}')
else:
    h_SFlowPt = infile.Get(f'h_NUM_MediumID_DEN_TrackerMuons_{args.tag}_low_val')
    h_SFlowPt.SetDirectory(0)
    hSFlowPt_up = infile.Get(f'h_NUM_MediumID_DEN_TrackerMuons_{args.tag}_low_sUP')
    hSFlowPt_up.SetDirectory(0)
    hSFlowPt_down = infile.Get(f'h_NUM_MediumID_DEN_TrackerMuons_{args.tag}_low_sDOWN')
    hSFlowPt_down.SetDirectory(0)
    h_SFmedPt = infile.Get(f'h_NUM_MediumID_DEN_TrackerMuons_{args.tag}_medium_val')

SF_2Dmap_with_sys(h_SFlowPt, hSFlowPt_up, hSFlowPt_down, '%s/SFmediumID_lowPt_%s'%(args.outdir, tag))
exit()
c = ROOT.TCanvas("c", "", 800, 800)
legend = ROOT.TLegend(0.60, 0.70, 0.80, 0.85)
legend.SetBorderSize(0)
legend.SetTextSize(0.035)

eta_pt_lowpT, eta_lim_lowpT, pT_vec_lowpT, pT_err_lowpT, sf_val_lowpT = SF_2DmapTo1Dgraph(h_SFlowPt)
eta_pt_medpT, eta_lim_medpT, pT_vec_medpT, pT_err_medpT, sf_val_medpT = SF_2DmapTo1Dgraph(h_SFmedPt)

for i, eta  in enumerate(eta_pt_lowpT):

    eta_binning = '%.1f < |$\eta$| < %.1f'%(eta_lim_lowpT[i][0], eta_lim_lowpT[i][1])
    print('- save TGraph for eta bin %s '%eta_binning)
    gr_low = ROOT.TGraphErrors(len(pT_vec_lowpT[i]), 
                                    np.array(pT_vec_lowpT[i],dtype=float), 
                                    np.array(sf_val_lowpT[i], dtype=float),
                                    np.array(pT_err_lowpT[i], dtype=float),
                                    np.zeros(len(sf_val_lowpT[i])))
    gr_med = ROOT.TGraphErrors(len(pT_vec_medpT[i]), 
                                    np.array(pT_vec_medpT[i],dtype=float), 
                                    np.array(sf_val_medpT[i], dtype=float),
                                    np.array(pT_err_medpT[i], dtype=float),
                                    np.zeros(len(sf_val_medpT[i])))
    gr_low.SetMarkerStyle(20)
    gr_low.SetMarkerSize(1.)
    gr_low.SetLineWidth(2)
    gr_low.SetLineColor(ROOT.kBlue)
    gr_low.SetMarkerColor(ROOT.kBlue)
    gr_low.SetMaximum(1.2) 
    gr_low.SetMinimum(0.8)
    gr_low.GetXaxis().SetLimits(0, 50) 
    gr_med.SetMarkerStyle(20)
    gr_med.SetMarkerSize(1.1)
    gr_med.SetLineWidth(2)
    gr_med.SetLineColor(ROOT.kRed)
    gr_med.SetMarkerColor(ROOT.kRed)
    legend.Clear()
    legend.SetHeader(eta_binning)
    legend.AddEntry(gr_low, "MediumID J/#psi")
    legend.AddEntry(gr_med, "MediumID Z")
    c.cd()

    gr_low.Draw('AP')
    #gr_med.Draw('P')   
    legend.Draw()
    
    
    x_tag = "eta_%.1f_%.1f"%(eta_lim_lowpT[i][0], eta_lim_lowpT[i][1])
    c.SaveAs('%s/SFmediumID_%s_%s.png'%(args.outdir, x_tag, tag))
    c.SaveAs('%s/SFmediumID_%s_%s.pdf'%(args.outdir, x_tag, tag))
