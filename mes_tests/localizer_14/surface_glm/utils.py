# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:08:50 2014

@author: mamalric
"""

""" Utility functions for GLM analysis

Author: Bertrand Thirion, 2013
"""

import numpy as np
from scipy.io import loadmat
from nibabel import load, Nifti1Image
import operator

from nipy.modalities.fmri.experimental_paradigm import BlockParadigm
from nipy.modalities.fmri.design_matrix import make_dmtx


def audiosentence_paradigm(datfile, n_run):

    run_data = loadmat(datfile) 
    n_trials = run_data['nb_trials'][0][0]  
    #n_trials = len(np.concatenate([x.ravel() for x in run_data['onsets'][0]]))
    correspondence = run_data['correspondance_final']
    sentence_type = np.mod(correspondence[:,1], 15) # number in [0;14] for the 15 different types
    session_indexes = np.arange(n_run * n_trials, (n_run + 1)* n_trials)
    	
    all_onsets = np.concatenate(
        [x.ravel() for x in run_data['time_data'][session_indexes]])
    sentence_type_for_this_run = sentence_type[session_indexes]
	
    names = [""]*33
    durations = np.zeros(30)   
    onsets = np.zeros(30)   
	   
    i_regressor = -1
    for i_stim in range(n_trials):
        ind = np.where(sentence_type_for_this_run == i_stim)[0][0]
        if i_stim == 0: 
            names[28] = 'trial_15_reg1' 
            names[29] = 'trial_15_reg2' 
            onsets[28] = all_onsets[ind*6] 
            onsets[29] = all_onsets[ind*6 + 1]
            durations[28] = all_onsets[ind*6 + 1] - all_onsets[ind*6]
            durations[29] = all_onsets[ind*6 + 3] - all_onsets[ind*6 + 1]
			
        else:
            for i_onset in range(1,3):
                i_regressor = i_regressor + 1
                names[i_regressor] = "trial_%02d_reg%d" % (i_stim, i_onset) 
                if i_onset == 1:
                    onsets[i_regressor] = all_onsets[ind*6]  # onsets are already saved after subtraction of the TTL clock onset
                    durations[i_regressor] = all_onsets[ind*6 + 1] - all_onsets[ind*6]
                elif i_onset == 2: # starts at sentence OFFSET, ends at the response
                    onsets[i_regressor] = all_onsets[ind*6 + 1]
                    durations[i_regressor] = all_onsets[ind*6 + 3] - all_onsets[ind*6 + 1]
               
    i_regressor = i_regressor +3
    names[i_regressor] = 'alert signal'
    onsets_recup = []
    [onsets_recup.append(all_onsets[i_stim*6 + 5]) for i_stim in range(n_trials)]
    onsets = np.concatenate((onsets, np.array(onsets_recup)),0)
    durations = np.concatenate((durations, 0.1*np.ones(n_trials)),0)
            
    i_regressor = i_regressor +1
    names[i_regressor] = 'response signal'
    onsets_recup = []
    [onsets_recup.append(all_onsets[i_stim*6 + 2]) for i_stim in range(n_trials)]    
    onsets = np.concatenate((onsets, np.array(onsets_recup)),0)
    durations = np.concatenate((durations, 0.1*np.ones(n_trials)),0)
            
    i_regressor = i_regressor +1
    names[i_regressor] = 'key press'
    onsets_recup = []
    [onsets_recup.append(all_onsets[i_stim*6 + 3]) for i_stim in range(n_trials)]
    onsets = np.concatenate((onsets, np.array(onsets_recup)),0)
    durations = np.concatenate((durations, 0.1*np.ones(n_trials)),0)
    
    names = np.concatenate((names[:-3], np.repeat(names[-3:], n_trials)))
    
    return BlockParadigm(names, onsets, durations)
   
  
'''
def audiosentence_paradigm(onset_file):
    """utility for audiosentence paradigm creation from the matlab onset file"""
    paradigm_data = loadmat(onset_file)
    durations = np.concatenate(
        [x.ravel() for x in paradigm_data['durations'][0]])
    onsets = np.concatenate(
        [x.ravel() for x in paradigm_data['onsets'][0]])
    names = np.concatenate(
        [x.ravel() for x in paradigm_data['names'][0]]).astype(str)
    names = np.concatenate((names[:-3], np.repeat(names[-3:], 16)))
    return BlockParadigm(names, onsets, durations)
'''

def audiosentence_dmtx(datfile, motion_file, n_scans, tr, n_run):
    """Utility for ceating a design matrix from onset and motion files"""
    # Some default parameters
    hrf_model = 'canonical'  # hemodynamic reponse function
    drift_model = 'cosine'   # drift model 
    hfcut = 128              # low frequency cut
    motion_names = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'] 
    # motion param identifiers
    frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)

    paradigm = audiosentence_paradigm(datfile, n_run)
    #paradigm = audiosentence_paradigm(onset_file)
    
    # add motion regressors and low frequencies
    # and create the design matrix
    motion_params = np.loadtxt(motion_file)
    dmtx = make_dmtx(frametimes, paradigm, hrf_model=hrf_model,
                     drift_model=drift_model, hfcut=hfcut,
                     add_regs=motion_params, add_reg_names=motion_names)
    return dmtx


def audiosentence_contrasts(names_, final_data, n_session):
    """Create the contrasts,
    given the names of the columns of the design matrix

    names_: list of strings
    ratings: list of arrays,
             high-level variables describing the trials 
    """
    ratings = define_contrast_audiosentence(final_data)

    n_reg = len(ratings[0]) / 6  # assumes that  there are 6 eqaully length sessions

    # keep only the values relavant for the session that you are considering
    session_indexes = np.arange(n_session * n_reg, (n_session + 1)* n_reg)
    (vrai, faux, meaningless, meaningful, math, language, math_true, math_false, math_meaningless, math_meaningful, 
    analyse_true, analyse_false, analyse_meaningless, algebra_true, algebra_false, algebra_meaningless, topo_true,
    topo_false, topo_meaningless, geo_true, geo_false, geo_meaningless, nonmath_true, nonmath_false, nonmath_meaningless,
    analyse_meaningful, algebra_meaningful, topo_meaningful, geo_meaningful, nonmath_meaningful, math_intuitive, 
    math_nonintuitive, math_imagery, math_nonimagery) = (
        [np.array(ratings[x])[session_indexes] for x in range(len(ratings))])    
        
#        ratings[0][session_indexes], ratings[1][session_indexes],
#        ratings[2][session_indexes], ratings[3][session_indexes], 
#        ratings[4][session_indexes], ratings[5][session_indexes], 
#        ratings[6][session_indexes], ratings[7][session_indexes], 
#        ratings[8][session_indexes], ratings[9][session_indexes], 
#        ratings[10][session_indexes], ratings[11][session_indexes], 
#        ratings[12][session_indexes], ratings[13][session_indexes], 
#        ratings[14][session_indexes], ratings[15][session_indexes], 
#        ratings[16][session_indexes], ratings[17][session_indexes], 
#        ratings[18][session_indexes], ratings[19][session_indexes], 
#        ratings[20][session_indexes], ratings[21][session_indexes], 
#        ratings[22][session_indexes], ratings[23][session_indexes], 
#        ratings[24][session_indexes], ratings[25][session_indexes], 
#        ratings[26][session_indexes], ratings[27][session_indexes], 
#        ratings[28][session_indexes], ratings[29][session_indexes], 
#        ratings[30][session_indexes], ratings[31][session_indexes],
#        ratings[32][session_indexes], ratings[33][session_indexes])
#        
#[   
        
    # Caveat: assumes that  names_ order is:
    # 'alert signal', 'key press', 'response signal',  'trial_01_ ...
    reordering = np.concatenate((np.arange(30, 33), np.arange(30), 
                                np.arange(33, 39)))

    (vrai, faux, meaningless, meaningful, math, language, math_true, math_false, math_meaningless, math_meaningful, 
    analyse_true, analyse_false, analyse_meaningless, algebra_true, algebra_false, algebra_meaningless, topo_true,
    topo_false, topo_meaningless, geo_true, geo_false, geo_meaningless, nonmath_true, nonmath_false, nonmath_meaningless,
    analyse_meaningful, algebra_meaningful, topo_meaningful, geo_meaningful, nonmath_meaningful, math_intuitive, 
    math_nonintuitive, math_imagery, math_nonimagery) = (
        vrai[reordering], faux[reordering], meaningless[reordering], 
        meaningful[reordering], math[reordering], language[reordering], math_true[reordering], 
        math_false[reordering], math_meaningless[reordering], math_meaningful[reordering], 
        analyse_true[reordering], analyse_false[reordering], 
        analyse_meaningless[reordering], algebra_true[reordering], 
        algebra_false[reordering], algebra_meaningless[reordering], 
        topo_true[reordering], topo_false[reordering], topo_meaningless[reordering], 
        geo_true[reordering], geo_false[reordering], geo_meaningless[reordering], 
        nonmath_true[reordering], nonmath_false[reordering], 
        nonmath_meaningless[reordering], analyse_meaningful[reordering], 
        algebra_meaningful[reordering], topo_meaningful[reordering], 
        geo_meaningful[reordering], nonmath_meaningful[reordering], 
        math_intuitive[reordering], math_nonintuitive[reordering], 
        math_imagery[reordering], math_nonimagery[reordering])
                               
    contrasts = {}
    audio = np.array([name[-4:] == 'reg1' for name in names_], np.float)
    contrasts['audio'] = audio / audio.sum()
    visual = np.array([name[-6:] == 'signal' for name in names_], np.float)
    contrasts['visual'] = visual/ visual.sum()
    motor = np.array([name == 'key press' for name in names_], np.float)
    contrasts['motor'] = motor
    reflection = np.array([name[-4:] == 'reg2' for name in names_],
                          np.float)
    contrasts['reflection'] = reflection / reflection.sum()
    
    
    contrasts['analyse_true - rest'] = np.zeros(len(names_))    
    contrasts['analyse_true - rest'][:n_reg] = analyse_true

    contrasts['analyse_false - rest'] = np.zeros(len(names_))
    contrasts['analyse_false - rest'][:n_reg] = analyse_false

    contrasts['analyse_meaningless - rest'] = np.zeros(len(names_))
    contrasts['analyse_meaningless - rest'][:n_reg] = analyse_meaningless
    
    contrasts['algebra_true - rest'] = np.zeros(len(names_))
    contrasts['algebra_true - rest'][:n_reg] = algebra_true

    contrasts['algebra_false - rest'] = np.zeros(len(names_))
    contrasts['algebra_false - rest'][:n_reg] = algebra_false

    contrasts['algebra_meaningless - rest'] = np.zeros(len(names_))
    contrasts['algebra_meaningless - rest'][:n_reg] = algebra_meaningless

    contrasts['topo_true - rest'] = np.zeros(len(names_))
    contrasts['topo_true - rest'][:n_reg] = topo_true

    contrasts['topo_false - rest'] = np.zeros(len(names_))
    contrasts['topo_false - rest'][:n_reg] = topo_false

    contrasts['topo_meaningless - rest'] = np.zeros(len(names_))
    contrasts['topo_meaningless - rest'][:n_reg] = topo_meaningless

    contrasts['geo_true - rest'] = np.zeros(len(names_))
    contrasts['geo_true - rest'][:n_reg] = geo_true

    contrasts['geo_false - rest'] = np.zeros(len(names_))
    contrasts['geo_false - rest'][:n_reg] = geo_false

    contrasts['geo_meaningless - rest'] = np.zeros(len(names_))
    contrasts['geo_meaningless - rest'][:n_reg] = geo_meaningless

    contrasts['non_math_true - rest'] = np.zeros(len(names_))
    contrasts['non_math_true - rest'][:n_reg] = nonmath_true

    contrasts['non_math_false - rest'] = np.zeros(len(names_))
    contrasts['non_math_false - rest'][:n_reg] = nonmath_false

    contrasts['non_math_meaningless - rest'] = np.zeros(len(names_))
    contrasts['non_math_meaningless - rest'][:n_reg] = nonmath_meaningless
    
    contrasts['math_intuitive'] = np.zeros(len(names_))
    contrasts['math_intuitive'][:n_reg] = math_intuitive
    
    contrasts['math_nonintuitive'] = np.zeros(len(names_))
    contrasts['math_nonintuitive'][:n_reg] = math_nonintuitive
    
    contrasts['math_imagery'] = np.zeros(len(names_))
    contrasts['math_imagery'][:n_reg] = math_imagery
    
    contrasts['math_nonimagery'] = np.zeros(len(names_))
    contrasts['math_nonimagery'][:n_reg] = math_nonimagery
    
    contrasts['math - nonmath'] = np.zeros(len(names_))    
    contrasts['math - nonmath'][:n_reg] = math*language.sum() - math.sum()*language
    
    contrasts['nonmath - math'] = np.zeros(len(names_))
    contrasts['nonmath - math'][:n_reg] = math.sum()*language - language.sum()*math
    
    contrasts['math_meaningful - math_meaningless'] = np.zeros(len(names_))
    contrasts['math_meaningful - math_meaningless'][:n_reg] = math_meaningless.sum()*math_meaningful - math_meaningful.sum()*math_meaningless
    
    contrasts['nonmath_meaningful - nonmath_meaningless'] = np.zeros(len(names_))
    contrasts['nonmath_meaningful - nonmath_meaningless'][:n_reg] = nonmath_meaningless.sum()*nonmath_meaningful - nonmath_meaningful.sum()*nonmath_meaningless
    
    contrasts['analyse_meaningful - othermath'] = np.zeros(len(names_))
    bigsum = algebra_meaningful + topo_meaningful + geo_meaningful
    contrasts['analyse_meaningful - othermath'][:n_reg] = bigsum.sum()*analyse_meaningful - analyse_meaningful.sum()*(algebra_meaningful + topo_meaningful + geo_meaningful)
    
    contrasts['algebra_meaningful - othermath'] = np.zeros(len(names_))
    bigsum = analyse_meaningful + topo_meaningful + geo_meaningful
    contrasts['algebra_meaningful - othermath'][:n_reg] = bigsum.sum()*algebra_meaningful - sum(algebra_meaningful)*(analyse_meaningful + topo_meaningful + geo_meaningful)
    
    contrasts['topo_meaningful - othermath'] = np.zeros(len(names_))
    bigsum = analyse_meaningful + algebra_meaningful + geo_meaningful
    contrasts['topo_meaningful - othermath'][:n_reg] = bigsum.sum()*topo_meaningful - topo_meaningful.sum()*(analyse_meaningful + algebra_meaningful + geo_meaningful)
    
    contrasts['geo_meaningful - othermath'] = np.zeros(len(names_))
    bigsum = analyse_meaningful + algebra_meaningful + topo_meaningful
    contrasts['geo_meaningful - othermath'][:n_reg] = bigsum.sum()*geo_meaningful - geo_meaningful.sum()*(analyse_meaningful + algebra_meaningful + topo_meaningful)
    
    contrasts['true -false'] = np.zeros(len(names_))
    contrasts['true -false'][:n_reg] = vrai*faux.sum() - vrai.sum()*faux
    
    contrasts['mathtrue - mathfalse'] = np.zeros(len(names_))
    contrasts['mathtrue - mathfalse'][:n_reg] = math_false.sum()*math_true - math_true.sum()*math_false
    
    contrasts['nonmathtrue - nonmathfalse'] = np.zeros(len(names_))
    contrasts['nonmathtrue - nonmathfalse'][:n_reg] = nonmath_false.sum()*nonmath_true - nonmath_true.sum()*nonmath_false
    
    
#    i_con = i_con + 1;
#    matlabbatch{i_subj}.spm.stats.con.consess{i_con}.fcon.name = 'F test on 4 categories of math ';
#    matlabbatch{i_subj}.spm.stats.con.consess{i_con}.fcon.convec = { [ 
#        analyse_meaningful - math_meaningful;
#        algebra_meaningful - math_meaningful;
#        topo_meaningful - math_meaningful;
#        geo_meaningful - math_meaningful;
#        ] };
   
#    contrasts['true-false'] = np.zeros(len(names_))
#    contrasts['true-false'][:n_reg] = vrai * faux.sum() - faux * vrai.sum()
    return contrasts


def fixed_effects_img(con_imgs, var_imgs, mask_img):
    """Compute the fixed effets given images of first-level effects and variance
    """
    con, var = [], []
    mask = mask_img.get_data().astype(np.bool)
    for (con_img, var_img) in zip(con_imgs, var_imgs):
        con.append(con_img.get_data()[mask])
        var.append(var_img.get_data()[mask])
    
    arrays = fixed_effects(con, var)
    outputs = []
    for array in arrays:
        vol = mask.astype(np.float)
        vol[mask] = array
        outputs.append(Nifti1Image(vol, mask_img.get_affine()))
    return outputs

def fixed_effects(contrasts, variances):
    """Compute the fixed effets given arrays of first-level effects and variance
    """
    tiny = 1.e-16
    con, var = np.asarray(contrasts), np.asarray(variances)
    var = np.maximum(var, tiny)
    prec = 1./ var
    ffx_con = np.sum(con * prec, 0) * 1./ np.sum(prec, 0)
    ffx_var = 1./ np.sum(prec, 0)
    ffx_stat = ffx_con / np.sqrt(ffx_var)
    arrays = [ffx_con, ffx_var, ffx_stat]
    return arrays

def make_mask(fmri_files):
    """ Generate a mask from a set of fMRI files"""
    # from nipy.labs.mask import compute_mask
    from nilearn.masking import compute_multi_epi_mask
    """
    mean = None
    for fmri_file in fmri_files:
        if mean == None:
            mean = load(fmri_file).get_data().mean(-1)
            affine = load(fmri_file).get_affine()
        else:
            mean += load(fmri_file).get_data().mean(-1)

    mask_img = Nifti1Image(compute_mask(mean, opening=3).astype(np.uint8),
                           affine)
    """
    mask_img = compute_multi_epi_mask(fmri_files)
    return mask_img


def formatted_matrix(ind_mod, understood_level, intuition_level,
                     immediacy_level, visual_imagery_level, mode):
    """ 
    Attempt to translate the formatted_matrix_v2 matlab function
    
    Caveat: may be buggy. Check it

    mode define what part of stimulus is analyzed: (mode = 1 pour ecoute et
    mode = 2 pour reflexion)
    """
    n_sentences = 90
    n_conds = 15
    n_sessions = 6
    n_reg = 39
    n_total = n_reg * n_sessions
	
    cond = np.zeros(n_total)
    positive_intuitive_cond = np.zeros(n_total)
    negative_intuitive_cond = np.zeros(n_total)
    positive_visu_cond = np.zeros(n_total)
    negative_visu_cond = np.zeros(n_total)
    
    # load data corresponding to the boolean condition "boolean"
    understood_level_cond = understood_level[ind_mod]
    a = [x for x in range(len(understood_level_cond)) if understood_level_cond[x] != 0]
    indices_for_boolean_condition_understood = [ind_mod[x] for x in a]
    intuition_level_cond = intuition_level[ind_mod]
    immediacy_level_cond = immediacy_level[ind_mod]
    visual_imagery_level_cond = visual_imagery_level[ind_mod]
    
    # remove not understood sentences
    if understood_level.sum() > 20:
        intuition_understood = intuition_level_cond[understood_level_cond != 0]
        visual_imagery_understood = visual_imagery_level_cond[
            understood_level_cond != 0]
        immediacy_understood = immediacy_level_cond[understood_level_cond != 0]
    
    # also remove all immediate responses from the intuition analysis:
    intuition_understood_non_immediate = intuition_understood[
        immediacy_understood != 1]
    visual_imagery_understood_immediate = visual_imagery_understood[
        immediacy_understood != 1]

    #compute the mean and std of intuition and visual_imagery only on the
    # sentences of interest:
    positive_mean_int = np.mean(intuition_understood_non_immediate )
    negative_mean_int = np.mean(7 - intuition_understood_non_immediate)
    positive_mean_visu = np.mean(visual_imagery_understood_immediate)
    negative_mean_visu = np.mean(7 - visual_imagery_understood_immediate)

    for i_sentence in range(n_sentences):
        if mode == 1:
            i_regressor = 2 * i_sentence + 9 * np.floor(i_sentence / n_conds)
        elif mode == 2:
            i_regressor = 2 * i_sentence + 1 + (
                9 * np.floor(i_sentence / n_conds))
        if i_sentence in indices_for_boolean_condition_understood:
            cond[i_regressor] = 1
            ##if i_sentence in indices_for_boolean_condition_understood[immediacy_understood != 1]:  ## immediacy not removed
            positive_intuitive_cond[i_regressor] =\
                intuition_level[i_sentence] - positive_mean_int
            negative_intuitive_cond[i_regressor] =\
                7 - intuition_level[i_sentence] - negative_mean_int
            positive_visu_cond[i_regressor] =\
                visual_imagery_level[i_sentence] - positive_mean_visu
            negative_visu_cond[i_regressor] = 7 -\
                visual_imagery_level[i_sentence] - negative_mean_visu
    return (cond, positive_intuitive_cond, negative_intuitive_cond, 
            positive_visu_cond, negative_visu_cond)


def define_contrast_audiosentence(final_data):
    
    fd = loadmat(final_data)
    response_questionnaire = fd['response_questionnaire']
    correspondence = fd['correspondance_final']	

    # read 4 variables in reponse_questionnaire
    understood = response_questionnaire[:, 1]
    intuition = 7 - response_questionnaire[:, 4]
    immediacy = response_questionnaire[:, 5]
    visual_imagery = response_questionnaire[:, 6]
	
	# define types
    sentence_type = np.mod(correspondence[:,1], 15) 
    # number in [0;14] for the 15 different types
    	
    n_sentences = 90
    
    understood_level = np.zeros(n_sentences)
    immediacy_level = np.zeros(n_sentences)
    intuition_level = np.zeros(n_sentences)
    visual_imagery_level = np.zeros(n_sentences)
	
    for i_stim in range(15):
        ind = np.where(sentence_type == i_stim)[0]
        if i_stim == 0: 
		indices = [x + 14 for x in [0, 15, 30, 45, 60, 75]]
        else:
		indices = [x + i_stim - 1 for x in [0, 15, 30, 45, 60, 75]]
		
        for x in range(len(indices)):
            understood_level[indices[x]] = understood[ind[x]]
            intuition_level[indices[x]] = intuition[ind[x]]
            immediacy_level[indices[x]] = immediacy[ind[x]]
            visual_imagery_level[indices[x]] = visual_imagery[ind[x]]
	
	mode = 2
	
	#true:
    ind_mod = range(0,90,3)
    (vrai, positive_intuitive_vrai, negative_intuitive_vrai,
    positive_visu_vrai,negative_visu_vrai) = formatted_matrix(
        ind_mod, understood_level, intuition_level, immediacy_level,
        visual_imagery_level, mode)
	
	#false:
    ind_mod = range(1,90,3)
    (faux,positive_intuitive_faux,negative_intuitive_faux,
     positive_visu_faux,negative_visu_faux) = formatted_matrix(
		ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
		
	#meaningless:
    ind_mod = range(2,90,3)
    (meaningless,positive_intuitive_meaningless,negative_intuitive_meaningless,
     positive_visu_meaningless,negative_visu_meaningless) = formatted_matrix(
		ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
    
	#analyse:
    ind_mod = np.reshape([range(0+x,3+x) for x in [0,15,30,45,60,75]],(1,18))[0]
    (analyse,positive_intuitive_analyse,negative_intuitive_analyse,
    positive_visu_analyse,negative_visu_analyse) = formatted_matrix(
         ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
		 
	#algebra:	 
    ind_mod = np.reshape([range(3+x,6+x) for x in [0,15,30,45,60,75]],(1,18))[0]
    (algebra,positive_intuitive_algebra,negative_intuitive_algebra,
     positive_visu_algebra,negative_visu_algebra) = formatted_matrix(
         ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
	
	
    #topo:
    ind_mod = np.reshape([range(6+x,9+x) for x in [0,15,30,45,60,75]],(1,18))[0]
    (topo,positive_intuitive_topo,negative_intuitive_topo,
     positive_visu_topo,negative_visu_topo) = formatted_matrix(
         ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
	
	#geo:
    ind_mod = np.reshape([range(9+x,12+x) for x in [0,15,30,45,60,75]],(1,18))[0]
    (geo,positive_intuitive_geo,negative_intuitive_geo,
     positive_visu_geo,negative_visu_geo) = formatted_matrix(
         ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
		 
	#nonmath:
    ind_mod = np.reshape([range(12+x,15+x) for x in [0,15,30,45,60,75]],(1,18))[0]
    (nonmath,positive_intuitive_nonmath,negative_intuitive_nonmath,
     positive_visu_nonmath,negative_visu_nonmath) = formatted_matrix(
         ind_mod,understood_level,intuition_level,immediacy_level,visual_imagery_level,mode)
		     
    # Combined vectors:
    meaningful = vrai + faux
    math = analyse + algebra + topo + geo
    
    math_true = map(operator.mul, math, vrai)
    math_false = map(operator.mul, math, faux)
    math_meaningful = map(operator.mul, math, meaningful)
    math_meaningless = map(operator.mul, math, meaningless)
	
	# 15 categories elementaires modulated par la comprehension des phrases:
    
    analyse_true = map(operator.mul, analyse, vrai)
    analyse_false = map(operator.mul, analyse, faux)
    analyse_meaningless = map(operator.mul, analyse, meaningless)
    algebra_true = map(operator.mul, algebra, vrai)
    algebra_false = map(operator.mul, algebra, faux)
    algebra_meaningless = map(operator.mul,algebra, meaningless)
    topo_true = map(operator.mul, topo, vrai)
    topo_false = map(operator.mul, topo, faux)
    topo_meaningless = map(operator.mul, topo, meaningless)
    geo_true = map(operator.mul,geo, vrai)
    geo_false = map(operator.mul, geo, faux)
    geo_meaningless = map(operator.mul, geo, meaningless)
    nonmath_true = map(operator.mul, nonmath, vrai)
    nonmath_false = map(operator.mul, nonmath, faux)
    nonmath_meaningless = map(operator.mul, nonmath, meaningless)
    
    analyse_meaningful = map(operator.mul, analyse, meaningful)
    algebra_meaningful = map(operator.mul, algebra, meaningful)
    topo_meaningful = map(operator.mul, topo, meaningful)
    geo_meaningful = map(operator.mul, geo, meaningful)
    nonmath_meaningful = map(operator.mul, nonmath, meaningful)
       
    
    analyse_meaningful = map(operator.mul, analyse, meaningful)
    algebra_meaningful = map(operator.mul, algebra, meaningful)
    topo_meaningful = map(operator.mul, topo, meaningful)
    geo_meaningful = map(operator.mul, geo, meaningful)
    nonmath_meaningful = map(operator.mul, nonmath, meaningful)
       
    # define other subcategories:
    
    math_intuitive = positive_intuitive_analyse + positive_intuitive_algebra + positive_intuitive_topo + positive_intuitive_geo
    math_nonintuitive = negative_intuitive_analyse + negative_intuitive_algebra + negative_intuitive_topo + negative_intuitive_geo
    math_imagery = positive_visu_analyse + positive_visu_algebra + positive_visu_topo + positive_visu_geo
    math_nonimagery = negative_visu_analyse + negative_visu_algebra + negative_visu_topo + negative_visu_geo
    
 
    ratings = [vrai, faux, meaningless, meaningful, math, nonmath, math_true, math_false, math_meaningless, math_meaningful, 
    analyse_true, analyse_false, analyse_meaningless, algebra_true, algebra_false, algebra_meaningless, topo_true,
    topo_false, topo_meaningless, geo_true, geo_false, geo_meaningless, nonmath_true, nonmath_false, nonmath_meaningless,
    analyse_meaningful, algebra_meaningful, topo_meaningful, geo_meaningful, nonmath_meaningful, math_intuitive, 
    math_nonintuitive, math_imagery, math_nonimagery]    
    
    return ratings


def make_ratings(final_data):
    
    (vrai, faux, meaningless, meaningful, math, language, math_true, math_false, math_meaningless, math_meaningful, 
     analyse_true, analyse_false, analyse_meaningless, algebra_true, algebra_false, algebra_meaningless, topo_true, 
     topo_false, topo_meaningless, geo_true, geo_false, geo_meaningless, nonmath_true, nonmath_false, nonmath_meaningless, 
     analyse_meaningful, algebra_meaningful, topo_meaningful, geo_meaningful, nonmath_meaningful, math_intuitive, 
     math_nonintuitive, math_imagery, math_nonimagery) = define_contrast_audiosentence(
            final_data)
            
    ratings = [vrai, faux, meaningless, meaningful, math, language, math_true, math_false, math_meaningless, math_meaningful, 
    analyse_true, analyse_false, analyse_meaningless, algebra_true, algebra_false, algebra_meaningless, topo_true,
    topo_false, topo_meaningless, geo_true, geo_false, geo_meaningless, nonmath_true, nonmath_false, nonmath_meaningless,
    analyse_meaningful, algebra_meaningful, topo_meaningful, geo_meaningful, nonmath_meaningful, math_intuitive, 
    math_nonintuitive, math_imagery, math_nonimagery]
    
    return ratings


def localizer_paradigm():
    """ Set up the paradigm for the parietal task """
    onset = np.array([
            0, 2400, 5700, 8700, 11400, 15000, 18000, 20700, 23700, 26700,
            29700, 33000, 35400, 39000, 41700, 44700, 48000, 50700, 53700, 
            56400, 59700, 62400, 66000, 69000, 71400, 75000, 78000, 80400, 
            83400, 87000, 89700, 93000, 96000, 99000, 102000, 105000, 108000, 
            110400, 113700, 116700, 119400, 122700, 125400, 129000, 131400, 
            135000, 137700, 140400, 143400, 146700, 149400, 153000, 156000, 
            159000, 162000, 164400, 167700, 170400, 173700, 176700, 179700,
            182700, 186000, 188400, 191700, 195000, 198000, 201000, 203700, 
            207000, 210000, 212700, 215700, 218700, 221400, 224700, 227700, 
            230700, 234000, 236700, 240000, 243000, 246000, 248400, 251700, 
            254700, 257400, 260400, 264000, 266700, 269700, 272700, 275400, 
            278400, 281700, 284400, 288000, 291000, 293400, 296700]) * .001
    task = np.array([ 
            8, 8, 11, 1, 3, 10, 5, 10, 4, 6, 10, 2, 7, 9, 9, 7, 7, 11, 11, 9,
            1, 4, 11, 5, 6, 9, 11, 11, 7, 3, 10, 11, 2, 11, 11, 11, 7, 11, 11,
            6, 10, 2, 8, 11, 9, 7, 7, 2, 3, 10, 1, 8, 2, 9, 3, 8, 9, 4, 7, 1,
            11, 11, 11, 1, 7, 9, 8, 8, 2, 2, 2, 6, 6, 1, 8, 1, 5, 3, 8, 10, 11,
            11, 9, 1, 7, 4, 4, 8, 2, 1, 1, 11, 5, 2, 11, 10, 9, 5, 10, 10])
    names = ['damier_H', 'damier_V', 'clicDaudio', 'clicGaudio',
             'clicDvideo', 'clicGvideo', 'calculaudio', 'calculvideo',
             'phrasevideo', 'phraseaudio']
    onset, task = onset[task < 11], task[task < 11]

    duration = 1 * np.ones_like(task)
    con_id = np.array([names[t - 1] for t in task])
    return BlockParadigm(con_id, onset, duration)


def localizer_dmtx(motion_file, n_scans, tr):
    hrf_model = 'canonical'
    drift_model = 'cosine'
    hfcut = 128
    frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)
    paradigm = localizer_paradigm()
    motion_names = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    motion_params = np.loadtxt(motion_file)
    dmtx = make_dmtx(frametimes, paradigm, hrf_model=hrf_model,
                     drift_model=drift_model, hfcut=hfcut, 
                     add_regs=motion_params, add_reg_names=motion_names)
    return dmtx
 

def localizer_contrasts(dmtx):
    contrasts = {}
    n_columns = len(dmtx.names)
    for i in range(10):
        contrasts['%s' % dmtx.names[i]] = np.eye(n_columns)[i]

    # and more complex/ interesting ones
    contrasts['loc_audio'] = contrasts["clicDaudio"] + contrasts["clicGaudio"] +\
        contrasts["calculaudio"] + contrasts["phraseaudio"]
    contrasts["loc_video"] = contrasts["clicDvideo"] + contrasts["clicGvideo"] + \
        contrasts["calculvideo"] + contrasts["phrasevideo"]
    contrasts["left"] = contrasts["clicGaudio"] + contrasts["clicGvideo"]
    contrasts["right"] = contrasts["clicDaudio"] + contrasts["clicDvideo"]
    contrasts["computation"] = contrasts["calculaudio"] + contrasts["calculvideo"]
    contrasts["sentences"] = contrasts["phraseaudio"] + contrasts["phrasevideo"]
    contrasts["H-V"] = contrasts["damier_H"] - contrasts["damier_V"]
    contrasts["V-H"] = contrasts["damier_V"] - contrasts["damier_H"]
    contrasts["left-right"] = contrasts["left"] - contrasts["right"]
    contrasts["right-left"] = contrasts["right"] - contrasts["left"]
    contrasts['motor-cognitive'] = contrasts["left"] + contrasts["right"] -\
    contrasts["computation"] - contrasts["sentences"]
    contrasts["audio-video"] = contrasts["loc_audio"] - contrasts["loc_video"]
    contrasts["video-audio"] = contrasts["loc_video"] - contrasts["loc_audio"]
    contrasts["computation-sentences"] = contrasts["computation"] -  \
        contrasts["sentences"]
    contrasts["reading-visual"] = contrasts["sentences"] * 2 - \
        contrasts["damier_H"] - contrasts["damier_V"]
    return contrasts


def visualcateg_paradigm(onset_file):
    paradigm_data = loadmat(onset_file) 
    onsets = np.concatenate(
        [x for x in paradigm_data['onsets'][0]])
    n_repet = onsets.shape[1]
    durations = np.concatenate(
        [x.repeat(n_repet) for x in paradigm_data['durations'][0]])
    names = np.concatenate(
        [x.repeat(n_repet) for x in paradigm_data['names'][0]]).astype(str)
    onsets = onsets.ravel()
    return BlockParadigm(names, onsets, durations)
    

def visualcategs_dmtx(onset_file, motion_file, n_scans, tr):
    hrf_model = 'canonical'  # hemodynamic reponse function
    drift_model = 'cosine'   # drift model 
    hfcut = 128              # low frequency cut
    motion_names = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'] 
    # motion param identifiers
    frametimes = np.linspace(0, (n_scans - 1) * tr, n_scans)

    paradigm = visualcateg_paradigm(onset_file)
    
    # add motion regressors and low frequencies
    # and create the design matrix
    motion_params = np.loadtxt(motion_file)
    dmtx = make_dmtx(frametimes, paradigm, hrf_model=hrf_model,
                     drift_model=drift_model, hfcut=hfcut,
                     add_regs=motion_params, add_reg_names=motion_names)
    return dmtx

def visualcategs_contrasts(names):
    contrasts = {}
    contrasts['bodies-rest'] = np.array([name=='body' for name in names]).astype(float)   
    contrasts['math-rest'] = np.array([name=='eq' for name in names]).astype(float)
    contrasts['houses-rest'] = np.array([name=='maison' for name in names]).astype(float)
    contrasts['words-rest'] = np.array([name=='mot' for name in names]).astype(float)   
    contrasts['numbers-rest'] = np.array([name=='nb' for name in names]).astype(float)
    contrasts['tools-rest'] = np.array([name=='outils' for name in names]).astype(float)
    contrasts['faces-rest'] = np.array([name=='visage' for name in names]).astype(float)
    contrasts['checkers-rest'] = np.array([name=='CheckerBoard' for name in names]).astype(float)
    
#    al = (np.array([name=='body' for name in names]) + np.array([name=='eq' for name in names]) +\
#        np.array([name=='maison' for name in names]) + np.array([name=='mot' for name in names]) +\
#        np.array([name=='nb' for name in names]) + np.array([name=='outils' for name in names]) +\
#        np.array([name=='visage' for name in names]) + np.array([name=='CheckerBoard' for name in names]))

    al = (contrasts['bodies-rest'] + contrasts['math-rest'] + contrasts['houses-rest'] +\
        contrasts['words-rest'] + contrasts['numbers-rest'] + contrasts['tools-rest'] +\
        contrasts['faces-rest'] + contrasts['checkers-rest']) /8
    
    
    contrasts['symbols-rest'] = np.array(
        [name in ['eq', 'mot', 'nb'] for name in names]).astype(float)   
    contrasts['pictures-rest'] = np.array(
        [name in ['outils', 'maison', 'body', 'visage'] for name in names]).astype(float)   
    contrasts['symbols-pictures'] = contrasts['symbols-rest'] -\
        contrasts['pictures-rest']
    contrasts['pictures-symbols'] = contrasts['pictures-rest'] -\
        contrasts['symbols-rest']
    
    contrasts['bodies-others'] = contrasts['bodies-rest'] - al    
    contrasts['math-others'] = contrasts['math-rest'] - al
    contrasts['houses-others'] = contrasts['houses-rest'] - al
    contrasts['words-others'] = contrasts['words-rest'] - al    
    contrasts['numbers-others'] = contrasts['numbers-rest'] - al
    contrasts['tools-others'] = contrasts['tools-rest'] - al
    contrasts['faces-others'] = contrasts['faces-rest'] - al
    contrasts['checkers-others'] = contrasts['checkers-rest'] - al
    
    contrasts['bodies-checkers'] = contrasts['bodies-rest'] - contrasts['checkers-rest']  
    contrasts['math-checkers'] = contrasts['math-rest'] - contrasts['checkers-rest']  
    contrasts['houses-checkers'] = contrasts['houses-rest'] - contrasts['checkers-rest']  
    contrasts['words-checkers'] = contrasts['words-rest'] - contrasts['checkers-rest']      
    contrasts['numbers-checkers'] = contrasts['numbers-rest'] - contrasts['checkers-rest']  
    contrasts['tools-checkers'] = contrasts['tools-rest'] - contrasts['checkers-rest']  
    contrasts['faces-checkers'] = contrasts['faces-rest'] - contrasts['checkers-rest']  
    
            
        
        
    return contrasts





