# Documentation for the function image_to_world in shot

Function for calculating the ground coordinates of an image point, starting from a given z.
It is built into the shot object to calculate the coordinates of the point in the field, based on the desired acquisition.

## Parameters

1. col: column coordinates of the point in the image in float format.
2. lig: line coordinates of the point in the image in float format.
3. cam: a Camera object.
4. proj: a EuclideanProj object.
5. z : The z position of the approximate default point = 0.

The Camera object is the camera used for acquisition, defined by a name, its ppax, ppay and focal.

The EuclidieanProj object, defined by two coordinates x and y, which are the barycentre of the construction site, and a ProjEngine object.

The ProjEngine object is defined by a string giving the ESPG code of the site's map projection, e.g. "EPSG:2154", followed by a dictionary found in src.data.projection_list.json, which contains 3 important tags:
 * "geoc" returns the EPSG code of the geocentric projection on site.
 * "geog" returns the EPSG code of the geographic projection on the building site.
 * "geoid" returns a list of GeoTIFF names for the site.

These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj or you can give in argument the path to the GeoTIFF forlder.

The data in the "geoid" tag is not used in this function and is therefore not mandatory.

## Calculation step

### From image frame to beam frame

* Creation of 3d vector in image frame minus perceptual center.
```
x_shot = col - cam.ppax
y_shot = line - cam.ppay
z_shot = cam.focal
```

* Application of inverse systematizations if available (inverse distortion correction function).
```
x_shot, y_shot, z_shot = self.f_sys_inv(x_shot, y_shot, z_shot)
```
if there is no distortion or it has already been corrected f_sys_inv() is an identity function.

* Passage through the beam marker.
```
x_bundle = x_shot / cam.focal * z_shot
y_bundle = y_shot / cam.focal * z_shot
z_bundle = z_shot
```

* Transition to the Euclidean reference frame.
```
p_local = proj.rot_to_euclidean_local @ np.array([x_bundle, y_bundle, z_bundle])
```
With proj.rot_to_euclidean_local the rotation matrix of the Euclidean frame of reference set up from the site's barycentre.

* Converting the acquisition position to the Euclidean reference frame. With projeucli's world_to_eucliean() function.

* Addition of local point acquisition.
```
p_local = p_local + pos_eucli
```

* Create lambda to convert local point into Euclidean point.
```
lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
```

* Convert Euclidean point to terrain point, using proj's euclidean_to_world(x, y, z) function.

* Returns the point as an array (3,).

### Example to use

Example for one point 
```
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj

# Point to calculate coordinate 
point_image = np.array([24042.25, 14781.17])

# Shot where there is the point
shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")

# Camera of the shot
cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)

# Projection of the worksite
proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")

# Euclidean projection of the worksite with position of shot is the barycenter of the system
projeucli = EuclideanProj(814975.925, 6283986.148, proj)

# The calculation
actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli,54.960)
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)