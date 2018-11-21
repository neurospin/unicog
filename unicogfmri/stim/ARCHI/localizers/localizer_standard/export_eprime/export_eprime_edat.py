#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:22:08 2018

@author: id983365
"""

import pandas as pd


#Fixation cross all the time excepted during rsvp and pictseq
#In order to take into account the original localizer in eprime
#Launch the stimulation as follow:
#python audiovis.py ./localizer/export_session1_localizer.csv --rsvp-display-time=250 --rsvp-display-isi=100 --picture-display-time=200 --picture-isi=0

condition_name = []
type_stimulus = []
stim = []

csv_file = './localizer_standard-44-4-export-edat2.txt'
df = pd.read_csv(csv_file, sep = '\t', header = 0, encoding ='utf-16-le')
for i, r_value in enumerate(df.itertuples(), 0):
    manip = r_value[65] #corresponds to the 'manip' column
    if manip == "calculs lus":
        condition_name.append('calculvideo')
        type_stimulus.append('rsvp')
        stim.append('{},{},{},{}'.format(df.mot1[i], df.mot2[i], df.mot3[i], df.mot4[i]))
    elif manip == "calculs entendus":
       condition_name.append('calculaudio')
       type_stimulus.append('sound')
       stim.append(df.son[i])
    elif manip == "clics D entendus":
       condition_name.append('clicDaudio')
       type_stimulus.append('sound')
       stim.append(df.son[i])
    elif manip == "clics G entendus":
       condition_name.append('clicGaudio')
       type_stimulus.append('sound')
       stim.append(df.son[i])
    elif manip == "clics D lus":
       condition_name.append('clicDvideo')
       type_stimulus.append('rsvp')
       stim.append('{},{},{},{}'.format(df.mot1[i], df.mot2[i], df.mot3[i], df.mot4[i]))
    elif manip == "clics G lus":
       condition_name.append('clicGvideo')
       type_stimulus.append('rsvp')
       stim.append('{},{},{},{}'.format(df.mot1[i], df.mot2[i], df.mot3[i], df.mot4[i]))
    elif manip == "damier H":
       condition_name.append('CboardH')
       type_stimulus.append('pictseq')
       stim.append('checherboardhpb.bmp,checherboardhnb.bmp,checherboardhpb.bmp,checherboardhnb.bmp,checherboardhpb.bmp,checherboardhnb.bmp')
    elif manip == "damier V":
       condition_name.append('CboardV')
       type_stimulus.append('pictseq')
       stim.append('checherboardvpb.bmp,checherboardvnb.bmp,checherboardvpb.bmp,checherboardvnb.bmp,checherboardvpb.bmp,checherboardvnb.bmp')
    elif manip == "phrases lues":
       condition_name.append('phraseVideo')
       type_stimulus.append('rsvp')
       stim.append('{},{},{},{}'.format(df.mot1[i], df.mot2[i], df.mot3[i], df.mot4[i]))
    elif manip == "phrases entendues":
       condition_name.append('phraseAudio')
       type_stimulus.append('sound')
       stim.append(df.son[i])
    else:
       print('repos')
       

#EXPORT ONSET
onset_file = './onset_standartloc_events.tsv'
onset_df = pd.read_csv(onset_file, sep = '\t')
onsets = onset_df['onset']*1000
onsets_int=[]
for onset in onsets:
    onsets_int.append(int(onset))

#CREATE THE CSV
stim_data = {'condition_name': condition_name,
        'onset': onsets_int,
        'stype': type_stimulus,
        'stimulus': stim}

df = pd.DataFrame(stim_data)
file_csv = './localizer_standard-44-4-export-edat2.csv'
df.to_csv(file_csv, index=False, sep='\t', header=0)
  