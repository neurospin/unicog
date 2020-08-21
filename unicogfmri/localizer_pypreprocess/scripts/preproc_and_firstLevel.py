#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:06:19 2020

@author: id983365
"""

import time
import os
import numpy as np
import glob
import nibabel

from nistats.design_matrix import (make_first_level_design_matrix,
                                   check_design_matrix)
from nistats.first_level_model import FirstLevelModel
from nistats.reporting import make_glm_report

from pypreprocess.nipype_preproc_spm_utils import do_subjects_preproc

from nilearn.masking import compute_epi_mask

import paradigm_contrasts



def first_level(subject):
    subject_id = subject['subject_id']
    data_dir = subject['output_dir']
    subject_session_output_dir = os.path.join(data_dir, 'res_stats')
    if not os.path.exists(subject_session_output_dir):
             os.makedirs(subject_session_output_dir)    

    design_matrices=[]

    for e, i in enumerate(subject['func']) :
        
        # Parameters
        tr = subject['TR']
        drift_model = None
        hrf_model = 'spm'  # hemodynamic reponse function
        hfcut = 128.
        fwhm = [5, 5, 5]
        n_scans = nibabel.load(subject['func'][e]).shape[3]
 
        # Preparation of paradigm
        events_file = subject['onset'][e]
        paradigm = paradigm_contrasts.localizer_paradigm(events_file)
        
        # Motion parameter
        motion_path = subject['realignment_parameters'][e]
        motion_names = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        motion = np.loadtxt(motion_path)
        
        
        # Build design matrix
        frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)
        design_matrix = make_first_level_design_matrix(
                frametimes, paradigm, hrf_model=hrf_model, drift_model=drift_model,
                high_pass=hfcut, add_regs=motion,
                add_reg_names=motion_names)
        _, dmtx, names = check_design_matrix(design_matrix)
        design_matrices.append(design_matrix)
        #print(names)
    
    # Specify contrasts
    contrasts = paradigm_contrasts.localizer_contrasts(design_matrix)

    # GLM Analysis
    print('Fitting a GLM (this takes time)...')    
    
    #for mask_img; use the False or the mask of t1 mni template
    #the computed mask by default on fmri seems not always correct.
    # For a specific mask, try this: 
    #mask_path = os.path.join(subject_session_output_dir, "mask.nii.gz")
    #mask = compute_epi_mask(fmri_f)
    #nibabel.save(mask , mask_path)
    #mask_images.append(compute_epi_mask(mask))
    
    fmri_glm = FirstLevelModel(mask_img=False, t_r=tr,
                               smoothing_fwhm=fwhm).fit(subject['func'], design_matrices=design_matrices)                                        
                
    # compute contrasts
    z_maps = {}
    for contrast_id, contrast_val in contrasts.items():
        print("\tcontrast id: %s" % contrast_id)

        # store stat maps to disk
        for map_type in ['z_score', 'stat', 'effect_size', 'effect_variance']:
            stat_map = fmri_glm.compute_contrast(
                contrast_val, output_type=map_type)
            map_dir = os.path.join(
                subject_session_output_dir, '%s_maps' % map_type)
            if not os.path.exists(map_dir):
                os.makedirs(map_dir)
            map_path = os.path.join(map_dir, '%s.nii.gz' % contrast_id)
            print("\t\tWriting %s ..." % map_path)
            stat_map.to_filename(map_path)

            # collect zmaps for contrasts we're interested in
            if map_type == 'z_score':
                z_maps[contrast_id] = map_path

    anat_img = glob.glob(os.path.join(data_dir, 'anat/wsub*T1w.nii.gz'))[0]
    stats_report_filename = os.path.join(
        subject_session_output_dir, 'report_stats.html')

    report = make_glm_report(fmri_glm,
                             contrasts,
                             threshold=3.0,
                             bg_img=anat_img,
                             cluster_threshold=15,
                             title="GLM for subject %s" % subject_id,
                             )
    report.save_as_html(stats_report_filename)
                
    return z_maps

if __name__ == '__main__':
    subs = ["sub-01","sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08",
        "sub-09", "sub-10", "sub-11", "sub-12", "sub-13", "sub-14"]
    
    
    # Do one subject by one subject, otherwise it doesn't work for many subjects at time 
    for sub in subs:
        file_template = "/volatile/test/pypreprocess/test_localizer_bids/script/config_template.ini"
        new_text = ""
        with open(file_template , "r") as fichier:
            for line in fichier.readlines():
                if (line.find("include_only_these_subject_ids") != -1):
                    new_line = "include_only_these_subject_ids = " + sub +"\n\n"
                else : 
                    new_line = line
                new_text = new_text + new_line
    
        jobfile = "/volatile/test/pypreprocess/test_localizer_bids/script/config.ini"
        file_to_write = open(jobfile, "w")
        file_to_write.write(new_text)
        file_to_write.close()

        # Preproc
        subject_data = do_subjects_preproc(jobfile, report=True)
        print(subject_data)
        
        # Launch first level for each subject
        for subject in subject_data :
            z_maps = first_level(subject)

    
    
    
        
