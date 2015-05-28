function [meany,meanY,sey,seY,firy,firY,firciy,firciY]=stanplot_group(Finterest,groupvar,timeaxis,baselinepoints,varargin)
%%%% PLOT OF GROUP FMRI CURVES IN SPM5
%%%% Stan Dehaene  April 2009 (based on earlier code in SPM5) 
%%%% Comes with no warranty!!! But pretty nice plots...
%%%%
%%%% This function makes an average event-related plot of one or several groups of subjects
%%%%
%%%% The arguments are passed directly to stanplot_singlesubject.m
%%%% (see this function for detailed help)
%%%%
%%% EXAMPLE
%
% stanplot_singlemodel(1,repmat(1:4,1,5),[-4.8:2.4:14.4],3,[66 -18 9])
%
%%%% Note that the program calls another function 'getsubjectsdata.m' which
%%%% specifies the subjects groups, numbers and names
%%%%
% % Example of function getsubjects.data.m :
% % 
% % %%%% give the number of subject groups
% % ngroups=1;
% % %%%% name the groups of subjects 
% % groupn{1} = 'all';  %% here only one group
% % %%%% give the number of subjects in each group
% % nsub(1) = 3;
% % totsub = sum(nsub);  %% total number of subjects
% % %%%% give the path names for each subject's model
% % 
% % %% first in simplified form:
% % subjects = {'TR070015','RK090001','QB090003'};
% % %% then with the full path
% % rootdir = '/neurospin/unicog/protocols/IRMf/Compression_Vagharchakian_new_2009/Subjects';
% % modeldir = 'fMRI/acquisition1/analysis/model1_compression_HRF_fix_duration';
% % for i=1:nsub
% %     subjectsdir{i} = fullfile(rootdir,subjects{i},modeldir);
% % end


%%% get all arguments
if length(varargin)==0  %%%% last argument is missing, find it in the SPM figure
    figure(1);
    xyzmm=spm_mip_ui('GetCoords')
else
    xyzmm = varargin{1}';
end
XYZstr = sprintf('Voxel at [%g, %g, %g] mm',xyzmm);

getsubjectsdata;
%feval(subjectmfile);

ntimes = length(timeaxis);
timeresol = (timeaxis(2)-timeaxis(1));
noutconds = max(groupvar);

figure(40);clf;
figure(42);clf;

for g=1:ngroups

    %%% initialize the output

    ninmean{g} = zeros(noutconds,ntimes);
    meany{g} = zeros(noutconds,ntimes);
    meanY{g} = zeros(noutconds,ntimes);
    sey{g} = zeros(noutconds,ntimes);
    seY{g} = zeros(noutconds,ntimes);
    firy{g} = zeros(noutconds,ntimes);
    firY{g} = zeros(noutconds,ntimes);
    firciy{g} = zeros(noutconds,ntimes);
    firciY{g} = zeros(noutconds,ntimes);

    if g>1
        startnumber = sum(nsub(1:g-1));
    else
        startnumber = 0;
    end

    for sub=startnumber+(1:nsub(g))
        
        modeldir = subjectsdir{sub}
        
        [smeany,smeanY,ssey,sseY,sfiry,sfirY,sfirciy,sfirciY]=stanplot_singlemodel_b(modeldir,Finterest,groupvar,timeaxis,baselinepoints,xyzmm);
        if any(~isnan(smeany(:)))
            ninmean{g} = ninmean{g} + 1;
            meany{g} = meany{g} + smeany;
            meanY{g} = meanY{g} + smeanY;
            sey{g} = sey{g} + smeany .^2;
            seY{g} = seY{g} + smeanY .^2;
            firy{g} = firy{g} + sfiry;
            firY{g} = firY{g} + sfirY;
            firciy{g} = firciy{g} + sfiry.^2;
            firciY{g} = firciY{g} + sfirY.^2;
        end
    end

    %% final averages
    for cond=1:noutconds
        for i=1:ntimes
            meany{g}(cond,i) = meany{g}(cond,i)/ninmean{g}(cond,i);
            meanY{g}(cond,i) = meanY{g}(cond,i)/ninmean{g}(cond,i);
            sey{g}(cond,i) = sqrt( ((sey{g}(cond,i)- ninmean{g}(cond,i)*meany{g}(cond,i).^2)/(ninmean{g}(cond,i)-1))/ninmean{g}(cond,i) );
            seY{g}(cond,i) = sqrt( ((seY{g}(cond,i)- ninmean{g}(cond,i)*meanY{g}(cond,i).^2)/(ninmean{g}(cond,i)-1))/ninmean{g}(cond,i) );
            firy{g}(cond,i) = firy{g}(cond,i)/ninmean{g}(cond,i);
            firY{g}(cond,i) = firY{g}(cond,i)/ninmean{g}(cond,i);
            firciy{g}(cond,i) = sqrt( ((firciy{g}(cond,i)- ninmean{g}(cond,i)*firy{g}(cond,i).^2)/(ninmean{g}(cond,i)-1))/ninmean{g}(cond,i) );
            firciY{g}(cond,i) = sqrt( ((firciY{g}(cond,i)- ninmean{g}(cond,i)*firY{g}(cond,i).^2)/(ninmean{g}(cond,i)-1))/ninmean{g}(cond,i) );
        end
    end
    
    %%% now plot the data for this group

    figure(40);
    subplot(1,ngroups,g);cla;
    hold on;
%%    plot(timeaxis,meanY{g},'-','LineWidth',3); %%% model
    plot(timeaxis,meany{g},'-','LineWidth',3); %%% model
    for cond=1:noutconds
        errorbar(timeaxis,meany{g}(cond,:),sey{g}(cond,:),'.k');
        condlabel{cond} = sprintf('cond %d',cond);
    end
    legend(condlabel);
    plot(timeaxis,meany{g},'o','LineWidth',3); %%% data
    s=sprintf('Event-related average, group %d [%s,%d subjects], %s',g,groupn{g},nsub(g),XYZstr);
    s = strrep(s,'_','-');
    title(s);

    figure(42);
    subplot(1,ngroups,g);cla;
    hold on;
%    plot(timeaxis,firY{g},'-','LineWidth',3); %%% model
    plot(timeaxis,firy{g},'-','LineWidth',3); %%% data
    for cond=1:noutconds
        errorbar(timeaxis,firy{g}(cond,:),firciy{g}(cond,:),'.k');
        condlabel{cond} = sprintf('cond %d',cond);
    end
    legend(condlabel);
    plot(timeaxis,firy{g},'o','LineWidth',3); %%% data
    s=sprintf('Event-related average, group %d [%s,%d subjects], %s',g,groupn{g},nsub(g),XYZstr);
    s = strrep(s,'_','-');
    title(s);

end

%%% put all the plots on a comparable scale
for g=1:ngroups
    figure(40);
    subplot(1,ngroups,g);
    a = cell2mat(meany);
    mi = min(a(:));
    ma = max(a(:));
    ylim([mi - (ma-mi)*0.5     ma + (ma-mi)*0.5 ]);
    xlim([ min(timeaxis)-1 max(timeaxis)+1 ] );

    figure(42);
    subplot(1,ngroups,g);
    a = cell2mat(firy);
    mi = min(a(:));
    ma = max(a(:));
    ylim([mi - (ma-mi)*0.5     ma + (ma-mi)*0.5 ]);
    xlim([ min(timeaxis)-1 max(timeaxis)+1 ] );
end
