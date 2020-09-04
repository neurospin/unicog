# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 16:35:41 2014

@author: id983365
"""

from setuptools import setup, find_packages


datafiles = {'unicog': ['bids/template_deface/facemask.nii.gz',
                          'bids/template_deface/mean_reg2mean.nii.gz']}


setup(
    name='unicog',
    distname='unicog',
    version='0.1',
    description='Tools for mri processing',
    author='isabelle denghien',
    author_email='isabelle.denghien@cea.fr',
    url='https://github.com/neurospin/unicog',
    packages=find_packages(),
    install_requires=[
        'pydicom',
        'pandas',
        'mne',
        'mne-bids',
        'pydeface',
        'PyYAML',
        'bids-validator',
    ],
    python_requires='~=3.6',
    package_data=datafiles,
    scripts=['bids/neurospin_to_bids.py'],
    zip_safe=False
)
