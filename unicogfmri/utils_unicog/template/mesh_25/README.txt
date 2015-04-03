------------------------------------------------------------------------------
README for template_meshes
------------------------------------------------------------------------------

- The meshes in this directory have been created by Alan Tucholka
from 25 subjects (some twins and localizer subjects).

- The inflated meshes can be created with the line command "AimsInflate" :

Example :

AimsInflate -i brain_mesh.mesh 
            -o brain_mesh_inflated.mesh 
            -c brain_mesh_inflated.tex
            -B 4000

-c --> defines an output file for the texture of the mean curvature
-B --> defines the bound for the force computation

For more information, use "AimsInflate -h"
------------------------------------------------------------------------------
