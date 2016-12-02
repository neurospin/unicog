"""Utilities to handle the BIDS standard."""
import os
import pandas as pd
import glob as glob
import json
import shutil
import subprocess
import dicom
from itertools import combinations
import time
import argparse
import re


def file_manager_default_file(main_path, filter_list, file_tag,
                              file_type='*', allow_other_fields=True):
    """Path to the most specific file with respect to optional filters.

    Each filter is a list [key, value]. Like [sub, 01] or [ses, 02].

    Following BIDS standard files can be of the form
    [key-value_]...[key-value_]file_tag.file_type.
    """
    filters = []
    for n in list(reversed(range(1, len(filter_list) + 1))):
        filters += combinations(filter_list, n)
    filters += [[]]
    for filt in filters:
        found = get_bids_files(main_path,
                               sub_folder=False, file_type=file_type,
                               file_tag=file_tag, filters=filt,
                               allow_other_fields=allow_other_fields)
        if found:
            return found[0]
    return None


def file_reference(img_path):
    reference = {}
    reference['file_path'] = img_path
    reference['file_basename'] = os.path.basename(img_path)
    parts = reference['file_basename'].split('_')
    tag, typ = parts[-1].split('.', 1)
    reference['file_tag'] = tag
    reference['file_type'] = typ
    reference['file_fields'] = ''
    reference['fields_ordered'] = []
    for part in parts[:-1]:
        reference['file_fields'] += part + '_'
        field, value = part.split('-')
        reference['fields_ordered'].append(field)
        reference[field] = value
    return reference


def get_bids_files(main_path, file_tag='*', file_type='*', sub_id='*',
                   file_folder='*', filters=[], ref=False, sub_folder=True,
                   allow_other_fields=True):
    """Return files following bids spec

    Filters are of the form (key, value). Only one filter per key allowed.
    A file for which a filter do not apply will be discarded.
    """
    if sub_folder:
        files = os.path.join(main_path, 'sub-*', 'ses-*')
        if glob.glob(files):
            files = os.path.join(main_path, 'sub-%s' % sub_id, 'ses-*',
                                 file_folder, 'sub-%s*_%s.%s' %
                                 (sub_id, file_tag, file_type))
        else:
            files = os.path.join(main_path, 'sub-%s' % sub_id, file_folder,
                                 'sub-%s*_%s.%s' %
                                 (sub_id, file_tag, file_type))
    else:
        files = os.path.join(main_path, '*%s.%s' % (file_tag, file_type))

    files = glob.glob(files)
    files.sort()
    if filters:
        if not allow_other_fields:
            files = [file_ for file_ in files if
                     len(os.path.basename(file_).split('_')) <=
                     len(filters) + 1]
        files = [file_reference(file_) for file_ in files]
        for key, value in filters:
            files = [file_ for file_ in files if (key in file_ and
                                                  file_[key] == value)]
    else:
        files = [file_reference(file_) for file_ in files]

    if ref:
        return files
    else:
        return [ref_file['file_path'] for ref_file in files]


def bids_copy_events(behav_path='exp_info/recorded_events', data_root_path='',
                     dataset_name=None):
    data_path = get_bids_default_path(data_root_path, dataset_name)
    if glob.glob(os.path.join(data_root_path, behav_path, 'sub-*', 'ses-*')):
        sub_folders = glob.glob(os.path.join(behav_path, 'sub-*', 'ses-*'))
    else:
        sub_folders = glob.glob(os.path.join(data_root_path, behav_path, 'sub-*'))

    for sub_folder in sub_folders:
        for file_name in os.listdir(os.path.join(sub_folder, 'func')):
            shutil.copy2(os.path.join(sub_folder, 'func', file_name),
                         os.path.join(data_path, os.path.basename(sub_folder),
                                      'func', file_name))


def get_bids_path(data_root_path='', subject_id='01', folder='',
                  session_id=None):
    if session_id is None:
        session_id = ''
    else:
        session_id = 'ses-' + session_id
    return os.path.join(data_root_path, 'sub-' + subject_id,
                        session_id, folder)


def get_bids_file_descriptor(subject_id, task_id=None, session_id=None,
                             acq_id=None, rec_id=None, run_id=None,
                             file_tag=None, file_type=None):
    """Creates a filename descriptor following BIDS.

    subject_id refers to the subject label
    task_id refers to the task label
    run_id refers to run index
    acq_id refers to acquisition parameters as a label
    rec_id refers to reconstruction parameters as a label
    """
    descriptor = 'sub-{0}'.format(subject_id)
    if session_id is not None:
        descriptor += '_ses-{0}'.format(session_id)
    if task_id is not None:
        descriptor += '_task-{0}'.format(task_id)
    if acq_id is not None:
        descriptor += '_acq-{0}'.format(acq_id)
    if rec_id is not None:
        descriptor += '_rec-{0}'.format(rec_id)
    if run_id is not None:
        descriptor += '_run-{0}'.format(run_id)
    if file_tag is not None and file_type is not None:
        descriptor += '_{0}.{1}'.format(file_tag, file_type)
    return descriptor


def get_bids_default_path(data_root_path='', dataset_name=None):
    """Default experiment raw dataset folder name"""
    if dataset_name is None:
        dataset_name = 'bids_dataset'
    return os.path.join(data_root_path, dataset_name)


def get_exp_info_path():
    """Default experiment runs information folder name."""
    return 'exp_info'


def bids_init_dataset(data_root_path='', dataset_name=None,
                      dataset_description=dict(), readme='', changes=''):
    """Create directories and files missing to follow bids.

    Files and folders already created will be left untouched.
    This is an utility to initialize all files that should be present
    according to the standard. Particularly those that should be filled
    manually like participants.tsv and README files.

    participants.tsv columns can be extended as desired, the first column
    is mandatory by the standard, while the acq_date and NIP columns are only
    relevant as Neurospin/Unicog scanning reference and will be useful for
    automatic download of acquisitions respecting bids conventions.

    README is quite free as a file

    CHANGES follow CPAN standards

    Mandatory fields for dataset description saved by default are:
    Name: dataset_name
    BidsVersion: 1.0.0
    """
    dataset_name = get_bids_default_path(data_root_path, dataset_name)   
    if not os.path.exists(dataset_name):
        os.makedirs(dataset_name)
    # Check dataset_description.json
    f = os.path.join(get_bids_default_path(data_root_path, dataset_name),
                     'dataset_description.json')
    if not os.path.isfile(f):
        f = open(f, 'w')
        dataset_description.update({'Name': dataset_name,
                                    'BIDSVersion': '1.0.0'})
        json.dump(dataset_description, f)
    # Check README
    f = os.path.join(get_bids_default_path(data_root_path, dataset_name),
                     'README')
    if not os.path.isfile(f):
        f = open(f, 'w')
        f.write(readme)
        f.close()
    # Check CHANGES
    f = os.path.join(get_bids_default_path(data_root_path, dataset_name),
                     'CHANGES')
    if not os.path.isfile(f):
        f = open(f, 'w')
        f.write(changes)
        f.close()


def bids_acquisition_download(data_root_path='', dataset_name=None,
                              download_database='prisma',
                              force_download=False,
                              behav_path='exp_info/recorded_events',
                              test_paths=False):
    """Automatically download files from neurospin server to a BIDS dataset.

    Download-database is based on Neurospin server conventions.
    Options are 'prisma', 'trio' and custom path.
    Prisma db_path = '/neurospin/acquisition/database/Prisma_fit'
    Trio db_path = '/neurospin/acquisition/database/TrioTim'

    The bids dataset is created if necessary before download with some
    empy mandatory files to be filled like README in case they dont exist.

    The download depends on the file '[sub-*_][ses-*_]download.csv' contained
    in the folder 'exp_info'.

    NIP and acq date of the subjects will be taken automatically from
    exp_info/participants.tsv file that follows bids standard. The file will
    be copied in the dataset folder without the NIP column for privacy.

    Posible exceptions
    1) exp_info directory not found
    2) participants.tsv not found
    3) download files not found
    4) Acquisition directory in neurospin server not found
    5) There is more than one acquisition directory (Have to ask manip for
    extra digits for NIP, the NIP then would look like xxxxxxxx-ssss)
    6) Event file corresponding to downloaded bold.nii not found
    """
    # Check paths and files
    exp_info_path = os.path.join(data_root_path, get_exp_info_path())
    if not os.path.exists(exp_info_path):
        raise Exception('exp_info directory not found')
    if not os.path.isfile(os.path.join(exp_info_path, 'participants.tsv')):
        raise Exception('exp_info/participants.tsv not found')

    # Determine target path
    target_root_path = get_bids_default_path(data_root_path, dataset_name)
    # Determine path to files in Neurospin server
    if download_database == 'prisma':
        db_path = '/neurospin/acquisition/database/Prisma_fit'
    elif download_database == 'trio':
        db_path = '/neurospin/acquisition/database/TrioTim'
    else:
        db_path = download_database

    # Create dataset directories and files if necessary
    bids_init_dataset(data_root_path, dataset_name)

    # Get info of subjects/sessions to download
    pop = pd.read_csv(os.path.join(exp_info_path, 'participants.tsv'),
                      dtype=str, sep='\t', index_col=False)
#    pop = pd.read_csv(os.path.join(get_exp_info_path(), 'participants.tsv'),
#                      dtype=str, sep='\t', index_col=False)

    download_report = ('download_report_' +
                       time.strftime("%d-%b-%Y-%H:%M:%S", time.gmtime()) +
                       '.csv')
    download_report = open(os.path.join(target_root_path,
                                        download_report), 'w')
    report_line = '%s,%s,%s\n' % ('subject_id', 'session_id', 'download_file')
    download_report.write(report_line)
    # Download command for each subject/session
    # (following neurospin server conventions)
    for row_idx, subject_info in pop.iterrows():
        subject_id = subject_info['participant_id'].split('-')[1]
        if 'session_id' in subject_info.index:
            session_id = subject_info['session_id'].split('-')[1]
        else:
            session_id = None

        if session_id is None:
            ses_path = ''
        else:
            ses_path = 'ses-' + session_id
        sub_path = os.path.join(target_root_path, 'sub-' + subject_id,
                                ses_path)

        # Create subject path if necessary
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
        # Avoid redownloading subjects/sessions
        if not force_download:
            check_file = os.path.join(sub_path, 'downloaded')
            if os.path.isfile(check_file):
                continue

        # DATE has to be transformed from bids to neurospin server standard
        # Neurospin standard is yyyymmdd
        # Bids standard is YYYY-MM-DD
        DATE = subject_info['acq_date'].replace('-', '').replace('\n', '')
        NIP = subject_info['NIP']
        nip_dirs = glob.glob(os.path.join(db_path, str(DATE), str(NIP) + '-*'))
        print os.path.join(db_path, str(DATE), str(NIP) + '-*')
        if len(nip_dirs) < 1:
            raise Exception('No directory found for given NIP %s SESSION %s' %
                            (NIP, session_id))
        elif len(nip_dirs) > 1:
            raise Exception('Multiple path for given NIP %s SESSION %s' %
                            (NIP, session_id))

        optional_filters = [('sub', subject_id)]
        if session_id is not None:
            optional_filters += [('ses', session_id)]

        # Get appropriate download file. As specific as possible
        specs_path = file_manager_default_file(exp_info_path,
                                               optional_filters, 'download',
                                               file_type='tsv',
                                               allow_other_fields=False)
        report_line = '%s,%s,%s\n' % (subject_id, session_id, specs_path)
        download_report.write(report_line)

        specs = pd.read_csv(specs_path, dtype=str, sep='\t', index_col=False)

        # clean directories, in case a previous download failed
        for ridx, row in specs.iterrows():
            toclean = os.path.join(sub_path, row['acq_folder'])
            if os.path.exists(toclean):
                shutil.rmtree(toclean)

        # download images
        for ridx, row in specs.iterrows():
            def get_value(key, text):
                m = re.search(key + '-(.+?)_', text)
                if m:
                    return m.group(1)
                else:
                    return None

            run_task = get_value('task', row['acq_name'])
            run_id = get_value('run', row['acq_name'])
            run_session = get_value('ses', row['acq_name'])
            target_path = os.path.join(sub_path, row['acq_folder'])
            dicom_path = os.path.join(target_path, 'dicom')

            run_path = glob.glob(os.path.join(nip_dirs[0], '{0:06d}_*'.
                                              format(int(row['acq_id']))))
            if run_path:
                shutil.copytree(run_path[0], dicom_path)
            else:
                raise Exception('DICOM FILES NOT FOUNDS FOR RUN %s'
                                ' TASK %s SES %s SUB %s' % (run_id, run_task,
                                                            run_session,
                                                            subject_id))

#            subprocess.call("dcm2nii -g n -d n -e n -p n " + dicom_path,
#                            shell=True)
            subprocess.call(("dcm2niix -b y -z n -o {output_path} {data_path}".format(output_path=dicom_path, data_path=dicom_path)),
                            shell=True)

            # Expecting page 10 bids specification file name
            filename = get_bids_file_descriptor(subject_id, task_id=run_task,
                                                run_id=run_id,
                                                session_id=run_session,
                                                file_tag=row['acq_name'],
                                                file_type='nii')
                                                
            filename_json = os.path.join(target_path, filename[:-3] + 'json')
            
            shutil.copyfile(glob.glob(os.path.join(dicom_path,
                                                   '*.nii'))[0],
                            os.path.join(target_path, filename))
                          
            shutil.copyfile(glob.glob(os.path.join(dicom_path,
                                                   '*.json'))[0],
                            os.path.join(filename_json))
                            
            # Copy slice_times from dicom reference file
            #do by dcm2niix
#            if 'bold' in row['acq_name']:
#                dicom_ref = sorted(glob.glob(os.path.join(dicom_path,
#                                   '*.dcm')))[4]
#                slice_times = dicom.read_file(dicom_ref)[0x19, 0x1029].value
#                TR = dicom.read_file(dicom_ref).RepetitionTime
#                json_ref = open(os.path.join(target_path, filename[:-3] +
#                                'json'), 'a')
#                json.dump({'SliceTiming': slice_times,
#                           'RepetitionTime': int(TR)}, json_ref)
#                json_ref.close()
            # remove temporary dicom folder
            shutil.rmtree(dicom_path)

        done_file = open(os.path.join(sub_path, 'downloaded'), 'w')
        done_file.close()
    download_report.close()

    # Create participants.tsv in dataset folder (take out NIP column)
    participants_path = os.path.join(target_root_path, 'participants.tsv')
    pop.drop('NIP', 1).to_csv(participants_path, sep='\t', index=False)

    # Copy recorded event files
    bids_copy_events(behav_path, data_root_path, dataset_name)

if __name__ == "__main__":
    # Parse arguments from console
    parser = argparse.ArgumentParser(description='Neurospin to BIDS program')
    parser.add_argument('-root_path',
                        type=str,
                        nargs=1,
                        default=[''],
                        help='directory containing exp_info to download to')
    parser.add_argument('-dataset_name',
                        type=str,
                        nargs=1,
                        default=['bids_dataset'],
                        help='desired name for the dataset')
    parser.add_argument('-neurospin_database',
                        type=str,
                        nargs=1,
                        default=['prisma'],
                        help='neurospin server to download from')
    # LOAD CONSOLE ARGUMENTS
    args = parser.parse_args()
    bids_acquisition_download(data_root_path=args.root_path[0],
                              dataset_name=args.dataset_name[0],
                              download_database=args.neurospin_database[0],
                              force_download=False,
                              behav_path='exp_info/recorded_events',
                              test_paths=False)
