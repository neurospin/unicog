# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:08:35 2015

@author: id983365
"""

from nibabel.gifti.giftiio import read
from nibabel import load, save, MGHImage
from nibabel.freesurfer.mghformat import MGHHeader, MGHError
import numpy as np

v2r = np.array([[-1.0, 0.0, 0.0, 81921.0], 
                  [0.0, 0.0, 1.0, -0.5], 
                  [0.0, -1.0, 0.0, 0.5], 
                  [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

#v2r = np.array([[1, 2, 3, -13], [2, 3, 1, -11.5],
#                [3, 1, 2, -11.5], [0, 0, 0, 1]], dtype=np.float32)
#gii = read("/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/subject01/audio-video_z_map_lh.gii")    
gii = read("/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012/Surface_analysis/aa130114/fmri/results/math - nonmath_z_map_lh.gii")          
#gii = read("/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/conversion_fsaverage/lh.curv.gii")

data = gii.darrays
d = data[0]
v = d.data

np.savetxt('/tmp/temporary_ascii_map_math_no_math', v, newline='\n')
#my_file = open('/tmp/temporary_ascii', "w")
#for value in v:
#    my_file.write(value)
#my_file.close()

#freesurfer_texture = MGHImage(v, v2r)
#save(img, '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/tmp/tmp_audio-video_z_map_lh.mgz')