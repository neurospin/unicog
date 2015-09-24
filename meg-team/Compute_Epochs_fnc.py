def Compute_Epochs_fnc(wdir, Condition, Subject):

	################################################
#	# test input
#	wdir       = "/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF"
#	Condition  = ['PSS_Vfirst', 'PSS_Afirst']
#	Subject    = 'sl130503'
	 ###############################################

	import os
	import mne
	import matplotlib
 	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	from mne.minimum_norm import (make_inverse_operator, apply_inverse)

	cwd = os.path.dirname(os.path.abspath(__file__)) # where the scripts are
	os.chdir(cwd)
	import recode_events as rc


###############################################################################################
################################## SUBFUNCTIONS ###############################################
###############################################################################################
	def EPOCHING(wdir, Condition, Subject):

		# import parameters from configuration file
        	from configuration import ( tmin, tmax,
                            		decim, reject,
                            		fmin, fmax,
                            		tmin_bsl, tmax_bsl,
                            		ListRunPerSubject, ListTrigger)
  
		# load trans_sss data, low-pass filtering 45Hz
		ListRun = [wdir + '/data/maxfilter/' + Subject + '/' + Subject + '_' + x + '_trans_sss_filt140_raw.fif' for x in ListRunPerSubject[Subject]]      
		raw           = mne.io.Raw(ListRun, preload = True)
		raw.filter(l_freq = fmin, h_freq=fmax, method = 'iir', n_jobs=3)

		# define (mandatory) and recode events (optional)
		eventsb       = mne.find_events(raw,stim_channel ='STI101', shortest_event = 1)
		events        = rc.recode_events(eventsb)

		# cleaning, epoching
		picks   = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=True, include=[], exclude=[])
		epochs  = []
		evokeds = [] 
		for i,cond in enumerate(Condition):
			epochs.append(mne.Epochs(raw, events, ListTrigger[cond], tmin, tmax, picks=picks, baseline = [tmin_bsl, tmax_bsl], decim = decim, reject=reject, preload = True))

		# equalizing trial number across conditions
		mne.epochs.equalize_epoch_counts(epochs)

		# averaging
		for i,cond in enumerate(Condition):
			evokeds.append(epochs[i].average())

		return epochs, evokeds

###############################################################################################
        def INVERSE(wdir, Subject, epoch_info, evokeds):

		# import parameters from configuration file
        	from configuration import ( lambda2, method )

		# compute noise covariance from empty room data
		emptyroom_raw = mne.io.Raw(wdir + '/data/maxfilter/' + Subject + '/'+ Subject +'_empty_sss.fif')  
		noise_cov     = mne.compute_raw_data_covariance(emptyroom_raw)

		# compute dSPM solution
		fname_fwd     = wdir + '/data/forward/' + Subject + '/' + Subject + '_phase1_trans_sss_filt140_raw-ico5-fwd.fif'
		forward       = mne.read_forward_solution(fname_fwd, surf_ori=True)

		# create inverse operator
		inverse_operator = make_inverse_operator(epoch_info, forward, noise_cov, loose=0.4, depth=0.8)

		# Compute inverse solution
		stcs = []
		for evoked in evokeds:
			stcs.append(apply_inverse(evoked, inverse_operator, lambda2, method=method, pick_ori = None))

		# save a covariance picture for visual inspection
		mne.viz.plot_cov(noise_cov, epoch_info, colorbar=True, proj=True,show_svd=False,show=False)
		plt.savefig(wdir + "/plots/" + Subject + "_covmat")
		plt.close()

		return stcs
	 
###############################################################################################
####################################### MAIN ##################################################  
###############################################################################################

	epochs, evokeds = EPOCHING(wdir, Condition, Subject)
	stcs            = INVERSE(wdir, Subject, epochs[0].info, evokeds)

	for i, cond in enumerate(Condition):
		epochs[i].save(wdir + '/data/epochs/' + Subject + '_' + cond + '-epo.fif')
		evokeds[i].save(wdir + '/data/epochs/' + Subject + '_' + cond + '-ave.fif')
		stcs[i].save(wdir + '/data/stc/' + Subject + '_' + cond)	    

    





