function lcogn_single_firstlevel(params,todo)
% Create an SPM5 job for single subject first level analysis
%
% PARAMETERS = structure with fields:
%   o rootdir:   Absolute path of the study
%   o subjects:  Cell array of subjects name (that matches folders name)
%   o funcdirs:  Cell array of strings, each string being a relative path 
%                containing functional scans of a session
%   o funcwc:    Wildcard for functional scans (regular expression)
%   o rpwc:      Wildcard for realignment parameters (regular expression)
%   o modelname: Name of the model (matches a directory in 'stats')
%   o TR:        Repetition time
%   o HF_cut:    High-pass filter cutoff (in seconds)
%   o bases:     Basis functions, being one of these structures:
%                   Canonical => struct('type','hrf'); with 'hrf' | 'hrf+deriv' | 'hrf+2derivs'
%                   FIR => struct('type','fir','length',XXX,'order',XXX);
%                   Fourier => struct('type','fourier','length',XXX,'order',XXX);
%   o rp:        Realignment parameters as covariates (1|0)
%   o report:    Parameters for results report, as a structure with
%                threshold type ('FWE' | 'FDR' | 'none') and threshold (0.05, 0.001, ...):
%                   struct('type','FWE','thresh',0.05);
%   o email:     email address to which results will be sent
%   o logfile:   Filename of the text logfile
%
% TODO = structure with binary fields (1 | 0):
%   o deletefiles:     Delete (all) previous analysis files
%   o specify:         Model specification
%   o estimate:        Model estimation
%   o deletecontrasts: Delete (all) previous contrasts
%   o contrasts:       Contrasts specification and estimation
%   o results:         Results report
%   o run:             Execute batch job
%   o sendmail:        Send results by email
%
% This function calls the two following functions that have to be written
% by the user:
%  o specif_model.m: specification of the paradigm timing
%  o specif_contrasts.m: specification of the contrasts

%-Parameters checking
%----------------------------------------------------------------------
error(nargchk(2,2,nargin));

fields = fieldnames(params);
valid_fields = {'rootdir', 'funcdirs', 'funcwc', 'rpwc', 'TR', 'HF_cut', ...
    'bases', 'rp', 'report', 'email', 'logfile'};
fielddiff = setdiff(fields,valid_fields);
if ~isempty(fielddiff)
    error('Unknown parameters: %s',sprintf('%s  ',fielddiff{:}));
end
fielddiff = setdiff(valid_fields,fields);
if ~isempty(fielddiff)
    error('Mandatory parameters: %s',sprintf('%s  ',fielddiff{:}));
end

fields = fieldnames(todo);
valid_fields = {'deletefiles','specify','estimate','deletecontrasts','contrasts','results','sendmail','run'};
if ~isempty(setxor(fields,valid_fields))
    error('Invalid todo list.');
end

%wd = pwd; %DEL%
rootdir = params.rootdir;
%cd(rootdir); %DEL%

logfile = fullfile(rootdir,params.logfile);

logmsg(logfile,sprintf('First level analysis in folder %s...',rootdir));

spm_select('clearvfiles');  

%-Get functional scans and realignment parameters file, for each session
%-----------------------------------------------------------------------
logmsg(logfile,'Scanning for functional scans...');
for n=1:length(params.funcdirs)
%    params.funcdirs{n} = spm_select('CPath',fullfile('..','..',params.funcdirs{n}),rootdir);
%    params.funcdirs{n} = spm_select('CPath',fullfile('..',''),rootdir);
%    params.funcdirs{n} = spm_select('CPath',fullfile('..','..','..','..',params.funcdirs{n}),rootdir);
    params.funcdirs{n} = spm_select('CPath',fullfile(rootdir,'..','..',params.funcdirs{n}));
    f = spm_select('List',params.funcdirs{n},params.funcwc);
    files{n} = [repmat(spm_select('CPath','',params.funcdirs{n}),size(f,1),1), f];
	f = spm_select('List',params.funcdirs{n},params.rpwc);
    rp{n} = fullfile(spm_select('CPath','',params.funcdirs{n}),f);
    if params.rp && isempty(f)
        logmsg(logfile,'*** Realignment parameters cannot be found: option discarted ***');
        params.rp = 0;
    end
end
logmsg(logfile,sprintf('  found %d files in %d session(s) ',sum(cellfun('size',files,1)),length(files)));
for n=1:length(params.funcdirs)
    logmsg(logfile,sprintf('    with %d files in session %s',size(files{n},1),params.funcdirs{n}));
end

%- Jobs definition
%----------------------------------------------------------------------
jobs = {};
nbjobs = 0;

%- Delete previous SPM.mat
%----------------------------------------------------------------------
if todo.deletefiles
    logmsg(logfile,'Deleting previous analysis...');
    fls = {'^SPM.mat$','^mask\..{3}$','^ResMS\..{3}$','^RPV\..{3}$',...
        '^beta_.{4}\..{3}$','^con_.{4}\..{3}$','^ResI_.{4}\..{3}$',...
        '^ess_.{4}\..{3}$', '^spm\w{1}_.{4}\..{3}$'};

    for i=1:length(fls)
        j = spm_select('List',rootdir,fls{i});
        for k=1:size(j,1)
            spm_unlink(fullfile(rootdir,deblank(j(k,:))));
        end
    end
else
    if exist(fullfile(rootdir,'SPM.mat'),'file')
        logmsg(logfile,'Stats directory already contains an SPM model!');
    end
end

%- Model specification
%----------------------------------------------------------------------
if todo.specify
    logmsg(logfile,'Model Specification...');
    nbjobs = nbjobs + 1;

    %- Call user-defined function that generates subject-specific variables
    [session,condition,onset,duration] = specif_model(spm_select('CPath',fullfile('..','..'),rootdir));
    if any(diff([numel(session),numel(condition),numel(onset),numel(duration)]))
        error('Invalid number of items in the model specification.');
    end
    
    timing.units   = 'secs';
    timing.RT      = params.TR;
    timing.fmri_t  = 16; % should be the number of slices of the normalized functional scans
    timing.fmri_t0 = 1;  % should correspond to the reference slice chosen during slice timing

    jobs{nbjobs}.stats{1}.fmri_spec.timing = timing;
    jobs{nbjobs}.stats{1}.fmri_spec.dir = cellstr(rootdir);

    switch lower(params.bases.type)
        case 'hrf'
            jobs{nbjobs}.stats{1}.fmri_spec.bases.hrf.derivs = [0 0];
        case 'hrf+deriv'
            jobs{nbjobs}.stats{1}.fmri_spec.bases.hrf.derivs = [1 0];
        case 'hrf+2derivs'
            jobs{nbjobs}.stats{1}.fmri_spec.bases.hrf.derivs = [1 1];
        case 'fir'
            jobs{nbjobs}.stats{1}.fmri_spec.bases.fir = ...
                struct('length',params.bases.length,'order',params.bases.order);
        case 'fourier'
            jobs{nbjobs}.stats{1}.fmri_spec.bases.fourier = ...
                struct('length',params.bases.length,'order',params.bases.order);
        otherwise
            error('Unknown basis function');
    end

    nbsess = length(files);
    logmsg(logfile,sprintf('  There are %d sessions.',nbsess));
    for i=1:nbsess
        jobs{nbjobs}.stats{1}.fmri_spec.sess(i).scans = cellstr(files{i});
        jobs{nbjobs}.stats{1}.fmri_spec.sess(i).hpf = params.HF_cut;
        cond = unique(condition(session==i));
        logmsg(logfile,sprintf('    Session %d contains %d conditions.',i,length(cond)));
        for j=1:length(cond)
            ons = onset(condition==cond(j) & session==i);
            dur = duration(condition==cond(j) & session==i);
            jobs{nbjobs}.stats{1}.fmri_spec.sess(i).cond(j).name = ['sess' num2str(i) '.cond' num2str(cond(j))];
            jobs{nbjobs}.stats{1}.fmri_spec.sess(i).cond(j).onset = ons / 1000;
            jobs{nbjobs}.stats{1}.fmri_spec.sess(i).cond(j).duration = dur / 1000;
        end
        if params.rp
            jobs{nbjobs}.stats{1}.fmri_spec.sess(i).multi_reg = cellstr(rp{i});
        end
    end
end

%- Model estimation
%----------------------------------------------------------------------
if todo.estimate
    logmsg(logfile,'Model Estimation...');
    nbjobs = nbjobs + 1;
    jobs{nbjobs}.stats{1}.fmri_est.spmmat = cellstr(fullfile(rootdir,'SPM.mat'));
end

%- Delete previous contrasts
%----------------------------------------------------------------------
if todo.deletecontrasts
    logmsg(logfile,'Contrasts Deletion...');
    if ~todo.contrasts
        nbjobs = nbjobs + 1;
        jobs{nbjobs}.stats{1}.con.spmmat = cellstr(fullfile(rootdir,'SPM.mat'));
        jobs{nbjobs}.stats{1}.con.delete = 1;
    end
end

%- Contrasts specification
%----------------------------------------------------------------------
if todo.contrasts
    logmsg(logfile,'Contrasts Specifications...');
    nbjobs = nbjobs + 1;
[session,condition,onset,duration] = specif_model(spm_select('CPath',fullfile('..','..'),rootdir));
    %- Call user-defined function that specifies contrasts to be defined
    [names, values] = specif_contrasts(session,condition);
    if numel(names) ~= numel(values)
        error('Different number of "names" and "values" in contrast specification.');
    end

    jobs{nbjobs}.stats{1}.con.spmmat = cellstr(fullfile(rootdir,'SPM.mat'));
    if todo.deletecontrasts
        jobs{nbjobs}.stats{1}.con.delete = 1;
    end
    for i=1:length(names)
        if size(values{i},1) == 1
            jobs{nbjobs}.stats{1}.con.consess{i}.tcon.name = names{i};
            jobs{nbjobs}.stats{1}.con.consess{i}.tcon.convec = values{i};
            %jobs{nbjobs}.stats{1}.con.consess{i}.tcon.sessrep = 'none';
        else
            jobs{nbjobs}.stats{1}.con.consess{i}.fcon.name = names{i};
            for j=1:size(values{i},1)
                jobs{nbjobs}.stats{1}.con.consess{i}.fcon.convec{j} = values{i}(j,:);
            end
            %jobs{nbjobs}.stats{1}.con.consess{i}.fcon.sessrep = 'none';
        end
    end
end

%- Display results
%----------------------------------------------------------------------
if todo.results
    logmsg(logfile,'Display results...');
    nbjobs = nbjobs + 1;

    jobs{nbjobs}.stats{1}.results.spmmat = cellstr(fullfile(rootdir,'SPM.mat'));
    jobs{nbjobs}.stats{1}.results.print  = 1;
    jobs{nbjobs}.stats{1}.results.conspec.title = ''; % determined automatically if empty
    jobs{nbjobs}.stats{1}.results.conspec.contrasts = Inf; % Inf for all contrasts
    jobs{nbjobs}.stats{1}.results.conspec.threshdesc = params.report.type;
    jobs{nbjobs}.stats{1}.results.conspec.thresh = params.report.thresh;
    jobs{nbjobs}.stats{1}.results.conspec.extent = 0;
end

%- Send an email
%----------------------------------------------------------------------
if todo.sendmail
    logmsg(logfile,'Send email...');
    nbjobs = nbjobs + 1;

    jobs{nbjobs}.tools{1}.sendmail.recipient = params.email;
    jobs{nbjobs}.tools{1}.sendmail.subject = '[SPM] [%DATE%] SPM5 Job Manager';
    jobs{nbjobs}.tools{1}.sendmail.message = 'Your SPM5 first level batch has been completed!';
    jobs{nbjobs}.tools{1}.sendmail.attachments = {fullfile(rootdir, ...
        ['spm_' datestr(now,'yyyy') datestr(now,'mmm') datestr(now,'dd') '.ps'])};
    smtp = getpref('Internet','SMTP_Server');
    if isempty(smtp), smtp = 'mx.intra.cea.fr'; end
    jobs{nbjobs}.tools{1}.sendmail.params.smtp = smtp;
    jobs{nbjobs}.tools{1}.sendmail.params.email = params.email;
    jobs{nbjobs}.tools{1}.sendmail.params.zip = 'Yes';
end

%- Save and Run job
%----------------------------------------------------------------------
logmsg(logfile,sprintf('Job batch file saved in %s.',fullfile(rootdir,'jobs_model.mat')));
save(fullfile(rootdir,'jobs_model.mat'),'jobs');
if todo.run
    spm_jobman('run',jobs);
else
    spm_jobman('interactive',jobs);
    spm('show');
end

%cd(wd); %DEL%
