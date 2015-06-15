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

import matplotlib.pyplot as plt
from nilearn.plotting import plot_epi, plot_stat_map, plot_roi
from nilearn.input_data import NiftiLabelsMasker




path_results = "/neurospin/unicog/protocols/IRMf/Unicogfmri/results6"
contrasts_of_interest = ['left-right']
roi = "/neurospin/unicog/protocols/IRMf/Tests_Isa/git_depot/unicog/unicogfmri/utils_unicog/time_series_analysis/roi_3voxels.nii"
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



fmri = nibabel.load(glob_files[0])
roi = nibabel.load(roi)

data_fmri = fmri.get_data()
data_roi = roi.get_data()

mask = np.where(data_roi, data_fmri, 0)
mask = np.where(mask>0)

#
#mask_vt_filename = haxby_dataset.mask_vt[0]
#vt = nibabel.load(mask_vt_filename).get_data().astype(bool)
values = np.logical_and(data_fmri, data_roi)
values = np.where(values.astype(int)>0)

#plot_roi(nibabel.Nifti1Image(bin_p_values_and_vt.astype(np.int),
#         fmri_img.get_affine()),
#         mean_img, title='Intersection with ventral temporal mask',
#         cut_coords=cut_coords)


#res = nipy.labs.mask.series_from_mask(glob_files[0], roi)
#print type(res)
res = np.where(data_roi>0)
print res.shape()
print "values"
print values
#print mask

#mask_type = np.array(mask, dtype=[('bold', '<f8')])
#Z = np.zeros(mask_type.shape,  dtype = [('events', '<f8')])
#
#data =  merge_arrays((E,Z))
##data_path = os.path.join(nitime.__path__[0], 'data')
##data = csv2rec(os.path.join(data_path, 'event_related_fmri.csv'))
#
#
#t1 = ts.TimeSeries(data.bold, sampling_interval=TR)
#t2 = ts.TimeSeries(data.events, sampling_interval=TR)
#
#E = nta.EventRelatedAnalyzer(t1, t2, len_et)
#
#fig01 = viz.plot_tseries(E.eta, ylabel='BOLD (% signal change)', yerror=E.ets)
#
#plt.show



HISTORY
import nibabel as nb
roi3 = nb.load('roi_3voxels.nii')
roi3.get_shape
roi3.get_shape()
more roi_3voxels.nii.minf
import nilearn
from nilearn import masking
res = masking.intersect_masks([('roi_3voxels.nii', 'fmri.nii.gz')])
res = masking.intersect_masks([('roi_4voxels.nii', 'fmri.nii.gz')])
fmri= nb.load('fmri.nii.gz')
roi = nb.load('roi_4voxels.nii')
roi_aff = roi.get_affine()
fmri_aff = fmri.get_affine()
roi_aff
fmri_aff
pwd
ls
res = masking.intersect_masks([('IFGoper.nii', 'con_0004.img)])
res = masking.intersect_masks([('IFGoper.nii', 'con_0004.img')])
ls
from nilearn import region
res = region.img_to_signals_labels('con_0004.img', 'IFGoper.nii')
ls
res = region.img_to_signals_labels('con_0004.nii', 'IFGoper.nii')
res = region.img_to_signals_labels('IFGoper.nii', 'IFGoper.nii')
res = region.img_to_signals_labels('IFGoper.nii', 'IFGoper.nii')
res = region.img_to_signals_labels('con_0004.nii', 'con_0004.nii')
roi = nb.load('IFGoper.nii')
fmri = nb.load('con_0004.nii')
res = region.img_to_signals_labels(fmri, roi)
type(roi)
type(fmri)
roi_data = roi.get_data()
fmri_data = fmri.get_data()
res = region.img_to_signals_labels(fmri_data, roi_data)
type(fmri)
type(roi)
res = region.img_to_signals_labels(fmri, roi)
res = region.img_to_signals_labels(roi, fmri)
res =img_to_signals_maps(roi, fmri)
res =region.img_to_signals_maps(roi, fmri)
from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
atlas_filename = './IFGoper.nii'
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
masker
time_series = masker.fit_transform('./con_0004.nii')
fmri
fmri.from_filename
fmri.from_filename()
type(fmri)
fmri.get_header
fmri.get_header()
masker
masker.get_params()
masker.fit?
masker.fit_transform?
masker.fit_transform(fmri)
masker.fit_transform('./con_0004.img')
type(fmri)
type(roi)
fmri.get_header
fmri.get_header()
h = fmri.get_header()
h
h.get_data_shape
h.get_data_shape()
h.set_data_shape?
seq = (53, 63, 46, 1)
h.set_data_shape(seq)
h.get_data_shape()
type(fmri)
masker.fit_transform('./con_0004.img')
masker.fit_transform(fmri)
ls
masker.fit_transform('fmri.nii.gz')
ls
masker.fit_transform('mean_func.nii')
res = masker.fit_transform('mean_func.nii')
res
time_series = masker.fit_transform('./con_0004.ni
res = masker.fit_transform('mean_func.ni)
atlas_filename = './roi_4voxels.nii'
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
res = masker.fit_transform('mean_func.ni')
res2 = masker.fit_transform('mean_func.nii')
res
res2
res2.shape
res2 = masker.fit('mean_func.nii')
res2
from nilearn import masking
res3 = masking.apply_mask('./con_0004.img', 'roi_4voxels.nii')
res3 = masking.apply_mask('./mean_func.nii', 'roi_4voxels.nii')
res3
res3 = masking.apply_mask('./mean_func.nii', 'roi_4voxels.nii')
res3 = masking.apply_mask('./mean_func.nii', 'IFGoper.nii')
res3 = masking.apply_mask('./con_0004.nii', 'IFGoper.nii')
res3 = masking.apply_mask('./con_0004.nii', 'IFGoper.ni
res3 = masking.apply_mask('./mean_func.nii', 'IFGoper.nii')
res3 = masking.apply_mask('./mean_func.nii', 'IFGoper.nii')
ll
res3 = masking.apply_mask('./con_0004.img', 'IFGoper.nii')
res3 = masking.apply_mask('IFGoper.nii', './con_0004.nii')
res3 = masking.apply_mask('./con_0004.img', 'IFGoper.nii')
nilearn.__file__
history



from nilearn.input_data import NiftiMasker
>>> from nilearn import datasets
>>> dataset = datasets.fetch_haxby()

mask_filename = haxby_dataset.mask_vt[0]
# For decoding, standardizing is often very important
nifti_masker = NiftiMasker(mask_img=mask_filename, standardize=True)

func_filename = haxby_dataset.func[0]
# We give the nifti_masker a filename and retrieve a 2D array ready
# for machine learning with scikit-learn
fmri_masked = nifti_masker.fit_transform(func_filename)

# Restrict the classification to the face vs cat discrimination
fmri_masked = fmri_masked[condition_mask








In [37]: history
import nilearn as nl
nl.__version__
from nilearn import masking
res3 = masking.apply_mask('./con_0004.img', 'roi_4voxels.nii')
res3 = masking.apply_mask('./con_0004.nii', 'IFGoper.nii')
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
labels_img = './IFGoper.nii'
from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
atlas_filename = './IFGoper.nii'
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
time_series = masker.fit_transform('./con_0004.nii')
from nilearn.input_data import NiftiMasker
mask_filename = haxby_dataset.mask_vt[0]
# For decoding, standardizing is often very important
nifti_masker = NiftiMasker(mask_img=mask_filename, standardize=True)
func_filename = haxby_dataset.func[0]
# We give the nifti_masker a filename and retrieve a 2D array ready
# for machine learning with scikit-learn
fmri_masked = nifti_masker.fit_transform(func_filename)
# Restrict the classification to the face vs cat discrimination
from nilearn import datasets
dataset = datasets.fetch_haxby()
dataset.func
dataset.mask_vt
mask_filename = dataset.mask_vt[0]
nifti_masker = NiftiMasker(mask_img=mask_filename, standardize=True)
func_filename = dataset.func[0]
fmri_masked = nifti_masker.fit_transform(func_filename)
labels = np.recfromcsv(dataset.session_target[0], delimiter=" ")
import numpy as np
labels = np.recfromcsv(dataset.session_target[0], delimiter=" ")
condition_mask = np.logical_or(labels['labels'] == b'face',
                               labels['labels'] == b'cat')
fmri_masked = fmri_masked[condition_mask]
fmri_masked
fmri_masked.shape
history



# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 10:44:44 2015

@author: id983365
"""



from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
print "masker"
print masker

# Here we go from nifti files to the signal time series in a numpy
# array. Note how we give confounds to be regressed out during signal
# extraction
print data.func[0]
time_series = masker.fit_transform(data.func[0], confounds=data.confounds)
print time_series
