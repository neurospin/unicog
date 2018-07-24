# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 10:23:46 2014

@author: id983365
"""

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

    # needed here in oder to be compliant with AIMS
    app = QtGui.QApplication(sys.argv)
except:
    warnings.warn('Anatomist no installed: the mdodule may not work properly, \
                   please investigate')


def fusion2D_map_activation(
        dic_maps,
        template_file="/i2bm/local/spm12/canonical/single_subj_T1.nii",
        dic_templates="",
        threshold=3.1,
        maxval=10,
        orientation='Axial',
        cursor=[0, 0, 0, 0],
        block=False):

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

    if len(dic_templates) == 0:
        template = a.loadObject(template_file)
        #template = a.loadObject(file_name, objectName=objectName )
        # load information from header for the template
        template.loadReferentialFromHeader()
        
        # load referentials
        ref_template = template.getReferential()
        tmp_template = 'truth for ' + os.path.basename(template_file)

        liste_ref = a.getReferentials()
        for ref in liste_ref:
            dict_ref = ref.getInfos()
            if 'name' in dict_ref.keys():
        #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
        #                    ref_mni_spm = ref
                if dict_ref['name'].find(tmp_template) != -1:
                    ref_template = ref
    
        a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                                     ref_template, mni_ref)                             
        #dic_templates_fusion[name_contrast] = template 
        dic_templates_fusion["template"] = template





    if len(dic_templates) == len(dic_maps):
        for name_contrast, file_name in dic_templates.items():
            #template
            objectName = "wanatFor_" + name_contrast
            #template = a.loadObject(file_name)
            template = a.loadObject(file_name, objectName=objectName )
            # load information from header for the template
            template.loadReferentialFromHeader()
            
            # load referentials
            ref_template = template.getReferential()
            tmp_template = 'truth for ' + os.path.basename(objectName)
    
            liste_ref = a.getReferentials()
            for ref in liste_ref:
                dict_ref = ref.getInfos()
                if 'name' in dict_ref.keys():
            #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
            #                    ref_mni_spm = ref
                    if dict_ref['name'].find(tmp_template) != -1:
                        ref_template = ref
        
            a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                                         ref_template, mni_ref)                             
            dic_templates_fusion[name_contrast] = template
    else:
        warnings.warn('The number of templates and constrasts are differents.')     


    fusion_list = []   
    window_list = [] 
    
    if block:
        #compute the number of columns which are needed to display in block
        ncol=2
        nrow=1
        nimg=len(dic_maps)
        print "NB IMG", nimg
        def nb_col(ncol, nrow, nimg):
            ncases = ncol*nrow
            while ncases < nimg :
                if (ncol - nrow == 1):
                    ncol = ncol + 1     
                else :
                    nrow = nrow + 1   
                ncases = ncol*nrow
            return ncol, nrow
                
        if nimg == 1:
            new_ncol = 1
        else:
            new_ncol, new_row = nb_col(ncol, nrow, nimg)     
        
        
        block=a.createWindowsBlock(new_ncol, new_row)                       
   
    #loop on maps 
    for fusion_name, file_name in dic_maps.items():
        map_activation = a.loadObject(file_name, fusion_name)
        # load identity transformtion to mni_SPM
        tmp_map = 'truth for ' + os.path.basename(fusion_name)

        # load information from header
        map_activation.loadReferentialFromHeader()
        
        # load referentials
        ref_map_activation = map_activation.getReferential()
        
        liste_ref = a.getReferentials()  
        for ref in liste_ref:
            dict_ref = ref.getInfos()
            if 'name' in dict_ref.keys():
    #                if dict_ref['name'] == 'Talairach-MNI template-SPM':
    #                    ref_mni_spm = ref
    #            if dict_ref['name'].find(tmp_template) != -1:
    #                ref_template = ref
                if dict_ref['name'].find(tmp_map)  != -1:
                    ref_map_activation= ref
        

        a.loadTransformation([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
                                 ref_map_activation, mni_ref)
        
        #palette and options
        map_activation.setPalette("Rainbow1-fusion",
                                  minVal=threshold,
                                  maxVal=maxval,
                                  absoluteMode=True)
        # create the fusion object  
        if dic_templates_fusion.has_key("template"):
            fusion_map = a.fusionObjects([map_activation, 
                                         dic_templates_fusion["template"]],
                                         'Fusion2DMethod')       
        else:
            fusion_map = a.fusionObjects([map_activation, 
                                         dic_templates_fusion[fusion_name]],
                                         'Fusion2DMethod')    
                                     
        fusion_list.append(fusion_map)
        if block:
            window_list.append(a.createWindow(orientation, block=block))
        else:
            window_list.append(a.createWindow(orientation))   
    
    
    #a.linkWindows(window_list, 1)
    #a.AWindowsBlock(nbCols=4,)
    
    for w,f in zip(window_list, fusion_list) :
        # show the fusion
        f.setReferential(mni_ref)
        w.assignReferential(mni_ref)
        w.moveLinkedCursor(cursor)
        a.addObjects(f, w)
        
        
        #changement de position du curseur   
        a.execute('LinkedCursor',
                  object=f,
                  mode="linear_on_defined",
                  rate=0.5)
    
    # start loop
    sys.exit(app.exec_())
