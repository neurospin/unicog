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
os.chdir("/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF")

#######################################################################
# define parameters
subjects_dir = "/neurospin/meg/meg_tmp/MTT_MEG_Baptiste/MEG"
wdir         = "/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF"

ListSubject = ['pf120155','pe110338','cj100142','jm100042',
               'jm100109','sb120316','tk130502','sl130503',
               'rl130571','bd120417','rb130313','mp140019']
                               
ListRunPerSubject = [['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'            ],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase1bis','phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3'],
                     ['phase1','phase2'   ,'phase3']] 

ListCondition     = [['PSS_Vfirst' ,'PSS_Afirst' ],
                     ['JND1_Vfirst','JND1_Afirst'],
                     ['JND2_Vfirst','JND2_Afirst']]

ListTrigger       = [[22, 21],
                     [12, 11],
                     [32, 31]]                     
                  
############################################################################### 
# the epoching script will be called in command line with arguments
# get the full list of command lines to be send in parallel
CMD = []
CMD = [wdir + '/functions/Compute_Epochs_cmd.py'  
       + ' -wdir '    + wdir 
       + ' -subject ' + sub 
       + ' -cond1 '   + str(ListCondition[c][0])
       + ' -cond2 '   + str(ListCondition[c][1])
       + ' -trig1 '   + str(ListTrigger[c][0])
       + ' -trig2 '   + str(ListTrigger[c][1])
       + ' -runlist ' + ' '.join(ListRunPerSubject[s])       
       for s,sub in enumerate(ListSubject)
       for c,cond in enumerate(ListCondition)]     

# the name that will appear in soma_workflow interface
# just display the script name and the argument values
CMDname = []
CMDname = ['Compute_Epochs_cmd '  
       +  sub 
       + str(ListCondition[c][0])
       + str(ListCondition[c][1])
       + str(ListTrigger[c][0])
       + str(ListTrigger[c][1])
       + ' '.join(ListRunPerSubject[s])       
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

        




     
                 