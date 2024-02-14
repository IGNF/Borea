# Documentation for the function world_to_image in src/datastruct/shot

Function for calculating the image coordinates of a point, starting from a terrain point.
It is built into the shot object to calculate the coordinates of the point in the desired acquisition.

## Parameters

It takes as parameters :
1. x: coordinate x
2. y: coordinate y
3. z: coordinate z
4. cam: a Camera object.
5. dem: Dem of the worksite
6. type_z_data: type of z you want in output 'a' for altitude, 'h' for height 
7. type_z_shot: type of z there are in shot's position 'a', 'al', 'h', 'hl' -> 'l' it's with linear alteration. 

The Camera object is the camera used for acquisition, defined by a name, its ppax, ppay and focal length.

The dem allows to convert the data they have linear alteration. it's not mandatory if type_z_data equal type_z_shot or don't need tranfo to add or remove linear alteration

recall:  
The ProjEngine object is defined by a string giving the ESPG code of the site's map projection, e.g. "EPSG:2154", followed by a dictionary found in src.data.projection_list.json, which groups together 3 important tags:
 * "geoc" returns the EPSG code of the geocentric projection on site.
 * "geog" returns the EPSG code of the geographic projection on the building site.
 * "geoid" returns a list of GeoTIFF names at site level.

These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.  
it's not mandatory if there ara not tranfo between altitude and height.

## Calculation step

### Conversion of terrain data into a Euclidean reference frame (local tangent)

* Convert the z of the data to the same unit (altitude, height), de-correct the z of the linear alteration acquisition if corrected

* Conversion from cartographic -> image to Euclidean -> image rotation matrix. With projeucli's mat_to_mat_eucli function.

### From Euclidean frame of reference to image frame of reference

* Calculation of the vector between the acquisition position and the terrain point and change of reference frame.
$$
p_{bundle} = \left(\begin{array}{cc}x_{bundle}\\y_{bundle}\\z_{bundle}\end{array}\right) = rot_{eucli} * (p_{eucli} – pos_{eucli})
$$

* Change from 3d to 2d point in the image frame.
$$
x_{shot} = x_{bundle} * focal / z_{bundle}
$$
$$
y_{shot} = y_{bundle} * focal / z_{bundle}
$$
$$
z_{shot} = z_{bundle}
$$


* Application of systematizations, if any (distortion correction function).
$$
x_{shot}, y_{shot}, z_{shot} = f_{sys}(x_{shot}, y_{shot}, z_{shot})
$$
if there is no distortion or it has already been corrected f_sys() is an identity function.

* From vector to image point.
$$
x_{col} = ppax + x_{shot}
$$
$$
y_{line} = ppay + y_{shot}
$$

* Returns $x_{col}$ and $y_{line}$ in an array (2,).

## Example to use

Example for one point:
```
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj

# Point to calculate coordinate 
x = 815601.510
y = 6283629.280
z = 54.960

# Shot where we want to calculate its image coordinate
shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", "d")

# Camera of the shot
cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)

# Projection of the worksite
proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")

# Setup euclidean projection for the shot
shot.set_param_eucli_shot(proj)

# Add dem
# Dem(path_dem, type_dem)
# type_dem = 'h' for height or 'a' for altitude
# The dem is mandatory for the function image to world
dem = Dem('MNT_France_25m_h_crop.tif','h')

# The calculation
# image_to_world(x, y, z, camera, dem, type_z_data, type_z_shot)
# type_z_data = type of z you want in output 'a' or 'h'
# type_z_shot = z's type of position shot 'a' 'al' 'h' 'hl' -> l with linear alteration 
point_image = shot.world_to_image(x, y, z, cam, dem, "a", "al")
```

Example for multi-point in worksite step by step:
```
from src.datastruct.worksite import Worksite

# Create worksite with just a name
work = Worksite("test")

# Add one or multiples shots
work.add_shot("shot_test1", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test', "d")
work.add_shot("shot_test2", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test', "d")

# Setup projection
work.set_proj("EPSG:2154", "test/data/proj.json", "./test/data/")

# Add camera information
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)

# Add connecting points
work.add_gipoint('gcp_test1', 'shot_test1', 0, 0)
work.add_gipoint('gcp_test2', 'shot_test1', 0, 0)
work.add_gipoint('gcp_test3', 'shot_test2', 0, 0)
work.check_gip = True

# Add gcps points
work.add_gcp('gcp_test1', 13, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp('gcp_test2', 3, np.array([815601.510, 6283629.280, 54.960]))
work.add_gcp('gcp_test3', 13, np.array([815601.510, 6283629.280, 54.960]))
work.check_gcp = True

# Add dem
# Dem(path_dem, type_dem)
# type_dem = 'h' for height or 'a' for altitude
# The dem is mandatory for the function image to world
work.add_dem('MNT_France_25m_h_crop.tif','h')

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

############# Data ###############

# path to photogrammetric site file
path_opk = "Worksite_FR_2024.OPK"

# line taken and header
line_taken = [1, None]
header = ['N', 'X', 'Y', 'Zal', 'Od', 'Pd', 'Kd', 'C']

# info in epsg and epsg data
epsg = "EPSG:2154"
proj_json = "projection_epsg.json"
folder_geoid = "./data_geotiff/"

# path(s) to camera's file
path_camera = ["Camera.txt"]

# path(s) to connecting points file
path_copoints = ["liaison.mes"]

# path(s) to image ground control points file
path_gipoints = ["terrain.mes"]

# path(s) to ground control points file with unit of z and code of control point
path_gcps = ["GCP.app"]
type_z_data = 'h'
type_control = [13]

# path to dem file and unit of the dem
path_dem = "dem.tif"
type_dem = "h"

################# Function ###################

# Readind data and create objet worksite
work = reader_orientation(path_opk, line_taken, header)

# Add a projection to the worksite
work.set_proj("EPSG:2154", "projection_epsg.json", "./data_geotiff/")

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_gipoints(path_gipoints, work)

# Reading GCP
read_gcp(path_gcps, work)

# Add dem
# Dem(path_dem, type_dem)
# type_dem = 'h' for height or 'a' for altitude
# The dem is mandatory for the function image to world
work.add_dem(path_dem, type_dem)

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp(type_control)
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)