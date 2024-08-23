// ROOT includes
#include "TChain.h"
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TROOT.h"
// C++ includes
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>

#include <sys/stat.h>
#include <stdio.h>
#include <boost/program_options.hpp>
namespace po = boost::program_options;

// to compile :
// g++ -o NLO_Wkinematics_correction NLO_Wkinematics_correction.C `root-config --cflags --libs` -lboost_system -lboost_filesystem -lboost_program_options -static-libgcc
// to run :
// ./NLO_Wkinematics_correction -lo [nanoAOD_LO_fileList.txt] -nlo [nanoAOD_NLO_fileList.txt] -y [year] -o [outputDir]

int main(int argc, char* argv[]) {
    gROOT->SetBatch(true);
    gStyle->SetOptStat(0);

    std::string xrootd_prefix = "root://cms-xrd-global.cern.ch/";
    std::string isLastCopy_string = "(GenPart_statusFlags & (1<<13))";
    int W_pdgID = 24;
    std::string Wgen_selection = "(fabs(GenPart_pdgId) == " + std::to_string(W_pdgID) + ") && " + isLastCopy_string;

    // input parser
    std::string inputList_LO;
    std::string inputList_NLO;
    std::string year;
    std::string outputDir;
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "USAGE : ./NLO_Wkinematics_correction -lo [nanoAOD_LO_fileList.txt] -nlo [nanoAOD_NLO_fileList.txt] -y [year] -o [outputDir]")
        ("lo",          po::value<std::string>(&inputList_LO),      ".txt file with list of LO NanoAOD files")
        ("nlo",         po::value<std::string>(&inputList_NLO),     ".txt file with list of NLO NanoAOD files")
        ("year,y",      po::value<std::string>(&year)->default_value("2022EE"),           "year-era")
        ("output,o",    po::value<std::string>(&outputDir)->default_value("./plots/"), "output directory");
    
    po::variables_map vm;
    try {
        po::store(po::parse_command_line(argc, argv, desc), vm);
        po::notify(vm);
    } catch (std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    if (vm.count("help")) {
        std::cout << desc << "\n";
        return 1;
    }

    // --- read NANOAOD files from txt file
    std::string file_name;
    // tau3mu
    std::ifstream input_t3m_file_list(inputList_LO);
    TChain tree_t3m("Events");
    while (std::getline(input_t3m_file_list, file_name)) {
        tree_t3m.Add((xrootd_prefix + file_name).c_str());
    }
    std::cout << "[+] LO file has " << tree_t3m.GetEntries() << " entries" << std::endl;

    // NLO
    std::ifstream input_NLO_file_list(inputList_NLO);
    TChain tree_NLO("Events");
    while (std::getline(input_NLO_file_list, file_name)) {
        tree_NLO.Add((xrootd_prefix + file_name).c_str());
    }
    std::cout << "[+] NLO file has " << tree_NLO.GetEntries() << " entries" << std::endl;
    std::cout << std::endl;
    // --- W kinematics
    // pT vs eta
    int pT_bins = 15;
    double pT_lo = 0, pT_hi = 150;
    int eta_bins  = 20;
    double eta_lo = 0, eta_hi = 10;

    tree_t3m.Draw(("fabs(GenPart_eta):GenPart_pt>>h_Wgen_"+ year +"_t3m_pTeta(" + std::to_string(pT_bins) + "," + std::to_string(pT_lo) + "," + std::to_string(pT_hi) + "," + std::to_string(eta_bins) + "," + std::to_string(eta_lo) + "," + std::to_string(eta_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    TH2F* h_Wgen_t3m_pTeta = (TH2F*)gDirectory->Get(Form("h_Wgen_%s_t3m_pTeta", year.c_str()));
    tree_NLO.Draw(("fabs(GenPart_eta):GenPart_pt>>h_Wgen_"+ year +"_NLO_pTeta(" + std::to_string(pT_bins) + "," + std::to_string(pT_lo) + "," + std::to_string(pT_hi) + "," + std::to_string(eta_bins) + "," + std::to_string(eta_lo) + "," + std::to_string(eta_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    TH2F* h_Wgen_NLO_pTeta = (TH2F*)gDirectory->Get(Form("h_Wgen_%s_NLO_pTeta", year.c_str()));
    std::cout << "... done with pT VS eta histo" << std::endl;
    // pT
    TH1D* h_Wgen_t3m_pT = h_Wgen_t3m_pTeta->ProjectionX(Form("h_Wgen_%s_t3m_pT", year.c_str()));
    TH1D* h_Wgen_NLO_pT = h_Wgen_NLO_pTeta->ProjectionX(Form("h_Wgen_%s_NLO_pT", year.c_str()));
    //tree_t3m.Draw(("GenPart_pt>>h_Wgen_t3m_pT(" + std::to_string(pT_bins) + "," + std::to_string(pT_lo) + "," + std::to_string(pT_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    //TH1F* h_Wgen_t3m_pT = (TH1F*)gDirectory->Get("h_Wgen_t3m_pT");
    //tree_NLO.Draw(("GenPart_pt>>h_Wgen_NLO_pT(" + std::to_string(pT_bins) + "," + std::to_string(pT_lo) + "," + std::to_string(pT_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    //TH1F* h_Wgen_NLO_pT = (TH1F*)gDirectory->Get("h_Wgen_NLO_pT");
    std::cout << "... done with pT histo" << std::endl;
    // eta
    TH1D* h_Wgen_t3m_eta = h_Wgen_t3m_pTeta->ProjectionY(Form("h_Wgen_%s_t3m_eta", year.c_str()));
    TH1D* h_Wgen_NLO_eta = h_Wgen_NLO_pTeta->ProjectionY(Form("h_Wgen_%s_NLO_eta", year.c_str()));
    //tree_t3m.Draw(("GenPart_eta>>h_Wgen_t3m_eta(" + std::to_string(eta_bins) + "," + std::to_string(eta_lo) + "," + std::to_string(eta_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    //TH1F* h_Wgen_t3m_eta = (TH1F*)gDirectory->Get("h_Wgen_t3m_eta");
    //tree_NLO.Draw(("GenPart_eta>>h_Wgen_NLO_eta(" + std::to_string(eta_bins) + "," + std::to_string(eta_lo) + "," + std::to_string(eta_hi) + ")").c_str(), Wgen_selection.c_str(), "goff");
    //TH1F* h_Wgen_NLO_eta = (TH1F*)gDirectory->Get("h_Wgen_NLO_eta");
    std::cout << "... done with eta histo" << std::endl;

    

    // normalize
    h_Wgen_t3m_eta->Scale(1/h_Wgen_t3m_eta->Integral());
    h_Wgen_NLO_eta->Scale(1/h_Wgen_NLO_eta->Integral());
    h_Wgen_t3m_pT->Scale(1/h_Wgen_t3m_pT->Integral());
    h_Wgen_NLO_pT->Scale(1/h_Wgen_NLO_pT->Integral());
    h_Wgen_t3m_pTeta->Scale(1/h_Wgen_t3m_pTeta->Integral());
    h_Wgen_NLO_pTeta->Scale(1/h_Wgen_NLO_pTeta->Integral());

    TH2F* h_Wgen_ratio = (TH2F*)h_Wgen_NLO_pTeta->Clone(Form("h_Wgen_%s_ratio_pTeta", year.c_str()));
    h_Wgen_ratio->Divide(h_Wgen_t3m_pTeta);

    // --- save to file
    std::string output_file_name = outputDir + "/W_NLOvsT3m_" + year + ".root";
    TFile output_file(output_file_name.c_str(), "RECREATE");
    output_file.cd();
    h_Wgen_t3m_pT->Write();
    h_Wgen_NLO_pT->Write();
    h_Wgen_t3m_eta->Write();
    h_Wgen_NLO_eta->Write();
    h_Wgen_t3m_pTeta->Write();
    h_Wgen_NLO_pTeta->Write();
    h_Wgen_ratio->Write();
    output_file.Close();
    std::cout << "[i] saved to " << output_file_name << std::endl;

    return 0;
}
