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

#subjects = ['aa130114',
#            'aa130169',
#            'al130244',
#            'bm120103',
#            'ce130459',
#            'cf120444',
#            'fm120345',
#            'hr120357',
#            'jc130030',
#            'jl120341',
#            'jl130200',
#            'kg120369',
#            'ld130145',
#            'lr120300',
#            'mp130263',
#            'mr120371',
#            'rm130241',
#            'mk130199',
#            'of140017']
subjects = ['subject01']


#contrasts = (['faces-others',
#              'math - nonmath'])
contrasts = (['audio-video'])
# colormaps = dict(
#     words=dict(name='orange', H=30),
#     houses=dict(name='jaune', H=60),
#     faces=dict(name='rouge', H=0),
#     math=dict(name='vert', H=120),
#     numbers=dict(name='bleu', H=240),
#     tools=dict(name='violet', H=270),
#     bodies=dict(name='rose', H=300),
#     checkers=dict(name='cyan', H=180)
# )


#def make_colormap(name, color_hue):
#    color = colorsys.hsv_to_rgb(color_hue, 1., 1.)
#    color4 = tuple(list(color) + [1.])
#    cmap = colors.LinearSegmentedColormap.from_list(
#        name, [(0., 0., 0., .9), color4])   # La 4e valeur: alpha
#
#    return cmap
#
#
#for _, description in colormaps.items():
#    description['colormap'] = make_colormap(description['name'],
#                                            description['H'] / 360.)

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

    mlab.title(subject)

    # cmaps = [colormaps[c.split("-")[0]]['colormap'] for c in contrasts]
    # cmaps = cm.cold_hot

    #for contrast, colormap in zip(contrasts, cmaps):
    # functional mesh
    data = get_contrast(subject, contrast, side)
    func_mesh = mlab.pipeline.triangular_mesh_source(x, y, z, triangles,
                                                 scalars=data)
        # threshold
    thresh = mlab.pipeline.threshold(func_mesh, low=threshold)
    surf = mlab.pipeline.surface(thresh, colormap='hot', transparent=True,
                      opacity=.5, vmin=3., vmax=7) # diminuer pour avoir plus de transparence

                      
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
#threshold = 3.

for s in side:
    mfig = show_contrasts(subject, contrast, s, threshold)



#def usage_message():
#    print "Subjects to be chosen from "
#    print "\n".join(subjects)
#
#    print "\nContrasts to be chosen from"
#    print "\n".join(contrasts)
#
#
#if __name__ == "__main__":
#    from argparse import ArgumentParser
#    import sys
#    parser = ArgumentParser()
#    parser.add_argument("subject")
#    parser.add_argument("--contrasts", nargs="+")
#    parser.add_argument("--side", nargs="+")
#    parser.add_argument("--threshold")
#
#    try:
#        args = parser.parse_args()
#    except:
#        usage_message()
#        sys.exit()
#
#    if args.subject is None:
#        usage_message()
#        sys.exit()
#
#
#    if args.contrasts is None:
#        usage_message()
#        sys.exit()
#
#    for contrast in args.contrasts:
#        if contrast not in contrasts:
#            usage_message()
#            sys.exit()
#
#    if args.side is None:
#        side = ['lh', 'rh']
#    else:
#        side = args.side
#
#    if args.threshold is None:
#        threshold = 2.
#    else:
#        threshold = int(args.threshold)
#
#    for s in side:
#        mfig = show_contrasts(args.subject, args.contrasts, s, threshold)

