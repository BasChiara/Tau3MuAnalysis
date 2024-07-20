import os
import sys
import re
import time
import optparse
import datetime
import numpy as np

from condor_job_manager import *

def setup_executable(exe_file, LxyS, options):
    
    with open(exe_file, 'w') as exe :
        exe.write(
'''
#!/bin/bash\n
cd $T3M_ANA
cmsenv
cd {workdir}

echo **BDT hyperparameter optimization with Optuna**
python3 xgb_hp_optimizer.py --prep_sig {signal} --prep_bkg {data} --LxySign_cut {L_cut} -N {Ntrials} --tag {tag}
#echo **Train the model with optimal hyperparams**
#python3 xgb_trainer_kFold.py --prep_sig {signal} --prep_bkg {data} --LxySign_cut {L_cut} --opt_parameters {workdir}/optimization/BestTrial_OptunaXGBopt_LxyS{L_cut}_{tag}_{today}.json --plot_outdir {out_plt} --save_output --tag Optuna_{tag}

'''.format(
    pwd     = os.environ['PWD'],
    workdir = os.path.abspath(options.workdir),
    signal  = options.signal,
    data    = options.data,
    L_cut   = LxyS,
    Ntrials = options.Trials,
    tag     = options.tag,
    today   = datetime.date.today().strftime('%Y%b%d'),
    out_plt = options.plot_outdir,
        )
    )
    return


def setup_condor_jobs():

    executable = ''
    # add custom arguments
    parser = make_condor_parser( executable= executable )
    parser.add_option('-s','--signal',       action='store',            dest='signal',          help='signal sample')
    parser.add_option('-d','--data',         action='store',            dest='data',            help='data sample')
    parser.add_option('-L', '--LxySign_cut', action='append',           dest='LxySign_cut',     help='displacement cut to apply to data',                       )
    parser.add_option('-T', '--Trials',      action='store',            dest='Trials',          help='number of trials for Optuna',                             default='100')
    parser.add_option('--workdir',           action='store',            dest='workdir',         help='copy the output datacard and .root in the specified path',default='./mva/')
    parser.add_option('--tag',               action='store',            dest='tag',             help='tag that identifies the task')
    parser.add_option('--plot_outdir',       action='store',            dest='plot_outdir',     help='copy the output plot in the specified EOS path',          default = '')
    parser.add_option('--debug',             action='store_true',       dest='debug',           help='useful printouts',                                        default = False)
    (opt, args) = parser.parse_args()
    print('\n')

    # input/output
    now = datetime.datetime.now()
    if len(opt.LxySign_cut) < 2 :
        job_tag = f'BDT_Optuna_LxyS{opt.LxySign_cut[0]}' + ('_' + opt.tag if opt.tag else '')
    else :
        job_tag = f'BDT_Optuna_LxyS{opt.LxySign_cut[0]}_{opt.LxySign_cut[-1]}' + ('_' + opt.tag if opt.tag else '')


    # --> set-up the report directory
    jobdir = f'./{opt.prefix}/{job_tag}_'+ now.strftime("%Y%m%d_%H%M%S")
    make_report_folder(jobdir)

    #look for the current directory
    pwd = os.environ['PWD']
    scramarch = os.environ['SCRAM_ARCH']

    # --> split the jobs

    disp_cut_list = [1.4, 1.9, 2.0, 2.1]
    disp_cut_list = opt.LxySign_cut 
    print(f'\n run optimization for Lxy significance working points : {disp_cut_list}')
    srcfiles = []
    for i, cut in enumerate(disp_cut_list):
        print(f'\t* setup job Lxy/s > {cut}')
        src_filename = f'{jobdir}/src/submit_{str(i)}.src'
        setup_executable(src_filename, cut, opt)
        srcfiles.append(src_filename)
    
    if opt.scheduler=='condor':
        cf = makeCondorFile(jobdir, srcfiles, job_tag, opt)
        subcmd = 'condor_submit {rf} '.format(rf = cf) #lunch jobs
        if opt.create:
            print('\n[i] running dry, printing the commands...')
            print(subcmd)
        else:
            print('\n[i] submitting for real...')
            os.system(subcmd)



if __name__ == "__main__":

    setup_condor_jobs()
