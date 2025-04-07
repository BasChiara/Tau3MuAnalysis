import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()
import argparse
import os
import sys
import pandas as pd
# from my config
sys.path.append(os.path.abspath('../'))
import mva.config as cfg
import plots.plotting_tools as ptools

import warnings
warnings.filterwarnings("ignore", category=UserWarning)




parser = argparse.ArgumentParser()
parser.add_argument('--plot_outdir',    
                    default= '/eos/user/c/cbasile/www/Tau3Mu_Run3/BDTtraining/features', 
                    help=' output directory for plots')
parser.add_argument('--category', 
                    help= 'resolution category to compute (A, B, C)')
parser.add_argument('--tag',            
                    default= 'app_emulateRun2',                                  
                    help='tag to the training')
parser.add_argument('--bdt_cut',        
                    default= 0.995, 
                    type= float,                                 
                    help='bdt threshold')
parser.add_argument('--debug',          
                    action = 'store_true' ,                                      
                    help='set it to have useful printout')
parser.add_argument('--LxySign_cut',    
                    default=  0.0,  
                    type = float,                                
                    help='set random state for reproducible results')
parser.add_argument('-p', '--process',  
                    choices = cfg.process_name, 
                    default = 'WTau3Mu',help='which process in the simulation')
parser.add_argument('-s', '--signal',   
                    action = 'append',                                           
                    help='file with signal events with BDT applied')
parser.add_argument('-d', '--data',     
                    action = 'append',                                           
                    help='file with data events with BDT applied')

args = parser.parse_args()

year_list = ['2022', '2023', '2024']
year_colors = [ROOT.kBlue, ROOT.kOrange+7, ROOT.kGreen+2]
tag = args.tag
removeNaN = False

observables = cfg.features + ['tau_fit_eta', 'tau_fit_mass', 'tau_mu12_fitM', 'tau_mu23_fitM', 'tau_mu13_fitM', 'tau_Lxy_val_BS', 'tau_Lxy_err_BS']
observables = ['tau_Lxy_val_BS']

# ------------ INPUT/OUTPUT ------------ # 
if not os.path.isdir(args.plot_outdir):
    os.makedirs(args.plot_outdir)
    os.system(f'cp ~/public/index.php {args.plot_outdir}')
    print(f'[i] created directory for output plots : {args.plot_outdir}')
else:
    print(f'[i] already existing directory for output plots : {args.plot_outdir}')

# ------------ APPLY SELECTIONS ------------ #
base_selection = ' & '.join([
    cfg.base_selection,
    cfg.phi_veto,
    f' (tau_Lxy_sign_BS > {args.LxySign_cut})',

])
sig_selection  = base_selection 
if (args.process == 'invMedID') : 
    sig_selection = base_selection
bkg_selection  = base_selection + f'& {cfg.sidebands_selection}'
if (args.process == 'W3MuNu') : 
    sig_selection = bkg_selection

print('[!] base-selection : %s'%base_selection)
print('[S] signal-selection : %s'%sig_selection)
print('[B] background-selection : %s'%bkg_selection)

#  ------------ PICK SIGNAL & BACKGROUND -------------- #
if(args.signal is None):
    signals     = cfg.mc_samples[args.process]
else :
    signals = args.signal 
if(args.data is None):
    backgrounds  = cfg.data_samples[args.process]
else :
    backgrounds = args.data 

#print('[+] signal events read from \n', signals)
#print('[+] data events read from \n', backgrounds)

tree_name = 'WTau3Mu_tree'

sig_rdf = ROOT.RDataFrame(tree_name, signals).Filter(sig_selection)
sig = pd.DataFrame( sig_rdf.AsNumpy(observables) )
if(args.debug):print(sig)
bkg_rdf = ROOT.RDataFrame(tree_name, backgrounds).Filter(bkg_selection)
bkg = pd.DataFrame( bkg_rdf.AsNumpy(observables) )
if(args.debug):print(bkg)
    
##             ##
#    PLOTTING   #
##             ##
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(0.035)



leg_coords = {
    'x1': 0.60,
    'y1': 0.70,
    'x2': 0.90,
    'y2': 0.90,
}
legend_mc   = ROOT.TLegend(leg_coords['x1'], leg_coords['y1'], leg_coords['x2'], leg_coords['y2'])
legend_mc.SetBorderSize(0)
legend_mc.SetFillStyle(0)
legend_mc.SetTextSize(0.035)

legend_data = ROOT.TLegend(leg_coords['x1'], leg_coords['y1'], leg_coords['x2'], leg_coords['y2'])
legend_data.SetBorderSize(0)
legend_data.SetFillStyle(0)
legend_data.SetTextSize(0.035)

for obs in observables:
    mc_dist = []
    data_dist = []
    print(f'\n---- plotting {obs} ----')
    for i,y in enumerate(year_list):
        # ---- MC ---- #
        h_sig = sig_rdf.Filter(cfg.year_selection[y]).Histo1D((f'hSig_{y}{obs}', '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs, 'weight').GetPtr()
        h_sig.Scale(1./h_sig.Integral())
        h_sig.SetLineColor(year_colors[i])
        h_sig.SetLineWidth(2)
        h_sig.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3])
        h_sig.GetYaxis().SetTitle('a.u.')
        mc_dist.append(h_sig)
        legend_mc.AddEntry(h_sig, f'{y} MC', 'l')
        
        # ---- DATA ---- #
        h_bkg = bkg_rdf.Filter(cfg.year_selection[y]).Histo1D((f'hBkg_{y}{obs}', '', cfg.features_NbinsXloXhiLabelLog[obs][0], cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]), obs).GetPtr()
        h_bkg.Scale(1./h_bkg.Integral())
        h_bkg.SetLineColor(year_colors[i])
        h_bkg.SetLineWidth(2)
        h_bkg.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3])
        h_bkg.GetYaxis().SetTitle('a.u.')
        data_dist.append(h_bkg)
        legend_data.AddEntry(h_bkg, f'{y} data sidebands', 'l')
    
    # - plot MC - #
    ptools.ratio_plot_CMSstyle(
        histo_num=mc_dist[1:],
        histo_den=mc_dist[0],
        ratio_w  = 0.40,
        ratio_yname=f'/ {year_list[0]}',
        x_lim = [cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]],
        y_lim = [ 0.0 , max([h.GetMaximum() for h in mc_dist])*1.4],
        log_y = cfg.features_NbinsXloXhiLabelLog[obs][4], 
        to_ploton=[legend_mc],
        file_name=f'{args.plot_outdir}/{obs}_MC_{args.process}_{args.tag}',
        isMC=True,
    )
    mc_dist.clear()
    legend_mc.Clear()
    # - plot DATA - #
    ptools.ratio_plot_CMSstyle(
        histo_num=data_dist[1:],
        histo_den=data_dist[0],
        ratio_w  = 0.15,
        ratio_yname=f'/ {year_list[0]}',
        x_lim = [cfg.features_NbinsXloXhiLabelLog[obs][1], cfg.features_NbinsXloXhiLabelLog[obs][2]],
        y_lim = [ 0.0 , max([h.GetMaximum() for h in data_dist])*1.4],
        log_y = cfg.features_NbinsXloXhiLabelLog[obs][4], 
        to_ploton=[legend_data],
        file_name=f'{args.plot_outdir}/{obs}_DATA_{args.process}_{args.tag}',
        year = 'Run3',
        isMC=False,
    )

    data_dist.clear()
    legend_data.Clear()

# plot BDT output
tree_name = 'tree_w_BDT'
file_mc_2223 = cfg.mc_bdt_samples[args.process]
file_mc_24   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_WTau3Mu_MC_2024only.root'
file_data_2223 = cfg.data_bdt_samples[args.process]
file_data_24   = '/eos/user/c/cbasile/Tau3MuRun3/data/mva_data/output/XGBout_WTau3Mu_DATA_2024only.root'

observables = ['bdt_score']
rdf_mc_2223 = ROOT.RDataFrame(tree_name, file_mc_2223).Filter(sig_selection)
rdf_mc_24   = ROOT.RDataFrame(tree_name, file_mc_24).Filter(sig_selection)
rdf_data_2223 = ROOT.RDataFrame(tree_name, file_data_2223).Filter(bkg_selection)
rdf_data_24   = ROOT.RDataFrame(tree_name, file_data_24).Filter(bkg_selection)
   
obs = 'bdt_score'
mc_dist = []
data_dist = []
nbins, xlo, xhi = (101, 0., 1.0)
print(f'\n---- plotting {obs} ----')
for i,y in enumerate(year_list):
    # ---- MC ---- #
    if y == '2024':
        h_sig = rdf_mc_24.Histo1D((f'hSig_{y}{obs}', '', nbins, xlo, xhi), obs, 'weight').GetPtr()
    else:
        h_sig = rdf_mc_2223.Filter(cfg.year_selection[y]).Histo1D((f'hSig_{y}{obs}', '', nbins, xlo, xhi), obs, 'weight').GetPtr()
    h_sig.Scale(1./h_sig.Integral())
    h_sig.SetLineColor(year_colors[i])
    h_sig.SetLineWidth(2)
    h_sig.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3])
    h_sig.GetYaxis().SetTitle('a.u.')
    mc_dist.append(h_sig)
    legend_mc.AddEntry(h_sig, f'{y} MC', 'l')
    
    # ---- DATA ---- #
    if y == '2024':
        h_bkg = rdf_data_24.Histo1D((f'hBkg_{y}{obs}', '', nbins, xlo, xhi), obs).GetPtr()
    else:
        h_bkg = rdf_data_2223.Filter(cfg.year_selection[y]).Histo1D((f'hBkg_{y}{obs}', '', nbins, xlo, xhi), obs).GetPtr()
    h_bkg.Scale(1./h_bkg.Integral())
    h_bkg.SetLineColor(year_colors[i])
    h_bkg.SetLineWidth(2)
    h_bkg.GetXaxis().SetTitle(cfg.features_NbinsXloXhiLabelLog[obs][3])
    h_bkg.GetYaxis().SetTitle('a.u.')
    data_dist.append(h_bkg)
    legend_data.AddEntry(h_bkg, f'{y} data sidebands', 'l')
# - plot MC - #
ptools.ratio_plot_CMSstyle(
    histo_num=mc_dist[1:],
    histo_den=mc_dist[0],
    ratio_w  = 0.40,
    ratio_yname=f'/ {year_list[0]}',
    x_lim = [0.850, xhi],
    y_lim = [ 0.0 , max([h.GetMaximum() for h in mc_dist])*1.4],
    log_y = cfg.features_NbinsXloXhiLabelLog[obs][4], 
    to_ploton=[legend_mc],
    file_name=f'{args.plot_outdir}/{obs}_MC_{args.process}_{args.tag}',
    isMC=True,
)
mc_dist.clear()
legend_mc.Clear()
# - plot DATA - #
ptools.ratio_plot_CMSstyle(
    histo_num=data_dist[1:],
    histo_den=data_dist[0],
    ratio_w  = 1.0,
    ratio_yname=f'/ {year_list[0]}',
    x_lim = [0.850, xhi],
    y_lim = [ 0.0, 1e-3],
    log_y = cfg.features_NbinsXloXhiLabelLog[obs][4], 
    to_ploton=[legend_data],
    file_name=f'{args.plot_outdir}/{obs}_DATA_{args.process}_{args.tag}',
    year = 'Run3',
    isMC=False,
)
data_dist.clear()
legend_data.Clear()



# ---- close all ---- #
print('closing all open files')
ROOT.gROOT.GetListOfFiles().Delete()
print('closing all open canvases')
ROOT.gROOT.GetListOfCanvases().Delete()




