from ROOT import gROOT, TCanvas, TChain, EnableImplicitMT, TFile, TH1F, TArrow, TMath, TLegend
from ROOT import RooWorkspace, RooArgList, RooAddPdf, RooChi2Var, RooAbsData, RooCategory, RooMultiPdf, RooExtendPdf, RooRealVar, RooArgSet, RooDataSet, RooGenericPdf, RooFit
import argparse, json
import numpy as np

gROOT.SetBatch(True)
EnableImplicitMT()

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


def getGoodnessOfFit(mass, mpdf, data, name, nBinsForFit=40, i=0):
    ntoys = 1000
    name =  os.path.join(save_at, f'{name}_gofTest{i}.pdf')
    norm = RooRealVar("norm", "norm", data.sumEntries(), 0, 10e6)

    pdf = RooExtendPdf("ext", "ext", mpdf, norm)

    plot_chi2 = mass.frame()
    data.plotOn(plot_chi2, RooFit.Binning(nBinsForFit), RooFit.Name("data"))
    pdf.plotOn(plot_chi2, RooFit.Name("pdf"))

    npara = pdf.getParameters(data).getSize()
    chi2 = plot_chi2.chiSquare("pdf", "data", npara)
    print(
        f"[INFO] Calculating GOF for pdf {pdf.GetName()}, using {npara} fitted parameters"
    )

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
            binnedtoy = pdf.generateBinned(RooArgSet(mass), nToyEvents, 0, 1)
            pdf.fitTo(
                binnedtoy,
                RooFit.Minimizer("Minuit2", "minimize"),
                RooFit.Minos(0),
                RooFit.Hesse(0),
                RooFit.PrintLevel(-1),
                RooFit.Strategy(0),
            )

            plot_t = mass.frame()
            binnedtoy.plotOn(plot_t)
            pdf.plotOn(plot_t)
            chi2_t = plot_t.chiSquare(npara)
            if chi2_t >= chi2:
                npass += 1
            toy_chi2.append(chi2_t * (nBinsForFit - npara))
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
            chi2 * (nBinsForFit - npara),
            toyhist.GetMaximum(),
            chi2 * (nBinsForFit - npara),
            0,
        )
        lData.SetLineWidth(2)
        lData.Draw()
        can.SaveAs(name)

        params.assignValueOnly(preParams)
    else:
        prob = TMath.Prob(chi2 * (nBinsForFit - npara), nBinsForFit - npara)

    print(f"[INFO] GOF Chi2 in Observed =  {chi2 * (nBinsForFit - npara)}")
    print(f"[INFO] GOF p-value  =  {prob}")

    del pdf
    return prob


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
    
    cut = args.bdt_cut if hasattr(args, 'bdt_cut') else 0.0
    label = '_'.join([
        f'bdt{cut:,.4f}',
        process_name,
        args.tag, 
        'blind' if isblind else 'unblind']
    ).strip('_')
    print('\n')
    
    # --- OUTPUT ---
    log = open(f"discrete_profiling_{process_name}.log", "w")

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    print(f'{ct.BOLD}[+]{ct.END} output directory: {outputdir}')
    log.write('[+] output directory {dir} '.format(dir=outputdir))

    out_workspace = os.path.join(outputdir, f'multiPDF_workspaces', f'multipdfs_{process_name}.root')
    path_out_workspace = os.path.dirname(out_workspace)
    path_out_plots     = os.path.join(outputdir, f'multiPDF_plots')
    
    if not os.path.exists(path_out_workspace):
        os.makedirs(path_out_workspace)
    log.write('[+] output workspace {dir} '.format(dir=out_workspace))
    if not os.path.exists(path_out_plots):
        os.makedirs(path_out_plots)
    save_at = path_out_plots
    log.write('[+] output plots {dir} '.format(dir=path_out_plots))

    
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
    log.write("Max order: %d \n" % max_order)

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
        c_bernstein = '{'+f'c_Bernstein{i}0_{cat}[1]'+','+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'   .format(i, j, catYY) for j in range(1, i+1)])+'}'
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
    
    can = TCanvas('can_multipdf_{}'.format(process_name), '', 800, 800)
    leg = TLegend(0.5, 0.65, 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    
    gofmax  = -1
    gofmin = 1000
    bestfit = None
    worstfit = None
    families = ['Exponential', 'PowerLaw', 'Bernstein', 'Chebychev']#, 'Polynomial']

    allpdfs_list = RooArgList(pdfs.allPdfs())
    allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]

    converged = 0
    
    for j, fam in enumerate(families):
        log.write("> I'm in %s \n" % fam)

        fam_gofmax = 0
        pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
        mnlls    = []
        for i, pdf in enumerate(pdf_list):
            log.write(">> Pdf: %s \n" % pdf.GetName())
            norm = RooRealVar("multipdf_nbkg_{}".format(cat), "", 10.0, 0.0, 5000.0)
            ext_pdf = RooAddPdf(pdf.GetName()+"_ext", "", RooArgList(pdf), RooArgList(norm))

            if isblind:
                results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Range(fit_range), RooFit.Extended(True))
            else:
                results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Extended(True))
            chi2 = RooChi2Var("chi2"+pdf.GetName(), "", ext_pdf, hist, RooFit.DataError(RooAbsData.Expected))
            mnll = results.minNll()+0.5*(i)

            gof_prob = TMath.Prob(chi2.getVal(), int(hist.sumEntries())-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
            #if few entries, use toy-based GOF
            if data.sumEntries()<100:
                gof_prob = getGoodnessOfFit(mass, pdf, data, f'{catYY}_{fam}-{i}', 20, i)
            fis_prob = TMath.Prob(2.*(mnlls[-1]-mnll), i-converged) if len(mnlls) else 0
            if results.covQual()==3:
                mnlls.append(mnll)
                converged = i

            log.write(">>> %s chi2 %f \n" % (pdf.GetName(), chi2.getVal()) )
            log.write(">>> results.covQual(): %f \n" % results.covQual())
            log.write(">>> fis_prob: %f \n" % fis_prob)
            log.write(">>> gof_prob: %f \n" % gof_prob)

            if (gof_prob > 0.01 and fis_prob < 0.1 and results.covQual()==3) or ("Exponential" in pdf.GetName()):
            #if (fis_prob < 0.1) or ("Exponential" in pdf.GetName()):
                if gof_prob > gofmax:
                    gofmax = gof_prob
                    bestfit = pdf.GetName()
                if gof_prob < gofmin:
                    gofmin = gof_prob
                    worstfit = pdf.GetName()

                envelope.add(pdf)

                log.write(">>> "+pdf.GetName()+" added to envelope \n")
                print(">>>", pdf.GetName(), " added to envelope")
                print("gof_prob:", gof_prob, " fis_prob:", fis_prob, " mnll: ",mnll)
                ext_pdf.plotOn(frame, RooFit.LineColor(envelope.getSize()), RooFit.Name(pdf.GetName()),
                            RooFit.NormRange(fit_range if isblind else "full_range"),
                            RooFit.Range('full_range'),#(fit_range if isblind else "full_range"))
                )
            #elif fis_prob >= 0.1:
            #    break
            del chi2 
    for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
        #if worst_fit==True:
        #    leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (worstfit)" if worstfit==pdf.GetName() else pdf.GetName(), "l")
        #else:
        leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")

    frame.SetMinimum(1e-4)
    frame.SetMaximum(1.5*frame.GetMaximum())
    frame.Draw()
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