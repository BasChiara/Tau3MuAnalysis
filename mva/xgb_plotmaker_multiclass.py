import ROOT
import argparse
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics         import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold

from scipy.stats import ks_2samp

from collections import OrderedDict
from itertools import product

from pdb import set_trace

# from my config
from config import * 

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/', help=' output directory for plots')
parser.add_argument('--category'   ,                                                                 help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',            default= 'kF5_multiC',                                       help='tag to the training')
parser.add_argument('--debug',          action = 'store_true' ,                                      help='set it to have useful printout')
parser.add_argument('--unblind',        action = 'store_true' ,                                      help='set it to unblind the data')
parser.add_argument('-s', '--signal',   action = 'append',                                           help='file with signal events with BDT applied')
parser.add_argument('-w', '--w3m_input',action = 'append',                                           help='file with W3MuNu MC events with BDT applied')
parser.add_argument('-d', '--data',     action = 'append',                                           help='file with data events with BDT applied')

args = parser.parse_args()
tag = args.tag
removeNaN = False 

 # ------------ APPLY SELECTIONS ------------ # 
base_selection = '(HLT_isfired_Tau3Mu||HLT_isfired_DoubleMu)&(tau_fit_mass > %.2f & tau_fit_mass < %.2f )'%(mass_range_lo,mass_range_hi) +( '& ' + cat_selection_dict[args.category] if (args.category) else '') 
sig_selection  = base_selection 
bkg_selection  = base_selection + ('& (tau_fit_mass < %.2f | tau_fit_mass > %.2f)'%(blind_range_lo, blind_range_hi) if not (args.unblind) else '')

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

tag += '_cat%s_%s'%(args.category if (args.category) else 'ABC', 'open' if (args.unblind) else 'blind')

#  ------------ PICK SIGNAL & BACKGROUND -------------- #
if(args.signal is None):
    signals     = [
        '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_signal_HLToverlapResample_kFold_2024Apr21.root',
    ]
else :
    signals = args.signal 
if(args.data is None):
    data  = [
        '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_data_HLToverlapResample_kFold_2024Apr21_open.root',
    ]
else :
    data = args.data 
if (args.w3m_input is None):
    background_W3Mu =[
        '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/XGBout_W3MuNu_HLToverlapResample_kFold_2024Apr21.root',
    ]
else:
    background_W3Mu = args.w3m_input

print('[+] W->tau->3mu signal events read from \n', signals)
print('[+] data events read from \n', data)
print('[+] W->3mu+nu signal events read from \n', background_W3Mu)

tree_name = 'tree_w_BDT'

sig_rdf = ROOT.RDataFrame(tree_name, signals, branches).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy() )
bkgD_rdf = ROOT.RDataFrame(tree_name, data, branches).Filter(bkg_selection)
bkgD = pd.DataFrame( bkgD_rdf.AsNumpy() )
bkgW3m_rdf = ROOT.RDataFrame(tree_name, background_W3Mu, branches).Filter(sig_selection)
bkgW3m =  pd.DataFrame( bkgW3m_rdf.AsNumpy() )
if(args.debug):print(sig)
if(args.debug):print(bkgD)
if(args.debug):print(bkgW3m)

#  ------------ MERGE IN 1 DATASET -------------- #
data = pd.concat([sig, bkgD, bkgW3m])
data = data.sample(frac = 1, random_state = 1234).reset_index(drop=True)
if(args.debug) : print(data)
#data = data.sample(frac = 1, random_state = args.seed).reset_index(drop=True)
if (removeNaN) :
    check_for_nan = data.isnull().values.any()
    print ("check for NaN " + str(check_for_nan))
    if (check_for_nan):
        data = data.dropna()
        check_for_nan = data.isnull().values.any()
        print ("check again for NaN " + str(check_for_nan))
    
##             ##
#    PLOTTING   #
##             ##
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendTextSize(0.035)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendFillColor(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetHistFillStyle(3004)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetTitleXSize(0.04)
ROOT.gStyle.SetMarkerStyle(20)
ROOT.gStyle.SetFillStyle(3004)

train_selection = ((data.target == 0) | (data.target == 2) | ((data.target == 1) & ((data.tau_fit_mass < blind_range_lo) | (data.tau_fit_mass > blind_range_hi))))
plot_data = data[train_selection]

classes = list(bdt_label_process.keys())
bdt_appendix = dict(zip(classes,['t3m', 'b', 'w3m']))


# ------------ BDT SCORE ACROSS CLASSES ------------ # 
ROOT.gStyle.SetPalette(ROOT.kCMYK)
kFold = 5
canv  = ROOT.TCanvas('c_dat', '', 900,800)
legend = ROOT.TLegend(0.5, 0.7, 0.75, 0.85)
x_low , x_high , nbins = -0.1,1.1, 60
for c in classes:
    # tau -> 3mu MC
    h_BDT_t3m       = sig_rdf.Histo1D(('h_BDT_t3m_%s'%c, 'bdt score in t3m MC for %s class'%c, nbins, x_low, x_high), 'bdt_score_%s'%bdt_appendix[c]).GetPtr()
    h_BDT_t3m.Scale(1./h_BDT_t3m.GetEntries())
    h_BDTtrain_t3m  = sig_rdf.Histo1D(('h_BDTtrain_t3m_%s'%c, 'bdt score in t3m MC for %s class'%c, nbins, x_low, x_high), 'bdt_training_%s'%bdt_appendix[c]).GetPtr()
    h_BDTtrain_t3m.Scale(1./h_BDTtrain_t3m.GetEntries())

    h_BDT_t3m.SetLineColor(color_process['Tau3Mu'])
    h_BDT_t3m.SetMarkerColor(color_process['Tau3Mu'])
    h_BDTtrain_t3m.SetLineColor(color_process['Tau3Mu'])
    h_BDTtrain_t3m.SetFillColor(color_process['Tau3Mu'])
    # data SB
    h_BDT_data      = bkgD_rdf.Histo1D(('h_BDT_data_%s'%c, 'bdt score in data SB for %s class'%c, nbins, x_low, x_high), 'bdt_score_%s'%bdt_appendix[c]).GetPtr()
    h_BDT_data.Scale(1./h_BDT_data.GetEntries())
    h_BDTtrain_data = bkgD_rdf.Histo1D(('h_BDTtrain_data_%s'%c, 'bdt score in data SB for %s class'%c, nbins, x_low, x_high), 'bdt_training_%s'%bdt_appendix[c]).GetPtr()
    h_BDTtrain_data.Scale(1./h_BDTtrain_data.GetEntries())


    h_BDT_data.SetLineColor(color_process['DataSB'])
    h_BDT_data.SetMarkerColor(color_process['DataSB'])
    h_BDTtrain_data.SetLineColor(color_process['DataSB'])
    h_BDTtrain_data.SetFillColor(color_process['DataSB'])
    # w -> 3mu nu MC
    h_BDT_w3m       = bkgW3m_rdf.Histo1D(('h_BDT_w3m_%s'%c, 'bdt score in w3m MC for %s class'%c, nbins, x_low, x_high), 'bdt_score_%s'%bdt_appendix[c]).GetPtr()
    h_BDT_w3m.Scale(1./h_BDT_w3m.GetEntries())
    h_BDTtrain_w3m  = bkgW3m_rdf.Histo1D(('h_BDTtrain_w3m_%s'%c, 'bdt score in w3m MC for %s class'%c, nbins, x_low, x_high), 'bdt_training_%s'%bdt_appendix[c]).GetPtr()
    h_BDTtrain_w3m.Scale(1./h_BDTtrain_w3m.GetEntries())

    h_BDT_w3m.SetLineColor(color_process['W3MuNu'])
    h_BDT_w3m.SetMarkerColor(color_process['W3MuNu'])
    h_BDTtrain_w3m.SetLineColor(color_process['W3MuNu'])
    h_BDTtrain_w3m.SetFillColor(color_process['W3MuNu'])
    
    legend.Clear()
    canv.cd()
    #ROOT.gPad.SetMargin(0.12,0.15,0.15, 0.15)

    h_BDTtrain_data.SetMaximum(10)
    h_BDTtrain_data.GetXaxis().SetTitle('BDT_{%s} score'%bdt_appendix[c])
    h_BDTtrain_data.Draw('HIST')
    h_BDT_data.Draw('SAME PE')
    legend.AddEntry('h_BDT_data_%s'%c, 'data sidebands (test)', 'pe')
    legend.AddEntry('h_BDTtrain_data_%s'%c, 'data sidebands (train)', 'f')
    h_BDT_t3m.Draw('SAME PE')
    h_BDTtrain_t3m.Draw('SAME HIST')
    legend.AddEntry('h_BDT_t3m_%s'%c, 'MC[$\\tau \\to 3\mu$] (test)', 'pe')
    legend.AddEntry('h_BDTtrain_t3m_%s'%c, 'MC[$\\tau \\to 3\mu$] (train)', 'f')
    h_BDT_w3m.Draw('SAME PE')
    h_BDTtrain_w3m.Draw('SAME HIST')
    legend.AddEntry('h_BDT_w3m_%s'%c, 'MC[$W\\to3\mu\\nu$] (test)', 'pe')
    legend.AddEntry('h_BDTtrain_w3m_%s'%c, 'MC[$W\\to3\mu\\nu$] (train)', 'f')
    
    currentPlot_name = '%sBDTfor%s_%s' %(args.plot_outdir, c,tag)
    canv.SetLogy(1)
    legend.Draw()
    canv.SaveAs(currentPlot_name+'.png')
    canv.SaveAs(currentPlot_name+'.pdf')
    print('[=] save BDT score vs class in %s.png(pdf) '%currentPlot_name)


# ------------ D estimator (?) ------------ # 
D_low , D_high , Dnbins = -0.1, 1.1, 60
x_low , x_high , nbins  =  0.95, 1.01, 48
D_estimator = 'bdt_score_b/(bdt_score_b+bdt_score_w3m)'
h_D_t3m = sig_rdf.Define('D_t3m_b', D_estimator).Histo1D(('h_D_t3m', '', nbins, D_low, D_high), 'D_t3m_b').GetPtr()
#h_t3mVsD_t3m = sig_rdf.Define('D_t3m_b', D_estimator).Histo2D(('h_t3mVsD_t3m', '', nbins, x_low, x_high, nbins, D_low, D_high), 'bdt_score_t3m','D_t3m_b').GetPtr()
h_t3mVsD_t3m = sig_rdf.Histo2D(('h_t3mVsD_t3m', '', nbins, x_low, x_high, nbins, 1 - x_high, 1 - x_low), 'bdt_score_t3m','bdt_score_w3m').GetPtr()
h_D_t3m.Scale(1./h_D_t3m.GetEntries())
h_D_b = bkgD_rdf.Define('D_t3m_b', D_estimator).Histo1D(('h_D_b', '', nbins, D_low, D_high), 'D_t3m_b').GetPtr()
#h_t3mVsD_b= bkgD_rdf.Define('D_t3m_b', D_estimator).Histo2D(('h_t3mVsD_b', '', nbins, x_low, x_high, nbins, D_low, D_high), 'bdt_score_t3m','D_t3m_b').GetPtr()
h_t3mVsD_b = bkgD_rdf.Histo2D(('h_t3mVsD_b', '', nbins, x_low, x_high, nbins, 1 - x_high, 1 - x_low), 'bdt_score_t3m','bdt_score_w3m').GetPtr()
h_D_b.Scale(1./h_D_b.GetEntries())
h_D_w3m = bkgW3m_rdf.Define('D_t3m_b', D_estimator).Histo1D(('h_D_w3m', '', nbins, D_low, D_high), 'D_t3m_b').GetPtr()
h_D_w3m.Scale(1./h_D_w3m.GetEntries())
#h_t3mVsD_w3m= bkgW3m_rdf.Define('D_t3m_b', D_estimator).Histo2D(('h_t3mVsD_w3m', '', nbins, x_low, x_high, nbins, D_low, D_high), 'bdt_score_t3m','D_t3m_b').GetPtr()
h_t3mVsD_w3m = bkgW3m_rdf.Histo2D(('h_t3mVsD_w3m', '', nbins, x_low, x_high, nbins, 1 - x_high, 1 - x_low), 'bdt_score_t3m','bdt_score_w3m').GetPtr()


h_D_t3m.SetLineColor(color_process['Tau3Mu'])
h_D_t3m.SetFillColor(color_process['Tau3Mu'])
h_t3mVsD_t3m.SetMarkerColor(color_process['Tau3Mu'])
h_t3mVsD_t3m.SetFillColor(color_process['Tau3Mu'])
h_D_b.SetLineColor(color_process['DataSB'])
h_D_b.SetFillColor(color_process['DataSB'])
h_t3mVsD_b.SetMarkerColor(color_process['DataSB'])
h_t3mVsD_b.SetFillColor(color_process['DataSB'])
h_D_w3m.SetLineColor(color_process['W3MuNu'])
h_D_w3m.SetFillColor(color_process['W3MuNu'])
h_t3mVsD_w3m.SetMarkerColor(color_process['W3MuNu'])
h_t3mVsD_w3m.SetFillColor(color_process['W3MuNu'])

legend.Clear()
h_D_b.Draw('HIST')
h_D_b.SetXTitle(D_estimator)
h_D_b.SetMaximum(10)
legend.AddEntry('h_D_b', 'data sidebands', 'f')
h_D_t3m.Draw('SAME HIST')
legend.AddEntry('h_D_t3m', 'W#tau3#mu', 'f')
h_D_w3m.Draw('SAME HIST')
legend.AddEntry('h_D_w3m', 'W3#mu#nu', 'f')
canv.SetLogy(1)
legend.Draw()
currentPlot_name = '%sDestim%s_%s' %(args.plot_outdir, c,tag) 
canv.SaveAs(currentPlot_name+'.png')
canv.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT score vs class in %s.png(pdf) '%currentPlot_name)
canv.cd()
canv.SetLogy(0)
h_t3mVsD_b.GetXaxis().SetTitle('BDT_{#tau3#mu}')
h_t3mVsD_b.GetYaxis().SetNdivisions(810)
#h_t3mVsD_b.GetYaxis().SetTitle('BDT_{b}/(BDT_{b}+BDT_{W3#mu})')
h_t3mVsD_b.GetYaxis().SetTitle('BDT_{W3#mu}')
h_t3mVsD_t3m.Draw('')
h_t3mVsD_b.Draw('same')
h_t3mVsD_w3m.Draw('same')
currentPlot_name = '%sProbT3m_VS_Destim%s_%s' %(args.plot_outdir, c,tag) 
canv.SaveAs(currentPlot_name+'.png')
canv.SaveAs(currentPlot_name+'.pdf')



# ------------ ROC CURVE  ------------ # 
from sklearn.metrics import RocCurveDisplay

# --> ONE vs REST
# binarize the target from a flat (n_events) array to (n_events, n_classes)
from sklearn.preprocessing import LabelBinarizer
label_binarizer = LabelBinarizer().fit(plot_data.target[:10000])
target_onehot   = label_binarizer.transform(plot_data.target)
if(args.debug) : print('binarized labels ', target_onehot.shape)

from sklearn.metrics import RocCurveDisplay
# analysis set
fig, ax = plt.subplots(figsize=(10,8))
for class_of_interest in range(len(classes)):
    class_id = np.flatnonzero(label_binarizer.classes_ == class_of_interest)[0]
    predicted_score = plot_data['bdt_score_%s'%bdt_appendix[classes[class_of_interest]]]
    print('[ROC] class %s with ID %d'%(classes[class_of_interest], class_id))
    print(' target', target_onehot[:10, class_id])
    print(' prediction',predicted_score[:10])
    RocCurveDisplay.from_predictions(
        target_onehot[:, class_id],
        predicted_score,
        name=f"{classes[class_of_interest]} vs the rest",
        ax=ax,
    )
_ = ax.set(
    xlabel="False Positive Rate",
    ylabel="True Positive Rate",
    title="One-vs-Rest ROC curves",
    ylim=(0.0, 1.0),
    xlim=(10**-5, 1.0),
    xscale='log',
)
ax.grid()
fig.tight_layout()
xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
ax.plot(xy, xy, color='grey', linestyle='--', linewidth=3)
#ax.set_xticks(fontsize=16)
#ax.set_yticks(fontsize=16)
fig.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
fig.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
print('[=] save inclusive  ROC curve %sroc_%s'%(args.plot_outdir, tag))

# ------------ CONFUSION MATRIX ------------ #
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
class_prob_pred = plot_data[['bdt_score_t3m', 'bdt_score_b', 'bdt_score_w3m']].values
class_abs_pred = [np.argmax(x) for x in class_prob_pred]
conf_matrix = confusion_matrix(plot_data.target, class_abs_pred)

f,ax = plt.subplots(figsize = (8,6))
# write labels with percentages
disp = ConfusionMatrixDisplay.from_predictions(plot_data.target, class_abs_pred, display_labels=classes, normalize='true')
disp.plot(ax = ax, cmap='Blues')
ax.set_title('')

plt.suptitle('Confusion Matrix')
plot_name = '%sConfMat_%s.' %(args.plot_outdir, tag) 
plt.savefig(plot_name + 'png')
plt.savefig(plot_name + 'pdf')
print('[=] save signal correlation in %s(png/pdf)'%(plot_name))


# ------------ CORRELATION MATRIX ------------ # 
# Compute the correlation matrix for the signal
corr_sig    = sig   [features + ['tauEta','bdt_score_t3m', 'bdt_score_b', 'bdt_score_w3m', 'tau_fit_mass']].corr()
corr_bkgD   = bkgD  [features + ['tauEta','bdt_score_t3m', 'bdt_score_b', 'bdt_score_w3m', 'tau_fit_mass']].corr()
corr_bkgW3m = bkgW3m[features + ['tauEta','bdt_score_t3m', 'bdt_score_b', 'bdt_score_w3m', 'tau_fit_mass']].corr()
if (args.debug) : print(corr_sig)
corr_matrices = [corr_sig,corr_bkgD,corr_bkgW3m]

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
for i, corr in enumerate(corr_matrices):
    g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0},  annot_kws={"size":9})

    # rotate axis labels
    g.set_xticklabels(labels.values(), rotation='vertical', fontsize = 16)
    g.set_yticklabels(labels.values(), rotation='horizontal', fontsize = 16)

    # plt.show()
    plt.title('linear correlation matrix - %s'%classes[i], fontdict={'fontsize':18}, pad=16)
    plt.tight_layout()
    plot_name = '%scorr_%s_%s.' %(args.plot_outdir, classes[i], tag) 
    plt.savefig(plot_name + 'png')
    plt.savefig(plot_name + 'pdf')
    print('[=] save correlation for %s sample in %s(png/pdf)'%(classes[i],plot_name))
    plt.clf()

# ------------ FEATURES IMPORTANCE ------------ # 
load_model = './classifiers/BDTclassifiers_multiclass_HLToverlap_kFold_2024Apr12.pck' 
print('[+] load model from %s'%load_model)
with open(load_model, 'rb') as f:
    classifiers = pickle.load(f)

bdt_inputs = features + ['tauEta']
fscores = OrderedDict(zip(bdt_inputs, np.zeros(len(bdt_inputs))))
for i, iclas in classifiers.items():
    myscores = iclas.get_booster().get_fscore()
    for jj in myscores.keys():
        fscores[jj] += myscores[jj]

totalsplits = sum(float(value) for value in fscores.values())
for k, v in fscores.items():
    fscores[k] = float(v)/float(totalsplits) 

plt.xlabel('relative F-score')
plt.ylabel('feature')

orderedfscores = OrderedDict(sorted(fscores.items(), key=lambda x : x[1], reverse=False ))

bars = [labels[k] for k in orderedfscores.keys()]
y_pos = np.arange(len(bars))
 
# Create horizontal bars
plt.barh(y_pos, orderedfscores.values())
 
# Create names on the y-axis
plt.yticks(y_pos, bars)
plt.tight_layout()
plot_name ='%sFeaturesImportance_%s.' %(args.plot_outdir,tag) 
plt.savefig(plot_name + 'png')
plt.savefig(plot_name + 'pdf')
plt.clf()
print('[=] save features importance in %s(png/pdf)'%(plot_name))

exit(-1)
# ------------ BDT VS MASS ------------ # 
bdt_th = 0.5 

h_BDTmass = bkg_rdf.Histo2D(('h_BDTmass', 'bdt score in data vs reco tau candidate mass', 50, bdt_th , 1.0, 40, mass_range_lo, mass_range_hi), 'bdt_score', 'tau_fit_mass')
c = ROOT.TCanvas('c1', '', 800,800)
h_BDTmass.Draw('colz')
h_BDTmass.GetXaxis().SetTitle('BDT score')
h_BDTmass.GetXaxis().SetTitleSize(0.35)
h_BDTmass.GetYaxis().SetTitle('M 3#mu (GeV)')
h_BDTmass.GetYaxis().SetTitleSize(0.35)

currentPlot_name = '%sBDTvsMtau_data_%s' %(args.plot_outdir,tag)

c.SaveAs(currentPlot_name+'.png')
c.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs Mtau in %s.png(pdf) '%currentPlot_name)


# ------------ BDT SCORE ACROSS kFOLDs ------------ # 
ROOT.gStyle.SetPalette(ROOT.kCMYK)
kFold = 5
h_BDTfold_data  = []
h_BDTfold_signal = []
for i in range(kFold):
    h_BDTfold_data.append(bkg_rdf.Filter('bdt_to_apply==%d'%i).Histo1D(('h_BDTfold_data_%d'%i, 'bdt score in data n fold %d'%i, 50, 0.0, 1.0), 'bdt_score'))
    h_BDTfold_signal.append(sig_rdf.Filter('bdt_to_apply==%d'%i).Histo1D(('h_BDTfold_signal_%d'%i, 'bdt score in MC in fold %d'%i, 50, 0.0, 1.0), 'bdt_score'))

h_BDTfold_data[0].GetXaxis().SetTitle('BDT score')
h_BDTfold_data[0].GetXaxis().SetTitleSize(0.35)
h_BDTfold_signal[0].GetXaxis().SetTitle('BDT score')
h_BDTfold_signal[0].GetXaxis().SetTitleSize(0.35)

c_dat  = ROOT.TCanvas('c_dat', '', 800,800)
legend_dat = ROOT.TLegend(0.6, 0.6, 0.80, 0.85)
c_sig  = ROOT.TCanvas('c_sig', '', 800,800)
legend_sig = ROOT.TLegend( 0.15, 0.6, 0.35, 0.85)
for i in range(kFold):
    c_dat.cd()
    h_BDTfold_data[i].Scale(1./h_BDTfold_data[i].GetEntries())
    h_BDTfold_data[i].SetLineWidth(2)
    h_BDTfold_data[i].Draw('same hist plc')
    legend_dat.AddEntry('h_BDTfold_data_%d'%i, 'fold %d'%i,'f')
    c_sig.cd()
    h_BDTfold_signal[i].Scale(1./h_BDTfold_signal[i].GetEntries())
    h_BDTfold_signal[i].SetLineWidth(2)
    h_BDTfold_signal[i].Draw('same hist plc')
    legend_sig.AddEntry('h_BDTfold_signal_%d'%i, 'fold %d'%i, 'f')

currentPlot_name = '%sBDTvsFolds_data_%s' %(args.plot_outdir,tag)
c_dat.SetLogy(1)
c_dat.cd()
legend_dat.Draw()
c_dat.SaveAs(currentPlot_name+'.png')
c_dat.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT score vs folds in %s.png(pdf) '%currentPlot_name)
    
currentPlot_name = '%sBDTvsFolds_signal_%s' %(args.plot_outdir,tag)
c_sig.SetLogy(1)
c_sig.cd()
legend_sig.Draw()
c_sig.SaveAs(currentPlot_name+'.png')
c_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT score vs folds in %s.png(pdf) '%currentPlot_name)


# ------------ EFFICIENCY vs Mtau ------------ # 

bdt_cuts = [0.300, 0.600, 0.800, 0.900, 0.950, 0.990, 0.995]
h_bdt0_sig = sig_rdf.Histo1D(('h_bdt0_sig', '', 40, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
h_bdt0_sig.Sumw2()
h_bdt0_bkg = bkg_rdf.Histo1D(('h_bdt0_bkg', '', 40, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr()
h_bdt0_bkg.Sumw2()
h_bdtSel_sig = []
h_bdtSel_bkg = []
for cut in bdt_cuts:
    h_bdtSel_sig.append( sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_bdtSel%d_sig'%cut*1000, '', 40, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr() )
    h_bdtSel_bkg.append( bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_bdtSel%d_bkg'%cut*1000, '', 40, mass_range_lo, mass_range_hi), 'tau_fit_mass').GetPtr() )


c2_sig = ROOT.TCanvas('c2_sig', '', 1000,800)
ROOT.gPad.SetMargin(0.1, 0.2, 0.1,0.1)
c2_bkg = ROOT.TCanvas('c2_bkg', '', 1000,800)
ROOT.gPad.SetMargin(0.1, 0.2, 0.1,0.1)
legend = ROOT.TLegend(0.8, 0.5, 0.99,0.99)
h_bdtSel_sig[0].GetXaxis().SetTitle('M(3 #mu) (GeV)')
h_bdtSel_bkg[0].GetXaxis().SetTitle('M(3 #mu) (GeV)')
h_bdtSel_sig[0].GetYaxis().SetTitle('efficiency')
h_bdtSel_bkg[0].GetYaxis().SetTitle('efficiency')
h_bdtSel_sig[0].GetYaxis().SetRangeUser(0.0, 1.5)
h_bdtSel_bkg[0].GetYaxis().SetRangeUser(0.0001, 0.25)
for i in range(len(bdt_cuts)) :
    h_bdtSel_sig[i].Sumw2()
    h_bdtSel_bkg[i].Sumw2()
    h_bdtSel_sig[i].Divide(h_bdt0_sig)
    h_bdtSel_bkg[i].Divide(h_bdt0_bkg)
    h_bdtSel_sig[i].SetLineWidth(2)
    h_bdtSel_bkg[i].SetLineWidth(2)
    legend.AddEntry(h_bdtSel_sig[i], 'BDT > %.3f'%bdt_cuts[i])
    c2_sig.cd()
    h_bdtSel_sig[i].Draw('EP same plc')
    c2_bkg.cd()
    h_bdtSel_bkg[i].Draw('EP same plc')

currentPlot_name = '%sBDTeffvsMtau_signal_%s' %(args.plot_outdir,tag)
c2_sig.cd()
legend.Draw()
c2_sig.SaveAs(currentPlot_name+'.png')
c2_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)
currentPlot_name = '%sBDTeffvsMtau_sidebands_%s' %(args.plot_outdir,tag)
c2_bkg.cd()
c2_bkg.SetLogy(1)
legend.Draw()
c2_bkg.SaveAs(currentPlot_name+'.png')
c2_bkg.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT efficiency vs tau mass in %s.png(pdf) '%currentPlot_name)

# ------------ BDT score vs TAU CHARGE ------------ # 
# signal
h_bdt_chp1_sig = sig_rdf.Filter('tau_fit_charge==1').Histo1D(('h_bdt_chp1_sig', '', 50, 0.0, 1.0), 'bdt_score').GetPtr()
h_bdt_chp1_sig.Scale(1./sig_rdf.Count().GetValue())
h_bdt_chm1_sig = sig_rdf.Filter('tau_fit_charge==-1').Histo1D(('h_bdt_chm1_sig', '', 50, 0.0, 1.0), 'bdt_score').GetPtr()
h_bdt_chm1_sig.Scale(1./sig_rdf.Count().GetValue())

c3_sig = ROOT.TCanvas('c3_sig', '', 1000, 800)
leg_sig = ROOT.TLegend(0.15, 0.75, 0.4, 0.85)

h_bdt_chp1_sig.SetLineColor(ROOT.kGreen + 2)
h_bdt_chp1_sig.SetFillColor(ROOT.kGreen + 2)
h_bdt_chp1_sig.SetFillStyle(3004)
h_bdt_chp1_sig.GetXaxis().SetTitle('BDT score')
leg_sig.AddEntry(h_bdt_chp1_sig, 'q(3 #mu) = +1')
h_bdt_chm1_sig.SetLineColor(ROOT.kOrange + 2)
h_bdt_chm1_sig.SetFillColor(ROOT.kOrange + 2)
h_bdt_chm1_sig.SetFillStyle(3004)
leg_sig.AddEntry(h_bdt_chm1_sig, 'q(3 #mu) = -1')

c3_sig.cd()
h_bdt_chp1_sig.Draw('hist')
h_bdt_chm1_sig.Draw('hist same')
currentPlot_name = '%sBDTvsTauCharge_signal_%s' %(args.plot_outdir,tag)
c3_sig.cd()
c3_sig.SetLogy(1)
leg_sig.Draw()
c3_sig.SaveAs(currentPlot_name+'.png')
c3_sig.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs tau charge in %s.png(pdf) '%currentPlot_name)

# background

h_bdt_chp1_bkg = bkg_rdf.Filter('tau_fit_charge==1').Histo1D(('h_bdt_chp1_bkg', '', 50, 0.0, 1.0), 'bdt_score').GetPtr()
h_bdt_chp1_bkg.Scale(1./bkg_rdf.Count().GetValue())
h_bdt_chm1_bkg = bkg_rdf.Filter('tau_fit_charge==-1').Histo1D(('h_bdt_chm1_bkg', '', 50, 0.0, 1.0), 'bdt_score').GetPtr()
h_bdt_chm1_bkg.Scale(1./bkg_rdf.Count().GetValue())

c3_bkg = ROOT.TCanvas('c3_bkg', '', 1000, 800)
leg_bkg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
h_bdt_chp1_bkg.SetLineColor(ROOT.kGreen + 2)
h_bdt_chp1_bkg.SetFillColor(ROOT.kGreen + 2)
h_bdt_chp1_bkg.SetFillStyle(3004)
h_bdt_chp1_bkg.GetXaxis().SetTitle('BDT score')
leg_bkg.AddEntry(h_bdt_chp1_bkg, 'q(3 #mu) = +1')
h_bdt_chm1_bkg.SetLineColor(ROOT.kOrange + 2)
h_bdt_chm1_bkg.SetFillColor(ROOT.kOrange + 2)
h_bdt_chm1_bkg.SetFillStyle(3004)
leg_bkg.AddEntry(h_bdt_chm1_bkg, 'q(3 #mu) = -1')

c3_bkg.cd()
h_bdt_chp1_bkg.Draw('hist')
h_bdt_chm1_bkg.Draw('hist same')
currentPlot_name = '%sBDTvsTauCharge_data_%s' %(args.plot_outdir,tag)
c3_bkg.cd()
c3_bkg.SetLogy(1)
leg_bkg.Draw()
c3_bkg.SaveAs(currentPlot_name+'.png')
c3_bkg.SaveAs(currentPlot_name+'.pdf')
print('[=] save BDT vs tau charge in %s.png(pdf) '%currentPlot_name)

# ------------ DISPLACEMENT ------------ # 
cut = 0.995
c4 = ROOT.TCanvas('c4', '', 800, 800)
h_LxyVal_sig = sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxyVal%d_sig', '', 40, 0, 2), 'tau_Lxy_val_BS').GetPtr()
h_LxyVal_sig.SetLineColor(ROOT.kRed)
h_LxyVal_sig.SetFillColor(ROOT.kRed)
h_LxyVal_sig.SetFillStyle(3004)
h_LxyVal_sig.Scale(10*sig_rdf.Mean('weight').GetValue())
h_LxyVal_bkg = bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxyVal%d_bkg', '', 40, 0, 2), 'tau_Lxy_val_BS').GetPtr()
h_LxyVal_bkg.GetXaxis().SetTitle('L_{xy} (cm)')
h_LxyVal_bkg.SetLineColor(ROOT.kBlue)
h_LxyVal_bkg.SetFillColor(ROOT.kBlue)
h_LxyVal_bkg.SetFillStyle(3004)

c4.cd()
h_LxyVal_bkg.Draw('hist')
h_LxyVal_sig.Draw('hist same')
currentPlot_name = '%sSVdisplacement_value_BDT0p%d%s' %(args.plot_outdir, cut*1000,tag)
c4.SaveAs(currentPlot_name+'.png')
c4.SaveAs(currentPlot_name+'.pdf')


h_LxySig_sig = sig_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxySig%d_sig', '', 40, 0,10), 'tau_Lxy_sign_BS').GetPtr()
h_LxySig_sig.SetLineColor(ROOT.kRed)
h_LxySig_sig.SetFillColor(ROOT.kRed)
h_LxySig_sig.SetFillStyle(3004)
h_LxySig_sig.Scale(10*sig_rdf.Mean('weight').GetValue())
h_LxySig_bkg = bkg_rdf.Filter('bdt_score>%.3f'%cut).Histo1D(('h_LxySig%d_bkg', '', 40, 0,10), 'tau_Lxy_sign_BS').GetPtr()
h_LxySig_bkg.GetXaxis().SetTitle('L_{xy}/#sigma')
h_LxySig_bkg.SetLineColor(ROOT.kBlue)
h_LxySig_bkg.SetFillColor(ROOT.kBlue)
h_LxySig_bkg.SetFillStyle(3004)

c4.cd()
h_LxySig_bkg.Draw('hist')
h_LxySig_sig.Draw('hist same')
currentPlot_name = '%sSVdisplacement_significance_BDT0p%d%s' %(args.plot_outdir, cut*1000,tag)
c4.SaveAs(currentPlot_name+'.png')
c4.SaveAs(currentPlot_name+'.pdf')
# ------------ ROC CURVE inclusive ------------ # 
cuts_to_display = [0.600, 0.990, 0.995, 0.998]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
fig = plt.figure(figsize = (8,6))
plt.plot(xy, xy, color='grey', linestyle='--', linewidth=3)
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('background efficiency $\\epsilon_{B}$', fontsize = 18)
plt.xticks(fontsize=16)
plt.ylabel('signal efficiency $\\epsilon_{S}$', fontsize = 18)
plt.yticks(fontsize=16)
plt.xscale('log')

# analysis set
fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_score, sample_weight=plot_data.weight)
plt.plot(fpr, tpr, label='analysis set', color='b', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
plt.scatter(wp_x, wp_y)

# train set
fpr, tpr, wps = roc_curve(plot_data.target, plot_data.bdt_training, sample_weight=plot_data.weight)
plt.plot(fpr, tpr, label='train set', color='r', linewidth=2)

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]), horizontalalignment='left')

print ('ROC AUC train ', roc_auc_score(plot_data.target,  plot_data.bdt_training, sample_weight=plot_data.weight))
print ('ROC AUC test  ', roc_auc_score(plot_data.target , plot_data.bdt_score , sample_weight=plot_data.weight))

plt.legend(loc='best', fontsize='18')
plt.grid()
plt.tight_layout()
plt.savefig('%sroc_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sroc_%s.pdf' %(args.plot_outdir,tag))
print('[=] save inclusive  ROC curve %sroc_%s'%(args.plot_outdir, tag))

# ------------ ROC CURVE by category ------------ # 

fig = plt.figure(figsize = (8,6))
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('background efficiency $\\epsilon_{B}$', fontsize = 18)
plt.xticks(fontsize=16)
plt.ylabel('signal efficiency $\\epsilon_{S}$', fontsize = 18)
plt.yticks(fontsize=16)
plt.xscale('log')

resol_limit_category = {
    'A' : [0.0,   0.007],
    'B' : [0.007, 0.012],
    'C' : [0.012, 10]
}

for cat in ['A', 'B', 'C']:
    data_cat = plot_data.loc[(plot_data['tau_fit_mass_err']/plot_data['tau_fit_mass'] > resol_limit_category[cat][0]) & (plot_data['tau_fit_mass_err']/plot_data['tau_fit_mass'] < resol_limit_category[cat][1])]
    fpr, tpr, wps = roc_curve(data_cat.target, data_cat.bdt_score, sample_weight=data_cat.weight)
    auc = roc_auc_score(data_cat.target,  data_cat.bdt_training, sample_weight=data_cat.weight)
    plt.plot(fpr, tpr, label='category %s AUC= %.3f'%(cat, auc), linewidth=2)
    
    wp_x = []
    wp_y = []
    for icut in cuts_to_display:
        idx = (wps>icut).sum()
        wp_x.append(fpr[idx])
        wp_y.append(tpr[idx])
    #plt.scatter(wp_x, wp_y)
    #for i, note in enumerate(cuts_to_display):
    #    plt.annotate(note, (wp_x[i], wp_y[i]), horizontalalignment='left')
    
plt.legend(loc='best', fontsize='18')
plt.grid()
plt.tight_layout()
plt.savefig('%sROCbyCategory_%s.png' %(args.plot_outdir,tag))
plt.savefig('%sROCbyCategory_%s.pdf' %(args.plot_outdir,tag))
print('[=] save ROC by category curve %sroc_%s'%(args.plot_outdir, tag))

# ------------ CORRELATION MATRIX ------------ # 
# Compute the correlation matrix for the signal
corr = sig[features + ['tauEta','bdt_score', 'tau_fit_mass']].corr()
print(corr)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0},  annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical', fontsize = 16)
g.set_yticklabels(labels.values(), rotation='horizontal', fontsize = 16)

# plt.show()
plt.title('linear correlation matrix - signal', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_sig_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_sig_%s.pdf' %(args.plot_outdir, tag))
print('[=] save signal correlation in %scorr_sig_%s'%(args.plot_outdir, tag))
plt.clf()

# Compute the correlation matrix for the signal
corr = bkg[features + ['tauEta','bdt_score', 'tau_fit_mass']].corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": 1.0}, annot_kws={"size":9})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical', fontsize = 16)
g.set_yticklabels(labels.values(), rotation='horizontal', fontsize = 16)

# plt.show()
plt.title('linear correlation matrix - background', fontdict={'fontsize':18}, pad=16)
plt.tight_layout()
plt.savefig('%scorr_bkg_%s.png' %(args.plot_outdir, tag))
plt.savefig('%scorr_bkg_%s.pdf' %(args.plot_outdir, tag))
print('[=] save background correlation in %scorr_bkg_%s'%(args.plot_outdir, tag))



