import ROOT
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import numpy as np
import glob
import cmsstyle as CMS
CMS.SetExtraText("Simulation Preliminary")
CMS.SetEnergy("13.6")


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

#YEAR_ = '2022'
YEAR_ = '2023'
CMS.SetLumi(YEAR_, unit = "")

infile = glob.glob(f'../../outRoot/WTau3Mu_MCanalyzer_{YEAR_}*_HLT_overlap_onTau3Mu.root')
intree = "WTau3Mu_tree"
#outdir = "$WWW/Tau3Mu_Run3/MCstudies/2022preEE/"
outdir = "."

if not os.path.exists(outdir):
    os.makedirs(outdir)
    print("[INFO] Output directory created: ", outdir)
if isinstance(infile, list):
    for f in infile:
        if not os.path.exists(f):
            print("[ERROR] Input file does not exist: ", f)
            sys.exit(1)
        else:
            print(" [+] ", f)
else:
    if not os.path.exists(infile):
        print("[ERROR] Input file does not exist: ", infile)
        sys.exit(1)
    else:
        print(" [+] ", infile)

rdf = ROOT.RDataFrame(intree, infile)
# define different isolation varying delta beta
dBeta = [0.05, 0.10, 0.15, 0.30]
for dB in dBeta:
    print(f"[INFO] Defining isolation with Δβ = {dB}")
    rdf = rdf.Define(f'tau_relIso_dB' + str(dB).replace('.', 'p'), f'(tau_Iso_chargedDR04+std::max(0.0,tau_Iso_photonDR04-{dB}*(tau_Iso_puDR08)))/tau_fit_pt')


# efficiency VS pileup
colors = [ROOT.kBlack, ROOT.kCyan, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta]
to_plot = {
    'Iso_eff' :
        {
            'type': 'efficiency',
            'title': '',
            'xaxis': 'PVs',
            'yaxis': 'Efficiency',
            'variable': 'nGoodPV',
            'bins' : [10, 14, 16, 18 , 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 60],
            'yrange': (0, 1.3),
            'num' : '(tau_relIso < 0.2)',
            'sel': ['(isMCmatching)'],
            'legend': ['MC truth'],
            'logy': False,
        },
    'fakeRate_eff' :
        {
            'type': 'efficiency',
            'title': '',
            'xaxis': 'PVs',
            'yaxis': 'Fake Rate',
            'variable': 'nGoodPV',
            'bins' : [10, 14, 16, 18 , 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 60],
            'yrange': (0, 0.06),
            'num' : '(!isMCmatching)',
            'sel': ['(1)',
                    '(tau_relIso < 0.15)',
                    #'(tau_relIso > 0.15)',
                    '(tau_relIso_dB0p05 < 0.15)',
                    '(tau_relIso_dB0p1 < 0.15)',
                    '(tau_relIso_dB0p15 < 0.15)',
                    '(tau_relIso_dB0p3 < 0.15)',
                    ],
            'legend': [
                'inclusive',
                '#Delta#beta = 0.20 Irel < 0.15', 
                '#Delta#beta = 0.05 Irel < 0.15',
                '#Delta#beta = 0.10 Irel < 0.15',
                '#Delta#beta = 0.15 Irel < 0.15',
                '#Delta#beta = 0.30 Irel < 0.15',
                       ],
            'logy': False,
        },
}



for obs in to_plot:
    nbins, bins = len(to_plot[obs]['bins']) - 1, np.array(to_plot[obs]['bins'], dtype=float)
    var = to_plot[obs]['variable']

    c = CMS.cmsCanvas(
        f'{obs}_canvas',
        x_min = bins[0], x_max = bins[-1],
        y_min = to_plot[obs]['yrange'][0], y_max = to_plot[obs]['yrange'][1],
        nameXaxis = to_plot[obs]['xaxis'],
        nameYaxis = to_plot[obs]['yaxis'],
        square=True,
        iPos=11,
        extraSpace=0.03,
    )
    legend = ROOT.TLegend(0.55, 0.15, 0.90, 0.50)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    h_list = []
    for i, s in enumerate(to_plot[obs]['sel']):
        
        data = rdf.Filter(s)
        h_den = data.Histo1D((obs + '_den', obs + '_den', nbins, bins), var, 'weight').GetValue()
        h_num = data.Filter(to_plot[obs]['num']).Histo1D((obs + '_num', obs + '_num', nbins, bins), var, 'weight').GetValue()

        if not h_den or not h_num:
            print(f"[ERROR] No data for selection: {s} in {obs}")
            exit(1)

        h_den.Sumw2()
        h_num.Sumw2()
        h_eff = h_num.Clone(obs + '_eff')
        h_eff.Divide(h_den)
        h_eff.SetDirectory(0)
        
        legend.AddEntry(h_eff, 
                        to_plot[obs]['legend'][i] if to_plot[obs]['legend'] else f'{s}',
                        'l')
        
        h_list.append(h_eff)
    
    for i, h in enumerate(h_list): 
        CMS.cmsDraw(
            h,
            style = 'PE' + (' same' if i > 0 else ''),
            marker=20,
            msize=1.2,
            mcolor=colors[i],
            lstyle=ROOT.kSolid,
            lwidth=2,
            lcolor=colors[i],
            fstyle=0,
            fcolor=0,
        )
        if (len(h_list)> 1) : legend.Draw()
    
    CMS.SaveCanvas(c, os.path.join(outdir, obs + f'_{YEAR_}.png'), False)
    CMS.SaveCanvas(c, os.path.join(outdir, obs + f'_{YEAR_}.pdf'), True)