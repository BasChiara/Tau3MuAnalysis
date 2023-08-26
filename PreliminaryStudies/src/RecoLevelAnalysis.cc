#include "../include/prepStudiesT3m.h"


//C++ includes
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

//ROOT includes
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>

using namespace std;

// read data from T2 with xrootd file by file

int main(int argc, char* argv[]) {

	// inputs from shell
	char inputFileName[1000];
	char outputDir[1000];
	TString dataset;
    int Nfiles = 1000;
	int ifile = 1;
	if ( argc < 2 ){
		std::cout << " missing argument: insert the file and the dataset you want to use :-)" << std::endl; 
		std::cout <<  argv[0] <<" inputFile [outpudir] [dataset] [Nfiles]" << std::endl;
		return 1;
	}
	
	strcpy(inputFileName,argv[1]);
	strcpy(outputDir,argv[2]);
    dataset = argv[3];
    if (argc > 4) Nfiles = std::stoi(argv[4]);
	
	// -------------------------
	// Loading the file from a .txt
	TChain *theChain = new TChain("Events");
	char Buffer[5000];
	std::string NtupleDir;
	char MyRootFile[10000];
	TString ChainPath("");
	std::cout << " [INPUT] : " << inputFileName << std::endl;
	ifstream *inputFile = new ifstream(inputFileName);
    int Nfile = 0;

    while( !(inputFile->eof()) ){
        inputFile->getline(Buffer,500);
        if (!strstr(Buffer,"#") && !(strspn(Buffer," ") == strlen(Buffer)))
        {
            sscanf(Buffer,"%s",MyRootFile);
            std::cout << MyRootFile << std::endl;
            for(int i = 0; i < Nfiles; i++){
                ChainPath = TString(MyRootFile);
                if(ChainPath.EndsWith("_")){
                    if(i==0) continue;
                    ChainPath.Append(Form("%d.root", i));
                }else ChainPath.Append(Form("%.3d.root", i));
                
                int status = theChain->Add(TString(ChainPath));
                Nfile++;
                std::cout << " + chaining " << ChainPath << std::endl; 
            }
        }
    }

	cout<<" Number of chained files : " << Nfile << std::endl; 

	inputFile->close();
	delete inputFile;

	//cout<<" Number of events: " << theChain->GetEntries()<<std::endl;
    prepStudiesT3m* recoAnalyzer = new prepStudiesT3m(theChain, dataset);
	recoAnalyzer->Loop();

    delete recoAnalyzer;
	return 0;
}
