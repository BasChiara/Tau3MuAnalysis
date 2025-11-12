#############################################
#  code to fit Tau-> 3 Mu signal and bkg   #
#############################################

import ROOT
ROOT.gROOT.SetBatch(True)

import numpy as np
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
import mva.config as cfg
import models.fit_utils as fit_utils
from plots.color_text import color_text as ct

import cmsstyle as CMS
CMS.setCMSStyle()
CMSStyle = CMS.getCMSStyle()

import argparse

def get_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--plot_outdir',default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/SigBkg_models/', help=' output directory for plots')
    parser.add_argument('--tag',        default= 'emulateRun2', help='tag to the training')
    parser.add_argument('--debug',      action = 'store_true' ,help='set it to have useful printout')
    parser.add_argument('--category',   choices=['ABC', 'A', 'B', 'C'],  default = 'ABC', help='which category to select')
    parser.add_argument('--year',       choices=['2022', '2023', 'all'], default = 'all', help='which year to select')
    parser.add_argument('--bdt_cut',    type= float, default = 0.990)
    parser.add_argument('--mu_pair',    choices=['12', '13', '23', 'all'], default = '12')
    parser.add_argument('--resonance',  choices=['phi', 'omega'], default = 'phi', help='which resonance to fit')

    args = parser.parse_args()
    return args

def message_logger(message, logger):
    print(message)
    logger.write(message + '\n')

# --- OPTIMIZE THE VETO WINDOW ---
def optimize_vetoWindow(fitresults = {'x': None, 'nsig':None, 'mean': None, 'width':None}, sigma_min= 0.5, sigma_max=5.0, sigma_step = 0.5, outlog = None, thresold_events = 1.0):

    # build a model for the signal only
    x = fitresults['x']
    N = fitresults['nsig']
    mean = fitresults['mean']
    width = fitresults['width']
    model = ROOT.RooGaussian('signal_only', 'signal_only', x, mean, width)

    best_n_sigma = 0.
    sigma_thresholds = np.linspace(sigma_min, sigma_max, int((sigma_max - sigma_min)/sigma_step) + 1)
    if outlog : message_logger('\n Veto window optimization:', outlog)
    
    for n_sigma in sigma_thresholds:
        region_name = f'sig_region_{n_sigma:.1f}sigma'
        x.setRange(region_name, mean.getVal() - n_sigma*width.getVal(), mean.getVal() + n_sigma*width.getVal())
        res_signal = N.getVal()*(1. - model.createIntegral(
            ROOT.RooArgSet(mumu_mass), 
            ROOT.RooArgSet(mumu_mass), 
            region_name
        ).getValV())
        if outlog : message_logger(f' +/- {n_sigma:.1f} sigma: expected signal = {res_signal:.1f} (efficiency = {res_signal/nsig.getVal()*100:.2f} %)\n', outlog)
        
        # optimal window -> less than 1 expected signal event
        if res_signal < thresold_events:
            best_n_sigma = n_sigma
            if outlog : message_logger(f'  = best veto window found at +/- {best_n_sigma:.1f} sigma\n', outlog)
            break

    return best_n_sigma

# --- DRAW WITH CMS STYLE ---
def draw_cms_style(frame, lumi_args = {'lumi': 1, 'run': 2022}, components = {'data': 'Data', 'fit': 'Fit'}, veto = [0.0, 1000, 0], additionalText= [], outfile = 'fit'):
    CMS.SetLumi(**lumi_args)
    CMS.ResetAdditionalInfo()
    [CMS.AppendAdditionalInfo(txt) for txt in additionalText]
    
    # legend
    legend = CMS.cmsLeg(x1=0.60, y1=0.70, x2=0.90, y2=0.90, textSize = 0.05)
    [legend.AddEntry(frame.findObject(key), components[key], 'PE' if 'data' in key else 'L') for key in components.keys()]
    
    # add line in the veto region
    line_lo = ROOT.TLine(veto[0], 0, veto[0], frame.GetMaximum())
    line_hi = ROOT.TLine(veto[1], 0, veto_hi, frame.GetMaximum())
    legend.AddEntry(line_lo, f'veto #pm {veto[2]:.1f} #sigma', 'L')

    # draw
    canv = CMS.cmsCanvas(
        frame.GetName(),
        x_min=frame.GetXaxis().GetXmin(), x_max=frame.GetXaxis().GetXmax(),
        y_min=1e-5, y_max=frame.GetMaximum()*1.5,
        nameXaxis=frame.GetXaxis().GetTitle(),
        nameYaxis=frame.GetYaxis().GetTitle(),
        square=False,
        extraSpace= 0.05,
        yTitOffset=1.0,
    )
    canv.cd()
    ROOT.TGaxis.SetMaxDigits(3)
    CMS.cmsObjectDraw(frame)
    CMS.cmsDrawLine(line_lo, lcolor=ROOT.kGray+2, lstyle=ROOT.kDashed, lwidth=3)
    CMS.cmsDrawLine(line_hi, lcolor=ROOT.kGray+2, lstyle=ROOT.kDashed, lwidth=3)
    legend.Draw('same')
    CMS.SaveCanvas(canv, outfile+'.png', False)
    CMS.SaveCanvas(canv, outfile+'.pdf', False)

    
    

if __name__ == '__main__':

    # arguments
    args = get_arguments()
    tag = args.tag
    name = {'12': 'Mu1Mu2', '23':'Mu2Mu3', '13':'Mu1Mu3', 'all':'MuMu'}
    decay_label = {'phi': '#phi', 'omega': '#omega'}
    catyyyy = f'{args.category}{args.year}' if args.year != 'all' else f'{args.category}'


    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(True)
    ROOT.TH1.SetDefaultSumw2()

    # **** USEFUL CONSTANT VARIABLES *** #

    ctrl_bdt_lo, ctrl_bdt_hi = 0.00, 0.900


    phi_mass = 1.019 #GeV
    omega_mass = 0.783 #GeV
    rho_mass = 0.770 #GeV
    if args.resonance == 'phi':
        fit_range_lo  , fit_range_hi   = 0.90, 1.16 # GeV
        res_mass = phi_mass
    elif args.resonance == 'omega':
        fit_range_lo  , fit_range_hi   = 0.70, 0.86 # GeV
        res_mass = omega_mass
    binw  = 0.005 if args.resonance == 'phi' else 0.004 # GeV
    nbins = int((fit_range_hi - fit_range_lo)/binw) + ( 1 if args.resonance == 'phi' else 0)



    # ** IMPORT DATA **
    input_tree_name = 'tree_w_BDT'
    data_file = cfg.data_bdt_samples['WTau3Mu'] if args.mu_pair != 'all' else 'data_mumuOS.root'
    data_tree = ROOT.TChain(input_tree_name)
    data_tree.AddFile(data_file)
    if data_tree.GetEntries() == 0:
        print(f'{ct.RED}[ERROR]{ct.END} data tree empty!')
        exit()

    # open a logger
    logger_file = f'{args.plot_outdir}/simulfit_{args.resonance}To{name[args.mu_pair]}_bdt{args.bdt_cut:.3f}_{catyyyy}.log'
    logger = open(logger_file, 'w')
    message_logger(f'\n{"="*30}\n FITTING {args.resonance.upper()}->{name[args.mu_pair]} MASS SPECTRUM \n{"="*30}\n', logger)

    # ** SIGNAL and CONTROL region selection **
    base_selection = '&'.join([
        cfg.cat_eta_selection_dict_fit[args.category],
        cfg.year_selection[args.year] if args.year != 'all' else '(1)',
        ])
    message_logger(f'[INFO] base selection: {base_selection}', logger)
    ctrl_selection = '&'.join([
        base_selection,
        f'(bdt_score > {ctrl_bdt_lo} && bdt_score < {ctrl_bdt_hi})'
        ])
    message_logger(f'[INFO] CONTROL region selection: {ctrl_selection}', logger)
    signal_selection = '&'.join([
        base_selection,
        f'(bdt_score > {args.bdt_cut})'
        ])

    # ** RooFit Variables ** 
    thevars = ROOT.RooArgSet()
    # BDT score
    bdt = ROOT.RooRealVar('bdt_score', 'BDT score'  , 0.0,  1.0, '' )
    thevars.add(bdt)
    weight = ROOT.RooRealVar('weight',    'event weight', 0.0, 10.0, '' )
    # eta
    eta = ROOT.RooRealVar('tau_fit_eta', 'tau eta'  , -5.0,  5.0, '' )
    thevars.add(eta)
    # year ID
    year = ROOT.RooRealVar('year_id', 'year ID'  , 0,  300, '' )
    thevars.add(year)
    # di-muon mass
    if args.mu_pair == 'all':
        ref_var= 'tau_mumuOS_M'
        mass_var = 'tau_mumuOS_fitM'
        mumu_ref  = ROOT.RooRealVar(ref_var,  "m(#mu^{+}#mu^{-})", 0.0, 10.0, 'GeV' )
        mumu_mass = ROOT.RooRealVar(mass_var, "m(#mu^{+}#mu^{-})", fit_range_lo,  fit_range_hi, 'GeV' )

    else :
        ref_var= f'tau_mu{args.mu_pair}_M'
        mass_var = f'tau_mu{args.mu_pair}_fitM'
        mumu_ref = ROOT.RooRealVar(ref_var, cfg.features_NbinsXloXhiLabelLog[ref_var][3], 0.0, 10.0, 'GeV' )
        mumu_mass = ROOT.RooRealVar(mass_var, cfg.features_NbinsXloXhiLabelLog[mass_var][3], fit_range_lo,  fit_range_hi, 'GeV' )
        thevars.add(weight)

    mumu_mass.setRange('fit_range', fit_range_lo, fit_range_hi)
    thevars.add(mumu_ref)
    thevars.add(mumu_mass)

    # ** IMPORT DATASET **
    datactrl = ROOT.RooDataSet('datactrl', 'datactrl', data_tree, thevars, ctrl_selection)
    datactrl = datactrl.reduce(ROOT.RooArgSet(mumu_mass))
    datasig = ROOT.RooDataSet('data', 'data', data_tree, thevars, signal_selection)
    datasig = datasig.reduce(ROOT.RooArgSet(mumu_mass))
    print(f'\n {ct.GREEN}[INFO]{ct.END} dataset to fit, entries = {datasig.numEntries()}')
    datasig.Print('v')
    if datasig.numEntries() == 0:
        print(f'{ct.RED}[ERROR]{ct.END} dataset to fit empty!')
        logger.write('ERROR: dataset to fit empty!\n')
        logger.close()
        exit()

    # ** BUILD THE MODEL **
    # shared signal params
    M_mumu   = ROOT.RooRealVar('M_mumu' , 'M_{#mu#mu}' , res_mass, res_mass - 0.002, res_mass + 0.002)
    width  = ROOT.RooRealVar('width',  'width', 
                                0.015,   
                                0.001,#initial_width[args.category]*(1.-dw), 
                                0.050 #initial_width[args.category]*(1.+dw)
                            )
    smodel = ROOT.RooGaussian('signal_mumu', 'signal_mumu', mumu_mass, M_mumu, width)
    # different normalizations
    nsig     = ROOT.RooRealVar('Ns', 'N signal', 0.2*datasig.sumEntries(), 0., datasig.sumEntries())
    nsig_ctrl = ROOT.RooRealVar('Ns_ctrl', 'Nctrl signal', 0.2*datactrl.sumEntries(), 0., datactrl.sumEntries())
    
    # COMBINATORIAL BACKGROUND
    # signal region
    a0 = ROOT.RooRealVar('a0', 'a0', 0, -1.0,1.0)
    a1 = ROOT.RooRealVar('a1', 'a1', 0, -1.0,1.0)
    a2 = ROOT.RooRealVar('a2', 'a2', 0, -1.0,1.0)
    a3 = ROOT.RooRealVar('a3', 'a3', 0, -1.0,1.0)
    order =  ROOT.RooArgList(a0, a1, a2, a3) if args.bdt_cut < 0.5 else ROOT.RooArgList(a0)
    #if args.resonance == 'omega' and args.bdt_cut < 0.5: order = ROOT.RooArgList(a0, a1)
    bmodel = ROOT.RooChebychev('bmodel', 'bmodel', mumu_mass, order)

    nbkg = ROOT.RooRealVar('Nb', 'N combinatorics', 0.8*datasig.numEntries(), 0., datasig.numEntries())
    full_model = ROOT.RooAddPdf('full_model', 'full_model', ROOT.RooArgList(smodel,bmodel), ROOT.RooArgList(nsig, nbkg))
    # control region
    b0 = ROOT.RooRealVar('b0', 'b0', 0, -1.0,1.0)
    b1 = ROOT.RooRealVar('b1', 'b1', 0, -1.0,1.0)
    b2 = ROOT.RooRealVar('b2', 'b2', 0, -1.0,1.0)
    b3 = ROOT.RooRealVar('b3', 'b3', 0, -1.0,1.0)
    order_ctrl  =  ROOT.RooArgList(b0, b1, b2)
    bmodel_ctrl = ROOT.RooChebychev('bmodel_ctrl', 'bmodel_ctrl', mumu_mass, order_ctrl)
    
    nbkg_ctrl       = ROOT.RooRealVar('Nb_ctrl', 'Nctrl combinatorics', 0.8*datactrl.numEntries(), 0., datactrl.numEntries())
    full_model_ctrl = ROOT.RooAddPdf('full_model_ctrl', 'full_model_ctrl', ROOT.RooArgList(smodel,bmodel_ctrl), ROOT.RooArgList(nsig_ctrl, nbkg_ctrl))


    # ** SIMULTANEOUS FIT **
    bdt_regions = ROOT.RooCategory("bdt_regions", "BDT regions", {"looseBDT" : -1, "tightBDT" : 1})
    datatofit   = ROOT.RooDataSet("datatofit", "datatofit", 
                                    {mumu_mass}, 
                                    ROOT.RooFit.Index(bdt_regions),
                                    ROOT.RooFit.Import("looseBDT", datactrl),
                                    ROOT.RooFit.Import("tightBDT", datasig)
                                )
    simul_model = ROOT.RooSimultaneous("simul_model", "simul_model", bdt_regions)
    simul_model.addPdf(full_model_ctrl, "looseBDT")
    simul_model.addPdf(full_model,      "tightBDT")
    # -- FITTING
    results = simul_model.fitTo(
        datatofit, 
        ROOT.RooFit.Range('fit_range'), 
        ROOT.RooFit.Save(),
        ROOT.RooFit.Extended(ROOT.kTRUE),
        ROOT.RooFit.SumW2Error(True),
    )
    results.Print('v')

    # -- OPTIMIZE THE VETO WINDOW
    nSigmaVeto = optimize_vetoWindow(
        fitresults={
            'x': mumu_mass,
            'nsig': nsig,
            'mean': M_mumu,
            'width': width,
        },
        sigma_min=0.5, sigma_max=5.0, sigma_step=0.5,
        outlog=logger,
        thresold_events=1.0,
    )
    nSigmaSR = 3.0 #nSigmaVeto
    mumu_mass.setRange('sig_range', M_mumu.getVal() - nSigmaSR*width.getVal(), M_mumu.getVal() + nSigmaSR*width.getVal())
    B = nbkg.getVal()*(bmodel.createIntegral(ROOT.RooArgSet(mumu_mass), ROOT.RooArgSet(mumu_mass), 'sig_range').getValV())
    significance = nsig.getVal()/((nsig.getVal()+B)**0.5) if (nsig.getVal()+B)>0 else 0
    message_logger(f' SIGNIFICANCE S/√B = {significance:.2f}', logger)
    
    # ** PLOTTING **
    # signal region
    frame = mumu_mass.frame(Title = f'{decay_label[args.resonance]}#rightarrow #mu#mu - SR')
    catSet = {bdt_regions}
    
    datatofit.plotOn(
        frame,
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.MarkerSize(1.),
        ROOT.RooFit.Name('data'),
        Cut= 'bdt_regions==bdt_regions::tightBDT',   
    )
    simul_model.plotOn(
        frame, 
        ROOT.RooFit.LineColor(ROOT.kRed),
        ROOT.RooFit.MoveToBack(),
        ROOT.RooFit.Name('fit'),
        Slice= (bdt_regions, 'tightBDT'),
        ProjWData=(catSet, datatofit),
    )
    chi2 = frame.chiSquare()

    frame_ctrl = mumu_mass.frame(Title = f'{decay_label[args.resonance]}#rightarrow #mu#mu - CR')
    datatofit.plotOn(
        frame_ctrl,
        ROOT.RooFit.Binning(nbins), 
        ROOT.RooFit.MarkerSize(1.),
        ROOT.RooFit.Name('data_ctrl'),
        Cut= 'bdt_regions==bdt_regions::looseBDT',   
    )
    simul_model.plotOn(
        frame_ctrl, 
        ROOT.RooFit.LineColor(ROOT.kBlue),
        ROOT.RooFit.MoveToBack(),
        ROOT.RooFit.Name('fit_ctrl'),
        Slice= (bdt_regions, 'looseBDT'),
        ProjWData=(catSet, datatofit),
    )
    chi2_ctrl = frame_ctrl.chiSquare()

    # CMS style 
    veto_lo = M_mumu.getVal() - nSigmaVeto*width.getVal()
    veto_hi = M_mumu.getVal() + nSigmaVeto*width.getVal()
    draw_cms_style(
        frame=frame,
        lumi_args={'lumi': cfg.LumiVal_plots[args.year], 'run': str(args.year) if args.year != 'all' else '2022+2023'},
        components={'data': 'Data', 'fit': '#phi #rightarrow #mu#mu fit'},
        veto=[veto_lo, veto_hi, nSigmaVeto],
        additionalText=[
            f'CAT {args.category}',
            f'BDT >{args.bdt_cut}', f'S/#sqrt{{B}} = {significance:.1f}',
            f'#sigma = {width.getVal()*1000:.1f} #pm {width.getError()*1000:.1f} MeV',
            ],
        outfile=f'{args.plot_outdir}/simulfit_{args.resonance}To{name[args.mu_pair]}_mass_bdt{args.bdt_cut:.3f}_SR_{catyyyy}'
    )
    draw_cms_style(
        frame=frame_ctrl,
        lumi_args={'lumi': cfg.LumiVal_plots[args.year], 'run': str(args.year) if args.year != 'all' else '2022+2023'},
        components={'data_ctrl': 'Data', 'fit_ctrl': '#phi #rightarrow #mu#mu fit'},
        additionalText=[f'CAT {args.category}', f'{ctrl_bdt_lo} < BDT < {ctrl_bdt_hi}'],
        veto=[veto_lo, veto_hi, nSigmaVeto],
        outfile=f'{args.plot_outdir}/simulfit_{args.resonance}To{name[args.mu_pair]}_mass_bdt{args.bdt_cut:.3f}_CR_{catyyyy}'
    )
    # ** PRINT RESULTS **
    # - summary text
    message_logger(f'\n [INFO] fit results:', logger)
    message_logger(f' = (SR) chi2/ndof : {chi2:.2f}', logger)
    message_logger(f' = (CR) chi2/ndof : {chi2_ctrl:.2f}', logger)
    message_logger('''
    Fit results (SR):
    - signal mean = {:.4f} +/- {:.4f} GeV
    - signal width = {:.4f} +/- {:.4f} GeV
    - N signal = {:.1f} +/- {:.1f}
    - N bkg = {:.1f} +/- {:.1f} ( {:.1f} in +/- {:.1f} in the signal region )
    - significance = {:.2f}
    '''.format(
        M_mumu.getVal(), M_mumu.getError(),
        width.getVal(), width.getError(),
        nsig.getVal(), nsig.getError(),
        nbkg.getVal(), nbkg.getError(), B, (nbkg.getError()/nbkg.getVal())*B,
        significance,
    ), logger)

    # ---- CIAO ----
    logger.close()