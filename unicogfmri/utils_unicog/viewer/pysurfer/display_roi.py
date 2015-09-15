# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:03:54 2015

@author: id983365
"""

import os
import glob

from surfer import Brain, io


# Ini the subjects_dir paramater
subjects_dir = "/neurospin/unicog/protocols/IRMf/Tests_Isa/dataBase_FS_brainvisa"
os.environ['SUBECTS_DIR'] = subjects_dir

# Get the datadir
#datadir = utils.get_rootdir()
datadir = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_pysurfer"


# Glob the ROIs
rois = glob.glob(datadir + '/*.nii')

#  PLEASE READ THIS PART CAREFULLY
# If rois are in  MNI152, don't forget to register data
# reg_file = os.path.join(os.environ["FREESURFER_HOME"],
#                        "average/mni152.register.dat")
# If rois are in MNI305, nothing to do

# For 12 rois, if more, please add more colors
color_list = [[255, 255, 0], [255, 153, 18], [128, 42, 42],
            [0, 255, 0], [61, 145, 64], [50, 205, 50],
            [106, 90, 205], [19, 795, 0], [0, 10, 12], 
            [0, 31, 37], [255, 64, 64], [0, 0, 255] ]
cpt_color = 0
pos_y = 0.7

# Just for 'lh', remove [:1] for both
list_hemi = ['lh', 'rh'][:1]



for hemi in list_hemi:
    """Bring up the visualization"""
   
    #  Surface used to project 'white', 'inflated' or other
    surf = "inflated" 
    brain = Brain("fsaverage", hemi, surf, views=['lat'],
                  config_opts=dict(background="white", colorbar="False")) 
    for r in sorted(rois):  
    #   Name of ROI 
        name_roi = os.path.splitext(os.path.basename(r))[0]
        save_png= os.path.join(datadir, "{h}_{name_roi}".format(h=hemi, name_roi=name_roi))
        
    #   Manage the color
        color = [val/255. for val in color_list[cpt_color]]

    #   Add a title 
        pos_y += 0.05
        text = brain.add_text(0.1, pos_y, color=tuple(color), 
                       text=name_roi, name=name_roi)
        text = brain.texts[name_roi]
        text.width = 0.2

    #   Projection part
    #   If reg_file if needed: 
    #   surf_data = io.project_volume_data(r, "lh", reg_file)
    #   Projection parameters, see the docstring for more information
        projmeth = "frac" # frac' methode, projection on a fraction of thickness
        projsum = "max"   #the max value is projected
        projarg = [0, 1, 0.1] # from 0 to 1 thickness fract every 0.1 step
        smooth_fwhm = 0       # no smoothing  
        io.project_volume_data()
        surf_data = io.project_volume_data(r, hemi,
                                          projmeth=projmeth,
                                          projsum=projsum, 
                                          projarg=projarg,
                                          smooth_fwhm = smooth_fwhm,
                                          subject_id='fsaverage')
#        surf_data= io.project_volume_data(r, hemi,             
#                                          subject_id='fsaverage')
        name_overlay = '{name_roi}_{hemi}'.format(name_roi=name_roi, hemi=hemi)
        brain.add_overlay(surf_data, name=name_overlay, hemi=hemi)
        overlay_roi = brain.overlays[name_overlay]
        lut = overlay_roi.pos_bar.lut.table.to_array()
        lut[0:255, 0:3] = color_list[cpt_color]
        overlay_roi.pos_bar.lut.table = lut
        
    #   Save in png   
        brain.save_imageset(save_png, ['lat'], 'png', colorbar=None)  
        
    #   Color cpt
        cpt_color += 1
        
    #   If you just want one roi by one  
    #   Remove for the next roi
#        for overlay in brain.overlays_dict[name_overlay]:
#            overlay.remove()  
        
    brain.close()