function [c, r, t, cpulse, verbose] = tapas_physio_read_physlogfiles_siemens(log_files, ...
    verbose, varargin)
% reads out physiological time series and timing vector for Siemens
% logfiles of peripheral cardiac monitoring (ECG/Breathing Belt or
% pulse oximetry)
%
%   [cpulse, rpulse, t, c] = tapas_physio_read_physlogfiles_siemens(logfile, vendor, cardiac_modality)
%
% IN    log_files
%       .log_cardiac        contains ECG or pulse oximeter time course
%                           for GE: ECGData...
%       .log_respiration    contains breathing belt amplitude time course
%                           for GE: RespData...
%
% OUT
%   cpulse              time events of R-wave peak in cardiac time series (seconds)
%                       for GE: usually empty
%   r                   respiratory time series
%   t                   vector of time points (in seconds)
%                       NOTE: This assumes the default sampling rate of 40
%                       Hz
%   c                   cardiac time series (ECG or pulse oximetry)
%
% EXAMPLE
%   [ons_secs.cpulse, ons_secs.rpulse, ons_secs.t, ons_secs.c] =
%       tapas_physio_read_physlogfiles_siemens(logfile, vendor, cardiac_modality);
%
%   See also tapas_physio_main_create_regressors
%
% Author: Lars Kasper
%         file structure information from PhLeM Toolbox, T. Verstynen (November 2007);
%                and Deshpande and J. Grinstead, Siemens Medical Solutions (March 2009)
%         additional log information Miriam Sebold, Charite Berlin (2014)
%
% Created: 2014-07-08
% Copyright (C) 2014 Institute for Biomedical Engineering, ETH/Uni Zurich.
%
% This file is part of the PhysIO toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.
%
% $Id: tapas_physio_read_physlogfiles_siemens.m 466 2014-04-27 13:10:48Z kasperla $

%% read out values

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Added by A. Moreno - 19/05/2016
% From first tests in data_selection_tapas

% Output initialization
c = [];
r = [];
t = [];
cpulse = [];

% tick_time = 2.5; % ms - one tick (sampling dwell time)

% LOAD AND DISPLAY DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%log_files.cardiac           = 'data/Physio_20160405_sess1_PULS.txt';
%log_files.respiration       = 'data/Physio_20160405_sess1_RESP.txt';
%log_files.info              = 'data/Physio_20160405_sess1_Info.txt';
log_files.sampling_interval = 1/400; % in seconds; tick_time = 2.5 ms % TO AUTOMATIZE!! **********
log_files.relative_start_acquisition = 0 ; % in seconds

% PULS - cardiac signal %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% puls_file = fopen('data/Physio_20160405_sess1_PULS.txt');
puls_file = fopen(log_files.cardiac);
s = textscan(puls_file,'%d\t%s\t%d\t%s','HeaderLines',1);
fclose(puls_file);
acq_ticks_puls = s{1};
channel_puls = s{2};
value_puls = s{3};
signal_puls = s{4};

dt = log_files.sampling_interval; % tick_time

%time_axis_puls = (double((acq_ticks_puls - acq_ticks_puls(1)))* tick_time)/1000; % (ticks * seconds/tick) converted to seconds
%time_axis_puls = (double(acq_ticks_puls)* tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_puls = double(acq_ticks_puls * dt); % (ticks * seconds/tick) converted to seconds
%time_axis_puls_min = time_axis_puls / 60; % minutes

signal_puls_num = zeros(length(signal_puls),1);
for i = 1:length(signal_puls)
    if strcmp(signal_puls{i},'PULS_TRIGGER')
        signal_puls_num(i) = max(value_puls)/2;
    elseif strcmp(signal_puls{i},'EXT1_TRIGGER')
        signal_puls_num(i) = max(value_puls);
    else % strcmp(signal_puls{i},'')
        signal_puls_num(i) = 0;
    end
end

figure(30);
clf;
subplot(3,1,1);
%plot(time_axis_puls,value_puls,'-r',time_axis_puls,signal_puls_num,'c*','LineWidth',1);
%plot(time_axis_puls,value_puls,'-r','LineWidth',1);
plot(acq_ticks_puls,value_puls,'-r','LineWidth',1);

% RESP - respiration %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% resp_file = fopen('data/Physio_20160405_sess1_RESP.txt');
resp_file = fopen(log_files.respiration);
s = textscan(resp_file,'%d\t%s\t%d\t%s','HeaderLines',1);
fclose(resp_file);
acq_ticks_resp = s{1};
channel_resp = s{2};
value_resp = s{3};
signal_resp = s{4};

%time_axis_resp = (double(acq_ticks_resp - acq_ticks_resp(1)) * tick_time)/1000; % (ticks * seconds/tick) converted to seconds
%time_axis_resp = (double(acq_ticks_resp) * tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_resp = double(acq_ticks_resp * dt); % (ticks * seconds/tick) converted to seconds
%time_axis_resp_min = time_axis_resp / 60; % minutes

signal_resp_num = zeros(length(signal_resp),1);
for i = 1:length(signal_resp)
    if strcmp(signal_resp{i},'PULS_TRIGGER')
        signal_resp_num(i) = max(value_resp)/2;
    elseif strcmp(signal_resp{i},'EXT1_TRIGGER')
        signal_resp_num(i) = max(value_resp);
    else % strcmp(signal_resp{i},'')
        signal_resp_num(i) = 0;
    end
end

subplot(3,1,2);
%plot(time_axis_resp,value_resp,'-g',time_axis_resp,signal_resp_num,'c*','LineWidth',1);
%plot(time_axis_resp,value_resp,'-g','LineWidth',1);
plot(acq_ticks_resp,value_resp,'-g','LineWidth',1);


% Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% info_file = fopen('data/Physio_20160405_sess1_Info.txt');
info_file = fopen(log_files.info);
s = textscan(info_file,'%d\t%d\t%d\t%d','HeaderLines',1);
fclose(info_file);
volume_info = s{1};
slice_info = s{2};
acq_start_ticks_info = s{3};
acq_finish_ticks_info = s{4};

%time_axis_info = (double(acq_start_ticks_info) * tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_info = double(acq_start_ticks_info * dt); % (ticks * seconds/tick) converted to seconds
%time_axis_info_min = time_axis_info / 60; % minutes

ttl_value = zeros(length(volume_info),1);
prev_volume_number = 0;
for i = 1:length(volume_info)
    if i == 1
        ttl_value(i) = volume_info(i);
        ttl_start_in_ticks = acq_start_ticks_info(i);
    else
        if (volume_info(i)~=prev_volume_number)
            ttl_value(i) = volume_info(i);
        end
    end
    prev_volume_number = volume_info(i);
    ttl_end_in_ticks = acq_finish_ticks_info(i);
end

subplot(3,1,3);
%plot(time_axis_info,ttl_value,'bo','LineWidth',1);
%plot(time_axis_info,volume_info,'b-',time_axis_info,ttl_value,'k+','LineWidth',1);
plot(acq_start_ticks_info,volume_info,'b-',acq_start_ticks_info,ttl_value,'k+','LineWidth',1);


% SELECTION OF THE USEFUL DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%ttl_start_in_ticks
%ttl_end_in_ticks

count = 1;
for i = 1:length(value_puls)
    if (acq_ticks_puls(i) > ttl_start_in_ticks) && (acq_ticks_puls(i) < ttl_end_in_ticks)
        cardiac_ticks(count) = acq_ticks_puls(i);
        cardiac(count) = (double(value_puls(i)));
        count = count + 1;
    end
end
cardiac = cardiac';
cardiac_ticks = cardiac_ticks';

%time_axis_cardiac = ((double(cardiac_ticks) - double(ttl_start_in_ticks))* tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_cardiac = (double(cardiac_ticks) - double(ttl_start_in_ticks)) * dt; % (ticks * seconds/tick) converted to seconds

figure(31);
clf;
subplot(3,1,1);
%plot(cardiac_ticks,cardiac,'-r','LineWidth',1);
plot(time_axis_cardiac,cardiac,'-r','LineWidth',1);

count = 1;
for i = 1:length(value_resp)
    if (acq_ticks_resp(i) > ttl_start_in_ticks) && (acq_ticks_resp(i) < ttl_end_in_ticks)
        respiration_ticks(count) = acq_ticks_resp(i);
        respiration(count) = (double(value_resp(i)));
        count = count + 1;
    end
end
respiration = respiration';
respiration_ticks = respiration_ticks';

%time_axis_resp = ((double(respiration_ticks) - double(ttl_start_in_ticks))* tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_resp = (double(respiration_ticks) - double(ttl_start_in_ticks)) * dt; % (ticks * seconds/tick) converted to seconds

subplot(3,1,2);
%plot(respiration_ticks,respiration,'-g','LineWidth',1);
plot(time_axis_resp,respiration,'-g','LineWidth',1);


%time_axis_volumes = ((double(acq_start_ticks_info) - double(ttl_start_in_ticks))* tick_time)/1000; % (ticks * seconds/tick) converted to seconds
time_axis_volumes = (double(acq_start_ticks_info) - double(ttl_start_in_ticks)) * dt; % (ticks * seconds/tick) converted to seconds

subplot(3,1,3);
%plot(acq_start_ticks_info,volume_info,'b-',acq_start_ticks_info,ttl_value,'k+','LineWidth',1);
plot(time_axis_volumes,volume_info,'b-',time_axis_volumes,ttl_value,'k+','LineWidth',1);


% DRIFTER processing %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% SPM must be run before running DRIFTER

% tick_time = 2.5; % ms

%cardiac_period = (2*tick_time)/1000; % in seconds, SampleTime = 2
cardiac_period = 2 * dt; % in seconds, SampleTime = 2
cardiac_freq = 1/cardiac_period;

%respiration_period = (8*tick_time)/1000; % in seconds, SampleTime = 8
respiration_period = 8 * dt; % in seconds, SampleTime = 8
respiration_freq = 1/respiration_period;


% Adaptation to read physiological data from Minneapolis sequence
c = cardiac;
r = respiration;
%t = time_axis_volumes;
t = time_axis_cardiac;
cpulse = [];

%*** PROBLEM : c, r and t MUST HAVE THE SAME LENGTH !!!!!!!!!!!!! ***

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% if nargin < 2
%     verbose.level = 0;
% end
% DEBUG = verbose.level >=2;
% 
% % process optional input parameters and overwrite defaults
% defaults.ecgChannel         = 'mean'; % 'mean'; 'v1'; 'v2'
% defaults.endCropSeconds     = 1;
% 
% args                = tapas_physio_propval(varargin, defaults);
% tapas_physio_strip_fields(args);
% 
% cpulse              = [];
% dt                  = log_files.sampling_interval;
% 
% 
% if ~isempty(log_files.cardiac)
%     fid             = fopen(log_files.cardiac);
%     C               = textscan(fid, '%s', 'Delimiter', '\n', 'bufsize', 1e9);
%     fclose(fid);
%     
%     % Determine relative start of acquisition from dicom headers and
%     % logfile footers
%     hasScanTimingDicomImage = ~isempty(log_files.scan_timing);
%     
%     if hasScanTimingDicomImage
%         
%         %Get time stamps from footer:
%         
%         linesFooter = C{1}(2:end);
%         LogStartTimeSeconds =   str2num(char(regexprep(linesFooter(~cellfun(@isempty,strfind(linesFooter,...
%             'LogStartMDHTime'))),'\D',''))) / 1000;
%         LogStopTimeSeconds =    str2num(char(regexprep(linesFooter(~cellfun(@isempty,strfind(linesFooter,...
%             'LogStopMDHTime'))),'\D',''))) / 1000;
%         
%         % load dicom
%         dicomHeader             = spm_dicom_headers(fullfile(log_files.scan_timing));
%         ScanStartTimeSeconds    = dicomHeader{1}.AcquisitionTime;
%         ScanStopTimeSeconds     = dicomHeader{1}.AcquisitionTime + ...
%             dicomHeader{1}.RepetitionTime/1000;
%         
%         % This is just a different time-scale, I presume, it does definitely
%         % NOT match with the Acquisition time in the DICOM-headers
%         % ScanStartTime = str2num(char(regexprep(linesFooter(~cellfun(@isempty,strfind(linesFooter,...
%         %     'LogStartMPCUTime'))),'\D','')));
%         % ScanStopTime = str2num(char(regexprep(linesFooter(~cellfun(@isempty,strfind(linesFooter,...
%         %     'LogStopMPCUTime'))),'\D','')));
%         
%         switch log_files.align_scan
%             case 'first'
%                 relative_start_acquisition = ScanStartTimeSeconds - ...
%                     LogStartTimeSeconds;
%             case 'last'
%                 relative_start_acquisition = ScanStopTimeSeconds - ...
%                     LogStopTimeSeconds;
%         end
%     else
%         relative_start_acquisition = 0;
%     end           
%         
%     % add arbitray offset specified by user
%     relative_start_acquisition = relative_start_acquisition + ...
%         log_files.relative_start_acquisition;
%     
%     
%     lineData = C{1}{1};
%     iTrigger = regexpi(lineData, '6002'); % signals start of data logging
%     lineData = lineData((iTrigger(end)+4):end);
%     data = textscan(lineData, '%d', 'Delimiter', ' ', 'MultipleDelimsAsOne',1);
%     
%     % Remove the systems own evaluation of triggers.
%     cpulse  = find(data{1} == 5000);  % System uses identifier 5000 as trigger ON
%     cpulse_off = find(data{1} == 6000); % System uses identifier 5000 as trigger OFF
%     recording_on = find(data{1} == 6002);% Scanner trigger to Stim PC?
%     recording_off = find(data{1} == 5003);
%     
%     
%     % Filter the trigger markers from the ECG data
%      %Note: depending on when the scan ends, the last size(t_off)~=size(t_on).
%     iNonEcgSignals = [cpulse; cpulse_off; recording_on; recording_off];
%     codeNonEcgSignals = [5000*ones(size(cpulse)); ...
%         6000*ones(size(cpulse_off)); ...
%         6002*ones(size(recording_on))
%         5003*ones(size(recording_off))];
%     
%     % data_stream contains only the 2 ECG-channel time courses (with
%     % interleaved samples
%     data_stream = data{1};
%     data_stream(iNonEcgSignals) = [];
%     
%     %iDataStream contains the indices of all true ECG signals in the full
%     %data{1}-Array that contains also non-ECG-signals
%     iDataStream = 1:numel(data{1});
%     iDataStream(iNonEcgSignals) = [];
%     
%     nSamples = numel(data_stream);
%     nRows = ceil(nSamples/2);
%     
%     % create a table with channel_1, channels_AVF and trigger signal in
%     % different Columns
%     % - iData_table is a helper table that maps the original indices of the
%     % ECG signals in data{1} onto their new positions
%     data_table = zeros(nRows,3);
%     iData_table = zeros(nRows,3);
%     
%     data_table(1:nRows,1) = data_stream(1:2:end);
%     iData_table(1:nRows,1) = iDataStream(1:2:end);
%     
%     if mod(nSamples,2) == 1
%         data_table(1:nRows-1,2) = data_stream(2:2:end);
%         iData_table(1:nRows-1,2) = iDataStream(2:2:end);
%     else
%         data_table(1:nRows,2) = data_stream(2:2:end);
%         iData_table(1:nRows,2) = iDataStream(2:2:end);
%     end
%     
%     % now fill up 3rd column with trigger data
%     % - for each trigger index in data{1}, check where ECG data with closest
%     % smaller index ended up in the data_table ... and put trigger code in
%     % same row of that table
%     nTriggers = numel(iNonEcgSignals);
%     
%     for iTrigger = 1:nTriggers
%         % find index before trigger event in data stream and
%         % detect it in table
%         iRow = find(iData_table(:,2) == iNonEcgSignals(iTrigger)-1);
%         
%         % look in 1st column as well whether maybe signal detected there
%         if isempty(iRow)
%             iRow = find(iData_table(:,1) == iNonEcgSignals(iTrigger)-1);
%         end
%         
%         data_table(iRow,3) = codeNonEcgSignals(iTrigger);
%     end
%     
%     
%     % set new indices to actual
%     cpulse = find(data_table(:,3) == 5000);
%     cpulse_off = find(data_table(:,3) == 6000);
%     recording_on = find(data_table(:,3) == 6002);
%     recording_off = find(data_table(:,3) == 5003);
%     
%     % Split a single stream of ECG data into channel 1 and channel 2.
%     channel_1   = data_table(:,1);
%     channel_AVF = data_table(:,2);
%     meanChannel = mean([channel_1(:) channel_AVF(:)],2);
%     
%     % Make them the same length and get time estimates.
%     switch ecgChannel
%         case 'mean'
%             c = meanChannel - mean(meanChannel);
%             
%         case 'v1'
%             c = channel_1 - mean(channel_1);
%             
%         case 'v2'
%             c = channel_AVF - mean(channel_AVF);
%     end;
%     
%     % compute timing vector and time of detected trigger/cpulse events
%     nSamples = size(c,1);
%     t = -relative_start_acquisition + ((0:(nSamples-1))*dt)';
%     cpulse = t(cpulse);
%     cpulse_off = t(cpulse_off);
%     recording_on = t(recording_on);
%     recording_off = t(recording_off);
%     
%     % TODO: put this in log_files.relative_start_acquisition!
%     % for now: we assume that log file ends when scan ends (plus a fixed
%     % EndClip
%     
%     endClipSamples = floor(endCropSeconds/dt);
%     stopSample = nSamples - endClipSamples;
%     ampl = max(meanChannel); % for plotting timing events
%     
%     if DEBUG
%         stringTitle = 'Raw Siemens physlog data';
%         verbose.fig_handles(end+1) = tapas_physio_get_default_fig_params();
%         set(gcf, 'Name', stringTitle);
%         stem(cpulse, ampl*ones(size(cpulse)), 'g'); hold all;
%         stem(cpulse_off, ampl*ones(size(cpulse_off)), 'r');
%         stem(t(stopSample), ampl , 'm');
%         plot(t, channel_1);
%         plot(t, channel_AVF);
%         plot(t, meanChannel);
%        
%         stringLegend = { ...
%             'cpulse on', 'cpulse off', 'assumed last sample of last scan volume', ...
%             'channel_1', 'channel_{AVF}', 'mean of channels'};
%         
%         if ~isempty(recording_on)
%             stem(recording_on, ampl*ones(size(recording_on)), 'k');
%             stringLegend{end+1} = 'phys recording on';
%         end
%         
%         if ~isempty(recording_off)
%             stem(recording_off, ampl*ones(size(recording_off)), 'k');
%             stringLegend{end+1} = 'phys recording off';
%         end
%         legend(stringLegend);
%         title(stringTitle);
%         xlabel('t (seconds)');
%     end
%     % crop end of log file
%     
%     cpulse(cpulse > t(stopSample)) = [];
%     t(stopSample+1:end) = [];
%     c(stopSample+1:end) = [];
%     
% else
%     c = [];
% end
% 
% if ~isempty(log_files.respiration)
%     r = load(log_files.respiration, 'ascii');
%     nSamples = size(r,1);
%     t = relative_start_acquisition + ((0:(nSamples-1))*dt)';
% else
%     r = [];
% end

end
