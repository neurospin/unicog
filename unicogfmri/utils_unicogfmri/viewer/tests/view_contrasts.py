"""
Created on Mon Feb 24 15:12:04 2014

@author: id983365

Script to illustrate how you can select and display many fusions with the
/i2bm/local/spm8/canonical/single_subj_T1.nii.
In order to change the template, use the template_file option in fusion2D_map_activation

1- Configure paths
2- Select activation maps
3- Call the fusion2D_map_activation


In this example, we select a dictionary of contrasts across many subjects.
We suppose data are organized with the same structure.
if you want to add a selection of subjects, add a python list of subjects
and add a loop too.


"""

import glob
import os

from unicogfmri.utils_unicogfmri.viewer import pyanatomist_viewer

######  Parameters to change ###############################################

path_results = "/neurospin/unicog/protocols/IRMf/Unicogfmri/results6"
dic_maps = {}
contrasts_of_interest = ['left-right', 'right-left',
                         'audio-video', 'video-audio']
############################################################################
# Basic using


## glob files and add them to the dictionary
for c in contrasts_of_interest:
    #describe here your own pattern
    glob_files = glob.glob((path_results + "/*/" + '/res_stats/t_maps/*'
                        + c + '.nii.gz'))
    if glob_files:
        for file_name in glob_files:
            name_fusion = os.path.basename(file_name)
            name_fusion = name_fusion.replace(".nii.gz", "")
            #add in the dic {'name_fusion': file_name}
            dic_maps[name_fusion] = file_name

# print dic_maps
# call the function to display maps with the dictionary
pyanatomist_viewer.fusion2D_map_activation(dic_maps)

