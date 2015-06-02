#! /usr/bin/env python
# Time-stamp: <2015-03-24 17:13 christophe@pallier.org>


"""
Extracts voxels from masks (ROIs) in a series of maps,
creating one text file per mask
"""
 
import glob
import os
import os.path as op
import nibabel
import numpy as np
from collections import OrderedDict

def get_rootdir():
    rootdir = os.getenv('ROOTDIR')
    if rootdir is None:
        rootdir = '/neurospin/unicog/protocols/IRMf/ConstituantPriming_Pattamadilok_Pallier_2012'
    return rootdir


def get_rois():
    """
    return a dictionary roi_name:path_of_corresponding_mask_file
    """

    rois = ['IFGorb_Pallier_2011', 'IFGtri_Pallier_2011', 'TP_Pallier_2011',
            'aSTS_Pallier_2011', 'pSTS_Pallier_2011', 'TPJ_Pallier_2011', 'IFGoper']
    # rois = rois + [ 'BA_44op', 'PrCentralSulcus', 'lPrecentral Gyrus_BA6_whmov', 'antSTGBrennan']
    # rois = rois + ['AngSupramargGynbArg', 'rPrecuneus_nbArg', 'pSTS_Arg']
    # rois = rois + ['LIFSanterior_Fried', 'LIFSmiddle_Fried', 'LIFSposterior_Fried']

    roi_path = op.join(get_rootdir(), 'Scripts/ROI_classic/ROIs_SyntMov_53x63x46')
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


if __name__ == '__main__':
    maps = get_maps_original()
    rois = get_rois()
    save_data_from_rois(maps, rois, prefix='')
