%%%% generic function for declaring the structure of a group analysis

%%%% give the number of subject groups
ngroups=1;

%%%% name the groups of subjects 
%groupn = {'anova_new'};  
groupn = {'all'};  

subjects = { 'AB120569', 'AB130058', 'AD130144', 'AD130195', 'BP120556', ...
             'CB130170', 'CT120531', 'EH120568', 'EJ130127', 'LL130202', ...
             'MD130210', 'NF130330', 'NM120471', 'OC120573', 'PD130222', ...
             'PG130069', 'PL130014', 'PL130312', 'PM120407', 'VA130085' };

nsub = size(subjects, 2);
totsub = size(subjects, 2);


%% then with the full path
rootdir = '/neurospin/unicog/protocols/IRMf/complexityLSF_MorenoPallier_2012/spm8/Subjects';

modeldir = '/analyses/clsf';


for i=1:totsub
    subjectsdir{i} = fullfile(rootdir, subjects{i}, modeldir);
end
