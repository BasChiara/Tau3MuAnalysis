import ROOT
import numpy as np
import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import mva.config as config
import plots.color_text as ct

debug = False

# systematics sources wich are uncorrelated among categories 
sys_sources = {
    'mu_mediumID'   : ['tau_mu1_IDrecoSF', 'tau_mu2_IDrecoSF','tau_mu3_IDrecoSF'],
    'NLO'           : ['NLO_weight'],
    'PU'            : ['PU_weight'],
    'mc_stat'       : [''],
    #'HLT_DoubleMu'  : ['tau_DoubleMu4_3_LowMass_SF'],
    'HLT_Tau3Mu'    : ['HLT_isfired_Tau3Mu'],
}

def HLT_Tau3Mu_sys(rdf):

    large_sys = 0.30
    f_fired = rdf.Filter('(HLT_isfired_Tau3Mu) & !(HLT_isfired_DoubleMu)').Count().GetValue() / rdf.Count().GetValue()

    return (f_fired*large_sys + 1)


# build systematics dictionary
def correction_sys(input_file, tree_name, selection):
    
    # parse input file
    rdf = ROOT.RDataFrame(tree_name, input_file).Filter(selection)
    if(debug): print(f'{ct.color_text.BOLD}[+]{ct.color_text.END} entries in the tree: {rdf.Count().GetValue()}')
    print(f'{ct.color_text.BOLD}[+] uncorrelated systematics sources:{ct.color_text.END}')

    sys_dict = {}

    # loop on systematics sources
    for sy_src in sys_sources:
        print(f' > {sy_src}')
        f_up = 1.
        f_down = 1.
        f_tot = 1.
        # MC stat systematics
        if sy_src == 'mc_stat':
            S_nominal = rdf.Count().GetValue()
            f_tot = 1. / np.sqrt(S_nominal) + 1.
        # HLT_Tau3Mu systematics
        elif sy_src == 'HLT_Tau3Mu':
            f_tot = HLT_Tau3Mu_sys(rdf)
        # other systematics
        else:
            if len(sys_sources[sy_src]) > 0:
            
                apply_nominal = f'{sy_src}'
                rdf = rdf.Define(apply_nominal, '*'.join(sys_sources[sy_src]))
                apply_down    = f'{sy_src}_sysDOWN'
                rdf = rdf.Define(apply_down, '*'.join([f'{sf}_sysDOWN' for sf in sys_sources[sy_src]]))
                apply_up      = f'{sy_src}_sysUP' 
                rdf = rdf.Define(apply_up, '*'.join([f'{sf}_sysUP' for sf in sys_sources[sy_src]]) )
            else :
                apply_nominal = sys_sources[sy_src][0]
                apply_down    = f'{apply_nominal}_sysDOWN'
                apply_up      = f'{apply_nominal}_sysUP'

            if(debug) : print (f'   nominal: {apply_nominal} \n   up: {apply_up} \n   down: {apply_down}')
            S_nominal   = rdf.Sum(apply_nominal).GetValue() 
            S_up        = rdf.Sum(apply_up).GetValue()
            S_down      = rdf.Sum(apply_down).GetValue()
            S_delta     = np.abs(S_up - S_down)

            f_up    = S_up / S_nominal
            f_down  = S_down / S_nominal
            f_tot   = S_delta / S_nominal + 1.
        
        sys_dict[sy_src] = {'up': f_up, 'down': f_down, 'total': f_tot}
        print(f'   f_up = {f_up:.4f} \t f_down = {f_down:.4f} \t f_tot = {f_tot:.4f}')
    
    #print(sys_dict)
    return sys_dict
