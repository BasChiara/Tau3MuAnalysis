#! /usr/bin/env python

import os
import sys
import re
import time
import optparse
import datetime
import numpy as np
sys.path.append('../../')
import scripts.condor_job_manager as cjm

def main():
    
    ############# USAGE #############

    # --defaults
    executable = 'NLO_Wkinematics_correction'
    year_era_list = ['2022preEE', '2022EE', '2023preBPix', '2023BPix']
    year_era_list = ['2022EE']
    NLO_file_list = [
        #'fileLists/WtoLNu-2Jets_Run3Summer22preEENanoAODv12_fileList.txt',
        #'fileLists/WtoLNu-2Jets_Run3Summer22EENanoAODv12_fileList.txt',
        #'fileLists/WtoLNu-2Jets_Run3Summer23preBPixNanoAODv12_fileList.txt',
        #'fileLists/WtoLNu-2Jets_Run3Summer23BPixNanoAODv12_fileList.txt',
        #'fileLists/DYto2L-2Jets_Run3Summer22preEENanoAODv12_fileList.txt',
        'fileLists/DYto2L-2Jets_Run3Summer22EENanoAODv12-TAUbugfix_fileList.txt',
        #'fileLists/DYto2L-2Jets_Run3Summer23preBPixNanoAODv12_fileList.txt',
        #'fileLists/DYto2L-2Jets_Run3Summer23BPixNanoAODv12_fileList.txt',
    ]
    NLO_file_dict = dict(zip(year_era_list, NLO_file_list))
    LO_file_list = [
        #'fileLists/WtoTauNu_Tauto3Mu_Run3Summer22preEENanoAODv12_fileList.txt',
        #'fileLists/WtoTauNu_Tauto3Mu_Run3Summer22EENanoAODv12_fileList.txt',
        #'fileLists/WtoTauNu_Tauto3Mu_Run3Summer23preBPixNanoAODv12_fileList.txt',
        #'fileLists/WtoTauNu_Tauto3Mu_Run3Summer23BPixNanoAODv12_fileList.txt',
        #'fileLists/Zto2Tauto3Mu_Run3Summer22preEENanoAODv12_fileList.txt',
        'fileLists/Zto2Tauto3Mu_Run3Summer22EENanoAODv12_fileList.txt',
        #'fileLists/Zto2Tauto3Mu_Run3Summer23preBPixNanoAODv12_fileList.txt',
        #'fileLists/Zto2Tauto3Mu_Run3Summer23BPixNanoAODv12_fileList.txt',
    ]
    LO_file_dict = dict(zip(year_era_list, LO_file_list))

    # jobs params
    parser = cjm.make_condor_parser( executable= executable )
    # application params
    parser.add_option('--tag',               action='store',            dest='tag',             help='tag that identifies the task')
    parser.add_option('--V_pdgID',           action='store',            dest='V_pdgID',         help='PDG ID of vector boson W=24 or Z=23',                               default = 'W')
    parser.add_option('--plot_outdir',       action='store',            dest='plot_outdir',     help='copy the output plot in the specified EOS path',          default = '')
    parser.add_option('--debug',             action='store_true',       dest='debug',           help='useful printouts',                                        default = False)
    (opt, args) = parser.parse_args()
 
    print("\n\n")

    ##### INPUT/OUTPUT #####
    now = datetime.datetime.now()
    job_tag = f'NLOreweight_{opt.tag}'
    
    # --> setup the ouput directory
    if not os.path.isdir(opt.plot_outdir):
        os.system(f'mkdir -p {opt.plot_outdir}')
        #os.system(f'cp ~/public/index.php {opt.plot_outdir}')
        print(f'[+] output-directory created : {opt.plot_outdir}')
    else:
        print(f'[+] output-directory already exists : {opt.plot_outdir}')

    # --> set-up the report directory
    jobdir = f'./{opt.prefix}/NLOreweight_{opt.tag}_'+ now.strftime("%Y%m%d_%H%M%S")
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

    srcfiles = []
    for i, year in enumerate(year_era_list):
    
        # --> setup the command sequence to run
        src_filename = f'{jobdir}/src/submit_{str(i)}.src'
        with open(src_filename, 'w') as src:
            src.write(
            '''
#!/bin/bash\n
cd $T3M_ANA
cmsenv
cd {pwd} 
echo $PWD\n

./NLO_Wkinematics_correction --lo {f_lo} --nlo {f_nlo} -y {year} -o {out} -v {pdgID}
    '''.format(
        pwd     = pwd,
        f_lo    = LO_file_dict[year],
        f_nlo   = NLO_file_dict[year],
        year    = year,
        out     = opt.plot_outdir,
        pdgID   = opt.V_pdgID
        )
        )
        
        srcfiles.append(src_filename)

   
    #######################################

    if opt.scheduler=='condor':
        cf = cjm.makeCondorFile(jobdir, srcfiles, job_tag, opt)
        subcmd = 'condor_submit {rf} '.format(rf = cf) #lunch jobs
        if opt.create:
            print('running dry, printing the commands...')
            print(subcmd)
        else:
            print('submitting for real...')
            os.system(subcmd)

if __name__ == "__main__":
        main()
