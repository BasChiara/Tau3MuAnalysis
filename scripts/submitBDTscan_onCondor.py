#! /usr/bin/env python

import os
import sys
import re
import time
import optparse
import datetime
import numpy as np

from condor_job_manager import *


def setup_executable(exe_file, category, options):

    # dump the text datacard
    with open(exe_file, 'w') as exe:
        exe.write(
    '''
#! /usr/bin/bash

WORK_DIR="{workdir}"
BASE_DIR="{basedir}/models/"

TAG="{tag}"

COMBINE_DIR="$WORK_DIR/input_combine"

EOS_DIR="{eos}"
YEAR="{year}"
SIGNAL="{signal}"
DATA="{data}"

CATEGORY="{cat}"

echo -e "\n"
echo    "|  CATEGORY $CATEGORY  |"
echo -e "\n"
echo 'TIME TO FIT'
python3 $BASE_DIR/Tau3Mu_fitSB.py --plot_outdir $EOS_DIR --combine_dir $COMBINE_DIR -s $SIGNAL -d $DATA --category $CATEGORY -y $YEAR --tag $TAG --optim_bdt --save_ws --bkg_func dynamic --BDTmin 0.9900 --BDTmax 0.9995 --BDTstep 0.0005
#echo 'TIME TO CALCULATE LIMITS'
# with AsymptoticLimits
#python3 $BASE_DIR/runBDTOptimCombine.py -i $COMBINE_DIR -o $EOS_DIR --scan_sensitivity input_combine/sensitivity_tree_bdt_scan_{full_tag}.root -d {full_tag} -n {full_tag} --BDTmin 0.9900 --BDTmax 0.9995 --BDTstep 0.0005 -s all
# with HybridNew 
#python3 $BASE_DIR/runBDTOptimCombine.py -i $COMBINE_DIR -o $EOS_DIR --scan_sensitivity input_combine/sensitivity_tree_bdt_scan_WTau3Mu_{full_tag}.root -d {full_tag} -n {full_tag} -M HybridNew --BDTmin 0.9900 --BDTmax 0.9995 --BDTstep 0.0005 -s all
#echo 'TIME TO COMPARE THE METHODS'
# compare the methods
python3 $BASE_DIR/compareLimitScan.py --inputs input_combine/Tau3MuCombine.{full_tag}_BDTscan.AsymptoticLimits.root --labels AsymptoticLimits --inputs input_combine/Tau3MuCombine.{full_tag}_BDTscan.HybridNew.root --labels HybridNew -o $EOS_DIR -d {full_tag} -n {full_tag} -y 20$YEAR -c $CATEGORY
    '''.format(
        workdir = os.path.abspath(options.workdir),
        basedir = os.getcwd(),
        tag     = options.tag,
        eos     = options.plot_outdir,
        year    = options.year,
        signal  = options.signal,
        data    = options.data,
        cat     = category,
        full_tag= f'WTau3Mu_{category}{options.year}_{options.tag}'
    )
    )

    os.system(f'chmod +x {exe_file}')
    
    return
    

    

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
    parser.add_option('--year',              choices=['22', '23'],      dest='year',            help='data taking year',                                        default = '22')
    parser.add_option('--debug',             action='store_true',       dest='debug',           help='useful printouts',                                        default = False)
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
    
        # --> setup the executable
        #executable_file_path = f'{opt.workdir}/{opt.application}_{cat}.sh'
        #setup_executable(executable_file_path, cat, opt)
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

python3 models/Tau3Mu_fitSB.py --plot_outdir {eos} --combine_dir {workdir}/input_combine -s {signal} -d {data} --category {cat} -y {year} --tag {tag} --optim_bdt --save_ws --bkg_func dynamic --BDTmin 0.9900 --BDTmax 0.9995 --BDTstep 0.0005
    '''.format(
        pwd = pwd,
        tag     = opt.tag,
        eos     = opt.plot_outdir,
        workdir = opt.workdir,
        year    = opt.year,
        signal  = opt.signal,
        data    = opt.data,
        cat     = cat,
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
