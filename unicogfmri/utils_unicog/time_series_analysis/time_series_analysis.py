# -*- coding: utf-8 -*-
"""
SCRIPT DEMO: Event related fMRI
"""


import os

from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt

import nitime
import nitime.timeseries as ts
import nitime.analysis as nta
import nitime.viz as viz

import nibabel

import glob

import nipy 

import numpy as np
from numpy.lib.recfunctions import merge_arrays

path_results = "/neurospin/unicog/protocols/IRMf/Unicogfmri/results6"
contrasts_of_interest = ['left-right']
roi = "/neurospin/unicog/protocols/IRMf/Tests_Isa/git_depot/unicog/unicogfmri/utils_unicog/time_series_analysis/roi.nii"
############################################################################
#Basic using


##glob files and add them to the dictionary
for c in contrasts_of_interest:
    print c
    #describe here your own pattern
    glob_files = glob.glob((path_results + "/va100099/" + '/res_stats/t_maps/*'
                        + c + '.nii.gz'))

print glob_files 


TR = 2.4
len_et = 15  # This is given in number of samples, not time!

"""

Next, we load the data into a recarray from the csv file, using csv2rec

"""


#res = nipy.labs.mask.series_from_mask(glob_files[0], roi)
#print type(res)

fmri = nibabel.load(glob_files[0])
roi = nibabel.load(roi)

data_fmri = fmri.get_data()
data_roi = roi.get_data()

mask = np.where(data_roi, data_fmri, 0)
mask = np.where(mask>0)

print mask

mask_type = np.array(mask, dtype=[('bold', '<f8')])
Z = np.zeros(mask_type.shape,  dtype = [('events', '<f8')])

data =  merge_arrays((E,Z))
#data_path = os.path.join(nitime.__path__[0], 'data')
#data = csv2rec(os.path.join(data_path, 'event_related_fmri.csv'))


t1 = ts.TimeSeries(data.bold, sampling_interval=TR)
t2 = ts.TimeSeries(data.events, sampling_interval=TR)

E = nta.EventRelatedAnalyzer(t1, t2, len_et)

fig01 = viz.plot_tseries(E.eta, ylabel='BOLD (% signal change)', yerror=E.ets)

plt.show