# unicog

"unicog" is a set of tools (scripts, python modules, examples, ...)  to perform various tasks.  

The files are gathered in a git repository named "unicog" located on http://github.com

### installation

To install the tools, you first need to make a local copy on your computer, using the following command line:

    git clone https://github.com/neurospin/unicog.git

This creates a folder 'unicog' which contains all the files:

    cd unicog

Then, to install the Python modules

    python setup.py install --user
    

To check that everything is ok, try to load the unicogfmri 

    python
    import unicogfmri

    
### updating

From time to time, to update you local copy of "unicog", got to the unicog folder and type:

    git pull
    python setup.py install --user


