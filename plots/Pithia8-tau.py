import ROOT
ROOT.gROOT.SetBatch(True)

import plotting_tools as pt

import sys, os


genLevel_histo = {
    'Wtaunu' :{
        'label': 'W #rightarrow #tau#nu',
        'color' : ROOT.kGreen+2,
        'lstyle': ROOT.kSolid,
        'xaxis': 'p_{T}^{#tau} (GeV)',
        'tonorm': True,
        'bins' : 
        [
            [2.00, 79.54],
            [6.00, 245.80],
            [10.00,	368.32],
            [14.00,	547.71],
            [18.00,	683.35],
            [22.00,	847.43],
            [26.00,	1059.63],
            [30.00,	1140.58],
            [34.00,	1470.92],
            [38.00,	1593.44],
            [42.00,	961.19],
            [46.00,	414.26],
            [50.00,	215.18],
            [54.00,	112.35],
            [58.00,	75.16],
            [62.00,	51.10],
            [66.00,	31.41],
            [70.00,	24.01],
            #[74.00,	22.66],
            #[78.00,	13.91],
            #[82.00,	15.28],
            #[86.00,	8.73],
            #[90.00,	6.55],
            #[94.00,	8.73],
            #[98.00,	10.91],
        ]
    },
    'Dtaunu' :{
        'label' : 'D #rightarrow #tau#nu',
        'color' : ROOT.kRed+1,
        'lstyle': ROOT.kSolid,
        'xaxis': 'p_{T}^{#tau} (GeV)',
        'tonorm': False,
        'bins' :[
            [0.375, 0.1654],
            [1.125, 0.2700],
            [1.875, 0.2107],
            [2.625, 0.1358],
            [3.375, 0.0838],
            [4.125, 0.0505],
            [4.875, 0.0305],
            [5.625, 0.0179],
            [6.375, 0.0117],
            [7.125, 0.0071],
            [7.875, 0.0043],
            [8.625, 0.0031],
            [9.375, 0.0015],
            [10.125, 0.0007],
            [10.875, 0.0006],
            [11.625, 0.0006],
            [12.375, 0.0001],
            [13.125, 0.]
        ],
    },
    'Btaunu' :{
        'label' : 'B #rightarrow #tau X',
        'color':  ROOT.kBlue+1,
        'lstyle': ROOT.kSolid,
        'xaxis': 'p_{T}^{#tau} (GeV)',
        'tonorm': False,
        'bins' :[
            [0.375	, 0.1314],
            [1.125	, 0.2524],
            [1.875	, 0.2115],
            [2.625	, 0.1453],
            [3.375	, 0.0925],
            [4.125	, 0.0577],
            [4.875	, 0.0367],
            [5.625	, 0.0228],
            [6.375	, 0.0144],
            [7.125	, 0.0094],
            [7.875	, 0.0066],
            [8.625	, 0.0039],
            [9.375	, 0.0023],
            [10.125,    0.0010],
            [10.875, 	0.0015],
            [11.625, 	0.0014],
            [12.375, 	0.0006], 
            [13.125, 0.]
        ],
    },
}




def plot_pithia8_tau():
    ROOT.gStyle.SetOptStat(0)
    outpath = os.path.expandvars('$WWW/Tau3Mu_Run3/MCstudies/')
    text = ROOT.TLatex(0.6, 0.85, "PYTHIA8 LO")
    text.SetNDC()
    text.SetTextSize(0.04)
    text.SetTextFont(42)

    histo_to_plot = []
    leg_entries = []
    for channel in genLevel_histo.keys():

        settings = genLevel_histo[channel]

        bins = [bin[0] for bin in settings['bins']]
        vals = [bin[1] for bin in settings['bins']]
        binw = bins[1] - bins[0]
        nbins = len(bins) +1
        print(f' > channel {channel} with {nbins} bins of width {binw}')
        print(f' > bins: {bins}')
    
        histo = ROOT.TH1F(f"histo_{channel}", "", len(bins), bins[0] - binw, bins[-1] + binw)
        for i, bin in enumerate(bins):
            histo.SetBinContent(i+1, vals[i])
        histo.SetLineColor(settings['color'])
        histo.SetLineWidth(2)
        histo.GetXaxis().SetTitle(settings['xaxis'])
        if settings['tonorm']:
            histo.Scale(1.0 / histo.Integral())
        histo.GetYaxis().SetTitle("a.u.")
        histo.SetLineStyle(settings['lstyle'])
        
        histo_to_plot.append(histo)
        leg_entries.append(settings['label'])

    pt.plot_CMSstle(
      histo_to_plot,
      description=leg_entries, 
      leg_coord=[0.60, 0.65, 0.90, 0.80],
      to_ploton=[text],
      file_name=os.path.join(outpath, f'Pithia8_tau3mu_genLevel_tauPt'),
      y_lim = (0, histo.GetMaximum()*1.4),
      CMSextraText = "Preliminary",
      isMC = True,
      yesr = '2022+2023'
    )


if __name__ == "__main__":
    plot_pithia8_tau()
