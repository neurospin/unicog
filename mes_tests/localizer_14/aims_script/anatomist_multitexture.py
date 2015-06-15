# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:42:35 2015

@author: id983365
"""

# -*- coding: utf-8 -*-
import sys
import warnings
import os
import subprocess
import glob


try:
    from PyQt4 import QtGui, QtCore
except:
    warnings.warn('Qt not installed: the mdodule may not work properly, \
                   please investigate')

# Anatomist
try:
    import anatomist.api as ana
    #import anatomist.direct.api as ana
    #import anatomist.socket.api as ana

    # needed here in oder to be compliant with AIMS
    app = QtGui.QApplication(sys.argv)
except:
    warnings.warn('Anatomist no installed: the mdodule may not work properly, \
                   please investigate')
#def fusion2D_map_activation(
#        dic_maps,
#        template_file="/i2bm/local/spm8/canonical/single_subj_T1.nii",
#        dic_templates=""):
#
#
#    """ Function to merge one or many activation maps with a the
#    single_subj_T1.nii template of spm8. The defaults values are
#    "Rainbow1-fusion" palette set to minVal = 1.
#    Please use the interface to change values.
#
#    **Parameters :**
#        * dict_maps: dictionnary: {'name_fusion': map_file}
#
#    **Outputs :**
#        * launch Anatomist software with all activation map merged with the
#        template
#    """
#    # initialize Anatomist
#    a = ana.Anatomist()
#
#    #load the mni referential
#    mni_ref = a.mniTemplateRef
#    liste_ref = a.getReferentials()
#
#    dic_templates_fusion = {}
#
#    if len(dic_templates) == 0:
#        template = a.loadObject(template_file)
#        #template = a.loadObject(file_name, objectName=objectName )
#        # load information from header for the template
#        template.loadReferentialFromHeader()
#        
#        # load referentials
#        ref_template = template.getReferential()
#        tmp_template = 'truth for ' + os.path.basename(template_file)
#
#        liste_ref = a.getReferentials()
#        for ref in liste_ref:
#            dict_ref = ref.getInfos()
#            if 'name' in dict_ref.keys():
#        #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
#        #                    ref_mni_spm = ref
#                if dict_ref['name'].find(tmp_template) != -1:
#                    ref_template = ref
#    
#        a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
#                                     ref_template, mni_ref)                             
#        #dic_templates_fusion[name_contrast] = template 
#        dic_templates_fusion["template"] = template
#
#
#
#
#
#    if len(dic_templates) == len(dic_maps):
#        for name_contrast, file_name in dic_templates.items():
#            #template
#            objectName = "wanatFor_" + name_contrast
#            #template = a.loadObject(file_name)
#            template = a.loadObject(file_name, objectName=objectName )
#            # load information from header for the template
#            template.loadReferentialFromHeader()
#            
#            # load referentials
#            ref_template = template.getReferential()
#            tmp_template = 'truth for ' + os.path.basename(objectName)
#    
#            liste_ref = a.getReferentials()
#            for ref in liste_ref:
#                dict_ref = ref.getInfos()
#                if 'name' in dict_ref.keys():
#            #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
#            #                    ref_mni_spm = ref
#                    if dict_ref['name'].find(tmp_template) != -1:
#                        ref_template = ref
#        
#            a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
#                                         ref_template, mni_ref)                             
#            dic_templates_fusion[name_contrast] = template
#    else:
#        warnings.warn('The number of templates and constrasts are differents.')     
#
#
#    fusion_list = []   
#    window_list = []                         
#   
#    #loop on maps 
#    for fusion_name, file_name in dic_maps.items():
#        map_activation = a.loadObject(file_name, fusion_name)
#        # load identity transformtion to mni_SPM
#        tmp_map = 'truth for ' + os.path.basename(fusion_name)
#
#        # load information from header
#        map_activation.loadReferentialFromHeader()
#        
#        # load referentials
#        ref_map_activation = map_activation.getReferential()
#        
#        liste_ref = a.getReferentials()  
#        for ref in liste_ref:
#            dict_ref = ref.getInfos()
#            if 'name' in dict_ref.keys():
#    #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
#    #                    ref_mni_spm = ref
#    #            if dict_ref['name'].find(tmp_template) != -1:
#    #                ref_template = ref
#                if dict_ref['name'].find(tmp_map)  != -1:
#                    ref_map_activation= ref
#        
#
#        a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
#                                 ref_map_activation, mni_ref)
#        
#        #palette and options
#        map_activation.setPalette("Rainbow1-fusion",
#                                  minVal=1,
#                                  absoluteMode=True)
#        # create the fusion object  
#        if dic_templates_fusion.has_key("template"):
#            fusion_map = a.fusionObjects([map_activation, 
#                                         dic_templates_fusion["template"]],
#                                         'Fusion2DMethod')       
#        else:
#            fusion_map = a.fusionObjects([map_activation, 
#                                         dic_templates_fusion[fusion_name]],
#                                         'Fusion2DMethod')                              
#                                     
#        fusion_list.append(fusion_map)
#        window_list.append(a.createWindow('Axial'))
#    
#    
#    
#    for w,f in zip(window_list, fusion_list) :
#        # show the fusion
#        w.assignReferential(mni_ref)
#        a.addObjects(f, w)
#        
#        #changement de position du curseur   
#        a.execute('LinkedCursor',
#                  object=f,
#                  mode="linear_on_defined",
#                  rate=0.5,
#                  position=[100, 100, 100, 0])
#    
#    # start loop
#    sys.exit(app.exec_()



def multitexture_fusion(tex_surface_glm_file, tex_curv_file, mesh_flatten_file, mesh_inflated_file):
    # initialize Anatomist
    a = ana.Anatomist()
    
    for side in ['lh']:
        tex_surface_glm = a.loadObject(tex_surface_glm_file.replace('?', side))
        tex_surface_glm.setPalette("tvalues100-100-100")
        #tex_surface_glm.setPalette("zfun-EosB", minVal=3, maxVal=8.6)
        tex_curv = a.loadObject(tex_curv_file.replace('?', side))
        tex_curv.setPalette("B-W LINEAR")
        mesh_flatten= a.loadObject(mesh_flatten_file.replace('?', side))
        mesh_inflated= a.loadObject(mesh_inflated_file.replace('?', side))
        
        fusion_curv = a.fusionObjects([mesh_flatten, tex_curv],
                                      'FusionTexSurfMethod')
        fusion_mulitexture = a.fusionObjects([tex_surface_glm, fusion_curv],
                                      'FusionMultiTextureMethod')
    
        win=a.createWindow('3D')
        #a.addObjects(mesh_inflated, win)
    #    a.addObjects( [ mesh_inflated ], [ win ] )
        a.addObjects( [ fusion_mulitexture ], [ win])
        
        fusion_curv2 = a.fusionObjects([mesh_inflated, tex_curv],
                                      'FusionTexSurfMethod')
        fusion_mulitexture2 = a.fusionObjects([tex_surface_glm, fusion_curv2],
                                      'FusionMultiTextureMethod')
        win2=a.createWindow('3D')
        a.addObjects( [ fusion_mulitexture2 ], [ win2])    
        
    for side in ['rh']:
        tex_surface_glm_bis = a.loadObject(tex_surface_glm_file.replace('?', side))
        #tex_surface_glm_bis.setPalette("tvalues100-100-100")
        tex_surface_glm_bis.setPalette("zfun-EosB", minVal=3, maxVal=8.6)
        tex_curv_bis = a.loadObject(tex_curv_file.replace('?', side))
        tex_curv_bis.setPalette("B-W LINEAR")
        mesh_flatten_bis= a.loadObject(mesh_flatten_file.replace('?', side))
        mesh_inflated_bis= a.loadObject(mesh_inflated_file.replace('?', side))
        
        fusion_curv_bis = a.fusionObjects([mesh_flatten_bis, tex_curv_bis],
                                      'FusionTexSurfMethod')
        fusion_mulitexture_bis = a.fusionObjects([tex_surface_glm_bis, fusion_curv_bis],
                                      'FusionMultiTextureMethod')
    
        win_bis=a.createWindow('3D')
        #a.addObjects(mesh_inflated, win)
    #    a.addObjects( [ mesh_inflated ], [ win ] )
        a.addObjects( [ fusion_mulitexture_bis ], [ win_bis])
        
        fusion_curv2_bis = a.fusionObjects([mesh_inflated_bis, tex_curv_bis],
                                      'FusionTexSurfMethod')
        fusion_mulitexture2_bis = a.fusionObjects([tex_surface_glm_bis, fusion_curv2_bis],
                                      'FusionMultiTextureMethod')
        win2_bis=a.createWindow('3D')
        a.addObjects( [ fusion_mulitexture2_bis ], [ win2_bis])    
    #changement de position du curseur   
#    a.execute('LinkedCursor',
#                  object=f,
#                  mode="linear_on_defined",
#                  rate=0.5,
#                  position=[100, 100, 100, 0])
        
    # start loop
    sys.exit(app.exec_())
    
if __name__ == "__main__" :  
    
    tex_surface_glm = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/subject01/audio-video_z_map_?.gii'
    tex_curv = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/?.curv.gii'
    mesh_flatten = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/flat_?_aims.gii'
    mesh_inflated = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/inflated_?_aims.gii'
   
#    tex_surface_glm = '/neurospin/unicog/protocols/IRMf/mathematicians_Amalric_Dehaene2012/Surface_analysis/mathematicians/cf120444/fmri/results/math - nonmath_z_map_?.gii'
#    tex_curv = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/?.curv.gii'
#    mesh_flatten = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/flat_?_aims.gii'
#    mesh_inflated = '/volatile/depot_pycortex/pycortex/filestore/db/fsaverage/conversion_aims_ref/inflated_?_aims.gii'
  
  
    multitexture_fusion(tex_surface_glm, tex_curv, mesh_flatten, mesh_inflated)

