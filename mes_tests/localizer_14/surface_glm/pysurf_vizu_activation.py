print(__doc__)

from surfer import Brain
import os

os.environ['SUBJECTS_DIR'] = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"

"""
Bring up the visualization window.
"""
brain = Brain("fsaverage", "lh", "inflated")

"""
Get a path to the overlay file.
"""
#overlay_file = "/volatile/depot_pysurfer/PySurfer/examples/example_data/lh.sig.nii.gz"
#overlay_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/subject01/audio-video_z_map_lh.gii"
overlay_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fmri_results/subject01/res_stats/z_maps/subject01audio-video.nii.gz"
#overlay_file = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db/fsaverage/surf/lh.curv"
"""
Display the overlay on the surface using the defaults to control thresholding
and colorbar saturation.  These can be set through your config file.
"""
#brain.add_overlay(overlay_file)
#brain.add_contour_overlay(overlay_file)


"""
You can then turn the overlay off.
"""
#brain.overlays["sig"].remove()


"""
Now add the overlay again, but this time with set threshold and showing only
the positive activations.
"""
#brain.add_overlay(overlay_file, min=5, max=20, sign="pos")
brain.add_overlay(overlay_file, min=2, max=12)
brain.show_view('lateral')