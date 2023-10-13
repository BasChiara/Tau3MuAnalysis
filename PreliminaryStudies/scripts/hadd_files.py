import os
import sys
import argparse

usage = 'usage : python hadd_file.py'
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument('-p','--path',    default = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/', help = 'path containing the files to hadd' )
parser.add_argument('-d','--dataset', default = 'ParkingDoubleMuonLowMass', help = 'CMS dataset name' )
parser.add_argument('-y','--year',    default = '2022', help = 'data-taking year' )
parser.add_argument('-e','--era',     default = 'E', help = 'VdM data-taking era' )
parser.add_argument('-a','--app',     default = 'recoKinematicsT3m', help = 'condor job application' )

args = parser.parse_args()
print(' [...] hadd files from '+ args.path)


out_file = args.path+'/'+args.app+'_'+args.dataset+'_'+args.year+args.era+'.root'
hadd_command = 'hadd -f ' + out_file
N_datasetParkingDoubleMuonLowMass = 8
# /eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/ParkingDoubleMuonLowMass0_2022E/recoKinematicsT3m_ParkingDoubleMuonLowMass0_2022E_ 
for n in range(N_datasetParkingDoubleMuonLowMass):
   path_to_hadd = args.path+'/'+args.dataset+str(n)+'_'+args.year+args.era+'/'+args.app+'_'+args.dataset+str(n)+'*.root'
   hadd_command += ' '+path_to_hadd

#print(hadd_command)
os.system(hadd_command)
