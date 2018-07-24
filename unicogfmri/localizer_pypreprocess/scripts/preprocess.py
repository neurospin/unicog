# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:49:36 2018

@author: id983365
"""

import sys

from pypreprocess.nipype_preproc_spm_utils import do_subjects_preproc


# preproc
def preproc(jobfile):
    '''Launch the preprocesses on data with pypreprocess python module.
    See: https://github.com/neurospin/pypreprocess/
    Tape: python preprocess.py <jobfile>

    Keyword arguments:
    jobfile -- text file for initialisation of processes step and configuration
    '''
    do_subjects_preproc(jobfile, report=True)

if __name__ == '__main__':
    #File containing configuration for preprocessing the data
    jobfile=sys.argv[1]

    #Preproc
    subject_data = preproc(jobfile)
 