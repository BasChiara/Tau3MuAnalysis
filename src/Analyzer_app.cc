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
#include <boost/program_options.hpp>
namespace po = boost::program_options;

//ROOT includes
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
using namespace std;

int main(int argc, char* argv[]) {
	
   // usage : ./bin/Analyzer_app data/file.txt outputdir/ DATA 2022A Tau3Mu Nfiles
   // INPUT PARSER
   std::string inputFileName;
   std::string outputDir;
   std::string dset;
   std::string year;
   std::string analyzer = "Tau3Mu";
   std::string process = "default";
   int Nfiles = 1000;
   int init_file = 0;
   std::string tag;

   po::options_description desc("Allowed options");
    desc.add_options()
      ("help,h", "produce help message")
      ("input,i",      po::value<std::string>(&inputFileName),                               "input file list")
      ("output,o",     po::value<std::string>(&outputDir)->default_value("./outRoot"),       "output directory")
      ("dataset,d",    po::value<std::string>(&dset),                                     "DATA - MC - file.root")
      ("year,y",       po::value<std::string>(&year),                                        "year-era")
      ("analyzer,a",   po::value<std::string>(&analyzer)->default_value("Tau3Mu"),           "analyzer : [Tau3Mu,DsPhiPi]")
      ("process,p",    po::value<std::string>(&process)->default_value("data"),              "process: [data, Tau3Mu, DsPhiPi, W3MuNu]")
      ("Nfiles,N",     po::value<int>(&Nfiles)->default_value(1000),                         "number of files")
      ("init_file,f",  po::value<int>(&init_file)->default_value(0),                         "initial file")
      ("tag,t",        po::value<std::string>(&tag),                                         "tag");

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

   if (analyzer != "Tau3Mu" && analyzer != "DsPhiPi") {
      std::cerr << " [ERROR] specify which analyzer to use options are: \"Tau3Mu\" or \"DsPhiPi\"." << std::endl;
      return 1;
   }
   if (process != "data" && process != "Tau3Mu" && process != "DsPhiPi" && process != "W3MuNu"){
      std::cerr << " [ERROR] specify which sample to analyze options are: \"data\", \"Tau3Mu\", \"DsPhiPi\" or \"W3MuNu\"." << std::endl;
      return 1; 
   }
   
   // create a root TChain with input files
   TString dataset(dset);
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
      std::cerr << " [ERROR] dataset must be specified as MC or DATA (no case sensitive)" << std::endl;
		exit(-1);
	}


   // lounch analyzer
	if (analyzer == "Tau3Mu"){
      WTau3Mu_analyzer* recoAnalyzer = new WTau3Mu_analyzer(chain, outputDir, year, process, tag, isMC);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }else if (analyzer == "DsPhiPi"){
      DsPhiMuMuPi_analyzer* recoAnalyzer = new DsPhiMuMuPi_analyzer(chain, outputDir, year, isMC);
      recoAnalyzer->Loop();

      delete recoAnalyzer;
   }
	return 0;
}
