#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-05-06 10:16 christophe@pallier.org>

import os, sys, glob
from soma_workflow.client import Job, Workflow, Helper

if len(sys.argv)==1:
    spm8_batches = glob.glob("*.mat")
else:
    spm8_batches = sys.argv[1:]

jobs = []
for b in spm8_batches:
    jobs.append(Job(command=["spm12", "run", os.path.abspath(b)], name=b))

workflow=Workflow(jobs)

Helper.serialize('spm12_batches.somawf', workflow)

print '''Now, you can open 'spm12_batches.somawf' in soma_workflow_gui and submit it'''
