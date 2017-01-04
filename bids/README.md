
We propose, here, a script to import data from the neuropsin dataserver with 
the BIDS organization (Brain Imaging Data Structure / http://bids.neuroimaging.io/).
The BIDS oragnization has been selected because the organization is simple, 
easily shared and supported by many software.
We are focused on fMRI data but other modalities can be added (diffusion imaging, behavioral ...)
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
        python path_to/neurospin_to_bids.py -neurospin_database trio

In this case, the **\<path_to/test_dataset\>** directory contains a **exp_info** directory with 2 files 
(**participants.tsv** and **download.tsv**) indicating what are the subjects to download.
For details on the files content/structure, read the Additional information section.
What about, the parameter neurospin_database refers to the neurospin server where your 
data are stored. Either "prisma" or "trio" (prisma is the default parameter).

# Advanced usage:

        python neurospin_to_bids.py -root_path <root_path> -dataset_name <my_dataset> -neurospin_database trio

The **-root_path** option allows to indicate a specific path including the **exp_info** directory.
The **-dataset_name** option allows to give a specific name to the dataset ( the default is bids_dataset).
For more information, read the Additional information section.

# Additionnal information
## Input files for the preparation of importation for one session per subject:
Two input files are mandatories and the events are optionals:

- **participants.tsv**: corresponds to the list of participants. 
Single session case:

        participant_id	NIP	acq_date
        sub-01	nip_number	2010-06-28
        sub-02	nip_number	2010-07-01

Multiple session case: 
The multiple session case corresponds to the acquisition of several identical or simalar data at 
different points in time. Typically, it corresponds to a longitudinal study. For more information, read
the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

        participant_id	session_id NIP	acq_date
        sub-01 sess-01 nip_number	date
        sub-01 sess-02 nip_number	date
        sub-02 sess-01 nip_number	date
        sub-02 sess-02 nip_number	date


- **download.tsv**: corresponds to the acquisitions to download. 
Single session case: one **download.tsv** file
If the number of acquisitions is the same for all subjects, you have to indicate only 
the acquisition number once. Here is an example:

        acq_id	acq_folder	acq_name
        <number> 	anat	T1w
        <number>	 	func	task-<name_task_one>
        <number>	 	func	task-<name_task_two>


Multiple runs per acquisition: add one line per run

        acq_id	acq_folder	acq_name
        <number> 		anat	T1w
        <number>	 	func	task-<name_task_one>_run01
        <number>	 	func	task-<name_task_one>_run02


Multiple session case: many **sess-<numb>_download.tsv** files
In this case you have to define one file per session. For instance, if you have 2 sessions:

File: **ses-01_download.tsv**

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<name-task>

File: **ses-02_download.tsv**

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<name-task>


# Importation events:
The events can be imported if files exist like this:

    <data_root>/exp_info/recorded_events/sub-*/func/sub-*_<task>_events.tsv


- **sub-\*\_\<task\>\_events.tsv**: here is an example:

        onset	duration	trial_type
        0.0	1	computation_video
        2.4	1	computation_video
        8.7	1	h_checkerboard
        11.4	1	r_hand_audio
        15.0	1	sentence_audio

Onset and duration fields should be expressed in second

Other information can be added to events.tsv files such as ​response_time or other
arbitrary additional columns.
See the bids specification (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).


Note 1: if the importation has been interrupted or partial, then launch again the script. All
data will be redownloaded.

Note 2: the files contained into exp_info are not a part of bids specifications. They are needed
in order to import and to organize data as defined in bids specifications.

Note 3: the .tsv extension means "tabulation separated values", so each value must be separated by a tabulation and not 
a set of dots. If you have some problems to read information contained into this kind of files, the confusion can be due
to points instead of tabulations. In order to check that point, display the tabulations thanks to your text editor.
 