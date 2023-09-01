#include "../include/MCTau3Mu_base.h"
#include "../include/MCstudiesT3m.h"

#include <iostream>
#include <fstream>
#include <dirent.h>
#include <sys/stat.h>

#include <TStyle.h>
#include <TCanvas.h>


using namespace std;

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


int main (int argc, char* argv[]){

   

   if(argc < 2){
      std::cout << "... Usage ./GenLevelAnalysis [Indata directory] [tag] [SGN/NORM]"<< std::endl;
      return 1;
   }  

   std::string DirPath = argv[1];
   TString tag = argv[2];

   TChain* chain = TChainLoader(DirPath);

   MCstudiesT3m* genAnalyzer = new MCstudiesT3m(chain, tag);
   genAnalyzer->Loop();

   delete genAnalyzer;
   delete chain;

}//main()
