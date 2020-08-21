# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 13:51:55 2018

@author: id983365
"""


import numpy as np
import pandas as pd

from pypreprocess.external.nistats.design_matrix import check_design_matrix


def localizer_paradigm(task_file):
    '''
    Create the paradigm for the localizer task

    Keyword arguments:
    task_file -- file of events in tsv format

    Return
    The paradigm in dataframe format
    '''
   
    # Read the the events file
    df = pd.read_csv(task_file, sep='\t')
    
    # Read the columns of interest
    onsets = df['onset']
    task = df['trial_type']
    duration = df['duration']    
    
    # Grap the value for each column
    np_onset = onsets.values # in seconde
    np_task = task.values
    np_duration = duration.values   
    
    paradigm = pd.DataFrame({'onset': np_onset, 
                             'duration': np_duration, 
                             'trial_type': np_task})

    return paradigm   
        


def localizer_contrasts(design_matrix):
    '''
    Create a dictionary of contrasts

    Keyword arguments:
    task_file -- file of events in tsv format
    design_matrix -- 

    Return
    Dictionary : {name_contrast : array numpy of contrast}
    '''    
      
    contrasts = {}
    _, matrix, names = check_design_matrix(design_matrix)
    contrast_matrix = np.eye(len(names)) 
    for i in range(len(names)):
        if names[i] != 'constant':
            contrasts[names[i]] = contrast_matrix[i]  
        else :
            contrasts['constant'] = contrast_matrix[i] 

#    contrasts["audio"] =\
#        contrasts["r_hand_audio"] + contrasts["l_hand_audio"] +\
#        contrasts["computation_audio"] + contrasts["sentence_audio"]
#    contrasts["video"] =\
#        contrasts["r_hand_video"] + contrasts["l_hand_video"] + \
#        contrasts["computation_video"] + contrasts["sentence_video"]
#    contrasts["left"] = contrasts["l_hand_audio"] + contrasts["l_hand_video"]
#    contrasts["right"] = contrasts["r_hand_audio"] + contrasts["r_hand_video"]
#    contrasts["computation"] =\
#        contrasts["computation_audio"] + contrasts["computation_video"]
#    contrasts["sentences"] = contrasts["sentence_audio"] +\
#        contrasts["sentence_video"]
#    contrasts["H-V"] = contrasts["h_checkerboard"] - contrasts["v_checkerboard"]
#    contrasts["V-H"] = contrasts["v_checkerboard"] - contrasts["h_checkerboard"]
#    contrasts["left-right"] = contrasts["left"] - contrasts["right"]
#    contrasts["right-left"] = contrasts["right"] - contrasts["left"]
#    contrasts['motor-cognitive'] = contrasts["left"] + contrasts["right"] -\
#        contrasts["computation"] - contrasts["sentences"]
#    contrasts["audio-video"] = contrasts["audio"] - contrasts["video"]
#    contrasts["video-audio"] = contrasts["video"] - contrasts["audio"]
#    contrasts["computation-sentences"] = contrasts["computation"] -  \
#                                         contrasts["sentences"]
#    contrasts["reading-visual"] = contrasts["sentence_video"] - \
#                                  contrasts["h_checkerboard"]
#    # contrasts['effects_of_interest'] = np.eye(n_columns)[:10]



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
        
    contrasts["left-right"] = contrasts["left"] - contrasts["right"]
    
    contrasts["right-left"] = contrasts["right"] - contrasts["left"]
    
    contrasts['motor-cognitive'] = contrasts["left"] + contrasts["right"] -\
        contrasts["computation"] - contrasts["sentences"]
        
    contrasts["audio-video"] = contrasts["audio"] - contrasts["video"]
    
    contrasts["video-audio"] = contrasts["video"] - contrasts["audio"]
    
    contrasts["computation-sentences"] = contrasts["computation"] -  \
                                         contrasts["sentences"]
                                         

    # contrasts['effects_of_interest'] = np.eye(n_columns)[:10]


    return contrasts

if __name__ == '__main__':
    para = localizer_paradigm()