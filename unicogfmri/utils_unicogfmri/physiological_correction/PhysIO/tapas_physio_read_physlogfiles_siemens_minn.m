function [c, r, t, cpulse] = tapas_physio_read_physlogfiles_siemens_minn(log_files, ...
    verbose)
% reads out physiological time series and timing vector from custom-made logfiles
%   of peripheral cardiac monitoring (ECG
% or pulse oximetry)
%
%    [c, r, t, cpulse] = tapas_physio_read_physlogfiles_custom(logfiles)
%
% IN
%   log_files                   tapas.log_files; see also tapas_physio_new
%           .respiratory
%           .cardiac
%           .sampling_interval
%           .relative_start_acquisition
% OUT
%   c                   cardiac time series (ECG or pulse oximetry)
%   r                   respiratory time series
%   t                   vector of time points (in seconds)
%   cpulse              time events of R-wave peak in cardiac time series (seconds)
%
% EXAMPLE
%   [ons_secs.cpulse, ons_secs.rpulse, ons_secs.t, ons_secs.c] =
%   tapas_physio_read_physlogfiles(logfile, vendor, cardiac_modality);
%
%   See also tapas_physio_main_create_regressors
%
% Author: Lars Kasper
% Created: 2013-02-16
% Copyright (C) 2013, Institute for Biomedical Engineering, ETH/Uni Zurich.
%
% This file is part of the PhysIO toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.
%
% $Id: tapas_physio_read_physlogfiles_custom.m 538 2014-09-22 14:45:23Z kasperla $

%% read out values

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Added by A. Moreno - 01/06/2016
% From first tests in data_selection_tapas
% Adapted from "tapas_physio_read_physlogfiles_custom.m"

% Output initialization
c = [];
r = [];
t = [];
cpulse = [];

% LOAD AND DISPLAY DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

log_files.relative_start_acquisition = 0 ; % in seconds

dt = log_files.sampling_interval; % tick_time

% PULS - cardiac signal %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

puls_file = fopen(log_files.cardiac);
%s = textscan(puls_file,'%d\t%s\t%d\t%s','HeaderLines',1);
s = textscan(puls_file,'%d\t%s\t%d\t%s','HeaderLines',8);
fclose(puls_file);
acq_ticks_puls = s{1};
channel_puls = s{2};
value_puls = s{3};
signal_puls = s{4};

time_axis_puls = double(acq_ticks_puls * dt(3)); % (ticks * seconds/tick) converted to seconds

value_cpulse = zeros(length(value_puls),1);
visible_value_cpulse = zeros(length(value_puls),1);
signal_puls_num = zeros(length(signal_puls),1);
for i = 1:length(signal_puls)
    if strcmp(signal_puls{i},'PULS_TRIGGER')
        signal_puls_num(i) = max(value_puls)/2;
        visible_value_cpulse(i) = max(value_puls); % just for visualization in graphics
        value_cpulse(i) = 1; % value 1 for every PULS_TRIGGER
    elseif strcmp(signal_puls{i},'EXT1_TRIGGER')
        signal_puls_num(i) = max(value_puls);
    else % strcmp(signal_puls{i},'')
        signal_puls_num(i) = 0;
    end
end

% figure(30);
% clf;
% subplot(3,1,1);
% plot(acq_ticks_puls,value_puls,'-r','LineWidth',1);


% RESP - respiration %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

resp_file = fopen(log_files.respiration);
%s = textscan(resp_file,'%d\t%s\t%d\t%s','HeaderLines',1);
s = textscan(resp_file,'%d\t%s\t%d\t%s','HeaderLines',8);
fclose(resp_file);
acq_ticks_resp = s{1};
channel_resp = s{2};
value_resp = s{3};
signal_resp = s{4};

time_axis_resp = double(acq_ticks_resp * dt(3)); % (ticks * seconds/tick) converted to seconds

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

% subplot(3,1,2);
% plot(acq_ticks_resp,value_resp,'-g','LineWidth',1);


% Info %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

info_file = fopen(log_files.scan_timing);
%s = textscan(info_file,'%d\t%d\t%d\t%d','HeaderLines',1);
s = textscan(info_file,'%d\t%d\t%d\t%d','HeaderLines',9);
fclose(info_file);
volume_info = s{1};
slice_info = s{2};
acq_start_ticks_info = s{3};
acq_finish_ticks_info = s{4};

time_axis_info = double(acq_start_ticks_info * dt(3)); % (ticks * seconds/tick) converted to seconds

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

% subplot(3,1,3);
% plot(acq_start_ticks_info,volume_info,'b-',acq_start_ticks_info,ttl_value,'k+','LineWidth',1);


% SELECTION OF THE USEFUL DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

count = 1;
for i = 1:length(value_puls)
    if (acq_ticks_puls(i) > ttl_start_in_ticks) && (acq_ticks_puls(i) < ttl_end_in_ticks)
        cardiac_ticks(count) = acq_ticks_puls(i);
        cardiac(count) = (double(value_puls(i)));
        my_cpulse(count) = value_cpulse(i);
        count = count + 1;
    end
end
cardiac = cardiac';
my_cpulse = my_cpulse';
visible_my_cpulse = max(cardiac)*my_cpulse;
cardiac_ticks = cardiac_ticks';

%% Important %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
log_files.relative_start_acquisition = double(cardiac_ticks(1) * dt(3)); %(double(ttl_start_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
log_files.relative_start_acquisition_in_ticks = cardiac_ticks(1); %(double(ttl_start_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
%%

%time_axis_cardiac = (double(cardiac_ticks) - double(ttl_start_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
time_axis_cardiac = (double(cardiac_ticks) - double(log_files.relative_start_acquisition_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds

% figure(31);
% clf;
% subplot(3,1,1);
% plot(time_axis_cardiac,cardiac,'-r','LineWidth',1);

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

%time_axis_resp = (double(respiration_ticks) - double(ttl_start_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
time_axis_resp = (double(respiration_ticks) - double(log_files.relative_start_acquisition_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds

% subplot(3,1,2);
% plot(time_axis_resp,respiration,'-g','LineWidth',1);


%time_axis_volumes = (double(acq_start_ticks_info) - double(ttl_start_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
time_axis_volumes = (double(acq_start_ticks_info) - double(log_files.relative_start_acquisition_in_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds

% subplot(3,1,3);
% plot(time_axis_volumes,volume_info,'b-',time_axis_volumes,ttl_value,'k+','LineWidth',1);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

DEBUG = verbose.level >=3;

hasRespirationFile = ~isempty(log_files.respiration);
hasCardiacFile = ~isempty(log_files.cardiac);

if hasRespirationFile
    %r = load(log_files.respiration, 'ascii');
    r = respiration;
else 
    r = [];
end

if hasCardiacFile
    %c = load(log_files.cardiac, 'ascii');
    c = cardiac;
else 
    c = [];
end

%% resample data, if differen sampling frequencies given
%dt = log_files.sampling_interval;

hasDifferentSamplingRates = numel(dt) > 1;

if hasDifferentSamplingRates && hasCardiacFile && hasRespirationFile
    dtCardiac = dt(1);
    dtRespiration = dt(2);
    isHigherSamplingCardiac = dtCardiac < dtRespiration;
    
    nSamplesRespiration = size(r,1);
    nSamplesCardiac = size(c,1);
    
%     tCardiac = -log_files.relative_start_acquisition + ...
%         ((0:(nSamplesCardiac-1))*dtCardiac)';
%     tCardiac = time_axis_cardiac;
%     tCardiac = -log_files.relative_start_acquisition + ...  %%%%%%%% commencer à cardiac_tick(1) ??????
%         (double(cardiac_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
    tCardiac = time_axis_cardiac; % (ticks * seconds/tick) converted to seconds

%     tRespiration = -log_files.relative_start_acquisition + ...
%         ((0:(nSamplesRespiration-1))*dtRespiration)';
%     tRespiration = time_axis_resp;
%     tRespiration = -log_files.relative_start_acquisition + ...
%         (double(respiration_ticks)) * dt(3); % (ticks * seconds/tick) converted to seconds
    tRespiration = time_axis_resp; % (ticks * seconds/tick) converted to seconds
    
    if isHigherSamplingCardiac
        t = tCardiac;
        rInterp = interp1(tRespiration, r, t);
        
        if DEBUG
            fh = plot_interpolation(tRespiration, r, t, rInterp, ...
                {'respiratory', 'cardiac'});
            verbose.fig_handles(end+1) = fh;
        end
        r = rInterp;
        %% Added by A. Moreno - 02/08/2016
        % To avoid error with NaN in Butterworth filter
        r(isnan(r))=0;
        %%
        
    else
        t = tRespiration;
        cInterp = interp1(tCardiac, c, t);
        
        if DEBUG
            fh = plot_interpolation(tCardiac, c, t, cInterp, ...
                {'cardiac', 'respiratory'});
            verbose.fig_handles(end+1) = fh;
        end
        c = cInterp;
          
    end
    
else
    nSamples = max(size(c,1), size(r,1));
    t = -log_files.relative_start_acquisition + ((0:(nSamples-1))*dt)';
end

%% ADAPTATION - A. Moreno 25/07/2016
cpulse = []; % no "cpulse" for Siemens_minn (PULS_TRIGGER not reliable!)

end

%% local function to plot interpolation result
function fh = plot_interpolation(tOrig, yOrig, tInterp, yInterp, ...
    stringOrigInterp)

%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
linewidth = 1;
axesfontsize = 15;
%%

fh = tapas_physio_get_default_fig_params;
stringTitle = sprintf('Interpolation of %s signal', stringOrigInterp{1});
set(fh, 'Name', stringTitle);

%plot(tOrig, yOrig, 'go--');  hold all;
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
plot(tOrig, yOrig, 'go--', 'LineWidth', linewidth);  hold all;


%plot(tInterp, yInterp,'r.');
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
plot(tInterp, yInterp,'r.', 'LineWidth', linewidth);

xlabel('t (seconds)');
legend({
    sprintf('after interpolation to %s timing', ...
    stringOrigInterp{1}), ...
    sprintf('original %s time series', stringOrigInterp{2}) });
title(stringTitle);

%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
set(gca,'FontSize',axesfontsize)
%%

end
