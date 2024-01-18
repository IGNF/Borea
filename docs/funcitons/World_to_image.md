# Documentation for the function world_to_image in shot

Function for calculating the image coordinates of a point, starting from a terrain point.
It is built into the shot object to calculate the coordinates of the point in the desired acquisition.

## Parameters

It takes as parameters :
    1. point: a point in numpy format np.array([x, y, z]).
    2. cam: a Camera object.
    3. projeucli: a EuclideanProj object.

The Camera object is the camera used for acquisition, defined by a name, its ppax, ppay and focal length.

The EuclidieanProj object, defined by two coordinates x and y, which are the barycentre of the building site, and a ProjEngine object.

The ProjEngine object is defined by a string giving the ESPG code of the site's map projection, e.g. "EPSG:2154", followed by a dictionary found in src.data.projection_list.json, which groups together 3 important tags:
 * "geoc" returns the EPSG code of the geocentric projection on site.
 * "geog" returns the EPSG code of the geographic projection on the building site.
 * "geoid" returns a list of GeoTIFF names at site level.

These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.

## Calculation step

### Conversion of terrain data into a Euclidean reference frame (local tangent)

* Recovery of the acquisition altitude (z_alti) without alteration by pyproj (thanks to GeoTIFF).

* Convert terrain data into Euclidean reference frame, point [x, y, z] and acquisition position [x_pos, y_pos, z_alti], replacing z_pos with z_alti. With projeucli's world_to_eucliean() function.

* Conversion from cartographic -> image to Euclidean -> image rotation matrix. With projeucli's mat_to_mat_eucli function.

### From Euclidean frame of reference to image frame of reference

* Calculation of the vector between the acquisition position and the terrain point and change of reference frame.
```
p_bundle = mat_eucli @ (p_eucli – pos_eucli)
```

* Change from 3d to 2d point in the image frame.
```
x_shot = p_bundle[0] * cam.focal / p_bundle[2]
y_shot = p_bundle[1] * cam.focal / p_bundle[2]
z_shot = p_bundle[2]
```

* Application of systematizations, if any (distortion correction function).
```
x_shot, y_shot, z_shot = self.f_sys(x_shot, y_shot, z_shot)
```
if there is no distortion or it has already been corrected f_sys() is an identity function.

* From vector to image point.
```
x_col = cam.ppax + x_shot
y_lig = cam.ppay + y_shot
```

* Returns x_col and y_lig in an array (2,).

### Example to use

Example for one point:
```
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj

# Point to calculate coordinate 
point_terrain = np.array([815601.510, 6283629.280, 54.960])

# Shot where we want to calculate its image coordinate
shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")

# Camera of the shot
cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)

# Projection of the worksite
proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")

# Euclidean projection of the worksite with position of shot is the barycenter of the system
projeucli = EuclideanProj(814975.925, 6283986.148, proj)

# The calculation
point_image = shot.world_to_image(point_terrain, cam, projeucli)
```

Example for multi-point in worksite step by step:
```
from src.datastruct.worksite import Worksite

# Create worksite with just a name
work = Worksite("test")

# add one or multiples shots
work.add_shot("shot_test1", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
work.add_shot("shot_test2", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')

# Setup projection
work.set_proj("EPSG:2154", "test/data/proj.json", "./test/data/")

# Add camera information
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)

# add connecting points
work.add_copoint('gcp_test1', 'shot_test1', 0, 0)
work.add_copoint('gcp_test2', 'shot_test1', 0, 0)
work.add_copoint('gcp_test3', 'shot_test2', 0, 0)
work.check_cop = True

# add gcps points
work.add_gcp('gcp_test1', 13, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp('gcp_test2', 3, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp('gcp_test3', 13, np.array([815601.510, 6283629.280, 54.960]))
work.check_gcp = True

# Calculate coordinate image gcp for gcp with code 13
work.calculate_world_to_image_gcp([13])

point_gcp1 = work.shots["shot_test1"].gcps["gcp_test1"]
point_gcp2 = work.shots["shot_test1"].gcps["gcp_test2"]
point_gcp3 = work.shots["shot_test2"].gcps["gcp_test3"]
```

Example with file
```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp

path_opk = "Worksite_FR_2024.OPK"
path_camera = ["Camera.txt"]
path_copoints = ["liaison.mes", "terrain.mes"]
path_gcps = ["GCP.app"]
writer = "opk"
pathreturn = "tmp/"

# Readind data and create objet worksite
work = reader_orientation(path_opk, 1)

# Add a projection to the worksite
work.set_proj("EPSG:2154", "projection_epsg.json", "./data_geotiff/")

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_copoints(path_copoints, work)

# Reading GCP
read_gcp(path_gcps, work)

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp([3])
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)