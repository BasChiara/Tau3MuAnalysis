#include "../include/MCTau3Mu_base.h"
#include "../include/MCstudiesT3m.h"

#include "../include/FileReader.h"

#include <TStyle.h>
#include <TCanvas.h>


using namespace std;

int main (int argc, char* argv[]){

   

   if(argc < 2){
      std::cout << "... Usage " << argv[0] << " [Indata directory] [tag] "<< std::endl;
      return 1;
   }  

   std::string DirPath = argv[1];
   TString tag = argv[2];

   FileReader chain_loader(DirPath);
   TChain* chain = chain_loader.lxplusTChain_loader();


   MCstudiesT3m* genAnalyzer = new MCstudiesT3m(chain, tag);
   genAnalyzer->Loop();

   delete genAnalyzer;
   delete chain;

}//main()
