#include "../include/MCTau3Mu_base.h"
#include "../include/MCstudiesT3m.h"
#include "../include/DsPhiMuMuPi_analyzer.h"

#include "../include/FileReader.h"

#include <TStyle.h>
#include <TCanvas.h>


using namespace std;

int main (int argc, char* argv[]){

   
   // parse options
   if(argc < 2){
      std::cout << "... Usage " << argv[0] << " [Indata directory] [Tau3Mu/DsPhiPi] [out directory] [tag] "<< std::endl;
      return 1;
   }  

   std::string DirPath = argv[1];
   bool analyzeControlChannel = false;
   TString channel = argv[2];
   if (channel == "DsPhiPi") analyzeControlChannel = true;
   if (channel != "Tau3Mu" && channel != "DsPhiPi") {
      std::cout << " [ERROR] specify which channel you want to analyze options are \"Tau3Mu\" or \"DsPhiPi\"." << std::endl;
      exit(-1);
   }
   TString outdir = argv[3];
   TString tag = argv[4];

   FileReader chain_loader(DirPath);
   TChain* chain = chain_loader.lxplusTChain_loader();

   if (analyzeControlChannel){
      DsPhiMuMuPi_analyzer* genAnalyzer = new DsPhiMuMuPi_analyzer(chain, outdir, tag, true);
      genAnalyzer->Loop();

      delete genAnalyzer;
   }else{
      MCstudiesT3m* genAnalyzer = new MCstudiesT3m(chain, tag);
      genAnalyzer->Loop();

      delete genAnalyzer;
   }
   delete chain;

}//main()
