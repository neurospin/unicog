# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:14:29 2015

@author: id983365
"""

#import cortex
#import numpy as np
#
##cp ?h.cortex.patch.flat en ?h.cortex.flat.patch.3d dans la base de SUBJECTS_DIR
##importation de ?h.cortex.flat.patch.3d en <config_pycortex>db/fsaverage/surfaces/flat_lh.gii
#cortex.freesurfer.import_flat('fsaverage', 'cortex')
#
#
##view
#cortex.surfs.fsaverage.surfaces.flat.show()



#load a volume:
#cf def test_dataset() dans https://github.com/gallantlab/pycortex/blob/master/cortex/tests/test_dataset.py

#importer un sujet
#lancer freesurfer
#ipython
#cortex.freesurfer.import_subj



import cortex
import tempfile
import numpy as np

from cortex import db, dataset

#subj, xfmname, nverts, volshape = "S1", "fullhead", 304380, (31,100,100)
subj, xfmname, volshape= "subject01_test_flat", "fsTOmni", (46, 63 ,53)


def test_braindata():
    vol = np.random.randn(*volshape)
    tf = tempfile.TemporaryFile(suffix='.png')
    mask = db.get_mask(subj, xfmname, "thick")

    data = dataset.Volume(vol, subj, xfmname, cmap='RdBu_r', vmin=0, vmax=1)
    web = cortex.webgl.show(data)

def test_align_automatic():
    cortex.align.automatic('fsaverage', 'fsTOmni', '/volatile/depot_pycortex/pycortex/filestore/db/subject01_test_flat/subject01audio-video.nii.gz')


if __name__ == "__main__":
    test_braindata()
    #test_align_automatic()