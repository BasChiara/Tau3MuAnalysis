#include "../include/prepStudiesT3m.h"
#include "../include/DsPhiMuMuPi_analyzer.h"
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

	// inputs from shell
	std::string inputFileName;
	std::string outputDir;
	TString dataset;
   int Nfiles = 1000;
   TString channel = "Tau3Mu";
	if ( argc < 2 ){
		std::cout << " [ERROR] missing arguments : insert the file and the dataset you want to use :-)" << std::endl; 
		std::cout <<  argv[0] <<" [inputFile] [outpudir] [dataset] [Nfiles] [channel]" << std::endl;
		return 1;
	}
	
	inputFileName = argv[1];
   outputDir = argv[2];
   dataset = argv[3];
   if (argc > 4) Nfiles = std::stoi(argv[4]);
   if (argc > 5) channel = argv[5];
   if (channel != "Tau3Mu" && channel != "DsPhiPi") {
      std::cout << " [ERROR] specify which channel you want to analyze options are \"Tau3Mu\" or \"DsPhiPi\"." << std::endl;
      exit(-1);
   }

	TChain* chain = new TChain("Events");
   FileReader file_loader = FileReader(inputFileName);
	if(dataset.Contains("data",TString::kIgnoreCase) || dataset.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase) )
      chain = file_loader.xrootdTChain_loader(Nfiles);
	else if (dataset.Contains("mc",TString::kIgnoreCase )) 
      chain = file_loader.lxplusTChain_loader();
   else if (dataset.Contains(".root")) 
      chain->Add(TString(inputFileName));
	else{
      std::cout << " [ERROR] dataset must be specified as MC or DATA (no case sensitive)" << std::endl;
		exit(-1);
	}
	if (channel == "Tau3Mu"){
      prepStudiesT3m* recoAnalyzer = new prepStudiesT3m(chain,outputDir,dataset);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }else if (channel == "DsPhiPi"){
      DsPhiMuMuPi_analyzer* recoAnalyzer = new DsPhiMuMuPi_analyzer(chain, outputDir, dataset, false);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }
	return 0;
}
