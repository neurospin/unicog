
We propose a script to import data from the neurospin dataserver according to 
the BIDS organization (Brain Imaging Data Structure / http://bids.neuroimaging.io/). The BIDS oragnization has been selected because the organization is simple, easy to share and supported by many software. We are focused on fMRI data but other modalities can be added (diffusion imaging, behavioral ...). For a full description, please see the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

# Dependencies (can simply pip install packages):

        pip install pydicom --user
        pip install pandas --user

# Installation:
The neurospin_to_bids.py script can be used as a bash command. There is no need for installation.

Simply download the unicog repository:

        cd <path_to_download_to>
        git clone https://github.com/neurospin/unicog.git

# Usage:

After downloading the unicog repository, you will find a dataset example in unicog/bids. The test_dataset follows the minimal set of conventions necessary to make a test download.

To make it work you simply have to open a terminal and write the following commands:

        cd <path_to>/unicog/bids/test_dataset
        python <path_to>/unicog/bids/neurospin_to_bids.py -neurospin_database trio

* The **\<path_to\>/test_dataset** directory must contain an **exp_info** directory with 2 files (**participants.tsv** and **download.tsv**), indicating what are the subjects to download. For more details, on the files content and structure, read the Additional information section.
* The neurospin_to_bids.py script will download files from a Neurospin server based on the information contained in the **exp_info** directory. The script when used as a bash command accept three optional arguments:
    * **-root_path**: allows to specify the target directory, if not given the current directory will be taken as root_path.
    * **-neurospin_database**: refers to the neurospin server where your images are stored, either "prisma" or "trio" (prisma, the most recent server, is the default parameter).
    * **-dataset_name**: the folder name of the downloaded bids formatted dataset. It is "bids_dataset" by default.

As can be seen in the previous example since we cd to the target path we do not need to provide the root_path. Since this is an old dataset, its files are stored in the "trio" server, so we have to specify it, but for new datasets it would not be necessary. Finally in this example the bids formatted dataset would be created in a folder name "bids_dataset".

If instead we wanted to pass the root_path (the one containing an **exp_info** folder) and specify a name for the bids dataset folder we would run the command as follows:

        python neurospin_to_bids.py -root_path some_path -dataset_name my_dataset -neurospin_database trio

To read the script documentation you can write:

        python neurospin_to_bids.py -h

# Additionnal information
## Basic BIDS organization
For anatomical and functional data, the bids nomenclature corresponds to the following organisation of files.

Anatomical:

        sub­-<participant_label>/
            [ses-<session_label>]/
                anat/
                    sub­-<participant_label>[_ses-<session_label>]_T1w.nii[.gz]

Functional:

        sub­-<participant_label>/
            [ses-<session_label>]/
                func/
                    sub­-<participant_label>[_ses-<session_label>]_task-­<task_label>[_run-­<run_label>]_bold.nii[.gz]

As seen by the examples, if you have a session level, a **ses-<ses_label>** directory is added under the **sub­-<participant_label>** and it would then be the one to contain the modality folders (here, **anat** or **func**). Moreover it should also form part of the file names.

The run_id "run-<run_label>" is optional if there is only one functional run for a particular task.

Moreover there are plenty more optional id fields to include in the file names depending on your needs. For more details on that please check directly the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

## Input files for the importation of data:
Two files are mandatories: **participants.tsv** and **[sub-*_][ses-*_]download.csv** in the **exp_info** directory. 
Those files are not a part of bids specifications. They are needed in order to import and organize data as defined in bids specifications
Their configuration is depending on the dataset (number of sessions, runs, tasks ....). Many cases are presented below.

### One session/subject 
- **participants.tsv**: corresponds to the list of participants. Some additional field can be added such
as sex, age ... 

--------------------------------------------------------------------
Nomenclature                            Example
-------------------------------------   ----------------------------
participant_label	NIP	acq_date     participant_label	NIP	acq_date
sub-label	nip_number	YYYY-MM-DD        sub-01	tt989898	2015-02-28
sub-label	nip_number	YYYY-MM-DD        sub-02	pp898989	2015-02-27
--------------------------------------------------------------------


+----------------------------+-------+
| En-tête                    | etc... |
+===+===+
| Plusieurs lignes de texte  | - liste |
| dans la même cellule, mais | - à puces |
| toujours aligné à gauche ! |
+---+---+
| Texte _formaté_,           | #. liste |
| `code`, etc...             | #. numérotée |
+---+---+



- **download.tsv**: corresponds to the acquisitions to download.
If the number of acquisitions are the same for all subjects, you can share the **download.tsv** file for all subjects:

        acq_label    acq_folder	acq_name
        label	     anat	T1w
        label	     func	task-<label>
        label	     func	task-<label>

If the number of acquisitions are not the same for all subjects, you have to write a specific **[sub-*_][ses-*_]download.csv** file for all
subject:

* **sub-01_download.tsv** file:
        acq_label    acq_folder	acq_name
        label	     anat	T1w
        label	     func	task-<label>

* **sub-02_download.tsv** file:
        acq_label    acq_folder	acq_name
        label	     anat	T1w
        label	     func	task-<label>


The **acq_label** corresponds to a part of the acquired files. For instance, for **000002_mprage-sag-T1-160sl** file, the line 
will be:

        2 	anat	T1w

If the **acq_label** is not the same for all subjects, you have to create a specific **download.tsv** per subject.
For instance:

* **sub-01_download.tsv** file:


        acq_label	acq_folder	acq_name
        2	anat	T1w
        10	func	task-<label>


* **sub-02_download.tsv** file:

        acq_label	acq_folder	acq_name
        2	anat	T1w
        9	func	task-<label>


### Multiple runs/acquisition: 
The **participants.tsv** file is the same as above.

For the **download.tsv** file add one line per run in as follows:

        acq_label	acq_folder	acq_name
        <number> 		anat	T1w
        <number>	 	func	task-<label>_run01
        <number>	 	func	task-<label>_run02

### Multiple sessions/subject: 
The multiple session case corresponds to the acquisition of several identical or simalar data at 
different points in time. Typically, it corresponds to a longitudinal study. For more information, read
the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).


- The **participants.tsv** file will be:

        participant_label	session_id NIP	acq_date
        sub-01 ses-01 nip_number	YYYY-MM-DD
        sub-01 ses-02 nip_number	YYYY-MM-DD
        sub-02 ses-01 nip_number	YYYY-MM-DD
        sub-02 ses-02 nip_number	YYYY-MM-DD


- Many **ses-\<numb\>\_download.tsv**  files as follows:

    **ses-01_download.tsv** file:

        acq_label	acq_folder	acq_name
        2	anat	T1w
        9	func	task-label


    **ses-02_download.tsv** file:

        acq_label	acq_folder	acq_name
        2	anat	T1w
        9	func	task-label

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
* Note 2: the .tsv extension means "tabulation separated values", so each value must be separated by a tabulation and not 
a set of dots. If the neurospin_to_bids.py script has some problems to read information contained in this kind of files, the problem can be due
to dots instead of tabulations. In order to check that point, display the tabulations thanks to your text editor.
 
