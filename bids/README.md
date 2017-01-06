
We propose a script to import data from the neuropsin dataserver according to 
the BIDS organization (Brain Imaging Data Structure / http://bids.neuroimaging.io/).
The BIDS oragnization has been selected because the organization is simple, 
easily shared and supported by many software.
We are focused on fMRI data but other modalities can be added (diffusion imaging, behavioral ...).
For a full description, please see the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

# Dependencies (can simply pip install package):
pydicom  
pandas

# Installation:
The neurospin_to_bids.py script can be use without install the unicog module.
 
## Download the unicog module:

        git clone https://github.com/neurospin/unicog.git

## Read the documentation:

        python neurospin_to_bids.py -h

# Demonstration data:
The test_dataset follows a minimal set of conventions for the download to work.


# Basic usage:

        cd <path_to/test_dataset>
        python <path_to>/neurospin_to_bids.py -neurospin_database trio

* The **\<path_to/test_dataset\>** directory contains an **exp_info** directory with 2 files 
(**participants.tsv** and **download.tsv**) indicating what are the subjects to download.
For details on the files content/structure, read the Additional information section.
* The **neurospin_database** parameter refers to the neurospin server where your 
data are stored, either "prisma" or "trio" (prisma is the default parameter).

# Advanced usage:

        python neurospin_to_bids.py -root_path <root_path> -dataset_name <my_dataset> -neurospin_database trio

* The **root_path** option allows to indicate a specific path including the **exp_info** directory.
* The **dataset_name** option allows to give a specific name to the dataset (the default is bids_dataset).

# Additionnal information
## Input files for the importation of data:
Two files are mandatories: **participants.tsv** and **[sub-*_][ses-*_]download.csv**. Their configuration is depending
to the dataset (number of sessions, runs, tasks ....). Many cases are presented below.

### One session/subject 
- **participants.tsv**: corresponds to the list of participants. Some additional field can be added such
as sex, age ... 

        participant_id	NIP	acq_date
        sub-01	nip_number	year-month-day
        sub-02	nip_number	year-month-day

- **download.tsv**: corresponds to the acquisitions to download.
If the number of acquisitions is the same for all subjects, you have to indicate only 
the acquisition number once. Here is an example:

        acq_id	acq_folder	acq_name
        <number> 	anat	T1w
        <number>	 	func	task-<name_task_one>
        <number>	 	func	task-<name_task_two>

The **acq_id** corresponds to a part of the acquired files. For instance, for **000002_mprage-sag-T1-160sl** file, the line 
will be:

        2 	anat	T1w

If the **acq_id** is not the same for all subjects, you have to create a specific **download.tsv** per subject.
For instance:

* **sub-01_download.tsv** file:


        acq_id	acq_folder	acq_name
        2	anat	T1w
        10	func	task-<name-task>


* **sub-02_download.tsv** file:

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<name-task>


### Multiple runs/acquisition: 
The **participants.tsv** file is the same as above.

For the **download.tsv** file add one line per run in as follows:

        acq_id	acq_folder	acq_name
        <number> 		anat	T1w
        <number>	 	func	task-<name_task_one>_run01
        <number>	 	func	task-<name_task_one>_run02

### Multiple sessions/subject: 
The multiple session case corresponds to the acquisition of several identical or simalar data at 
different points in time. Typically, it corresponds to a longitudinal study. For more information, read
the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).


- The **participants.tsv** file will be:

        participant_id	session_id NIP	acq_date
        sub-01 ses-01 nip_number	date
        sub-01 ses-02 nip_number	date
        sub-02 ses-01 nip_number	date
        sub-02 ses-02 nip_number	date


- Many **ses-\<numb\>\_download.tsv**  files as follows:

    **ses-01_download.tsv** file:

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<name-task>


    **ses-02_download.tsv** file:

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<name-task>

If you have some specific information on subjects for each session, you have to create files as **[sub-*_][ses-*_]download.csv**.

# Importation events:
The events (optionals) can be imported if files exist as follows:

    <data_root>/exp_info/recorded_events/sub-*/func/sub-*_<task>_events.tsv


Here is an example of **sub-\*\_\<task\>\_events.tsv**: 

        onset	duration	trial_type
        0.0	1	computation_video
        2.4	1	computation_video
        8.7	1	h_checkerboard
        11.4	1	r_hand_audio
        15.0	1	sentence_audio

Onset and duration fields should be expressed in second.
Other information can be added to events.tsv files such as ​response_time or other
arbitrary additional columns.
See the bids specification (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).


# Notes:
* Note 1: if the importation has been interrupted or partial, then launch again the script. All
data will be redownloaded.
* Note 2: the files contained in the exp_info directory are not a part of bids specifications. They are needed
in order to import and organize data as defined in bids specifications.
* Note 3: the .tsv extension means "tabulation separated values", so each value must be separated by a tabulation and not 
a set of dots. If the neurospin_to_bids.py script has some problems to read information contained in this kind of files, the problem can be due
to dots instead of tabulations. In order to check that point, display the tabulations thanks to your text editor.
 