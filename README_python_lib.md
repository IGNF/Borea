# Python lib

## Read data and instantiate worksite

Creation of a worksite object from a worksite file (.opk) to be read by `reader_orientation(pathfile, arg_dict)`.  
`arg_dict` is a dictionary for different args: 
* `"interval":[first_line, last_line]` is an list of int that specifies the number of lines you want to read. `first_line` allows you to skip the file header, which must not be taken into account when reading the file, as specified in the `header` variable. If `first_line = None` skips everything up to `last_line`, if `lastline = None` skips everything from `first_line` to the end, and if both are None reads the entire file.
* `"header":header` described in the section above, is a list of str e.g. `['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']`, detail letter below. 
* `"unit_angle": "degree"` degree or radian. 
* `"linear_alteration": True` boolean saying True if z shots are corrected by linear alteration.

Once the object has been created, you can add other data to it:

* Setup the projection of the worksite `work.set_proj(epsg, path_geoid)`, with:
    * `epsg` the code epsg e.g. 2154
    * `path_geoid` path to the file pyproj GeoTIFF of geoid

* The camera with `read_camera([filepath], worksite)`, this function only reads txt and xml files referencing camera data, and can take several camera files if there are several.

* Link points with `read_co_points([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files.

* Link points with `read_gcp2d([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files. In addition, the z data type 'height' or 'altitude' must be added to worksite `worksite.type_z_data = 'altitude'`. 

* Field points (GCPs) with `read_gcp([pathfile], worksite)`. Adds control and support terrain points in .app file format, can read multiple files. In addition, the z data type 'height' and 'altitude' must be added to worksite `worksite.type_z_data = 'altitude'` same variable than before. 

* Add Dtm to your worksite `work.set_dtm(path_dtm, type_dtm)`, It converts z data between gcp and acquisition position if these are not in the same unit (one in altitude and one in height). `type_dtm` is the unit of the dtm 'altitude' or 'height'.

## Different process

* Set different parameters for shots (projection system of shot and z_nadir), mandatory if data is to be processed afterwards. `work.set_param_shot()`.

* Can calculate the position of image points in world with `ImageWorldWork(worksite).manage_image_world(type_point, type_process, type_control)`.   
    * `type_point` is the type of point you want to calcule `co_points` or `gcp2d`.   
    * `type_process` is the type of process you want to use intersection with key `inter` or least square methode with key `square`.  
    * `type_control` egal None by default, is used if the type_point = gcp2d and if you want just one type code point, else None to process on all point.  

    The result can be found in `worksite.co_pts_world['name_point']` when type_point = co_points or `worksite.img_pts_world['name_point]` when type_point = gcp2d.

* Can calculate the position of terrain points in images with `WorldImageWork(work).calculate_world_to_image(type_control)` with `type_control` egal None by default, is used if the type_point = gcp2d and if you want just one type code point, else None to process on all point. . The result can be found in `worksite.shots['name_shot'].gcps['name_gcp']` for each image and each gcps.

* Can calculate spatial resection for each shot in worksite with `SpaceResection(work).space_resection_on_worksite(add_pixel = (0,0))`. `add_pixel` is used to add a deviation to the position of the points to modify the shot's 6 external parameters for data conversion, for example.

* Can calculate spatial resection in poitn of shot for creating worksite with `SpaceResection(work).space_resection_to_worksite(pt2d, pt3d, pinit)`.  
The DataFrame **pt2d** is a table with 4 column and n line. The id of column must be:
    * `id_pt`: the id of the point
    * `id_shot`: the name of the shot where the point is located
    * `column`: column coordinate in pixel of the point in the image
    * `line`: line coordinate in pixel of the point in the image  

    it can be created with the function `read_file_pt_dataframe(path_file_pt,header_file,"pt2d")`  
The DataFrame **pt3d** is a table with 5 column and n line. The id of column must be:
    * `id_pt`: the id of the point
    * `type`: if point is gcp with type else None
    * `x`: x coordinate in your projection system of the point
    * `y`: y coordinate in your projection system of the point
    * `z`: z coordinate in your projection system of the point  

    it can be created with the function `read_file_pt_dataframe(path_file_pt,header_file,"pt3d")`  
The dictionary **pinit** which give the initialization point X, Y, Z. A point on the worksite with a z at an approximate flying height. The name of the key in the dictionary is `coor_init`.  
Example at the end of explanation of function [file](./docs/functions/Space_resection.md).

* You can calculate some control point statistics to see how accurate your site is `stat = Stat(work, pathreturn, control_type)` to init the object and run for all stat with `stat.main_stat_and_save()`. Make stat on function image to world and world to image, if there are data. And save result on *pathreturn/Stat_{Name_worksite}.txt*.

## Write data

* Can write worksite object as .opk. `manager_reader(writer, pathreturn, worksite)` with `writer` the type of output `"opk"`.

## Example

```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_co_points import read_co_points
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_reader
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork
from src.transform_world_image.transform_worksite.space_resection import SpaceResection
from src.stat.statistics import Stat


############# Data ###############

# path to photogrammetric site file
path_opk = "dataset/23FD1305_alt_test.OPK"

# line taken and header
line_taken = [2, None]
header = list('NXYZOPKC')
# or
header = ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
unit_angle = 'degree' # or "radian"
linear_alteration = True # If z shot is corrected by linear alteration

# info in epsg and epsg data
epsg = "EPSG:2154"
path_geoid = ["dataset/fr_ign_RAF20.tif"]

# path(s) to camera's file
path_camera = ["dataset/Camera1.txt"]

# path(s) to connecting points file
path_co_points = ["dataset/liaisons_test.mes"]

# path(s) to image ground control points file
path_gcp2d= ["dataset/terrain_test.mes"]

# path(s) to ground control points file with unit of z and code of control point
path_gcps = ["dataset/GCP_test.app"]
type_z_data = 'height'
type_control = [13]

# path to dtm file and unit of the dtm
path_dtm = "dataset/MNT_France_25m_h_crop.tif"
type_dtm = "height"

# type process for function image to world "inter or "square"
type_process = "inter"

# type of output file (opk or rpc)
writer = "opk"

# folder path for the output
pathreturn = "./"

################# Function ###################

# Readind data and create objet worksite
work = reader_orientation(path_opk, {"interval": line_taken,
                                     "header": header,
                                     "unit_angle": unit_angle,
                                     "linear_alteration": linear_alteration})

# Add a projection to the worksite
work.set_proj(epsg, path_geoid)

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_co_points(path_co_points, work)

# Reading ground controle point in image
read_gcp2d(path_gcp2d, work)

# Reading GCP
read_gcp(path_gcps, work)
work.type_z_data = type_z_data

# Add Dtm to the worksite
work.set_dtm(path_dtm, type_dtm)

# Setup parameters of shot (projection system of shot and z_nadir)
work.set_param_shot()

# Calculate world coordinate of "co_points" or "ground_image_pts"
# Type control isn't mandatory, take all points if not specified 
ImageWorldWork(work).manage_image_world("gcp2d", type_process,type_control)

# Calculate image coordinate of GCP if they exist for 2 type
# Type control isn't mandatory, take all points if not specified 
WorldImageWork(work).calculate_world_to_image(type_control)

# Calculate shooting position with a factor pixel, to change projection for example
SpaceResection(work).space_resection_on_worksite(add_pixel = (0,0))

# Calculate stat on world_to_image and image_to_world
stat = Stat(work, pathreturn, type_control)
stat.main_stat_and_save()

# Writing data
manager_reader(writer, pathreturn, work)
```
Examples of the different formats can be found in *./dataset/*.

## Detail

### Header of file
`header` is used to describe the format of the opk file read. It provides information on what's in each column, and gives the data unit for Z and angles.   
Type is:
| Symbol | Details |
| :----: | :------ |
| S | to ignore the column |
| N | name of shot |
| X | coordinate x of the shot position |
| Y | coordinate y of the shot position |
| Z | coordinate z altitude of the shot position |
| H | coordinate z height of the shot position |
| O | omega rotation angle |
| P | phi rotation angle |
| K | kappa rotation angle |
| C | name of the camera |

## Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its **name** (str), **ppax** (float), **ppay** (float), **focal** (float) and image size, **width** (int) and **height** (int) in pixels. .  
Ppax and ppay are the main points of image deformation in x and y directions.  
Each line of the file corresponds to a piece of information, starting with the **type = info**.
```
name = UCE-M3-f120-s06
ppax = 13210.00
ppay = 8502.00
focal = 30975.00
width = 26460
height = 17004
```
Only these 6 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool.
An example file can be found in *./dataset/Camera1.txt*.

## File projection JSON format

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The varaible in example for adding a geoid is path_geoid, a list which contains paths of geoids, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)