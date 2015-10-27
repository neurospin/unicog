def Plot_groupERF_fnc(wdir, ListCond, ListSubj):

    ################################################
    # test input
    #wdir       = "/neurospin/meg/meg_tmp/tools_tmp/MEG_DEMO_SOMAWF"
    #ListSubject  = ['pf120155','pe110338','cj100142','jm100042','jm100109','sb120316',
    #            'tk130502', 'sl130503', 'rl130571','bd120417','rb130313', 'mp140019']
    #                 
    #ListCondition = ('PSS_Vfirst', 'PSS_Afirst')
    ###############################################
    
    import os
    import mne
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    cwd = os.path.dirname(os.path.abspath(__file__)) # where the scripts are
    os.chdir(cwd)

    ###############################################################################################
    ################################## SUBFUNCTIONS ###############################################
    ###############################################################################################
    def GDAVG(wdir, ListCondition , ListSubject):
        
        GrandAverages = []
        for c,cond in enumerate(ListCondition):
            
            Evokeds = []
            for s,subject in enumerate(ListSubject):
                
                EvokedPath = wdir + '/data/epochs/' + subject + '_' + cond + '-ave.fif'
                Evokeds.append(mne.read_evokeds(EvokedPath)[0])
            GrandAverages.append(mne.grand_average(Evokeds))
            
        return GrandAverages

###############################################################################################
####################################### MAIN ##################################################  
###############################################################################################
    PlotDir = wdir + '/plots/'

    GrandAverages = GDAVG(wdir, ListCondition , ListSubject)
    mne.viz.plot_topo(GrandAverages)
    plt.savefig(PlotDir + 'TOPOS_' + ListCondition[0] + ListCondition[1], '.png')
    
    GrandAverages[0].plot_topomap()
    plt.savefig(PlotDir + 'TOPOMAP_' + ListCondition[0], '.png')
    
    GrandAverages[1].plot_topomap()
    plt.savefig(PlotDir + 'TOPOMAP_' + ListCondition[1], '.png')
    
    (GrandAverages[0] - GrandAverages[1]).plot_topomap()
    plt.savefig(PlotDir + 'TOPOMAP_DIFF__' + ListCondition[0] + ListCondition[1], '.png')
 
 

    





