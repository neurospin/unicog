# MEG analysis parallelization with SOMA_WORKFLOW

We provide some example scripts to illustrate how you can use soma_worklow to process differents subjects and conditions in parallel
We gathered canonical processing steps: epoching, averaging, inverse_operator and stc computation in a python function
We then call a script that builds the workflow object

We provide two alternative ways to distribute your analysis in a serie of jobs that can be send in parallel

### Compute_Epochs_fnc 
is the analysis function
it take 1 subject, 1 pair of conditions and a list of acquisition runs as arguments
compute and write sensor-space averages, stc and a plot the  covariance matrix
### Create_Workflow_fnc
create the workflow, an object you can load in soma_workflow interface
From the list af subject and conditions pairs, it will generate a serie of python scripts calling Compute_Epochs_fnc with specific subject and conditions pair and put it in a workflow

### Compute_Epochs_cmd
is the strict equivalent of Compute_Epochs_cmd but can take its arguments directly in a command line call thanks the argument parser (module argparse)
### Create_Workflow_cmd
create the workflow containing this time command lines

### recode_events
is used to epochs with respect to specific combinations of triggers

