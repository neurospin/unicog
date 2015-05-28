"""Visualize the mesh using Mayavi

Author: Bertrand Thirion, 2013--2014
"""
import os
import nibabel.freesurfer as nf
import mayavi.mlab as mlab
import numpy as np
from nibabel.gifti import read
from nibabel import load
from nipy.labs import viz3d
from nipy.labs.viz import cm
import commands
from nibabel import freesurfer

# Get the data
#subjects = ['cf120444','jl120341','lr120300','aa130114','aa130169','mk130199',
#            'jl130200','mp130263','rm130241','al130244','bm120103','ce130459',
#            'of140017','jf140025','cr140040','fm120345','hr120357','kg120369',
#            'mr120371','jc130030','ld130145','cf140022','jn140034','mv140024',
#            'tj140029','ap140030','af140169','pp140165','eb140248','gq140243']
            
subjects = ['subject01','subject02','subject03','subject04',
            'subject05','subject06','subject07','subject08',
            'subject09','subject10','subject11','subject12',
            'subject13','subject14']

#work_dir = os.path.join(
#    '/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012',
#    'Surface_analysis/mathematicians')
work_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data'
subject = subjects[0]

os.environ['SUBJECTS_DIR'] = ""

fun_work_dir = '/neurospin/tmp/mathematicians'
fun_work_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data'
#contrasts = ['faces-others', 'audio-video', 'checkers-others',
#             'math - nonmath', 'math-others', 'math-rest']
#contrasts = ['audio-video','video-audio','computation']
contrasts = ['audio-video']
THRESHOLD = 3.

if 0:
    #fs_dir = '/home/bertrand/fs_db/subjects/fsaverage/surf'
    fs_dir = '/i2bm/local/freesurfer/subjects/fsaverage/surf'
else:
    #fs_dir = '/volatile/thirion/fs_db/fsaverage/surf'
    fs_dir = '/i2bm/local/freesurfer/subjects/fsaverage/surf'

# load the meshes

def display(fun_dir, fs_dir, contrast):
    mlab.figure(bgcolor=(1, 1, 1))
    left_mesh = freesurfer.read_geometry(os.path.join(fs_dir, 'lh.inflated'))
    right_mesh = freesurfer.read_geometry(os.path.join(fs_dir, 'rh.inflated'))
    left_curv = os.path.join(fs_dir, 'lh.curv')
    right_curv = os.path.join(fs_dir, 'rh.curv')
    meshes = [left_mesh, right_mesh]
    curves = [left_curv, right_curv]
    for hemisphere, mesh_file, curv_file in zip(['lh', 'rh'], meshes, curves):
        fun_file = os.path.join(fun_dir, '%s_z_map_%s.gii' % (
                contrast, hemisphere))
        fun_file = "/tmp/pysurfer-v2sGuKnHs.mgz"
        coords, triangles = mesh_file
        x, y, z = coords.T

        if hemisphere == 'lh':
            x -= 50
        else:
            x += 50

        curv = freesurfer.read_morph_data(curv_file).astype(np.float)
        curv = (freesurfer.read_morph_data(curv_file) < 0).astype(int)
#        curv = (read_morph_data(curv_file) < 0).astype(int)
        tex = np.array([darrays.data for darrays in 
                        read(fun_file).darrays]).ravel()
        print fun_file, tex.min(), tex.max()
        name = ''
        cmin = -1
        cmax = 1
#        mlab.triangular_mesh(x, y, z, triangles, transparent=True, opacity=1.,
#                             name=name, scalars=curv, colormap="bone",
#                             vmin=cmin, vmax=cmax)
#        mlab.triangular_mesh(x, y, z, triangles, transparent=True, opacity=1.,
#                             name=name, scalars=curv, colormap="bone",
#                             vmin=-1, vmax=2)                    
        mlab.triangular_mesh(x, y, z, triangles, transparent=False,
                         opacity=1., name=subject,
                         scalars=curv, colormap="bone", vmin=-1, vmax=2)
                             
                             
        func_mesh = mlab.pipeline.triangular_mesh_source(
            x, y, z, triangles, scalars=tex)
         #display func   
        thresh = mlab.pipeline.threshold(func_mesh, low=THRESHOLD)
        mlab.pipeline.surface(thresh, colormap="hot", vmin=THRESHOLD, vmax=7)

"""
# plot individual images
for contrast in contrasts:
    display(os.path.join(fun_work_dir, subject, 'fmri/results'),
            fs_dir, contrast)
"""

from scipy.stats import ttest_1samp
from nibabel.gifti import read, write, GiftiDataArray, GiftiImage
write_dir='/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/tmp'

for contrast in contrasts:
    for side in ['lh', 'rh']:
#        stat_img = [os.path.join(fun_work_dir, subject, 'fmri/results',
#                                 '%s_z_map_%s.gii' % (contrast, side))
        stat_img = [os.path.join(fun_work_dir, 'surface_glm', subject,
                                 '%s_z_map_%s.gii' % (contrast, side))
                    for subject in subjects]
        X = np.array([np.asarray(read(simg).darrays[0].data)
                      for simg in stat_img])
        t_vals, _ = ttest_1samp(X, 0)
        stat_texture = GiftiImage(darrays=[
                    GiftiDataArray().from_array(t_vals, intent='z score')])
        stat_path = os.path.join(write_dir, '%s_z_map_%s.gii' %
                                 (contrast, side))
        write(stat_texture, stat_path)

    display(write_dir, fs_dir, contrast)


