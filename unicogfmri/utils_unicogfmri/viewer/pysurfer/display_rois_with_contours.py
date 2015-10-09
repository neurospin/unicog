# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:03:54 2015

@author: id983365
"""

import os
import glob
import numpy as np

# pysufer module
from surfer import Brain, io

# unicog module
from unicogfmri.utils_unicog import utils

# Ini the subjects_dir paramater
subjects_dir = "/PATH/FREESURFER_DATABASE"
os.environ['SUBECTS_DIR'] = subjects_dir

# Get the datadir
datadir = utils.get_rootdir()

# Glob the ROIs
rois = glob.glob(datadir + '/*.nii')


#  PLEASE READ THIS PART CAREFULLY
# If rois are in  MNI152, don't forget to register data
# reg_file = os.path.join(os.environ["FREESURFER_HOME"],
#                        "average/mni152.register.dat")
# If rois are in MNI305, nothing to do



# For 12 rois, if more, please add more colors
color_list = [[255, 255, 0], [255, 153, 18], [128, 142, 42],
            [0, 255, 0], [61, 145, 64], [50, 205, 50],
            [19, 95, 0], [0, 10, 12], [0, 31, 37],
            [255, 64, 64], [0, 0, 255], [201, 102, 250], 
            [78, 120, 255], [50, 200, 255], [166, 190, 205] ]

# Just for 'lh', remove [:1] for both
list_hemi = ['lh', 'rh'][:1]
list_hemi = ['rh', 'lh']


for hemi in list_hemi:
    #  Surface used to project 'white', 'inflated' or other, 
    #  Here we use the fsaverage of freesurfer as template
    surf = "inflated" 
    brain = Brain("fsaverage", hemi, surf, views=['lat'],
                  config_opts=dict(background="white", colorbar="False")) 
                  
    # ini some variables              
    cpt_color = 0 # for the colors
    pos_y = 0.9   # for y position of lables in figure
    pos_x = 0.9   # for y position of lables in figure
    
    for r in sorted(rois):  
    #   Name of ROI 
        name_roi = os.path.splitext(os.path.basename(r))[0]
        # same len of each name of roi because a specific scaling 
        # when the text_label.width property below
        size =  len(name_roi)
        name_roi = name_roi + " "*(12-size)            
        
    #   Manage the color for the label
        color = [val/255. for val in color_list[cpt_color]]

    #   Projection part
    #   If reg_file if needed: 
    #   surf_data = io.project_volume_data(r, "lh", reg_file)
    #   Projection parameters, see the docstring for more information
        projmeth = "frac" # frac' method, projection on a fraction of thickness
        projsum = "max"   # the max value is projected
        projarg = [0, 1, 0.1] # from 0 to 1 thickness fract every 0.1 step
        smooth_fwhm = 0       # no smoothing  
        surf_data = io.project_volume_data(r, hemi,
                                          projmeth=projmeth,
                                          projsum=projsum, 
                                          projarg=projarg,
                                          smooth_fwhm = smooth_fwhm,
                                          subject_id='fsaverage')
        
        # nothing to do, if all points in the projection are nul                              
        if surf_data.max()!=0:
            # Set the position of label
            if pos_x > 0.2:        
                pos_x -= 0.1
            else: # as add a new line
                pos_x = 0.9
                pos_y -= 0.05 
                
            # Set the text of the projection
            text = brain.add_text(pos_x, pos_y, color=tuple(color), 
                           text=name_roi, name=name_roi)
            text_label = brain.texts[name_roi]
            text_label.width = 0.1            
            
            # Add the projection and manage the color 
            name_overlay = '{name_roi}_{hemi}'.format(name_roi=name_roi, hemi=hemi)
            brain.add_overlay(surf_data, name=name_overlay, hemi=hemi)
            overlay_roi = brain.overlays[name_overlay]
            lut = overlay_roi.pos_bar.lut.table.to_array()
    #        lut = np.zeros((255, 4))
    #        print lut.shape
            lut[0:256, 0:3] = color_list[cpt_color]
    #        lut[0:255, 0:3] = [255, 255, 0]
            lut_alpha = lut
            lut_alpha[0:256, 3] = 100 # change opacity for the roi
            overlay_roi.pos_bar.lut.table = lut
                      
            # Add topographic contours
            brain.add_contour_overlay(surf_data,
                              min=0, max=10,
                              n_contours=10,
                              colormap = lut,
                              line_width=1,
                              remove_existing=False, 
                              colorbar = False) 
                             
            # Save in png   
            #brain.save_imageset(save_png, ['lat'], 'png', colorbar=None)  
            
            # Color cpt
            cpt_color += 1
            
            # If you just want one roi by one  
            # Remove for the next roi
            # for overlay in brain.overlays_dict[name_overlay]:
            #    overlay.remove()  
    
    # Save in png  
    save_png = os.path.join(datadir, "all_rois_{hemi}".format(hemi=hemi))  
    brain.save_imageset(save_png, ['lat'], 'png', colorbar=None) 
    brain.close()