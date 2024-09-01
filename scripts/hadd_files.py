import os
import sys
import argparse
import glob
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from plots.color_text import color_text as ct

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
print(f' {ct.BOLD}[+]{ct.END} hadd files from '+ args.path)


out_file = args.path+'/'+args.app+'_'+args.dataset+'_'+args.year+args.era+'_'+args.hlt+'.root'
hadd_command = 'hadd -f -v 1 ' + out_file
N_datasetParkingDoubleMuonLowMass = 8
# /eos/user/c/cbasile/Tau3MuRun3/CMSSW_12_4_11/src/Tau3MuAnalysis/condor_data/ParkingDoubleMuonLowMass0_2022E/recoKinematicsT3m_ParkingDoubleMuonLowMass0_2022E_ 
for n in range(N_datasetParkingDoubleMuonLowMass):
   if (args.skip_files and n in args.skip_files): 
      print (f' {ct.PURPLE}[-]{ct.END} skip dataset '+args.dataset+str(n))         
      continue
   path_to_hadd = args.path+'/'+args.dataset+str(n)+'_'+args.year+args.era+'/'+args.app+'_'+args.dataset+str(n)+'_'+args.year+args.era+'_'+args.hlt+'_*.root'
   # number of file to hadd
   N_files = len(glob.glob(path_to_hadd))
   hadd_command += ' '+path_to_hadd
print(f'{ct.BOLD} [i]{ct.END} adding {N_files} files from {args.dataset}_{args.year}{args.era} to {out_file}')
#print(hadd_command)
os.system(hadd_command)

# check if the output file exists
print('\n... cecking if the output file exists')
if not os.path.isfile(out_file):
   print(f' {ct.RED}[ERROR]{ct.END} output file {out_file} does not exist')
   sys.exit(1)
else:
   print(f' {ct.GREEN}[+]{ct.END} output file {out_file} exists :)')
   sys.exit(0)
