This script exports imaging data from the NeuroSpin archive into the 
BIDS format ([Brain Imaging Data Structure](http://bids.neuroimaging.io)).
The BIDS format has been selected because it is simple, easy to share
and supported by lots of software. We are focused on fMRI data but other
modalities can be added (diffusion imaging, behavioral, ...). For a full
description, please consult the
[BIDS specifications](http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

# Dependencies (can simply pip install packages):

        pip install pydicom --user
        pip install pandas --user

# Installation and usage:
## With the installation of the module
You can install the unicog repository and use `neurospin_to_bids.py` from anywhere.
To install the module, please tape:

        cd <path_to_download_to>
        git clone https://github.com/neurospin/unicog.git
        python setup.py install --user

and use as follow:

        neurospin_to_bids.py -h

## Without the installation of the module
If you don't want install the module, you can just use the `neurospin_to_bids.py` script as a python script.
Simply download the unicog repository:

        cd <path_to_download_to>
        git clone https://github.com/neurospin/unicog.git

and use as follow for instance:
                                        
        python <path_to_download_to>/unicog/bids/neurospin_to_bids.py -h


# Preparation of data
**To import data from NeuroSpin, you have to be connected to the NeuroSpin network.** 
In a few words, information about subjects to import are stored into a **exp_info** directory. For instance:

        ├── exp_info
        │   ├── download.tsv
        │   ├── participants.tsv
        │   └── recorded_events
        │       ├── sub-01
        │       │   └── func
        │       │       └── sub-01_task-standartloc_events.tsv
        │       └── sub-02
        │           └── func
        │               └── sub-02_task-standartloc_events.tsv



See a small example at [https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer_pypreprocess/scripts/exp_info](https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer_pypreprocess/scripts/exp_info)

# Importation of data
Now we set all files into **exp_info** directory, you can launch the importation:

	cd <path_where_is_exp_info>
	neurospin_to_bids.py -neurospin_database trio 

# More information on usage
You will find a dataset examples at:

* [https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer_pypreprocess/scripts/exp_info](https://github.com/neurospin/unicog/tree/master/unicogfmri/localizer_pypreprocess/scripts/exp_info)
* [https://github.com/neurospin/unicog/tree/master/bids/test_dataset/exp_info](https://github.com/neurospin/unicog/tree/master/bids/test_dataset/exp_info)

To make it work you simply have to open a terminal and write the following commands:

        cd <path_to>/data
        python neurospin_to_bids.py -neurospin_database trio

* The `<path_to>/data` folder must contain an `exp_info` subfolder with at least two files (`participants.tsv` and `download.tsv`) specifying the subjects to download. For more details on the content and structure of these files, read the Additional information section.
* The `neurospin_to_bids.py` script will export files from the NeuroSpin archive based on the information contained in the **exp_info** directory. The script when used as a bash command accept three optional arguments:
    * **-root_path**: specifies the target folder - by default the current directory.
    * **-neurospin_database**: refers to the NeuroSpin database where your images are stored, _prisma_, _trio_ or a full path - by default the most recent database _prisma_.
    * **-dataset_name**: the folder name to export the dataset to, by default subfolder `bids_dataset` of the target folder.

In the previous example we do not need `-root_path` since we move
into the target folder. This is an old dataset, its files are stored in the
_trio_ database, so we have to specify it, but for new datasets stored in
the _prisma_ database it would not be necessary. Finally in this example
the BIDS formatted dataset would be created in subfolder `bids_daw:taset`.

If instead we were to specify the target folder (the one containing an
`exp_info` subfolder) and a name for the BIDS dataset subfolder, we would
run the command as follows:

        neurospin_to_bids.py -root_path some_path -dataset_name my_dataset -neurospin_database trio

To read the script documentation you can write:

        neurospin_to_bids.py -h

# Additionnal information

## Basic BIDS organization
For anatomical and functional data, the bids nomenclature corresponds to the following organisation of files.

Anatomical:

        sub­-<participant_label>/
            [ses-<session_label>/]
                anat/
                    sub­-<participant_label>[_ses-<session_label>]_T1w.nii[.gz]

Functional:

        sub­-<participant_label>/
            [ses-<session_label>/]
                func/
                    sub­-<participant_label>[_ses-<session_label>]_task-­<task_label>[_run-­<run_label>]_bold.nii[.gz]

As seen by the examples, if you have a session level, a `ses-<session_label>`
subfolder is added under the `sub­-<participant_label>` folder and it would
then be the one to contain the modality folders (here, `anat` or `func`).
Moreover it should also form part of the file names.

The run level `run-<run_label>` is optional if there is only one functional
run for a particular task.

There are plenty more optional fields to include in the file names depending
on your needs. For more details on that please check directly the
[BIDS specifications](http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

## Files in the `exp_info` folder specifying the data download

Two files are mandatory in the `exp_info` directory: `participants.tsv`
and `[sub-<participant_label>_][ses-<session_label>_]download.tsv`.
Those files are not part of the BIDS standard. They are defined to contain
the minimum information needed to simplify creating a BIDS dataset with the
data from the NeuroSpin server. So some of the information is related to
the server and some to the experimental design and desired file naming.

### Participants.tsv

Contains information about the participants and their acqusitions.
It contains three mandatory columns: _participant_label_, _NIP_ and
_acq_data_.
When there are multiple sessions per subject (with different acquisition
dates), then the _session_label_ column is also mandatory. Moreover other
columns with subject information can be included like _sex_, _manuality_,
etc.

        -----------------------------------------------------------------------------
        Nomenclature                       
        -----------------------------------------------------------------------------
        participant_label  NIP         acq_date    session_label (if sessions)  other
        label              nip_number  YYYY-MM-DD  label                        xxx
        -----------------------------------------------------------------------------

        ----------------------------------------------------------------
        Example
        ----------------------------------------------------------------
        participant_label  NIP         acq_date     session_label    sex
        01                 tt989898    2015-02-28   01               M
        01                 tt989898    2015-03-15   02               M
        02                 pp898989    2015-02-27   01               F
        02                 pp898989    2015-03-20   02               F
        ----------------------------------------------------------------

The order of the rows does not really matter, although we recommend to add
the subjects as they are acquired and download to perform sanity checks
of the data. Downloads are incremental so there is no need for you to wait
until the end of experiment to start exporting files to the BIDS format
and start exploring your data.

As you may have noticed only when multiple sessions take place we will find
more than one row for the same participant, these rows should be identically
in every value except for the acq_date and session_label.

The _NIP_ column will only be used to identify subjects in the NeuroSpin
database and will not be included in any way on the BIDS dataset to ensure
proper de-identification. Moreover we recommend you to not use the NIP as
the _participant_label_ to avoid the need of future de-identification of
the BIDS dataset before publication.

The _participant_label_ and _session_label_ are taken from this file to
create the folders and file names in the BIDS dataset, every other column
will be added to a new `participants.tsv` file included under the
`bids_dataset` top folder.

### Download.tsv

Contains information about the specific files to export from the NeuroSpin
server and how they should be named in the `bids_dataset`. This file convention
was created to extremely facilitate specifying how to download and name the
files for regular experimental designs for which each subject/session contains
the same acquisition structure. Nonetheless it is also easy to add exceptions,
like when the acquisition ids change due to repetition/cancelation of runs
in the scanner or when the design itself is not regular across subjects.

So if the experimental design of all sessions is the same for all subjects,
you only need to create one `download.tsv` file.

        -----------------------------------------------------------
        Nomenclature                       
        -----------------------------------------------------------
        acq_number   acq_folder              acq_name
        n            bids_modality_folder    bids_desired_file_name
        -----------------------------------------------------------

**bids_modality_folder**: _anat_ for the anatomical images and _func_ for functional images.

**IMPORTANT bids_desired_file_name**: Before panicking rest assured that a filename like `task-MyTask_run-01_bold` is all you really need to know in most cases. Here we clarify details if you need extra fields of information or want to go beyond in available options.

the desired file name should comply with the specifications for any image type considered in the standard like is the case for anatomical and functional MRI. You need to provide here all the fields relevant for your file name respecting the BIDS standard fields specification, most of which are optional.

Moreover you have to give the tag at the end of the file appropriate for the file type but you will not include any file name extension, since the same file name is used with different extensions in the BIDS standard. For example there is bold.nii and bold.json for functional images and their accompanying acquisition information.

It is EXTREMELY important that the file_name avoids prohibited characters in the label of any field chosen (like the task field in functional images), to be safe limit yourself to write labels with the TitleCase format like field-MyParadigm or completely in lowercase like field-myparadigm.

The _subject_id_ (`sub-<participant_label>`) and _session_id_ (`ses-<session_label>`) of course will be added for each subject and session as necessary, you only need to add the final tag name (like T1w or bold) and the relevant fields (like task and run on a functional image).

For more details about file naming please consult the
[BIDS specifications](http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

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

Now in case there is a different design or an exception in acq_number due to problems during acquistion. You have to create additional files `[sub-<participant_label>_][ses-<session_label>_]download.tsv` as necessary. Where the _participant_label_ and _session_label_ are the same as in `participants.tsv`. You are not forced to create a specific file for each subject and session, the script looks for the most specific file it can find and use that one. For example if `sub-01_download.tsv` is provided and there are multiple sessions for that subject, all of them will assume the files follow the content of `sub-01_download.tsv`. If there is no file for `sub-04` then it will assume the content of `download.tsv`. Basically there is a default reference file unless you provide a more specific one.

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
The events for functional runs will be automatically copied in the BIDS dataset if the files are available in a `recorded_events` folder that already respect the bids structure. Which means that files would have the same fields as the bold.nii files in its file name but its final name part would be events.tsv instead, for example:

    <data_root>/exp_info/recorded_events/sub-<sub_label>[/ses-<ses_label>]/func/sub-*_<task>_events.tsv

Here is an example of `sub-*_<task>_events.tsv` following the BIDS standard:

        onset   duration   trial_type
        0.0     1          computation_video
        2.4     1          computation_video
        8.7     1          h_checkerboard
        11.4    1          r_hand_audio
        15.0    1          sentence_audio

the onset, duration and trial_type columns are the only mandatory ones. onset and duration fields should be expressed in seconds. Other information can be added to events.tsv files such as ​response_time or other arbitrary additional columns respecting subject anonimity. See the [BIDS specification](http://bids.neuroimaging.io/bids_spec1.0.0.pdf).

# Notes:
* Note 1: if the importation has been interrupted or partially then, then launch again the script. The last partially downloaded data folder will be redownloaded from scratch.
* Note 2: the .tsv extension means "tabulation separated values", so each value must be separated by a tabulation and not commas, spaces or dots. If files in `exp_info` are not tsv, most likely the `neurospin_to_bids.py` script will fail. Please make sure your files comply with your favorite text editor.
