# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 11:22:59 2014

@author: id983365

Script to share all paradigm an constrasts for IBC protocols

"""
import os

import csv
import numpy as np


from nipy.modalities.fmri.experimental_paradigm import BlockParadigm



def localizer_paradigm(print_option=False):
    """
    Definition:
    Onset for the standart localizer.
    ----------
    Parameters:
    print_option: boolean option, if True jsut print the onsets.
        
    ----------    
    Return
    Either a print of onsets if print_option, otherwise a BlockParadigm object
    """  
    
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
    names = ['h_checkerboard', 'v_checkerboard', 'r_hand_audio', 'l_hand_audio',
             'r_hand_video', 'l_hand_video', 'computation_audio',
             'computation_video', 'sentence_video', 'sentence_audio']
    onset, task = onset[task < 11], task[task < 11]
    duration = 1 * np.ones_like(task)
    con_id = np.array([names[t - 1] for t in task])
    if print_option:
        return (con_id, onset)
    else:
        return BlockParadigm(con_id, onset, duration)    
    
def localizer_contrasts(dmtx):
    """
    Definition:
    Create the dictionary for contrasts
    ----------
    Parameters:
    dmtx: nipy.modalities.fmri.design_matrix
        
    ----------    
    Return
    a dictionary with the name : {name_contrast : array numpy of contrast
    """    
    
    contrasts = {}
    n_columns = len(dmtx.names)
    for i in range(0, n_columns):
        contrasts['%s' % dmtx.names[i]] = np.eye(n_columns)[i] 
        
    # and more complex/ interesting ones
    contrasts["audio"] =\
        contrasts["r_hand_audio"] + contrasts["l_hand_audio"] +\
        contrasts["computation_audio"] + contrasts["sentence_audio"]
    contrasts["video"] =\
        contrasts["r_hand_video"] + contrasts["l_hand_video"] + \
        contrasts["computation_video"] + contrasts["sentence_video"]
    contrasts["left"] = contrasts["l_hand_audio"] + contrasts["l_hand_video"]
    contrasts["right"] = contrasts["r_hand_audio"] + contrasts["r_hand_video"]
    contrasts["computation"] =\
        contrasts["computation_audio"] + contrasts["computation_video"]
    contrasts["sentences"] = contrasts["sentence_audio"] +\
        contrasts["sentence_video"]
    contrasts["H-V"] = contrasts["h_checkerboard"] - contrasts["v_checkerboard"]
    contrasts["V-H"] = contrasts["v_checkerboard"] - contrasts["h_checkerboard"]
    contrasts["left-right"] = contrasts["left"] - contrasts["right"]
    contrasts["right-left"] = contrasts["right"] - contrasts["left"]
    contrasts['motor-cognitive'] = contrasts["left"] + contrasts["right"] -\
        contrasts["computation"] - contrasts["sentences"]
    contrasts["audio-video"] = contrasts["audio"] - contrasts["video"]
    contrasts["video-audio"] = contrasts["video"] - contrasts["audio"]
    contrasts["computation-sentences"] = contrasts["computation"] -  \
                                         contrasts["sentences"]
    contrasts["reading-visual"] = contrasts["sentence_video"] - \
                                  contrasts["h_checkerboard"]
    # contrasts['effects_of_interest'] = np.eye(n_columns)[:10]
    return contrasts

def contrats_dictionary():
    """
    Definition:
    Used for the second level
    ----------    
    Return
    a dictionary with the name : id of constrats
    """
    list_contrats = ['h_checkerboard', 'v_checkerboard', 'r_hand_audio', 
                     'l_hand_audio', 'r_hand_video', 'l_hand_video', 
                     'computation_audio', 'computation_video', 
                     'sentence_video', 'sentence_audio', 'audio',
                     'video', 'left', 'right', 'computation', 'sentences', 
                     'H-V', 'V-H', 'left-right', 'right-left', 
                     'motor-cognitive', 'audio-video', 'video-audio', 
                     'computation-sentences', 'reading-visual']
                     
    dictionary_contrasts  = {i:"name contrast" for i in list_contrats }
    
    return dictionary_contrasts