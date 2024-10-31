import os
import json
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
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



def combineDatacard_writer(**kwargs):
    # needed arguments
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

    # get S and B model from workspace
    if not workspace:
        print('No workspace provided')
        return 1
    wspace_name = workspace.GetName()
    process_name = f'WTau3Mu_{cat}{year}'
    # -- signal -- #
    signal_model = workspace.pdf(f'model_sig_{process_name}')
    if not signal_model:
        print('No signal model found in the workspace')
        return 1
    width = signal_model.getVariables().find(f'width_{cat}{year}')
    # -- background -- #
    b_model = workspace.pdf(f'model_bkg_{process_name}')
    print(f'[B] B function : {bkg_func}')
    if not b_model:
        print('No background model found in the workspace')
        return 1
    if bkg_func == 'expo' : 
        slope = b_model.getVariables().find(f'slope_{cat}{year}')
    elif bkg_func == 'poly1': slope = b_model.getVariables().find(f'p1_{cat}{year}')
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
        with open(config.LxySign_cut_systematics[f'20{year}']) as f:
            sys_dict['LxyS_cut'] = json.load(f)[f'{cat}']
        sys_sources = sys_dict.keys()
        
        # uncorrelated systematics from shape variations
        with open(config.shape_systematics['20' + year]) as f:
            shape_sys = json.load(f)[f'{cat}{year}']
        f.close()
        #print(shape_sys)

    

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
shapes bkg         {proc}       {ws_file} {ws_name}:{bkg_model}
shapes sig         {proc}       {ws_file} {ws_name}:{sig_model}
shapes data_obs    {proc}       {ws_file} {ws_name}:data_obs
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
        #correlated systematics
        card.write(
'''lumi{yy}             lnN           {Lsys}               -
xsec_ppWx           lnN           {xsec_ppWx}               -
Br_Wmunu            lnN           {Br_Wmunu}               -
Br_Wtaunu           lnN           {Br_Wtaunu}               -
'''.format(
            Lsys     = config.Lumi_systematics['20'+year],          # luminosity uncertainty
            yy       = year,
            xsec_ppWx= config.xsec_ppW_sys,         # pp->Wx cross section uncertainty
            Br_Wmunu = config.Br_Wmunu_sys,         # W->munu branching ratio uncertainty
            Br_Wtaunu= config.Br_Wtaunu_sys         # W->taunu branching ratio uncertainty
        )
        )
        # uncorrelated systematics
        # **SF**
        for sys in sys_sources:
            card.write(
'{systematic_name}_{corr_deg}       lnN           {sys_tot:.3f}               -\n'.format(
                systematic_name = sys,
                corr_deg = sys_dict[sys]['corregree'],
                #yy = year,
                #c = cat,
                sys_tot = sys_dict[sys]['total']
                #sys_up = sys_dict[sys]['up'],
                #sys_down = sys_dict[sys]['down']
                )
            )
        # **SIGNAL**
        if write_sys:
            width_error = np.sqrt(width.getError()**2 + (width.getVal()*shape_sys['width'])**2)
            card.write(
'{width_name}         param          {val:.4f}     {err:.4f}'.format(
                width_name  = width.GetName(),
                val         = width.getVal(),
                err         = np.max([1e-4, width_error])
            )
            )
            print(f' width = {width.getVal()} +/- {shape_sys["width"]}')
        # **BACKGROUND**
        card.write(
'''
bkgNorm_{c}{yy}       rateParam     {proc}              bkg      1.      [{bkg_lo:.2f},{bkg_hi:.2f}]
bkgNorm_{c}{yy}       flatParam
'''.format(
                proc     = process_name,
                c        = cat,
                yy       = year,
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
