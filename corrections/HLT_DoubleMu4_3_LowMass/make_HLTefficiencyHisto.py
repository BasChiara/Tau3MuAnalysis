import ROOT
import HLT_DoubleMu_sf2022 as src22

DeltaR_lo, DeltaR_hi = 0.0, 1.5 
DeltaR_bins = [DeltaR_lo ,0.35, DeltaR_hi]
pT_lo, pT_hi = 0.0, 50.0
pT_bins = [pT_lo, 6.5, 10.0, 15.0, 20.0, pT_hi]

eta_edges ={
    'barrel': [0.0, 0.9],
    'overlap': [0.9, 1.2],
    'endcap': [1.2, 2.4]
}
triggers = ['L1', 'HLT']


# template 2D histogram
h_template = ROOT.TH2Poly()
h_template.SetNameTitle("h_template", "efficiency")
#[print(f' x_lo : {x_lo} x_hi : {x_hi} y_lo : {y_lo} y_hi : {y_hi}') for x_lo, x_hi in zip(pT_bins, pT_bins[1:]) for y_lo, y_hi in zip(DeltaR_bins, DeltaR_bins[1:])]
[h_template.AddBin(x_lo, y_lo, x_hi, y_hi) for x_lo, x_hi in zip(pT_bins, pT_bins[1:]) for y_lo, y_hi in zip(DeltaR_bins, DeltaR_bins[1:])]

# savehistograms on file 
f_out = ROOT.TFile('HLT_DoubleMu_efficiency2022.root', 'RECREATE')
# loop on detector regions
for region in eta_edges.keys():
    eta_lo, eta_hi = eta_edges[region]
    print(f'- {region}: {eta_lo} < |eta| < {eta_hi}')
    # loop on triggers 
    for trg in triggers:
        print(f'  - {trg}')
        
        # retrive L1 and HLT efficiencies
        mc_eff = getattr(src22, f'{region}_mc_{trg}_eff')
        data_eff = getattr(src22, f'{region}_data_{trg}_eff')
        # fill the histogram
        h_mc = h_template.Clone(f'h_mc_{trg}eff_{region}')
        h_mc.SetTitle(f'MC #varepsilon {trg} - {region}')
        h_data = h_template.Clone(f'h_data_{trg}eff_{region}')
        h_data.SetTitle(f'DATA #varepsilon {trg} - {region}')

        #[print(f' pT : {coord[0]} DR : {coord[1]} eff : {mc_eff[coord][0]}') for coord in mc_eff]
        [h_mc.Fill(coord[0], coord[1], mc_eff[coord][0]) for coord in mc_eff]
        h_mc.Write()
        [h_data.Fill(coord[0], coord[1], data_eff[coord][0]) for coord in data_eff]
        h_data.Write()

f_out.Close()
    
     