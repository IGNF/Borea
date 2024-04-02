# Documentation for the function image_to_world in src/transform_world_image/transform_shot/image_world_shot.py

Function for calculating the ground coordinates of an image point, starting from a given z.
It is built into the shot object to calculate the coordinates of the point in the field, based on the desired acquisition.

## Parameters

1. **coor_2d**: [column, line]
2. **cam**: a Camera object.
3. **type_z_data**: type of z you want in output 'altitude', 'height' 
4. **type_z_shot**: type of z there are in shot's position 'altitude' or 'height'. 

The **Camera** object is the camera used for acquisition, defined by a **name**, its **ppax**, **ppay**, **focal** and **width** and **height** of the image in pixel. Ppax and ppay are the main points of image deformation in x and y directions.

**type_z_data** and **type_z_shot** are used to make the right conversions between different data so that calculations are made in the same system.

Object to instantiate before calculation :

* The **Dtm** allows a first estimate z terrain, and converts the data they have linear alteration.

* The **ProjEngine** object is defined by a string giving the ESPG code of the site's map projection, e.g. 2154, followed by a list of pyproj GeoTIFF of geoid.

  These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.


## Calculation step

* Creation of 3d vector in image frame minus perceptual center.
$$
x_{shot} = col - ppax
$$
$$
y_{shot} = line - ppay
$$
$$
z_{shot} = focal
$$

* Application of inverse systematizations if available (inverse distortion correction function).
$$
x_{shot}, y_{shot}, z_{shot} = f_{sys inv}(x_{shot}, y_{shot}, z_{shot})
$$
if there is no distortion or it has already been corrected $f_{sys inv}()$ is an identity function.

* Passage through the beam marker.
$$
x_{bundle} = x_{shot} / focal * z_{shot}
$$
$$
y_{bundle} = y_{shot} / focal * z_{shot}
$$
$$
z_{bundle} = z_{shot}
$$

* Transition to the Euclidean reference frame.
$$
\left(\begin{array}{cc} 
x_{local}\\
y_{local}\\
z_{local}
\end{array}\right) = rot_{eucli}^T * 
\left(\begin{array}{cc} 
x_{bundle}\\
y_{bundle}\\
z_{bundle}
\end{array}\right)
$$
With proj.rot_to_euclidean_local the rotation matrix of the Euclidean frame of reference set up from the site's barycentre.

* Converting the acquisition position to the Euclidean reference frame. With projeucli's world_to_eucliean() function. Warning: $z_{posShot}$ must be de-corrected for linear alteration and must be of the same unit as the others (altitude or height).

* Addition of local point acquisition.
$$
\left(\begin{array}{cc} 
x_{local}\\
y_{local}\\
z_{local}
\end{array}\right) = 
\left(\begin{array}{cc} 
x_{local}\\
y_{local}\\
z_{local}
\end{array}\right) + 
\left(\begin{array}{cc} 
x_{posEucli}\\
y_{posEucli}\\
z_{posEucli}
\end{array}\right)
$$


* Create lambda to convert local point into Euclidean point.
$$
lamb = (z - z_{posEucli})/(z_{local} - z_{posEucli})
$$
$$
x_{local} = x_{posEucli} + (x_{local} - x_{posEucli}) * lamb
$$
$$
y_{local} = y_{posEucli} + (y_{local} - y_{posEucli}) * lamb
$$

* Convert Euclidean point to terrain point, using proj's euclidean_to_world(x, y, z) function.

* Returns the point as an array (3,).

## Example to use

```
import numpy as np
from src.datastruct.worksite import Worksite
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork

# Create worksite with just a name
work = Worksite("Test")

# Add two shots
# Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration)
# unit_angle = "degree" or "radian".
# linear_alteration True if z shot is corrected by linear alteration.
work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree", True)
work.add_shot("shot2",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree", True)

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

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)