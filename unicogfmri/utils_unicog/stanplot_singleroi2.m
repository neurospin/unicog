function [meany,meanY,sey,seY,firy,firY,firciy,firciY]=stanplot_singleroi2(modeldir,Finterest,groupvar,timeaxis,baselinepoints,marsbarroi,name);
%%%% PLOT OF FMRI CURVES IN SPM5
%%%% Stan Dehaene  April 2009 (based on earlier code in SPM5) 
%%%% Comes with no warranty!!! But pretty nice plots...
%%%%
%%%% EXAMPLES: 
%
% modeldir = '/neurospin/unicog/protocols/IRMf/dyslexie_monzalvo_2007/al080002/stats/LggHRF';
% stanplot_singlemodel(modeldir,1,repmat(1:4,1,5),[-4.8:2.4:14.4],3,[66 -18 9])
%
% To regroup conditions, and eliminate some others (marked as 0):
% stanplot_singlemodel('f:\runAd\stats\statrunad',12,repmat([1 0 1 0 ],1,5),3,[-4:2:30]);
%
%%%%
%%%% This program starts with a simple SPM Model, whose location is given in modeldir.
%%%% - loads the file names in SPM.mat
%%%% - gets the data for a given voxel in the original data files,
%%%% - corrects it according to the model's filter and variables of
%%%% non-interest
%%%% - finds the conditions and their onsets in SPM.mat
%%%% - computes and plots the time-locked averages for the different conditions, grouped according the variable groupvar.
%%%% - also computes the FIR estimate of the deconvolved hemodynamic responses
%%%% 
%%%% Some of the program's nicest features are:
%%%% - it is generic and works with any SPM model with as many runs and
%%%% event onsets as needed.
%%%% - it incorporates all of SPM's whitening, filtering, and regressing out of
%%%% variables of non-interest; all of those undesired effects are removed
%%%% prior to averaging or deconvolving.
%%%% - it works at any desired temporal resolution! The program will
%%%% attempt to estimate the hemodynamic response at the desired time
%%%% points. Of course this will work only if the events are randomly
%%%% jittered with respect to the fMRI acquisition -- but even if this is
%%%% not the case, the program will not crash, but simply report the
%%%% presence of missing points in the final curves.
%%%% - it usually does not crash when the original data have been moved,
%%%% but attempts to retrieve them using the current model path.
%%%%
%%%% The argument modeldir is the name of the directory where the model
%%%% (i.e. SPM.mat) is located).
%%%%
%%%% The argument Finterest (usually = 1) indicates which contrast in the SPM model
%%%% refers to the F test of real interest. This F test usually has ones in columns for all
%%%% variables of interest, and zero everywhere else, e.g. for movement
%%%% regressors whose effects on the data must be subtracted out.
%%%% Specify zero (0) if you have no contrast of interest. However, note
%%%% that your plot may not be as nice as it could be (for instance, the
%%%% effects of movement might be regressed out in the SPM stats, but not
%%%% in your plot).
%%%%
%%%% The argument groupvar is a "remapping" vector which allows you to regroup conditions at will.
%%%% It must be as long as the numbers of
%%%% runs X the numbers of conditions in each run. For each such condition
%%%% declared in the model, groupvar gives the output
%%%% condition. Use zero for conditions that you don't want to see in the
%%%% plot.
%%%% Examples:
%%%% groupvar=ones(1:5*2) will regroup all conditions (of a 5 runs and 2 conds model) into a single output cell
%%%% groupvar = [ 1 2  1 2  1 2  1 2  1 2 ] will regroup these two conditions across all 5 runs
%%%% groupvar = [ 0 1  0 1  0 1  0 0  0 0 ] will discard condition 1 and
%%%% only plot condition 2 for the first 3 runs.
%%%%
%%%% The argument "timeaxis" specifies the time range and resolution of
%%%% the resulting plot, in seconds
%%%% e.g. timeaxis = [-4:1:12] will give you a plot from -4 to 12 seconds,
%%%% with a spacing of 1 second between the successive time points.
%%%%
%%%% The argument "baselinepoints" specifies the number of initial points of the curve that serve as a baseline
%%%% The mean of these points will be subtracted from each curve.
%%%%
%%%% The voxel xyz coordinates in mm can be passed as the last argument
%%%% e.g. [-42 -57 -12 ] for the VWFA
%%%% If they are not passed, then the program attemps to find them from the current cursor location in the
%%%% current SPM figure 1
%%%%
%%%% The output gives the mean and standard error for the actual data (y)
%%%% and the model (Y), separately for event-related averaging and FIR
%%%% estimation.
%%%%
%%%% TIPS:
%%%% - Be aware that event-related averaging often does not provide a satisfactory
%%%% solution. It works really well only for slow-event-related designs
%%%% with non-overlapping events. Nothing will prevent this program from
%%%% running in other cases -- but the results will be meaningless!
%%%% - In general the FIR estimates should therefore be easier to interpret
%%%% as hemodynamic responses. However, they can be poorly estimable, for
%%%% instance if the design is a block design. In general, FIR should work
%%%% best with random fast event-related designs, where conditions are
%%%% ideally uncorrelated. Also, FIR works quite poorly if there is a high
%%%% density of points to be estimated, compared to the number of images.
%%%% It is a good idea to set the resolution to about one TR, and decrease
%%%% this value until the FIR matrix which appears in figure 31 peaks at 1, not 2 or more.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% get all arguments
% if length(varargin)==0  %%%% last argument is missing, find it in the SPM figure
%     figure(1);
%     xyzmm=spm_mip_ui('GetCoords')
% else
%     xyzmm = varargin{1};
% end
% if size(xyzmm,1)==1
%     xyzmm = xyzmm';
% end

load(fullfile(modeldir,'SPM.mat'));
%%%% determine the coordinates in voxels
% iM = SPM.xVol.iM;
% xyzvox = iM( 1:3, : ) * [ xyzmm ; 1 ] ;

% nvox = size(xyzvox,2);  %%% for possible extension to multiple voxels (not programmed yet)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% RECOVERY OF THE DATA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% read the data
fprintf( '\n READ RAW DATA\n' ) ;
VY = SPM.xY.VY;
y = ones( length(VY), 1 ) ;
%h = waitbar( 0, 'Raw data reading...' ) ;
for i = 1:1:length(VY)
    %waitbar( i/length(VY), h ) ;

    %%% check if data has been moved! and define some useful names
    subjname = '';
    expedir = '';
    k = strfind(modeldir,'analyses');
    if k>0
        subjdir = modeldir(1:k-2);
        k2 = max(strfind(subjdir,filesep));
        if k2>0
            subjname = subjdir(k2+1:end);
            expedir = subjdir(1:k2-1);
            k3=strfind(VY(i).fname,subjname); %%% try finding the same subject name
            if k3>0
                SPM.xY.VY(i).fname =fullfile(expedir,VY(i).fname(k3:end));
            end
            k3=strfind(VY(i).fname,'fMRI'); %%% try finding the 'functional' convention
            if k3>0
                SPM.xY.VY(i).fname =fullfile(expedir,subjname,VY(i).fname(k3:end));
            end
        end
    end
    %      y(i) = spm_sample_vol( VY(i), xyzvox(1), xyzvox(2), xyzvox(3), 0 ) ;
end
%close(h) ;

%%%    display one file name as feedback
SPM.xY.VY(1).fname

%%% also update the names in SPM.xY.P --- SPM structures are awfully
%%% redundant!
SPM.xY.P = char(SPM.xY.VY(:).fname);

%%%% the following part was taken literally from spm_graph.m
%%%% It is what is called when you plot data as a function of time

Ic = Finterest;
%xyz=xyzmm;
%XYZ = xyzvox;

%-Extract filtered and whitened data from files
%==========================================================================
marsbarroi = spm_hold(marsbarroi, 0); % set NN resampling

try
    % y = spm_get_data(SPM.xY.VY,XYZ);
    mm = get_marsy(marsbarroi, SPM.xY.VY, 'mean');
    y = summary_data(mm);
    %    y = mean(getvoxels_in_roi(SPM.xY.VY, marsbarroi));
    y = spm_filter(SPM.xX.K,SPM.xX.W*y);
catch err
    disp(getReport(err))
    try
        % remap files in SPM.xY.P if SPM.xY.VY is no longer valid
        %------------------------------------------------------------------
        SPM.xY.VY = spm_vol(SPM.xY.P);
        %        y = spm_get_data(SPM.xY.VY,XYZ);
        mm = get_marsy(marsbarroi, VY, 'mean');
        y = summary_data(mm);
        %y = getvoxels_in_roi(SPM.xY.VY, marsbarroi);     
        y = spm_filter(SPM.xX.K,SPM.xX.W*y);

    catch err
        disp(err.identifier)
   
        % data has been moved or renamed
        %------------------------------------------------------------------
        y = [];
        spm('alert!',{'Original data have been moved or renamed',...
            'Recomendation: please update SPM.xY.P'},...
            mfilename,0);
        
        exit
    end
end
XYZstr = name;


%-Compute residuals
%-----------------------------------------------------------------------
if isempty(y)

    % make R = NaN so it will not be plotted
    %----------------------------------------------------------------------
    R   = NaN*ones(size(SPM.xX.X,1),1);

else
    % residuals (non-whitened)
    %----------------------------------------------------------------------
    R   = spm_sp('r',SPM.xX.xKXs,y);

end

%-Parameter estimates:   beta = xX.pKX*xX.K*y;
%-Residual mean square: ResMS = sum(R.^2)/xX.trRV
%----------------------------------------------------------------------
for i=1:length(SPM.Vbeta);
    if isempty(strfind(SPM.Vbeta(i).fname,modeldir))  
        %%% if necessary add path, so we don't have to cd to this directory to find the betas
      SPM.Vbeta(i).fname = fullfile(modeldir,SPM.Vbeta(i).fname);
    end
end
SPM.Vbeta(1).fname
if isempty(strfind(SPM.VResMS.fname,modeldir))
    SPM.VResMS.fname = fullfile(modeldir,SPM.VResMS.fname);
end
SPM.VResMS.fname

%beta  = spm_get_data(SPM.Vbeta, XYZ);
mm2= get_marsy(marsbarroi, SPM.Vbeta, 'mean');
beta = summary_data(mm2);

%beta = mean(getvoxels_in_roi(SPM.Vbeta, marsbarroi));

%ResMS = spm_get_data(SPM.VResMS,XYZ);
mm3 = get_marsy(marsbarroi, [SPM.VResMS.fname], 'mean');
ResMS = summary_data(mm3)

%ResMS = mean(getvoxels_in_roi(SPM.xY.VY, marsbarroi));

Bcov  = ResMS*SPM.xX.Bcov;

% fitted (corrected)  data (Y = X1o*beta)
%--------------------------------------------------------------
if Ic>0
  Y = spm_FcUtil('Yc',SPM.xCon(Ic),SPM.xX.xKXs,beta);
else 
    Y = SPM.xX.X * beta;
end

% adjusted data
%------------------------------------------------------------------
y     = Y + R;


figure(29); %%% basic SPM-like figure as a function of time or scan 
plot([y Y]);
title(sprintf('Subj %s, %s',subjname,XYZstr));
legend('Data','Model');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% EVENT-RELATED AVERAGING PART
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% get the TR in seconds
TR = SPM.xY.RT

%%%% get the number of runs, etc
load(fullfile(modeldir,'SPM.mat'));
nruns = length(SPM.Sess);
ntimes = length(timeaxis);
timeresol = (timeaxis(2)-timeaxis(1));

%%%% initialize the loop variables and output variables
nprevscans = 0;
itotcond = 0;

noutconds = max(groupvar);

ninmean = zeros(noutconds,ntimes);
meany = zeros(noutconds,ntimes);
meanY = zeros(noutconds,ntimes);
sey = zeros(noutconds,ntimes);
seY = zeros(noutconds,ntimes);

for run = 1:nruns
    nscans = SPM.nscan(run);
    runtime = ((1:nscans)-1)*TR; %%% time at which each volume was acquired
    runy = y( nprevscans + (1:nscans));  %%%% this is the y data local to this run
    runY = Y( nprevscans + (1:nscans));  %%%% this is the y data local to this run
    nconds = length(SPM.Sess(run).U);
    for cond=1:nconds
        itotcond = itotcond + 1; %%% index of this condition in the big array of conditions "groupvar"
        outcond = groupvar(itotcond);
        if outcond>0
            nonsets = length(SPM.Sess(run).U(cond).ons);
            for scan = 1:nscans
                tscan = runtime(scan);
                for i=1:nonsets %%% look at each stimulus and check whether the data falls within the time axis around its onset
                    ons = SPM.Sess(run).U(cond).ons(i);
                    binscan = round ( (( tscan - ons - timeaxis(1) ) / timeresol) ) + 1 ;
                    if (binscan >0)&(binscan<=ntimes) %%%% the data fall within the range
                        ninmean(outcond,binscan) = ninmean(outcond,binscan) +1;
                        meany(outcond,binscan) = meany(outcond,binscan) + runy(scan);
                        meanY(outcond,binscan) = meanY(outcond,binscan) + runY(scan);
                        sey(outcond,binscan) = sey(outcond,binscan) + runy(scan).^2;
                        seY(outcond,binscan) = seY(outcond,binscan) + runy(scan).^2;
                    end
               end
            end
        end
    end
    nprevscans = nprevscans + nscans;
end    
    
%% compute the final average and standard deviation
for cond=1:noutconds
    for i=1:ntimes
        meany(cond,i) = meany(cond,i)/ninmean(cond,i);
        meanY(cond,i) = meanY(cond,i)/ninmean(cond,i);
        sey(cond,i) = sqrt( ((sey(cond,i)- ninmean(cond,i)*meany(cond,i).^2)/(ninmean(cond,i)-1))/ninmean(cond,i) );
        seY(cond,i) = sqrt( ((seY(cond,i)- ninmean(cond,i)*meanY(cond,i).^2)/(ninmean(cond,i)-1))/ninmean(cond,i) );
    end
end

%% subtract the baseline from each cond
if baselinepoints>0
  baseliney=mean(meany(:,1:baselinepoints),2);
  baselineY=mean(meanY(:,1:baselinepoints),2);
  meany=meany-repmat(baseliney,1,ntimes);
  meanY=meanY-repmat(baselineY,1,ntimes);
end

%%%%% make a nice final figure!
figure(30);
clf;
hold on;
plot(timeaxis,meanY','-','LineWidth',3); %%% model
for cond=1:noutconds
  errorbar(timeaxis,meany(cond,:),sey(cond,:),'.k');
  condlabel{cond} = sprintf('cond %d',cond);
end
legend(condlabel);
plot(timeaxis,meany','o','LineWidth',3); %%% data
s=sprintf('Event-related average, Subject %s, %s',subjname,XYZstr);
s = strrep(s,'_','-');
title(s);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% compute the FIR response by matrix deconvolution
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% create the matrix of regressors X
% X is a matrix with as many rows as the number of images
% and as many columns as the number of time points X the number of output conditions

X = zeros( length(y) , ntimes * noutconds );

nprevscans = 0;
itotcond = 0;
for run = 1:nruns
    nscans = SPM.nscan(run);
    runtime = ((1:nscans)-1)*TR; %%% time at which each volume was acquired
    nconds = length(SPM.Sess(run).U);
    for cond=1:nconds
        itotcond = itotcond + 1; %%% index of this condition in the big array of conditions "groupvar"
        outcond = groupvar(itotcond);
        if outcond>0
            nonsets = length(SPM.Sess(run).U(cond).ons);
            for scan = 1:nscans
                curscan = nprevscans + scan; %%% current scan in the total range of images
                tscan = runtime(scan);
                for i=1:nonsets %%% look at each stimulus and check whether the data falls within the time axis around its onset
                    ons = SPM.Sess(run).U(cond).ons(i);
                    binscan = round ( (( tscan - ons - timeaxis(1) ) / timeresol) ) + 1;
                    if (binscan >0)&(binscan<=ntimes) %%%% the data fall within the range
                        Xindex = binscan + ntimes * (outcond-1) ; % column for this condition and time in the X matrix
                        X( curscan, Xindex ) = X( curscan, Xindex ) +1;
                    end
                end
            end
        end
    end
    nprevscans = nprevscans + nscans;
end
figure(31);
imagesc(X);
colormap(gray);
colorbar;
title('FIR matrix');

% create labels for the matrix weights, so that it is easy to recover the
% corresponding data points later on
Xlabelcond = ((1:noutconds)'*ones(1,ntimes))';
Xlabelcond = Xlabelcond(:)';
Xlabeltime = repmat(1:ntimes,1,noutconds);

% remove columns that have only zeros (non-estimable parts of the curves)
sel = find(sum(X)>0);
X = X(:,sel);
Xlabelcond = Xlabelcond(sel);
Xlabeltime = Xlabeltime(sel);
nestimable = length(Xlabelcond);

% the following part is taken with modifications from spm_graph.m
xX          = spm_sp('Set',X);  % % Set up space structure, storing matrix, singular values, rank & tolerance
pX          = spm_sp('x-',xX);  % pseudo-inverse

PSTHy        = pX*y;  % application to the real data to get the Post-stimulus time histogram
res         = spm_sp('r',xX,y);  % residual
df          = size(X,1) - size(X,2); % degrees of freedom
bcov        = pX*pX'*sum(res.^2)/df; % covariance
CI = 1; %% to plot one standard error of the residual
PCIy         = CI*sqrt(diag(bcov));  %%% the PCI are the error bars 

PSTHY        = pX*Y;  % application to the model data to get the Post-stimulus time histogram
res         = spm_sp('r',xX,Y);  % residual
df          = size(X,1) - size(X,2); % degrees of freedom
bcov        = pX*pX'*sum(res.^2)/df; % covariance
CI = 1; %% to plot one standard error of the residual
PCIY         = CI*sqrt(diag(bcov));  %%% the PCI are the error bars 

% reorganize the output for plotting, with missing data at the appropriate
% locations
firy = nan(noutconds,ntimes);
firY = nan(noutconds,ntimes);
firciy = nan(noutconds,ntimes);
firciY = nan(noutconds,ntimes);
for i=1:nestimable
    firy(Xlabelcond(i),Xlabeltime(i)) = PSTHy(i);
    firY(Xlabelcond(i),Xlabeltime(i)) = PSTHY(i);
    firciy(Xlabelcond(i),Xlabeltime(i)) = PCIy(i);
    firciY(Xlabelcond(i),Xlabeltime(i)) = PCIY(i);
end

%% subtract the baseline from each cond
if baselinepoints>0
  baseliney=mean(firy(:,1:baselinepoints),2);
  baselineY=mean(firY(:,1:baselinepoints),2);
  firy=firy-repmat(baseliney,1,ntimes);
  firY=firY-repmat(baselineY,1,ntimes);
end

%%%%% make a nice final figure!
figure(32);
clf;
hold on;
plot(timeaxis,firY','-','LineWidth',3); %%% model
for cond=1:noutconds
  errorbar(timeaxis,firy(cond,:),firciy(cond,:),'.k');
  condlabel{cond} = sprintf('cond %d',cond);
end
legend(condlabel);
plot(timeaxis,firy','o','LineWidth',3); %%% data
s=sprintf('FIR estimation, Subject %s, %s',subjname,XYZstr);
s = strrep(s,'_','-');
title(s);




