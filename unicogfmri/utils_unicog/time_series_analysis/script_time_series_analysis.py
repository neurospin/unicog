# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Fri Jul 31 09:12:50 2015

@author: id983365

"""

"""
Event-related analysis

TR

INPUT / OUTPUT
INPUT
data :  raw data
        beta
        group level

mask : roi
       voxel

onsets

con

OUTPUT

average / sdt


FUNCTIONS
remove low frequence before
analysis one condtion
analysis grouping of conditions

calculer les résidus

ROI
1) extraction of data into fmri data and compute the mean
nscans * 1

2) extraction beta values and compute the mean
nscans * nb reg

3) SPM.mat : extraction of SPM.xX.X
nscans * nb reg

4) compute the Y and Y
case     Y = SPM.xX.X * beta;

5) prepare the time axis

6) prepare mean and sd
for each run in runs
 for condition in conditions
   test
   mean : add the value
   sdt : add the value


Not yet implemented : Finterest
Y = spm_FcUtil('Yc',SPM.xCon(Ic),SPM.xX.xKXs,beta);
LIKE IN STANPLOT
Finterest
%%%% The argument Finterest (usually = 1) indicates which contrast in the SPM model
%%%% refers to the F test of real interest. This F test usually has ones in columns for all
%%%% variables of interest, and zero everywhere else, e.g. for movement
%%%% regressors whose effects on the data must be subtracted out.
%%%% Specify zero (0) if you have no contrast of interest. However, note
%%%% that your plot may not be as nice as it could be (for instance, the
%%%% effects of movement might be regressed out in the SPM stats, but not
%%%% in your plot).

TO CHECK

bcov : to see

FIR


Reunion 28/07 

Conversion du stanplot

Input


Output



single subj
groupe
multigroup : comparaison groupes

pb avec stanplot pour definr les groupes

CAS single subj

timeS : y
cond / onset
-> selective avering ou FIR

donc reucp Y ou y

raw signal
rawsignal avec var nuisance enlevés
Y provenant du model FIT

-> implementaiton
y = get_raw_data(funcfiles, ROI) -> cas du voxel à traiter
(recréer une roi à partir d'une coord)
y2 = remove_nuissance_variables
onstes, conds = read_onset_onset_files (csv)
plot_fir(y, conds, onsets)
plot_avg(y, conds, onsets)

get_model_fit(SPM_mat ou autres valeurs contenant )

input

output

X : XiBi + xnBn + con 
XnBn -> varaibles nuisance


Attention affine qd extraction ROIs

B  si plusieurs sessions > moyenne


Comparaison des .dat


Modules nistat
nilearn : good
nipy : premier prjet à la dérive
nistat : new projet


Même ROIs pour tous les sujets
mais on peut faire l'instersection avec un masque du sujet
-> frederinko
liste sujet
liste locai
liste scans (betas ou con)
col roi, col suj, col signal(beta)
input ; localiser : intersction localizer/ roi

localizer puet etre un carte par ex de SPM_T
SPMT con, -> seuill SPm_T à 10-3 par ex, 3.2
intersection SPMt
defaut sjt avec bcp de voxles et d'autres non
etendu des activation sensibles aux seuils
-> donc pas bonne idee de choisi un seuil commun pour tous les sujets
autre methodes :
nvoxels (mm pour tous les sujets) les plus activées = p% de voxels activées env 20-25 %
si plus grosse ROI, % plus bas

code Christophe
-> cf code niftimasker ghtiutb nilearnissu
v1 : 1iere methode
v2 = seuil fix pour localizer
v3 = methode avec %

nop nifitmaps masker : serie images binaires

git -> code de christophe

qd  groupe

stanplot que methode 1, ajout possibilté des methodes 2 et 3

renomer les noms des methodes
get raw_data utilisr le code christophe


variables de nuissance
voir nilearn, nibabel sous forme de fichier txt, 
mm log que timeseries
et voir aussi filtrage temporel


comparaison de donner : simuler les données
generer + ajout bruit


read onset fmri -> martin


groupement des conditions
si grpmt et mis a zero -> part dans la baseline

SOA 4 secondes = pics tous les 4 secondes
-> mélanges de conditions
-> FIR régression linéaire, contribution des différentes conditions

FIR enlever l'effet de tous si on les mets tous ! [1 1 1 1 1] dans 
le groupVar

Utiliser nifitmasker qui vérifie l'affine

Correction : passer les params de realignements à la fonction
reader nibabel ou nilearn -> variables de nuisances

spm_filter reader nilearn -> see the cutoff

-- 
Bcp de basses fréquences 
SPM : cutoff à 128 par défaut
sin et cos de basse fréquence, 128s puis 2 fois, puis 4 fois 
puis regarder les résidus

--
pb autour de 0 -> baseline ?
Baseline utile mais pas forcée

--
Grp => cond, onsets
plot_fmri
noms des conditions, pas de labels avec des chiffres


manip pour merge les conditions
plot_fmri
plot_avg

d1 = dict(cd1=onset, cd2=onset)
d2=["new"] = d1[cond] + d2[cond2]

Localizer peut être 1 contraste de la manip principale,
données 1 session et utiliser sur les autres sessions. 
 
SUMMARY :

COMPARAISON OF:
pour un single subj | pour un groupe | multigroup : comparaison groupes


INPUT :
Input_1 : signal, can be
 raw signal | rawsignal avec var nuisance enlevés | Y provenant du model FIT
Input_2 : rois



timeS : y
cond / onset
-> selective avering ou FIR

donc reucp Y ou y


A VOIR:

Quand utilisation de 'c04':3 :
  File "/home/id983365/.local/lib/python2.7/site-packages/nitime/timeseries.py", line 977, in __getitem__
    return self.data[key]  # time is the last dimension
IndexError: index 177 is out of bounds for axis 1 with size 177

NiftiMasker


SCRIPT TO SHOW 

INPUT

OUTPUT :
evented related plot for unfiltered fmri signal.



"""
#GENERIC MODULES
from glob import glob
import os
import os.path as op

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

#SPECIFIC MODULES
import nibabel

from nitime import timeseries
from nitime import analysis
from nitime import viz

#UNICOG MODULES
import utils_rois



########################
# SET THE PATHS
########################
rootdir = ("/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_nitime/"
           "test_data_antonio")
os.environ['ROOTDIR'] = rootdir


#GET THE DATADIR
#datadir = utils_rois.get_rootdir()
#OR
datadir = os.path.join(os.getenv('ROOTDIR'))

save_analysis =  op.join(datadir, "times_series_analysis")     
            
########################
# ROI(s) ANALYSIS
########################
#CAS VOXEL COORDINATES 
#if rois are voxels coordinates in MNI, convert them into volume
#list_coord = []
#list_rois = utils_roi.get_volume_from_coord(list_coord, path_rois)

#CAS ROI NAMES
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
#here read the onset from a .dat file
path_onsets = op.join(datadir, 'AB130058', 'onsets/ab130058_cLSF1_bis.dat')
#conditions = {'T0':0, 'c01':1, 'c02':2, 'c04':3, 'c08':4, 'cM':5} #dic of conditions
conditions = {'c01':1, 'c02':2, 'c04':3, 'c08':4} #dic of conditions
#conditions = {'c08':4}
#conditions = {'c01':1, 'c02':2, 'c08':4}


########################
# PARAMS FOR THE ANALYZE
########################
#sampling_interval = TR value
sampling_interval = 2.4
time_unit = 's'



#SUBJECT LEVEL ANALYSIS
for r in list_rois :
    for s in list_subjs : 
        #Pattern to fetch data for each subj
        data_file = glob(datadir + "/" + s + "/fMRI/acquisition1/"
                                + "swaclsf1*.nii" )        

        #Many methods to extract data are available in utils_roi
        #Here using of NiftiMapsMasker
        path_roi = op.join(path_rois, r)
        data = utils_rois.get_data_in_roi(path_roi, data_file[0]) 

        #Filtered data ...
        #data = data_filtered(data)
      
        #INTIALIZATION
        et = []
        means = []
#        list_data_avg = []
#        list_data_se = []
        list_cd = []
        figure = plt.figure()
     
        #SAVE THE VALUES INTO DATAFRAME
        columns = ['condition_name', 
                   'condition_label', 
                   'time', 
                   'average',
                   'standart_deviation']                                        
        df_to_save = pd.DataFrame(columns=columns)
        
        for name_cond, label in conditions.iteritems():
            #get the onsets for one condition
            onsets = utils_rois.get_onsets(path_onsets, label)

            #methods available to plot data using ntime module
            analyzer = utils_rois.analyze_average(data.ravel(), onsets, 
                                       sampling_interval, 
                                       time_unit = time_unit)
#            print analyzer.eta
            et.append(analyzer.eta) 
            data_to_plot = (analyzer.eta.data)

            list_cd.append(name_cond)
#            list_data_avg.append = []
#            list_data_se.append = []
#            
            
            #fig02 = viz.plot_tseries(analyzer.FIR, ylabel='BOLD (% signal change)')            
            
            means.append(np.mean(data))
#            figure = viz.plot_tseries(
#                timeseries.TimeSeries(analyzer.eta, sampling_rate=sampling_interval, 
#                time_unit='s'), fig = figure, label=name_cond) 
#            figure = viz.plot_tseries(
#                timeseries.TimeSeries(analyzer.eta, 
#                                      sampling_rate=sampling_interval,
#                                      #time = analyzer.eta.time, 
#                                      time_unit = 's'), 
#                                      fig = figure, 
#                                      label=name_cond, 
#                                      linewidth=0.2, 
#                                      marker='+',
#                                      xdata= analyzer.eta.time
#                                      )
            if not figure.get_axes():
                ax = figure.add_subplot(1, 1, 1)
            else:
                ax = figure.get_axes()[0]
#            #ax = figure.add_subplot()
            
            #need to divide by the _conversion_factor attribute added by nitime
            time = np.array(analyzer.eta.time) / analyzer.eta.time._conversion_factor

            ax.xaxis.set_ticks(time)
            curve = ax.plot(time, analyzer.eta.data,
                    label=str(label) + ' : ' + name_cond, 
                    linewidth=0.2, 
                    marker='+',
                    xdata= time
                    )
            for_color = curve[0]
            #add sd
        
            y = analyzer.eta.data
            error = analyzer.ets.data
            ax.fill_between(time, y-error, y+error,
                alpha=0.03, edgecolor='#CC4F1B', facecolor=for_color.get_color())
            #ax.errorbar(time, analyzer.eta.data, yerr=error, linestyle="None", marker="None")

        
        
            curve = figure.axes[0]
#            curve.axis([-2, 6, 681,688])
            curve.legend()
            
            #SAVE IN DATA_FRAME
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
            print df_to_save

            
            
#            utils_rois.save_data_time_analysis(file_csv, 
#                                           time, 
#                                           name_cond,
#                                           label,
#                                           analyzer.eta.data, 
#                                           analyzer.ets.data)
       
            
            
        #plot the results: all condition for the same subj, the same rois
        #legend 
            
        #figure = viz.plot_tseries(analyzer.eta, ylabel='Bold signal', time_unit='s')       

        #select the condition for the display
#        list_data = []
#        for i, c in conditions.iteritems():
#            print i
#            print c
#            list_data.append(et[i].data)

#        data_to_plot=np.vstack(list_data)
#        print data_to_plot
        
        #Plot the data
#        figure = viz.plot_tseries(
##        timeseries.TimeSeries(data=np.vstack([et[3].data, et[4].data]),
##                  sampling_rate=et[3].sampling_rate, time_unit='s'))
#        timeseries.TimeSeries(data_to_plot,
#                              sampling_rate=sampling_interval, 
#                                time_unit='s'), axis = '-4.8' )
   
#        figure = plt.figure()
#        for plot in list_data:
#            figure = viz.plot_tseries(
#               timeseries.TimeSeries(plot, sampling_rate=sampling_interval, 
#                time_unit='s'), fig = figure, label='toto')  
#            curve = figure.axes[0]
#            curve.legend()
                                    
                                
                                
        #figure = viz.plot_tseries(timeseries.TimeSeries(data=np.vstack([et[0].data, et[1].data])), ylabel='Bold signal', time_unit='s')
#        print type(figure)
        ax = figure.get_axes()[0]
        xlim = ax.get_xlim()
        
        #add title
        conditions_name = ', '.join([key for key in conditions.iterkeys()])
#        print conditions_name
        title = 'Plot of {s}, for {roi} and the {conditions_name}'.format(s=s, roi=r, conditions_name=conditions_name)
        figure.suptitle(title)      
        
        #add legend
        xlim = ax.get_xlim()
#        print xlim
        
        #ax.plot([xlim[0], xlim[1]], [means[0], means[0]], 'b--')
        #ax.plot([xlim[0], xlim[1]], [means[1], means[1]], 'g--')
#        print figure.axes        
#        for subplot in figure.axes :
#            print subplot

        #SAVE THE PLOTS
        #matplotlib.pyplot.imsave
        conditions_name = '_'.join([key for key in conditions.iterkeys()])   
        file_name = '{s}_{roi}_{conditions_name}.png'.format(s=s, roi=r, conditions_name=conditions_name)
        #print op.join(save_analysis, file_png)        
        figure.savefig(op.join(save_analysis, '{file_name}.png'.format(file_name=file_name)))
        df_to_save.to_csv((op.join(save_analysis, '{file_name}.csv'.format(file_name=file_name))))
        plt.show() 
    



        
# save the figure to file
plt.close(figure)    # close the figure

#SAVE in pdf     
#from matplotlib.backends.backend_pdf import PdfPages
#pp = PdfPages('multipage.pdf')
#You can give the PdfPages object to savefig(), but you have to specify the format:
#plt.savefig(pp, format='pdf')
#An easier way is to call PdfPages.savefig:
#pp.savefig()
#Finally, the multipage pdf object has to be closed:
#pp.close()


        
    