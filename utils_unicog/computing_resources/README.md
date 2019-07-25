Computing resources are available at [Neurospin](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources) for submitting jobs.
Here are some technical propositions to launch jobs on the cluster: 

* the `qsub` command: launch jobs on the cluster by using `qsub`.
* a python module: [soma-workflow](http://brainvisa.info/web/soma/soma-workflow/), manage your jobs from the client side (with or without GUI).
* use singularity (container).

The choice between `qsub` and soma-workflow depends on users (advanced or not) and needs. See the following parts to make a choice. 

More information on the queues which are available for users at NeuroSpin (unicog or not) at [http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources).

# QSUB COMMAND

## LAUNCH ONE JOB:
Very basic using of `qsub`, without any options. By default, if any queue is mentionned, the **global_long** or **global_short** queue will be used (depends on the walltime parameter).

        $ qsub <pathtoScript>

Many options are available such as `-q` to indicate the queue. Many specific queues are available at NeuroSpin, take a look at [http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources). For instance, use the **Unicog_short** queue:

        $ qsub -q Unicog_short <pathtoScript>

Many other options are available. See the qsub documention to know all options:

        $ qsub -q <queue> -w e -N <job_name> -l h_vmem=<memory, e.g. 4G> -l walltime=<hh:mm:ss> -o <outputlogfile> -e <errorlogfile> <pathtoScript> <arg1> <arg2>

## LAUNCH MANY JOBS:
If you want to launch many jobs, you can use a shell or python script. Some examples are available at:

* [https://github.com/neurospin/unicog/tree/master/utils_unicog/computing_resources/example/qsub_python.py](https://github.com/neurospin/unicog/tree/master/utils_unicog/computing_resources/example/qsub_python.py)
* [https://github.com/neurospin/unicog/tree/master/utils_unicog/computing_resources/example/example_for_many_jobs.sh](https://github.com/neurospin/unicog/tree/master/utils_unicog/computing_resources/example/example_for_many_jobs.sh)


# SOMA-WORKFLOW TUTORIAL

## WHAT IS SOMA-WORKFLOW ?
Soma-workflow is an interface (graphical or not) for submission, control and monitoring of jobs on parallel computing resources.
One parallel computing resource could be your own computer by using all processors or a specific cluster like alambic at NeuroSpin.
Jobs are launched in parallel and not one after the other. Here, we are going to describe the cases for which you want to use alambic server, available
at NeuroSpin or on your own computer.

More information on [http://brainvisa.info/web/soma/soma-workflow/](http://brainvisa.info/web/soma/soma-workflow/)
and [https://github.com/populse/soma-workflow](https://github.com/populse/soma-workflow) 

## HOW CAN I LAUNCH MY JOBS WITH SOMA WORKFLOW ?
You can use soma-workflow in two ways:

* Only on your own workstation: if your machine is multi-core, Soma-workflow optimizes the use of resources on your PC.
* On a cluster: if you have an access to a cluster for instance at Neurospin we can use the alambic Server.

Please, note that:

| On your own workstation         | On a cluster     |
| --------------------------------|-----------------|
|Uncompiled MATLAB codes: Yes     | Uncompiled MATLAB codes: No (1)   |
|Compiled MATLAB codes: Yes       | Compiled MATLAB codes: Yes   |

1 : a MATLAB compiler is available at NeuroSpin.  


## INSTALLATION / CONFIGURATION / EXAMPLES
### INSTALLATION:

If you don't have an account on alambic, please take a look at:
[See information on wiki](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources)
Installation compatible with python 3.

#### MODULE INSTALLATION

##### BASIC INSTALLATION
On the client (your workstation) and the server (cluster), you have to install the same version of the modules.
Two modules are required, 'soma-workflow' and 'paramiko'.

	$  pip install soma-workflow --user
	$  pip install paramiko --user
	
The --user option allows to install the module into /home/~/.local. In this case you don't need root permissions, but the
module is available only for you. The module will be automatically found. 

##### ADVANCED INSTALLATION
If you need tha last version of soma-workflow, use the [github repository](https://github.com/populse/soma-workflow)

    $ cd <somewhere>
    $ git clone https://github.com/populse/soma-workflowt
    $ cd soma-workflow
    $ python setup.py install --user


#### LAUNCH soma_workflow_gui GRAPHICAL INTERFACE

Add the following line into your ~/.bashrc:

	export PATH=~/.local/bin:$PATH
	
Launch the soma_workflow_gui interface into a terminal:

	$ soma_workflow_gui 
	
If you want to check where is located the soma_workflow_gui :

	$ which soma_workflow_gui 


### CONFIGURATION:
#### CLIENT CONFIGURATION: 
On your PC, edit the following file:

    /home/your_logging/.soma-workflow.cfg

Add the following lines for the configuration and change the **your_logging** part:

    [DSV_cluster_your_logging]
    #remote access information
    CLUSTER_ADDRESS     = alambic.intra.cea.fr
    SUBMITTING_MACHINES = alambic.intra.cea.fr
    #optional on client
    QUEUES = run32 Global_long Global_short Unicog_short Unicog_long Unicog_run2 Unicog_run4 Unicog_run8 Unicog_run16 Unicog_run32 
    #optional login for the GUI
    LOGIN = your_logging


#### SERVER CONFIGURATION:
The "server" refers to the resource called alambic:
[See information on wiki](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources)

STEP1:
Connect to alambic from your workstation with the login/pw given for alambic:

    ssh your_logging_for_alambic@alambic.intra.cea.fr

STEP2:
On the server, edit the following file:

    /home/your_logging/.soma-workflow.cfg

Add the following lines for the configuration ([with vi](http://www.neurospin-wiki.org/pmwiki/Main/LINUX), to edit file into a console). Change the **your_logging** part:

    [DSV_cluster_your_logging]
    NATIVE_SPECIFICATION = -l walltime=01:00:00
    DATABASE_FILE        = /home/your_logging/soma-workflow/soma_workflow.db
    TRANSFERED_FILES_DIR = /home/your_logging/soma-workflow/transfered-files/
    NAME_SERVER_HOST     = alambic.intra.cea.fr
    SERVER_NAME          = soma_workflow_database_your_logging
    SERVER_LOG_FILE   = /home/your_logging/soma-workflow/logs/log_server
    SERVER_LOG_FORMAT = %(asctime)s => line %(lineno)s: %(message)s
    SERVER_LOG_LEVEL  = ERROR
    ENGINE_LOG_DIR    = /home/your_logging/soma-workflow/logs
    ENGINE_LOG_FORMAT = %(asctime)s => %(module)s line %(lineno)s: %(message)s %(threadName)s
    ENGINE_LOG_LEVEL  = ERROR
    PATH_TRANSLATION_FILES =
    MAX_JOB_IN_QUEUE = {10} run32{5} Global_long{5} Global_short{5}
    SCHEDULER_TYPES = pbspro

STEP3:
Create the following directories, if needed:

    mkdir /home/your_logging/soma-workflow
    mkdir /home/your_logging/soma-workflow/logs
    mkdir /home/your_logging/soma-workflow/soma-workflow
    mkdir /home/your_logging/soma-workflow/transfered-files


### EXAMPLES:
#### SIMPLE EXAMPLE WITH THE GRAPHICAL INTERFACE:

STEP1:
Create a job_to_launch.py python file into /tmp/python_file/:

	# -*- coding: utf-8 -*-
	import os
	import subprocess

	cmd = "touch  /tmp/file_test.txt" 
	subprocess.call(cmd, shell=True)
	
	
STEP2:
Create a /tmp/create_somaWF_jobs.py python file to generate your soma_workflow_job into:

	# -*- coding: utf-8 -*-
	import os, sys, glob
	from soma_workflow.client import Job, Workflow, Helper

	if len(sys.argv)==1:
		list_scripts = glob.glob("/tmp/python_file/job_to_launch.py")
	else:
		list_scripts= sys.argv[1:]

	jobs = []
	for f in list_scripts:
		jobs.append(Job(command=["python", os.path.abspath(f)], name=f))

	workflow=Workflow(jobs)
	Helper.serialize('test_script_python.somawf', workflow)


Then, launch the script:

    python /tmp/create_somaWF_jobs.py
	
This step creates a /tmp/test_script_python.somawf file.

STEP3:
Launch the soma_workflow_gui

	$ soma_workflow_gui

By default, your workstation is already into the liste of computing resources.
Probably, you have to add the '[DSV_cluster_your_logging]' which as indicated into the .soma-workflow.cfg configuration file.
Then open and sublit the /tmp/test_script_python.somawf
	
STEP4:
Check if a /tmp/file_test.txt was created.

#### SIMPLE EXAMPLE WITHOUT THE GRAPHICAL INTERFACE:

STEP1:
Create a job_to_launch.py python file into /tmp/python_file/:

	# -*- coding: utf-8 -*-
	import os
	import subprocess

	cmd = "touch  /tmp/file_test.txt" 
	subprocess.call(cmd, shell=True)
	
	
STEP2:
Create a /tmp/create_somaWF_jobs.py python file to generate your soma_workflow_job into. Change the **your_logging** and **your_password** part:

	# -*- coding: utf-8 -*-
	import os, sys, glob
	from soma_workflow.client import Job, Workflow, Helper
	from soma_workflow.client import WorkflowController

	if len(sys.argv)==1:
		list_scripts = glob.glob("/tmp/python_file/job_to_launch.py")
	else:
		list_scripts= sys.argv[1:]

	jobs = []
	for f in list_scripts:
		jobs.append(Job(command=["python", os.path.abspath(f)], name=f))

	workflow=Workflow(jobs)
	controller = WorkflowController("DSV_cluster_your_logging", "your_logging", "your_password")
	controller.submit_workflow(workflow=workflow,
                           name="simple example")

Launch the script:

    python /tmp/create_somaWF_jobs.py

STEP3:
Check if a /tmp/file_test.txt was created.


#### EXAMPLE WITH FREESURFER:
An example is available on the unicog module:</br>

    cd
    
    #if you have not already cloned unicog.git and installed it:
    git clone https://github.com/neurospin/unicog.git
    cd unicog
    python setup.py install --user
    
    cd ./unicog/utils_unicog/computing_resources/example
    
    #create your own script from a copy
    #change what the paths and configure your freesurfer database 
    cp example_somaWF_for_freesurfer.py example_somaWF_for_freesurfer_local.py
    
    #launch the script
    python example_somaWF_for_freesurfer.py


This script generates the blue files. The **soma_WF_JOBS** script must 
be used in **soma-workflow_gui** for launching the jobs on the server or
on your own workstation (if many cores).


![](./somaWF_jobs.png "somaWF_jobs.png")


### EXAMPLE FOR SPM BATCHES:
An example is available on the unicog module:</br>

    cd
    
    #if you have not already cloned unicog.git and installed it:
    git clone https://github.com/neurospin/unicog.git
    cd unicog
    python setup.py install --user 
    
    cd ./unicog/unicogfmri/utils_unicog/computing_resources/example
    
    #create your own script from a copy
    #and init some variables with the following script if needed
    cp example_somaWF_for_spm_batches.py example_somaWF_for_spm_batches_local.py
    
    #launch the script
    python example_somaWF_for_spm_batches.py

This must generate a file called **spm12_batches.somawf** which must be
used in **soma-workflow_gui** for launching the jobs on the server or
on your own workstation (if many cores).

# SINGUALARITY
For some specific cases (specific software version ...), containers such as [singularity](https://sylabs.io/docs/) can be used on the cluster.
Some examples are coming soon ....