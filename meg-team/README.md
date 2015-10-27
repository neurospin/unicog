## MEG analysis parallelization with SOMA_WORKFLOW

We provide some example scripts to illustrate how you can use soma_worklow to process different subjects and conditions in parallel.
We gathered canonical processing steps: epoching, averaging, inverse_operator, stc computation and grand average plotting in a python function (*Compute_Epochs_fnc.py* and *Plot_groupERF_fnc.py*).
We then call a script that builds the workflow file (*Create_Workflow_fnc.py*).
All the parameters used in the processing steps are gathered in a *configuration.py* file, systematically called in the scripts.
Additional functions can be used, as for instance *recode_event.py*, used to recode events from epochs object following relevant combinations of triggers.

### Building a workflow as a series of jobs 
First, each job is written in a python file. For instance, the job *Demo_bd1204117_JND1_Vfirst_JND1_Afirst.py* contains the code below (*bd1204117* is the subject, *JND1_Vfirst* and *JND1_Afirst* are two conditions):

    import sys 
    import Compute_Epochs_fnc as CE
    CE.Compute_Epochs_fnc('/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF',['JND1_Vfirst', 'JND1_Afirst'],'bd120417')

This is done for all subjects and conditions. Then, when all epochs and evokeds are written for a couple of conditions, a job will plot and save the grand averages. For instance, the code below corresponds to the conditions *JND1_Vfirst* and *JND1_Afirst*:

    import Plot_groupERF_fnc as ERF
    ERF.Plot_groupERF_fnc(['JND1_Vfirst', 'JND1_Afirst'],['pf120155', 'pe110338', 'cj100142', 'jm100042', 'jm100109',       'sb120316', 'tk130502', 'sl130503', 'rl130571', 'bd120417', 'rb130313', 'mp140019'])

##### Compute_Epochs_fnc 
This analysis function computes and writes sensor-space averages, stc and plots the  covariance matrix.  <br />
Arguments: <br />
  * wdir: working directory (for the example, */neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/* )
  * Condition: list of conditions (list of strings)
  * Subject: subject name (string)

##### Plot_groupERF_fnc 
This analysis function plots the grand average evoked response for a couple of conditions.  <br />
Arguments: <br />
  * wdir: working directory (for the example, */neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/* )
  * ListCond: couple of conditions (tuple of strings)
  * ListSubj: list of subject names (list of strings)

##### Create_Workflow_fnc
First, the function writes all the jobs in a dedicated folder. Then, it creates the workflow file organizing the jobs calls. The jobs plotting the grand average will be launched **after** the jobs creating epochs and evokeds for one couple of conditions (this is implemented with the "dependencies" parameter). Once written, the workflow can be loaded in soma_workflow interface and submitted.

### Alternative: jobs calls via command lines
Here, jobs are not written into *.py* files but are directly launched via command lines.

##### Compute_Epochs_cmd
It is the strict equivalent of *Compute_Epochs_fnc.py* except that it takes its arguments directly in a command line call (thanks to the argument parser, module *argparse*).<br />
Arguments: <br />
  * -wdir: working directory (for the example, */neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/* )
  * -cond1: condition 1 (string)
  * -cond2: condition 2 (string)
  * -subject: subject name (string)

##### Create_Workflow_cmd
It creates the workflow, a text file containing the command line corresponding to each job.

### How to run the example
In your terminal, create a folder on the neurospin server (important! it will not work from your volatile) to receive the git repository.

    mkdir myrepository

Clone the git repository unicog in your repository and move to the scripts folder.

    git clone https://github.com/neurospin/unicog.git
    cd unicog/meg-team

Lauch the script *Create_Workflow_fnc.py* to create the workflow. You can do it from an ipython interpreter.

    ipython
    %run Create_WorkFlow_fnc.py
    
Quit ipython and lauch the soma_workflow interface.

    exit
    soma_workflow_gui

Click on *open* and load your workflow (located in *neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/somawf/*). Submit the jobs, it's done!


