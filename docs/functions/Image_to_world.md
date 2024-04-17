# Formula documentation for the function image_to_world

Function to transform a terrain coordinates of an image coordinates, starting from a given z.  
It is built into the ImageWorldShot class [src/transform_world_image/transform_shot/image_world_shot.py](../../src/transform_world_image/transform_shot/image_world_shot.py).  
Tools where transformation is used are : opk_control.py, pt_image_to_world.py and ptfile_image_to_world.py.

## Formula

* Creation of 3d vector in image frame minus perceptual center. Switches from a 2D image frame to a 3D image frame.
```math
x_{shot} = col - ppa_x
```
```math
y_{shot} = line - ppa_y
```
```math
z_{shot} = focal
```
 **PPAx** and **PPAy** are the main points of image deformation in x and y directions. **col** and **line** is the image coordinates and **focal** is the focal of the camera.
* Application of inverse systematizations if available (inverse distortion correction function).
```math
x_{shot}, y_{shot}, z_{shot} = f_{sys inv}(x_{shot}, y_{shot}, z_{shot})
```
if there is no distortion or it has already been corrected $f_{sys inv}()$ is an identity function.

* Passage through the beam frame.
```math
x_{bundle} = x_{shot} / focal * z_{shot}
```
```math
y_{bundle} = y_{shot} / focal * z_{shot}
```
```math
z_{bundle} = z_{shot}
```

* Transition to the Euclidean reference frame.
```math
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} = rot_{eucli}^T * 
\begin{pmatrix} 
x_{bundle}\\
y_{bundle}\\
z_{bundle}
\end{pmatrix}
```
With Shot.projeucli.mat_rot_euclidean_local() the rotation matrix of the Euclidean frame of reference set up from the site's barycentre.

* Converting the acquisition position to the Euclidean reference frame. With projeucli's world_to_eucliean() function. Warning: $z_{posShot}$ must be de-corrected for linear alteration and must be of the same unit as the others (altitude or height).

* Addition of local point acquisition.
```math
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} = 
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} + 
\begin{pmatrix}
x_{posEucli}\\
y_{posEucli}\\
z_{posEucli}
\end{pmatrix}
```


* Create lambda to convert local point into Euclidean point.
```math
lamb = (z - z_{posEucli})/(z_{local} - z_{posEucli})
```
```math
x_{local} = x_{posEucli} + (x_{local} - x_{posEucli}) * lamb
```
```math
y_{local} = y_{posEucli} + (y_{local} - y_{posEucli}) * lamb
```

* Convert Euclidean point to terrain point, using proj's euclidean_to_world(x, y, z) function.

* Returns the point as an array (3,). However, the z coordinate is wrong, but with a DTM we can find the Z value with the X and Y position we've just calculated.

## Example to use

```
import numpy as np
from src.datastruct.worksite import Worksite
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork

# Create worksite with just a name
work = Worksite("Test")

# Add two shots
# Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration, order_axe)
# unit_angle = "degree" or "radian".
# linear_alteration True if z shot is corrected by linear alteration.
# order of rotation axe "opk" or "pok" ...
work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree", True,"opk")
work.add_shot("shot2",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree", True,"opk")

# Setup projection
# set_epsg(epsg, path_geoid)
# the geoid is mandatory if type_z_data and type_z_shot are different
work.set_proj(2154, ["./dataset/fr_ign_RAF20.tif"])

# Add camera information
# add_camera(name_cam, ppax, ppay, focal, width, height)
# ppax and ppay image center in pixel with distortion
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

# Add connecting points in each shot
# add_co_point(name_point, name_shot, column, line)
work.add_co_point('"1003"',"shot1",24042.25,14781.17)
work.add_co_point('"1003"',"shot2",24120.2,10329.3)

# Setup projection system of shot and z_nadir of shot
work.set_param_shot()

# Calculate world coordinate by least square.
# manage_image_world(type_point, type_process)
ImageWorldWork(work).manage_image_world("co_points", "square")

# Transform euclidiean coordinate to world coordinate 
coor_world = work.co_pts_world['"1003"']
```

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)