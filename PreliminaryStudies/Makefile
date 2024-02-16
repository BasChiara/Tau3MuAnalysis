ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --libs)
ROOTGLIBS     = $(shell root-config --glibs) -lTMVA -lRooFit -lRooFitCore -lMinuit

CXX           = g++
CXXFLAGS      = -g -fPIC -Wno-deprecated -O -ansi -D_GNU_SOURCE -g -O2
LD            = g++
LDFLAGS       = -g -lGenVector # con errori tipo 'undefined reference to `ROOT::Math::GenVector::Throw(char const*)'
SOFLAGS       = -shared


ARCH         := $(shell root-config --arch)
PLATFORM     := $(shell root-config --platform)


CXXFLAGS      += $(ROOTCFLAGS)
#CXX           += -I./
LIBS           = $(ROOTLIBS) 

NGLIBS         = $(ROOTGLIBS) 
GLIBS          = $(filter-out -lNew , $(NGLIBS))

INCLUDEDIR       = ./
CXX	         += -I$(INCLUDEDIR) -I.
OUTLIB	         = $(INCLUDEDIR)/lib/
OUTEXE				= $(INCLUDEDIR)/bin/

.SUFFIXES: .cc,.C,.hh,.h
.PREFIXES: ./lib/

$(OUTLIB)FileReader.o: $(INCLUDEDIR)src/FileReader.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)FileReader.o $<
$(OUTLIB)MCTau3Mu_base.o: $(INCLUDEDIR)src/MCTau3Mu_base.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)MCTau3Mu_base.o $<
$(OUTLIB)Tau3Mu_base.o: $(INCLUDEDIR)src/Tau3Mu_base.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)Tau3Mu_base.o $<
$(OUTLIB)MCstudiesT3m.o: $(INCLUDEDIR)src/MCstudiesT3m.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)MCstudiesT3m.o $<
$(OUTLIB)prepStudiesT3m.o: $(INCLUDEDIR)src/prepStudiesT3m.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)prepStudiesT3m.o $<
$(OUTLIB)WTau3Mu_base.o: $(INCLUDEDIR)src/WTau3Mu_base.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)WTau3Mu_base.o $<
$(OUTLIB)WTau3Mu_tools.o: $(INCLUDEDIR)src/WTau3Mu_tools.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)WTau3Mu_tools.o $<
$(OUTLIB)WTau3Mu_analyzer.o: $(INCLUDEDIR)src/WTau3Mu_analyzer.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)WTau3Mu_analyzer.o $<
$(OUTLIB)DsPhiMuMuPi_base.o: $(INCLUDEDIR)src/DsPhiMuMuPi_base.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)DsPhiMuMuPi_base.o $<
$(OUTLIB)DsPhiMuMuPi_tools.o: $(INCLUDEDIR)src/DsPhiMuMuPi_tools.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)DsPhiMuMuPi_tools.o $<
$(OUTLIB)DsPhiMuMuPi_analyzer.o: $(INCLUDEDIR)src/DsPhiMuMuPi_analyzer.C
		$(CXX) $(CXXFLAGS) -c -I$(INCLUDEDIR) -o $(OUTLIB)DsPhiMuMuPi_analyzer.o $<
# ==================== GEN LEVEL ANALYSIS =========================

GenLev:$(INCLUDEDIR)src/GenLevelAnalysis.cc\
		$(OUTLIB)FileReader.o\
		$(OUTLIB)MCTau3Mu_base.o\
		$(OUTLIB)MCstudiesT3m.o\
		$(OUTLIB)DsPhiMuMuPi_base.o\
		$(OUTLIB)DsPhiMuMuPi_tools.o\
		$(OUTLIB)DsPhiMuMuPi_analyzer.o
		$(CXX) $(CXXFLAGS) -ldl -o $(OUTEXE)GenLevelAnalysis $(OUTLIB)/*.o $(GLIBS) $(LDFLAGS) $ $<
GenLev.clean:
			 rm -f GenLev 

# ==================== RECO LEVEL ANALYSIS =========================

RecoLev: $(INCLUDEDIR)src/RecoLevelAnalysis.cc\
		 $(OUTLIB)FileReader.o\
		 $(OUTLIB)Tau3Mu_base.o\
		 $(OUTLIB)prepStudiesT3m.o\
		 $(OUTLIB)DsPhiMuMuPi_base.o\
		 $(OUTLIB)DsPhiMuMuPi_tools.o\
		 $(OUTLIB)DsPhiMuMuPi_analyzer.o
		 $(CXX) $(CXXFLAGS) -ldl -o $(OUTEXE)RecoLevelAnalysis $(OUTLIB)/*.o $(GLIBS) $(LDFLAGS) $ $<
RecoLev.clean:
			 rm -f RecoLev 

# ==================== FULL ANALYSIS =========================

Analyzer : $(INCLUDEDIR)src/Analyzer_app.cc\
		 	$(OUTLIB)FileReader.o\
		 	$(OUTLIB)WTau3Mu_base.o\
		 	$(OUTLIB)WTau3Mu_tools.o\
		 	$(OUTLIB)WTau3Mu_analyzer.o\
		 	$(OUTLIB)DsPhiMuMuPi_base.o\
		 	$(OUTLIB)DsPhiMuMuPi_tools.o\
		 	$(OUTLIB)DsPhiMuMuPi_analyzer.o
		 	$(CXX) $(CXXFLAGS) -ldl -o $(OUTEXE)Analyzer_app $(OUTLIB)/*.o $(GLIBS) $(LDFLAGS) $ $<
Analyzer.clean:
			 rm -f Analyzer 
# =================================================================

clean:
		@echo "cleaning..."
		rm -f $(OUTLIB)*.o
		rm -f $(OUTEXE)*
		rm -f GenLev
		rm -f RecoLev
		rm -f Analyzer 

ana: Analyzer
gen: GenLev
reco: RecoLev

