# TUTORIAL "Analysing Neurospin's localizer dataset"

This tutorial demonstrates how to analyse a simple fMRI dataset using pypreprocess. 

Data come from an experimental paradigm designed by Philippe Pinel at Neurospin. It consists of a 5 minutes block during which the participant saw various visual stimuli (checkboard, letter strings, ...), listened to spoken stimuli, performed some simple arithmetic computations, and pressed response buttons. 

In this tutorial, we will import scans from two individuals on Neurospin's data acquisition server, then run the preprocessing stages (realignment, spatial normalization, smoothing) and compute some statistical maps for some contrasts at the single subject level.

The preprocessing stages, driven by pypreprocess, are performed using
the standalone SPM12 program (avoiding the need for a matlab license)
while the statistic analyses rely on [http://nipy.org](http://nipy.org).

### Prerequisites

To run the tutorial, you will need:

* pypreprocess ([pypreprocess](https://github.com/neurospin/pypreprocess))
* nistats ([nistats](https://nistats.github.io/)) (last release in April 2020 - module will no longer updated - See nilearn and ([nipy](https://nipy.org/))
* nilearn ([nilearn](http://nilearn.github.io/))
* the 'unicog' toolbox ([https://github.com/neurospin/unicog](https://github.com/neurospin/unicog))  

They may already be installed on your computer. You can check that by starting a Python interpreter:

     ipython

and typing:

     import unicogfmri
     import pypreprocess
     import nilearn
     import nistats

If you see any error message, you will need to install the module(s) with issue. If you are in a hurry, here is how to quickly install unicogfmri and pypreprocess:

     cd /tmp
     git clone https://github.com/neurospin/unicog.git
     cd unicog 
     python setup.py install --user

     cd /tmp
     git clone https://github.com/neurospin/pypreprocess.git
     cd pypreprocess
     python setup.py install --user


## Preparation

Let us create a directory to run this tutorial, by issuing the following commands in a terminal:

       export ROOTDIR=/volatile/test_git_unicog/localizer
       mkdir -p $ROOTDIR
       cd $ROOTDIR

###  Data importation 
See more information on the importation with BIDS [https://github.com/neurospin/neurospin_to_bids](https://github.com/neurospin/neurospin_to_bids).

Here we have an example with 14 subjects from the localizer project.

Launch the importation:

      cd <where_is_the_exp_info_directory_including_the_participants.tsv>
      neurospin_to_bids.py


### Processing 

You have the possibility to use a $ROOTDIR path.
Copy the 'localizer/scripts' directory of unicogfmri
 
       cp -a /tmp/unicog/unicogfmri/localizer/scripts $ROOTDIR

(remark: if you installed the unicog git repository elsewhere than in /tmp, you will need to adjust the preceding line) 

We are ready to go! 
    
Note that all the commands that follow are supposed to be executed from the *scripts* folder.

       cd $ROOTDIR/scripts


#### Preprocessing and first level

We are now going to use the script for the preprocessing. The configuration of all steps (slice timing, normalisation, use SPM8 or SPM12, 
use the MCR (Matlab Compiled Runtime) .... ) are described in the config.ini file.
Check and set up the paths "dataset_dir" and 'output_dir" into the config.ini if needed.

If it is possible, pypreprocess will use the standalone version of SPM (instead of lauching a
matlab instance). So, check the following environment variables from your bashrc file :

        SPM_DIR="/i2bm/local/spm12-standalone/spm12_mcr/spm12"
        SPM_MCR="/i2bm/local/bin/spm12"

To launch the analysis:

        python preproc_and_firstlevel.py


#### For further analysis
Further analysis can be done with python tools. Please take a look at [https://nistats.github.io/auto_examples/index.html#second-level-analysis-examples](https://nistats.github.io/auto_examples/index.html#second-level-analysis-examples).


#### Additional step for visualizing contrasts with the Anatomist software

The maps can be visualized interactively with the [Anatomist Software](http://brainvisa.info/web/anatomist.html).


     source /i2bm/local/Ubuntu-18.04-x86_64/brainvisa/bin/bv_env.sh
     python display_maps.py


Note that it is possible to specify other maps to be displayed by editing the display_maps.py script.



