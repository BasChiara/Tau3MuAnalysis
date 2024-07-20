#! /usr/bin/env python
import os
import optparse

# general way to set-up a HTCondor job

def makeCondorFile(jobdir, srcFiles, batch_name, options):
    dummy_exec = open(jobdir+'/dummy_exec.sh','w')
    dummy_exec.write('#!/bin/bash\n')
    dummy_exec.write('bash $*\n')
    dummy_exec.close()

    condor_file_name = jobdir+'/condor_submit.condor'
    condor_file = open(condor_file_name,'w')
    condor_file.write('''
universe = vanilla
executable = {de}
use_x509userproxy = true

log        = {jd}/log/$(ProcId).log
output     = {jd}/out/$(ProcId).out
error      = {jd}/out/$(ProcId).error

getenv       = True
environment  = "LS_SUBCWD={here}"

{gpu}
request_cpus   = {cpu}
request_memory = {mem}


+MaxRuntime = {rt}
+JobBatchName = "{bn}"\n
'''.format(
    de      =os.path.abspath(dummy_exec.name), 
    jd      =os.path.abspath(jobdir),
    here    =os.environ['PWD'],
    cpu     =str(options.cpu),
    gpu     =(f'request_gpus   = {str(options.gpu)}' if options.gpu>0 else ''),
    mem     =options.memory,
    rt      =int(options.runtime*3600), 
    bn      =batch_name, 
    )
    )

    for sf in srcFiles:
        condor_file.write('arguments = {sf} \nqueue 1 \n\n'.format(sf=os.path.abspath(sf)))

    condor_file.close()
    return condor_file_name


def make_condor_parser(prefix = 'job_report', executable = './dummy.sh'):

    parser = optparse.OptionParser()
    defaultoutputdir = prefix
     
    # jobs params
    parser.add_option('-q', '--queue',       action='store',     dest='queue',        help='run in batch in queue specified as option (default -q 8nh)', default='8nh')
    parser.add_option('-n', '--nfileperjob', action='store',     dest='nfileperjob',  help='number of files processed by the single job'                , default=50,   type='int')
    parser.add_option('-p', '--prefix',      action='store',     dest='prefix',       help='the prefix to be added to the output'                      , default=defaultoutputdir)
    parser.add_option('-a', '--application', action='store',     dest='application',  help='the executable to be run'                                  , default=executable)
    parser.add_option('-c', '--create',      action='store_true',dest='create',       help='create only the jobs, do not submit them'                  , default=False)
    parser.add_option('-t', '--testnjobs',   action='store',     dest='testnjobs',    help='submit only the first n jobs'                              , default=1000000, type='int')
    parser.add_option('-r', '--runtime',     action='store',     dest='runtime',      help='New runtime for condor resubmission in hours. default None: will take the original one.', default=8, type=int)
    parser.add_option('--cpu',               action='store',     dest='cpu',          help='Request CPU(s)', default=1, type=int)
    parser.add_option('--gpu',               action='store',     dest='gpu',          help='Request GPU(s)', default=0, type=int)
    parser.add_option('-M', '--memory',      action='store',     dest='memory',       help='Request memory(MB)', default='5M')
    parser.add_option('--scheduler',         action='store',     dest='scheduler',    help='select the batch scheduler (lsf,condor). Default=condor'   , default='condor')

    return parser


def make_report_folder(jobdir = 'job_report'):
    
    os.system("mkdir -p "+jobdir)
    os.system("mkdir -p "+jobdir+"/log/")
    os.system("mkdir -p "+jobdir+"/out/")
    os.system("mkdir -p "+jobdir+"/src/")
    os.system("mkdir -p "+jobdir+"/cfg/")
    try: 
        os.path.isdir(jobdir)
    except:
        print('[ERROR] cannot create jobs-report directory ' + jobdir)
        exit()
    else :
        print('[i] jobs-report will be saved in '+ jobdir)
        return

