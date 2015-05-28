"""
Implement the level-1 GLM on a subject by subject basis on the cortical surface

Todo: both hemispheres

Author: Bertrand Thirion, 2013
"""
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from joblib import Memory
from joblib import Parallel, delayed

from nipy.modalities.fmri.glm import GeneralLinearModel
from utils import (
    audiosentence_paradigm, audiosentence_dmtx, audiosentence_contrasts,
    fixed_effects, make_mask, define_contrast_audiosentence, make_ratings,
    localizer_dmtx, localizer_contrasts, visualcategs_dmtx, 
    visualcategs_contrasts)
from nibabel.gifti import read, write, GiftiDataArray, GiftiImage

#subjects = ['cf120444','jl120341','lr120300','aa130114','aa130169','mk130199',
#            'jl130200','mp130263','rm130241','al130244','bm120103','ce130459',
#            'of140017','jf140025','cr140040','fm120345','hr120357','kg120369',
#            'mr120371','jc130030','ld130145','cf140022','jn140034','mv140024',
#            'tj140029','ap140030','af140169','pp140165','eb140248','gq140243']
            
subjects = ['subject01','subject02','subject03','subject04',
            'subject05','subject06','subject07','subject08',
            'subject09','subject10','subject11','subject12',
            'subject13','subject14']
#
#work_dir = '/neurospin/tmp/mathematicians'
#spm_dir = os.path.join('/neurospin/unicog/protocols/IRMf', 
#                       'mathematicians_Amalric_Dehaene2012/fMRI_data/')
#behavioral_dir = '/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012/behavioral_data/'

work_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data'
spm_dir = os.path.join(work_dir,'fmri_results')


# some fixed parameters
#tr = 1.5 # TR
tr = 2.4 # TR
contrast_names = []

def run_glms(subject):
    # necessary paths
    #analysis_dir = os.path.join(spm_dir, subject, 'analyses')
    subject_dir = os.path.join(work_dir, subject)
    if os.path.exists(subject_dir) == False:
        os.mkdir(subject_dir)
    #fmri_dir = os.path.join(subject_dir, 'fmri')
    fmri_dir = os.path.join(subject_dir, 'fmri_results')
    if os.path.exists(fmri_dir) == False:
        os.mkdir(fmri_dir)
    #result_dir = os.path.join(fmri_dir, 'results')
    result_dir = os.path.join(work_dir, 'surface_glm', subject)
    if os.path.exists(result_dir) == False:
        os.mkdir(result_dir)
    memory = Memory(cachedir=os.path.join(fmri_dir, 'cache_dir'), verbose=0)
    
#    # audiosentence protocol
#    # step 1: get the necessary files
#    spm_fmri_dir = os.path.join(spm_dir, subject, 'fMRI/audiosentence')
#    onset_dir = os.path.join(analysis_dir, 'audiosentence')
#    onset_files = glob.glob(os.path.join(onset_dir, 'onsetfile*.mat'))
#    motion_files = glob.glob(
#        os.path.join(spm_fmri_dir, 'rp*.txt'))
#    left_fmri_files = glob.glob(os.path.join(spm_fmri_dir, 'sraaudio*_lh.gii'))
#    right_fmri_files = glob.glob(os.path.join(spm_fmri_dir, 'sraaudio*_rh.gii'))
#    onset_files.sort()
#    motion_files.sort()
#    left_fmri_files.sort()
#    right_fmri_files.sort()
#    
#    # get the ratings of the trials
#    final_data = os.path.join(behavioral_dir, subject,
#                               'finaldata_%s.mat' %subject)
#    ratings = make_ratings(final_data)
#    
#    # scan times
#    n_scans = 200
#    lh_effects, lh_variances, rh_effects, rh_variances = {}, {}, {}, {}
#    for i, (onset_file, motion_file, left_fmri_file, right_fmri_file) in\
#            enumerate(zip(
#            onset_files, motion_files, left_fmri_files, right_fmri_files)):
#        # Create the design matrix
#        dmtx = audiosentence_dmtx(final_data, motion_file, n_scans, tr, i)
#        ax = dmtx.show()
#        ax.set_position([.05, .25, .9, .65])
#        ax.set_title('Design matrix')
#        session_contrasts = audiosentence_contrasts(dmtx.names, final_data, i)
#        fmri_glm = GeneralLinearModel(dmtx.matrix)
#
#        # left hemisphere
#        Y = np.array([darrays.data for darrays in read(left_fmri_file).darrays])
#        # fit the GLM
#        fmri_glm.fit(Y, model='ar1')
#        # Estimate the contrasts
#        print('Computing contrasts...')
#        for index, contrast_id in enumerate(session_contrasts):
#            print('  Contrast % i out of %i: %s' %
#                  (index + 1, len(session_contrasts), contrast_id))
#            # save the z_image
#            contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
#            if i == 0:
#                lh_effects[contrast_id] = [contrast_.effect.ravel()]
#                lh_variances[contrast_id] = [contrast_.variance.ravel()]
#            else:
#                lh_effects[contrast_id].append(contrast_.effect.ravel())
#                lh_variances[contrast_id].append(contrast_.variance.ravel())
#        
#        # right hemisphere
#        Y = np.array(
#            [darrays.data for darrays in read(right_fmri_file).darrays])
#        # fit the GLM
#        fmri_glm.fit(Y, model='ar1')
#
#        # Estimate the contrasts
#        
#        for index, contrast_id in enumerate(session_contrasts):
#            # save the z_image
#            contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
#            if i == 0:
#                rh_effects[contrast_id] = [contrast_.effect.ravel()]
#                rh_variances[contrast_id] = [contrast_.variance.ravel()]
#            else:
#                rh_effects[contrast_id].append(contrast_.effect.ravel())
#                rh_variances[contrast_id].append(contrast_.variance.ravel())
#        
#    
#    for index, contrast_id in enumerate(session_contrasts):
#        # left hemisphere
#        _, _, z_map = fixed_effects(
#            lh_effects[contrast_id], lh_variances[contrast_id])
#        z_texture = GiftiImage(
#            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
#        z_map_path = os.path.join(result_dir, '%s_z_map_lh.gii' % contrast_id)
#        write(z_texture, z_map_path)
#        # right hemisphere
#        _, _, z_map = fixed_effects(
#            rh_effects[contrast_id], rh_variances[contrast_id])
#        z_texture = GiftiImage(
#            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
#        z_map_path = os.path.join(result_dir, '%s_z_map_rh.gii' % contrast_id)
#        write(z_texture, z_map_path)

    #########################################################################
    # localizer protocol
    # get the necessary files
    #spm_fmri_dir = os.path.join(spm_dir, subject, 'fMRI/localizer')
    spm_fmri_dir = os.path.join(spm_dir, subject, 'data')
#    motion_file, = glob.glob(
#        os.path.join(spm_dir, subject, 'fMRI/localizer/rp*.txt'))
#    left_fmri_file = glob.glob(
#        os.path.join(spm_fmri_dir, 'sralocalizer*_lh.gii'))[0]
#    right_fmri_file = glob.glob(
#        os.path.join(spm_fmri_dir, 'sralocalizer*_rh.gii'))[0]
    
    tmp = os.path.join(spm_fmri_dir, 'srafun_rh.gii')    
    print tmp
    motion_file, = glob.glob(
        os.path.join(spm_fmri_dir, 'rp*.txt'))
    left_fmri_file = glob.glob(
        os.path.join(spm_fmri_dir, 'srafun_lh.gii'))[0]
    right_fmri_file = glob.glob(
        os.path.join(spm_fmri_dir, 'srafun_rh.gii'))[0]    
    
    
    #n_scans = 205
    n_scans = 128
    
    # Create the design matrix
    dmtx = localizer_dmtx(motion_file, n_scans, tr)
    ax = dmtx.show()
    ax.set_position([.05, .25, .9, .65])
    ax.set_title('Design matrix')
    session_contrasts = localizer_contrasts(dmtx)
    fmri_glm = GeneralLinearModel(dmtx.matrix)
    
    # left hemisphere
    Y = np.array([darrays.data for darrays in read(left_fmri_file).darrays])
    # fit the GLM
    fmri_glm.fit(Y, model='ar1')
    # Estimate the contrasts
    print('Computing contrasts...')
    for index, contrast_id in enumerate(session_contrasts):
        print('  Contrast % i out of %i: %s' %
              (index + 1, len(session_contrasts), contrast_id))
        # save the z_image
        contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
        z_map = contrast_.z_score()
        z_texture = GiftiImage(
            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
        z_map_path = os.path.join(result_dir, '%s_z_map_lh.gii' % contrast_id)
        write(z_texture, z_map_path)

    # right hemisphere
    Y = np.array([darrays.data for darrays in read(right_fmri_file).darrays])
    # fit the GLM
    fmri_glm.fit(Y, model='ar1')
    # Estimate the contrasts
    print('Computing contrasts...')
    for index, contrast_id in enumerate(session_contrasts):
        print('  Contrast % i out of %i: %s' %
              (index + 1, len(session_contrasts), contrast_id))
        # save the z_image
        contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
        z_map = contrast_.z_score()
        z_texture = GiftiImage(
            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
        z_map_path = os.path.join(result_dir, '%s_z_map_rh.gii' % contrast_id)
        write(z_texture, z_map_path)
    
#    #########################################################################
#    # VisualCategs protocol
#    # get the necessary files
#    spm_fmri_dir = os.path.join(spm_dir, subject, 'fMRI/visualcategs')
#    onset_dir = os.path.join(analysis_dir, 'visualcategs')
#    onset_files = glob.glob(os.path.join(onset_dir, 'onsetfile*.mat'))
#    motion_files = glob.glob(
#        os.path.join(spm_dir, subject, 'fMRI/visualcategs/rp*.txt'))
#    fmri_files = glob.glob(os.path.join(fmri_dir, 'crvisu*.nii.gz'))
#    onset_files.sort()
#    motion_files.sort()
#    fmri_files.sort()
#
#    left_fmri_files = glob.glob(
#        os.path.join(spm_fmri_dir, 'sravisu*_lh.gii'))
#    right_fmri_files = glob.glob(
#        os.path.join(spm_fmri_dir, 'sravisu*_rh.gii'))
#    n_scans = 185
#
#    lh_effects, lh_variances, rh_effects, rh_variances = {}, {}, {}, {}
#    
#    for i, (onset_file, motion_file, left_fmri_file, right_fmri_file) in\
#            enumerate(zip(
#            onset_files, motion_files, left_fmri_files, right_fmri_files)):
#        # Create the design matrix
#        dmtx = visualcategs_dmtx(onset_file, motion_file, n_scans, tr)
#        ax = dmtx.show()
#        ax.set_position([.05, .25, .9, .65])
#        ax.set_title('Design matrix')
#        session_contrasts = visualcategs_contrasts(dmtx.names)
#        fmri_glm = GeneralLinearModel(dmtx.matrix)
#    
#        # left hemisphere
#        Y = np.array([darrays.data for darrays in read(left_fmri_file).darrays])
#        # fit the GLM
#        fmri_glm.fit(Y, model='ar1')
#        # Estimate the contrasts
#        print('Computing contrasts...')
#        for index, contrast_id in enumerate(session_contrasts):
#            print('  Contrast % i out of %i: %s' %
#                  (index + 1, len(session_contrasts), contrast_id))
#            # save the z_image
#            contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
#            if i == 0:
#                lh_effects[contrast_id] = [contrast_.effect.ravel()]
#                lh_variances[contrast_id] = [contrast_.variance.ravel()]
#            else:
#                lh_effects[contrast_id].append(contrast_.effect.ravel())
#                lh_variances[contrast_id].append(contrast_.variance.ravel())
#
#        # right hemisphere
#        Y = np.array([
#                darrays.data for darrays in read(right_fmri_file).darrays])
#        # fit the GLM
#        fmri_glm.fit(Y, model='ar1')
#        # Estimate the contrasts
#        print('Computing contrasts...')
#        for index, contrast_id in enumerate(session_contrasts):
#            print('  Contrast % i out of %i: %s' %
#                  (index + 1, len(session_contrasts), contrast_id))
#            # save the z_image
#            contrast_ = fmri_glm.contrast(session_contrasts[contrast_id])
#            if i == 0:
#                rh_effects[contrast_id] = [contrast_.effect.ravel()]
#                rh_variances[contrast_id] = [contrast_.variance.ravel()]
#            else:
#                rh_effects[contrast_id].append(contrast_.effect.ravel())
#                rh_variances[contrast_id].append(contrast_.variance.ravel())
#
#    for index, contrast_id in enumerate(session_contrasts):
#        # left hemisphere
#        _, _, z_map = fixed_effects(
#            lh_effects[contrast_id], lh_variances[contrast_id])
#        z_texture = GiftiImage(
#            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
#        z_map_path = os.path.join(result_dir, '%s_z_map_lh.gii' % contrast_id)
#        write(z_texture, z_map_path)
#        # right hemisphere
#        _, _, z_map = fixed_effects(
#            rh_effects[contrast_id], rh_variances[contrast_id])
#        z_texture = GiftiImage(
#            darrays=[GiftiDataArray().from_array(z_map, intent='t test')])
#        z_map_path = os.path.join(result_dir, '%s_z_map_rh.gii' % contrast_id)
#        write(z_texture, z_map_path)


Parallel(n_jobs=4)(delayed(run_glms)(subject) for subject in subjects)
