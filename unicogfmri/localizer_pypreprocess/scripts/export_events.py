# -*- coding: utf-8 -*-

"""
Created on Tue Nov  8 10:53:10 2016

@author: id983365
"""
from __future__ import division

import numpy as np
import pandas as pd

np.set_printoptions(precision=3)

onset = np.array([0, 2400, 5700, 8700, 11400, 15000, 18000, 20700, 23700, 26700,
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
        278400, 281700, 284400, 288000, 291000, 293400, 296700])


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
onset = onset.tolist()
onset = [ o / 1000 for o in onset ]

duration = 1 * np.ones_like(task)
con_id = [names[t - 1] for t in task]

#print(onset)
task = task.tolist()
duration = duration.tolist()

columns = ['onset', 'duration', 'trial_type']

raw_data =  {'onset': onset,
        'duration': duration,
        'trial_type': con_id}    


for i in range(1, 15) :
    if i <10 :
        i = "0"+str(i)
    file_events =  "/volatile/test/pypreprocess/test_localizer_bids/bids_dataset/sub-"+str(i)+"/func/sub-"+str(i)+"_task-localizer_events.tsv"
    print(file_events)
    df = pd.DataFrame(raw_data, columns=columns)
    df.to_csv(file_events, sep="\t", index=False)
