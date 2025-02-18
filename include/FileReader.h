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
      TChain* fileListTChain_loader(const int& Nfiles = -1);




   private:

      const TString NtuplesName_ = "Events";

      TChain* outChain_;
      std::string inputFileName_;
      TString xrootd_prefix_ = "root://cms-xrd-global.cern.ch//";
      //TString xrootd_prefix_ = "root://xrootd-cms.infn.it//";
      //TString xrootd_prefix_ = "root://eoscms.cern.ch//";

      char Buffer[5000];
      std::string NtupleDir;
      char MyRootFile[10000];
      const bool debug = false;


};

#endif
