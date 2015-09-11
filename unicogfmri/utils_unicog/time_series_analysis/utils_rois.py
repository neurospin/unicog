# -*- coding: utf-8 -*-

from glob import glob
import os
import os.path as op
from collections import OrderedDict

import pandas as pd
import csv

import numpy as np
import nibabel
from skimage import morphology
from nilearn.input_data import NiftiMapsMasker
from nilearn.masking import intersect_masks

from nilearn.masking import apply_mask
from scipy.stats import scoreatpercentile
from nilearn.plotting import plot_roi

from nitime import timeseries
from nitime import analysis
from nitime import viz



##################
### MAIN FUNCTIONS
##################

def get_rootdir():
    rootdir = os.getenv('ROOTDIR')
    if rootdir is None:
        rootdir = rootdir
    if not rootdir:
        print "no rootdir initialized"
    return rootdir


##################
### FUNCTIONS ON ROIS 
##################
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
    nifti_obj = nibabel.load(data_file)
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


########
# ONSETS
########


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
    return list_onsets


##############
#PLOT DATA PART
##############

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
    events = timeseries.Events(onsets, time_unit = time_unit)
    
    # Timeseries analysis 
    #len_et = numbre of TR what you want to see
    #offset = number of offset including in len_et 
    analyzer = analysis.EventRelatedAnalyzer(ts, events, len_et=len_et, offset=offset)
   
    return analyzer
    

##############
# COORDINATES
##############

def convert_coord_into_volume(list_coord):
    """
    Convert MNI coordinates into a volume
    return a list of volume paths
    """
    #list_vol_path = []
    #not implemented yet
    pass

def voxel_to_mm(vol, voxel_coords):
    """
    Get the coordinates in mm by using the affine
    
    Example 1:
    utils_rois.voxel_to_mm('T1.nii', [0,0,0])
    array([  90., -126.,  -72.])
    
    Example 2:
    utils_rois.voxel_to_mm('T1.nii', [[0,0,0], [0,0,1]]) 
    array([[  90., -126.,  -72.],
           [  90., -126.,  -70.]])

    """
    img = nibabel.load(vol)
    aff = img.get_affine()
    mm_coords = nibabel.affines.apply_affine(aff, voxel_coords)
    return mm_coords

def mm_to_voxel(vol, mm_coords):
    """
    Get the coordinates in voxel by using the inverse of affine
    Example :
    utils_rois.mm_to_voxel("T1.nii", [[90., -126.,  -72.]])
    array([ 0.,  0.,  0.])    
    """
    import numpy.linalg as npl
    img = nibabel.load(vol)
    aff = img.get_affine()
    list_coord = []
    for coord in mm_coords:
        coords_voxel = nibabel.affines.apply_affine(npl.inv(aff), coord)
        list_coord.append(coords_voxel)
    return list_coord

def get_value_in_mm(vol, mm_x, mm_y, mm_z):
    """
    Get the value of one voxel by giving the coord in mm
    Example :
    utils_rois.get_value_in_mm("T1.nii", 90., -126.,  -72.)
    0.013717801310122013
    """
    img = nibabel.load(vol)
    data = img.get_data()
    coords_voxel = mm_to_voxel(vol, [[mm_x, mm_y, mm_z]])
    value = data[coords_voxel[0][0], coords_voxel[0][1], coords_voxel[0][2]]
    return value
    
    
#######################
### CREATE BASIC ROIS

def cube(file_roi, vol, mm_x=0, mm_y=0, mm_z=0, width=3, dtype=np.uint8):
#    img = nibabel.load(vol)
#    v_x, v_y, v_z = mm_to_voxel(vol, [mm_x, mm_y, mm_z]) 
#    data = img.get_data()
#    roi = np.zeros(data.shape)
#    roi[v_x-1:v_x+1,v_y-1:v_y+1, v_z-1:v_z+1 ] = 1
#    roi_img = nibabel.Nifti1Image(roi, img.get_affine(),img.get_header() )
#    nibabel.save(roi_img, file_roi)
    pass
#    #return np.ones((width, width, width), dtype=dtype)


def sphere(file_roi, vol, mm_x=0, mm_y=0, mm_z=0, radius=4, dtype=np.uint8):
    img = nibabel.load(vol)
    header = img.get_header()
    voxels_size= header.get_zooms()
    coord_center_voxel = mm_to_voxel(vol, [[mm_x, mm_y, mm_z]])    
    shape_x, shape_y, shape_z = img.shape[0], img.shape[1], img.shape[2]
    roi = np.zeros((shape_x, shape_y, shape_z))
    
    radius = radius / voxels_size[0]
    if radius > 1 :
       radius -= 1 

    first_x = coord_center_voxel[0][0] - radius
    first_y = coord_center_voxel[0][1] - radius
    first_z = coord_center_voxel[0][2] - radius

    elem = morphology.ball(radius)
    
    #check voxel size is isotropic
    #check radius is at least one voxel
    for x in range(0,elem.shape[0]):
            for y in range(0, elem.shape[1]):
                    for z in range(0, elem.shape[2]):
                        x_ = int(first_x) + x
                        y_ = int(first_y) + y
                        z_ = int(first_z) + z
                        roi[x_, y_, z_] = elem[x,y,z]
  
    roi_img = nibabel.Nifti1Image(roi, img.get_affine(),img.get_header() )
    nibabel.save(roi_img, file_roi)


def voxel(file_roi, vol, mm_x=0, mm_y=0, mm_z=0):
    img = nibabel.load(vol)
    header = img.get_header()
    voxels_size= header.get_zooms()
    data = img.get_data()
    coord_first_voxel = mm_to_voxel(vol, [[mm_x, mm_y, mm_z]])    
    shape_x, shape_y, shape_z = img.shape[0], img.shape[1], img.shape[2]
    roi = np.zeros((shape_x, shape_y, shape_z))
    x_ = coord_first_voxel[0][0]
    y_ = coord_first_voxel[0][1]
    z_ = coord_first_voxel[0][2]
    roi[int(x_) , int(y_), int(z_)] = 1
    roi_img = nibabel.Nifti1Image(roi, img.get_affine(),img.get_header() )
    nibabel.save(roi_img, file_roi)


