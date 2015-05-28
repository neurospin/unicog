
import numpy as np
import glob
import os.path

from freesurfer.freesurferMeshToAimsMesh import freesurferMeshToAimsMesh
from freesurfer.regularizeMeshFromIsin import regularizeMesh
from freesurfer.regularizeTexture import regularizeTexture
from soma import aims

subjects = ['subject01', 'subject02', 'subject03', 'subject04',
            'subject05', 'subject06', 'subject07', 'subject08',
            'subject09', 'subject10', 'subject11', 'subject12',
            'subject13', 'subject14'][:1]
hemispheres = ['l', 'r']            
fs_dir = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fs_db"

def conversionAimsMesh(mesh_input, mesh_output):
    mesh_to_read = aims.read(mesh_input)
    trm_array =  np.array([[-1, 0, 0, 0], [0, -1, 0, 0],[0, 0, -1, 0], [0, 0, 0, 1]])
    trm = aims.Motion(trm_array)
    aims.SurfaceManip.meshTransform(mesh_to_read, trm)
    aims.write(mesh_to_read, mesh_output)


#for s in subjects:
#    print s
#    anat = os.path.join(fs_dir, s, 'mri','orig_from_mgz.nii' )    
#    for h in hemispheres:
#        mesh = os.path.join(fs_dir, s, 'surf', h + 'h.inflated.gii')
#        output_mesh = os.path.join(fs_dir, s, 'surf', h + 'h.inflated2_aims.gii')
#        freesurferMeshToAimsMesh(mesh, anat, output_mesh)

fs_dir = "/neurospin/unicog/protocols/IRMf/Karla_Isa_Test_Analyse/Brainvisa/base_donnees_test_FS"
s = "subject01"
isin = os.path.join(fs_dir, s, 'surf', 'lh.isin')
lh_white = os.path.join(fs_dir, s, 'surf', 'lh.white.gii')
tex = os.path.join(fs_dir, s, 'surf', 'audio-video_z_map_lh.gii') 
r_tex=  os.path.join(fs_dir, s, 'surf', 'raudio-video_z_map_lh.gii')
regularizeTexture (isin, lh_white, tex, r_tex)

#'python' '-c' 'from freesurfer.regularizeTexture import regularizeTexture as f; 
#f("/neurospin/unicog/protocols/IRMf/Karla_Isa_Test_Analyse/Brainvisa/base_donnees_test_FS/subject01/surf/rh.isin",
#"/neurospin/unicog/protocols/IRMf/Karla_Isa_Test_Analyse/Brainvisa/base_donnees_test_FS/subject01/surf/rh.white.gii", 
#"/neurospin/unicog/protocols/IRMf/Karla_Isa_Test_Analyse/Brainvisa/base_donnees_test_FS/subject01/surf/rh.curv.gii", 
#"/neurospin/unicog/protocols/IRMf/Karla_Isa_Test_Analyse/Brainvisa/base_donnees_test_FS/subject01/surf/rh.r.curv.gii")