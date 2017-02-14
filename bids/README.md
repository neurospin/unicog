
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

As can be seen in the previous example since we go to the target path we do not need to provide the root_path. This is an old dataset, its files are stored in the "trio" server, so we have to specify it, but for new datasets it would not be necessary. Finally in this example the bids formatted dataset would be created in a folder name "bids_dataset".

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

Moreover there are plenty more optional fields to include in the file names depending on your needs. For more details on that please check directly the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

## Files in the **exp_info** folder specifying the data download:
Two type of files are mandatories: **participants.tsv** and **[sub-<subject_label>_][ses-<ses_label>_]download.tsv** in the **exp_info** directory.
Those files are not part of the bids standard. They are defined to contain the minimum information needed to simplify creating a bids dataset with the data from the neurospin server. So some of the information is related to the server and some to the experimental design and desired file naming.

### Participants.tsv

Contains information about the participants and their acqusitions. It contains three mandatory columns: participant_label, NIP and acq_data. When there are multiple sessions per subject (with different acquisition_dates), then the session_label column is also mandatory. Moreover other columns with subject information can be included like sex, manuality, etc.

-------------------------------------------------------------------------------
Nomenclature                       
-------------------------------------------------------------------------------
participant_label	NIP	        acq_date     session_label (if sessions)  other
label	            nip_number	YYYY-MM-DD   label                        xxx 
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Example
------------------------------------------------------------------------------
participant_label  NIP         acq_date     session_label    sex
01                 tt989898    2015-02-28   01               M
01                 tt989898    2015-03-15   02               M
02                 pp898989    2015-02-27   01               F
02                 pp898989    2015-03-20   02               F
-----------------------------------------------------------------------------

The order of the rows do not really matter, although we recommend to add the acquisitions as they are done and automatically download to make sanity checks of the data. The download can be done incrementally so there is no need for you to wait until the end of experiment to start downloading files to the bids format and start playing with it.

As you may have noticed only when multiple sessions take place we will find more than one row for the same participant, these rows should be identically in every value except for the acq_date and session_label.

The NIP column will only be used to identify subjects in the server and will not be included in any way on the bids dataset due to subject anonymization. Moreover we recommend you to not use the NIP as the participant_label to avoid future preprocessing of all the filenames of the dataset before publication.

The participant_label and session_label are taken from this file to create the folders and file names in the bids dataset, every other column will be added to a new participants.tsv file included under the bids_dataset top folder.

### Download.tsv

Contains information about the specific files to download from the neurospin server and how they should be named in the bids_dataset. This file convention was created to extremely facilitate specifying how to download and name the files for regular experimental designs for which each subject/session contains the same acquisition structure. Nonetheless it is also easy to add exceptions, like when the acquisition ids change due to repetition/cancelation of runs in the scanner or when the design itself is not regular across subjects.

So if the experimental design of all sessions is the same for all subjects, you only need to create one **download.tsv** file.

-------------------------------------------------------------------------------
Nomenclature                       
-------------------------------------------------------------------------------
acq_number   acq_folder              acq_name
n            bids_modality_folder    bids_desired_file_name
-------------------------------------------------------------------------------
**bids_modality_folder**: "anat" for the anatomical images and "func" for functional images.

**IMPORTANT bids_desired_file_name**: Before panicking rest assured that a filename like "task-MyTask_run-01_bold" is all you really need to know in most cases. Here we clarify details if you need extra fields of information or want to go beyond in available options.

the desired file name should comply with the specifications for any image type considered in the standard like is the case for anatomical and functional MRI. You need to provide here all the fields relevant for your file name respecting the bids standard fields specification, most of which are optional.

Moreover you have to give the tag at the end of the file appropriate for the file type but you will not include any file name extension, since the same file name is used with different extensions in the bids standard. For example there is bold.nii and bold.json for functional images and their accompanying acquisition information.

It is EXTREMELY important that the file_name avoids prohibited characters in the label of any field chosen (like the task field in functional images), to be safe limit yourself to write labels with the TitleCase format like field-MyParadigm or completely in lowercase like field-myparadigm.

The subject_id (sub-<label>) and session_id (ses-<label>) of course will be added for each subject and session as necessary, you only need to add the final tag name (like T1w or bold) and the relevant fields (like task and run on a functional image).

For more details about file naming please consult the bids specifications (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

-------------------------------------------------------------------------------
Example
-------------------------------------------------------------------------------
acq_number   acq_folder              acq_name
3            anat                    T1w
7            func                    task-LanguageLocalizer_bold
9            func                    task-MyParadigm_run-01_bold
11           func                    task-MyParadigm_run-02_bold
13           func                    task-MyParadigm_run-02_bold
-------------------------------------------------------------------------------
**Clarification**: All labels accompanying fields in the file name are strings. So the task label, run label, participant label and session labels in the example that use a numeric style are not part of the standard, feel free to pick the most appropriate label for your particular case.

Now in case there is a different design or an exception in acq_number due to problems during acquistion. You have to create additional files **[sub-<participant_label>_][ses-<session_label>_]download.tsv** as necessary. Where the participant_label and session_label are the same as in **participants.tsv**. You are not forced to create a specific file for each subject and session, the script looks for the most specific file it can find and use that one. For example if **sub-01_download.tsv** is provided and there are multiple sessions for that subject, all of them will assume the files follow the content of sub-01_download.tsv. If there is no file for sub-04 then it will assume the content of **download.tsv**. Basically there is a default reference file unless you provide a more specific one.

-------------------------------------------------------------------------------
Example **sub-01_download.tsv** (same as **download.tsv** but acq_number)
-------------------------------------------------------------------------------
acq_number   acq_folder              acq_name
3            anat                    T1w
9            func                    task-LanguageLocalizer_bold
11           func                    task-MyParadigm_run-01_bold
13           func                    task-MyParadigm_run-02_bold
15           func                    task-MyParadigm_run-02_bold
-------------------------------------------------------------------------------

# Importation of events:
The events for functional runs will be automatically copied in the bids dataset if the files are available in a "recorded_events" folder that already respect the bids structure. Which means that files would have the same fields as the bold.nii files in its file name but its final name part would be events.tsv instead, for example:

    <data_root>/exp_info/recorded_events/sub-<sub_label>[/ses-<ses_label>]/func/sub-*_<task>_events.tsv

Here is an example of **sub-\*\_\<task\>\_events.tsv** following the bids standard:

        onset	duration	trial_type
        0.0	1	computation_video
        2.4	1	computation_video
        8.7	1	h_checkerboard
        11.4	1	r_hand_audio
        15.0	1	sentence_audio

the onset, duration and trial_type columns are the only mandatory ones. onset and duration fields should be expressed in seconds. Other information can be added to events.tsv files such as ​response_time or other arbitrary additional columns respecting subject anonimity. See the bids specification (http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

# Notes:
* Note 1: if the importation has been interrupted or partially then, then launch again the script. The last partially downloaded data folder will be redownloaded from scratch.
* Note 2: the .tsv extension means "tabulation separated values", so each value must be separated by a tabulation and not commas, spaces or dots. If files in exp_info are not tsv, most likely the neurospin_to_bids.py script will fail. Please make sure your files comply with your favorite text editor.
