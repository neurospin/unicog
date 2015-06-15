print(__doc__)

import os
from surfer import Brain, project_volume_data

os.environ['SUBJECTS_DIR'] = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"


"""
Bring up the visualization window.
"""
brain = Brain("fsaverage", "lh", "inflated")

"""
Get a path to the volume file.
"""
#volume_file = "example_data/zstat.nii.gz"
volume_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fmri_results/subject01/res_stats/z_maps/subject01audio-video.nii.gz"

"""
There are two options for specifying the registration between the volume and
the surface you want to plot on. The first is to give a path to a
Freesurfer-style linear transformation matrix that will align the statistical
volume with the Freesurfer anatomy.

Most of the time you will be plotting data that are in MNI152 space on the
fsaverage brain. For this case, Freesurfer actually ships a registration matrix
file to align your data with the surface.
"""
reg_file = os.path.join(os.environ["FREESURFER_HOME"],
                        "average/mni152.register.dat")
#print reg_file
#print volume_file
#tmp = "/neurospin/unicog/protocols/IRMf/Tests_Isa/tmp/tmp_reg.nii"
zstat = project_volume_data(volume_file, "lh", reg_file)
project_volume_data()

"""
Note that the contours of the fsaverage surface don't perfectly match the
MNI brain, so this will only approximate the location of your activation
(although it generally does a pretty good job). A more accurate way to
visualize data would be to run the MNI152 brain through the recon-all pipeline.

Alternatively, if your data are already in register with the Freesurfer
anatomy, you can provide project_volume_data with the subject ID, avoiding the
need to specify a registration file.

By default, 3mm of smoothing is applied on the surface to clean up the overlay
a bit, although the extent of smoothing can be controlled.
"""
#volume_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/tmp/map_subject01_To_Fsaverage.nii"

#zstat = project_volume_data(volume_file, "lh",
#                            subject_id="fsaverage", smooth_fwhm=0.5)

"""
Once you have the statistical data loaded into Python, you can simply pass it
to the `add_overlay` method of the Brain object.
"""
#/tmp/pysurfer-v2sRxmtk9.mgz
#/tmp/pysurfer-v2sWqEIhe.mgz
#brain.add_overlay('/tmp/pysurfer-v2s0PkvNj.mgz', min=2, max=12)
brain.add_overlay(zstat, min=2, max=12)

"""
It can also be a good idea to plot the inverse of the mask that was used in the
analysis, so you can be clear about areas that were not included.

It's good to change some parameters of the sampling to account for the fact
that you are projecting binary (0, 1) data.
"""
#mask_file = "example_data/mask.nii.gz"
#mask = project_volume_data(mask_file, "lh", subject_id="fsaverage",
#                           smooth_fwhm=0, projsum="max").astype(bool)
#mask = ~mask
#brain.add_data(mask, min=0, max=10, thresh=.5,
#               colormap="bone", alpha=.6, colorbar=False)

#brain.show_view("medial")
brain.show_view()
path = "/neurospin/unicog/protocols/IRMf/Tests_Isa/git_depot/unicog/mes_tests/localizer_14/surface_glm/snapshot"
brain.save_image(os.path.join(path, 'activation_map_audio_video.png'))



