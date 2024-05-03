#include "../include/DsPhiMuMuPi_analyzer.h"
#include "../include/WTau3Mu_analyzer.h"
#include "../include/FileReader.h"


//C++ includes
#include <iostream>
#include <fstream>
#include <dirent.h>
#include <sys/stat.h>
#include <string>
#include <stdio.h>

//ROOT includes
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>

using namespace std;

int main(int argc, char* argv[]) {
	
   // usage : ./bin/Analyzer_app data/file.txt outputdir/ DATA 2022A Tau3Mu Nfiles
   if ( argc < 2 ){
		std::cout << " [ERROR] missing arguments : insert the file and the dataset you want to use :-)" << std::endl; 
		std::cout <<  argv[0] <<" [inputFile] [outpudir] [DATA/MC] [year] [Tau3Mu/DsPhiPi] [Nfiles] [init_file] [opt-tag]" << std::endl;
		return 1;
	}

	// command line inputs
	std::string inputFileName = argv[1];
	std::string outputDir = argv[2];
	TString dataset = argv[3];
	TString year = argv[4];
   TString channel = "Tau3Mu";
   if (argc > 5) channel = argv[5];
   if (channel != "Tau3Mu" && channel != "DsPhiPi") {
      std::cout << " [ERROR] specify which channel you want to analyze options are \"Tau3Mu\" or \"DsPhiPi\"." << std::endl;
      exit(-1);
   }
   int Nfiles = 1000;
   if (argc > 6) Nfiles = std::stoi(argv[6]);
   int init_file = 0;
   if (argc > 7) init_file = std::stoi(argv[7]); 
   TString tag = "";
   if (argc > 8) tag = argv[8];

   // create a root TChain with input files
	TChain* chain = new TChain("Events");
   bool isMC = false;
   FileReader file_loader = FileReader(inputFileName);

	if(dataset.Contains("data",TString::kIgnoreCase) || dataset.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase) ){
      chain = file_loader.xrootdTChain_loader(Nfiles, init_file);
      isMC = false;
	}else if (dataset.Contains("mc",TString::kIgnoreCase )){ 
      chain = file_loader.lxplusTChain_loader();
      isMC = true;
   }else if (dataset.Contains(".root")) 
      chain->Add(TString(inputFileName));
	else{
      std::cout << " [ERROR] dataset must be specified as MC or DATA (no case sensitive)" << std::endl;
		exit(-1);
	}


   // lounch analyzer
	if (channel == "Tau3Mu"){
      WTau3Mu_analyzer* recoAnalyzer = new WTau3Mu_analyzer(chain, outputDir, year, tag, isMC);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }else if (channel == "DsPhiPi"){
      DsPhiMuMuPi_analyzer* recoAnalyzer = new DsPhiMuMuPi_analyzer(chain, outputDir, year, isMC);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }
	return 0;
}
