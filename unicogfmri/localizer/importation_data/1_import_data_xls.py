import os

from unicogfmri.utils_unicog.import_data import import_and_convert_dicom

######  Parameters to change ###############################################
#path where you want to put data
main_dir = '/volatile/test_localizer1/data3'
#information for subjects
data = '/neurospin/unicog/resources/git_depot/UnicogFmri/unicogfmri/localizer/importation_data/acquisitions_summary_localizer.xls'
scanner='3T'
###########################################################################

if not os.path.exists(main_dir):
  os.makedirs(main_dir)

# fetch information for subjects
acquisitions = ""
if os.path.isfile(data):
    acquisitions = import_and_convert_dicom.init_xls(data, scanner)
    print acquisitions
  
#importation and conversion    
if acquisitions:   
  acquisitions = import_and_convert_dicom.fetch_acquisitions(acquisitions, main_dir)
  import_and_convert_dicom.convert_all_dicoms(acquisitions, main_dir)
else:
    print "Nothing to do "
