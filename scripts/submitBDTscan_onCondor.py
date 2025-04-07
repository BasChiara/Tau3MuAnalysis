#! /usr/bin/env python

import os
import sys
import re
import time
import optparse
import datetime
import numpy as np

from condor_job_manager import *


def main():
    
    ############# USAGE #############

    # --defaults
    executable = 'to_run_fit_and_limits_condor'

    # jobs params
    parser = make_condor_parser( executable= executable )
    # application params
    parser.add_option('-s','--signal',       action='store',            dest='signal',          help='signal sample')
    parser.add_option('-d','--data',         action='store',            dest='data',            help='data sample')
    parser.add_option('--workdir',           action='store',            dest='workdir',         help='copy the output datacard and .root in the specified path')
    parser.add_option('--tag',               action='store',            dest='tag',             help='tag that identifies the task')
    parser.add_option('--plot_outdir',       action='store',            dest='plot_outdir',             help='copy the output plot in the specified EOS path',          default = '')
    parser.add_option('--category',          choices=['A', 'B', 'C', 'ABC'],   dest='category',        help='events category',                                         default = 'A')
    parser.add_option('--year',              choices=['22', '23', '24'],dest='year',            help='data taking year',                                        default = '22')
    parser.add_option('--debug',             action='store_true',       dest='debug',           help='useful printouts',                                        default = False)
    parser.add_option('--BDTmin',            action='store',            dest='BDTmin',          help='minimum BDT value',                                       default = 0.9800) 
    parser.add_option('--BDTmax',            action='store',            dest='BDTmax',          help='maximum BDT value',                                       default = 0.9980)
    parser.add_option('--BDTstep',           action='store',            dest='BDTstep',         help='step for BDT scan',                                       default = 0.0010)
    (opt, args) = parser.parse_args()

    print("\n\n")

    ##### INPUT/OUTPUT #####
    now = datetime.datetime.now()
    job_tag = f'BDTopt_20{opt.year}_{opt.tag}'
    categories = []
    if opt.category == 'ABC':
        categories =['A', 'B', 'C']
    else : categories.append(opt.category)
    # --> setup the working directory
    if not os.path.isdir(opt.workdir):
        os.system(f'mkdir -p {opt.workdir}/input_combine')
        #os.system(f'mkdir -p {opt.workdir}/src')
        print(f'[+] working-directory created : {opt.workdir}')
    else:
        print(f'[+] working-directory aleardy exists : {opt.workdir}')
    
    # --> setup the ouput directory
    if not os.path.isdir(opt.plot_outdir):
        os.system(f'mkdir -p {opt.plot_outdir}')
        os.system(f'cp ~/public/index.php {opt.plot_outdir}')
        print(f'[+] plot-directory created : {opt.plot_outdir}')
    else:
        print(f'[+] plot-directory already exists : {opt.plot_outdir}')

    # --> set-up the report directory
    jobdir = f'./{opt.prefix}/BDToptimization_{opt.category}{opt.year}_{opt.tag}_'+ now.strftime("%Y%m%d_%H%M%S")
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
    for i, cat in enumerate(categories):
    
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

python3 models/Tau3Mu_fitSB.py --plot_outdir {eos} --combine_dir {workdir}/input_combine/ -s {signal} -d {data} --category {cat} -y {year} --tag {tag} --optim_bdt --save_ws --bkg_func expo --fix_w --BDTmin {bdtmin} --BDTmax {bdtmax} --BDTstep {bdtstep} --goff

    '''.format(
        pwd = pwd,
        tag     = opt.tag,
        eos     = opt.plot_outdir,
        workdir = opt.workdir,
        year    = opt.year,
        signal  = opt.signal,
        data    = opt.data,
        cat     = cat,
        bdtmin  = opt.BDTmin,
        bdtmax  = opt.BDTmax,
        bdtstep = opt.BDTstep
        )
            )
        srcfiles.append(src_filename)

   
    #######################################

    if opt.scheduler=='condor':
        cf = makeCondorFile(jobdir, srcfiles, job_tag, opt)
        subcmd = 'condor_submit {rf} '.format(rf = cf) #lunch jobs
        if opt.create:
            print('running dry, printing the commands...')
            print(subcmd)
        else:
            print('submitting for real...')
            os.system(subcmd)

if __name__ == "__main__":
        main()
