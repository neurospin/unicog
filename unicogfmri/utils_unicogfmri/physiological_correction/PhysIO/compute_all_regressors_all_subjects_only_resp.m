%% Script to compute all regressors for all subjects

% RUN FIRST: spm12 + fMRI + quit

main_path   = '/neurospin/unicog/protocols/IRMf/my_path';
local_path  = 'fmri/acquisition1';
physio_dir  = 'physio/acquisition1/renamed';
regexp_func = '^epi_sess.*\.nii';

% sub_list = { 'sub01' }; % PROBLEM: file empty "epi_sess7_mp150285_20161018_24.resp"
sub_list = { 'sub03' }; % PROBLEM: all files *.puls have no signal (only one value = 2048)
% sub_list = { 'sub02', 'sub04', 'sub05', 'sub06', 'sub07', 'sub08', ...
%              'sub09', 'sub10', 'sub11', 'sub12', 'sub13', ...
%              'sub14', 'sub15', 'sub16'}; % OK

addpath('/..../physiological_correction_code/PhysIO/');
spm_path = '/i2bm/local/spm12';

for i_sub = 1:length(sub_list)
    
    disp('*****************************************************************');
    disp(sprintf('*********************   %s   *********************************',sub_list{i_sub}));
    disp('*****************************************************************');

    work_path = fullfile(main_path, sub_list(i_sub));
    cd(work_path{1});
    
    fdir =  fullfile(work_path, local_path);
    ffiles = spm_select('List', fdir, regexp_func);
    [n_files, n_col] = size(ffiles);
        
    % For every functional file, we compute the regressors
    for i_ffiles = 1:n_files
        
        file_name = ffiles(i_ffiles,1:end-4);

        % Copy the appropriate SliceTimingInfo_*.mat file into SliceTimingInfo.mat
        regexp_slicetimingfile = sprintf('^SliceTimingInfo_0000%s.*\\.mat',file_name(end-1:end));
        sltm_files = spm_select('List', fdir, regexp_slicetimingfile);
        cmd = sprintf('cd %s; cp %s SliceTimingInfo.mat', fdir{1}, sltm_files);
        unix(cmd)
        
        %physio_regressors_computation_tapas_7T_diff_dir(local_path, physio_dir, file_name, 3, 4, 1, 3); 
        physio_regressors_computation_tapas_7T_diff_dir_only_resp(local_path, physio_dir, file_name, 3, 4, 1, 1); 
        
        close all;
        
    end
    
end
