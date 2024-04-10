# Documentation for the function world_to_image in src/datastruct/shot

Function for calculating the image coordinates of a point, starting from a terrain point.
It is built into the shot object to calculate the coordinates of the point in the desired acquisition.

## Parameters

It takes as parameters :
1. **coor**: [X, Y, Z]
2. **cam**: a Camera object.
3. **type_z_data**: type of z you want in output 'altitude', 'height'.
4. **type_z_shot**: type of z there are in shot's position 'altitude', 'height'. 

The **Camera** object is the camera used for acquisition, defined by a **name**, its **ppax**, **ppay** and **focal** length, **width** and **height** of the image in pixel. Ppax and ppay are the main points of image deformation in x and y directions.

Object to instantiate before calculation :

* The **Dtm** allows to convert the data they have **linear alteration**. it's not mandatory if **type_z_data** equal **type_z_shot** or don't need tranfo to add or remove **linear alteration**.

* The **ProjEngine** object is defined by a string giving the ESPG code of the site's map projection, e.g. 2154, followed by a list of pyproj GeoTIFF of geoid.

  These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.

## Calculation step

### Conversion of terrain data into a Euclidean reference frame (local tangent)

* Convert the z of the data to the same unit (altitude, height), de-correct the z of the linear alteration acquisition if corrected

* Conversion from cartographic -> image to Euclidean -> image rotation matrix. With projeucli's mat_to_mat_eucli function.

### From Euclidean frame of reference to image frame of reference

* Calculation of the vector between the acquisition position and the terrain point and change of reference frame.
```math
p_{bundle} = \begin{pmatrix}x_{bundle}\\y_{bundle}\\z_{bundle}\end{pmatrix} = rot_{eucli} * (p_{eucli} – pos_{eucli})
```

* Change from 3d to 2d point in the image frame.
```math
x_{shot} = x_{bundle} * focal / z_{bundle}
```
```math
y_{shot} = y_{bundle} * focal / z_{bundle}
```
```math
z_{shot} = z_{bundle}
```


* Application of systematizations, if any (distortion correction function).
```math
x_{shot}, y_{shot}, z_{shot} = f_{sys}(x_{shot}, y_{shot}, z_{shot})
```
if there is no distortion or it has already been corrected f_sys() is an identity function.

* From vector to image point.
```math
x_{col} = ppax + x_{shot}
```
```math
y_{line} = ppay + y_{shot}
```

* Returns $x_{col}$ and $y_{line}$ in an array (2,).

## Example to use

Example for multi-point in worksite step by step:
```
import numpy as np
from src.datastruct.worksite import Worksite
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork

# Create worksite with just a name
work = Worksite("test")

# Add one or multiples shots
# Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration,order_axe)
# unit_angle = "degree" or "radian".
# linear_alteration True if z shot is corrected by linear alteration.
# order of rotation axe "opk" or "pok" ...
work.add_shot("shot_test1", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test', "degree", True, "opk")
work.add_shot("shot_test2", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test', "degree", True, "opk")

# Setup projection
# set_epsg(epsg, path_geoid)
# the geoid is mandatory if type_z_data and type_z_shot are different
work.set_proj(2154, ["./dataset/fr_ign_RAF20.tif"])

# Add camera information
# add_camera(name_cam, ppax, ppay, focal, width, height)
# ppax and ppay image center in pixel with distortion
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

# Add connecting points
# add_gcp2d(name_point, name_shot, column, line)
work.add_gcp2d('gcp_test1', 'shot_test1', 0, 0)
work.add_gcp2d('gcp_test2', 'shot_test1', 0, 0)
work.add_gcp2d('gcp_test3', 'shot_test2', 0, 0)

# Add gcps points
# add_gcp3d(name_gcp, code, coor)
work.add_gcp3d('gcp_test1', 13, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp3d('gcp_test2', 3, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp3d('gcp_test3', 13, np.array([815601.510, 6283629.280, 54.960]))

# Add dtm
# set_dtm(path_dtm, type_dtm)
# type_dtm = 'height' or 'altitude'
# The dtm is mandatory for the function image to world
work.set_dtm('MNT_France_25m_h_crop.tif','height')

# Setup projection system and z_nadir of shot
work.set_param_shot()

# Calculate coordinate image gcp for gcp with code 13
WorldImageWork(work).calculate_world_to_image([13])

point_gcp1 = work.shots["shot_test1"].gcp3d["gcp_test1"]
point_gcp2 = work.shots["shot_test1"].gcp3d["gcp_test2"]
point_gcp3 = work.shots["shot_test2"].gcp3d["gcp_test3"]
```

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)