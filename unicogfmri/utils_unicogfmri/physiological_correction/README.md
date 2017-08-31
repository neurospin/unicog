# Physiological correction code

PhysIO is a toolbox that can be used to correct fMRI images using physiological data acquired during acquisition (pulse and respiration). This toolbox computes the regressors (with RETROICOR algorithm) to be included in your design. It is a version of the [TAPAS toolbox](http://www.translationalneuromodeling.org/tnu-checkphysretroicor-toolbox/) (check their website for recent updates). It has been adapted for the 3T MRI scanner in NeuroSpin, using fMRI acquisitions with Minneapolis sequences, and also for the 7T MRI scanner in NeuroSpin.

### installation

Copy all the directory "PhysIO". Then, you will have to add the path to it in Matlab:
    
    addpath('/path_to_the_toolbox/PhysIO/')

### before using the toolbox

1.- Organize your data: .nii and .log files must be in the local "fMRI" directory for every subject.

2.- In Matlab, add the directory containing the "PhysIO" toolbox and run SPM (only necessary once for a Matlab session):

    addpath('/path_to_the_toolbox/PhysIO/')
    spm_path = '/i2bm/local/spm12'
    spm12 # or other version

3.- You need to get some acquisition information from your data. For this, you can use the provided function “create_SliceTimingInfo_mat” (or one of the adapted versions -see the comments in the corresponding file for further information-) that will create file SliceTimingInfo.mat (in the directory “fMRI” containing the .nii data) for every subject, by using file “list_subjects.txt” (the file typically used for importation).

**Attention**: 

* this function must be run in the directory where "list_file" is placed and where there are also the subjects directories.

* data must be placed in a subdirectory called "fMRI" for every subject.

More detailed information in the header of the function:

    function [SliceTiming, TR, TE, SliceThickness, SpacingBetweenSlices, ...
                NumberOfSlices, PixelSpacing, total_readout_time_spm, total_readout_time_fsl] ...
                = create_SliceTimingInfo_mat(spm_path, list_file, machine_ns)
    
    % Adapted by A. Moreno (September 2016) from code created by F. Meyniel:
    % https://github.com/florentmeyniel/fmspm12batch/blob/PhysioCorrection/fmspm12batch_preproc_GetSliceTiming_NS.m
    %
    % Function to get (and save) various acquisition parameter, such as
    % RT, slice timing info... from the Neurospin server for a particular subject. 
    % The parameters are read in the header of a parciular dicom volume; theyt should 
    % not vary across volume and subject. Note that the accuracy of the slice
    % timing is numbers is <5ms).
    % 
    % To get the parameter value from an arbitrary DICOM file, use the option 5th argument 
    % to overide the search on the Neurospin server. The file name of this reference
    % DICOM file should be a full path name..
    %
    % Possible values of the (optional) variable 'machine_ns':
    % machine_ns = '3T' (default value)
    % machine_ns = '7T'
    %
    % Value returned:
    % 	SliceTiming
    % 	TR
    % 	TE
    % 	SliceThickness
    % 	SpacingBetweenSlices
    % 	NumberOfSlices
    % 	PixelSpacing (inplane resolution)
    % 	total_readout_time_spm: effective readout time of 1 EPI
    % 	total_readout_time_fsl: same with a minor difference.
    % 
    % Usage:
    % [SliceTiming, TR, TE, SliceThickness, SpacingBetweenSlices, ...
    %            NumberOfSlices, PixelSpacing, total_readout_time_spm, total_readout_time_fsl] ...
    %            = create_SliceTimingInfo_mat(spm_path, list_file, machine_ns)
    %
    % Attention: 
    % - this function must be run in the directory where "list_file" is placed 
    %   and where there are also the subjects directories.
    % - data must be placed in a subdirectory called "fMRI" for every subject.
    % 
    % ---- list_subjects.txt 
    %   |
    %   |- subj01 --- anat
    %   |          |- fMRI
    %   |
    %   |- subj02 --- anat
    %   |          |- fMRI
    %   |
    %   |- subj03 --- anat
    %   |          |- fMRI
    %   |
    %   |- RUN THIS FUNCTION HERE
    % 
    %
    % Example:
    % > spm_path = '/i2bm/local/spm8'
    % > list_file = 'list_subjects.txt'
    % > create_SliceTimingInfo_mat(spm_path, list_file)
    % or:
    % > create_SliceTimingInfo_mat(spm_path, list_file, '7T')

### computing the regressors

Run function "physio_regressors_computation_tapas" (or the adapted version) with the appropriate parameters. For example:

    physio_regressors_computation_tapas('epi_sess1_bp160018_20160511_05',3,4,1,3)

**Attention**: this function only computes the regressors for ONE fMRI session (one .nii file)!

Some examples of use are furnished in files: “compute_all_regressors_all_subjects.m”, “compute_all_regressors_all_subjects_only_puls.m”, “compute_all_regressors_all_subjects_only_resp.m”.

More detailed information in the header of the function(s):

    function physio_regressors_computation_tapas(data_local_dir, root_file_name, c, r, cr, verbose_level)
    %
    % Performs PhysIO-Regressor generation from Siemens Minneapolis sequence
    % logfiles
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Adapted by A. Moreno and F. Meyniel - 2016
    %
    % IMPORTANT: 
    %
    % 1) put all your data (.nii file, .log files) in a directory called "data"
    %    at the same level as this .m file
    %
    % 2) before using this fuction, run the local installation of SPM8 
    %    (necessary only the first time after opening Matlab). For example:
    %
    % addpath /home/am985309/matlab/spm8
    % spm('fmri')
    %
    % CAREFUL: This function only computes the regressors for one fMRI session 
    %          (one .nii file)!
    %
    % Inputs: 
    %        - name of the local directory containing the data 
    %        - name of the .nii file (fMRI session) which must be the same root
    %        name for the physiological data files from Siemens 3T Minneapolis 
    %        (_PULS.log, _RESP.log and _Info.log)
    %        - verbose_level indicates the number of plots to display:
    %        0 = none; 1 = main plots (default);  2 = debugging plots, for 
    %        setting up new study; 3 = all plots
    %
    % Output: file containing the physiological regressors, which is named with 
    %         the prefix "physio_regressors_" plus the root name, plus ".txt"
    %         The output matrix contains columns corresponding to the
    %         regressors such that (for an example of order 3 for cardiac 
    %         signal and order 4 for respiration):
    %
    %       cardiac          |      respiration      |        interaction c-r       |   HRV    |    RVT   |
    %  6 columns (order 3)   |  8 columns (order 4)  |      4 columns (ordre 1)     | 1 column | 1 column |
    %  2(sin-cos) x 3(order) | 2(sin-cos) x 4(order) | 4(sin-cos/sincos-cossin) x 1 |          |          |
    % Total: 20 columns
    %
    % "The physIO Toolbox offers to model Fourier expansions of cardiac and 
    % respiratory phase according to RETROICOR (Glover et al., 2000; 
    % Harvey et al., 2008), as well as noise modeling of heart rate 
    % variability (HRV) and respiratory volume per time (RVT) utilizing
    % the cardiac and respiratory response function, respectively 
    % (Birn et al., 2008; Chang et al., 2009)" 
    % -- from Handbook_PhysIO_Toolbox.pdf in TAPAS toolbox
    %
    %
    % Example for running:
    % > physio_regressors_computation_tapas('data','epi_sess2_bp160018_20160511_07',3)
    %
    %
    % Original codes from:
    % http://www.translationalneuromodeling.org/tnu-checkphysretroicor-toolbox/

