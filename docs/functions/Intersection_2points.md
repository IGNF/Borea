# Documentation for the function eucli_intersection_2p in src/transform_world_image/transform_worksite/image_world_work.py

Function to calculate the Euclidean coordinates of a point, visible on two acquisitions. Function built in worksite to calculate from 2 acquisitions.

## Parameters

1. name_copoint: the name of the link point you wish to calculate its field position, in str format.
2. shot1: first acquisition where the point is visible and its image coordinates are known, Shot object format.
3. shot2: second acquisition where the point is visible and its image coordinates are known, Shot object format.

The Shot object is an object for an acquisition that defines it, with a name, position, rotation angles and camera name.

## Calculation step

### Data recovery
Recover point position in images
$$
p_{img1} = \left(\begin{array}{cc} 
c_{img1}\\
l_{img1}
\end{array}\right)
$$
$$
p_{img2} = \left(\begin{array}{cc} 
c_{img2}\\
l_{img2}
\end{array}\right)
$$
Recover camera for each image
$$
cam_1 = \left(\begin{array}{cc} 
ppa_{x1} & ppa_{y1} & focal_1
\end{array}\right)
$$
$$
cam_2 = \left(\begin{array}{cc} 
ppa_{x2} & ppa_{y2} & focal_2
\end{array}\right)
$$


### Converting image data to Euclidean projection

* Conversion of acquisition positions in the Euclidean reference frame
$$
pos_{eucli1} = \left(\begin{array}{cc} 
x_{posEucli1}\\y_{posEucli1}\\z_{posEucli1}
\end{array}\right) = 
f_{worldToEuclidean}(x_{posShot1},y_{posShot1},z_{posShot1})
$$
$$
pos_{eucli2} = \left(\begin{array}{cc} 
x_{posEucli2}\\y_{posEucli2}\\z_{posEucli2}
\end{array}\right) = 
f_{worldToEuclidean}(x_{posShot2},y_{posShot2},z_{posShot2})
$$

* Calculates image-to-Euclidean reference frame change matrices for each shot (rot is the rotation matrix)
$$
rot_{eucli1} = 
f_{matToMatEucli}(x_{posShot1},y_{posShot1},rot_{shot1})
$$
$$
rot_{eucli2} = 
f_{matToMatEucli}(x_{posShot2},y_{posShot2},rot_{shot2})
$$

### Euclidean position calculation

* Base calculation
$$
base = pos_{eucli1} - pos_{eucli2}
$$

* Calculates the vectors of each beam by acquisition
$$
vect_1 = rot_{eucli1} * \left(\begin{array}{cc} 
c_{img1} - ppa_{x1}\\l_{img1} - ppa_{y1}\\-focal_1
\end{array}\right)
$$
$$
vect_2 = rot_{eucli2} * \left(\begin{array}{cc} 
c_{img2} - ppa_{x2}\\l_{img2} - ppa_{y2}\\-focal_2
\end{array}\right)
$$

* Calculates products scalar product
$$
norme_{v1} = vect_1 * vect_1
$$
$$
norme_{v2} = vect_2 * vect_2
$$
$$
v_1v_2 = vect_1 * vect_2
$$
$$
bv_1 = base * vect_1
$$
$$
bv_2 = base * vect_2
$$

* Calculates the position of the point on the beam
$$
p_{eucli1} = pos_{eucli1} + \frac{bv_2*v_1v_2 - bv_1*norme_{v1}}{v_1v_2^2 - norme_{v1}*norme_{v2}} * vect_1
$$
$$
p_{eucli2} = pos_{eucli2} + \frac{bv_2*norme_{v1} - bv_1*v_1v_2}{v_1v_2^2 - norme_{v1}*norme_{v2}} * vect_2
$$


* Return the average position between the two points
$$
p_{world} = 0.5 * (p_{eucli1} + p_{eucli2})
$$

##  Example to use
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
# set_epsg(epsg, proj_json, folder_geoid)
# the geoid is mandatory if type_z_data and type_z_shot are different
work.set_proj(2154, "test/data/proj.json", "./test/data/")

# Add camera information
# add_camera(name_cam, ppax, ppay, focal, width, height)
# ppax and ppay image center in pixel with distortion
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

# Add connecting points in each shot
# add_co_point(name_point, name_shot, column, line)
work.add_co_point('"1003"',"shot1",24042.25,14781.17)
work.add_co_point('"1003"',"shot2",24120.2,10329.3)

# Setup projection system and z_nadir of shot
work.set_param_shot()

# Calculate eucliean coordinate of intersection
# manage_image_world(type_point, type_process)
ImageWorldWork(work).manage_image_world("co_points", "intersection")

# Transform euclidiean coordinate to world coordinate 
coor_world = work.co_pts_world['"1003"']
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)