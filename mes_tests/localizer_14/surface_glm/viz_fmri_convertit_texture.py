# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:56:30 2014

@author: mamalric
"""

import os
from nibabel.freesurfer import read_geometry, read_morph_data
from nibabel.gifti import read as gifti_read
from mayavi import mlab
import numpy as np
from nipy.labs.viz import cm
import colorsys
from matplotlib import colors


#basedir = ("/neurospin/unicog/protocols/IRMf/"
#           "mathematicians_Amalric_Dehaene2012/"
#           "Surface_analysis/mathematicians/")
contrats_dir = ("/neurospin/unicog/protocols/IRMf/"
            "Tests_Isa/Test_surface_glm/data/"
            "surface_glm")     
basedir  = ("/neurospin/unicog/protocols/"
                "IRMf/Tests_Isa/Test_surface_glm/"
                "data/fs_db")     


subjects = ['subject01']

contrasts = (['audio-video'])


def get_surface_file(subject, side, file_type="inflated"):
#    return os.path.join(basedir, subject, "t1", subject, "surf",
#                        "%s.%s" % (side, file_type))
#    return os.path.join(basedir, "surf",
#                        "%s.%s" % (side, file_type))
    path = ("/neurospin/unicog/protocols/IRMf/Tests_Isa/"
            "Test_surface_glm/data/fs_db/fsaverage/surf/")
    return os.path.join(path,
                        "%s.%s" % (side, file_type))         
            

def get_geometry(subject, side, surface_type="inflated"):
    mesh_file = get_surface_file(subject, side, surface_type)
    vertices, triangles = read_geometry(mesh_file)
    x, y, z = vertices.T

    return x, y, z, triangles


def get_curvature_sign(subject, side):
    curv_file = get_surface_file(subject, side, "curv")
    #print curv_file
    curv = (read_morph_data(curv_file) < 0).astype(int)

    return curv


def get_contrast_file(subject, contrast, side):
    return os.path.join(contrats_dir, subject,
                        "%s_z_map_%s.gii" % (contrast, side))


def get_contrast(subject, contrast, side):
    contrast_file = get_contrast_file(subject, contrast, side)
    gii = gifti_read(contrast_file)
    contrast = gii.darrays[0].data

    return contrast




def show_contrasts(subject, contrasts, side, threshold):
    x, y, z, triangles = get_geometry(subject, side, "inflated")   ## inflated or white
    curv = get_curvature_sign(subject, side)

    f = mlab.figure()
    mlab.clf()

    #mlab.figure(bgcolor=(1, 1, 1))
    
    # anatomical mesh
    mlab.triangular_mesh(x, y, z, triangles, transparent=False,
                         opacity=1., name=subject,
        scalars=curv, colormap="bone", vmin=-1, vmax=2)
        
    title = subject + '_on_template_FSAVERAGE__volumique_video-audio'
    mlab.title(title)
    
    
    #add texture
    text_file = ("/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/"
                 "data/fmri_results/subject01/res_stats/z_maps/"
                 "conversion_gii_fsaverage/subject01video-audio.gii")
#    text_file = ("/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/"
#                 "data/fmri_results/subject01/res_stats/z_maps/"
#                 "conversion_gii_fsaverage/subject01computation.gii")
#    #print curv_file
#    tex = (read_morph_data(text_file) < 0).astype(int)
#    
#    data = get_contrast(subject, contrast, side)
#    func = mlab.pipeline.triangular_mesh_source(x, y, z, triangles, scalars=data)
#    
    tex = np.array([darrays.data for darrays in 
                        gifti_read(text_file).darrays]).ravel()    
    
    mlab.triangular_mesh(x, y, z, triangles, transparent=False,
                         opacity=0.5, name=subject,
        scalars=tex, colormap="hot", vmin=2.7, vmax=7)


    # cmaps = [colormaps[c.split("-")[0]]['colormap'] for c in contrasts]
    # cmaps = cm.cold_hot

    #for contrast, colormap in zip(contrasts, cmaps):
    # functional mesh
#    data = get_contrast(subject, contrast, side)
#    func_mesh = mlab.pipeline.triangular_mesh_source(x, y, z, triangles,
#                                                 scalars=data)
#        # threshold
#    thresh = mlab.pipeline.threshold(func_mesh, low=threshold)
#    surf = mlab.pipeline.surface(thresh, colormap='hot', transparent=True,
#                      opacity=.8, vmin=3., vmax=7) # diminuer pour avoir plus de transparence

                      
#    lut = (np.array([cmaps]) * 255
#                   ).astype(int)
#
#    surf.module_manager.scalar_lut_manager.lut.table = lut

    mlab.draw()

    return f
    
subject = subjects[0]
contrast = contrasts[0]
side = ['lh', 'rh']
side = ['lh']
threshold = 3.

for s in side:
    mfig = show_contrasts(subject, contrast, s, threshold)


