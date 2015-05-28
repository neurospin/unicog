"""
This script project the coregistered fMRI images to the surface:
the surface is the grey-white matter interface of the subject

The purpose is to perform proper group analysis on the surface on fsaverage,
and use existing  atlases on the surface.

Author: Bertrand Thirion, Marie Amalric, 2013--2014

"""
import os
import glob
import commands
from nipype.interfaces.freesurfer import BBRegister
from joblib import Parallel, delayed

FWHM = 3.

# get subject list and subject informations
#subjects = ['cf120444','jl120341','lr120300','aa130114','aa130169','mk130199',
#            'jl130200','mp130263','rm130241','al130244','bm120103','ce130459',
#            'of140017','jf140025','cr140040','fm120345','hr120357','kg120369',
#            'mr120371','jc130030','ld130145','cf140022','jn140034','mv140024',
#            'tj140029','ap140030','af140169','pp140165','eb140248','gq140243']
            
subjects = ['subject01','subject02','subject03','subject04',
            'subject05','subject06','subject07','subject08',
            'subject09','subject10','subject11','subject12',
            'subject13','subject14']
#work_dir = '/neurospin/tmp/mathematicians'

#work_dir = '/neurospin/unicog/protocols/IRMf/' +\
#    'mathematicians_Amalric_Dehaene2012/Surface_analysis/mathematicians'
#spm_dir = os.path.join('/neurospin/unicog/protocols/IRMf', 
#                       'mathematicians_Amalric_Dehaene2012/fMRI_data/')

work_dir = '/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data'
spm_dir = os.path.join(work_dir,'fmri_results')

os.environ['SUBJECTS_DIR'] = ""

#do_bbr = False
do_bbr = True

def do_process_subject(subject):
    #print "Subject :", subject
#    subject_dir = os.path.join(work_dir, subject)
#    t1_dir = os.path.join(subject_dir, 't1')
#    fmri_dir = os.path.join(subject_dir, 'fmri')
#    preproc_dir = os.path.join(spm_dir,subject,'fMRI')
    
    subject_dir = os.path.join(work_dir, subject)
    t1_dir = os.path.join(subject_dir, 't1')
    fmri_dir = os.path.join(subject_dir, 'fmri_results')
    preproc_dir = os.path.join(spm_dir,subject,'data')    
    
    # warning: we are globing non-relaigned, non-coregistered data
    # this may lead to poor results
    fmri_images_ = glob.glob(
        os.path.join(preproc_dir,'ra*.nii'))
    
    fmri_images_.sort()
    fmri_images = fmri_images_ 

#    fmri_images_ = glob.glob(
#        os.path.join(preproc_dir,'audiosentence/raaudio*.nii'))
#    fmri_images_.sort()
#    fmri_images += fmri_images_
#
#    fmri_images_ = glob.glob(
#        os.path.join(preproc_dir,'localizer/ralocalizer*.nii'))
#    fmri_images_.sort()
#    fmri_images += fmri_images_
    

#    fs_dir = os.path.join(t1_dir, subject)
    fs_dir = os.path.join(work_dir, 'fs_db')
    
#    mean_bold = glob.glob(
#        os.path.join(preproc_dir,'audiosentence/meanaaudio*.nii'))[0]
#NO MEAN 
    mean_bold = glob.glob(
             os.path.join(preproc_dir,'ra*.nii'))[0]   

    #os.environ['SUBJECTS_DIR'] = t1_dir
    os.environ['SUBJECTS_DIR'] = fs_dir
    if do_bbr:
#        # use BBR registration to finesse the coregistration
#        bbreg = BBRegister(subject_id=subject, source_file=mean_bold,
#                           init='header', contrast_type='t2')
#        bbreg.run()
        
        #Use directly freesurfer commands
        regheader = mean_bold[:-4] + '_bbreg_%s.dat' % subject   
        commands.getoutput(
            '$FREESURFER_HOME/bin/bbregister --t2 --init-header --reg %s ' \ 
            '--mov %s --s %s' 
            %  (regheader, mean_bold, subject))       
    
    #regheader = mean_bold[:-4] + '_bbreg_%s.dat' % subject

    # --------------------------------------------------------------------
    # run the projection using freesurfer
            
    # take the fMRI series
            
    print "Subject :", subject
    print fmri_images
    for fmri_session in fmri_images:
        # output names
        # the .gii files will be put in the same directory as the input fMRI
        left_fmri_tex = fmri_session[:-7] + '_lh.gii' 
        right_fmri_tex = fmri_session[:-7] + '_rh.gii'
        #print left_fmri_tex, right_fmri_tex
        """
        # unzip the fMRI data
        fmri_file = fmri_session[:-3]
        f_in = open(fmri_session, 'rb')
        f_out = open(fmri_file, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        """
        # run freesrufer command   
        print "fmri_session"
        print fmri_session
        print "left_fmri_tex"
        print left_fmri_tex
        print "regheader"
        print regheader
        commands.getoutput(
            '$FREESURFER_HOME/bin/mri_vol2surf --src %s --o %s '\
                '--out_type gii --srcreg %s --hemi lh --projfrac 0.5'
            % (fmri_session, left_fmri_tex, regheader))

        commands.getoutput(
            '$FREESURFER_HOME/bin/mri_vol2surf --src %s --o %s '\
                '--out_type gii --srcreg %s --hemi rh --projfrac 0.5'
            % (fmri_session, right_fmri_tex, regheader))
        
        # delete the nii file
        #os.remove(fmri_file)
        
        left_smooth_fmri_tex = os.path.join(
            os.path.dirname(left_fmri_tex),
            's' + os.path.basename(left_fmri_tex))
        right_smooth_fmri_tex = os.path.join(
            os.path.dirname(right_fmri_tex),
            's' + os.path.basename(right_fmri_tex))
        
        print commands.getoutput(
            '$FREESURFER_HOME/bin/mri_surf2surf --srcsubject %s --srcsurfval '\
                '%s --trgsurfval %s --trgsubject ico --trgicoorder 7  '\
                '--hemi lh  --nsmooth-in 2' %
            (subject, left_fmri_tex, left_smooth_fmri_tex))
        print commands.getoutput(
            '$FREESURFER_HOME/bin/mri_surf2surf --srcsubject %s --srcsurfval '\
                '%s --trgsubject ico --trgsurfval %s --trgicoorder 7  '\
                '--hemi rh  --nsmooth-in 2' %
            (subject, right_fmri_tex, right_smooth_fmri_tex))

Parallel(n_jobs=6)(delayed(do_process_subject)(
            subject) for subject in subjects)

