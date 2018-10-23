#!/usr/bin/python
# Example PBS cluster job submission in Python
 
from popen2 import popen2
import time
import os, sys, glob
 
# Loop over your jobs

list_scripts = sorted(glob.glob("/home/user/files/file*.py"))

for i in list_scripts:
    # Open a pipe to the qsub command.
    output, input = popen2('qsub')
     
    # Customize your options here
    job_name = "test_run4_%s" % i
    walltime = "1:00:00"
    processors = "nodes=1:ppn=1"
    command = "python %s" % i
    job_string = """#!/bin/bash
    #PBS -N %s
    #PBS -q Unicog_run4  
    #PBS -l walltime=%s
    #PBS -l %s
    cd "/home/user/output"
    %s""" % (job_name, walltime, processors, command)
     
    # Send job_string to qsub
    input.write(job_string)
    input.close()

