function physio_regressors_computation_tapas_7T_diff_dir_only_resp(data_local_dir, physio_dir, root_file_name, c, r, cr, verbose_level)
%
% Performs PhysIO-Regressor generation from Siemens 7T sequence logfiles
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
%        name for the physiological data files from Siemens 7T 
%        (_PULS.log and _RESP.log)
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
% > physio_regressors_computation_tapas_7T('data','epi_sess1_mp150285_20161018_12',3,4,1,3)
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

% TO DO AUTOMATICALLY!!!
%scan_info = load(fullfile(data_local_dir, 'SliceTimingInfo_000020_mbepi-1.0mm-MB1-iPAT3-pF7-8-TR1.5s-TE24.2ms-fs.mat')) ;
scan_info = load(fullfile(data_local_dir, 'SliceTimingInfo.mat')) ;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

physio      = tapas_physio_new();   % create structure, numbering according to *PhysIO_PhysNoiseBackground.pptx
log_files   = physio.log_files;     % 1a) Read logfiles
sqpar       = physio.scan_timing.sqpar;         % 1b) Sequence timing
%sqpar       = physio.sqpar;         % 1b) Sequence timing
thresh      = physio.preproc;
%thresh      = physio.thresh;        % 2) Preprocess phys & align scan-timing
model       = physio.model;         % 3)/4) Model physiological time series
verbose     = physio.verbose;       % Auxiliary: Output


%% 1. Define Input Files

log_files.vendor            = 'siemens_ns';
% log_files.cardiac           = strcat(fullfile(physio_dir, root_file_name),'.puls');
log_files.respiration       = strcat(fullfile(physio_dir, root_file_name),'.resp');
%log_files.scan_timing       = strcat(fullfile(data_local_dir, root_file_name),'_Info.log');
%log_files.scan_timing       = strcat(fullfile(data_local_dir, 'rl130571-1482_001_000020_1.3.12.2.1107.5.2.34.18917.2016072615302776915702732.dcm'));
%log_files.scan_timing       = strcat(fullfile(data_local_dir, 'dicom', 'rl130571-1482_001_000019_1.3.12.2.1107.5.2.34.18917.2016072615245287763878402.dcm'));

%log_files.sampling_interval = [2*1/400 8*1/400 1/400]; % [cardiac_SampleTime respiration_SampleTime tick_time] in seconds
%log_files.sampling_interval = 1/50; % = cardiac_SampleTime = respiration_SampleTime  in seconds
log_files.sampling_interval = []; % computed directly from log files
% log_files.sampling_interval = 40.2/1000; % Message from Lars Kasper: 
%                                          % Basically, if you leave log_files.sampling_interval empty ([]), 
%                                          % I compute the sampling rate of the physiological log files from the file itself 
%                                          % (which is usually more accurate), i.e. 
%                                          % sampling-rate = nSamplesInLogfile/(EndTimeLogfile-StartTimeLogfile) (in MDH-Time). 
%                                          % In your case, this was 40.2 ms for both respiratory and cardiac log file, not 20 ms. 
%                                          % The duration is then much closer to the 300ms you expected (see screenshot). 
%                                          % Heart rate looks reasonable then as well.
log_files.align_scan        = 'last';
log_files.relative_start_acquisition = 0 ; % in seconds

%% 2. Define Nominal Sequence Parameter (Scan Timing)

sqpar.Nslices           = scan_info.NumberOfSlices;
sqpar.NslicesPerBeat    = sqpar.Nslices;   % typically equivalent to Nslices; exception: heartbeat-triggered sequence
sqpar.TR                = scan_info.TR; % in seconds
sqpar.Ndummies          = 0;    % number of dummy volumes
my_vol                  = spm_vol(strcat(fullfile(data_local_dir, root_file_name),'.nii'));
sqpar.Nscans            = numel(my_vol); % donne le nombre d'images 3D dans le volume 4D
sqpar.onset_slice       = floor( (scan_info.NumberOfSlices + 1) / 2);   % The one in the middle % BE CAREFUL - TO ADAPT
%sqpar.onset_slice       = 1; % BE CAREFUL - TO ADAPT

% Set to >=0 to count scans and dummy
% volumes from beginning of run, i.e. logfile,
% includes counting of preparation gradientssqpar.Nprep             = [];
sqpar.time_slice_to_slice  = sqpar.TR / sqpar.Nslices;


%% 3. Order of RETROICOR-expansions for cardiac, respiratory and
%% interaction terms. Option to orthogonalise regressors

model.type = 'RETROICOR';  % ‘RETROICOR’ , ‘HRV’, ‘RVT’ or 
                                   % any combination of them, e.g. 
                                   % ‘RETROICOR_HRV’, 
                                   % ‘RETROICOR_HRV_RVT’, ‘HRV_RVT’
% RETROICOR parameters
model.retroicor.include = 1; 
model.retroicor.order = struct('c',3,'r',4,'cr',1, 'orthogonalise', 'none'); 
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
model.hrv.include = 0; 
model.hrv.delays = 0; % TODO: include delays! - see tapas_physio_new.m
    
% RVT parameters - RVT (Model): Respiratory Volume per time model , Birn et al, 2006/8
% Create a respiratory volume/time regressor using the respiratory response
% function
model.rvt.include = 0;
model.rvt.delays = 0; % (TODO)

% OTHER
model.input_other_multiple_regressors = ''; % either .txt-file or .mat-file (saves variable R)
model.output_multiple_regressors = strcat(data_local_dir, '/physio_regressors_', root_file_name, '.txt');

%% 4. Define Gradient Thresholds to Infer Gradient Timing (Philips only)
%
% method to determine slice onset times
% 'nominal' - to derive slice acquisition timing from sqpar directly
% 'gradient' or 'gradient_log' - derive from logged gradient time courses
%                                in SCANPHYSLOG-files (Philips only)
%thresh.scan_timing.method = 'nominal'; %'gradient_log'; 'nominal'

physio.scan_timing.sync.method = 'nominal';
%physio.scan_timing.sync.method = 'scan_timing_log';
%physio.scan_timing.sync.method = 'scan_timing_log_minn';


%% 5. Define which Cardiac Data Shall be Used

thresh.cardiac.modality = 'ECG'; % 'PPU' 'OXY' 'ECG'
%thresh.cardiac.initial_cpulse_select.method = 'load_from_logfile'; % using
%Siemens cardiac pulse trigger on signals...try out for comparison
thresh.cardiac.initial_cpulse_select.method = 'auto_matched'; % auto detection using cross-correlation to a self-calibrated template
thresh.cardiac.posthoc_cpulse_select.method = 'off';
thresh.cardiac.initial_cpulse_select.min = 0.3; % minimum pulse height (for detection of pulse peaks)


%% 6. Output Figures to be generated

%verbose.level           = 2; % 0 = none; 1 = main plots (default);  2 = debugging plots, for setting up new study; 3 = all plots
%verbose.level           = 3; % 0 = none; 1 = main plots (default);  2 = debugging plots, for setting up new study; 3 = all plots
verbose.level           = verbose_level; % 0 = none; 1 = main plots (default);  2 = debugging plots, for setting up new study; 3 = all plots
%verbose.fig_output_file = 'PhysIO.ps'; % Physio.tiff, .ps, .fig possible
%verbose.fig_output_file = 'PhysIO.tiff'; % Physio.tiff, .ps, .fig possible
verbose.fig_output_file = strcat(root_file_name, '_PhysIO_figure.tiff'); % .tiff, .ps, .fig possible

%% 7. Run the main script with defined parameters

physio.log_files    = log_files;
physio.sqpar        = sqpar;
physio.model        = model;
%physio.thresh       = thresh;
physio.preproc      = thresh; % Added by A. Moreno - 25/07/2016
physio.verbose      = verbose;

%% Save RETROICOR order information
order_to_save = model.retroicor.order;
%save(strcat(root_file_name, '_retroicor_order_info.mat'),'order_to_save')

[physio_out, R, ons_secs] = tapas_physio_main_create_regressors(physio);
