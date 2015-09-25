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
                  
############################################################################### 
# the epoching script will be called in command line with arguments
# get the full list of command lines to be send in parallel
                  
initbody = 'import sys \n'
initbody = initbody + "sys.path.append(" + "'" + cwd + "')\n"
initbody = initbody + 'import Compute_Epochs_fnc as CE\n'                  
                  
                  
CMD = []
CMD = [cwd + '/Compute_Epochs_cmd.py'  
       + ' -wdir '    + wdir 
       + ' -subject ' + sub 
       + ' -cond1 '   + str(ListCondition[c][0])
       + ' -cond2 '   + str(ListCondition[c][1])    
       for s,sub in enumerate(ListSubject)
       for c,cond in enumerate(ListCondition)]     

# the name that will appear in soma_workflow interface
# just display the script name and the argument values
CMDname = []
CMDname = ['Compute_Epochs_cmd '  
       +  sub 
       + str(ListCondition[c][0])
       + str(ListCondition[c][1])    
       for s,sub in enumerate(ListSubject)
       for c,cond in enumerate(ListCondition)]

###############################################################################  
# create the workflow  
jobs = []
for c,cmd in enumerate(CMD):
    JobVar = Job(command = ['python ' + cmd], name = CMDname[c],
                 native_specification = '-l walltime=4:00:00, -l nodes=1:ppn=2')
    jobs.append(JobVar)
    WfVar = Workflow(jobs=jobs, dependencies=[])

    # save the workflow into a file
    somaWF_name = os.path.join(wdir, 'somawf/workflows/DEMO_WF')
    Helper.serialize(somaWF_name, WfVar)

        




     
                 