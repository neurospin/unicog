#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-05-06 10:16 christophe@pallier.org>
"""
Quick start:
1. if you do not have it (it comes with brainvisa), install
soma_workflow from github.

2. copy all the spm batch files in the directory containing the
following python script; then run

python create_workflow_spm12batches.py

This must generate a file called 'spm12_batches.somawf'

3. Launch soma_workflow_gui on he command line in the same directory;
open the spm12_batches.somawf file and press 'submit'

Note: use your own PC if there are many cores. 
"""

import os, sys, glob
from soma_workflow.client import Job, Workflow, Helper

if len(sys.argv)==1:
    spm12_batches = glob.glob("*.mat")
else:
    spm12_batches = sys.argv[1:]

jobs = []
for b in spm12_batches:
    jobs.append(Job(command=["spm12", "run", os.path.abspath(b)], name=b))

workflow=Workflow(jobs)

Helper.serialize('spm12_batches.somawf', workflow)

print '''Now, you can open 'spm12_batches.somawf' in soma_workflow_gui and submit it'''
