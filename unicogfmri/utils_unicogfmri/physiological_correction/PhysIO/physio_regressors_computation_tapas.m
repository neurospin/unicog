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
%
% Example for running:
% > physio_regressors_computation_tapas('data','epi_sess2_bp160018_20160511_07',3,4,1,3)
%
%
% Original codes from:
% http://www.translationalneuromodeling.org/tnu-checkphysretroicor-toolbox/
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   See also tapas_physio_new tapas_physio_read_physlogfiles_siemens
%
%
% Author: Lars Kasper, adapting similar code for file read-in 
%                      by Miriam Sebold, Charite Berlin (2014)
%
% Created: 2014-08-24
% Copyright (C) 2014 TNU, Institute for Biomedical Engineering, University of Zurich and ETH Zurich.
%
% This file is part of the TAPAS PhysIO Toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Load information in file 'SliceTimingInfo.mat' (this file has to be in
% the local data directory).
local_slice_timing_info_file = fullfile(data_local_dir, 'SliceTimingInfo.mat');
scan_info = load(local_slice_timing_info_file);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

physio      = tapas_physio_new();        % create structure, numbering according to *PhysIO_PhysNoiseBackground.pptx
log_files   = physio.log_files;          % 1a) Read logfiles
sqpar       = physio.scan_timing.sqpar;  % 1b) Sequence timing
thresh      = physio.preproc;            % 2) Preprocess phys & align scan-timing
model       = physio.model;              % 3)/4) Model physiological time series
verbose     = physio.verbose;            % Auxiliary: Output


%% 1. Define Input Files

log_files.vendor            = 'Siemens_minn';
log_files.cardiac           = strcat(fullfile(data_local_dir, root_file_name),'_PULS.log');
log_files.respiration       = strcat(fullfile(data_local_dir, root_file_name),'_RESP.log');
log_files.scan_timing       = strcat(fullfile(data_local_dir, root_file_name),'_Info.log');
log_files.sampling_interval = [2*1/400 8*1/400 1/400]; % [cardiac_SampleTime respiration_SampleTime tick_time] in seconds
log_files.align_scan        = 'first';
log_files.relative_start_acquisition = 0 ; % in seconds

%% 2. Define Nominal Sequence Parameter (Scan Timing)

sqpar.Nslices           = scan_info.NumberOfSlices;
sqpar.NslicesPerBeat    = sqpar.Nslices;   % typically equivalent to Nslices; exception: heartbeat-triggered sequence
sqpar.TR                = scan_info.TR; % in seconds
sqpar.Ndummies          = 0;    % number of dummy volumes
my_vol                  = spm_vol(strcat(fullfile(data_local_dir, root_file_name),'.nii'));
sqpar.Nscans            = numel(my_vol); % donne le nombre d'images 3D dans le volume 4D
sqpar.onset_slice       = 1; % or = floor( (scan_info.NumberOfSlices + 1) / 2);   % The one in the middle

% Set to >=0 to count scans and dummy
% volumes from beginning of run, i.e. logfile,
% includes counting of preparation gradientssqpar.Nprep             = [];
sqpar.time_slice_to_slice  = sqpar.TR / sqpar.Nslices;


%% 3. Order of RETROICOR-expansions for cardiac, respiratory and
%% interaction terms. Option to orthogonalise regressors

model.type = 'RETROICOR_HRV_RVT';  % ‘RETROICOR’ , ‘HRV’, ‘RVT’ or 
                                   % any combination of them, e.g. 
                                   % ‘RETROICOR_HRV’, 
                                   % ‘RETROICOR_HRV_RVT’, ‘HRV_RVT’
% RETROICOR parameters
model.retroicor.include = 1; 
model.retroicor.order = struct('c', order_c, 'r', order_r, 'cr', order_cr, 'orthogonalise', 'none'); 
                          % model.order.c: e.g. 3; order of cardiac phase 
                          %                Fourier expansion
                          % model.order.r: e.g. 4; order of respiratory
                          %                phase Fourier expansion
                          % model.order.cr: e.g. 1; order of sum/difference
                          %                 of cardiac/respiratory phase
                          %                 expansion (phase interaction)

% HRV parameters - HRV (Model): Heart Rate variability, Chang et al, 2009
% Create a heart-rate variability regressor using the cardiac response
% function
model.hrv.include = 1; 
model.hrv.delays = 0; % TODO: include delays! - see tapas_physio_new.m
    
% RVT parameters - RVT (Model): Respiratory Volume per time model , Birn et al, 2006/8
% Create a respiratory volume/time regressor using the respiratory response
% function
model.rvt.include = 1;
model.rvt.delays = 0; % (TODO)

% OTHER
model.input_other_multiple_regressors = ''; % either .txt-file or .mat-file (saves variable R)
output_multiple_regressors_filename = strcat('physio_regressors_', root_file_name, '.txt');
model.output_multiple_regressors = fullfile(data_local_dir, output_multiple_regressors_filename);

%% 4. Define Gradient Thresholds to Infer Gradient Timing (Philips only)
%
% method to determine slice onset times
% 'nominal' - to derive slice acquisition timing from sqpar directly
% 'gradient' or 'gradient_log' - derive from logged gradient time courses
%                                in SCANPHYSLOG-files (Philips only)
%thresh.scan_timing.method = 'nominal'; %'gradient_log'; 'nominal'

%physio.scan_timing.sync.method = 'nominal';
%physio.scan_timing.sync.method = 'scan_timing_log';
physio.scan_timing.sync.method = 'scan_timing_log_minn';


%% 5. Define which Cardiac Data Shall be Used

thresh.cardiac.modality = 'ECG';
%thresh.cardiac.initial_cpulse_select.method = 'load_from_logfile'; % using
%Siemens cardiac pulse trigger on signals...try out for comparison
thresh.cardiac.initial_cpulse_select.method = 'auto_matched'; % auto detection using cross-correlation to a self-calibrated template
thresh.cardiac.posthoc_cpulse_select.method = 'off';
thresh.cardiac.initial_cpulse_select.min = 0.3; % minimum pulse height (for detection of pulse peaks)


%% 6. Output Figures to be generated

verbose.level           = verbose_level; % 0 = none; 1 = main plots (default);  2 = debugging plots, for setting up new study; 3 = all plots
verbose.fig_output_file = strcat(root_file_name, '_PhysIO_figure.tiff'); % .tiff, .ps, .fig possible

%% 7. Run the main script with defined parameters

physio.log_files    = log_files;
physio.sqpar        = sqpar;
physio.model        = model;
physio.preproc      = thresh; % Added by A. Moreno - 25/07/2016
physio.verbose      = verbose;

% %% Save RETROICOR order information (uncomment if necessary)
% order_to_save = model.retroicor.order;
% save(strcat(root_file_name, '_retroicor_order_info.mat'),'order_to_save')

[physio_out, R, ons_secs] = tapas_physio_main_create_regressors(physio);
