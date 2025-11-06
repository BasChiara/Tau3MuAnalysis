import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT()
import numpy as np
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
import mva.config as config
import style.color_text as ct

files = config.mc_samples['WTau3Mu']
year  = '2023'

selection = '&&'.join([
    config.year_selection[year],
    '(fabs(tau_fit_eta) < 0.9)',  # eta cut
    ])


mass     = ROOT.RooRealVar('tau_fit_mass', 'm_{3#mu}'  , 1.6,  2.0, 'GeV' )
mass.setRange('plot_range', 1.60, 2.0)
mass.setRange('fit_range',  1.70, 1.88)
mass_raw = ROOT.RooRealVar('tau_raw_mass', 'm_{3#mu}'  , 1.6,  2.0, 'GeV' )
mass_raw.setRange('plot_range', 1.70, 1.85)
mass_raw.setRange('fit_range',  1.70, 1.85)
year_id  = ROOT.RooRealVar('year_id', 'year_id', 0, 500, '')
eta      = ROOT.RooRealVar('tau_fit_eta', 'tau_fit_eta', -5, 5, '')

# root data frame
tree = ROOT.TChain('WTau3Mu_tree')
[tree.Add(file) for file in files]
data = ROOT.RooDataSet('data', 'data', tree, ROOT.RooArgSet(mass, mass_raw, year_id, eta), selection)

# --- signal model with sum of 2 gaussians
# prefit
mean_prefit = ROOT.RooRealVar('mean_prefit', 'mean_prefit', 1.777, 1.65, 1.9)
mean_prefit.setConstant(True)  # fix the mean for prefit
sigma1_prefit = ROOT.RooRealVar('sigma1_prefit', 'sigma1_prefit', 0.02, 0.01, 0.05)
sigma2_prefit = ROOT.RooRealVar('sigma2_prefit', 'sigma2_prefit', 0.05, 0.01, 0.10)
gaussian1_prefit = ROOT.RooGaussian('gaussian1_prefit', 'gaussian1_prefit', mass_raw, mean_prefit, sigma1_prefit)
gaussian2_prefit = ROOT.RooGaussian('gaussian2_prefit', 'gaussian2_prefit', mass_raw, mean_prefit, sigma2_prefit)
frac_prefit = ROOT.RooRealVar('frac_prefit', 'frac_prefit', 0.5, 0.0, 1.0)
signal_prefit = ROOT.RooAddPdf('signal_prefit', 'signal_prefit', 
                                ROOT.RooArgList(gaussian1_prefit, gaussian2_prefit), 
                                ROOT.RooArgList(frac_prefit)
                                )
# postfit
mean   = ROOT.RooRealVar('mean', 'mean', 1.777, 1.6, 2.0)
mean.setConstant(True)  # free the mean for postfit
sigma1  = ROOT.RooRealVar('sigma1', 'sigma1', 0.02, 0.01, 0.05)
sigma2  = ROOT.RooRealVar('sigma2', 'sigma2', 0.05, 0.01, 0.10)
gaussian1 = ROOT.RooGaussian('gaussian1', 'gaussian1', mass, mean, sigma1)
gaussian2 = ROOT.RooGaussian('gaussian2', 'gaussian2', mass, mean, sigma2)
frac = ROOT.RooRealVar('frac', 'frac', 0.5, 0.0, 1.0)
signal = ROOT.RooAddPdf('signal', 'signal', 
                        ROOT.RooArgList(gaussian1, gaussian2), 
                        ROOT.RooArgList(frac)
                        )
# --- time to fit
result_prefit = signal_prefit.fitTo(
    data, 
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.Save(), 
    ROOT.RooFit.PrintLevel(-1), 
    ROOT.RooFit.Minimizer('Minuit2', 'migrad'), 
    )
result = signal.fitTo(
    data, 
    ROOT.RooFit.Range('fit_range'),
    ROOT.RooFit.Save(), 
    ROOT.RooFit.PrintLevel(-1), 
    ROOT.RooFit.Minimizer('Minuit2', 'migrad'), 
    )
# --- print results
sigma_prefit = np.sqrt((sigma1_prefit.getVal() * frac_prefit.getVal())**2 + (sigma2_prefit.getVal()*(1.-frac_prefit.getVal()))**2) *1000
sigma = np.sqrt((sigma1.getVal() * frac.getVal())**2 + (sigma2.getVal()*(1.-frac.
                                                                         getVal()))**2) *1000
print(f'{ct.color_text.BOLD}== Fit Results =={ct.color_text.END}')
print(f' -- prefit --')
result_prefit.Print()
print(f' -- postfit --')
result.Print()
print(f' -- prefit sigma = {sigma_prefit:.3f} MeV')
print(f' -- postfit sigma = {sigma:.3f} MeV')

# --- plot the results
# prefit
frame_prefit = mass_raw.frame(ROOT.RooFit.Title('Prefit: m_{3#mu}'))
data.plotOn(frame_prefit, 
            ROOT.RooFit.Name('data'), 
            ROOT.RooFit.MarkerSize(0.5)
            )
signal_prefit.plotOn(frame_prefit, 
                     ROOT.RooFit.Name('signal_prefit'), 
                     ROOT.RooFit.Range('plot_range'),
                     ROOT.RooFit.NormRange('plot_range'),
                     ROOT.RooFit.LineColor(ROOT.kRed),
                     ROOT.RooFit.LineWidth(2),

                     )
frame_prefit.GetYaxis().SetTitleOffset(1.4)
frame_prefit.GetYaxis().SetMaxDigits(3)
# postfit
frame = mass.frame(ROOT.RooFit.Title('Postfit: m_{3#mu}'))
data.plotOn(frame, 
            ROOT.RooFit.Name('data'), 
            ROOT.RooFit.MarkerSize(0.5)
            )
signal.plotOn(frame, 
               ROOT.RooFit.Name('signal_fit'), 
               ROOT.RooFit.Range('plot_range'),
               ROOT.RooFit.NormRange('plot_range'),
               ROOT.RooFit.LineColor(ROOT.kBlue), 
               ROOT.RooFit.LineWidth(2)
               )
frame.GetYaxis().SetTitleOffset(1.4)
frame.GetYaxis().SetMaxDigits(3)
# --- draw the plots
text_prefit = ROOT.TLatex(0.60, 0.85, f'#sigma = {sigma_prefit:.1f} MeV')
text_prefit.SetNDC()
text_prefit.SetTextFont(42)
text_prefit.SetTextSize(0.045)
text = ROOT.TLatex(0.60, 0.85, f'#sigma = {sigma:.1f} MeV')
text.SetNDC()
text.SetTextFont(42)
text.SetTextSize(0.045)
frame_prefit.addObject(text_prefit)
frame.addObject(text)

can = ROOT.TCanvas('can', 'can', 1500, 800)
can.Divide(2)
can.cd(1)
frame_prefit.Draw()
can.cd(2)
frame.Draw()
can.SaveAs(f'tau_mass_prepostfit_{year}.png')
can.SaveAs(f'tau_mass_prepostfit_{year}.pdf')
# log scale
can.cd(1)
can.GetPad(1).SetLogy()
can.cd(2)
can.GetPad(2).SetLogy()
can.SaveAs(f'tau_mass_postfit_{year}_log.png')
can.SaveAs(f'tau_mass_postfit_{year}_log.pdf')