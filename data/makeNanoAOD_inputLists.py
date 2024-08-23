import os
import glob
import argparse
import sys 
sys.path.append(os.path.abspath('..'))
from plots.color_text import color_text as ct

usage = 'usage : python3 makeNanoAOD_inoutLists.py'
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument('-p','--path', default = '/pnfs/roma1.infn.it/data/cms/store/group/phys_bphys/cbasile/Tau3MuNano2023_2024Jan24/', help = 'path containing the crab NanoAODs')
parser.add_argument('-s','--site',    choices=['T2_IT_Rome', 'eos'],   default = 'eos',                                                  help = 'site where the ntuples are stored')
parser.add_argument('-o','--output',                                default = '',                                                     help = 'location for ouput lists')
parser.add_argument('-d','--dataset',                               default = 'ParkingDoubleMuonLowMass',                             help = 'CMS dataset name' )
parser.add_argument('-y','--year',                                  default = '2022',                                                 help = 'data-taking year' )
parser.add_argument('-e','--era',                                   default = 'E',                                                    help = 'VdM data-taking era' )
parser.add_argument('-f','--filename',                              default = 'tau3muNANO_data_2024Jan24_',                           help = 'root file name' )
parser.add_argument('-k','--kfolders',                              default = 1, type = int,                                          help = 'root file name' )
parser.add_argument('-j','--jobtag',  nargs = '*', type = str,                                                                        help = 'jobtags' )
args = parser.parse_args()

if (args.site == 'eos'):
    base_path='/eos/cms/'
    xrootd_str='root://eoscms.cern.ch///'
elif (args.site == 'T2_IT_Rome'):
    base_path = '/pnfs/roma1.infn.it/data/cms/'
    xrootd_str = 'root://xrootd-cms.infn.it///'
else :
    raise Exception(f"{ct.RED}[ERROR]{ct.END} site %s not recognized"%args.site)

# retrive obtag list form eos
Ndatasets = 8
jobtag_list = []
if args.site == 'eos':
    for n in range(Ndatasets):
        data_dir = args.path + "/" + args.dataset + "%d/crab_data_Run%s%s_%d"%(n, args.year, args.era, n)
        # check if the directory exists
        if not os.path.isdir(data_dir):
            print(f' {ct.YELLOW}[WARNING]{ct.END} {data_dir} does not exist')
            jobtag_list.append('999999')
        else:
            jobtag_list.append(os.listdir(data_dir)[0])
    print("[=] jobtags list %s"%jobtag_list)
else:
    if (len(args.jobtag) != Ndatasets):
        raise Exception(f"{ct.RED}[ERROR]{ct.END} jobtags list should be of size %d, size is %d"%len(Ndatasets, args.jobtag))
    else :
        jobtag_list = args.jobtag

# remove site domain
print("[+] reading files from %s"%args.path)
ntuples_path = xrootd_str + args.path.removeprefix(base_path)
print(" base path with xrootd protocol %s" %ntuples_path)

# set output 
if os.path.isfile(args.output):
    raise Exception(f"{ct.RED}[ERROR]{ct.END} just specify the output folder")
if os.path.isdir(args.output):
    print("[OUT] save lists in existing directory %s"%args.output)
else :
    print("[OUT] creating directory %s"%args.output)
    os.makedirs(args.output)

for n, job in enumerate(jobtag_list):
    outfile = args.output + "/" + args.dataset + "%d_%s%s.txt"%(n, args.year, args.era)
    f = open(outfile, 'w+')
    for i in range(args.kfolders):
        line = ntuples_path + "/" + args.dataset +"%d/crab_data_Run%s%s_%d/%s/%04d/%s"%(n, args.year, args.era, n, job, i,args.filename) + (str(i) if i>0 else '') + '\n'
        f.write(line)
    print(f"{ct.GREEN}[=]{ct.END} written %s"%outfile)
    f.close()
