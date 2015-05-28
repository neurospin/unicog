"""Visualize the mesh using Mayavi

Author: Bertrand Thirion, 2013
"""
import os
import nibabel.freesurfer as nf
import mayavi.mlab as mlab
import numpy as np

#subjects = ['aa130114', 'jl120341', 'mp130263', 'aa130169', 'jl130200',
#            'mr120371', 'al130244', 'kg120369', 'nl120167', 'bm120103',
#            'ld130145',  'cb120288', 'ce130459', 'rm130241', 'cf120444', 
#            'll130242', 'el120268', 
#            'lr120300', 'tb120212', 'fm120345', 'vb120303', 'hr120357', 
#            'mh120250', 'vb120409', 'jc130030', 'mk130199']

subjects = ['subject01','subject02','subject03','subject04',
            'subject05','subject06','subject07','subject08',
            'subject09','subject10','subject11','subject12',
            'subject13','subject14']

#work_dir = '/neurospin/tmp/mathematicians'


subject = subjects[0]

#subject_dir = os.path.join(work_dir, subject)
#t1_dir = os.path.join(subject_dir, 't1')
t1_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db'
surf_dir = os.path.join(t1_dir, subject, 'surf')

mlab.figure()
#for hemisphere in ['l', 'r']:
#    mesh_file = os.path.join(surf_dir, '%sh.white' % hemisphere)
#    curv_file = os.path.join(surf_dir, '%sh.curv' % hemisphere)
#    
#    coords, triangles = nf.read_geometry(mesh_file)
#    x, y, z = coords.T
#    curv =  nf.read_morph_data(curv_file).astype(np.float)
#    
#    name = ''
#    if curv is not None:
#        cmin = -1
#        cmax = 1
#        mlab.triangular_mesh(x, y, z, triangles, transparent=False, opacity=1.,
#                             name=name, scalars=curv, colormap="bone",
#                             vmin=cmin, vmax=cmax)
#    else:
#        mlab.triangular_mesh(x, y, z, triangles, transparent=False, opacity=1.,
#                             name=name)
#
#mlab.figure()
#for hemisphere in ['l', 'r']: #problem d'origine
for hemisphere in ['l']:
    mesh_file = "/i2bm/local/freesurfer/subjects/fsaverage/surf/lh.cortex.patch.flat"
    #curv_file = os.path.join(surf_dir, '%sh.curv' % hemisphere)  
#    mesh_file = os.path.join(surf_dir, '%sh.inflated' % hemisphere)
#    curv_file = os.path.join(surf_dir, '%sh.curv' % hemisphere)
    
    coords, triangles = nf.read_geometry(mesh_file)
    x, y, z = coords.T
    curv =  nf.read_morph_data(curv_file).astype(np.float)
    
    name = ''
    if curv is not None:
        cmin = -1
        cmax = 1
        mlab.triangular_mesh(x, y, z, triangles, transparent=False, opacity=1.,
                             name=name, scalars=curv, colormap="bone",
                             vmin=cmin, vmax=cmax)
    else:
        mlab.triangular_mesh(x, y, z, triangles, transparent=False, opacity=1.,
                             name=name)


mlab.show()
