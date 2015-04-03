% UNICOGFMRI TUTORIAL


### INSTALL THE UNICOGFMRI

##### CLONE THE UNICOGFMRI GIT 

UnicogFmri is a git repository located at neurospin.
In order to launch python scripts and copy them to create your
own scritps, first you have to clone the repository.

    #create a directory <my_repository>
    mkdir <my_repository>
    cd <my_repository>
    git clone /neurospin/unicog/resources/git_server/UnicogFmri.git


##### INSTALL THE UNICOGFMRI GIT
The UnicogFmri is also a python module (stored in a git repository) and in order to use it from python you have to 
install it.

    cd <my_repository>/UnicogFmri
    python setup.py install --user


##### VISUALIZE FUSION OF ACTIVATION MAPS AND TEMPLATE WITH PYANATOMIST MODULE
The pyanatomist module is a python API for launching the Anatomist Software.
Very interesting if you grab files through many subjects and many
contrasts of interest, you can launch many fusions at the same time.

Note that before launching the script, it is necessary to initialize 
correctly paths for Anatomist with the first line.

    source /i2bm/local/Ubuntu-12.04-x86_64/brainvisa/bin/bv_env.sh
    cd <my_repository>/UnicogFmri/unicogfmri/utils_unicog/viewer/tests
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
will need to add a loop with a subject name selection.


##### UPDATE THE GIT REPOSITORY
From time to time, update the repository.
So, use git pull and perform a new installation.

    cd <my_repository>/UnicogFmri
    git pull
    python setup.py install --user

Note : a new install is mandatory if you do a "git pull" or if you add
new functions. But if you just use existing module or function, it won't
needed to do it.