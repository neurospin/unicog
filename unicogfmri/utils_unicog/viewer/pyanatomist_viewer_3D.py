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



def fusion3D_map_activation(
        list_maps,
        template_file="/neurospin/unicog/protocols/IRMf/Tests_Isa/template/avg152T1.nii",
        dic_templates=""):

    """ Function to merge one or many activation maps with a the
    single_subj_T1.nii template of spm8. The defaults values are
    "Rainbow1-fusion" palette set to minVal = 1.
    Please use the interface to change values.

    **Parameters :**
        * dict_maps: dictionnary: {'name_fusion': map_file}

    **Outputs :**
        * launch Anatomist software with all activation map merged with the
        template
    """
    # initialize Anatomist
    a = ana.Anatomist()
    
    #load the mni referential
    mni_ref = a.mniTemplateRef
    liste_ref = a.getReferentials()

    dic_templates_fusion = {}


    #load avg152_T1
#    if len(dic_templates) == 0:
    template = a.loadObject(template_file)
    #template = a.loadObject(file_name, objectName=objectName )
    # load information from header for the template
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
    for file_name in list_maps:
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

#        map_activation.setPalette("Rainbow1-fusion",
#                                  minVal=1,
#                                  absoluteMode=True)

                         
        #list of map_activation for the Fusion2DMethod
        list_map_activation.append(map_activation)                          
                                  

#    #Fusion2DMethod for all maps    
    fusion_map = a.fusionObjects(list_map_activation, 'Fusion2DMethod')
#    #fusion_map.setPalette(mixMethod='linear', linMixFactor=90)
##    print fusion_map.getInfos()
#    
#    #Fusion3DMethod for all maps  + Mesh
#    fusion_mesh = a.fusionObjects([fusion_map, template_mesh], 'Fusion3DMethod') 
    
#    #Put the Fusion3D into a 3D window
#    w_3d = a.createWindow('3D')
#    w_3d.assignReferential(mni_ref)
#    a.addObjects(fusion_mesh, w_3d)
    
    # for each map, create a 3DFusion
    fusion_list = []
    window_list = []
    for map_activation in list_map_activation:  
        fusion_mesh = a.fusionObjects([map_activation, template_mesh], 'Fusion3DMethod')                    
        fusion_list.append(fusion_mesh)
        window_list.append(a.createWindow('3D'))
    
# 
#    for w,f in zip(window_list, fusion_list) :
#        # show the fusion
#        w.assignReferential(mni_ref)
#        a.addObjects(f, w)
        
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
#    win3=a.createWindow('Axial' )
#    a.addObjects(fusion_map, win3)     
    
    # start loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    ######  Parameters to change ###############################################
    
    path_results = "/neurospin/unicog/protocols/IRMf/Unicogfmri/results6"
    dic_maps = {}
    contrasts_of_interest = ['left-right', 'right-left',
                             'audio-video', 'video-audio'][:1]
    ############################################################################
    # Basic using
    
    
    ## glob files and add them to the dictionary
    for c in contrasts_of_interest:
        #describe here your own pattern
#        glob_files = glob.glob((path_results + "/*/" + '/res_stats/t_maps/va*'
#                            + c + '.nii.gz'))

        path_tmp = "/home/id983365/temp"
        path_rois = "/neurospin/unicog/protocols/IRMf/SyntMov_Fabre_Pallier_2014/Group_analyses/full_ancova_nbchar.anova"

        glob_files = glob.glob((path_rois + '/*T_0244.img')) + glob.glob((path_rois + '/*T_0245.img')) + glob.glob((path_rois + '/*T_0119.img'))

#        path_rois = '/neurospin/unicog/protocols/IRMf/SyntMov_Fabre_Pallier_2014/masks_and_ROIs/ROIs_syntmov_def'
#        path_rois = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_nitime/test_data_antonio/ROIs_analyses'                           
#        glob_files = glob.glob((path_rois + '/*.nii'))  
        print glob_files
        print len(glob_files)                        
#        if glob_files:
#            for file_name in glob_files:
#                name_fusion = os.path.basename(file_name)
#                name_fusion = name_fusion.replace(".nii.gz", "")
#                #add in the dic {'name_fusion': file_name}
#                dic_maps[name_fusion] = file_name
    
    # print dic_maps
    # call the function to display maps with the dictionary
    
    list_map_thres = []
    for img in glob_files:
        vol = nibabel.load(img)
        data = vol.get_data()
        data = data > 3.72
        tmp = os.path.basename(img)
#        voxels_size= header.get_zooms()
        vol_thres = nibabel.Nifti1Image(data, vol.get_affine(), vol.get_header() )
        name_file = os.path.split(img)[1]
        tmp_name = 'threshold_3.72_' + os.path.splitext(name_file)[0] + '.nii'
        tmp_name = os.path.join(path_tmp, tmp_name)
        print tmp_name
        nibabel.save(vol_thres, tmp_name)        
        list_map_thres.append(tmp_name)
        
    
    fusion3D_map_activation(list_map_thres)