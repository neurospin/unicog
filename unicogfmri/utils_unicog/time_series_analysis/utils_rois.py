#! /usr/bin/env python
# Time-stamp: <2015-07-10 13:50 christophe@pallier.org>

from glob import glob
import os
import os.path as op
from collections import OrderedDict

import pandas as pd
import csv

import numpy as np
import nibabel
from nilearn.input_data import NiftiMapsMasker
from nilearn.masking import intersect_masks

from nilearn.masking import apply_mask
from scipy.stats import scoreatpercentile
from nilearn.plotting import plot_roi

from nitime import timeseries
from nitime import analysis
from nitime import viz



##################
### MAIN FUCNTIONS
##################

def get_rootdir():
    rootdir = os.getenv('ROOTDIR')
    if rootdir is None:
        rootdir = rootdir
    if not rootdir:
        print "no rootdir initialized"
    return rootdir


### Coming from get_data_from_rois #####################################
"""
Extracts voxels from masks (ROIs) in a series of maps,
creating one text file per mask
"""

def get_rois(rois, roi_path):
    """
    return a dictionary roi_name:path_of_corresponding_mask_file
    """

    roi_path = op.join(get_rootdir(), roi_path)
    frois = [op.join(roi_path, '%s.nii' % x) for x in rois]
    assert len(frois) != 0

    return OrderedDict(zip(rois, frois))


def get_maps_original():
    """
    returns an OrderedDict name:path_imgfile
    """
    from collections import OrderedDict

    subjdir = op.join(get_rootdir(), 'Subjects')
    sublist = glob.glob(os.path.join(subjdir, 'sub*'))
    sublist.sort()
    nsub = len(sublist)
    assert (nsub != 0)

    mdir = 'analyses/original/'
    conlist = [op.join(mdir, 'con_%04d.img' % x) for x in range(3, 11)]  

    maps = [op.join(sub, con) for sub in sublist for con in conlist]
    assert len(maps) != 0
    names = ['%s_%s' % (op.basename(sub), op.basename(con))
             for sub in sublist for con in conlist]

    return OrderedDict(zip(names, maps))


def extract_data_in_roi(scans, roi):
    """
    returns the values of voxels in scans that are inside the roi, as a matrix    (rows=voxels, columns=scans). 
    scans : list of 3D img files,
    roi : string, filename of mask file
    note: the current code assumes that mask and the scans have the same shape
    """
    mask = nibabel.load(roi).get_data() > 0
    data = np.zeros([mask.shape[0], mask.shape[1], mask.shape[2], len(scans)])
    for i in range(len(scans)):
        assert os.path.isfile(scans[i])
        img = nibabel.load(scans[i]).get_data()
        assert img.shape == mask.shape
        data[:, :, :, i] = img
    return data[mask, :]


def save_data_from_rois(maps, rois, prefix=''):
    """
    extract data from the scans listed in maps, in each roi
    from the dictionary rois, and save in one text file per roi

    maps: ordereddict names -> files
    roi : ordereddict names -> files
    prefix: prefix to be added in front of filenames
    """
    for nroi, froi in rois.iteritems():
        activations = extract_data_in_roi(maps.values(), froi)
        np.savetxt('%s%s.dat' % (prefix, nroi), activations,
                   delimiter=',',
                   header=",".join(maps.keys()), comments='')
          
          
###############################################################################
"""
Extract data from contrasts maps in the intersections of a priori ROIs
and subject-specific localizer masks.
"""

def binarize_img(img, threshold):
    mask = img.get_data().copy()
    mask[mask < threshold] = 0.
    mask[mask >= threshold] = 1.
    return nibabel.Nifti1Image(mask, img.get_affine())

def get_mask_size(mask_img):
    return np.sum(mask_img.get_data())

def create_bestvoxels_mask(roi_img, localizer_img, toppercentile=25):
    """ select voxels within roi_img having the largest values in localizer_img """
    masked_data = apply_mask(localizer_img, roi_img)
    threshold = scoreatpercentile(masked_data, 100 - toppercentile)
    mask = binarize_img(localizer_img, threshold)
    return intersect_masks((roi_img, mask), threshold=1)


def create_localizer_mask(roi_img, localizer_img, loc_threshold):
    """ select voxels within roi_img that have a value above loc_threshold in localizer_img """
    locmask = binarize_img(localizer_img, loc_threshold)
    return intersect_masks((roi_img, locmask), threshold=1)



###################################
# METHODS TO EXTRACT DATA FROM ROIs
###################################

def get_data_in_roi(path_roi, data_file):
    """Using of the NiftiMapsMasker """
    masker = NiftiMapsMasker([path_roi])
    nifti_obj = nibabel.load(data_file[0])
    data = masker.fit_transform(nifti_obj)
    return data
    

def get_data_in_rois_method1(ROIs, subjects, contrasts, condir):
    """ returns the average contratst in each ROI and for each subject """
    masker = NiftiMapsMasker(ROIs)
    print ROIs
    
    values = np.zeros((len(subjects), len(contrasts), len(ROIs)))
    for isub, sub in enumerate(subjects):
        conlist = [op.join(sub, condir, x) for x in contrasts]
        print conlist
        res = masker.fit_transform(conlist)
        values[isub, :] = masker.fit_transform(conlist)
        #print values
    return values


def get_data_in_rois_method2(ROIs, subjects, contrasts, condir, localizerf, threshold):
    """ returns, for individual subjects, the average contrasts values  in ROIs masked by individual localizers,
    thresholded at a fixed theshold"""
    values = np.zeros((len(subjects), len(contrasts), len(ROIs)))
    for isub, sub in enumerate(subjects):
        conlist = [op.join(sub, condir, x) for x in contrasts]
        localizer_img = nibabel.load(op.join(sub, localizerf))
        locmask = binarize_img(localizer_img, threshold)
        masker = NiftiMapsMasker(ROIs, locmask)
        values[isub, :] = masker.fit_transform(conlist)
    return values


def get_data_in_rois_method3(ROIs, subjects, contrasts, condir, localizerf, toppercentile):
    """ returns, for individual subjects, the average contrasts values  in ROIs masked by individual localizers,
    tresholded to keep a toppertcentil voxels in each ROI. """
    values = np.zeros((len(subjects), len(contrasts), len(ROIs)))
    print ROIs
    for isub, sub in enumerate(subjects):
        conlist = [op.join(sub, condir, x) for x in contrasts]
        localizer_img = nibabel.load(op.join(sub, localizerf))
        for iroi, roi in enumerate(ROIs):
            roi_img = nibabel.load(roi)
            locmask = create_bestvoxels_mask(roi_img, localizer_img, toppercentile)
            values[isub, :, iroi] = np.mean(apply_mask(conlist, locmask), axis=1)
    return values


##############

def ndarray2df(v):
    df = pd.DataFrame(columns=['Subject', 'ROI', 'contrast', 'beta'])

    subj = [op.splitext(op.basename(fn))[0] for fn in subjects]
    con = [op.splitext(op.basename(fn))[0] for fn in contrasts]
    rois = [op.splitext(op.basename(fn))[0] for fn in ROIs]
    n1, n2, n3 = v.shape
    k=0
    for i1 in range(n1):
        for i2 in range(n2):
            for i3 in range(n3):
                df.loc[k] = pd.Series({'Subject': subj[i1],
                                       'contrast': con[i2],
                                       'ROI': rois[i3],
                                       'beta': v[i1, i2, i3]})
                k = k + 1
    return df


##############

def convert_coord_into_volume(list_coord):
    """
    Convert MNI coordinates into a volume
    return a list of volume paths
    """
    list_vol_path = []
    pass
    #return list_vol_path = []


def get_onsets(path_onset, cond):
    """
    Get the onsets from a files ie a csv file
    return a list of onset value for the cond condition
    """
    list_onsets = []
    df = pd.read_csv(path_onset, ";",  header=None)
    subset = df [df[0] == cond ]
    onsest_values = subset[1]
    list_onsets = onsest_values.values.T.tolist()

#            onsets = np.array([121.499000000000,
#                       123.001000000000,
#                       124.502000000000,
#                       126.003000000000,
#                       127.504000000000,
#                       130.490000000000,
#                       283.499000000000,
#                       286.502000000000,
#                       288.003000000000,
#                       289.504000000000,
#                       290.990000000000,
#                       292.490000000000])

    return list_onsets


##############
#PLOT DATA PART

def plot_FRI():
    #not implemented yet
    pass

def analyze_average(data, onsets, 
                 sampling_interval, 
                 len_et = 12,
                 offset = -2, 
                 y_label = "Bold signal",
                 time_unit = 's'):
    
    
    # Times series initialization
    ts = timeseries.TimeSeries(data,
                               sampling_interval=sampling_interval, 
                               time_unit = time_unit)
    
    
    # Events initialization
    print onsets
    events = timeseries.Events(onsets, time_unit = time_unit)
    
    
    # Timeseries analysis 
    #len_et = numbre of TR what you want to see
    #offset = number of offset including in len_et 
    analyzer = analysis.EventRelatedAnalyzer(ts, events, len_et=len_et, offset=offset)
   
    return analyzer
    
    
def save_data_time_analysis(path_file, time, condition, label, values_avg, values_se):  
    """
    Write a csv to save the data of a time_series_analysis     
    
    Example of file:
    #header1 : Name Subject - Name Condition - Name of ROI - Methode (Avg/FIR) 
    Avg_value Se_Value Timepoint 
    """
    
#    with open(path_file, 'wb') as outcsv:
        #writer = csv.DictWriter(outcsv, delimiter='\t', fieldnames = [header])   
#        writer = csv.DictWriter(outcsv, delimiter='\t', \
#                                fieldnames = \
#                                ['Condition', 'Label', "Avg_value", "Se_value", "Time_point"])
#        writer.writeheader()

    with open(path_file, 'w') as csv_file:
        #reader = csv.reader(incsv)
        writer = csv.writer(csv_file, delimiter='\t', \
                                fieldnames = \
                                ['Condition', 'Label', "Avg_value", "Se_value", "Time_point"])

        #writer = csv.writer(csv_file)
        writer.writeheader()
        for i, val in enumerate(time):
            print i
            print time
            writer.writerows(
                {'Condition': condition,
                'Label': label,
                'Avg_value': values_avg[i], 
                'Se_value' : values_se[i], 
                'Time_point': time[i] })
            print condition
            print label
            print values_avg[i]
            print values_se[i]
            print time[i]
#            writer.writerows((
#                condition,
#                label,
#                values_avg[i], 
#                values_se[i], 
#                time[i]))


#    with open(path, "wb") as csv_file:
#        writer = csv.writer(csv_file, delimiter=',')
#        for line in data:
#            writer.writerow(line)

##############

#if __name__ == '__main__':
# 
##    rootdir = os.getenv('ROOTDIR')
##    if rootdir is None:
##        rootdir = '/neurospin/unicog/protocols/IRMf/SyntMov_Fabre_Pallier_2014/scripts/testdata/'
#
#    rootdir = '/volatile/test_time_analysis/testdata_ter'
#
#    # Subjects' paths
#    subjdir = op.join(rootdir, 'subjects')
#    subjects = sorted(glob(op.join(subjdir, 'subj*')))
#
#    # Contrast maps for each subject
#    condir = 'analyse_smooth5/full_ancova_nbchar/'
#    contrasts = ['scon_%04d.img' % x for x in (10, 11, 12, 13)]
#
#    # location of individual localizer T map
#    localizerf = 'analyse_smooth5/localizer_3/spmT_0001.img'
#    THR_loc = 3.1  # statistical threshold for localizer's T-map
#
#    # regions of interest (binary maps)
#    roidir = op.join(rootdir, 'ROIs')
#    ROIs = sorted(glob(op.join(roidir, '*.nii')))
#
#
#    # extract data and save in csv files
#    v1 = get_data_in_rois_method1(ROIs, subjects, contrasts, condir)
#    df1 = ndarray2df(v1)
#    df1.to_csv('/volatile/test_time_analysis/results/method1.csv')
#
##    v2 = get_data_in_rois_method2(ROIs, subjects, contrasts, condir, localizerf, THR_loc)
##    df2 = ndarray2df(v2)
##    df2.to_csv('method2.csv')
##
##    v3 = get_data_in_rois_method3(ROIs, subjects, contrasts, condir, localizerf, 10)
##    df3 = ndarray2df(v3)
##    df3.to_csv('method3.csv')
#
#    print 'you can now execture plot.R in R'
