#!/usr/bin/env python
"""Will fetch all dicoms from the data server and convert them to nifti files.

Authors: Isabelle Courcol, 2014
"""
import os
import glob
import shutil
import commands
import pandas as pd
import numpy as np

#GLOBALS VARIABLES
#path for scanner
DATA_PATH = '/neurospin/acquisition/database/'


def init_xls(file_name, scanner):
    acquisitions = {}
    params = {}
#    workbook = xlrd.open_workbook(file_name)
#    all_worksheets = workbook.sheets()
    

#    #normally only the 1st sheet is used
#    worksheet = all_worksheets[0]
#    if worksheet.nrows != 0:
#      for rownum in xrange(worksheet.nrows):
#        if rownum != 0:
#          #0: nip, 1: date, 2: id, 3: file_name, 4: importatio_to_do
##          run[worksheet.cell_value(rownum,3)] = dict(
##                        id = worksheet.cell_value(rownum,2).replace("'",""))
#          if worksheet.cell_value(rownum, 5) == 'y':
#            params = dict(
#                    subject_id=worksheet.cell_value(rownum,0),
#                    date=str(int(worksheet.cell_value(rownum,2))),
#                    scanner='3T',
#  #                  runs={worksheet.cell_value(rownum,2).replace("'",""):
#  #                       worksheet.cell_value(rownum,3)
#                    runs={worksheet.cell_value(rownum,4) :
#                        {'id':worksheet.cell_value(rownum,3).replace("'","")}}
#                    )
#            if worksheet.cell_value(rownum, 1) != "" :
#                 params['new_name'] = worksheet.cell_value(rownum, 1)
#            acquisitions[rownum] = params



    workbook = pd.ExcelFile(file_name)
    all_worksheets = workbook.sheet_names

    #normally only the 1st sheet is used
    worksheet = workbook.parse(all_worksheets[0])
    i = 0    
    if len(worksheet.columns) != 0:
      for rownum in worksheet.values:
          print "i ", i
          #0: nip, 1: date, 2: id, 3: file_name, 4: importatio_to_do
#          run[worksheet.cell_value(rownum,3)] = dict(
#                        id = worksheet.cell_value(rownum,2).replace("'",""))
          if rownum[5] == 'y':
            print rownum
            params = dict(
                    subject_id=rownum[0],
                    date=str(int(rownum[2])),
                    scanner='3T',
  #                  runs={worksheet.cell_value(rownum,2).replace("'",""):
  #                       worksheet.cell_value(rownum,3)
                    runs={rownum[4] :
                        {'id':rownum[3].replace("'","")}}
                    )
            if rownum[1] != "NaN" :
                 params['new_name'] = rownum[1]
            acquisitions[i] = params
            i = i + 1


    return acquisitions 
  
  
def init_txt(file_name, scanner):
    """ IMPORTATION FROM SCANNER

    Specific to neurospin center. Copy dicom data and convert to nifti format.
    Select data to import in a text file as follow:
    dirname date nip num1 name1 [num2 name2 [num3 name3 ...]
    where numXX specify the series\' number, using 2 digits
    ignore lines starting with \'#\'
    Download the dicom files from the server, convert them into nii
    and move them in the ANAT_DIR and FMRI_DIR subdirectories.

    Parameters
    ----------
    information_file : str (mandatory)
        file with date information to import, for instance:
         nip 20111122 nip 02 anat 04 localizer
         nip 20120214 nip 02 anat 33 localizer
    device : str (default TrioTim)
        scanner name
    outdir : str (default None: same loacation than informaiton file)
        the output directory.
    anat_dir : str (default t1mri/acquisition)
        name of directory containing anatomical sequence.
    fmri_dir : str (default fMRI/acquisition)
        name of directory containing fMRI sequence.
    check : bool (default False)
        manual check of the input parameters.
    verbose : bool (default True)
        print to stdout the function prototype.

    Returns
    -------
    None

    <proto>
        <item name=information_file" type="Path" />
        <item name=device" type="String" />
        <item name="outdir" type="Directory" />
        <item name="anat_dir" type="String" />
        <item name="fmri_dir" type="String" />
        <item name="upper_bound" type="Float" />
        <item name="check" type="Bool" />
        <item name="verbose" type="Bool" />
    </proto>
    """

    #additional variables
    #nip, acq, date, sample, i: start to scan which exam (05) must be
    #imported and its name (anat), e.g. 05 anat
   #nip, acq, date, sample, i = '', '1', '', '', 3

    acquisitions = {}
    params = {}

    #grap information to import data form a txt file
    data_to_import = np.genfromtxt(str(file_name), dtype=str,
                                   invalid_raise=False, comments='#')
                                   
    #reshape in 2D array
    if data_to_import.ndim == 1:
        data_to_import = data_to_import.reshape(1, -1)
    j = 0                                      
    for d in data_to_import:
        i = 3  
    #name of directory, data of acquisition, nip of subject
        while i < len(d):   
            params = dict(
                    new_name=d[0],
                    subject_id=d[2],
                    date=d[1],
                    scanner='3T',
                    runs={d[i+1] :
                        {'id' : d[i]}})
            # add into the dictionnary for all importation            
            acquisitions[j] = params
            j += 1
            i += 2
    
    return acquisitions
                                   

def get_path(scanner, date, subject_id, run_id):
    if scanner == "3T":
        scanner_name = "TrioTim"
    elif scanner == "7T":
        scanner_name = "Investigational_Device_7T"
    #path = os.path.join(DATA_PATH, scanner_name, date, "%s*" % subject_id, run_id)
    list_path = glob.glob(os.path.join(
        DATA_PATH, scanner_name, date, "%s*" % subject_id, "*%s*" % run_id))
    if list_path:
      return list_path[0]
    else:
      print " ! WARNING: this path doesn't exist {0}".format(
       os.path.join(DATA_PATH, scanner_name, date, "%s*" % subject_id, run_id))


def fetch_acquisition(acquisition_dict, target_folder):
    date = acquisition_dict['date']
    subject_id = acquisition_dict['subject_id']
    scanner = acquisition_dict['scanner']
    run_ids = acquisition_dict['runs']

    for key, value in run_ids.items():
        path = get_path(scanner, date, subject_id, value['id'])
        if path:        
          folder = os.path.join(target_folder, key)
          if os.path.exists(folder):
              continue
          shutil.copytree(path, folder)
        else:
          return False   

def fetch_acquisitions(acquisitions, fmri_dir, restrict_to=None):

    if restrict_to is None:
        restrict_to = acquisitions.keys()

    for session, acquisition in acquisitions.items():
        if session not in restrict_to:
            continue
        if acquisition.has_key('new_name'):
          subject_id = acquisition['new_name']
        else:
          subject_id = acquisition['subject_id']
        #dicom_dir = os.path.join(fmri_dir, subject_id, session, "dicoms")
        dicom_dir = os.path.join(fmri_dir, subject_id, "dicoms")
        dicom_dir = os.path.join(fmri_dir, subject_id)
        if not os.path.exists(dicom_dir):
            os.makedirs(dicom_dir)
        res = fetch_acquisition(acquisition, dicom_dir)
        if res == False:
          del acquisitions[session]
    return acquisitions


def convert_dicoms(first_dicom, target_folder):
    output = commands.getoutput(
        'dcm2nii -g N -r N -c N -f N -i Y -d N -p N -e N -o %s %s' % (
            target_folder, first_dicom))
    nifti_file = output.split(' ')[-1]
    return nifti_file

def remove_dicoms(dicom_dir):
    shutil.rmtree(dicom_dir)

def convert_all_dicoms(config, fmri_dir, sessions=None):

    if sessions is None:
        sessions = config.keys()

    nifti_files = dict()
    for session in sessions:
        nifti_files[session] = dict()
        
        if config[session].has_key('new_name'):
          subject_id = config[session]['new_name']
        else:
          subject_id = config[session]['subject_id']       
        
        
        session_dir = os.path.join(fmri_dir, subject_id)
        #dicom_dir = os.path.join(session_dir, "dicoms")
        dicom_dir = os.path.join(session_dir)
        print dicom_dir
        if os.path.isdir(dicom_dir):
          for run_name, run_info in config[session]['runs'].items():
              run_dir = os.path.join(dicom_dir, run_name)
              print run_dir
              first_dicom = sorted(glob.glob(os.path.join(run_dir, "*.dcm")))[0]
              nifti_file = convert_dicoms(first_dicom, session_dir)
              fmri_path = os.path.join(session_dir, "data")
              if not os.path.exists(fmri_path):
                  os.makedirs(fmri_path)
              new_name = os.path.join(fmri_path, "%s.nii" % run_name)
              #if os.path.isfile(new_name):
              #    continue
              shutil.move(nifti_file, new_name)
              # create a symbolic link toward a file called dc*
              # to have the next scripts running
              path = os.path.join(fmri_path, "dc%s.nii.gz" % run_name)
              if run_name[0] == 's' and run_name[2] == 'r':
                  output = commands.getoutput('gzip %s' % new_name)
                  link_name = os.path.join(fmri_path, "dc%s.nii.gz" % \
                                          run_name)
                  if not os.path.islink(link_name):
                      os.symlink(new_name + '.gz', link_name)
              nifti_files[session][run_name] = new_name
              print " -- Results of conversion: {0}".format(new_name)
              remove_dicoms(run_dir)


