# 4096 code for Vfirst (red button), 8192 code for A first (green button)
def recode_events(eventsb):
    
    from copy import deepcopy

    events = deepcopy(eventsb) #Locked by default on the visual stimulus

    for n in range(1,len(eventsb)):
		# For an ISI = PSS, the subject perceived the auditory stim first
		if(eventsb[n][2]==8192 and eventsb[n-1][2]==65): 
			 events[n-1][2]=21
		# For an ISI = PSS, the subject perceived the visual stim first
		elif(eventsb[n][2]==4096 and eventsb[n-1][2]==65): #pss Vfirst
			 events[n-1][2]=22
		# For an ISI = JND1, the subject perceived the auditory stim first
		elif(eventsb[n][2]==8192 and eventsb[n-1][2]==66): #jnd1
			 events[n-1][2]=11
		# For an ISI = JND1, the subject perceived the visual stim first
		elif(eventsb[n][2]==4096 and eventsb[n-1][2]==66): #jnd1
			 events[n-1][2]=12
		# For an ISI = JND2, the subject perceived the auditory stim first
		elif(eventsb[n][2]==8192 and eventsb[n-1][2]==67): #jnd2
			 events[n-1][2]=31
		# For an ISI = JND2, the subject perceived the visual stim first
		elif(eventsb[n][2]==4096 and eventsb[n-1][2]==67): #jnd2
			 events[n-1][2]=32

    return events
