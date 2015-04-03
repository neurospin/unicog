# TUTORIAL

##### VISUALIZE FUSION OF ACTIVATION MAPS AND TEMPLATE WITH PYANATOMIST MODULE
The pyanatomist module is a python API for launching the Anatomist Software.
Very interesting if you grab files through many subjects and many
contrasts of interest, you can launch many fusions at the same time.

Note that before launching the script, it is necessary to initialize 
correctly paths for Anatomist with the first line.

    source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh
    cd <my_repository>/unicog/unicogfmri/utils_unicog/viewer/tests
    python view_contrasts.py

Note: For more information on 
[pyanatomist module](http://brainvisa.info/doc/cartointernet/cartointernet_pg/en/html/ch05.html)

Note: If you work on your laptop, you probably have to install Brainvisa package
including pyanatomist and Anatomist.


##### NOW CREATE YOUR OWN SCRIPT
If you want to use scripts, you just have to copy a template script as view_contrast.py
and rename it. If you modify the view_contrast.py, it will be more difficult to update
your git repository.

The step of "glob" files is very depending on the organization of your files. It probably
will need to add a loop with a step of subject name selection.
