# TUTORIAL LOCALIZER

Here is a tutorial to start in fMRI with the very well known localizer data. The goal is to show you how to import, to process and to visualize data by 
using python scripts and the standalone SPM version (compiled version, without licence).
In fact, the standalone SPM is used for the preprocessing part, but the statistic levels 
are based on nipy.
We hope these scripts cover a lot of cases. Other pipelines are available at 
NeuroSpin, in particular in Capsul [http://nsap.intra.cea.fr/capsul-doc/index.html](http://nsap.intra.cea.fr/capsul-doc/index.html)
or [https://github.com/neurospin/capsul](https://github.com/neurospin/capsul)



### CONFIGURATION

##### Which python modules do you need ?

######unicog
unicog is a git repository located at neurospin.
You can use these scripts like templates with your own data.
So, first, don't forget to clone or to update the repository if needed.

See  [https://github.com/neurospin/unicog](https://github.com/neurospin/unicog) 


######pypreprocess
[pypreprocess](https://github.com/neurospin/pypreprocess) is an external module.
To ensure the pypreprocess module is available:

    ipython
    import pypreprocess
    #if you want to locate where is pypreprocess:
    pypreprocess.__file__ 

If pypreprocess module is not installed, please refer to [https://github.com/neurospin/pypreprocess](https://github.com/neurospin/pypreprocess).
Some additional python modules are available (numpy, nibabel ...). All information is available 
on [https://github.com/neurospin/pypreprocess](https://github.com/neurospin/pypreprocess) page.

###STEPS FOR PROCESSING

*Before running scripts, please check paths.*

#### STEP1: DATA IMPORTATION

To import data, 2 formats of description are possible: xls or txt (the same format than previously).
In order either to use xls or txt format, just use init_xls or init_txt in the following script [https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer/importation_data/1_import_data_txt.py](https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer/importation_data/1_import_data_txt.py)
In this example, we are going to use the txt format.
You can indicate in the same script where data will be imported in the **main_dir** variable.



**Importation of subjects**

    cd <my_repository>/unicog/unicogfmri/localizer
    python ./volume_glm/1_import_data_txt.py


Note : if  a message such as "ImportError: No module named pandas", it means the
pandas module is missing for python. This module is needed to read excel files.
To install this module:

    sudo pip install pandas
    
Another possibility is :
    
    #download the package on https://pypi.python.org/pypi/pandas
    tar zxvf <package>
    cd <package>
    python setup.py install --user 


#### STEP2: DATA PROCESSING
For this part, we are going to use the pypreprocess module. The data
processing includes the preprocessing and the first-level. 
 
###### Configuration of config.ini
Before launching the processing, please take a look at the configuration file, 
in order to check paths and options: 
    
[https://github.com/neurospin/unicog/blob/master/unicogfmri/localizer/volume_glm/Step1_config.ini](https://github.com/neurospin/unicog/blob/master/unicogfmri/localizer/volume_glm/Step1_config.ini)


###### Run the preprocessing and first-level
In this section, we launch the following python script and we indicate, at the
beginning of the line, the path to the standalone SPM to be used.

    cd <my_repository>/unicog/unicogfmri/localizer
    SPM_MCR=/i2bm/local/bin/spm8 python ./volume_glm/Step2_preprocess_1st_level.py

Take a look at the report for preprocessing:

&lt;output_dir&gt;/results/report_preproc.html

And the maps are located:

 * &lt;output_dir&gt;/results/&lt;name_subject&gt;/res_stats/t_maps
 * &lt;output_dir&gt;/results/&lt;name_subject&gt;/res_stats/z_maps
 * &lt;output_dir&gt;/results/&lt;name_subject&gt;/res_stats/variance_maps
 * &lt;output_dir&gt;/results/&lt;name_subject&gt;/res_stats/effects_maps

Note: pypreprocess uses a cached system, i.e. if you run again your script
the steps which have already been processed, will be skipped. Even if this system
is very interesting, it can take a lot of space.

Note: the &lt;output_dir&gt; is indicated in [https://github.com/neurospin/unicog/blob/master/unicogfmri/localizer/volume_glm/Step1_config.ini](https://github.com/neurospin/unicog/blob/master/unicogfmri/localizer/volume_glm/Step1_config.ini).

##### READ THE REPORT
Thanks to pypreprocess, we have an automatic report on processing.
We have a lot of information such as design matrix, onsets, names of conditions, 
snapshots... and so on.
 
Please refer to &lt;output_dir&gt;/&lt;name_subj&gt;/res_stats/report_stats.html


#### STEP 3: VIEW CONTRASTS
Now it is time to visualize the maps. Here we use [Anatomist Software](http://brainvisa.info/doc/anatomist-4.4/ana_training/en/html/index.html#ana_training%book),
but other solutions are possible. In our example, we select for each subject, a list of contrasts of interest (z or t maps). See the python script: 
**../volume_glm/Step3_view_maps.py**. Note that before launching the script, 
it is necessary to initialize correctly the path for Anatomist with the first line.

    source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh
    cd <my_repository>/UnicogFmri/unicogfmri/localizer
    python ./volume_glm/Step3_view_maps.py


<!-- 
#### ADDITIONAL STEPS:
######How to set up $PYTHONPATH variable in order to find modules?
Normally, the installation of python module is set up by using a setup.py or
a pip install. But sometimes, you have to add python modules directly in the $PYTHONPATH variable.
To update the $PYTHONPATH variable, change your ~/.bashrc:
    
    #add path for a python MODULE 
    export PYTHONPATH=$PYTHONPATH:<path_where_is_the_MODULE>
-->


