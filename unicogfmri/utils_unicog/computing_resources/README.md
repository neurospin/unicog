% SOMA-WORKFLOW TUTORIAL

### HOW TO USE SOMA-WORKFLOW ?
More information on [http://brainvisa.info/soma/soma-workflow/](http://brainvisa.info/soma/soma-workflow/)

### WHAT IS SOMA-WORKFLOW ?
Soma-workflow is an interface to launch "jobs" on parallel computing resources.
Here the parallel computing resource is a server (cluster) called Gabriel.
The parallel computing resource could be your computer by using all processors.
Jobs are launched in parallel and not one after the other.

### CREATE A COUNT
See on the [neurospin-wiki](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources)




### HOW TO USE SOMA-WORKFLOW ?

##### CLIENT CONFIGURATION: 
The "client" refers to your work_station. 
Create the **.soma-workflow.cfg** file on the client if needed:

    touch /home/your_logging/.soma-workflow.cfg

Client configuration of **.soma-workflow.cfg**:

    [DSV_cluster_your_logging]
    #remote access information
    CLUSTER_ADDRESS     = gabriel.intra.cea.fr
    SUBMITTING_MACHINES = gabriel.intra.cea.fr
    #optional on client
    QUEUES = run32 Global_long Global_short 
    #optional login for the GUI
    LOGIN = your_logging

<!-- 
Check into your .bashrc file you can launch /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh, for instance:
    alias brainvisa_pkg="source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh"
-->

##### SERVER CONFIGURATION:
The "server" refers to the resources called Gabriel:
[See information on wiki](http://www.neurospin-wiki.org/pmwiki/Main/ComputationalResources)

Connect to gabriel from your workstation:

    ssh  your_logging@gabriel.intra.cea.fr

Create the **.soma-workflow.cfg** file on the server if needed:

    touch /home/your_logging/.soma-workflow.cfg

Server configuration of **.soma-workflow.cfg**:

    [DSV_cluster_your_logging]
    NATIVE_SPECIFICATION = -l walltime=20:00:00
    DATABASE_FILE        = /home/your_logging/soma-workflow/soma_workflow.db
    TRANSFERED_FILES_DIR = /home/your_logging/soma-workflow/transfered-files/
    NAME_SERVER_HOST     = gabriel.intra.cea.fr
    SERVER_NAME          = soma_workflow_database_your_logging
    DRMAA_IMPLEMENTATION = PBS
    SERVER_LOG_FILE   = /home/your_logging/soma-workflow/logs/log_server
    SERVER_LOG_FORMAT = %(asctime)s => line %(lineno)s: %(message)s
    SERVER_LOG_LEVEL  = ERROR
    ENGINE_LOG_DIR    = /home/your_logging/soma-workflow/logs
    ENGINE_LOG_FORMAT = %(asctime)s => %(module)s line %(lineno)s: %(message)s %(threadName)s
    ENGINE_LOG_LEVEL  = ERROR
    PATH_TRANSLATION_FILES = brainvisa{/home/your_logging/.brainvisa/soma-workflow.translation}
    MAX_JOB_IN_QUEUE = {15} run32{15} Global_long{10}


Create the following directories, if needed:

    mkdir /home/your_logging/soma-workflow
    mkdir /home/your_logging/soma-workflow/logs
    mkdir /home/your_logging/soma-workflow/soma-workflow
    mkdir /home/your_logging/soma-workflow/transfered-files


Check the .bashrc with the following lines:

    # .bashrc
    # Source global definitions
    if [ -f /etc/bashrc ]; then
        . /etc/bashrc
    fi

    # User specific aliases and functions
    if [ -f /i2bm/local/etc/bashrc ]; then
       . /i2bm/local/etc/bashrc
    fi

    if [ -f /i2bm/local/etc/profile ]; then
       . /i2bm/local/etc/profile
    fi 

And add the following lines:

    bv_setup_devel
    export PYTHONPATH=/i2bm/brainvisa/CentOS-5.3-x86_64/python-2.7.3/lib/python2.7:$PYTHONPATH
    export PYTHONPATH=/i2bm/brainvisa/CentOS-5.3-x86_64/python-2.7.3/lib/python2.7/site-packages:$PYTHONPATH
    export PATH=/i2bm/brainvisa/CentOS-5.3-x86_64/python-2.7.3/bin:$PATH
    export LD_LIBRARY_PATH=/i2bm/brainvisa/CentOS-5.3-x86_64/python-2.7.3/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/i2bm/brainvisa/CentOS-5.3-x86_64/pbs_drmaa-1.0.13/lib/:$LD_LIBRARY_PATH

    export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:${LD_LIBRARY_PATH}
    build_dir=/neurospin/brainvisa/build/CentOS-5.3-x86_64/trunk
    source $build_dir/bin/bv_env.sh $build_dir
    export DRMAA_LIBRARY_PATH=/i2bm/brainvisa/CentOS-5.3-x86_64/pbs_drmaa-1.0.13/lib/libdrmaa.so

Optional step: If you want to launch brainvisa processes by using soma-workflow 
directly from your workstation. Launch Brainvisa just once:

    #option -X to indicate the graphic mode just for this time    
    ssh  -X your_logging@gabriel.intra.cea.fr
    #you don't need to create a database, it's just to create automatically /home/your_logging/.brainvisa/soma-workflow.translation
    #launch brainvisa
    brainvisa
    #then quit Brainvisa


Launch soma-workflow on Gabriel (if soma_workflow is not started on your gabriel count, 
you can't launch soma-workflow_gui from your workstation):

    python -m soma_workflow.start_database_server DSV_cluster_your_logging
    #to move the programm in background, use ctrl + Z then tape bg

Check if soma_workflow.start_database_server is started:

    ps -aux | grep your_logging

If you have a line like below, the configuration is correct:

    python -m soma_workflow.start_database_server DSV_cluster_your_logging &

##### LAUNCH JOBS FROM YOUR WORKSTATION (=THE CLIENT):
Launch brainvisa environment, if needed:

    source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh

Launch soma-workflow_gui

    soma-workflow_gui
    add [DSV_cluster_your_logging] resource
    submit the python file containing jobs


##### EXAMPLE WITH FREESURFER:
A script of demonstration is available on the unicogfmri module in:</br>

    cd <somewhere>
    git clone /neurospin/unicog/resources/git_server/UnicogFmri.git
    cd <somewhere>/UnicogFmri
    python setup.py install --user 
    cd ./unicogfmri/utils_unicog/computing_resources/test
    more create_jobs_for_somaWF.py
    #create your own script from a copy
    cp create_jobs_for_somaWF.py create_jobs_for_somaWF_local.py
    #change what the paths and configure your freesurfer database 
    #in create_jobs_for_somaWF_local.py
    #init some variables with the following script
    source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh
    #launch the script
    python create_jobs_for_somaWF_local.py


This script generates the blue files. The **soma_WF_JOBS** script must 
be used in **soma-workflow_gui** for launching the jobs on the server.


![](./somaWF_jobs.png "somaWF_jobs.png")









 
