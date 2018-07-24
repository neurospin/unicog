# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:49:36 2018

@author: id983365

"""

import time
import os
import numpy as np
import glob
import nibabel

from pypreprocess.external.nistats.glm import FirstLevelGLM
from pypreprocess.external.nistats.design_matrix import make_design_matrix
from pypreprocess.reporting.base_reporter import ProgressReport
from pypreprocess.reporting.glm_reporter import generate_subject_stats_report

import paradigm_contrasts



def first_level(subject_id):
    '''
    Launch the first level analysis for one subject
    ROOTDIR is an variable of environnmenent where your data are stored.
    ROOTDIR needs to be set up by the user.
    See: https://github.com/neurospin/pypreprocess/
    Tape: python first_level.py
    

    Keyword arguments:
    subject_id -- Name of the subject
    '''
    
    # Configure paths
    data_dir = os.path.join(os.environ["ROOTDIR"], "dataset", "bids_dataset", subject_id)
    output_dir = os.path.join(os.environ["ROOTDIR"], "processed_data", subject_id )
    subject_session_output_dir = os.path.join(output_dir, 'res_stats')
    if not os.path.exists(subject_session_output_dir):
             os.makedirs(subject_session_output_dir)    
    

    # Experimental paradigm meta-params
    stats_start_time = time.ctime()
    tr = 2.4
    drift_model = 'blank'
    #hrf_model = 'canonical'  # hemodynamic reponse function
    hrf_model = 'spm'  # hemodynamic reponse function
    hfcut = 128.
    n_scans = 128


    # Preparation of paradigm
    events_file = glob.glob(os.path.join(data_dir, 'func/*_task-standartloc_events.tsv'))[0]
    paradigm = paradigm_contrasts.localizer_paradigm(events_file)
    
    
    # Build design matrix
    frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)
    design_matrix = make_design_matrix(
        frametimes,
        paradigm, hrf_model=hrf_model,
        drift_model=drift_model, period_cut=hfcut,
        )


    # Specify contrasts
    contrasts = paradigm_contrasts.localizer_contrasts(design_matrix, events_file)
    
    
    # Fit GLM
    fmri_file = glob.glob(os.path.join(output_dir, 'func/wra*_task-standartloc_bold.nii.gz'))[0]
    print 'Fitting a GLM (this takes time)...'    
#    fmri_glm = FirstLevelGLM(noise_model='ar1', standardize=False).fit(fmri_files[0],
#                           [design_matrix for design_matrix in design_matrices]
#                           )
#    fmri_glm = FirstLevelGLM(noise_model='ar1', standardize=False).fit(fmri_file,
#                               [design_matrix for design_matrix in design_matrices]
#                               )
    fmri_glm = FirstLevelGLM(noise_model='ar1', standardize=False).fit(fmri_file,
                               design_matrix)
                               
                               
    # Save computed mask
    mask_images = []                        
    mask_path = os.path.join(subject_session_output_dir, "mask.nii.gz")
    nibabel.save(fmri_glm.masker_.mask_img_, mask_path)
    mask_images.append(mask_path)


    # Compute contrasts
    z_maps = {}
    effects_maps = {}
    for contrast_id, contrast_val in contrasts.iteritems():
        print "\tcontrast id: %s" % contrast_id
        z_map, t_map, effects_map, var_map = fmri_glm.transform([contrast_val] * 1, 
                                    contrast_name=contrast_id,
                                    output_z=True,
                                    output_stat=True,
                                    output_effects=True,
                                    output_variance=True)


        # Store stat maps to disk
        for map_type, out_map in zip(['z', 't', 'effects', 'variance'],
                                  [z_map, t_map, effects_map, var_map]):
            map_dir = os.path.join(
                subject_session_output_dir, '%s_maps' % map_type)
            if not os.path.exists(map_dir):
                os.makedirs(map_dir)
            map_path = os.path.join(
                map_dir, '%s%s.nii.gz' %(subject_id, contrast_id))
            print "\t\tWriting %s ..." % map_path
            nibabel.save(out_map, map_path)

            # collect zmaps for contrasts we're interested in
            if map_type == 'z':
                z_maps[contrast_id] = map_path
            if map_type == 'effects':
                effects_maps[contrast_id] = map_path


    # Do stats report
    anat_file = glob.glob(os.path.join(output_dir, 'anat/w*_T1w.nii.gz'))[0]
    anat_img = nibabel.load(anat_file)
    stats_report_filename = os.path.join(subject_session_output_dir,
                                         "report_stats.html")                              
    generate_subject_stats_report(
        stats_report_filename,
        contrasts,
        z_maps,
        fmri_glm.masker_.mask_img_,
        threshold=2.3,
        cluster_th=15,
        anat=anat_img,
        anat_affine=anat_img.get_affine(),
        design_matrices=[design_matrix],
        paradigm= paradigm,
        subject_id=subject_id,
        start_time=stats_start_time,
        title="GLM for subject %s" % subject_id,
        # additional ``kwargs`` for more informative report
        TR=tr,
        n_scans=n_scans,
        hfcut=hfcut,
        frametimes=frametimes,
        drift_model=drift_model,
        hrf_model=hrf_model,
        )

    ProgressReport().finish_dir(subject_session_output_dir)
    print "Statistic report written to %s\r\n" % stats_report_filename
    return z_maps

if __name__ == '__main__':
    # Create the liste of subject, e.g., ['sub-01', 'sub-02']
    subject_list = ['sub-%.2d' %i for i in range(1,3)]

    # Launch first level for each subject
    for subject_id in subject_list:
        z_maps = first_level(subject_id)
        
