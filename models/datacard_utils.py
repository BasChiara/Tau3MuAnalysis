import os
import json
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from style.color_text import color_text as ct
import mva.config as config
import corrections.corrections_sys as corr_sys

# Clopper Pearson intervals
from statsmodels.stats.proportion import proportion_confint
def cp_intervals(Nobs, Ntot, cl=0.68, verbose = False):

    # 'beta' returns the lower and upper bounds for the binomial proportion (= efficiency)
    eff = 1.*Nobs/Ntot
    lo, hi = proportion_confint(Nobs, Ntot, 1.-cl, method='beta')

    lor = lo/eff if eff else -99
    hir = hi/eff if eff else -99
    if verbose :
        print('-- Clopper Pearson --')
        print('\n'.join([
        'Ntot:  {T}','Nobs:  {O}','eff:  {E}','low:  {L}','high:  {H}'
        ]).format(T=Ntot, O=Nobs, E=eff, L=lo, H=hi))

    return lor, hir

def weight_systematics(sys1, sys2, weight):
    return (1 + np.sqrt(((sys1 - 1) * weight)**2 + ((sys2 - 1)*(1-weight))**2))

    
def fully_correlated_sys_writer(card, W_f, kwargs):
    process_name  = kwargs['process_name'] if 'process_name' in kwargs else 'wt3m'
    year = kwargs['year'] if 'year' in kwargs else '16'

    if 'W' in process_name or 'w' in process_name:
        card.write(
'''lumi_13p6TeV_{yyyy}             lnN           {Lsys}               -
xsec_13p6TeV_ppwx           lnN           {xsec_ppWx}               -
BR_wmn              lnN           {Br_Wmunu}               -
BR_wtn              lnN           {Br_Wtaunu}               -
'''.format(
            Lsys     = config.Lumi_systematics['20'+year],          # luminosity uncertainty
            yyyy     = year,
            xsec_ppWx= config.xsec_ppW_sys,         # pp->Wx cross section uncertainty
            Br_Wmunu = config.Br_Wmunu_sys,         # W->munu branching ratio uncertainty
            Br_Wtaunu= config.Br_Wtaunu_sys         # W->taunu branching ratio uncertainty
        )
        )
    elif 'V' in process_name or 'v' in process_name:
        card.write(
'''lumi_13p6TeV_{yyyy}             lnN           {Lsys}               -
xsec_13p6TeV_ppvx             lnN           {xsec_ppWx:.4f}               -
BR_vmn             lnN           {Br_Wmunu:.4f}               -
BR_vtn             lnN            {Br_Wtaunu:.4f}               -
'''.format(
            Lsys     = config.Lumi_systematics['20'+year],          # luminosity uncertainty
            yyyy     = '20'+year,
            xsec_ppWx= weight_systematics(config.xsec_ppW_sys,  config.xsec_ppZ_sys,   W_f),         # pp->Wx cross section uncertainty
            Br_Wmunu = weight_systematics(config.Br_Wmunu_sys,  config.Br_Zmumu_sys,   W_f),         # W->munu branching ratio uncertainty
            Br_Wtaunu= weight_systematics(config.Br_Wtaunu_sys, config.Br_Ztautau_sys, W_f),        # W->taunu branching ratio uncertainty
        )
        )



def combineDatacard_writer(**kwargs):
    # needed arguments
    process_name    = kwargs['process_name'] if 'process_name' in kwargs else 'wt3m'
    input_mc        = kwargs['input_mc'] if 'input_mc' in kwargs else None
    selection_mc    = kwargs['selection'] if 'selection' in kwargs else None
    wspace_filename = kwargs['ws_filename'] if 'ws_filename' in kwargs else None
    workspace       = kwargs['workspace'] if 'workspace' in kwargs else None
    datacard_name   = kwargs['datacard_name'] if 'datacard_name' in kwargs else 'datacard.txt'
    year            = kwargs['year'] if 'year' in kwargs else '16'
    cat             = kwargs['cat'] if 'cat' in kwargs else 'cat0'
    bkg_func        = kwargs['bkg_func'] if 'bkg_func' in kwargs else 'expo'
    Nobs            = kwargs['Nobs'] if 'Nobs' in kwargs else 0
    Nsig            = kwargs['Nsig'] if 'Nsig' in kwargs else 0
    Nbkg            = kwargs['Nbkg'] if 'Nbkg' in kwargs else 0
    Ndata           = kwargs['Ndata'] if 'Ndata' in kwargs else 0
    write_sys       = kwargs['write_sys']  if 'write_sys' in kwargs else False

    cat_yyyy = f'{cat}_20{year}'

    # get S and B model from workspace
    if not workspace:
        print(f'{ct.RED}[ERROR]{ct.END} NO workspace provided')
        return 1
    wspace_name = workspace.GetName()
    
    
    # -- signal -- #
    signal_model = workspace.pdf(f'model_sig_{process_name}')
    if not signal_model:
        print(f'{ct.RED}[ERROR]{ct.END} NO signal model found in the workspace')
        return 1
    width_list = []
    WZ_ratio = 1.0
    if 'W' in process_name or 'w' in process_name:
        width_list.append( signal_model.getVariables().find(f'signal_width_{cat_yyyy}') )
    elif 'V' in process_name or 'v' in process_name:
        width_list.append( signal_model.getVariables().find(f'signal_width_W_{cat_yyyy}') )
        width_list.append( signal_model.getVariables().find(f'signal_width_Z_{cat_yyyy}') )
        WZ_ratio = signal_model.getVariables().find(f'r_wz_{cat_yyyy}').getVal()
    
    # -- background -- #
    b_model = workspace.pdf(f'model_bkg_{process_name}')
    print(f'[B] B function : {bkg_func}')
    if not b_model:
        print(f'{ct.RED}[ERROR]{ct.END} NO background model found in the workspace')
        return 1
    if bkg_func == 'expo' : 
        slope = b_model.getVariables().find(f'background_slope_{cat_yyyy}')
        if not slope:  print(f'{ct.RED}[ERROR]{ct.END} NO background slope found in the workspace')
    elif bkg_func == 'poly1': slope = b_model.getVariables().find(f'p1_{cat_yyyy}')
    else :  slope = None
    print(slope)
    
    # uncorrelated systematics dictionary
    sys_dict = {}
    sys_sources = []
    shape_sys = {}

    if write_sys:
        # uncorrelated systematics from scale factors 
        sys_dict = corr_sys.correction_sys(input_mc, 'tree_w_BDT', selection_mc, cat, year)
        # uncorrelated sys for LxyS cut 
        with open(config.LxySign_cut_systematics['20'+year]) as f:
            sys_dict['LxyS_cut'] = json.load(f)[f'{cat}']
        sys_sources = sys_dict.keys()
        
        # uncorrelated systematics from shape variations
        with open(config.shape_systematics['20'+year]) as f:
            shape_sys = json.load(f)[f'{cat}{year}']
        f.close()
    

    # background normalization systematic --> make bkg normalization a nuisance parameter 
    #   floating in an interval marked by Clopper Pearson distribution for binomial proportion confidence level
    #   signal strenght for bkg normalizaion varies around 1.0 
    #   within an interval covering 99% CL of efficiency p.d.f. in counting experiment
    bkg_norm_lo, bkg_norm_hi = cp_intervals(Nobs =Nbkg, Ntot= Ndata, cl = 0.99, verbose = False)

    # write the datacard
    with open(datacard_name, 'w') as card:
        # ------- S and B YIELD and WORKSPACES -------
        card.write(
'''
imax 1 number of channels
jmax * number of background sources
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes bkg         {proc}       ./{ws_file} {ws_name}:{bkg_model}
shapes sig         {proc}       ./{ws_file} {ws_name}:{sig_model}
shapes data_obs    {proc}       ./{ws_file} {ws_name}:data_obs
--------------------------------------------------------------------------------
bin                {proc}
observation        {obs:d}
--------------------------------------------------------------------------------
bin                              {proc}         {proc}
process                          sig                 bkg
process                          0                   1
rate                             {signal:.4f}              {bkg:.4f}
--------------------------------------------------------------------------------
'''.format(
            proc     = process_name, 
            ws_file  = os.path.basename(wspace_filename), 
            ws_name  = wspace_name, 
            bkg_model= b_model.GetName(),
            sig_model= signal_model.GetName(),
            obs      = Nobs, # number of observed events
            signal   = Nsig, # number of EXPECTED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
            bkg      = Nbkg, # number of expected background events **over the full mass range** using the exponential funciton fitted in the sidebands 
        )
        )

    # ------- SYSTEMATICS -------
        #fully correlated
        fully_correlated_sys_writer(card, WZ_ratio, kwargs) 
        
        # uncorrelated
        # **SF**
        for sys in sys_sources:
            card.write(
'{systematic_name}{corr_deg}       lnN           {sys_tot:.3f}               -\n'.format(
                systematic_name = sys,
                corr_deg = '_' + sys_dict[sys]['corregree'] if sys_dict[sys]['corregree'] else '',
                sys_tot = sys_dict[sys]['total']
                )
            )
        # **SIGNAL**
        if write_sys:
            for width in width_list:
                width_error = np.sqrt(width.getError()**2 + (width.getVal()*shape_sys['width'])**2)
                card.write(
'{width_name}         param          {val:.4f}     {err:.4f}\n'.format(
                    width_name  = width.GetName(),
                    val         = width.getVal(),
                    err         = np.max([1e-4, width_error])
                )
                )
                print(f' width = {width.getVal():.5f} +/- {width.getError():.5f}(fit) +/- {width_error:.5f}(sys+fit)')
        # **BACKGROUND**
        card.write(
'''
bkg_scale_v_{c}_{yyyy}       rateParam     {proc}              bkg      1.      [{bkg_lo:.2f},{bkg_hi:.2f}]
bkg_scale_v_{c}_{yyyy}       flatParam
'''.format(
                proc     = process_name,
                c        = cat,
                yyyy     = '20' + year if not year.startswith('20') else year,
                bkg_lo   = bkg_norm_lo,
                bkg_hi   = bkg_norm_hi, 
            )
        )
        if slope:
            card.write(
'{slope_name}         param  {slopeval:.4f} {slopeerr:.4f}'.format(
                slope_name = slope.GetName(),
                slopeval   = slope.getVal(),
                slopeerr   = slope.getError()
                )
            )
    print(f'Written datacard: {datacard_name}')
    return 0
