# -*- coding: utf-8 -*-
"""
Script for:
    - preproc 
    - first-level analysis 
and using a first beta version of https://github.com/neurospin/pypreprocess.
"""

import time
import os
import sys
import numpy as np

import nibabel

from pypreprocess.external.nistats.glm import FirstLevelGLM
from pypreprocess.external.nistats.design_matrix import make_design_matrix
from pypreprocess.reporting.base_reporter import ProgressReport
from pypreprocess.reporting.glm_reporter import generate_subject_stats_report
from pypreprocess.nipype_preproc_spm_utils import do_subjects_preproc
from pypreprocess.conf_parser import _generate_preproc_pipeline

import paradigm_contrasts

#############################################################################
# preproc
def preproc(jobfile):
    subject_data = do_subjects_preproc(jobfile, report=True)
    return subject_data


#############################################################################
# firstLevel
def first_level(subject_dic):
    # experimental paradigm meta-params
    stats_start_time = time.ctime()
    tr = 2.4
    drift_model = 'blank'
    #hrf_model = 'canonical'  # hemodynamic reponse function
    hrf_model = 'spm'  # hemodynamic reponse function
    hfcut = 128.
    n_scans = 128

    # make design matrices
    mask_images = []
    design_matrices = []
    fmri_files = subject_dic['func']

    for x in xrange(len(fmri_files)):
        paradigm = paradigm_contrasts.localizer_paradigm()

        # build design matrix
        frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)
        design_matrix = make_design_matrix(
            frametimes,
            paradigm, hrf_model=hrf_model,
            drift_model=drift_model, period_cut=hfcut,
            )
        design_matrices.append(design_matrix)

    # Specify contrasts
    contrasts = paradigm_contrasts.localizer_contrasts(paradigm)
    for contrast_id, contrast_val in contrasts.items():
        contrasts[contrast_id] = np.append(contrast_val, 1.)
    
    #create output directory
    subject_session_output_dir = os.path.join(subject_dic['output_dir'],
                                                  'res_stats')

    if not os.path.exists(subject_session_output_dir):
             os.makedirs(subject_session_output_dir)

    # Fit GLM
    print 'Fitting a GLM (this takes time)...'    
    fmri_glm = FirstLevelGLM(noise_model='ar1', standardize=False).fit(fmri_files,
                               [design_matrix
                                for design_matrix in design_matrices]
                               )

    # save computed mask
    mask_path = os.path.join(subject_session_output_dir,
                             "mask.nii.gz")
    nibabel.save(fmri_glm.masker_.mask_img_, mask_path)
    mask_images.append(mask_path)

    # compute contrasts
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


        # store stat maps to disk
        for map_type, out_map in zip(['z', 't', 'effects', 'variance'],
                                  [z_map, t_map, effects_map, var_map]):
            map_dir = os.path.join(
                subject_session_output_dir, '%s_maps' % map_type)
            if not os.path.exists(map_dir):
                os.makedirs(map_dir)
            map_path = os.path.join(
                map_dir, '%s%s.nii.gz' %(subject_dic['subject_id'], contrast_id))
            print "\t\tWriting %s ..." % map_path
            nibabel.save(out_map, map_path)

            # collect zmaps for contrasts we're interested in
            if map_type == 'z':
                z_maps[contrast_id] = map_path
            if map_type == 'effects':
                effects_maps[contrast_id] = map_path

    # do stats report
    anat_img = nibabel.load(subject_dic['anat'])
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
        design_matrices=None,
        paradigm= paradigm,
        subject_id=subject_dic['session_id'],
        start_time=stats_start_time,
        title="GLM for subject %s" % subject_dic['session_id'],
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
    #File containing configuration for preprocessing the data
    jobfile=sys.argv[1]
    list_subjects, params =  _generate_preproc_pipeline(jobfile) 

    #Preproc
    subject_data = preproc(jobfile)
    
    #first_level
    for dict_subject in subject_data:
        dict_subject = dict_subject.__dict__
        z_maps = first_level(dict_subject)
