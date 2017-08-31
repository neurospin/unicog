function [SliceTiming, TR, TE, SliceThickness, SpacingBetweenSlices, ...
            NumberOfSlices, PixelSpacing] ...
            = create_SliceTimingInfo_mat_from_IMA(spm_path, file_name)

% Adapted by A. Moreno (June 2017) from code created by F. Meyniel:
% https://github.com/florentmeyniel/fmspm12batch/blob/PhysioCorrection/fmspm12batch_preproc_GetSliceTiming_NS.m
%
% Function to get (and save) various acquisition parameter, such as
% RT, slice timing info... from one dicom (IMA) file. 
% The parameters are read in the header of a parciular dicom volume. 
% Note that the accuracy of the slice timing is numbers is <5ms).
% 
% Value returned:
% 	SliceTiming
% 	TR
% 	TE
% 	SliceThickness
% 	SpacingBetweenSlices
% 	NumberOfSlices
% 	PixelSpacing (inplane resolution)
% 
% Usage:
% [SliceTiming, TR, TE, SliceThickness, SpacingBetweenSlices, ...
%            NumberOfSlices, PixelSpacing] ...
%            = create_SliceTimingInfo_mat_from_IMA(spm_path, file_name)
%
% This function must be run in the directory containing the dicom file.
% 
% Example:
% > spm_path = '/i2bm/local/spm8'
% > create_SliceTimingInfo_mat_from_IMA(spm_path, 'GM160212.MR.PTX_INVIVO.0007.0002.2017.06.14.15.30.44.906250.44516476.IMA')
%
% ATTENTION: DO NOT use the first dicom file to obtain the
% 'SliceTimingInfo.mat' file.


% add spm in the path
addpath(spm_path)

% We create the 'SliceTimingInfo.mat' for the input (dicom) file

hdr = spm_dicom_headers(file_name);

% Get the timing info:
SliceTiming = hdr{1}.Private_0019_1029; % slice timing
TR = hdr{1}.RepetitionTime/1000; % Convert to seconds
TE = hdr{1}.EchoTime;            % leave in ms.
SliceThickness = hdr{1}.SliceThickness;
SpacingBetweenSlices = hdr{1}.SpacingBetweenSlices;
NumberOfSlices = hdr{1}.Private_0019_100a;
PixelSpacing = hdr{1}.PixelSpacing; % [x, y] resolution in mm

% GET TOTAL READOUT TIME
% ----------------------
% explanation can be found in several web pages:
% https://lcni.uoregon.edu/kb-articles/kb-0003
% http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/TOPUP/TopupUsersGuide
% https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=fsl;92bd6f89.1403

% BW is the effective (or "reconstructed") BW in PE direction
% nVx is the reconstructed number of line
% 1/(BW*nVx) is the effective echo time. It is indep. from the GRAPPA
% since both BW and nVx are in the reconstructed space.
% The echo time reported by Siemens is the actual echo time. The actual
% time corresponds to the effective time times the GRAPPA factor.
% To check that the computation is correct, the effective echo time can be
% compared with the actual echo time interval reported in the Siemens PDF.
% actual echo time (Siemens) = iPAT/(BW*nVx).
%
% FSL and SPM needs is the effective echo time with a minor difference:
%   SPM counts from start of first echo to end of last echo (= exactly the echo time)
%   FLS counts from the middel of first echo to end of last echo.
%
% NB: FSL (topup guide) say that we should count with the number of
% "reconstructed" echos, not the actual one (in other words, which should
% not care about the GRAPPA factor).

% get number of voxel in the encoding direction
nVx = hdr{1}.Private_0051_100b;
nVx = str2double(nVx(1:(strfind(nVx, '*')-1)));

% get "Bandwidth per pixel phase encode" in Hz
% BW = hdr{1}.Private_0019_1028;
% 
% total_readout_time_spm = 1/BW;
% total_readout_time_fsl = (nVx-1)/(BW*nVx);

% save the slice timing info
fname = fullfile(pwd, 'SliceTimingInfo.mat');

if exist(fname)
    delete(fname); fprintf('\nremove previous SliceTimingInfo.mat\n')
end
save(fname, 'SliceTiming', 'TR', 'TE', 'SliceThickness', 'SpacingBetweenSlices', ...
    'NumberOfSlices', 'PixelSpacing');

end