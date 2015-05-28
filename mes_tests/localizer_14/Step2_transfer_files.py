# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:56:58 2015

@author: id983365
"""
import os
import shutil


path = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data'
list_dir = os.listdir(path)

for d in list_dir :
    print d
    path_fs = os.path.join(path, 'fs_db', d, 'mri', 'orig')
    if not os.path.exists(path_fs):
        os.makedirs(path_fs)
    src = os.path.join(path, d, 'data', 'anat.nii')
    dest = os.path.join(path_fs, '001.nii')
    print src
    print dest
    shutil.copyfile(src, dest)   

