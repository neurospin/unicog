%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generation of first level analysis batches
% 
% Time-stamp: <2012-07-26 13:32 christophe@pallier.org>

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% experiment-specific parameters

spm_path = '/i2bm/local/spm8';

root = '/my_data_path/Subjects'; 

fmridir =  'fMRI/acquisition1' ; % path of fMRI data (4D nifti) within subject directory

TR = 1.5;

output_dir = 'analyses/hrf' ; % path where the SPM.mat will be created, within each subjects' dir
onsets_dir = 'onsets';

suffix = '_hrf'; 

% list the subjects directory in the variable "subjects"
%[subjects] = textread(fullfile(root,'dirs.txt'),'%s');
%[subjects acq] = textread(fullfile(root,'dirs.txt'),'%s %s'); %% AM - 10/08/2012 - To take into account acquisitions in file dirs.txt

% see below if you want to modify the basis functions

% End of configuration section
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% addpath(spm_path); % comment to run in compiled spm8
spm('defaults', 'FMRI');
spm_jobman('initcfg');


for s = 1:length(subjects)
     
    rootdir = fullfile(root, subjects{s});

    %funcdir = spm_select('CPath','fMRI',rootdir);
    funcdir = spm_select('CPath',fmridir,rootdir); %% AM - 10/08/2012
    %funcfiles = cellstr(spm_select('List',funcdir, '^swn.*.nii$'));
    funcfiles = cellstr(spm_select('List',funcdir, '^sw.*.nii$'));

    nrun = size(funcfiles,1);
    clear matlabbatch
    
    if ~exist(fullfile(rootdir, output_dir),'dir') %% AM - 11/09/2012
        mkdir(rootdir, output_dir);
    end
    
    matlabbatch{1}.spm.stats.fmri_spec.dir = cellstr(spm_select('CPath', output_dir, rootdir));
    matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'secs';
    matlabbatch{1}.spm.stats.fmri_spec.timing.RT = TR;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 1;
%%

    for n=1:nrun
      cfile = funcfiles{n};
      ff = spm_select('ExtFPList',funcdir, cfile, Inf);
      basename = cfile(3:length(cfile)-4);
      %basename = cfile(4:length(cfile)-4); %% AM - 10/08/2012 - To be coherent with the wiki page: "The name of these onset files must be the same as the corresponding EPI files, with an additional suffix. E.g. if the image files are bloc1.nii, bloc2.nii, ... the mat files can be bloc1_model1.mat, bloc2_model1.nii,... This suffix system allows you to generate different models with different events." 
      rpfile = sprintf('rp_%s.txt', basename);
      %rpfile = sprintf('rp_a%s.txt', basename); %% AM - 10/08/2012 - For clean basename
      %matfile_name = sprintf('%s%s.mat', basename, suffix)
      matfile_name = 'localizer.mat'
      matfile = subdir(fullfile(root,matfile_name)) 
      %matfile = subdir(fullfile(root,onsets_dir,matfile_name)) %% AM - 11/09/2012 - .mat in the correct directory !!
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).scans = cellstr(ff);
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).cond = struct('name', {}, 'onset', {}, 'duration', {}, 'tmod', {}, 'pmod', {});
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).multi = { matfile.name };
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).regress = struct('name', {}, 'val', {});
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).multi_reg = cellstr(spm_select('CPath',rpfile,funcdir));
      matlabbatch{1}.spm.stats.fmri_spec.sess(n).hpf = 128;
    end

    matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
    matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
    matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
    matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';

    % bases functions [TODO: improve this part]
    matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
% Hrf simple
    matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [1 0];
% FIR:
%    matlabbatch{1}.spm.stats.fmri_spec.bases.fir.length = 14.4;
%    matlabbatch{1}.spm.stats.fmri_spec.bases.fir.order = 12;

    matlabbatch{2}.spm.stats.fmri_est.spmmat(1) = cfg_dep;
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).tname = 'Select SPM.mat';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).tgt_spec{1}(1).name = 'filter';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).tgt_spec{1}(1).value = 'mat';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).tgt_spec{1}(2).name = 'strtype';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).tgt_spec{1}(2).value = 'e';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).sname = 'fMRI model specification: SPM.mat File';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).src_exbranch = substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1});
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1).src_output = substruct('.','spmmat');
    matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

    batchname = [ 'level1_'  subjects{s} suffix '.mat' ] 
    save(batchname,'matlabbatch')
    jobs{s} = batchname;
        
end

spm_jobman('serial', jobs, '', {});


