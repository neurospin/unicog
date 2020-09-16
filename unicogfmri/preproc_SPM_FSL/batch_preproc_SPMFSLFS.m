
% batch for MRI preprocessing based on a combination of SPM and FSL and Freesurfer

% it assumes that single band reference images (SBref) have been saved in addition to the normal EPI volumes for each run 
% because of their enhanced signal and grey white matter contrast, SBref images are used for distortion correction (FSL topup) and coregistration (Freesurfer boundary based registration) 

% preprocessing steps: 
% - bias correction of anatomical image (SPM)
% - surface extraction of anatomical image (Freesurfer)
% - realignment of fmri images, high quality, wrt. first image, for epi runs and SBref images (SPM)
% - coregistration of meanSBref to meanepi (SPM)
% - coregistration of SBref_AP to meanSBref - applied to SBref PA (SPM)
% - estimation of distortion correction parameters from SBref images with two opposite phase encoding directions (FSL)
% - application of distortion correction to mean SBref and epi runs (FSL)
% - boundary based registration of meanSBref image to anatomy, application to urepi headers without resampling (Freesurfer)
% - surface-constrained smoothing (Freesurfer)

%  ee., 12/03/2019

subjects = [1:18];

% input data and parameters
% =========================================================================
% locate the data
spm_path         = '/i2bm/local/spm12-7487';
datadir          = '/neurospin/unicog/protocols/IRMf/...';
regexp_func      = '^epi_sess.*\.nii';                  % regular expression to recognize functional sessions  
regexp_meanfunc  = '^meanepi_sess.*\.nii';              % regular expression to recognize mean functional image
regexp_sbref	 = '^SBref_sess.*\.nii';		% regular expression to recognize single band reference images of the functional sessions
regexp_meansbref = '^meanSBref_sess.*\.nii';		% regular expression to recognize the mean single band reference image
regexp_anat      = '^anat.*\.nii';                   	% regular expression to recognize T1
regexp_AP  	 = '^SBref_AP.*\.nii';           	% regular expression to recognize the referce volumes for undistortion
regexp_PA  	 = '^SBref_PA.*\.nii';           	% regular expression to recognize the referce volumes for undistortion
funcdir          = 'fmri/acquisition1';                 % path of fMRI data (4D nifti) within subject directory
anatdir          = 't1mri/acquisition1';                % path of anatomical image within subject directory

% acquisition parameters
resolution	 = 1.5;
matrix		 = 130;
grappa		 = 2;
echo_spacing	 = 0.00064;
phase_encoding	 = 'AP'; % 'LR, 'AP'

smooth_fwhm_surfvol = 2;

% initialize spm
% =========================================================================
addpath(spm_path)
spm('defaults', 'FMRI');
spm_jobman('initcfg');

% initialise freesurfer
% ===========================================================================
bash_path = getenv('PATH')
setenv('PATH',[bash_path,':/i2bm/local/freesurfer',':/i2bm/local/freesurfer/bin',':/i2bm/local/freesurfer/mni/bin/']);
setenv('SUBJECTS_DIR','/neurospin/unicog/protocols/IRMf/.../mri_surface');
setenv('FREESURFER_HOME','/i2bm/local/freesurfer');
setenv('PERL5LIB','/i2bm/local/freesurfer/mni/share/perl5');


for s = 1:length(subjects)

	iSub = subjects(s);

	% Get the data files
	% =========================================================================

	% Get subject directory (with anat & fMRI)
	subjdir = sprintf('%s/mri_volume/sub%02d/', datadir, iSub);

	% Get anatomical image
	adir =  sprintf('%s/%s/', subjdir, anatdir);
	anatfile = spm_select('FPList', adir, regexp_anat);
	if isequal(anatfile,  '')
	    warning(sprintf('No anat file found for subject %s', ...
		num2str(iSub)))
	    return
	end	

	% Get functional files to analyze
	fdir =  sprintf('%s%s/', subjdir, funcdir);
	ffiles = spm_select('List', fdir, regexp_func);
	nrun = size(ffiles,1);
	if nrun == 0
	    warning(sprintf('No functional file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	funcfiles = cell(nrun, 1);
	cffiles = cellstr(ffiles);
	for irun = 1:nrun
	    funcfiles{irun} = cellstr(spm_select('ExtFPList', fdir, ['^', cffiles{irun}], Inf));
	end

	% get SBref images of functional sessions
	sbfiles = spm_select('List', fdir, regexp_sbref);
	nrun = size(sbfiles,1);
	if nrun == 0
	    warning(sprintf('No SBref file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	csbfiles = cellstr(sbfiles);
	for irun = 1:nrun
	    sbreffiles{irun} = cellstr(spm_select('ExtFPList', fdir, ['^', csbfiles{irun}], Inf));
	end

	

	% ONE SPM batch for bias correction of anatomical images (using SPM segment)
	% =========================================================================

	clear matlabbatch;
	stage = 0;
	stage = stage + 1;
	stage_segmentation = stage;

	matlabbatch{stage_segmentation}.spm.spatial.preproc.channel.vols = { anatfile };
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.write = [1 1];
	matlabbatch{stage_segmentation}.spm.spatial.preproc.channel.biasreg = 0.001;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.channel.biasfwhm = 60;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.channel.write = [0 1];
	ngaus  = [1 1 2 3 4 2];
	native = [1 1 1 0 0 0];
	for c = 1:6 % tissue class c
	    matlabbatch{stage_segmentation}.spm.spatial.preproc.tissue(c).tpm = {fullfile(spm('dir'), 'tpm', sprintf('TPM.nii,%d', c))};
	    matlabbatch{stage_segmentation}.spm.spatial.preproc.tissue(c).ngaus = ngaus(c);
	    matlabbatch{stage_segmentation}.spm.spatial.preproc.tissue(c).native = [native(c) 0];
	    matlabbatch{stage_segmentation}.spm.spatial.preproc.tissue(c).warped = [0 0];
	end
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.mrf = 1;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.cleanup = 1;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.affreg = 'mni';
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.fwhm = 0;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.samp = 3;
	matlabbatch{stage_segmentation}.spm.spatial.preproc.warp.write = [0 0];


	matfile = sprintf('%s/batch/preproc/batch_segment_preproc6_SPMFSLFS_sub%02.0f.mat', datadir, iSub);
	if exist(matfile) 
	    delete(matfile); fprintf('\nremove previous batch\n')
	end
	fprintf('\n Writing SPM batch for subject %d:', iSub)
	fprintf('\n %s\n', matfile)
	save(matfile,'matlabbatch');

	jobs = matfile;
	spm_jobman('serial', jobs, '', {});


	% FREESURFER SURFACE EXTRACTION
	% =========================================================================

	% copy bias corrected anatomy (manat) to surface folder

	anatfile = spm_select('List', adir, regexp_anat);
	cmd = sprintf('cp %s/m%s $SUBJECTS_DIR/sub%02d.nii', adir, anatfile, iSub);
	unix(cmd);

	% run recon-all on it
	cmd = sprintf('recon-all -i $SUBJECTS_DIR/sub%02d.nii -s sub%02d -all', iSub, iSub);
	unix(cmd);


	% ONE SPM batch to Realign the functional images and the SBref images
	% =========================================================================

	clear matlabbatch;
	stage = 0;

	stage = stage + 1;
	stage_realign1 = stage;

	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.data = funcfiles;

	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.quality = 1;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.sep = resolution;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.fwhm = 2;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.rtm = 0;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.interp = 4;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.wrap = [0 1 0];
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.eoptions.weight = '';
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.roptions.which = [2 1];
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.roptions.interp = 6;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.roptions.wrap = [0 1 0];
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.roptions.mask = 1;
	matlabbatch{stage_realign1}.spm.spatial.realign.estwrite.roptions.prefix = 'r';

	stage = stage + 1;
	stage_realign2 = stage;

	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.data = sbreffiles;

	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.quality = 1;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.sep = resolution;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.fwhm = 2;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.rtm = 0;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.interp = 4;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.wrap = [0 1 0];
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.eoptions.weight = '';
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.roptions.which = [2 1];
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.roptions.interp = 6;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.roptions.wrap = [0 1 0];
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.roptions.mask = 1;
	matlabbatch{stage_realign2}.spm.spatial.realign.estwrite.roptions.prefix = 'r';


	matfile = sprintf('%s/batch/preproc/batch_realign_preproc6_SPMFSLFS_sub%02.0f.mat', datadir, iSub);
	if exist(matfile) 
	    delete(matfile); fprintf('\nremove previous batch\n')
	end
	fprintf('\n Writing SPM batch for subject %d:', iSub)
	fprintf('\n %s\n', matfile)
	save(matfile,'matlabbatch');

	jobs = matfile;
	spm_jobman('serial', jobs, '', {});


	% ONE SPM batch for coregistration: 
	% =========================================================================

	% Get subject directory (with anat & fMRI)
	subjdir = sprintf('%s/mri_volume/sub%02d/', datadir, iSub);		

	% Get mean functional files to analyze
	fdir =  sprintf('%s%s/', subjdir, funcdir);
	ffile = spm_select('FPList', fdir, regexp_meanfunc);
	nrun = size(ffile,1);
	if nrun == 0
	    warning(sprintf('No mean functional file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	% get mean SBref image
	sbfile = spm_select('FPList', fdir, regexp_meansbref);
	nrun = size(sbfile,1);
	if nrun == 0
	    warning(sprintf('No mean SBref file found for subject %s', ...
		num2str(iSub)))
	    return
	end


	% Get AP and PA SBref images to analyse
	refdir =  sprintf('%s%s/', subjdir, funcdir);
	APfile = spm_select('FPList', refdir, regexp_AP);
	if isequal(APfile,  '')
	    warning(sprintf('No AP file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	PAfile = spm_select('FPList', refdir, regexp_PA);
	if isequal(PAfile,  '')
	    warning(sprintf('No PA file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	% meanSBref_sess to meanepi_sess
	% ========================================================================================

	clear matlabbatch;
	stage = 0;


	for irun = 1:nrun
		stage = stage + 1;
		stage_coregister1 = stage;

		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.ref(1) = {ffile}; % meanepi			
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.source(1) = {sbfile}; % meanSBref
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.other = {''};
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.eoptions.tol = ...
		    [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.roptions.interp = 6;
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.roptions.mask = 0;
		matlabbatch{stage_coregister1}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';

	    	sessdep_coregister1(irun) = ...
		cfg_dep('Coregister: Estimate & Reslice: Coregistered Images', ...
			substruct('.','val', '{}',{stage_coregister1}, '.','val', '{}',{1}, '.','val', '{}',{1}), ...
			substruct('.','cfiles'));
	end


	%  SBref_AP to meanSBref
	% =========================================================================

	stage = stage + 1;
	stage_coregister2 = stage;

	for irun = 1:nrun
		matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.ref(1) = sessdep_coregister1(1); % meanSBref		
		matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.source(1) = {APfile}; % SBref_AP
		matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.other = {PAfile}; % SBref_PA
	end

	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.eoptions.tol = ...
	    [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.roptions.interp = 6;
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.roptions.mask = 0;
	matlabbatch{stage_coregister2}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';


	matfile = sprintf('%s/batch/preproc/batch_coregister_preproc6_SPMFSLFS_sub%02.0f.mat', datadir, iSub);
	if exist(matfile) 
	    delete(matfile); fprintf('\nremove previous batch\n')
	end
	fprintf('\n Writing SPM batch for subject %d:', iSub)
	fprintf('\n %s\n', matfile)
	save(matfile,'matlabbatch');

	jobs = matfile;
	spm_jobman('serial', jobs, '', {});


	
	% FSL PROCESSING
	% ============================================================================================

    	% Get AP and PA SBref images
	refdir =  sprintf('%s%s/', subjdir, funcdir);
	APfile = spm_select('List', refdir, regexp_AP);
	if isequal(APfile,  '')
	    warning(sprintf('No AP file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	PAfile = spm_select('List', refdir, regexp_PA);
	if isequal(PAfile,  '')
	    warning(sprintf('No PA file found for subject %s', ...
		num2str(iSub)))
	    return
	end

	% Get mean SBref
	sbfile = spm_select('List', fdir, regexp_meansbref);
	nrun = size(sbfile,1);
	if nrun == 0
	    warning(sprintf('No mean SBref file found for subject %s', ...
		num2str(iSub)))
	    return
	end

    
	% ESTIMATION OF TOPUP PARAMETERS
	% ==========================================================================

	% Merge the AP & PA nii files in the same file
	cmd = sprintf('cd %s; fsl5.0-fslmerge -t b0_APPA %s %s', ...
	     fdir, ['r' APfile(1:end-4)], ['r' PAfile(1:end-4)]); 
	call_fsl(cmd)

	% Create a text file with the direction of phase encoding. 
	% A>P is -1; P>A is 1 
	TotRoEPI_sec = (matrix./grappa-1).*echo_spacing;
	if phase_encoding == 'AP'
		cmd = sprintf('cd %s; echo $''0 -1 0 %6.5f \n0 1 0 %6.5f'' > acq_param.txt', fdir, TotRoEPI_sec, TotRoEPI_sec);
	elseif phase_encoding == 'LR'
		cmd = sprintf('cd %s; echo $''-1 0 0 %6.5f \n1 0 0 %6.5f'' > acq_param.txt', fdir, TotRoEPI_sec, TotRoEPI_sec);	
	end
	unix(cmd)

	% Compute deformation with Topup, the result that will be used is APPA_DefMap
	% For sanity checks, sanitycheck_DefMap is the deformation field and sanitycheck_unwarped_B0 are the corrected images
	fprintf('\n Compute the APPA deformation with Topup')
	cmd = sprintf(['cd %s; fsl5.0-topup ', ...
	    '--imain=b0_APPA --datain=acq_param.txt --config=b02b0.cnf ', ...
	    '--out=APPA_DefMap --fout=sanitycheck_DefMap --iout=sanitycheck_unwarped_B0 --warpres=16,14,12,10,8,6,4,2,2 '], ...
	    fdir);
	call_fsl(cmd)


	% APPLY DISTORTION CORRECTION
	% ============================================================================

	APPA_DefMap = spm_select('List', fdir, '^APPA_DefMap_fieldcoef.nii');

	% apply distortion correction to the mean SBref 
	fprintf('\n Apply the topup correction... SBref: meanSBref')
	cmd = sprintf(['cd %s; fsl5.0-applytopup --imain=%s ', ...
		'--inindex=1 ', ...                                      
		'--topup=APPA_DefMap ' ...
		'--datain=acq_param.txt ', ...
		'--out=%s --method=jac'], ...
		fdir, sbfile(1:end-4), ['u' sbfile(1:end-4)]);
	call_fsl(cmd)

	for iFile = 1:numel(cffiles)

		% apply distortion correction to the rEPI images
		fprintf('\n Apply the topup correction... Sess: %d', iFile)
		cmd = sprintf(['cd %s; fsl5.0-applytopup --imain=%s ', ...
			'--inindex=1 ', ...                                      
			'--topup=APPA_DefMap ', ...
			'--datain=acq_param.txt ', ...
			'--out=%s --method=jac'], ...
			fdir, ['r' cffiles{iFile}(1:end-4)], ['ur' cffiles{iFile}(1:end-4)]);
		call_fsl(cmd)

	end

	% FREESURFER PROCESSING
	% =========================================================================================================
	
	% BOUNDARY BASED REGISTRATION OF FUNCTIONAL DATA TO ANATOMY
	% ================================================================================================	

	% estimate coregistration parameters from meanSBref
	fprintf('\n Estimating BBR parameters ... meanSBref ')
	cmd = sprintf(['cd %s; bbregister --s sub%02d ', ...
		'--mov %s ', ...                                     
		'--init-header --bold ' ...
		'--reg %s ', ...
		'--o %s'], ...
		fdir, iSub, ['u' sbfile], ['bbru' sbfile(1:end-4) '.dat'], ['bbru' sbfile]);
	unix(cmd)
	
	for iFile = 1:numel(cffiles)	

		% apply transformations to epi sessions	(written to header without resampling)	
		fprintf('\n Applying BBR ... Sess:%d ', iFile)
		cmd = sprintf(['cd %s; mri_vol2vol --fstarg ', ...
			'--mov %s ', ...                                     
			'--no-resample ' ...
			'--reg %s ', ...
			'--o %s'], ...
			fdir, ['ur' cffiles{iFile}], ['bbru' sbfile(1:end-4) '.dat'], ['bbrur' cffiles{iFile}]);
		unix(cmd)
	end	
    
	% SURFACE CONSTRAINED SMOOTHING OF FUNCTIONAL DATA
	% ==========================================================================================================

	fprintf('\n Smoothing constrained by surface ... ')

	for iFile = 1:numel(cffiles)
		fprintf('\n Sess:%d ', iFile)
		cmd = sprintf(['cd %s; mris_volsmooth --i %s --o %s --reg %s --projfrac-avg 0 1 0.2 --vol-fwhm %d'],...
		    fdir, ['bbrur' cffiles{iFile}], ['surfsbbrur' cffiles{iFile}], ['bbru' sbfile(1:end-4) '.dat'], smooth_fwhm_surfvol);
		unix(cmd)
	end

end
























