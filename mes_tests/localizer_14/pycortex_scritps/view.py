# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:03:15 2015

@author: id983365
"""

import cortex
import nibabel
import tempfile
import numpy as np

#subj, xfmname, nverts, volshape = "S1", "fullhead", 304380, (31,100,100)
#subj, xfmname, volshape = "subject01_test_flat", "fsTOmni", (46, 63 ,53)
#subj, xfmname = "subject01_test_flat", "fsTOmni"
#test isa
subj, xfmname = "fsaverage", "fsTOmni"

#test marie
subj, xfmname = "fsaverage", "fsTOspmT"

def test_braindata():
    #vol = np.random.randn(*volshape)
    #image = nibabel.load("/volatile/depot_pycortex/pycortex/filestore/db/subject01_test_flat/subject01audio-video.nii.gz")
    image = nibabel.load("/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012/fMRI_data/cf120444/analyses/audiosentence/spmT_0032.img")
    vol = image.get_data()  
    vol = np.swapaxes(vol, 0, 2)
    tf = tempfile.TemporaryFile(suffix='.png')
    mask = cortex.db.get_mask(subj, xfmname, "thick")

    data = cortex.dataset.Volume(vol, subj, xfmname, cmap='RdBu_r', vmin=2.5, vmax=6)

    #creer un "snaphot" en svg     
#    print type(data)    
#    cortex.add_roi(data)
    
    #view dans un browser
    web = cortex.webgl.show(data)
    
def test_align_automatic():
    cortex.align.automatic('fsaverage', 'fsTOspmT', '/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012/fMRI_data/cf120444/analyses/audiosentence/spmT_0032.img')



if __name__ == "__main__":
    #test_align_automatic()
    test_braindata()