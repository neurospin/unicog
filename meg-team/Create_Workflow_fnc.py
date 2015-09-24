# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:09:44 2015

@author: bgauthie & laetitia grabot
"""
####################################################################
# This script generate jobs.py files and creates a somwf file
# containing the jobs to be send to the cluster with soma_workflow
# you can then launch and follow the processing with soma_workflow interface

####################################################################
# import libraries
from soma_workflow.client import Job, Workflow, Helper
import os
#os.chdir("/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF")
cwd = os.path.dirname(os.path.abspath(__file__)) # where the scripts are
os.chdir(cwd)

from configuration import ( wdir )

#######################################################################
# List of parameters to parallelize
ListSubject  = ['pf120155','pe110338','cj100142','jm100042','jm100109','sb120316',
            'tk130502', 'sl130503', 'rl130571','bd120417','rb130313', 'mp140019']
                 
ListCondition = [['PSS_Vfirst', 'PSS_Afirst'],
                 ['JND1_Vfirst', 'JND1_Afirst'],
                 ['JND2_Vfirst', 'JND2_Afirst']]
                 
####################################################################       
# init jobs file content and names
List_python_files = []

initbody = 'import sys \n'
initbody = initbody + "sys.path.append(" + "'" + cwd + "')\n"
initbody = initbody + 'import Compute_Epochs_fnc as CE\n'

# write job files
# (basically a python script calling the function of interest with arguments of interest)
python_file, Listfile, ListJobName = [], [], []

for s,subject in enumerate(ListSubject):
    for c,condition in enumerate(ListCondition):
        
        body = initbody + "CE.Compute_Epochs_fnc('" + wdir + "',"   
        body = body + str(condition) +","
        body = body + "'" + subject + "')"
        
        # use a transparent and complete job name referring to arguments of interest    
        jobname = subject
        for cond in condition:
            jobname = jobname + '_' + cond 
        ListJobName.append(jobname)     
            
        # write jobs in a dedicated folder
        name_file = []
        name_file = os.path.join(wdir, ('somawf/jobs/Demo_' + jobname + '.py'))
        Listfile.append(name_file)
        with open(name_file, 'w') as python_file:
            python_file.write(body)
 
    
jobs = []
for i in range(len(Listfile)):
    JobVar = Job(command=['python', Listfile[i]], name = ListJobName[i],
                 native_specification = '-l walltime=4:00:00, -l nodes=1:ppn=2')
    jobs.append(JobVar)
    WfVar = Workflow(jobs=jobs, dependencies=[])

    # save the workflow into a file
    somaWF_name = os.path.join(wdir, 'somawf/workflows/DEMO_WF')
    Helper.serialize(somaWF_name, WfVar)

        




     
                 