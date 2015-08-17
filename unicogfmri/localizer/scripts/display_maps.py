"""
Visualization of maps
:Author: Isabelle Denghien
"""

import os
import glob

from unicogfmri.utils_unicog.viewer import pyanatomist_viewer


datadir = os.path.join(os.getenv('ROOTDIR'))
path_results = os.path.join(datadir, "results")
dic_maps = {}
contrasts_of_interest = ['left-right', 'right-left',
                         'audio-video', 'video-audio']

for c in contrasts_of_interest:
    #describe here your own pattern
    glob_files = glob.glob((path_results + "/*/" + '/res_stats/z_maps/*'
                        + c + '.nii.gz'))
    if glob_files:
        for file_name in glob_files:
            name_fusion = os.path.basename(file_name)
            name_fusion = name_fusion.replace(".nii.gz", "")
            #add in the dic {'name_fusion': file_name}
            dic_maps[name_fusion] = file_name

#print liste_z_maps
#view with Anatomist
pyanatomist_viewer.fusion2D_map_activation(dic_maps)
