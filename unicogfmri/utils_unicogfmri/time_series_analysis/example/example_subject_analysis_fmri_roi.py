# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 09:12:50 2015

@author: id983365
"""

# GENERIC MODULES
from __future__ import division
from glob import glob
import os
import os.path as op

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# SPECIFIC MODULES
from nilearn.masking import apply_mask
import nibabel
from nitime import timeseries
from nitime import analysis
from nitime import viz

# UNICOG MODULES
from unicogfmri.utils_unicog.utils import utils


########################
# SET THE PATHS
########################
# GET THE DATADIR
# datadir = utils.get_rootdir()

# OR
datadir = os.getenv('ROOTDIR')
datadir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_nitime/test_data_antonio'
save_analysis = op.join(datadir, "times_series_analysis")     
            
########################
# ROI(s) ANALYSIS
########################
# CAS VOXEL COORDINATES 
# if rois are voxels coordinates in MNI, convert them into volume
# list_coord = []
# list_rois = utils.get_volume_from_coord(list_coord, path_rois)

# CAS ROI NAMES
path_rois = op.join(datadir, "ROIs_analyses")
list_rois = ['pSTS_Pallier_2011.nii']




########################
# SUBJECT(s) SELECTION
########################
list_subjs = ['AB130058']

########################
# CONDITION(s) SELECTION
# IN THIS EXAMPLE
# 0 = T0 (target, sentence indicating to push on the button)
# 1 = c01 (liste de signes)
# 2 = c02
# 3 = c04
# 4 = c08 (phrases de 8 signes)
########################
# Here read the onset from a .dat file
path_onsets = op.join(datadir, 'AB130058', 'onsets/ab130058_cLSF1_bis.dat')
# conditions = {'T0':0, 'c01':1, 'c02':2, 'c04':3, 'c08':4, 'cM':5} #dic of conditions
conditions = {'c01':1, 'c02':2, 'c04':3, 'c08':4} #dic of conditions

########################
# PARAMS FOR THE ANALYZE
########################
# sampling_interval = TR value
sampling_interval = 2.4
time_unit = 's'

# SUBJECT LEVEL ANALYSIS
for r in list_rois :
    for s in list_subjs : 
        # Pattern to fetch data for each subj
        data_file = glob(datadir 
                        + "/" 
                        + s 
                        + "/fMRI/acquisition1/"
                        + "swaclsf1*.nii" )        

        # Many methods to extract data are available in utils
        # Here using of NiftiMapsMasker
        path_roi = op.join(path_rois, r)
        data = utils.get_data_in_roi(path_roi, data_file[0]) 

        data2= apply_mask(data_file[0], path_roi)

        print "data"
        print data[:10]
        print "data2"
        print data2[:10]
        print data.shape
        print data2.shape

        # Filtered data ...
        #data = data_filtered(data)
      
        # Initialization
        means = []
        figure = plt.figure()
     
        # Create the dataframe
        columns = ['condition_name', 
                   'condition_label', 
                   'time', 
                   'average',
                   'standart_deviation']                                        
        df_to_save = pd.DataFrame(columns=columns)
        
        for name_cond, label in conditions.iteritems():
            # get the onsets for one condition
            onsets = utils.get_onsets(path_onsets, label)

            # methods available to plot data using ntime module
            analyzer = utils.analyze_average(
                                    data.ravel(), 
                                    onsets, 
                                    sampling_interval, 
                                    time_unit = time_unit)       
            
            if not figure.get_axes():
                ax = figure.add_subplot(1, 1, 1)
            else:
                ax = figure.get_axes()[0]
            
            # need to divide by the _conversion_factor attribute added by nitime
            time = np.array(analyzer.eta.time) / analyzer.eta.time._conversion_factor
            ax.xaxis.set_ticks(time)
            
            # plot the data
            plot = ax.plot(time, analyzer.eta.data,
                    label=str(label) + ' : ' + name_cond, 
                    linewidth=0.2, 
                    marker='+',
                    xdata= time
                    )
            plot_color = plot[0]
            
            #add sd              
            y = analyzer.eta.data
            error = analyzer.ets.data
            ax.fill_between(time, y-error, y+error,
                alpha=0.03, edgecolor='#CC4F1B', 
                facecolor=plot_color.get_color())
            #ax.errorbar(time, analyzer.eta.data, yerr=error, linestyle="None", marker="None")

            #add means  
#            mean = np.mean(analyzer.eta.data)
#            xlim = ax.get_xlim()
#            ax.plot([xlim[0], xlim[1]], [mean, mean], plot_color.get_color())
        
            # display the legend of the plot
            curve = figure.axes[0]
            curve.legend()
            
            # save in dataframe
            to_save ={'condition_name': [name_cond for i in range(len(time))],
                    'condition_label': [label for i in range(len(time))],
                    'time': time.tolist(),
                    'average': analyzer.eta.data.tolist(),
                    'standart_deviation': analyzer.ets.data.tolist()}
            df = pd.DataFrame(to_save, columns=['condition_name', 
                                             'condition_label', 
                                             'time', 
                                             'average',
                                             'standart_deviation'])
            df_to_save = df_to_save.append(df)

                              
        # All plot are now displayed
        # So, add the title
        conditions_name = ', '.join([key for key in conditions.iterkeys()])
        title = 'Plot of {s}, for {roi} and the {conditions_name}'.format(s=s, roi=r, conditions_name=conditions_name)
        figure.suptitle(title)      
        
        # Save the plots and values
        print "\n### RESULTS"
        conditions_name = '_'.join([key for key in conditions.iterkeys()])   
        file_name = '{s}_{roi}_{conditions_name}'.format(s=s, roi=r, conditions_name=conditions_name)

        save_analysis_file = op.join(save_analysis, '{file_name}.png'.format(file_name=file_name))
        figure.savefig(save_analysis_file)
        print "\nView the plots in {file_name}".format(file_name=save_analysis_file)        
        
        df_to_save_file = op.join(save_analysis, '{file_name}.csv'.format(file_name=file_name))
        df_to_save.to_csv(df_to_save_file)
        print "\nView the results in the dataframe located in {file_name}".format(file_name=df_to_save_file)
        plt.show() 
    
        # Close the plots
        plt.close(figure)


        
    