# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:58:11 2015

@author: id983365
"""

import os
import glob
import numpy as np

from scipy.ndimage import label

from nibabel.affines import apply_affine
from nibabel.freesurfer import read_morph_data
from nibabel.freesurfer import read_geometry
from nibabel.gifti import read as read_gifti

from nilearn.image.resampling import coord_transform

from surfer import Brain, utils
os.environ['SUBJECTS_DIR'] = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"



"""
Exemple coming from http://nipy.org/nibabel/reference/nibabel.affines.html
aff = np.array([[0,2,0,10],[3,0,0,11],[0,0,4,12],[0,0,0,1]])
pts = np.array([[1,2,3],[2,3,4],[4,5,6],[6,7,8]])
apply_affine(aff, pts) 
"""

"""
NOTES
1. Yes, just apply the talairach.xfm transform to each vertex. Should be 
easy enough to do in matlab using read_surf.m
"""

#fsaverage to Talairach
aff = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])

#Texture value
path_tex = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/"

path_mesh = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/fsaverage/surf/"
#texture_file = os.path.join(path_tex,'left-right_z_map_lh.gii')
#texture_file = os.path.join(path_tex,'damier_H_z_map_lh.gii')


def cluster_analysis(data):
#    print data.shape
#    print type(data)
#    print data
    cluster_threshold = 10
    z_threshold = 4
    dic_cluster = {}
    vol_t = data < z_threshold
    data[vol_t] = 0 
    labels, n_labels = label(data)
#    print labels
#    print n_labels
#    print data.shape
#    print type(data)
    for k in range(n_labels):
        cluster_size = np.sum(labels == k + 1)
#        print cluster_size
        #selection of label
#        print cluster_size
        if cluster_size >= cluster_threshold:
#            print cluster_size
            #recupere les indexs
#            print labels
#            print k
            filter_data = np.where(labels == k)
#            print filter_data[0]
            #recupere la max
#            print data[filter_data]
            max_z = np.max(data[filter_data])
#            print k
#            print max_z
#            print data[max_z]
#            print n_labels
#            print labels
#            {max_value : coords_cluster}
            dic_cluster[max_z] = filter_data[0]
#            {max_value : coord_max_value}
            idx = np.where(data == max_z) 
#            print idx
#            print idx[0][0]
            dic_cluster[max_z] = idx[0][0]         
    return dic_cluster

def get_coord(path_mesh, dic_cluster):
    print dic_cluster
    coord, b = read_geometry(path_mesh)
    dic_coord = {}
    for max_z, coords in dic_cluster.iteritems():
        print max_z
        print coords
        dic_coord[max_z] = coord[coords]
    print dic_coord
    return dic_coord    
        
    

def get_texture(texture_file):
    text = read_gifti(texture_file)
    texture = text.darrays[0].data
#    print texture
    return texture

def get_geometry(mesh_file):
    text = read_gifti(texture_file)
    texture = text.darrays[0].data
    return texture


def FsaverageToMNI152(coord):
#    aff_fsaverageToMNI152 = array([[9.975314e-01, -7.324822e-03, 1.760415e-02, 9.570923e-01 ],
#                                   [-1.296475e-02, -9.262221e-03, 9.970638e-01, -1.781596e+01],
#                                   [-1.459537e-02, -1.000945e+00, 2.444772e-03, -1.854964e+01 ],
#                                   [   0.,    0.,    0.,    1.]])

    aff_fsaverageToMNI152 = array([[0.998, -0.007, 0.018, 0.957 ],
                                   [-0.013, -0.009, 0.997, -17.816],
                                   [-0.015, -1.001, 0.002, -18.550 ],
                                   [   0.,    0.,    0.,    1.]])


#    aff_fsaverageToMNI152 = array([[1, 0, 0, 10],
#                                   [0, 1, 0, 10],
#                                   [0, 0, 1, 10],
#                                   [ 0, 0, 0,1]])


#    comming from /pypreprocess/cluster_level_analysis.py
#    x, y, z = np.array(np.where(maxima_mask))
#    maxima_coords = np.array(coord_transform(x, y, z, affine)).T
#    x, y, z = coord[0, 0], coord[0, 1], coord[0, 2]
    x, y, z = coord[0], coord[1], coord[2]
    print x, y, z
    mni_152_coord = np.array(coord_transform(x, y, z, aff_fsaverageToMNI152 )).T
    return mni_152_coord

def get_max_coord_value(texture_file, mesh_file):
    print "searching ..."    
    text = read_gifti(texture_file)
    texture = text.darrays[0].data
    #darrays = text.darrays
    #obj = darrays[0]
    #obj.print_summary()
    data_texture = get_texture(texture_file)
    max_value = np.argmax(data_texture)
    a, b = read_geometry(path_mesh)
    texture[max_value]
    return a[max_value]
    

def print_cluster(dic_cluster, file_name, subject, hemi):
    #Set the name to write the cluster information
    ext = os.path.basename(file_name)
    con = os.path.splitext(ext)
    print subject
    print con[0]
    print hemi
    output_file = os.path.join(path_tex, subject, con[0] + '.txt')
    print output_file
    fic = open(output_file, "a")
    for max_value, coord in dic_cluster.iteritems():
      line = str(max_value) + "\t" + str(coord)
      print line
      fic.write(line)
    fic.close()
#Mesh geometry
#a, b = read_geometry(path_mesh)
#x, y, z = a.T
#print x[max_value]
#print y[max_value]
#print z[max_value]


if __name__ == "__main__":
#    ext = os.path.basename(file_name)
#    con = os.path.splitext(ext)
#    output_file = os.path.join(path_tex, subject, con[0], 'txt')
    subject = ['subject01',
                 'subject02',
                 'subject03',
                 'subject04',
                 'subject05',
                 'subject06',
                 'subject07',
                 'subject08',
                 'subject09',
                 'subject10',
                 'subject11',
                 'subject12',
                 'subject13',
                 'subject14'][0:1]

    hemi = ['lh', 'rh'] 
    for s in subject[:]:
        #fetch texture files for one subject
        glob_files = glob.glob(path_tex +'/'+ s + '/*_lh.gii')
        #print glob_files
        if glob_files:
            #print glob_files
            for file_texture in glob_files:
                name_file = os.path.basename(file_texture)
                name_con = name_file.replace("_lh.gii", "")
                print 'NAME', name_con
                for h in hemi :
                    print hemi
                    texture_file = os.path.join(path_tex, s, name_con + '_' + h + '.gii')
                    path_mesh_file = os.path.join(path_mesh, h + '.inflated')
    
    
    
                    #                    texture_file_lh = os.path.join(path_tex,'audio-video_z_map_lh.gii')
                    #                    path_mesh_lh = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/fsaverage/surf/lh.inflated"
                    #                    texture_file_rh = os.path.join(path_tex,'audio-video_z_map_rh.gii')
                    #                    path_mesh_rh = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/fsaverage/surf/rh.inflated"
                    #                    #texture = read_morph_data(texture_file)
                    #    
                    #    lh = get_max_coord_value (texture_file_lh, texture_file_lh)
                    #    rh = get_max_coord_value (texture_file_rh, texture_file_rh)
                    #    
                    #    print "results"
                    #    print "max value for lh {lh}".format(lh=lh)
                    #    print "max value for rh {rh}".format(rh=rh)
    
                    #Prepare the view
                    subject_id = "fsaverage"
                    brain = Brain(subject_id, h, "inflated")
    
                    #cluster analysis
                    data_texture = get_texture(texture_file)
                    dic_cluster = cluster_analysis(data_texture)
                    #print dic_cluster
                    dic_coord = get_coord(path_mesh_file, dic_cluster)
                    print_cluster(dic_coord, texture_file, s, h)
    
                    #conversion to MNI 152
                    #dic_coord_mni152 = {}
                    for max_value, coord in dic_coord.iteritems():
                        #print max_value
                #        print coord
                #        #coord = FsaverageToMNI152(coord)
                #        print "--", coord
                #        print max_value
                        #dic_coord_mni152[max_value] = coord  
                        #brain.add_foci(coord, map_surface="white", color="mediumseagreen")
                        brain.add_foci(coord, scale_factor = 0.5,
                                       map_surface="inflated", 
                                       alpha = 0.5,
                                       color="mediumseagreen")       

                    #and now .... visualization
                    #brain.show_view(dict(elevation=40, distance=430))
                    brain.show_view()
                    path_snapshot = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot"
                    brain.save_image(os.path.join(path_snapshot, 'filter_' + name_con + h + '.png'))
                    brain.close()
                    brain.show_view()