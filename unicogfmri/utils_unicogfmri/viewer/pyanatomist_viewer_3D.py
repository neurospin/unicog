# -*- coding: utf-8 -*-
"""
Created on Thusday Sep 17 10:23:46 2015

@author: id983365
"""

import sys
import warnings
import os
import subprocess
import glob

import nibabel

try:
    from PyQt4 import QtGui, QtCore
except:
    
    
    warnings.warn('Qt not installed: the mdodule may not work properly, \
                   please investigate')

# Anatomist
try:
    import anatomist.api as ana
    from soma import aims
    #import anatomist.direct.api as ana

    # needed here in oder to be compliant with AIMS
    app = QtGui.QApplication(sys.argv)
except:
    warnings.warn('Anatomist no installed: the mdodule may not work properly, \
                   please investigate')



def fusion3D_map_activation(list_maps, template_file="", path_mesh=""):
    template_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/template/avg152T1.nii"
    path_mesh = "/neurospin/unicog/protocols/IRMf/Tests_Isa/template/mni152_05_brain.mesh"

    # initialize Anatomist
    a = ana.Anatomist()
    
    # load the mni referential
    mni_ref = a.mniTemplateRef
    liste_ref = a.getReferentials()

    dic_templates_fusion = {}

    # load avg152_T1
    template = a.loadObject(template_file)
    template.loadReferentialFromHeader()
    
    # load referentials
    ref_template = template.getReferential()
    tmp_template = 'truth for ' + os.path.basename(template_file)

    #load the mesh and assign the T1 referential
    path_mesh = "/neurospin/unicog/protocols/IRMf/Tests_Isa/template/mni152_05_brain.mesh"
    template_mesh = a.loadObject(path_mesh)
    template_mesh.assignReferential(ref_template)
    dic_templates_fusion["template"] = template_mesh
        

    def create_palette(colors, name_palette):
        palette = a.createPalette(name_palette)
        palette.setColors(colors)
        return  palette

    fusion_list = []   
    window_list = []                         
    list_map_activation = []
    color_list = [[255, 255, 0], [255, 153, 18], [128, 42, 42],
        [0, 255, 0], [61, 145, 64], [50, 205, 50],
        [106, 90, 205], [19, 795, 0], [0, 10, 12], 
        [0, 31, 37], [255, 64, 64], [0, 0, 255], 
        [240, 35, 100], [74, 64, 250], [200, 150, 100] ]
    cpt_color = 0     
    
    #loop on maps to set correctly the referential 
    for file_name in list_maps.itervalues():
        print file_name
        map_activation = a.loadObject(file_name)
        # load identity transformtion to mni_SPM
        tmp_map = 'truth for ' + os.path.basename(file_name)

        # load information from header
        map_activation.loadReferentialFromHeader()
        
        # load referentials
        ref_map_activation = map_activation.getReferential()
        
        liste_ref = a.getReferentials()  
        for ref in liste_ref:
            dict_ref = ref.getInfos()
            if 'name' in dict_ref.keys():
                if dict_ref['name'].find(tmp_map)  != -1:
                    ref_map_activation= ref
        

        a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
                                 ref_map_activation, mni_ref)
        
        #palette and options
        name_palette = "palette_" + str(cpt_color)
        colors = [255,255,255]*1 + color_list[cpt_color]*179
        pal = create_palette(colors, name_palette)
        cpt_color += 1
        map_activation.setPalette(pal)
                         
        #list of map_activation for the Fusion2DMethod
        list_map_activation.append(map_activation)                          
                                  

    # Fusion2DMethod for all maps    
    fusion_map = a.fusionObjects(list_map_activation, 'Fusion2DMethod')
    
    # for each map, create a 3DFusion
    fusion_list = []
    window_list = []
    for map_activation in list_map_activation:  
        fusion_mesh = a.fusionObjects([map_activation, template_mesh], 'Fusion3DMethod')                    
        fusion_list.append(fusion_mesh)

    #now create a multitexture
    fusion_multiTexture = a.fusionObjects(fusion_list, 'FusionMultiTextureMethod')
    fusion_multiTexture_mesh = a.fusionObjects([fusion_multiTexture, template_mesh] , 'FusionTexSurfMethod')
    w3D_multiTexture_mesh = a.createWindow('3D')
    w3D_multiTexture_mesh.assignReferential(mni_ref)
    a.addObjects(fusion_multiTexture_mesh, w3D_multiTexture_mesh)
        
    #Fusion3DMethod for all maps  + T1
    fusion_t1 = a.fusionObjects([fusion_map, template], 'Fusion2DMethod') 
    
    #Put the Fusion3D into a 3D window
    w_ax = a.createWindow('Axial')
    w_ax.assignReferential(mni_ref)
    a.addObjects(fusion_t1, w_ax)
    
    file_name = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_nitime/test_data_antonio/ROIs_analyses/IFGorb_Pallier_2011.nii'
    a = a.loadObject(file_name)

    # start loop
    sys.exit(app.exec_())

