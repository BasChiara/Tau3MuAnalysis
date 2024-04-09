import os
import sys
import argparse

usage = 'usage : python hadd_file.py'
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument('-p','--path',    default = '/eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/Run3_2022', help = 'path containing the files to hadd' )
parser.add_argument('-d','--dataset', default = 'ParkingDoubleMuonLowMass', help = 'CMS dataset name' )
parser.add_argument('-y','--year',    default = '2022', help = 'data-taking year' )
parser.add_argument('-e','--era',     default = 'E', help = 'VdM data-taking era' )
parser.add_argument('-a','--app',     default = 'recoKinematicsT3m', help = 'condor job application' )
parser.add_argument('--hlt',          default = 'HLT_Tau3Mu', help = 'hlt applied in the ntuples' )
parser.add_argument('--skip_files',   nargs = '*', type = int, help = 'dataset to skip' )

args = parser.parse_args()
print(' [...] hadd files from '+ args.path)
if args.skip_files:
   print('  [-] skip datasets '+ str(args.skip_files)[1:-1])


out_file = args.path+'/'+args.app+'_'+args.dataset+'_'+args.year+args.era+'_'+args.hlt+'.root'
hadd_command = 'hadd -f ' + out_file
N_datasetParkingDoubleMuonLowMass = 8
# /eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/ParkingDoubleMuonLowMass0_2022E/recoKinematicsT3m_ParkingDoubleMuonLowMass0_2022E_ 
for n in range(N_datasetParkingDoubleMuonLowMass):
   if (args.skip_files and n in args.skip_files): 
      print (' [-] skip dataset '+args.dataset+str(n))         
      continue
   path_to_hadd = args.path+'/'+args.dataset+str(n)+'_'+args.year+args.era+'/'+args.app+'_'+args.dataset+str(n)+'*'+args.hlt+'.root'
   hadd_command += ' '+path_to_hadd

#print(hadd_command)
os.system(hadd_command)
