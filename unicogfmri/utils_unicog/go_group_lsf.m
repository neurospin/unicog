%
% Run SPM8 before running this script
%

thisdir = '/neurospin/unicog/protocols/IRMf/MainDatabaseLocalizers_PinelMoreno_2008/tests_version_matlab/stanplot_ROIs_lsf/';

%addpath /neurospin/unicog/protocols/IRMf/complexityLSF_MorenoPallier_2012/spm8/ROIs_analyses/stanplot_ROIs/lsf
addpath(thisdir)
addpath /i2bm/local/spm8/toolbox/marsbar/
addpath /i2bm/local/spm8/toolbox/marsbar/spm5

nruns = 4;
Finterest = 1;
%groupvar = repmat([1  2  3  4  5  6], 1, nruns); % clsf conditions
groupvar = repmat([0  1  2  3  4  0], 1, nruns); % clsf conditions - only c01, c02, c04, c08

timeaxis = -4.8:2.4:19.2; % TR = 2.4
baselinepoints = 2;

cd /neurospin/unicog/protocols/IRMf/complexityLSF_MorenoPallier_2012/spm8/GroupAnalyses_with_smoothing/ANOVA_within_norm/

colors = [ ...
         0         0    1.0000 ; ...
         0    1.0000         0 ; ...
    1.0000         0         0 ; ...
         0    0.7500    0.7500 ; ...
    0.7500         0    0.7500 ; ...
    0.7500    0.7500         0 ...
      ];
colors = [colors ; colors*0.7];  
set(0,'DefaultAxesColorOrder',colors);

% ROIs definition
% rois = { 'IFGorb_roi', 'IFGtri_roi', 'Putamen_roi', ...
%          'TP_roi', 'aSTS_roi', 'pSTS_roi', 'TPJ_roi', ...
%          'Putamen_Caudate_roi', ...
%          'BA_44op_-49_10_4_roi', 'left_MT_roi', 'Occipit_roi', ...
%          'pSTS_biolog_mov_roi', ...
%          'Precentral_Pallier_2011_oky_roi', ...
%          'dmPFC_Pallier_2011_oky_roi', ...
%        };
rois = { 'IFGorb_roi', 'TP_roi' };

roi_dir = '/neurospin/unicog/protocols/IRMf/complexityLSF_MorenoPallier_2012/spm8/ROIs_analyses/'; % ROIs (.mat) directory

%outdir = '/neurospin/unicog/protocols/IRMf/complexityLSF_MorenoPallier_2012/spm8/ROIs_analyses/stanplot_ROIs/lsf/';
outdir = thisdir;

title_size = 16;
axes_size = 14;

for i = 1:length(rois)
    roi = maroi('load',strcat(roi_dir, rois{i}, '.mat'));
    [meany,meanY,sey,seY,firy,firY,firciy,firciY] = stanplot_groupb_roi_withsavedata_lsf( ...
                                                    Finterest, groupvar, timeaxis, baselinepoints, roi, rois{i}, outdir);

    savefile = strcat(outdir, rois{i},'_lsf_timecourse_means.dat')
    save(savefile,'meany')
    savefile = strcat(outdir, rois{i},'_lsf_timecourse_se.dat')
    save(savefile,'sey')
    
    FIG=figure(40);
    h_title = get(gca,'Title');
    set(h_title,'FontSize',title_size,'FontWeight','bold','FontUnits','points');
    set(gca,'FontSize',axes_size,'FontUnits','points');
    xlabel(gca, 'Time (in seconds)');
    ylabel(gca, 'signal');
    nameplot = strcat(outdir, rois{i},'_lsf_avg.png');
    print(FIG, '-dpng', '-r300', nameplot);
    print(FIG, strcat(outdir, rois{i},'_lsf_avg.fig'));

    FIG=figure(42);
    h_title = get(gca,'Title');
    set(h_title,'FontSize',title_size,'FontWeight','bold','FontUnits','points');
    set(gca,'FontSize',axes_size,'FontUnits','points');
    xlabel(gca, 'Time (in seconds)');
    ylabel(gca, 'signal');
    nameplot = strcat(outdir, rois{i},'_lsf_fir.png');
    print(FIG, '-dpng', '-r300', nameplot);
    print(FIG, strcat(outdir, rois{i},'_lsf_fir.fig'));
    
end

