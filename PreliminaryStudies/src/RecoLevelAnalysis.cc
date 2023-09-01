#include "../include/prepStudiesT3m.h"


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

// read data from T2 with xrootd
TChain* xrootd_TChainLoader(const std::string& inputFileName, const int& Nfiles){
	
	TChain *theChain = new TChain("Events");
	
	// open the text file containing the input-files paths
	ifstream *inputFile = new ifstream(inputFileName);
	if (inputFile != nullptr) 
      std::cout << " ... [INPUT] " << inputFileName << std::endl;
	else{
		std::cout << " [ERROR] cannot open " << inputFileName << std::endl;
		exit(-1);
	}
	
	char Buffer[5000];
	std::string NtupleDir;
	char MyRootFile[10000];
	TString ChainPath("");
	
    int Nfile = 0;
    int filesToAdd = Nfiles;
    while( !(inputFile->eof()) ){
        inputFile->getline(Buffer,500);
        if (!strstr(Buffer,"#") && !(strspn(Buffer," ") == strlen(Buffer)))
        {
            sscanf(Buffer,"%s",MyRootFile);
            std::cout << " [+] start adding "<< filesToAdd << " files :" << MyRootFile << std::endl;
            for(int i = 0; i < filesToAdd; i++){
                ChainPath = TString(MyRootFile);
                if(ChainPath.EndsWith("_")){
                    if(i>0) ChainPath.Append(Form("%d.root", i));
                }else ChainPath.Append(Form("%.3d.root", i));
                
                int status = theChain->Add(TString(ChainPath));
                Nfile++;
                if(Nfile > 1000){
                    Nfile = 0;
                    filesToAdd -= 1000;
                    break;
                }
                //std::cout << " + chaining " << ChainPath << std::endl; 
            }
        }
    }

	cout <<" [+] number of chained files : " << Nfile << std::endl; 

	inputFile->close();
	delete inputFile;

	return theChain;

}// xrootd_TChainLoader()

TChain* TChainLoader(const std::string& inputFileName) {

   //================ Loading the directory path from file
   ifstream *inputFile = new ifstream(inputFileName);
   if (inputFile != nullptr) 
      std::cout << " ... [INPUT] " << inputFileName << std::endl;
   else{
		std::cout << " [ERROR] cannot open " << inputFileName << std::endl;
		exit(-1);
	}
   char Buffer[5000];
   char cDirPath[10000];
   while( !(inputFile->eof()) ){
      inputFile->getline(Buffer,500);
      if (!strstr(Buffer,"#") && !(strspn(Buffer," ") == strlen(Buffer))) sscanf(Buffer,"%s",cDirPath);
   
   }
   std::string DirPath = std::string(cDirPath);
   std::cout << " ... Loading file from directory " << DirPath << std::endl;

   int Nfiles = 0; 
   TString tree_path = "";
   const TString treeName = "/Events";

   //Creating chain
   TChain* chain =new TChain("Events");

   //Read the directory
   struct dirent* file = NULL; 
   struct stat file_stats;
   const char* directory;
   DIR* dir_pointer = NULL;

   directory = cDirPath;
   dir_pointer = opendir(directory);//point to the directory
   
   while((file = readdir (dir_pointer))){
      if(file == NULL){
         std::cout << "ERROR null pointer to file" << std::endl;
         exit(-1);
      }

      if (strcmp(file->d_name, "tau3muNANO_") < 0) continue; // skip "." and ".." and "log" 
      std::string file_path = DirPath + std::string(file->d_name);   
        stat(file_path.c_str(), &file_stats); 
      if(file_stats.st_size/1000. < 2378 ) continue;
      Nfiles ++;
      //std::cout << file->d_name << std::endl;
      tree_path = DirPath + "/" + file->d_name + treeName; 
      chain->Add(tree_path);
   }
      
      std::cout << " ... LOADING " << Nfiles << " FILES ..." << std::endl;
      cout<<" ... Total number of events: " << chain->GetEntries()<<std::endl;
      
      return chain;
} // TChainLoader()

int main(int argc, char* argv[]) {

	// inputs from shell
	std::string inputFileName;
	std::string outputDir;
	TString dataset;
    int Nfiles = 1000;
	if ( argc < 2 ){
		std::cout << " [ERROR] missing arguments : insert the file and the dataset you want to use :-)" << std::endl; 
		std::cout <<  argv[0] <<" inputFile [outpudir] [dataset] [Nfiles]" << std::endl;
		return 1;
	}
	
	inputFileName = argv[1];
	outputDir = argv[2];
   dataset = argv[3];
   if (argc > 4) Nfiles = std::stoi(argv[4]);

	TChain* chain = new TChain();
	if(dataset.Contains("data",TString::kIgnoreCase) || dataset.Contains("ParkingDoubleMuonLowMass",TString::kIgnoreCase) )
		chain = xrootd_TChainLoader(inputFileName, Nfiles);
	else if (dataset.Contains("mc",TString::kIgnoreCase )) 
		chain = TChainLoader(inputFileName);
	else{
		std::cout << " [ERROR] dataset must be specified as MC or DATA (no case sensitive)" << std::endl;
		exit(-1);
	}
	//cout<<" Number of events: " << theChain->GetEntries()<<std::endl;
    prepStudiesT3m* recoAnalyzer = new prepStudiesT3m(chain,outputDir,dataset);
	recoAnalyzer->Loop();

    delete recoAnalyzer;
	return 0;
}
