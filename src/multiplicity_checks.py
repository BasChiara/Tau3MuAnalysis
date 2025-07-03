import uproot
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json
import itertools
import ROOT
import cmsstyle as cms
cms.SetLumi("")
cms.SetEnergy("13.6")
# Write extra lines below the extra text (usuful to define regions/channels)
cms.ResetAdditionalInfo()
cms.AppendAdditionalInfo("W/Z channel")

def get_candidate_overlap(tree):

    # loead the needed branches
    branches = tree.arrays(["run", "event", "tau_mu1_idx", "tau_mu2_idx", "tau_mu3_idx", "tau_fit_mt"])
    # group entries by event identifiers and select those with more than one candidate
    event_ids = list(zip(branches["run"], branches["event"]))
    counts = Counter(event_ids)
    filtered = ((event_id, n_cands) for event_id, n_cands in counts.items() if n_cands > 1)
    #print(f'[i] fraction of events with more than one candidate: {len(filtered) / len(counts)*100:.2%}% ({len(filtered)}/{len(counts)})')
    
    # loop on filtered events
    overlap = []
    for event_id, n_cands in filtered:
        
        #print(f"\nEvent {event_id} has {n_cands} tau3μ candidates")
        # select the entries corresponding to the event_id
        mask = (branches["run"] == event_id[0]) & (branches["event"] == event_id[1])
        cands = branches[mask]

        # the highest mT candidate is the reference
        ref_idx = np.argmax(cands["tau_fit_mt"])
        ref_triplet = (cands["tau_mu1_idx"][ref_idx], cands["tau_mu2_idx"][ref_idx], cands["tau_mu3_idx"][ref_idx])
        #print(f"Reference triplet for event {event_id}: {ref_triplet}")
        
        # calculate the overlap with the reference candidate
        for i in range(len(cands)):
            if i == ref_idx:
                continue
            triplet = (cands["tau_mu1_idx"][i], cands["tau_mu2_idx"][i], cands["tau_mu3_idx"][i])
            overlap.append(len(set(ref_triplet) & set(triplet)))
            #print(f"Triplet {i} for event {event_id}: {triplet}, overlap with reference: {overlap[-1]}")

    return overlap

def get_candidate_multiplicity(tree):
    """
    Get the number of tau3μ candidates per event.
    """
    # Load the tree
    branches = tree.arrays(["run", "event"])
    
    # Group entries by unique event identifiers
    event_ids = list(zip(branches["run"], branches["event"]))
    counts = Counter(event_ids)
    
    # Count the number of candidates per event
    multiplicities = list(counts.values())
    
    return multiplicities, counts



    

# Load the tree for MC
#era = "2023BPix"
era = "2022EE"
if era == "2022EE":
    file = uproot.open("outRoot/WTau3Mu_MCanalyzer_2022EE_HLT_overlap_onTau3Mu_MULstudies.root")
    file_data = uproot.open("/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2022_MULstudies/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2022Gv1_HLT_overlap.root")
elif era == "2023BPix":
    file = uproot.open("outRoot/WTau3Mu_MCanalyzer_2023BPix_HLT_overlap_onTau3Mu_MULstudies.root")
    file_data = uproot.open("/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/reMini2023_MULstudies/WTau3Mu_DATAanalyzer_ParkingDoubleMuonLowMass_2023Dv1_HLT_overlap.root")

tree = file["WTau3Mu_tree"]

tree_data = file_data["WTau3Mu_tree"]

tag = f"{era}"

# -- MC --
multiplicities = get_candidate_multiplicity(tree) #list(counts.values())
h_mul_mc = ROOT.TH1F("mul_mc", "Candidate multiplicity per event", 6, -0.5, 5.5)
[h_mul_mc.Fill(m) for m in multiplicities[0]]
h_mul_mc.Scale(1.0 / h_mul_mc.Integral())
overlap = get_candidate_overlap(tree)
h_ovlp_mc = ROOT.TH1F("ovlp_mc", "Candidate overlap with reference candidate", 3, -0.5, 2.5)
[h_ovlp_mc.Fill(o) for o in overlap]
h_ovlp_mc.Scale(1.0 / h_ovlp_mc.Integral())

# -- Data --
multiplicities_data = get_candidate_multiplicity(tree_data) #list(counts.values())
h_mul_data = ROOT.TH1F("mul_data", "Candidate multiplicity per event", 11, -0.5, 10.5)
[h_mul_data.Fill(m) for m in multiplicities_data[0]]
h_mul_data.Scale(1.0 / h_mul_data.Integral())
overlap_data = get_candidate_overlap(tree_data)
h_ovlp_data = ROOT.TH1F("ovlp_data", "Candidate overlap with reference candidate", 3, -0.5, 2.5)
[h_ovlp_data.Fill(o) for o in overlap_data]
h_ovlp_data.Scale(1.0 / h_ovlp_data.Integral())

# report
print(f' [i] fraction of events with more than one candidate in MC: {h_mul_mc.GetBinContent(3) * 100:.2f}% ({h_mul_mc.GetEntries()})')
print(f' [i] fraction of events with more than one candidate in data: {h_mul_data.GetBinContent(3) * 100:.2f}% ({h_mul_data.GetEntries()})')


# plot multiplicity
mul_legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.7)
mul_legend.SetBorderSize(0)
mul_legend.SetFillStyle(0)
mul_legend.SetTextSize(0.04)
canv = cms.cmsCanvas(
        'canv',
        -0.5,
        5.5,
        1e-4,
        3.0,
        "tau#rightarrow 3#mu candidates",
        "Number of events",
        square=True,
        extraSpace=0.01,
        iPos = 12,
    )
canv.SetLogy()
cms.cmsDraw(h_mul_data, "HIST SAME",
            lcolor=ROOT.kBlue,
            lstyle=ROOT.kSolid,
            lwidth=2,
            fcolor=ROOT.kBlue,
            fstyle=3004,
            marker= 0,
            )
cms.cmsDraw(h_mul_mc, "HIST", 
            lcolor=ROOT.kRed,
            lstyle=ROOT.kSolid,
            lwidth=2,
            fcolor=ROOT.kRed,
            fstyle=3004,
            )
mul_legend.AddEntry(h_mul_data, "data sidebands", "F")
mul_legend.AddEntry(h_mul_mc, "W#rightarrow #tau(3#mu)#nu MC", "F")
mul_legend.Draw()
cms.SaveCanvas(canv, f'test/nTauCandidatesPerEvent_{tag}.png', False)
cms.SaveCanvas(canv, f'test/nTauCandidatesPerEvent_{tag}.pdf', True)

# plot overlap
ovl_legend = ROOT.TLegend(0.2, 0.6, 0.7, 0.7)
ovl_legend.SetBorderSize(0)
ovl_legend.SetFillStyle(0)
ovl_legend.SetTextSize(0.04)


canv2 = cms.cmsCanvas(
        'canv2',
        -0.5,
        2.5,
        1e-4,
        3.0,
        " # overlapping #mu",
        "Number of candidates",
        square=True,
        extraSpace=0.01,
        iPos = 11,
    )
canv2.SetLogy()
cms.cmsDraw(h_ovlp_data, "HIST SAME",
            lcolor=ROOT.kBlue,
            lstyle=ROOT.kSolid,
            lwidth=2,
            fcolor=ROOT.kBlue,
            fstyle=3004,
            marker= 0,
            )
cms.cmsDraw(h_ovlp_mc, "HIST", 
            lcolor=ROOT.kRed,
            lstyle=ROOT.kSolid,
            lwidth=2,
            fcolor=ROOT.kRed,
            fstyle=3004,
            )
ovl_legend.AddEntry(h_ovlp_data, "data sidebands", "F")
ovl_legend.AddEntry(h_ovlp_mc, "W #rightarrow #tau(3#mu)#nu MC", "F")
ovl_legend.Draw()
cms.SaveCanvas(canv2, f'test/candidateOverlap_{tag}.png', False)
cms.SaveCanvas(canv2, f'test/candidateOverlap_{tag}.pdf', True)

