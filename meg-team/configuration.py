###########################################################
################## CONFIGURATION FILE #####################
###########################################################

# This script contains all the parameters needed for the different steps of analysis.
# It has to be imported at the beginning of analysis script.


# PATHS ###########################################
wdir         = "/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF" 

# EPOCHING ########################################

tmin  = -0.3 		# tmin of the epoch
tmax  = 1 		# tmin of the epoch
decim = 4 		# decimation parameter
reject = dict(grad=4000e-13, mag=4e-12) # bad epoch rejection

tmin_bsl = tmin		# tmin for the baseline
tmax_bsl = 0		# tmax for the baseline

fmin = None		# high pass filtering
fmax = 45		# low pass filtering

ListRunPerSubject = {'pf120155' : ['phase1','phase2','phase3'],
                     'pe110338' : ['phase1','phase2'],
                     'cj100142' : ['phase1','phase2','phase3'],
                     'jm100042' : ['phase1','phase2','phase3'],
                     'jm100109' : ['phase1','phase2','phase3'],
                     'sb120316' : ['phase1','phase2','phase3'],
                     'tk130502' : ['phase1','phase1bis','phase3'],
                     'sl130503' : ['phase1','phase2','phase3'],
                     'rl130571' : ['phase1','phase2','phase3'],
                     'bd120417' : ['phase1','phase2','phase3'],
                     'rb130313' : ['phase1','phase2','phase3'],
                     'mp140019' : ['phase1','phase2','phase3']}      
                       

ListTrigger = {'PSS_Vfirst': 22, 'PSS_Afirst':21,
              'JND1_Vfirst': 12, 'JND1_Afirst':11,
              'JND2_Vfirst': 32, 'JND2_Afirst':31} # trigger

# INVERSE SOLUTION ################################
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = 'dSPM'
