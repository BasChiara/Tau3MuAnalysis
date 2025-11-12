from ROOT import gROOT, TCanvas, TChain, EnableImplicitMT, TFile, TH1F, TArrow, TMath, TLegend
from ROOT import RooWorkspace, RooArgList, RooAddPdf, RooChi2Var, RooAbsData, RooCategory, RooMultiPdf, RooExtendPdf, RooRealVar, RooArgSet, RooDataSet, RooGenericPdf, RooFit
from ROOT import RooMsgService
RooMsgService.instance().setGlobalKillBelow(RooFit.ERROR)

import argparse, json
import numpy as np

gROOT.SetBatch(True)
EnableImplicitMT()

import cmsstyle as CMS
CMS.setCMSStyle()
CMS.ResetAdditionalInfo()
CMS.SetEnergy(13.6)

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from style.color_text import color_text as ct
import mva.config as config
import models.fit_utils as fitu

save_at="MultiPdfPlots/"
branches = {}
categories = []
bdt_cuts = {}
year_set = 2022 #updated from argparse

min_deltaNLL_  = 1e-6 # small value to avoid 0
min_Pval_chi2_ = 0.01
max_Pval_2nll_ = 0.10
good_Cov_      = 3
min_nDoF_      = 2

def getGoodnessOfFit(mass, mpdf, data, name, nBinsForFit=40, i=0):
    ntoys = 1000
    name =  os.path.join(save_at, f'{name}_gofTest{i}.pdf')
    norm = RooRealVar("norm", "norm", data.sumEntries(), 0, 10e6)

    pdf = RooExtendPdf("ext", "ext", mpdf, norm)

    # get the observed chi2
    plot_chi2 = mass.frame()
    data.plotOn(plot_chi2, RooFit.Binning(nBinsForFit), RooFit.Name("data"))
    pdf.plotOn(plot_chi2, RooFit.Name("pdf"))

    pdfparams = pdf.getParameters(data)
    floatparams = pdfparams.selectByAttrib("Constant", False)
    npara = floatparams.getSize() #pdf.getParameters(data).getSize()
    chi2_red = plot_chi2.chiSquare("pdf", "data", npara)
    # get the actual number of plotted points
    hdata = plot_chi2.getHist("data")
    npoints = hdata.GetN()
    ndf  = max(1, npoints - npara)
    chi2 = chi2_red * ndf
    print(f"\t[GoF] chi2/ ndf = {chi2:.1f} / {ndf} (npoints = {npoints}, npara = {npara})")
    print(
        f"[INFO] Calculating GOF for pdf {pdf.GetName()}, using {npara} fitted parameters"
    )
    # if low statistics, run toys to get the p-value
    if data.sumEntries() / nBinsForFit < 5:
        print("[INFO] Running toys for GOF test")
        params = pdf.getParameters(data)
        preParams = RooArgSet()
        params.snapshot(preParams)
        ndata = int(data.sumEntries())

        npass = 0
        toy_chi2 = []
        for itoy in range(ntoys):
            params.assignValueOnly(preParams)
            nToyEvents = np.random.poisson(ndata)
            # generate unbinned toy
            toy = pdf.generate(RooArgSet(mass), nToyEvents, RooFit.Name("toy")) 
            #generate binned toy
            #toy = pdf.generateBinned(RooArgSet(mass), nToyEvents, 0, 1)
            pdf.fitTo(
                toy,
                RooFit.Minimizer("Minuit2", "minimize"),
                RooFit.Minos(0),
                RooFit.Hesse(0),
                RooFit.PrintLevel(-1),
                RooFit.Strategy(0),
            )

            plot_t = mass.frame()
            toy.plotOn(plot_t, RooFit.Binning(nBinsForFit), RooFit.Name("toy"))
            pdf.plotOn(plot_t, RooFit.Name("tpdf"))
            chi2_t_red = plot_t.chiSquare("tpdf", "toy", npara)
            npoints_t = plot_t.getHist("toy").GetN()
            ndf_t = max(1, npoints_t - npara)
            chi2_t = chi2_t_red * ndf_t
            if chi2_t >= chi2:
                npass += 1
            toy_chi2.append(chi2_t)
            del plot_t

        print("[INFO] complete")
        prob = npass / ntoys

        can = TCanvas()
        medianChi2 = np.median(toy_chi2)
        rms = np.sqrt(medianChi2)

        toyhist = TH1F(
            f"gofTest_{pdf.GetName()}.pdf",
            ";Chi2;",
            50,
            medianChi2 - 5 * rms,
            medianChi2 + 5 * rms,
        )
        for chi2_val in toy_chi2:
            toyhist.Fill(chi2_val)
        toyhist.Draw()

        lData = TArrow(
            chi2, #* (nBinsForFit - npara),
            toyhist.GetMaximum(),
            chi2, #* (nBinsForFit - npara),
            0,
        )
        lData.SetLineWidth(2)
        lData.Draw()
        can.SaveAs(name)

        params.assignValueOnly(preParams)
    else:
        prob = TMath.Prob(chi2, ndf) #(chi2 * (nBinsForFit - npara), nBinsForFit - npara)

    print(f"\t[GoF] GOF Chi2 in Observed =  {chi2:.2f}")
    print(f"\t[GoF] GOF p-value  =  {prob:.3f}")

    del pdf
    return prob, chi2, ndf


if __name__ == "__main__":

    # Import info from user
    parser = argparse.ArgumentParser(description="config and root file, settings")
    #parser.add_argument("--inputfile", type=str, help="path to input ntuple")
    parser.add_argument("--inputworkspace", type=str, help="path to input workspace with post-BDT selection data")
    parser.add_argument("--outdir",      type=str, default="multipdfs", help="output directory for workspaces")
    parser.add_argument("--unblind", action="store_true", help="is UNblind analysis ?")
    parser.add_argument('-c','--category',  choices = ['A', 'B', 'C'],  default = 'A',                          help='which categories to fit')
    parser.add_argument('-y','--year',      choices = config.year_list, default = '22',                         help='which CMS dataset to use')
    parser.add_argument('--bdt_cut',        type= float,                default = 0.9900,                       help='single value of the BDT threshold to fit')
    parser.add_argument('--tag', default='', help='tag to the training')

    args = parser.parse_args()

    # --- SETTINGS ---
    outputdir = args.outdir

    year_set = args.year
    year     = f'20{args.year}'
    cat      = args.category
    catYY    = f'{cat}{year_set}'
    catYYYY  = f'{cat}_{year}'
    isblind  = not args.unblind
    mass_name = 'tau_fit_mass'

    process_name = f'vt3m_{catYY}'

    CMS.SetLumi(config.LumiVal_plots[year], run=year)
    CMS.AppendAdditionalInfo(f'CAT {cat}')
    
    cut = args.bdt_cut if hasattr(args, 'bdt_cut') else 0.0
    label = '_'.join([
        f'bdt{cut:,.4f}',
        process_name,
        args.tag, 
        'blind' if isblind else 'unblind']
    ).strip('_')
    print('\n')
    
    # --- OUTPUT ---
    log = open(os.path.join(args.outdir, f"discrete_profiling_{process_name}.log"), "w")

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    print(f'{ct.BOLD}[+]{ct.END} output directory: {outputdir}')
    log.write('[+] output directory {dir}\n'.format(dir=outputdir))

    out_workspace      = os.path.join(outputdir, f'multiPDF_workspaces', f'multipdfs_{process_name}.root')
    path_out_workspace = os.path.dirname(out_workspace)
    path_out_plots     = os.path.join(outputdir, f'multiPDF_plots')
    
    if not os.path.exists(path_out_workspace):
        os.makedirs(path_out_workspace)
    log.write('[+] output workspace {dir}\n'.format(dir=out_workspace))
    if not os.path.exists(path_out_plots):
        os.makedirs(path_out_plots)
    save_at = path_out_plots
    log.write('[+] output plots {dir}\n'.format(dir=path_out_plots))

    
    # --- INPUT ---
      
    if args.inputworkspace:
        wsfile = TFile.Open(args.inputworkspace, "read")
        temp_ws = wsfile.Get(f'data_{process_name}') 
        if not temp_ws:
            print("No workspace found in the file, exiting...")
            exit()
    else:
        #temp_ws = load_data(args.inputfile)
        print("No input workspace provided, exiting...")
        exit()

    data = temp_ws.data("data_obs")
    data.Print()
    mass = data.get().find("tau_fit_mass")

    fit_range = 'left_SB,right_SB'
    sideband  = config.sidebands_selection 
    if isblind: data = data.reduce(RooArgSet(mass),sideband)
    else: data = data.reduce(RooArgSet(mass))


    hist = data.binnedClone('histo_'+cat)
    max_order = 3
    max_order = min(max_order, int(hist.sumEntries())-2)
    log.write(" [INFO] MAX order : %d (hard-coded)\n" % max_order)

    # - workspace for PDFs - 
    pdfs = RooWorkspace('pdfs_'+cat)
    print("Creating workspace")
    getattr(pdfs, 'import')(mass)

    # - powerlaw PDF -
    c_powerlaw  = RooRealVar(f"c_PLaw_{catYY}", "", 1, -100, 100)
    powerlaw    = RooGenericPdf(f"PowerLaw_{catYY}", "TMath::Power(@0, @1)", RooArgList(mass, c_powerlaw))
    getattr(pdfs, 'import')(powerlaw)

    # - exponential PDF -
    pdfs.factory(f"Exponential::Exponential_{catYY}({mass_name}, alpha_{catYY}[-0.9, -10, 10])")

    # - Bernstein - oder n has n+1 coefficients (starts from constant)
    for i in range(max_order+1):
        c_bernstein = '{'+f'c_Bernstein{i}0_{cat}[1]'+','+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'.format(i, j, catYY) for j in range(1, i+1)])+'}'
        #c_bernstein = '{'+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'   .format(i, j, cat) for j in range(0, i+1)])+'}'
        #print(c_bernstein)
        #exit()
        pdfs.factory('Bernstein::Bernstein{}_{}({}, {})'.format(i, catYY, mass_name, c_bernstein))

    # - Chebychev - order n has n coefficients (starts from linear)
    for i in range(min(max_order, 1)): # limit to 1nd order Chebychev
        c_chebychev = '{'+','.join(['c_Chebychev{}{}_{}[-10.0, 10.0]'.format(i+1, j, catYY) for j in range(i+1)])+'}'
        pdfs.factory('Chebychev::Chebychev{}_{}({}, {})'.format(i+1, catYY, mass_name, c_chebychev)) 

    # - Polynomial - order n has n coefficients (starts from constant)
    for i in range(1, max_order):
        c_polynomial = '{'+','.join(['c_Polynomial{}{}_{}[-10, 10]'.format(i, j, cat) for j in range(i+1)])+'}'
        pdfs.factory('Polynomial::Polynomial{}_{}({}, {})'.format(i, catYY, mass_name, c_polynomial)) 

    frame = mass.frame()
    frame.SetTitle(catYY)
    bins = int((mass.getMax() - mass.getMin())/0.01)+1
    data.plotOn(frame, RooFit.Binning(bins, mass.getMin(), mass.getMax()))
    
    envelope = RooArgList("envelope")
    
    
    leg = TLegend(0.5, 0.65, 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    nicenames = []

    
    gofmax  = -1
    gofmin = 1000
    bestfit = None
    worstfit = None
    families = ['Exponential', 'PowerLaw', 'Bernstein', 'Chebychev']#, 'Polynomial']

    allpdfs_list = RooArgList(pdfs.allPdfs())
    allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]

    converged = 0
    # loop over families 
    for j, fam in enumerate(families):
        log.write("> FAMILY : %s \n" % fam)

        fam_gofmax, fam_gofmin = 0, 1000
        pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
        
        fam_pdfbest = None
        p_val_nll = 1000
        mnlls    = []
        nDoFs    = []
        # loop over PDFs in the family
        for i, pdf in enumerate(pdf_list):
            log.write(f">> pdf-({i}) {pdf.GetName()} \n")
            
            # background model
            norm = RooRealVar("multipdf_nbkg_{}".format(cat), "", data.sumEntries(), 0.0, 1e7)
            ext_pdf = RooAddPdf(pdf.GetName()+"_ext", "", RooArgList(pdf), RooArgList(norm))
            if isblind:
                results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Range(fit_range), RooFit.Extended(True))
            else:
                results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Extended(True))
            
            # -- GOF --
            # calculate chi2 and minNLL + penalty for higher order (increase the likelihood)
            #chi2 = RooChi2Var("chi2_"+pdf.GetName(), "", ext_pdf, hist, RooFit.DataError(RooAbsData.Expected))
            #nDoF = int(hist.sumEntries())-pdf.getParameters(data).selectByAttrib("Constant", False).getSize()
            mnll = results.minNll() + 0.5*i

            # p-value from chi2 (= probability to have chi2 >= observed chi2)
            #gof_prob = TMath.Prob(chi2.getVal(), nDoF) 
            #if data.sumEntries()<100:
            gof_prob, chi2, nDoF = getGoodnessOfFit(mass, pdf, data, f'{catYY}_{fam}-{i}', 20, i)
            
            # p-value from NLL(simpler)-NLL(more complex)
            delta_NLL = 2.*(mnlls[-1]-mnll) if len(mnlls) else 2*min_deltaNLL_
            delta_nDoF = i - converged  if len(nDoFs) else 0
            fis_prob = TMath.Prob(delta_NLL, delta_nDoF) if len(mnlls) else -1
            if results.covQual()==3:
                mnlls.append(mnll)
                nDoFs.append(nDoF)
                converged = i

            log.write("    cov-quality  : %d \n" % results.covQual())
            log.write("    chi2/(nDoF)  : %.1f/%d \n" % (chi2, nDoF))#(chi2.getVal(), nDoF) )
            log.write("    p-value(chi2): %f \n" % gof_prob)
            log.write("    delta-NNL    : %f \n" % delta_NLL)
            log.write("    p-value(2NLL): %e \n" % fis_prob)
            if delta_NLL<min_deltaNLL_: 
                log.write(" xx  NLL did not improve, skipping the rest of the family \n")
                break # if NLL does not improve, skip the rest of the family

            if (gof_prob > min_Pval_chi2_ and fis_prob < max_Pval_2nll_ and results.covQual() == good_Cov_ and nDoF > min_nDoF_) or ("Exponential" in pdf.GetName()):
            #if (fis_prob < 0.1) or ("Exponential" in pdf.GetName()):
                if gof_prob > gofmax:
                    gofmax = gof_prob
                    bestfit = pdf.GetName()
                if gof_prob < gofmin:
                    gofmin = gof_prob
                    worstfit = pdf.GetName()

                envelope.add(pdf)

                log.write(" ++ "+pdf.GetName()+" added to envelope \n")
               
                ext_pdf.plotOn(frame,
                               RooFit.Name(pdf.GetName()),
                               RooFit.LineColor(envelope.getSize()), RooFit.Name(pdf.GetName()),
                               RooFit.NormRange(fit_range if isblind else "full_range"),
                               RooFit.Range('full_range'),#(fit_range if isblind else "full_range"))
                )
                nicenames.append(pdf.GetName().replace(f'_{catYY}', ''))
                
            else :
                log.write(" xx "+pdf.GetName()+" rejected \n")
            
            del chi2
    
    for i, pdf in enumerate([envelope.at(i) for i in range(envelope.getSize())]):

        leg.AddEntry(frame.findObject(pdf.GetName()), nicenames[i] + (" (bestfit)" if bestfit==pdf.GetName() else ""), "l")
        

    frame.SetMinimum(1e-4)
    frame.SetMaximum(10.0)
    #can = TCanvas('can_multipdf_{}'.format(process_name), '', 800, 800)
    can = CMS.cmsCanvas(
        'can',
        x_min=mass.getMin(), x_max=mass.getMax(),
        y_min=1e-4, y_max=10.0,
        nameXaxis='m_{3#mu} (GeV)',
        nameYaxis='Events / 10 MeV',
    )
    CMS.cmsObjectDraw(frame)
    leg.Draw("SAME")
    can.Update()
    can.SaveAs(os.path.join(path_out_plots, f'multipdf_{process_name}.png'))
    can.SaveAs(os.path.join(path_out_plots, f'multipdf_{process_name}.pdf'))

    roocat   = RooCategory(f'multipdf_bkg_cat_{catYY}', "")
    multipdf = RooMultiPdf(f'multipdf_bkg_{process_name}', "", roocat, envelope)
    #indexing Expo in the multipdf. Change line below to switch to "bestfit"
    #roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index('Exponential_{}'.format(cat)))
    if bestfit is not None:
        roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
        log.write(f' [==] Best fit PDF : {bestfit}\n')
    else:
        print(len(envelope))
        exit()
        roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(0))

    output = TFile.Open(out_workspace,"recreate")
    print("Creating workspace")
    w = RooWorkspace('w')
    getattr(w, 'import')(envelope)
    getattr(w, 'import')(multipdf)
    getattr(w, 'import')(roocat) 
    #getattr(w, 'import')(norm) 
    w.Print()
    w.Write()
    output.Close()
    
    del w
    del output
    del roocat
    del multipdf
    del hist
    del pdfs
    del data

    log.close()