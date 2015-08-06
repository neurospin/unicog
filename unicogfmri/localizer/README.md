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

The first step is to import data. 

The location of the scans is described in a text file. Here is an example of such a file:


     subj01  20110404 fp110067 02 anat 05 norm1 07 jabb1 09 norm2 
     subj02  20110404 kl198789 02 anat 05 norm1 07 jabb1 09 norm2 
  
The input consists of one line per participant: 

* The first item of each line specifies the name of the subdirectory that will be created to store this participant's data.
* The second item is the date of acquisition in the format YYYYMMDD,
* The third item is the participant's NIP identifier (Note: if, for any reason, a given participant appears to have been scanned several times the same day, the nip number is not sufficient to uniquely identify the scans and you must ask the manips for the nip and exam numbers. You then have to write: nip-exam number, for example: kl198789-4004)
* the remaining of the line is a series of pairs 'series_number' and 'target_name'. Each series is identified by a *two-digits number* (i.e. *01* rather than *1*), the "target name" will be added as a prefix to the file name for this series.

For this tutorial, we have already created the file.

      cd $ROOTDIR/scripts
      cat scan_list.txt
      subject01 20100628 tr070015 02 anat 09 func_1 
      subject02 20100701 ap100009 02 anat 09 func_1

To start the importation, you just have to type:

      python import_scans.py scan_list.txt

The scans should now reside in a directory 'raw_data'. You can check that with:

      ls $ROOTDIR/raw_data

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



