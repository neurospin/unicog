# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 11:37:04 2014

@author: id983365

script to generate :
    - .sh to launch one freesurfer command
    - .py which create the somaWF
"""

from soma_workflow.client import Job, Workflow, Helper
import os.path

######  Parameters to change ###############################################
subjects = ['subject01', 'subject02', 'subject03', 'subject04',
            'subject05', 'subject06', 'subject07', 'subject08',
            'subject09', 'subject10', 'subject11', 'subject12',
            'subject13', 'subject14']

subjects_dir = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"
#path_script = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/script/somaWF/conversion"
path_script = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/script/somaWF/recon-all"
#and see the anat, output and the cmd_freesurfer in 
#create_shell_file(id_subject)
############################################################################

shell_file = ".sh"
python_file = ".py"


def create_shell_file(id_subject):
#CONVERsION
#    anat = "{subjects_dir}/{id_subject}/mri/orig/001.nii".format(
#                    subjects_dir=subjects_dir, id_subject=id_subject)
#    output = "{subjects_dir}/{id_subject}/mri/orig/001.mgz".format(
#                    subjects_dir=subjects_dir, id_subject=id_subject)
#    cmd_freesurfer = "mri_convert -i {anat} -o {output}".format(
#                    anat=anat, output=output)

#RECON-ALL
    cmd_freesurfer = "recon-all -all -s {subject}".format(subject=id_subject)

    body = """#!/bin/sh
# FreeSurfer home directory
[ -z "$FREESURFER_HOME" ] && FREESURFER_HOME=/i2bm/local/freesurfer
 export FREESURFER_HOME
# Configure FreeSurfer
. ${FREESURFER_HOME}/FreeSurferEnv.sh

# FreeSurfer 5.1.0 or less require "en" locale
LANG='en_US.UTF-8'

# Set a variable to mark the FreeSurfer shells
I2BM_FREESURFER=$FREESURFER_HOME
export I2BM_FREESURFER
"""
    body = body + "\nexport SUBJECTS_DIR=" + subjects_dir
    body = body + "\n" + cmd_freesurfer

    name_file = os.path.join(path_script, (id_subject + '.sh'))
    shell_file = open(name_file, "w")
    shell_file.write(body)
    shell_file.close
    return name_file


def create_python_file(id_subject, shell_file):
    body = """import os\nimport subprocess
            """
    body = body + "\nscript_fs = '" + shell_file + "'"
    body = body + "\ncmd = \"source \" + script_fs"
    body = body + "\nsubprocess.call(cmd, shell=True)"

    name_file = os.path.join(path_script, (id_subject + '.py'))
    python_file = open(name_file, "w")
    python_file.write(body)
    python_file.close
    return name_file


# create the workflow:
def create_somaWF(liste_python_files):
    jobs = []
    for file_python in liste_python_files:
        file_name = os.path.basename(file_python)
        job_1 = Job(command=["python", file_python], name=file_name)
        jobs.append(job_1)

    #jobs = [job_1]
    dependencies = []
    workflow = Workflow(jobs=jobs, dependencies=dependencies)

    # save the workflow into a file
    somaWF_name = os.path.join(path_script, "soma_WF_JOBS")
    Helper.serialize(somaWF_name, workflow)

if __name__ == "__main__":
    liste_shell_files = []
    liste_python_files = []
    for s in subjects:
        name_shell_file = create_shell_file(s)
        name_python_file = create_python_file(s, name_shell_file)
        #liste_shell_files.append(name_shell_file)
        liste_python_files.append(name_python_file)

create_somaWF(liste_python_files)
