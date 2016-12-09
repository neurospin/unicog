%% Convert from .dat to .mat

datname = 'onsets_ns110383_localizer';

data = dlmread(sprintf('%s.dat',datname)); 
output = sprintf('%s.mat',datname);

conds = data(:,1);
%names = unique(conds);
names = unique(conds)'; % transposed - AM 17/09/2012

for i=1:length(names)
  name_i = names(i);
  onsets{i} = data(find(conds==name_i),2);
  durations{i} = data(find(conds==name_i),3);
  names_str{i} = num2str(names(i)); % AM 17/09/2012
end

%names = num2cell(names); % convert in cell array
names = names_str; % AM 17/09/2012
save(output,'names','onsets','durations')
