# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:40:11 2015

@author: id983365
"""
import nipype.interfaces.freesurfer as fs
import os
import cortex

os.environ['SUBJECTS_DIR'] = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"

mris = fs.MRIsConvert()
mris.inputs.in_file = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/conversion_fsaverage/tmp/lh.inflated'
mris.inputs.out_datatype = 'vtk'
mris.inputs.subjects_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db'
#mris.inputs.out_file = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/conversion_fsaverage/tmp/lh.inflated.vtk'
mris.run() 

cortex.webshow()

