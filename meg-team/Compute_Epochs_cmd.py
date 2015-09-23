# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:05:33 2015

@author: bgauthie
"""
################################################
# test input
#Condition = {'PSS_Vfirst': 22, 'PSS_Afirst':21}
#Subject = 'sl130503'
#listRun = ('phase1','phase2','phase3')
################################################

import os
import mne
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mne.minimum_norm import (make_inverse_operator, apply_inverse)

os.chdir('/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF/functions')
import recode_events as rc

os.environ['SUBJECTS_DIR'] = '/neurospin/meg/meg_tmp/MTT_MEG_Baptiste/mri'
os.environ['MNE_ROOT']     = '/neurospin/local/mne'

###############################################################################################
################################## SUBFUNCTIONS ###############################################
###############################################################################################
def EPOCHING(wdir, Condition, Subject, Run):

    # temp
    tmin  = -0.3
    tmax  = 1
    decim = 4
    reject = dict(grad=4000e-13, mag=4e-12)
    
    # load trans_sss data, low-pass filtering 45Hz
    ListRun = [wdir + '/data/maxfilter/' + Subject + '/' + Subject + '_' + x + '_trans_sss_filt140_raw.fif' for x in Run]      
    raw           = mne.io.Raw(ListRun, preload = True)
    raw.filter(l_freq = None, h_freq=45, method = 'iir', n_jobs=3)
    
    # define (mandatory) and recode events (optional)
    eventsb       = mne.find_events(raw,stim_channel ='STI101', shortest_event = 1)
    events        = rc.recode_events(eventsb)
    
    # cleaning, epoching
    picks   = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=True, include=[], exclude=[])
    epochs  = []
    evokeds = [] 
    for i,cond in enumerate(Condition):
        epochs.append(mne.Epochs(raw, events, Condition[cond], tmin, tmax, picks=picks, baseline = [tmin, 0], decim = decim, reject=reject, preload = True))
    
    # equalizing trial number across conditions
    mne.epochs.equalize_epoch_counts(epochs)
    
    # averaging
    for i,cond in enumerate(Condition):
        evokeds.append(epochs[i].average())
    
    return epochs, evokeds

###############################################################################################
###############################################################################################
def INVERSE(wdir, Subject, epoch, evokeds):

    # compute noise covariance from empty room data
    emptyroom_raw = mne.io.Raw(wdir + '/data/maxfilter/' + Subject + '/'+ Subject +'_empty_sss.fif')  
    noise_cov     = mne.compute_raw_data_covariance(emptyroom_raw)
    
    # compute dSPM solution
    fname_fwd     = wdir + '/data/forward/' + Subject + '/' + Subject + '_phase1_trans_sss_filt140_raw-ico5-fwd.fif'
    forward       = mne.read_forward_solution(fname_fwd, surf_ori=True)
    
    # create inverse operator
    inverse_operator = make_inverse_operator(epoch.info, forward, noise_cov, loose=0.4, depth=0.8)
    
    # Compute inverse solution
    snr = 3.0
    lambda2 = 1.0 / snr ** 2
    
    stcs = []
    for evoked in evokeds:
        stcs.append(apply_inverse(evoked, inverse_operator, lambda2, method='dSPM', pick_ori = None))
    
    # save a covariance picture for visual inspection
    mne.viz.plot_cov(noise_cov, epoch.info, colorbar=True, proj=True,show_svd=False,show=False)
    plt.savefig(wdir + "/plots/" + Subject + "_covmat")
    plt.close()
    
    return stcs
    	 
###############################################################################################
####################################### ARGUMENT PARSING ######################################
###############################################################################################
import argparse 
import sys
  
# define the argument you need to pass in command line
parser = argparse.ArgumentParser(description = 'test')     
parser.add_argument('-wdir'   ,type=str , nargs='*')
parser.add_argument('-subject',type=str , nargs='*')
parser.add_argument('-cond1'  ,type=str , nargs='*')
parser.add_argument('-cond2'  ,type=str , nargs='*')
parser.add_argument('-trig1'  ,type=int , nargs='*')           
parser.add_argument('-trig2'  ,type=int , nargs='*') 
# here you can input arguments in series that will be concatenated in a list
parser.add_argument('-runlist',metavar='runlist',type=str , nargs='+') 

# inputed argument transformed in a dict-like structure
args = vars(parser.parse_args())

wdir      = args['wdir'][0]
Subject   = args['subject'][0]
Condition = {str(args['cond1']):args['trig1'],str(args['cond2']):args['trig2']}
listRun   = args['runlist']

# to check the formatting and content of arguments
print >> sys.stderr, listRun
print >> sys.stderr, Subject
print >> sys.stderr, wdir

# call processing subfunctions
epochs, evokeds = EPOCHING(wdir, Condition, Subject, listRun)
stcs            = INVERSE(wdir, Subject, epochs[0], evokeds)

# save final results
for i, cond in enumerate(Condition):
		epochs[i].save(wdir + '/data/epochs/' + Subject + '_' + cond + '-epo.fif')
		evokeds[i].save(wdir + '/data/epochs/' + Subject + '_' + cond + '-ave.fif')
		stcs[i].save(wdir + '/data/stc/' + Subject + '_' + cond)	    







