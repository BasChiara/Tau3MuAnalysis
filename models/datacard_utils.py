import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import mva.config as config

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
    wspace_filename = kwargs['workspace'] if 'workspace' in kwargs else None
    wspace_name     = kwargs['ws_name'] if 'ws_name' in kwargs else 'w'
    datacard_name   = kwargs['datacard_name'] if 'datacard_name' in kwargs else 'datacard.txt'
    year            = kwargs['year'] if 'year' in kwargs else '16'
    cat             = kwargs['cat'] if 'cat' in kwargs else 'cat0'
    signal_model    = kwargs['sig_model'] if 'sig_model' in kwargs else None
    b_model         = kwargs['bkg_model'] if 'bkg_model' in kwargs else None
    bkg_func        = kwargs['bkg_func'] if 'bkg_func' in kwargs else 'expo'
    Nobs            = kwargs['Nobs'] if 'Nobs' in kwargs else 0
    Nsig            = kwargs['Nsig'] if 'Nsig' in kwargs else 0
    Nbkg            = kwargs['Nbkg'] if 'Nbkg' in kwargs else 0
    Ndata           = kwargs['Ndata'] if 'Ndata' in kwargs else 0
    slope           = kwargs['slope'] if 'slope' in kwargs else None
    width           = kwargs['width'] if 'width' in kwargs else None
    write_sys       = kwargs['write_sys']  if 'write_sys' in kwargs else False

    process_name = f'WTau3Mu_{cat}{year}'
    # uncorrelated systematics dictionary
    sys_dict = {}
    sys_sources = []
    shape_sys = {}
    if write_sys:
        # uncorrelated systematics from scale factors
        with open(config.uncorrelated_systematics['20' + year]) as f:
            sys_json = json.load(f)
        sys_dict = sys_json[cat]
        sys_sources = sys_dict.keys()
        f.close()
        # uncorrelated systematics from shape variations
        with open(config.shape_systematics['20' + year]) as f:
            shape_sys = json.load(f)[f'{cat}{year}']
        f.close()
        print(shape_sys)

    

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
            signal   = Nsig, # number of EXPEctED signal events, INCLUDES the a priori normalisation. Combine fit results will be in terms of signal strength relative to this inistial normalisation
            bkg      = Nbkg, # number of expected background events **over the full mass range** using the exponential funciton fitted in the sidebands 
        )
        )

    # ------- SYSTEMATICS -------
        #correlated systematics
        card.write(
'lumi{yy}             lnN           {Lsys}               -\n'.format(
            Lsys     = config.Lumi_systematics['20'+year],          # luminosity uncertainty
            yy       = year
        )
        )
        # uncorrelated systematics
        # **SF**
        for sys in sys_sources:
            card.write(
'{systematic_name}_{c}{yy}   lnN    {sys_up:.4f}/{sys_down:.4f}   -\n'.format(
                proc = process_name,
                yy = year,
                c = cat,
                systematic_name = sys,
                sys_up = sys_dict[sys]['up'],
                sys_down = sys_dict[sys]['down']
                )
            )
        # **SIGNAL**
        if write_sys:
            
            card.write(
'width_{c}{yy}       param  {val:.4f} {err:.4f}'.format(
                c = cat,
                yy = year,
                val = width.getVal(),
                err = width.getVal() * shape_sys['width']
            )
            )
        # **BACKGROUND**
        card.write(
        '''
bkgNorm_{c}{yy}       rateParam     {proc}              bkg      1.      [{bkg_lo:.2f},{bkg_hi:.2f}]
bkgNorm_{c}{yy}       flatParam
{activator}slope_{c}{yy}        param  {slopeval:.4f} {slopeerr:.4f}
        '''.format(
                proc     = process_name,
                c        = cat,
                yy       = year,
                bkg_lo   = bkg_norm_lo,
                bkg_hi   = bkg_norm_hi, 
                activator = '' if bkg_func == 'expo' else '#',
                slopeval = slope.getVal(),
                slopeerr = slope.getError()
            )
        )
    print(f'Written datacard: {datacard_name}')
    return 0
