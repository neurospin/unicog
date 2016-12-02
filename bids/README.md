
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


# Using:

        cd path_to/test_dataset
        python path_to/neurospin_to_bids.py -neurospin_database trio


# Additionnal information
## Input files for the preparation of importation:
Two input files are needed:
- participants.tsv: corresponds to the list of participants. Here is an example:

        participant_id	NIP	acq_date
        sub-1	nip_number	2010-06-28
        sub-2	nip_number	2010-07-01



- download.tsv: corresponds to the acquisitions to download. If the number of acquisition is
the same for all subjects, you have to indicate only the acquisition number once. Here is an 
example:

        acq_id	acq_folder	acq_name
        2	anat	T1w
        9	func	task-loc_std_bold

## Importation of data:
Remind this script is dedecated to Neurospin server.

        cd path_to/<data>
        python neurospin_to_bids.py -neurospin_database trio

Select your database_neurospin either "prisma" or "trio" (prisma is the default parameter).
If you need, you can use a specific path.

Note:
If the importation is interrupted, the script will import only missing data.   

<!-- Importation events: -->
