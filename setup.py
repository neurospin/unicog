# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 16:35:41 2014

@author: id983365
"""

from setuptools import setup, find_packages


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
        'pandas',
        'mne',
    ],
    python_requires='~=3.6',
    zip_safe=False
)
