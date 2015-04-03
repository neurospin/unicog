# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 10:28:16 2014

@author: id983365

SCRIPT DEMO: MULTIPLICATION OF IMAGES
"""


import nibabel


#multiplication of images
#load image
img1 = nibabel.load("imageA.nii")
img2 = nibabel.load("imageB.nii")

#load data
tab1 = img1.get_data()
tab2 = img2.get_data()

#operation on data
tab3 = tab1 * tab2

#load affine
aff = img1.get_affine()

#load header to avoid the loss of information
header = img1.get_header()

#save data
new_image = nibabel.Nifti1Image(tab3, aff, header)
nibabel.save(new_image, "new_image")