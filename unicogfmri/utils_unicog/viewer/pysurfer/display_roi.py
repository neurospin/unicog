# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:03:54 2015

@author: id983365
"""

import os
import glob
import pdb


from surfer import Brain, io

from unicogfmri.utils_unicog.utils import utils



# Ini the subjects_dir paramater
subjects_dir = "/PATH_FREESURFER_DATABASE"

# Get the datadir
datadir = utils.get_rootdir()

# Glob the ROIs
rois = glob.glob(datadir + '/*.nii')

#  PLEASE READ THIS PART CAREFULLY
#If rois are in  MNI152, don't forget to register data
#reg_file = os.path.join(os.environ["FREESURFER_HOME"],
#                        "average/mni152.register.dat")
#If rois are in MNI305, nothing to do

list_hemi = ['rh', 'lh']
for hemi in list_hemi:
    """Bring up the visualization"""
    brain = Brain("fsaverage", hemi, "inflated", views=['lat'],
                  config_opts=dict(background="white", colorbar="False")) 
    for r in rois:  
    #   Name of ROI 
        name_roi = os.path.splitext(os.path.basename(r))[0]
        save_png= os.path.join(datadir, "{h}_{name_roi}".format(h=hemi, name_roi=name_roi))
        
    #   Add a title    
        brain.add_text(0.3, 0.8, color = (0, 0, 0), text=name_roi, name='title')
     
    #   If reg_file if needed: 
    #   surf_data = io.project_volume_data(r, "lh", reg_file)
        surf_data= io.project_volume_data(r, hemi, subject_id='fsaverage')
        name_overlay = '{name_roi}_{hemi}'.format(name_roi=name_roi, hemi=hemi)
        brain.add_overlay(surf_data, name=name_overlay, hemi=hemi)
        overlay_roi = brain.overlays[name_overlay]
        lut = overlay_roi.pos_bar.lut.table.to_array()
        overlap = [116, 208, 241] # RGB color code
        lut[0:255, 0:3] = overlap
        overlay_roi.pos_bar.lut.table = lut
        
    #   Save in png   
        brain.save_imageset(save_png, ['lat'], 'png', colorbar=None)    
    
    #   Remove for the next roi
        for overlay in brain.overlays_dict[name_overlay]:
            overlay.remove()  
    brain.close()

    

