
We propose, here, a script to import data from the neuropsin dataserver with 
the BIDS organization (Brain Imaging Data Structure / http://bids.neuroimaging.io/).
The BIDS oragnization has been selected because the organization is simple, 
easily shared and supported by many software even if it is not a standard.

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
For more information, read the Additional information section.
Indicate your **neurospin_database** either "prisma" or "trio" (prisma is the default parameter).

# Advanced usage:

        python neurospin_to_bids.py -root_path <root_path> -dataset_name <my_dataset> -neurospin_database trio

The **-root_path** option allows to indicate a specific path including the **exp_info** directory.
The **-dataset_name** option allows to give a specific name to the dataset ( the default is bids_dataset).
For more information, read the Additional information section.

# Additionnal information
## Input files for the preparation of importation:
Two input files are mandatory and the events are optionals:

- **participants.tsv**: corresponds to the list of participants. Here is an example:

        participant_id	NIP	acq_date
        sub-1	nip_number	2010-06-28
        sub-2	nip_number	2010-07-01



- **download.tsv**: corresponds to the acquisitions to download. If the number of acquisition is
the same for all subjects, you have to indicate only the acquisition number once. Here is an 
example:

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-loc_std_bold


- **sub-\*\_\<task\>\_events.tsv**: here is an example:

        onset	duration	trial_type	trial_name
        0.0	1	8	computation_video
        2.4	1	8	computation_video
        8.7	1	1	h_checkerboard
        11.4	1	3	r_hand_audio
        15.0	1	10	sentence_audio


# Importation events:
The events can be imported if files exist like this:

    <data_root>/exp_info/recorded_events/sub-*/func/sub-*_<task>_events.tsv


<!-- * Multiple session: --> 

Note:
If the importation is interrupted, the script will import only missing data.   