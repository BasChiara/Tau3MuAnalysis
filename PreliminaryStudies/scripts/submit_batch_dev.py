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

def makeCondorFile(jobdir, srcFiles, options):
    dummy_exec = open(jobdir+'/dummy_exec.sh','w')
    dummy_exec.write('#!/bin/bash\n')
    dummy_exec.write('bash $*\n')
    dummy_exec.close()

    condor_file_name = jobdir+'/condor_submit.condor'
    condor_file = open(condor_file_name,'w')
    condor_file.write('''
Universe = vanilla
Executable = {de}
use_x509userproxy = true
Log        = {jd}/log/$(ProcId).log
Output     = {jd}/out/$(ProcId).out
Error      = {jd}/out/$(ProcId).error
getenv      = True
environment = "LS_SUBCWD={here}"
request_memory = 1000
+MaxRuntime = {rt}\n
'''.format(de=os.path.abspath(dummy_exec.name), jd=os.path.abspath(jobdir), rt=int(options.runtime*3600), here=os.environ['PWD'] ) )

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
    parser.add_option('-n', '--nfileperjob', action='store',     dest='nfileperjob',  help='split the jobs with n files read/batch job'                , default=1,   type='int')
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
    parser.add_option('-F', '--nfiles',      action='store',     dest='Nfiles',       help='number of files in a remote directory', default = 1000, type ='int')
    parser.add_option('--DsPhiPi',           action='store_true',dest='isDsPhiPi',    help='wether to run on the control channel Ds->Phi(MuMu)Pi', default = False)
    parser.add_option('--HLT_path',          choices=['HLT_DoubleMu', 'HLT_Tau3Mu', 'HLT_overlap'], dest='HLT_path', help='HLT path to use', default = 'HLT_Tau3Mu')
    (opt, args) = parser.parse_args()
    
    if len(args) != 1:
        print('[ERROR] no arguments were provided') 
        print(usage)
        sys.exit(1)
    print('[+] reading input from')
    [print('   > '+a) for a in args]

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

    # --> read the inputs
    inputfiles = inputListfile.readlines()
    ijob=0
    srcfiles = []
    while (len(inputfiles) > 0):
        L = []
        for line in range(min(opt.nfileperjob,len(inputfiles))):
            ntpfile = inputfiles.pop(0)
            if ntpfile.startswith("#"): continue
            ntpfile = ntpfile.rstrip('\n')
            if ntpfile != '':
                L.append(ntpfile+"\n")
        if not L : continue
        #print(L)
    
    # Njobs = len(L)
    # for ijob, file_dat in enumerate(L):

        # prepare the txt with root files
        icfgfilename = jobdir +"/cfg/tnp_"+str(ijob)+".txt"
        icfgfile = open(icfgfilename,'w')
        [icfgfile.write(lfile) for lfile in L]
        icfgfile.close()

        # prepare the script to run
        #rootoutputfile = dataset+'_'+str(ijob)+'.root'
        outdirtmp = '/tmp/'
        job_tag = dataset+'_'+str(ijob)
        rootoutputfile =  outdirtmp + ("WTau3Mu" if not opt.isDsPhiPi else "DsPhiMuMuPi")+ "_DATAanalyzer_" + job_tag + "_" + opt.HLT_path + ".root"  
        #if opt.scheduler=='condor':
        #    rootoutputfile = '/tmp/'+rootoutputfile
        print('[OUT] output saved as: ' + rootoutputfile)

        srcfilename = jobdir+"/src/submit_"+str(ijob)+".src"
        srcfile = open(srcfilename,'w')
        srcfile.write('#!/bin/bash\n')
        srcfile.write('cd '+pwd+'\n')
        srcfile.write('echo $PWD\n')
        Nf = 1000
        if (opt.Nfiles >= 1000) : opt.Nfiles = opt.Nfiles - 1000
        else : Nf = opt.Nfiles 
        print(' # %d job processing %d files '%(ijob, Nf))
        srcfile.write(opt.application+' '+icfgfilename+' '+outdirtmp+' DATA '+ job_tag +' '+ ("Tau3Mu" if not opt.isDsPhiPi else "DsPhiPi") + ' ' + str(Nf)+' \n')
        if(opt.eos!=''):    
            outdireos = opt.eos+dataset+'/'
            if not (os.path.isdir(outdireos)): os.system('mkdir -p '+outdireos)
            srcfile.write('cp '+rootoutputfile+' '+ outdireos +'\n')
            srcfile.write('rm '+rootoutputfile)
            print("[OUT] output saved in final destination : " + outdireos)
        srcfile.close()

        logfile = jobdir+"/log/"+dataset+"_"+str(ijob)+".log"
        scriptfile = pwd+"/"+srcfilename
        if opt.scheduler=='condor':
            srcfiles.append(srcfilename)
        else:
            print("ERROR. Only Condor scheduler available")
            sys.exit(1)

        ijob = ijob+1
        if(ijob==opt.testnjobs or opt.Nfiles < 1): break
        #if (opt.eventsperfile == -1): break

    if opt.scheduler=='condor':
        cf = makeCondorFile(jobdir,srcfiles,opt)
        subcmd = 'condor_submit {rf} '.format(rf = cf) #lunch jobs
        if opt.create:
            print('running dry, printing the commands...')
            print(subcmd)
        else:
            print('submitting for real...')
            os.system(subcmd)

if __name__ == "__main__":
        main()
