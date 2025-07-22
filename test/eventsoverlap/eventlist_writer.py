import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as config


infile = config.mc_bdt_samples['WTau3Mu']
intree = 'tree_w_BDT'
rdf = ROOT.RDataFrame(intree, infile)

col_tosave = [
    'run',
    'event',
    'LumiBlock',
    'year_id',
    'tau_fit_eta',
    'tau_fit_mass',
]

year = 23
outdir = '.'

base_selection      = ' & '.join([
    config.base_selection,
    config.phi_veto,
    config.displacement_selection,
    config.year_selection["20"+str(year)],
])
print(f'[i] Base selection: {base_selection}')

bdt_selection = ' | '.join([
    f'(({config.cat_eta_selection_dict["A"]}) & (bdt_score > {config.wp_dict[str(year)]["A"]}))',
    f'(({config.cat_eta_selection_dict["B"]}) & (bdt_score > {config.wp_dict[str(year)]["B"]}))',
    f'(({config.cat_eta_selection_dict["C"]}) & (bdt_score > {config.wp_dict[str(year)]["C"]}))',
])
print(f'[i] BDT selection: {bdt_selection}')
total_selection = f'({base_selection}) & ({bdt_selection})'

rdf = rdf.Define('tau_fit_absEta', 'fabs(tau_fit_eta)').Filter(total_selection)
print(f'[i] events after selection: {rdf.Count().GetValue()}')

# write the event numbers to a csv file
nprdf = pd.DataFrame( rdf.AsNumpy(columns=col_tosave))
print(f'[i] Number of events: {len(nprdf)}')
print(nprdf.head())
outfile = os.path.join(outdir, f'eventlist_{year}.csv')
if os.path.exists(outfile):
    os.remove(outfile)
nprdf.to_csv(outfile, index=False)
print(f'[i] Event list written to {outfile}')
