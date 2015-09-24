## MEG analysis parallelization with SOMA_WORKFLOW

We provide some example scripts to illustrate how you can use soma_worklow to process differents subjects and conditions in parallel.
We gathered canonical processing steps: epoching, averaging, inverse_operator and stc computation in a python function (*Compute_Epochs_~.py*).
We then call a script that builds the workflow object (*Create_Workflow_~.py*).
All the parameters used in the processing steps are gathered in a configuration.py file, systematically called in the scripts.
Additional functions can be used, as for instance *recode_event.py*, used to recode events from epochs object following relevant combinations of triggers.

We provide two alternative ways to distribute your analysis in a serie of jobs that can be send in parallel.

### Parallelization via function call
Each job is written in a python file and calls the function *Compute_Epochs_fnc*.

##### Compute_Epochs_fnc 
This analysis function compute and write sensor-space averages, stc and plot the  covariance matrix. <br />
Arguments: <br />
  * wdir: working directory (for the example, */neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/* )
  * Condition: list of conditions 
  * Subject: subject name (string)

##### Create_Workflow_fnc
It both creates a serie of python scripts calling the function *Compute_Epochs_fnc*, and the workflow, a text file calling all the created serie. Each python script corresponds to a subject/conditions combination (called job). The workflow will be loaded in soma_workflow interface.

### Parallelization via command lines
Each job is directly lauch via a command line.

##### Compute_Epochs_cmd
It is the strict equivalent of *Compute_Epochs_fnc.py* except that it takes its arguments directly in a command line call thanks to the argument parser (module argparse).<br />
Arguments: <br />
  * wdir: working directory (for the example, */neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/* )
  * cond1: condition 1 (string)
  * cond2: condition 2 (string)
  * subject: subject name (string)

##### Create_Workflow_cmd
It only creates the workflow, a text file containing the command line corresponding to each job.

### How to run the example
In your terminal, create a file in neurospin servor (important! it will not work from your volatile) to receive the git repository.

    mkdir myrepository

Clone the git repository unicog in your repository and move to the scripts folder.

    git clone https://github.com/neurospin/unicog.git
    cd unicog/meg-team

Lauch the script *Create_Workflow_~.py* to create the workflow. You can do it from an ipython interpreter.

    ipython
    %run Create_WorkFlow_cmd.py
    
Quit ipython and lauch the soma_workflow interface.

    exit
    soma_workflow_gui

Click on *open* and load your workflow (located in *neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/somawf/*). Submit the jobs, it's done!


