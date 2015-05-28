# -*- coding: utf-8 -*-
"""
Created on Fri May 22 14:22:47 2015

@author: id983365
"""

from freesurfer.freesurferMeshToAimsMesh import freesurferMeshToAimsMesh as f

f("/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/surfaces/inflated_rh.gii", 
"/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/anatomicals/raw.nii.gz", 
"/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/inflated_rh_aims.gii");

f("/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/surfaces/flat_rh.gii", 
"/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/anatomicals/raw.nii.gz", 
"/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/flat_rh_aims.gii");