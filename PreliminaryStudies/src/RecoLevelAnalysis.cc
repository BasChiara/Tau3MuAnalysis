#include "../include/prepStudiesT3m.h"
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
	if ( argc < 2 ){
		std::cout << " [ERROR] missing arguments : insert the file and the dataset you want to use :-)" << std::endl; 
		std::cout <<  argv[0] <<" [inputFile] [outpudir] [dataset] [Nfiles]" << std::endl;
		return 1;
	}
	
	inputFileName = argv[1];
	outputDir = argv[2];
    dataset = argv[3];
    if (argc > 4) Nfiles = std::stoi(argv[4]);

	TChain* chain = new TChain("Events");
   FileReader file_loader = FileReader(inputFileName);
	if(dataset.Contains("data",TString::kIgnoreCase) || dataset.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase) )
        chain = file_loader.xrootdTChain_loader(Nfiles);
	else if (dataset.Contains("mc",TString::kIgnoreCase )) 
		chain = file_loader.lxplusTChain_loader();
	else{
		std::cout << " [ERROR] dataset must be specified as MC or DATA (no case sensitive)" << std::endl;
		//exit(-1);
		chain->Add(TString(inputFileName));
	}
	//cout<<" Number of events: " << theChain->GetEntries()<<std::endl;
   prepStudiesT3m* recoAnalyzer = new prepStudiesT3m(chain,outputDir,dataset);
	recoAnalyzer->Loop();

    delete recoAnalyzer;
	return 0;
}
