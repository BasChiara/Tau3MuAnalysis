#ifndef FileReader_h
#define FileReader_h

#include <iostream>
#include <fstream>
#include <dirent.h>
#include <sys/stat.h>

#include "TString.h"
#include "TTree.h"
#include "TChain.h"

class FileReader{

   public:
      FileReader(const std::string& in_file);
      ~FileReader(){ }

      TChain* lxplusTChain_loader();
      TChain* xrootdTChain_loader(const int& Nfiles, const int& init_file = 1);




   private:

      const TString NtuplesName_ = "Events";

      TChain* outChain_;
      std::string inputFileName_;

      char Buffer[5000];
      std::string NtupleDir;
      char MyRootFile[10000];
      const bool debug = true;


};

#endif
