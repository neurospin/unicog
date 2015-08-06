#! /usr/bin/env python
# Time-stamp: <2015-08-06 14:02:01 cp983411>

import os
import sys

from unicogfmri.utils_unicog.import_data import import_and_convert_dicom

datadir = os.path.join(os.getenv('ROOTDIR'), 'raw_data')
if not os.path.exists(datadir):
    os.makedirs(datadir)

if len(sys.argv) < 2:
  print """"Usage: %s scan_listing

  where scan_listing is a text file describing the scans to be imported, 
  following the convention described at ...

"""
  exit(1)


print "Reading scans list " + sys.argv[1] 
acquisitions = import_and_convert_dicom.init_txt(sys.argv[1], '3T')

print "fetching scans"
acquisitions = import_and_convert_dicom.fetch_acquisitions(acquisitions, datadir)

print "Converting dicoms to nifti"
import_and_convert_dicom.convert_all_dicoms(acquisitions, datadir)
