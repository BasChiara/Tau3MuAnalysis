import ROOT

import os
import glob
import optparse

from colorama import init
from termcolor import colored

############# USAGE #############

usage = '''usage: %prog [opts] dataset'''
parser = optparse.OptionParser(usage=usage)

parser.add_option('--job_dir',                              help='job-report directory'                , default='./job_report/')
parser.add_option('--out_dir',                              help='root ntuples directory'              , default='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/')
parser.add_option('--era',                                  help='era ID to process'                   , default='2022Cv1')
parser.add_option('--debug',    action='store_true',        help='useful printout'                     ) 


(opt, args) = parser.parse_args()

# make the job directories list
base_name = 'Analyzer_ParkingDoubleMuonLowMass'
Ndataset = 8
job_dir_list = []
for i_dataset in range(Ndataset):
    matching = glob.glob(f'{opt.job_dir}/{base_name}{str(i_dataset)}_{opt.era}_*') 
    
    if len(matching) == 1 :
       job_dir_list.append(matching[0]) 
    elif len(matching) == 0 :
        print(f'[INFO] found no job-report for {base_name}{str(i_dataset)}')
    elif len(matching) > 1:
        print('[ERROR] found multiple job-report... cancel the unwanted directoriries')
        [print(f' - {d}') for d in matching]
        exit(-1)
# check are not empty
for d in job_dir_list :
    if not glob.glob(d):
        print(f'[ERROR] job directory {d} is empty')
        exit(-1)

print(f'[+] running checks on  the following reports')
[print(f' - {r}') for r in job_dir_list]
print('----------------------------------------------')

for d in job_dir_list :
    # jobs lounched
    log_files       = os.listdir(d+'/log/')
    Nlounched_jobs  = len(log_files)
    Nsuccesful_jobs = 0
    Failed_jobID    = []
    if(opt.debug) : print(log_files)
    print(f'= {Nlounched_jobs} jobs in {d}')
    N_processed_events = 0
    N_saved_events = 0
    for ijob in range(Nlounched_jobs) :
        job_is_ok = True 
        if(opt.debug) :print(f'\tcheck job {ijob}/{Nlounched_jobs}')
        # check if the output .root exists 
        src_file = d + '/src/submit_' + str(ijob) + '.src'
        src_file_lines = open(src_file).readlines()
        for line in src_file_lines: 
            if not line.startswith("cp"): continue
            strings       = line.split() 
            out_file_root = strings[-1] + os.path.basename(strings[1])
            # out-file is OK :)
            if (out_file_root.endswith('.root') and os.path.isfile(out_file_root) ):
                if(opt.debug) : print(f' jobID {ijob} output exists :)')
                report_file = d + '/out/' + str(ijob) + '.out' 
                report_file_lines = open(report_file).readlines()
                for l in report_file_lines:
                    l = l.rstrip('\n')
                    l = l.lstrip()
                    # retrive number of processed events
                    if l.startswith('Events processed'):
                        nevts = int(l.split()[-1])
                        if nevts > 0 : 
                            N_processed_events += nevts
                            if(opt.debug): print(f'\tevents processed {nevts}')
                        else : 
                            job_is_ok = False
                            print(f'WARNING : job {ijob} has {nevts} processed events')
                    # retrive number of saved events
                    if l.startswith('Events after HLT_DoubleMu reinforcement'): 
                        nevts = int(l.split()[-1])
                        if nevts > 0 : 
                            N_saved_events += nevts
                            if(opt.debug): print(f'\tevents saved {nevts}')
                        else :
                            job_is_ok = False
                            print(f'WARNING : job {ijob} has {nevts} saved events')
            # out-file is KO :(
            else:
                job_is_ok = False
                Failed_jobID.append(ijob)
                print(f'[!] jobID {ijob} output not found :(')
            if job_is_ok : Nsuccesful_jobs += 1

    # ** final report
    
    print(colored(f' succesful jobs : {Nsuccesful_jobs}/{Nlounched_jobs}', 'red' if Nsuccesful_jobs/Nlounched_jobs < 1.0 else 'green' ))
    
    if Failed_jobID :
        print(f'\tfound {len(Failed_jobID)}/{Nlounched_jobs} failed jobs')
        [print('\t%d'%j) for j in Failed_jobID]
    print(f'\ttotal processed events : {N_processed_events}')
    print(f'\ttotal saved events     : {N_saved_events}')
    print('\n')
    
