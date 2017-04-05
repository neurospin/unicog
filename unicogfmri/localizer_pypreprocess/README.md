# TUTORIAL "Analysing Neurospin's localizer dataset"

This tutorial demonstrates how to analyse a simple fMRI dataset using pypreprocess. 

Data come from an experimental paradigm designed by Philippe Pinel at Neurospin. It consists of a 5 minutes block during which the participant saw various visual stimuli (checkboard, letter strings, ...), listened to spoken stimuli, performed some simple arithmetic computations, and pressed response buttons. 

In this tutorial, we will import scans from two individuals on Neurospin's data acquisition server, then run the preprocessing stages (realignment, spatial normalization, smoothing) and compute some statistical maps for some contrasts at the single subject level.

The preprocessing stages, driven by pypreprocess, are performed using
the standalone SPM8 program (avoiding the need for a matlab license)
while the statistic analyses rely on [http://nipy.org](Nipy).

### Prerequisites

To run the tutorial, you will need:

* pypreprocess ([pypreprocess](https://github.com/neurospin/pypreprocess))
* the 'unicog' toolbox ([https://github.com/neurospin/unicog](https://github.com/neurospin/unicog))  

They may already be installed on your computer. You can check that by starting a Python interpreter:

     ipython

and typing:

     import unicogfmri
     import pypreprocess

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

       export ROOTDIR=/volatile/test_localizer
       mkdir -p $ROOTDIR
       cd $ROOTDIR

And copy there the 'localizer/scripts' directory of unicogfmri
 
       cp -a /tmp/unicog/unicogfmri/localizer/scripts $ROOTDIR

(remark: if you installed the unicog git repository elsewhere than in /tmp, you will need to adjust the preceding line) 

We are ready to go! 

### Processing 
    
Note that all the commands that follow are supposed to be executed from the *scripts* folder.


       cd $ROOTDIR/scripts

####  Data importation 
Please the importation with BIDS [https://github.com/neurospin/unicog/tree/master/bids](BIDS).


###### Preprocessing and first-level

We are now going to use pypreprocess to run the preprocessing and the first level analysis in a single step. All the information resides in a configuration file, here *config.ini*. Read this file. The parameters are document on pypreprocess website. 


Then, run:

      python preprocess_and_1st_level.py config.ini


If everything works well, reports have been create in html files which you can open, e.g., with firefox. 

* $ROOTDIR/processed_data/report_preproc.html
* $ROOTDIR/processed_data/sub*/res_stats/report_stats.

The statistics maps are located in the subjects subfolders in results:


#### Visualizing contrasts

The maps can be visualized interactively with the [Anatomist Software](http://brainvisa.info/doc/anatomist-4.4/ana_training/en/html/index.html#ana_training%book).


     source /i2bm/local/Ubuntu-14.04-x86_64/brainvisa/bin/bv_env.sh
     python display_maps.py


Note that it is possible to specify other maps to be displayed by editing the display_maps.py script.



