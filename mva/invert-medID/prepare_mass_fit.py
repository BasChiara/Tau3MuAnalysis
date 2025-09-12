import ROOT
ROOT.gROOT.SetBatch(True)

import numpy as np
import os, sys
from sys import argv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import mva.config as cfg


if __name__ == '__main__':
    '''
    usage : python prepare_mass_fit.py <input_file> <output_file>
    '''

    input_file = str(argv[1])
    treename = 'tree_w_BDT'
    output_file = str(argv[2])

    # -- SETTINGS -- #
    mass = 'tau_fit_mass'
    nbins, low, high = 65, 1.40, 2.05
    categories = ['ABC', 'A', 'B', 'C']
    bdt_cuts   = np.linspace(0.980, 0.999, 20)  # 10 bins between 0.98 and 1.0
    print(f"[i] BDT cuts: {bdt_cuts}")

    # -- INPUT -- #
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    print(f"[+] Input file: {input_file}")
    rdf = ROOT.RDataFrame(treename, input_file).Filter('(is_dataSB == 0)')

    
    # -- OUTPUT -- #
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    out_f = ROOT.TFile(output_file, 'RECREATE')
    print(f"[OUT] Output file: {output_file}")
    for cat in categories:
        print(f"\n[>>>] Processing category: {cat}")
        cat_selection = cfg.cat_eta_selection_dict_fit[cat]
        for bdt in bdt_cuts:
            print(f"   --- BDTscore > {bdt:.3f}")
            bdt_selection = f'(bdt_score > {bdt:.3f})'
            selection = '&'.join([cat_selection, bdt_selection])

            h_mass = rdf.Filter(selection).Histo1D(
                (f'h_mass_{cat}_BDT{bdt:.3f}', f'Tau mass in cat {cat} with BDT > {bdt:.3f}; m_{{3#mu}} [GeV]; Events / {(high-low)/nbins:.3f} GeV', 
                nbins, low, high), 
                mass, 'weight')
            h_mass.Write()
            print(f"   [i] Histogram saved: {h_mass.GetName()}")
            

