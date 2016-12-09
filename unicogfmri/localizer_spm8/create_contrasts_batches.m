%-----------------------------------------------------------------------
% Job configuration created by cfg_util (rev $Rev: 4252 $)
%-----------------------------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% experiment-specific parameters

root = '/my_data_path/Subjects';

[subjects acq] = textread(fullfile(root,'dirs.txt'),'%s %d');

option = 'localizer'; 
suffix = '_hrf'; 

output_dir = 'analyses/hrf'; % path where the SPM.mat will be created, within each subjects' dir
%onsets_dir = 'onsets';

sessrep_value = 'none';
%sessrep_value = 'replsc';
%sessrep_value = 'repl';

% End of configuration section
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear matlabbatch

% SPECIFICATION OF THE CONTRASTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Call adapted specif_contrasts_*.m file
eval(sprintf('specif_contrasts%s',suffix));

if numel(names) ~= numel(values)
    error('Different number of "names" and "values" in contrast specification.');
end

% CREATION OF BATCH FILES (.MAT) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for s = 1:length(subjects)
    
    rootdir = fullfile(root, subjects{s});
    %funcdir = fullfile('fMRI',sprintf('acquisition%d',acq(s))); % path of fMRI data (4D nifti) within subject directory

    matlabbatch{s}.spm.stats.con.spmmat = cellstr(fullfile(rootdir, output_dir, 'SPM.mat'));
    matlabbatch{s}.spm.stats.con.delete = 1;  %% delete any previous contrasts

    for i=1:length(names)
        if size(values{i},1) == 1
            matlabbatch{s}.spm.stats.con.consess{i}.tcon.name = names{i};
            matlabbatch{s}.spm.stats.con.consess{i}.tcon.convec = values{i};
            matlabbatch{s}.spm.stats.con.consess{i}.tcon.sessrep = sessrep_value;
        else
            matlabbatch{s}.spm.stats.con.consess{i}.fcon.name = names{i};
            for j=1:size(values{i},1)
                matlabbatch{s}.spm.stats.con.consess{i}.fcon.convec{j} = values{i}(j,:);
            end
            matlabbatch{s}.spm.stats.con.consess{i}.fcon.sessrep = sessrep_value;
        end
    end
    
    batchname = ['contrasts_' subjects{s} suffix '.mat'];
    save(fullfile(root,batchname),'matlabbatch')
    jobs{s} = batchname;

end

spm_jobman('serial', jobs, '', {});
