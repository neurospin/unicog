function main(confirm)

% AJOUTER LA LISTE DE TYPES D'IMAGES A TRAITER ET NUMERO D'ACCQUISITION
% PAR EXEMPLE : S'IL Y A 2 T1, OU PLUSIEURS LOCALIZERS...
%
%PROCESS_ANATOMY = 1;
%PROCESS_FUNCTIONAL = 1;
%
%            todo_preproc.slice_timing = 1*PROCESS_FUNCTIONAL;
%            todo_preproc.realign      = 1*PROCESS_FUNCTIONAL;
%            todo_preproc.normalize    = 1*PROCESS_ANATOMY;
%            todo_preproc.coregister   = 1*PROCESS_FUNCTIONAL;
%            todo_preproc.apply_norm   = 1*PROCESS_FUNCTIONAL;
%            todo_preproc.smooth       = 1*PROCESS_FUNCTIONAL;
%            todo_preproc.run          = 1;

%----------------------------------------------------------------------
% TODO LIST (0 = not do; 1 = do)
%----------------------------------------------------------------------
todo_initializations = 1;

todo_clean_old_results = 0; % 0 = do not remove anything, 1 = remove old results
todo_convert_and_remove_dicoms = 0; % 0 = keep them in a "dicom" directory, 1 = remove them
todo_rename = 0;
todo_rename_with_subject_name = 0; % =1 if we want the name of the subject to be includes in file names

todo_preprocessing = 0;
todo_firstlevelprocessing = 1;

% Necessary for the new version of lcogn_single_preproc.m that can do 
% the EPI normalization with respect to a EPI template (this parameter is 
% necessary even if the EPI normalization is not done this way... I know,
% it is a bit absurd)
EPItemplate = '/neurospin/unicog/protocols/IRMf/MainDatabaseLocalizers_PinelMoreno_2008/Tools/template/sym_mean10twinsEPI.img';

todo_smooth_con = 0;
todo_smooth_gmwm = 0;
todo_symmetry = 0;
todo_segm_postproc = 0;
% todo_remove_nan = 0;

%----------------------------------------------------------------------
% GENERAL PARAMETERS
%----------------------------------------------------------------------

data_path = '/my_data_path/Subjects';

list_subjects = {'subj01', 'subj02'}; % ACQUISITION 1

anat_path = 't1mri/acquisition1';

modality = 'fMRI';

list_acquisitions = {'acquisition1'};

list_sessions = {'localizer_1'};

%----------------------------------------------------------------------
% SELECT THE ORIGIN OF THE DATA :
%----------------------------------------------------------------------

% origin_name = '15T_shfj'; % '15T_shfj' (s*)
% study_name = 'localizer_15T_shfj';
% slice_order = 'interleaved_ascending';
% TR = 2.4;

% origin_name = '3T_shfj'; % '3T_shfj' (bru*)
% study_name = 'localizer_3T_shfj';
% slice_order = 'sequential_ascending';
% TR = 2.4;

origin_name = '3T_neurospin'; % '3T_neurospin'
study_name = 'localizer_3T_neurospin';
slice_order = 'sequential_ascending';
TR = 2.4;

% origin_name = '3T_neurospin'; % '3T_neurospin' - IMAGEN
% study_name = 'localizer_3T_neurospin';
% %slice_order = 'interleaved_descending'; % NOOOOOOO !!!!
% slice_order = 'sequential_descending';
% TR = 2.2;

%----------------------------------------------------------------------
% ADAPTED PARAMETERS FOR PREPROCESSING AND FIRST LEVEL:
% TO MODIFY FOR EACH PARTICULAR CASE
%----------------------------------------------------------------------

ref_slice = 1;
voxelsize = [3 3 3];
smoothing = 5;

%----------------------------------------------------------------------
% GENERAL PARAMETERS FOR PREPROCESSING AND FIRST LEVEL:
% DO NOT NEED TO BE MODIFIED
%----------------------------------------------------------------------

anatdir = anat_path;
anatwc  = '^anat.*\.img$';
%modelname = 'stats';


% INITIALIZATIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if todo_initializations
    cd(fullfile(data_path,'../Tools/mfiles'));
    spm5 % and quit
    startup
end


%----------------------------------------------------------------------
% MAIN PROGRAMS (FOR EACH SUBJECT...)
%----------------------------------------------------------------------

for k=1:length(list_subjects)

    sprintf('***** PROCESSING SUBJECT %s *****',list_subjects{k});

    anat_name{k} = sprintf('anat_%s_%s',list_subjects{k},origin_name);
    
    % FOR EACH ACQUISITION
    for mm=1:length(list_acquisitions)

        cd(fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm}));
        
        for m=1:length(list_sessions)
            modelname{m} = sprintf('analysis/stats_%s/',list_sessions{m});
        end


        % REMOVAL OF OLD RESULTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if todo_clean_old_results

            system(sprintf('rm -f %s/*.mat',fullfile(data_path,list_subjects{k})));
            system(sprintf('rm -f %s/*.log',fullfile(data_path,list_subjects{k})));

            system(sprintf('rm -f %s/c*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/GM*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/WM*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/w*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/m*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/*.mat',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/*.minf',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/nobias*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/r*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/hfiltered*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -f %s/flip*',fullfile(data_path,list_subjects{k},anatdir)));
            system(sprintf('rm -rf %s/analysis',fullfile(data_path,list_subjects{k},anatdir)));

            for m=1:length(list_sessions)

                system(sprintf('rm -f %s/a*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/w*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/sw*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/mean*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/A*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/rp*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -rf %s',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},modelname{m})));
                
                system(sprintf('rm -f %s/*.mat',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/*.log',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));
                system(sprintf('rm -f %s/spm_*',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));

                system(sprintf('rm -rf %s/stats',fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m})));

            end

        end


        % CREATION OF OUTPUT DIRECTORY (FOR STATS AND .ps FILES) %%%%%%%%%%

        for m=1:length(list_sessions)

            wd = fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm});

            disp(sprintf('Creating new output directory "%s".',modelname{m}));
            mkdir(wd,modelname{m});

        end


        % CONVERSION OF ALL THE IMAGES FROM DICOM TO NIFTI FORMAT %%%%%%%%%

        % Recursively import DICOM data into NIfTI format
        % Inspired from code by Guillaume Flandin, 2007, Copyright (c) INSERM U562

        if todo_convert_and_remove_dicoms

            sub_dicom_import(fullfile(data_path,list_subjects{k},anatdir),todo_convert_and_remove_dicoms);

            for m=1:length(list_sessions)

                wd = fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},list_sessions{m});
                sub_dicom_import(wd,todo_convert_and_remove_dicoms);

            end

        end

        
        % RENAME FILES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if todo_rename
            for m=1:length(list_sessions)
                session_path = fullfile(modality,list_acquisitions{mm},list_sessions{m});
                if todo_rename_with_subject_name
                    study_name_bis = strcat(study_name,'_',list_subjects{k},'_',list_acquisitions{mm},'_',list_sessions{m});
                    rename_files(data_path, list_subjects{k}, anat_path, anat_name{k}, session_path, study_name_bis, origin_name);
                else
                    rename_files(data_path, list_subjects{k}, anat_path, anat_name{k}, session_path, study_name, origin_name);
                end
            end
        end


        % EXECUTION OF THE PREPROCESSING BATCH %%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % THE APPROPRIATE PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if todo_preprocessing

            %- List of tasks to be performed
            if ~nargin
                todo_preproc.slice_timing = 1;
                todo_preproc.realign      = 1;
                todo_preproc.normalize    = 1;
                todo_preproc.normalizeOnEPI = 0;
                todo_preproc.coregister   = 1;
                todo_preproc.apply_norm   = 1;
                todo_preproc.smooth       = 1;
                todo_preproc.run          = 1;
            else
                todo_preproc.slice_timing = ask('yes','Apply slice timing');
                todo_preproc.realign      = ask('yes','Realign functional images');
                todo_preproc.normalize    = ask('yes','Compute normalization for anat');
                todo_preproc.normalizeOnEPI = ask('yes','Compute normalization of EPI on an EPI template');
                todo_preproc.coregister   = ask('yes','Coregister anat onto target functional image');
                todo_preproc.apply_norm   = ask('yes','Apply normalization to functional images');
                todo_preproc.smooth       = ask('yes','Smooth functional images');
                todo_preproc.run          = ask('yes','Run Batch');
            end

            % PARTICULAR PARAMETERS
            for m=1:length(list_sessions)
                params_preproc.funcdirs{m} = fullfile(modality,list_acquisitions{mm},list_sessions{m});
            end

            params_preproc.anatdir = anatdir;
            params_preproc.anatwc  = anatwc;
            params_preproc.TR = TR;
            params_preproc.ref_slice = ref_slice;
            params_preproc.slice_order = slice_order;
            params_preproc.voxelsize = voxelsize;
            params_preproc.smoothing = smoothing;
            params_preproc.EPItemplate = EPItemplate;

            params_preproc.funcwc  = '^.*\.img$';
            params_preproc.logfile = 'preproc.log';

            % EXECUTION
            p = params_preproc;
            p.rootdir = fullfile(data_path,list_subjects{k});
            p.funcdirs = params_preproc.funcdirs;
            cd(fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm}));
            lcogn_single_preproc(p,todo_preproc);

            % APPLICATION OF THE NORMALIZATION TO THE GREY AND WHITE MATTERS
            % SEGMENTED

            anat_name_temp_img = spm_select('List', fullfile(data_path,list_subjects{k},anatdir), anatwc);
            [dirdir,anat_name_temp,niu,niu] = fileparts(anat_name_temp_img);

            matrice_path = fullfile(data_path,list_subjects{k},anat_path);
            matrice_name = sprintf('%s/%s%s',matrice_path,anat_name_temp,'_seg_sn.mat');
            matrice = load(matrice_name);
            cd(matrice_path);

            ligne=sprintf('!mv c1%s.img GM_%s.img',anat_name_temp,anat_name_temp);
            eval(ligne)
            ligne=sprintf('!mv c1%s.hdr GM_%s.hdr',anat_name_temp,anat_name_temp);
            eval(ligne)

            ligne=sprintf('!mv c2%s.img WM_%s.img',anat_name_temp,anat_name_temp);
            eval(ligne)
            ligne=sprintf('!mv c2%s.hdr WM_%s.hdr',anat_name_temp,anat_name_temp);
            eval(ligne)

            name_c1 = sprintf('GM_%s.img',anat_name_temp);
            name_c2 = sprintf('WM_%s.img',anat_name_temp);
            spm_write_sn(name_c1,matrice);
            spm_write_sn(name_c2,matrice);

        end


        % EXECUTION OF THE FIRST LEVEL (LOCALIZER) BATCH WITH %%%%%%%%%%%%%
        % THE APPROPRIATE PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if todo_firstlevelprocessing

            %- List of tasks to be performed
            if ~nargin
                todo_firstlevel.deletefiles     = 1;
                todo_firstlevel.specify         = 1;
                todo_firstlevel.estimate        = 1;
                todo_firstlevel.deletecontrasts = 1;
                todo_firstlevel.contrasts       = 1;
                todo_firstlevel.results         = 0;
                todo_firstlevel.sendmail        = 0;
                todo_firstlevel.run             = 1;
            else
                todo_firstlevel.deletefiles     = ask('yes','Delete previous SPM model');
                todo_firstlevel.specify         = ask('yes','Specify first level model');
                todo_firstlevel.estimate        = ask('yes','Estimate first level model');
                todo_firstlevel.deletecontrasts = ask('yes','Delete previous contrasts');
                todo_firstlevel.contrasts       = ask('yes','Specify and estimate contrasts');
                todo_firstlevel.results         = ask('yes','Display results');
                todo_firstlevel.sendmail        = ask('yes','Send results by email');
                todo_firstlevel.run             = ask('yes','Run Batch');

            end

            % PARTICULAR PARAMETERS
            for m=1:length(list_sessions)
                params_firstlevel.funcdirs{m} = list_sessions{m};
            end

            params_firstlevel.TR = TR;
            params_firstlevel.funcwc = '^swa.*\.img$';
            params_firstlevel.rpwc   = '^rp.*\.txt$';
            params_firstlevel.HF_cut = 128;
            params_firstlevel.bases = struct('type','hrf+deriv');
            params_firstlevel.rp = 0;
            %params_firstlevel.rp = 1; % Changé pour voir l'effet du mouvement
            params_firstlevel.report = struct('type','none', 'thresh',0.001);
            params_firstlevel.email = 'firstname.lastname@cea.fr';
            params_firstlevel.logfile = 'firstlevel.log';

            % EXECUTION
            p = params_firstlevel;
            for m=1:length(list_sessions)
                wd = fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm});
                p.rootdir = fullfile(wd,modelname{m});
                p.funcdirs = params_firstlevel.funcdirs;
                cd(fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm}));
                lcogn_single_firstlevel(p,todo_firstlevel);
            end
            close all hidden
        end

        
        % SMOOTH THE CONTRASTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if todo_smooth_con

            jobs_smooth = {};
            nbjobs_smooth = 0;
            logfile_consmooth = fullfile(data_path,list_subjects{k},'con_smooth.log');
            
            con_smoothing = smoothing;
            conwc  = '^con.*\.img$';
            
            logmsg(logfile_consmooth,'Scanning for contrast files...');
            con_images = cellstr(spm_select('List', fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},modelname{m}), conwc));
            
            for n=1:length(con_images)
                con_images{n} = fullfile(data_path,list_subjects{k},modality,list_acquisitions{mm},modelname{m},con_images{n});
            end
            
            logmsg(logfile_consmooth,sprintf('Smoothing %d files ("%s"...) with fwhm = %d mm',sum(cellfun('size',con_images,1)),con_images{1}(1,:),con_smoothing));
            nbjobs_smooth = nbjobs_smooth + 1;
            jobs_smooth{nbjobs_smooth}.spatial{1}.smooth.data = cellstr(strvcat(con_images));
            jobs_smooth{nbjobs_smooth}.spatial{1}.smooth.fwhm = con_smoothing;

            logmsg(logfile_consmooth,sprintf('Job batch file saved in %s.',fullfile(data_path,list_subjects{k},'jobs_con_smooth.mat')));
            save(fullfile(data_path,list_subjects{k},'jobs_con_smooth.mat'),'jobs_smooth');
            spm_jobman('run',jobs_smooth);

        end


        % SMOOTH GREY AND WHITE MATTER SEGMENTATIONS %%%%%%%%%%%%%%%%%%%%%%
        if todo_smooth_gmwm
            
            logfile_gmwmsmooth = fullfile(data_path,list_subjects{k},'gmwm_smooth.log');
            gmwm_smoothing = 3;
            
            % Grey matter
            
            jobs_gmwmsmooth = {};
            nbjobs_gmwmsmooth = 0;
                        
            gmwmwc  = '^wGM.*\.img$';
            
            logmsg(logfile_gmwmsmooth,'Scanning for grey matter files...');
            gmwm_images = cellstr(spm_select('List', fullfile(data_path,list_subjects{k},anatdir), gmwmwc));
            
            for n=1:length(gmwm_images)
                gmwm_images{n} = fullfile(data_path,list_subjects{k},anatdir,gmwm_images{n});
            end
            
            logmsg(logfile_gmwmsmooth,sprintf('Smoothing %d files ("%s"...) with fwhm = %d mm',sum(cellfun('size',gmwm_images,1)),gmwm_images{1}(1,:),gmwm_smoothing));
            nbjobs_gmwmsmooth = nbjobs_gmwmsmooth + 1;
            jobs_gmwmsmooth{nbjobs_gmwmsmooth}.spatial{1}.smooth.data = cellstr(strvcat(gmwm_images));
            jobs_gmwmsmooth{nbjobs_gmwmsmooth}.spatial{1}.smooth.fwhm = gmwm_smoothing;

            logmsg(logfile_gmwmsmooth,sprintf('Job batch file saved in %s.',fullfile(data_path,list_subjects{k},'jobs_gmwm_smooth.mat')));
            save(fullfile(data_path,list_subjects{k},'jobs_gmwm_smooth.mat'),'jobs_gmwmsmooth');
            spm_jobman('run',jobs_gmwmsmooth);

            % White matter
            
            jobs_gmwmsmooth = {};
            nbjobs_gmwmsmooth = 0;
                        
            gmwmwc  = '^wWM.*\.img$';
            
            logmsg(logfile_gmwmsmooth,'Scanning for white matter files...');
            gmwm_images = cellstr(spm_select('List', fullfile(data_path,list_subjects{k},anatdir), gmwmwc));
            
            for n=1:length(gmwm_images)
                gmwm_images{n} = fullfile(data_path,list_subjects{k},anatdir,gmwm_images{n});
            end
            
            logmsg(logfile_gmwmsmooth,sprintf('Smoothing %d files ("%s"...) with fwhm = %d mm',sum(cellfun('size',gmwm_images,1)),gmwm_images{1}(1,:),gmwm_smoothing));
            nbjobs_gmwmsmooth = nbjobs_gmwmsmooth + 1;
            jobs_gmwmsmooth{nbjobs_gmwmsmooth}.spatial{1}.smooth.data = cellstr(strvcat(gmwm_images));
            jobs_gmwmsmooth{nbjobs_gmwmsmooth}.spatial{1}.smooth.fwhm = gmwm_smoothing;

            logmsg(logfile_gmwmsmooth,sprintf('Job batch file saved in %s.',fullfile(data_path,list_subjects{k},'jobs_gmwm_smooth.mat')));
            save(fullfile(data_path,list_subjects{k},'jobs_gmwm_smooth.mat'),'jobs_gmwmsmooth');
            spm_jobman('run',jobs_gmwmsmooth);
            
        end


        % SYMMETRY COMPUTATION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if todo_symmetry
            finalstats_path = fullfile(modality,list_acquisitions{mm},modelname{m});
            anat_name_temp_img = spm_select('List', fullfile(data_path,list_subjects{k},anatdir), anatwc);
            [dirdir,anat_name_temp,niu,niu] = fileparts(anat_name_temp_img);
            symmetry_process(data_path, list_subjects{k}, list_sessions, anat_path, anat_name_temp, finalstats_path);
        end
        
    end

    % SEGMENTATION POST-PROCESSING RE-ORGANIZATION %%%%%%%%%%%%%%%%%%%%
    if todo_segm_postproc
%         anat_name_temp_img = spm_select('List', fullfile(data_path,list_subjects{k},anatdir), anatwc);
%         [dirdir,anat_name_temp,niu,niu] = fileparts(anat_name_temp_img);
%         segmentation_process(data_path, list_subjects{k}, anat_path, anat_name_temp);

        anat_completepath = fullfile(data_path,list_subjects{k},anatdir);
        cd(anat_completepath);

        % Creation of directories
        mkdir('analysis');
        mkdir('analysis/spm_segmentation');

        % Move the grey matter and white matter images to the
        % "spm_segmentation" directory
        ligne=sprintf('!mv *GM* analysis/spm_segmentation/');
        eval(ligne)

        ligne=sprintf('!mv *WM* analysis/spm_segmentation/');
        eval(ligne)

    end

    % NAN REMOVAL ON FINAL IMAGES (TO AVOID %%%%%%%%%%%%%%%%%%%%%%%%%%%
    % IMPORTATION PROBLEMS WITH BRAINVISA) %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     if todo_remove_nan
% 
%         anat_completepath = fullfile(data_path,list_subjects{k},anatdir);
%         cd(anat_completepath);
% 
%         normalized_anat = '^wmanat.*\.img$';
%         anat_name_temp_img = spm_select('List', fullfile(data_path,list_subjects{k},anatdir), normalized_anat);
%         [dirdir,anat_name_temp,niu,niu] = fileparts(anat_name_temp_img(1,:));
%             
%         % Remove the "nan" on the image and save the resulting image with
%         % the same name plus "_nonan"
%         ligne=sprintf('!AimsRemoveNaN -i %s.img -o %s_nonan.img',anat_name_temp, anat_name_temp);
%         eval(ligne)
% 
%     end



end
