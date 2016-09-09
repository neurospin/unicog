function fh = tapas_physio_plot_cropped_phys_to_acqwindow(ons_secs, sqpar)
% plot parts of the time series to be processed into regressors
%
% USAGE
%   fh = tapas_physio_plot_cropped_phys_to_acqwindow(ons_secs, sqpar, y)
%
% INPUT
%   ons_secs    - output of tapas_physio_crop_scanphysevents_to_acq_window
%   sqpar       - output of tapas_physio_crop_scanphysevents_to_acq_window
%
% OUTPUT
%   fh          figure handle of output figure
%
% Author: Lars Kasper
%
% Copyright (C) 2013, Institute for Biomedical Engineering, ETH/Uni Zurich.
%
% This file is part of the PhysIO toolbox, which is released under the terms of the GNU General Public
% Licence (GPL), version 3. You can redistribute it and/or modify it under the terms of the GPL
% (either version 3 or, at your option, any later version). For further details, see the file
% COPYING or <http://www.gnu.org/licenses/>.
%
% $Id: tapas_physio_plot_cropped_phys_to_acqwindow.m 763 2015-07-14 11:28:57Z kasperla $

%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
linewidth = 1;
axesfontsize = 15;
%%

[fh, MyColors] = tapas_physio_get_default_fig_params();
set(fh,'Name','Cutout actual scans - all events and gradients');

Ndummies    = sqpar.Ndummies;
Nslices     = sqpar.Nslices;
sampling    = 1;

%% 1. Plot uncropped data
t        = ons_secs.raw.t;
cpulse      = ons_secs.raw.cpulse;
r           = ons_secs.raw.r;
c           = ons_secs.raw.c;
spulse      = ons_secs.raw.spulse;
svolpulse   = ons_secs.raw.svolpulse;

hasCardiacData = ~isempty(c);
hasRespData = ~isempty(r);

maxValc = max(abs(c));
maxValr = max(abs(r));
if hasCardiacData && hasRespData
    maxVal = maxValc; % max(maxValc, maxValr);
elseif hasCardiacData
    maxVal = maxValc;
else
    maxVal = maxValr;
end

ampsv = maxVal*1;
amps = maxVal*0.8; % maxVal / 3;
ampc = maxVal*1.2; % maxVal / 2;

y = [r, c];
x = y (1:sampling:end, :);
%stem(spulse(1:Ndummies*Nslices),amps*ones(Ndummies*Nslices,1),'r--');
%% Added by A. Moreno - 04/07/2016
stem(spulse(1:Ndummies*Nslices),amps*ones(Ndummies*Nslices,1),'r--', 'LineWidth', linewidth);
hold on;
%stem(svolpulse(Ndummies+1:end),ampsv*ones(length(svolpulse)-Ndummies,1),'--g', 'LineWidth',2);
%% Added by A. Moreno - 04/07/2016
stem(svolpulse(Ndummies+1:end),ampsv*ones(length(svolpulse)-Ndummies,1),'--g', 'LineWidth', linewidth);
%stem(spulse((Ndummies*Nslices+1):end), amps*ones(length(spulse)-Ndummies*Nslices,1), 'c--') ;
%% Added by A. Moreno - 04/07/2016
stem(spulse((Ndummies*Nslices+1):end), amps*ones(length(spulse)-Ndummies*Nslices,1), 'c--', 'LineWidth', linewidth) ;

if hasCardiacData
    %stem(cpulse, ampc*ones(length(cpulse),1), 'm--') ;
    %% Added by A. Moreno - 04/07/2016
    stem(cpulse, ampc*ones(length(cpulse),1), 'm--', 'LineWidth', linewidth) ;
end
%plot(t(1:sampling:end), x, '--');
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
plot(t(1:sampling:end), x, '--', 'LineWidth', linewidth);
set(gca,'FontSize',axesfontsize)
%%

%% 2. Plot cropped data

t           = ons_secs.t;
cpulse      = ons_secs.cpulse;
r           = ons_secs.fr;
c           = ons_secs.c;
spulse      = ons_secs.spulse;
svolpulse   = ons_secs.svolpulse;


hs = zeros(1,0);

%plot physiological time courses and scan events
if hasRespData
    hs(end+1) = plot(t,r,'ko');
else
    hs(end+1) = plot(t,c,'ko');
end

y = [c, r];
x = y (1:sampling:end, :);
%hs(end+1) = stem(spulse(1:Ndummies*Nslices),amps*ones(Ndummies*Nslices,1),'r');
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
hs(end+1) = stem(spulse(1:Ndummies*Nslices),amps*ones(Ndummies*Nslices,1),'r', 'LineWidth', linewidth);
hold on;
%hs(end+1) = stem(svolpulse(Ndummies+1:end),ampsv*ones(length(svolpulse)-Ndummies,1),'g', 'LineWidth',2);
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
hs(end+1) = stem(svolpulse(Ndummies+1:end),ampsv*ones(length(svolpulse)-Ndummies,1),'g', 'LineWidth',linewidth);
%hs(end+1) = stem(spulse((Ndummies*Nslices+1):end), amps*ones(length(spulse)-Ndummies*Nslices,1), 'c') ;
%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
hs(end+1) = stem(spulse((Ndummies*Nslices+1):end), amps*ones(length(spulse)-Ndummies*Nslices,1), 'c', 'LineWidth', linewidth) ;

%% Added by A. Moreno - 04/07/2016
% To improve figures visualization
set(gca,'FontSize',axesfontsize)
%%


%%


if hasCardiacData
    %hs(end+1) = stem(cpulse, ampc*ones(length(cpulse),1), 'm') ;
    %% Added by A. Moreno - 04/07/2016
    % To improve figures visualization
    hs(end+1) = stem(cpulse, ampc*ones(length(cpulse),1), 'm', 'LineWidth', linewidth) ;

end

for iLine = 1:size(x,2)
    %hs(end+1) = plot(t(1:sampling:end), x(:,iLine), '-')';
    %% Added by A. Moreno - 04/07/2016
    % To improve figures visualization
    hs(end+1) = plot(t(1:sampling:end), x(:,iLine), '-', 'LineWidth', linewidth)';
end

xlabel('t (s)'); ylabel('Amplitude (a. u.)');
title('Cutout region for physiological regressors');

%% Changed by A. Moreno - 04/07/2016
ylim(1.4*maxVal*[-1 1]);

if hasCardiacData && hasRespData
    
    legend( hs, {
        'used respiratory signal', ...
        ['dummy scan event marker (N = ' int2str(Ndummies*Nslices) ')'], ...
        ['volume event marker (N = ' int2str(length(svolpulse)-Ndummies) '), without dummies'], ...
        ['scan event marker (N = ' int2str(length(spulse)-Ndummies*Nslices) ')'], ...
        ['cardiac pulse (heartbeat) marker (N = ' int2str(length(cpulse)) ')'], ...
        'cardiac signal', 'respiratory signal'}, 'Location', 'southeast'); %% 'Location' added by A. Moreno - 04/07/2016
elseif hasCardiacData
    legend( hs, {
        'used cardiac signal', ...
        ['dummy scan event marker (N = ' int2str(Ndummies*Nslices) ')'], ...
        ['volume event marker (N = ' int2str(length(svolpulse)-Ndummies) '), without dummies'], ...
        ['scan event marker (N = ' int2str(length(spulse)-Ndummies*Nslices) ')'], ...
        ['cardiac pulse (heartbeat) marker (N = ' int2str(length(cpulse)) ')'], ...
        'cardiac signal'}, 'Location', 'southeast'); %% 'Location' added by A. Moreno - 04/07/2016
else % only respData
    legend( hs, {
        'used respiratory signal', ...
        ['dummy scan event marker (N = ' int2str(Ndummies*Nslices) ')'], ...
        ['volume event marker (N = ' int2str(length(svolpulse)-Ndummies) '), without dummies'], ...
        ['scan event marker (N = ' int2str(length(spulse)-Ndummies*Nslices) ')'], ...
        'respiratory signal'}, 'Location', 'southeast'); %% 'Location' added by A. Moreno - 04/07/2016
end

%ylim(1.4*maxVal*[-1 1]);
