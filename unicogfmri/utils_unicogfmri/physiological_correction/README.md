# Physiological correction code

The files in PhysIO are a tool for correct fMRI images using physiological data acquired during acquisition (pulse and respiration). This toolbox computes the regressors (with RETROICOR algorithm) to be included in your design. It is a version of the TAPAS toolbox adapted for the 3T MRI scanner in NeuroSpin, using fMRI acquisitions with Minneapolis sequences.

### installation

Copy all the directory "PhysIO" in your local Matlab-SPM-toolbox directory:
    ~/matlab/spm8/toolbox/PhysIO/

### before using the toolbox

1) Organize your data (.nii, .log files).

2) In Matlab, run your local installation of SPM8 (only necessary once for a Matlab session):

    addpath /home/yourlogin/matlab/spm8
    spm('fmri')

3) You need to get some acquisition information from your data. For this, you can use the provided function "create_SliceTimingInfo_mat" that will create file SliceTiming.mat (in the directory of the .nii data) for every subject, by using file "list_subjects.txt" (the one used for importation).

More detailed information in the header of the function:

    function [SliceTiming, TR, TE, SliceThickness, SpacingBetweenSlices, ...
                NumberOfSlices, PixelSpacing, total_readout_time_spm, total_readout_time_fsl] ...
                = create_SliceTimingInfo_mat(spm_path, list_file, output_dir)
    
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
    %            = create_SliceTimingInfo_mat(spm_path, list_file, output_dir)
    %
    % Example:
    % > spm_path = '/home/yourlogin/matlab/spm8'
    % > list_file = '/yourworkingdirectory/list_subjects.txt'
    % > output_dir = '/yourworkingdirectory/subj1/data'
    % > create_SliceTimingInfo_mat(spm_path, list_file, output_dir)
 
### computing the regressors

Run function "physio_regressors_computation_tapas" with the appropriate parameters. For example :

    physio_regressors_computation_tapas('data','epi_sess1_bp160018_20160511_05',3,4,1,3)

*Attention*: this function only computes the regressors for ONE fMRI session (one .nii file)!

More detailed information in the header of the function:

    function physio_regressors_computation_tapas(data_local_dir, root_file_name, order_c, order_r, order_cr, verbose_level)
    %
    % Performs PhysIO-Regressor generation from Siemens Minneapolis sequence
    % logfiles
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Adapted by A. Moreno and F. Meyniel - 2016
    %
    % IMPORTANT: 
    %
    % 1) put all your data (.nii file, .log files) in a same directory for 
    %    every subject and session
    %
    % 2) before using this fuction, run the local installation of SPM8 
    %    (necessary only the first time after opening Matlab). For example:
    %
    % addpath /home/yourlogin/matlab/spm8
    % spm('fmri')
    %
    % CAREFUL: This function only computes the regressors for one fMRI session 
    %          (one .nii file)!
    %
    % Inputs: 
    %        - name of the local directory containing the data: .nii images,
    %        the physiological data (files _PULS.log, _RESP.log, _Info.log),
    %        and the file 'SliceTimingInfo.mat' (computed with the function 
    %        'create_SliceTimingInfo_mat.m'). This directory will also be the
    %        output directory where the regressors ( file 
    %        "physio_regressors_*.txt") will be copied in.
    %        - name of the .nii file (fMRI session) which must be the same root
    %        name for the physiological data files from Siemens 3T Minneapolis 
    %        (_PULS.log, _RESP.log and _Info.log)
    %        - order of cardiac phase Fourier expansion (e.g. 3)
    %        - order of respiratory phase Fourier expansion (e.g. 4)
    %        - order of sum/difference of cardiac/respiratory phase expansion 
    %        (phase interaction) (e.g. 1)
    %        - verbose_level indicates the number of plots to display:
    %        0 = none; 1 = main plots (default); 2 = debugging plots, for 
    %        setting up new study; 3 = all plots
    %
    % Output: file containing the physiological regressors, which is named with 
    %         the prefix "physio_regressors_" plus the root name, plus ".txt".
    %         This file is copied in the local data directory.
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
    % Example for running:
    % > physio_regressors_computation_tapas('data','epi_sess2_bp160018_20160511_07',3,4,1,3)
    %
    % Original codes from:
    % http://www.translationalneuromodeling.org/tnu-checkphysretroicor-toolbox/

