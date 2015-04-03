"""
Created on Mon Feb 24 15:12:04 2014

@author: id983365

Script to illustrate how you can select and display many fusions with their
anatomy file

1- Configure paths
2- Select activation maps and anatomy
3- call the fusion2D_map_activation

In this example, we select a dictionary of contrasts across many subjects

And we suppose data are organized with the same structure.
 - for using a specific template for each maps
in this case, add dic_template with the same structure than dic_maps
so the key referters to same fusion in both dictionaries.
"""


from unicogfmri.utils_unicog.viewer import pyanatomist_viewer
import glob
import os


######  Parameters to change ###############################################
path_results = "/neurospin/unicog/protocols/IRMf/Unicogfmri/results6"
contrasts_of_interest = ['left-right', 'right-left',
                         'audio-video', 'video-audio']
#dic_template and dic_maps share the same key
dic_maps = {}
dic_templates = {}


######  Glob files  ########################################################
#glob subjects
glob_subjects = glob.glob((path_results + "/*"))  

for s in glob_subjects:
    subj = s.split('/')[-1]
    for c in contrasts_of_interest:
        #glob files for maps activation
        glob_files = glob.glob((path_results + "/" + subj + '/res_stats/t_maps/*'
                            + c + '.nii.gz'))     

        #glob files for T1 normalized
        glob_files2 = glob.glob((path_results + "/" + subj + '/data/wanat.nii'))     

        if glob_files2 and glob_files:
            for file_name in glob_files:
                name_fusion = os.path.basename(file_name)
                name_fusion = name_fusion.replace(".nii.gz", "")
                #add in the dic {'name_fusion': file_name}
                dic_maps[name_fusion] = file_name   

            for file_name in glob_files2:
                dic_templates[name_fusion] = file_name


#call the function to display maps with the dictionary
pyanatomist_viewer.fusion2D_map_activation(dic_maps=dic_maps, dic_templates=dic_templates)
