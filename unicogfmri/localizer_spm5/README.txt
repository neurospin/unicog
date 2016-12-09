Laboratoire de NeuroImagerie Cognitive (LCOGN):
===============================================
INSERM U562 / NeuroSpin CEA/DSV/I2BM

Batch system for SPM5 (http://www.fil.ion.ucl.ac.uk/spm/)

INSTALLATION:
-------------
Copy all batch files in a 'mfiles' directory in your study hierarchy:

     study
        |___ subject1
        |        |___ t1mri
        |        |      |___ acquisition1
        |        |      |       |____ analysis
        |        |      |                |____ spm_segmentation
        |        |      |
        |        |      |___ acquisition2
        |        |      |___     ...
        |        |
        |        |___ fMRI
        |               |___ acquisition1
        |               |         |___ session1
        |               |         |___ session2
        |               |         |___    ...
        |               |         |____ analysis
        |               |                  |_____ stats_session1
        |               |                  |_____ stats_session2
        |               |                  |_____     ...
        |               |___ acquisition2
        |               |___     ...
        |
        |___ subject2
        |        |___  ...
        |
        |___ mfiles
        |       |___ main.m
        |       |___ startup.m
        |       |___ README.txt
        |       |___ lcogn_preproc
        |       |___ lcogn_firstlevel
        |       |___ lcogn_secondlevel
        |       |___ tools
        |___ rfxmodel
                |___ condition1
                |___ condition2
                |___    ...

From there, run 'main' Matlab command.
   >> main

Note: The command 'startup' setups pathes for the system of batch and checks 
SPM installation.

This batch system allows to perform 3 kinds of jobs: preprocessings, first 
level analyses, and second level analyses.

FIRST LEVEL:
------------
You also need to adapt the two functions 'specif_model.m' and 'specif_contrasts.m'
to specify your model and contrasts.

SECOND LEVEL:
-------------
For the moment it is not included in the main.m file but you can adapt the file 
furnished in /lcogn_secondlevel/ (lcogn_rfx.m).
