import ROOT

import os
import sys
import glob
import optparse
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from plots.color_text import color_text as ct

from colorama import init
from termcolor import colored

access_error = 'Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error:'
output_error = 'Transport endpoint is not connected'
execution_error = '*** Break *** segmentation violation'

############# USAGE #############

usage = '''usage: %prog [opts] dataset'''
parser = optparse.OptionParser(usage=usage)

parser.add_option('--job_dir',                              help='job-report directory'                , default='./job_report/')
parser.add_option('--out_dir',                              help='root ntuples directory'              , default='/eos/user/c/cbasile/Tau3MuRun3/data/analyzer_prod/')
parser.add_option('--era',                                  help='era ID to process'                   , default='2022Cv1')
parser.add_option('--resubmit', action='store_true',        help='resubmit failed jobs'                )
parser.add_option('--no_out',   action='store_true',        help='check if there is the output file')
parser.add_option('--dryrun',   action='store_true',        help='when --resubmit -> dryrun mode')
parser.add_option('--debug',    action='store_true',        help='useful printout'                     ) 


(opt, args) = parser.parse_args()

# list of job-report directories 
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
        print(f'{ct.RED}[ERROR]{ct.END} found multiple job-report... cancel the unwanted directoriries')
        [print(f' - {d}') for d in matching]
        exit(-1)

# check if the job directories are empty
for d in job_dir_list :
    if not glob.glob(d):
        print(f'{ct.RED}[ERROR]{ct.END} job directory {d} is empty')
        exit(-1)

print(f'[+] running checks on  the following reports')
[print(f' - {r}') for r in job_dir_list]
print('----------------------------------------------')

# *** CHECKING JOBS ***
for d in job_dir_list :

    # count the number of submitted/successful/failed jobs 
    log_files       = os.listdir(d+'/log/')
    Nsub_jobs  = len(log_files)
    Nsuccesful_jobs = 0
    Failed_jobID    = []
    if(opt.debug) : print(log_files)
    print(f'= {Nsub_jobs} submitted jobs in {d}')
    
    # loop over the jobs
    N_processed_events = 0
    N_saved_events = 0
    for ijob in range(Nsub_jobs) :
        job_is_ok = True
        if(opt.debug) :print(f'\tcheck job {ijob}/{Nsub_jobs}')

        # JOB OUTPUT
        src_file    = d + '/src/submit_' + str(ijob) + '.src'
        stdout_file = d + '/out/' + str(ijob) + '.out'
        error_file  = d + '/out/' + str(ijob) + '.error'
        # read the job stdout file
        if not os.path.isfile(stdout_file):
            print(f'{ct.YELLOW}[WARNING]{ct.END} out file {stdout_file} not found')
            job_is_ok = False
            if opt.no_out : Failed_jobID.append(ijob)
            continue
        # read the error file
        N_access_error = 0
        if os.path.isfile(error_file):
            error_file_lines = open(error_file).readlines()
            for l in error_file_lines:
                if (access_error in l and ijob < (Nsub_jobs-1)): # last job can have access error
                    N_access_error += 1
                elif execution_error in l:
                    job_is_ok = False
                    print(f'{ct.RED}[ERROR]{ct.END} job {ijob} has a segmentation violation')
                    break
                elif output_error in l:
                    job_is_ok = False
                    print(f'{ct.RED}[ERROR]{ct.END} job {ijob} has a transport endpoint error')
                    break
            if N_access_error : print(f'{ct.YELLOW}[WARNING]{ct.END} {N_access_error} access error in job {ijob}')
            
            if not job_is_ok : 
                Failed_jobID.append(ijob)
                continue

        else:
            print(f'{ct.YELLOW}[WARNING]{ct.END} error file {error_file} not found')

        # check if the output.root is produced
        src_file_lines = open(src_file).readlines()
        for line in src_file_lines:
    
            # find in the job src file the line with the output.root
            if not line.startswith("cp"): continue
            strings       = line.split() 
            out_file_root = strings[-1] + os.path.basename(strings[1])
            # out-file is OK :)
            if (out_file_root.endswith('.root') and os.path.isfile(out_file_root) ):
                if(opt.debug) : print(f' jobID {ijob} output exists :)')
                
                # save number of processed/saved events
                stdout_file_lines = open(stdout_file).readlines()
                for l in stdout_file_lines:
                    l = l.rstrip('\n')
                    l = l.lstrip()
                    # processed events
                    if l.startswith('Events processed'):
                        nevts = int(l.split()[-1])
                        if nevts > 0 : 
                            N_processed_events += nevts
                            if(opt.debug): print(f'\tevents processed {nevts}')
                        else : 
                            job_is_ok = False
                            print(f'   {ct.RED}[WARNING]{ct.END} : job {ijob} has {nevts} processed events')
                    # saved events
                    if l.startswith('Events -> HLT_DoubleMu reinforcement'): 
                        nevts = int(l.split()[-1])
                        if nevts > 0 : 
                            N_saved_events += nevts
                            if(opt.debug): print(f'\tevents saved {nevts}')
                        else :
                            job_is_ok = False
                            print(f'   {ct.RED}[WARNING]{ct.END} : job {ijob} has {nevts} saved events')
            # out-file is KO :(
            else:
                job_is_ok = False
                print(f'[!] jobID {ijob} output not found :(')
            
            # single job outcome
            if job_is_ok : Nsuccesful_jobs += 1
            else : Failed_jobID.append(ijob)

    # ** final report
    
    print(colored(f' succesful jobs : {Nsuccesful_jobs}/{Nsub_jobs}', 'red' if Nsuccesful_jobs/Nsub_jobs < 1.0 else 'green' ))
    
    if Failed_jobID :
        print(f'\t {len(Failed_jobID)}/{Nsub_jobs} failed job(s) -> ID : {Failed_jobID}\n')
    print(f'\ttotal processed events : {N_processed_events}')
    print(f'\ttotal saved events     : {N_saved_events}')
    print('\n')

    # *** RESUBMITTING JOBS ***
    if (opt.resubmit and Failed_jobID) :
        print('****** resubmitting failed jobs ******')
        condor_script       = d + '/condor_submit.condor'
        # save the original condor script
        with open(condor_script, 'r') as f:
            lines = f.readlines()
        f.close()
        # loop on the failed jobs
        for j in Failed_jobID:
            # copy only the condor env setup
            job_src             = d + '/src/submit_' + str(j) + '.src' 
            resub_condor_script = d + '/condor_resub_'+ str(j) +'.condor'
            new_lines =  [ l.replace('$(ProcId)', str(j)) for l in lines]
            with open(resub_condor_script, 'w') as f: 
                # put the correct $(ProcId)
                [ f.write(l) for l in new_lines if not ('arguments' in l or 'queue' in l)  ]
                # job to resub
                f.write(f'arguments = {os.path.abspath(job_src)}\n')
                f.write('queue 1 \n')   
            f.close()
            # resubmit the jobs
            command = f'condor_submit {resub_condor_script}'
            if(opt.dryrun) : print(f'{ct.BOLD}[DRYRUN]{ct.END} {command}')
            else :
                print(f'{ct.BOLD}[EXEC]{ct.END} resubmitting jobs -> {command}') 
                os.system(command)

    print('\n')
