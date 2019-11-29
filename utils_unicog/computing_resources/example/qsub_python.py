# Example PBS cluster job submission in Python
import subprocess
import os, glob

# Loop over your jobs

list_scripts = sorted(glob.glob("/home/user/files/file*.py"))

for e, i in enumerate(list_scripts, 1):
    # Customize your options here
    job_name = "test_run4_%s" % os.path.basename(i)
    walltime = "1:00:00"
    processors = "nodes=1:ppn=1"
    command = "python %s" % i
    job_string = """#!/bin/bash
    #PBS -N %s
    #PBS -q Unicog_run4 
    #PBS -l walltime=%s
    #PBS -l %s
    cd "/home/id983365/output"
    %s""" % (job_name, walltime, processors, command)

    # Create a pbs file
    name_file = "qsub_cmd_%s" %e
    fichier = open(name_file, "w")
    fichier.write(job_string)
    fichier.close()

    # Send job_string to qsub
    cmd = "qsub %s"%(name_file)
    subprocess.call(cmd, shell=True)

