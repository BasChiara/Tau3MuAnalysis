#include "../include/FileReader.h"

FileReader::FileReader(const std::string& in_file){
    inputFileName_ = in_file;
    outChain_ = new TChain(NtuplesName_);
}//FileReader()

TChain* FileReader::lxplusTChain_loader(){

    //================ Loading the directory path from file
   std::ifstream *inputFile = new std::ifstream(inputFileName_);
   if (inputFile != nullptr) 
      std::cout << " ... [INPUT] " << inputFileName_ << std::endl;
   else{
		std::cout << " [ERROR] cannot open " << inputFileName_ << std::endl;
		exit(-1);
	}

    //
    char cDirPath[10000];
    int Nfiles = 0; 
    TString tree_path = "";
    const TString treeName = "/" + NtuplesName_;

    outChain_->Reset();

    while( !(inputFile->eof()) ){
      inputFile->getline(Buffer,500);
      if (!strstr(Buffer,"#") && !(strspn(Buffer," ") == strlen(Buffer))) sscanf(Buffer,"%s",cDirPath);
      else continue;

      std::string DirPath = std::string(cDirPath);
      std::cout << " ... Loading file from directory " << DirPath << std::endl;


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

         if (strcmp(file->d_name, "tau3muNANO_") < 0 ) continue; // skip "." and ".." and "log" 
         std::string file_path = DirPath + std::string(file->d_name);   
         stat(file_path.c_str(), &file_stats); 
         //if(file_stats.st_size/1000. < 2378 ) continue;
         if(debug) std::cout << file->d_name << std::endl;
         Nfiles ++;
         tree_path = DirPath + "/" + file->d_name + treeName; 
         outChain_->Add(tree_path);
      }
      
   }
      std::cout << " ... LOADED " << Nfiles << " FILES ..." << std::endl;
      std::cout<<" ... Total number of events: " << outChain_->GetEntries()<<std::endl;

    return outChain_;
}//lxplusTChain_loader()

TChain* FileReader::xrootdTChain_loader(const int& Nfiles, const int& init_file){

    // open the text file containing the input-files paths
	std::ifstream *inputFile = new std::ifstream(inputFileName_);
	if (inputFile != nullptr) 
      std::cout << " ... [INPUT] " << inputFileName_ << std::endl;
	else{
		std::cout << " [ERROR] cannot open " << inputFileName_ << std::endl;
		exit(-1);
	}
	
	char MyRootFile[10000];
	TString ChainPath("");
	
    int addedFiles = 0;
    int filesToAdd = Nfiles;
    int last_file  = Nfiles + init_file; 
    if (debug) std::cout << " + adding " << filesToAdd << " files" << std::endl; 
    // read the .txt lines
    while( !(inputFile->eof()) && (filesToAdd > 0) ){
        inputFile->getline(Buffer,500);
        if (!strstr(Buffer,"#") && !(strspn(Buffer," ") == strlen(Buffer)))
        {
            sscanf(Buffer,"%s",MyRootFile);
            if (debug) std::cout << " [+] start adding "<< filesToAdd << " files from " << MyRootFile << std::endl;
            for(int i = init_file; i < last_file; i++){
                ChainPath = TString(MyRootFile);
                if(ChainPath.EndsWith("_")) ChainPath.Append(Form("%d.root", i+1));
                else ChainPath.Append(Form("%.3d.root", i));
                if (debug) std::cout << " + " << ChainPath << std::endl; 
                int status = outChain_->Add(TString(ChainPath));
                addedFiles++;
                if(addedFiles > 1000 || addedFiles == Nfiles) last_file -= addedFiles;
            }
        }
    }

	std::cout <<" [+] number of chained files : " << addedFiles << std::endl; 

	inputFile->close();
	delete inputFile;

    


    return outChain_;
}//xrootdTChain_loader()
