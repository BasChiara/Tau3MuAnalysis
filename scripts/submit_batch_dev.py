# 
#! /usr/bin/env python
#
# !! TO DO BEFORE SUBMITTING ...
#       in the release
#           $cmsenv
#
#       if files are accessed via Grid, before you need:
#           $ source ~/setup_env.sh
#       to initialize the proxy and place them in te proper directory
#
# example: python scripts/submit_batch.py -c -N -1 -n 1 -p testtnp myfiles.txt
# -c = just create and do not submit (remove it to submit)
# this is to write 1 job per file in the dataset (-N = run on all the events in a file; -n = 1job/file)
#
# THIS ONE I USE --> to copy the output on EOS: python submit_batch.py -c -N -1 -n 1 -p testtnp --eos=ok myfiles.txt
#
#
# myfiles.txt   contains the paths to the root files I need (./data/CharmoniumUL_Run2017B.txt ecc..)


import os
import sys
import re
import time
import optparse
import datetime
import numpy as np

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
getenv      = True
environment = "LS_SUBCWD={here}"
request_memory = 5M 
+MaxRuntime = {rt}\n
+JobBatchName = "{bn}"\n
'''.format(de=os.path.abspath(dummy_exec.name), jd=os.path.abspath(jobdir), rt=int(options.runtime*3600), bn=batch_name,here=os.environ['PWD'] ) )

    for sf in srcFiles:
        condor_file.write('arguments = {sf} \nqueue 1 \n\n'.format(sf=os.path.abspath(sf)))

    condor_file.close()
    return condor_file_name

def main():
    
    ############# USAGE #############

    usage = '''usage: %prog [opts] dataset'''
    parser = optparse.OptionParser(usage=usage)

    # --defaults
    executable = './bin/Analyzer_app'
    now = datetime.datetime.now()
    defaultoutputdir='./jobReport'

    # jobs params
    parser.add_option('-q', '--queue',       action='store',     dest='queue',        help='run in batch in queue specified as option (default -q 8nh)', default='8nh')
    parser.add_option('-n', '--nfileperjob', action='store',     dest='nfileperjob',  help='number of files processed by the single job'                , default=50,   type='int')
    parser.add_option('-s', '--dirpersplit', action='store',     dest='dirpersplit',  help='number of directories processed together'                   , default=1,   type='int')
    parser.add_option('-p', '--prefix',      action='store',     dest='prefix',       help='the prefix to be added to the output'                      , default=defaultoutputdir)
    parser.add_option('-a', '--application', action='store',     dest='application',  help='the executable to be run'                                  , default=executable)
    parser.add_option('-c', '--create',      action='store_true',dest='create',       help='create only the jobs, do not submit them'                  , default=False)
    parser.add_option('-t', '--testnjobs',   action='store',     dest='testnjobs',    help='submit only the first n jobs'                              , default=1000000, type='int')
    parser.add_option('-N', '--neventsjob',  action='store',     dest='neventsjob',   help='split the jobs with n events  / batch job'                 , default=200,   type='int')
    parser.add_option('-T', '--eventsperfile',action='store',    dest='eventsperfile',help='number of events per input file'                        , default=-1,   type='int')
    parser.add_option('-r', '--runtime',     action='store',     dest='runtime',      help='New runtime for condor resubmission in hours. default None: will take the original one.', default=8, type=int);
    parser.add_option('--scheduler',         action='store',     dest='scheduler',    help='select the batch scheduler (lsf,condor). Default=condor'   , default='condor')
    # application params
    parser.add_option('--eos',               action='store',     dest='eos',          help='copy the output in the specified EOS path'                 , default='')
    parser.add_option('-F', '--Nfiles',      action='store',     dest='Nfiles',       help='number of files in a remote directory', default = 1000, type ='int')
    parser.add_option('--DsPhiPi',           action='store_true',dest='isDsPhiPi',    help='wether to run on the control channel Ds->Phi(MuMu)Pi', default = False)
    parser.add_option('--HLT_path',          choices=['HLT_DoubleMu', 'HLT_Tau3Mu', 'HLT_overlap'], dest='HLT_path', help='HLT path to use', default = 'HLT_Tau3Mu')
    parser.add_option('--debug',       action='store_true',dest='debug',        help='useful printouts', default = False)
    (opt, args) = parser.parse_args()
    
    if len(args) != 1:
        print('[ERROR] no arguments were provided') 
        print(usage)
        sys.exit(1)
    print('\n[+] reading input from')
    [print('   '+a) for a in args]
    print('---------------------------------------------------')

    ##### INPUT/OUTPUT #####
    # --> .txt files containg the ntuples path
    inputlist = args[0]
    dataset = os.path.splitext(os.path.basename(inputlist))[0]
    inputListfile=open(inputlist)
    
    # --> set-up the report directory
    jobdir = opt.prefix+'/Analyzer_'+dataset+'_'+ now.strftime("%Y%m%d_%H%M%S")
    os.system("mkdir -p "+jobdir)
    os.system("mkdir -p "+jobdir+"/log/")
    os.system("mkdir -p "+jobdir+"/out/")
    os.system("mkdir -p "+jobdir+"/src/")
    os.system("mkdir -p "+jobdir+"/cfg/")
    print('[LOG] report will be saved in '+ jobdir)

    #look for the current directory
    #######################################
    pwd = os.environ['PWD']
    scramarch = os.environ['SCRAM_ARCH']
    #######################################

   
    #  process xxx file per job
    max_file_dir    = 1000
    root_files_job  = opt.nfileperjob
    files_to_submit = opt.Nfiles
    exp_dir         = int(files_to_submit/max_file_dir) + (1 if files_to_submit%max_file_dir > 0 else 0)
    exp_job_number  = int(files_to_submit/root_files_job) + (1 if files_to_submit%root_files_job > 0 else 0)
    if opt.debug : print(f'\t> processing {files_to_submit} files in {exp_dir} directories')
    print(f'\tsplitting {files_to_submit} files in {exp_job_number} jobs')
    # --> parse input directories
    total_jobs = 0
    srcfiles = []
    inputfiles = inputListfile.readlines()
    while (len(inputfiles) > 0):
        L = []
        for line in range(min(opt.dirpersplit,len(inputfiles))):
            ntpfile = inputfiles.pop(0)
            if ntpfile.startswith("#"): continue
            ntpfile = ntpfile.rstrip('\n')
            if ntpfile != '':
                L.append(ntpfile+"\n")
        if not L : continue
        if opt.debug : print('[IN] files\n %s'%L)
        files_in_this_dir = np.min([files_to_submit, max_file_dir])
        Njobs = int(files_in_this_dir/root_files_job + (1 if files_in_this_dir%root_files_job > 0 else 0))
        if opt.debug : print(f'> preparing {Njobs} jobs for {files_in_this_dir} files')
        for ijob in range(Njobs):

            init_file  = ijob*root_files_job
            abs_job_id = total_jobs+ijob
            print(f' jobID {abs_job_id} processing {root_files_job} files starting from {init_file}')

            # prepare the txt with root files
            icfgfilename = jobdir +"/cfg/tnp_"+str(abs_job_id)+".txt"
            icfgfile = open(icfgfilename,'w')
            [icfgfile.write(lfile) for lfile in L]
            icfgfile.close()

            # temporary output location
            outdirtmp = '/tmp/'
            #job_tag = dataset+'_'+str(abs_job_id)
            job_tag = '_'.join([dataset, opt.HLT_path, str(abs_job_id)])
            #rootoutputfile =  outdirtmp + ("WTau3Mu" if not opt.isDsPhiPi else "DsPhiMuMuPi")+ "_DATAanalyzer_" + job_tag + "_" + opt.HLT_path + ".root"  
            rootoutputfile =  outdirtmp + ("WTau3Mu" if not opt.isDsPhiPi else "DsPhiMuMuPi")+ "_DATAanalyzer_" + job_tag + ".root"  
            
            print('  [OUT] output saved temporarly as : ' + rootoutputfile)
            # script to run
            srcfilename = jobdir+"/src/submit_"+str(abs_job_id)+".src"
            srcfile = open(srcfilename,'w')
            srcfile.write('#!/bin/bash\n')
            srcfile.write('cd '+pwd+'\n')
            srcfile.write('echo $PWD\n')
            srcfile.write(opt.application+' -i '+icfgfilename+' -o '+outdirtmp+' -d DATA -y '+ dataset +' -a '+ ("Tau3Mu" if not opt.isDsPhiPi else "DsPhiPi") + ' -N ' + str(root_files_job)+' -f ' + str(init_file) + ' -t ' + str(abs_job_id) + '\n')
            if(opt.eos!=''):    
                outdireos = opt.eos+dataset+'/'
                if not (os.path.isdir(outdireos)): os.system('mkdir -p '+outdireos)
                srcfile.write('cp '+rootoutputfile+' '+ outdireos +'\n')
                srcfile.write('rm '+rootoutputfile)
                print("  [OUT] output saved in final destination : " + outdireos)
            srcfile.close()

            logfile = jobdir+"/log/"+dataset+"_"+str(abs_job_id)+".log"
            scriptfile = pwd+"/"+srcfilename
            if opt.scheduler=='condor':
                srcfiles.append(srcfilename)
            else:
                print("ERROR. Only Condor scheduler available")
                sys.exit(1)

            #ijob = ijob+1        
            if(ijob==opt.testnjobs or files_to_submit < 1): break
            #if (opt.eventsperfile == -1): break
        
        total_jobs += Njobs
        files_to_submit -= files_in_this_dir

    if opt.scheduler=='condor':
        cf = makeCondorFile(jobdir, srcfiles, dataset, opt)
        subcmd = 'condor_submit {rf} '.format(rf = cf) #lunch jobs
        if opt.create:
            print('running dry, printing the commands...')
            print(subcmd)
        else:
            print('submitting for real...')
            os.system(subcmd)

if __name__ == "__main__":
        main()
