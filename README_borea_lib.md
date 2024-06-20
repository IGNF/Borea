[![IGNF badge](https://img.shields.io/badge/IGNF-8cbd3a)](https://www.ign.fr/) [![PyPI Downloads](https://img.shields.io/pypi/dm/ign-borea.svg?label=PyPI%20downloads)](
https://pypi.org/project/ign-borea/)

Borea is an open-source python package tools-box photogrammetric conversion format and transformation coordinate of image and terrain.  
Why Borea? **B** for Box and **orea** is a back slang of aero.

## Installation

Due to different dependency used installation of the library require `GDAL>=3.3.2`, which is not included in the dependency.
```
pip install ign-borea
```
For GDAL installation you need `libgdal-dev`:
```
sudo apt-get install libgdal-dev
```
Please note that the `GDAL` version depends on the `libgdal-dev` version.
```
apt-cache show libgdal-dev
# or if you are ogr
ogrinfo --version
```
```
pip install GDAL==<GDAL VERSION FROM OGRINFO>
```
You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) if you have problems installing GDAL.

## Tools

Some tools are already implemented in the library:
* Conversion OPK to OPK: `opk-to-opk -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Control OPK file: `opk-control -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_opk_control.md)
* Conversion OPK to RPC: `opk-to-rpc -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_opk_to_rpc.md)
* Conversion OPK to Conl: `opk-to-conl -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_opk_to_conl.md) (Conl = light conical file, IGN France format)
* Transforms coordinates terrain from image: `pt-image-to-world -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_pt_image_to_world.md)
* Transforms coordinates image from terrain: `pt-world-to-image -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_pt_world_to_image.md)
* Transforms coordinates file terrain from image: `ptfile-image-to-world -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_ptfile_image_to_world.md)
* Transforms coordinates file image from terrain: `ptfile-world-to-image -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_ptfile_world_to_image.md)
* Calculates opk by space resection: `spaceresection-opk -h` [doc](https://github.com/IGNF/Borea/tree/main/borea_tools/docs_tools/README_spaceresection_opk.md)

## Read data and instantiate worksite

Creation of a worksite object from a worksite file (.opk) to be read by `reader_orientation(pathfile, arg_dict)` with `from borea.reader.orientation.manage_reader import reader_orientation`.  
`arg_dict` is a dictionary for different args: 
* `"interval":[first_line, last_line]` is an list of int that specifies the number of lines you want to read. `first_line` allows you to skip the file header, which must not be taken into account when reading the file, as specified in the `header` variable. If `first_line = None` skips everything up to `last_line`, if `lastline = None` skips everything from `first_line` to the end, and if both are None reads the entire file.
* `"header":header` described in the section above, is a list of str e.g. `['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C'] = list("NXYZOPKC")`, detail of letter at section [header of file opk](#header-of-file-opk) below. 
* `"unit_angle": "degree"` degree or radian. 
* `"linear_alteration": True` boolean saying True if z shots are corrected by linear alteration.
* `"order_axe: "opk"` string to define the order of angle to calculate rotation matrix.

Once the object has been created, you can add other data to it:

* Setup the projection of the worksite `work.set_proj(epsg, path_geoid)`, with:
    * `epsg` the code epsg e.g. 2154
    * `path_geoid` path to the file pyproj GeoTIFF of geoid

* The camera with `read_camera([filepath], worksite)` in `from borea.reader.reader_camera import read_camera`, this function only reads txt and xml files referencing camera data, and can take several camera files if there are several.

* Link points with `read_file_pt(filepath, header, type_point, worksite)` in `from borea.reader.reader_point import read_file_pt`. this function reads all .txt, .mes, .app and other file types, as long as the data structure in the file is column-based and delimited by spaces. The first args is the file path of one file. The second is the column type in the file detail of letter at section [header of point file](#header-of-point-file) below. The third is the type of point **'co_points'** for connecting points, **'gcp2d'** for coordinnate of gcp in images and **'gcp3d'** for gcp coordinate in the ground. And the last args is the worksite where data will be save.

* Add Dtm to your worksite `work.set_dtm(path_dtm, type_dtm)`, It converts z data between gcp and acquisition position if these are not in the same unit (one in altitude and one in height). `type_dtm` is the unit of the dtm 'altitude' or 'height'.

Examples in section [examples](#examples) below.

## Different process

* Set different parameters for shots (projection system of shot and z_nadir), mandatory if data is to be processed afterwards. `work.set_param_shot()`.

* Can calculate the position of image points in world with `ImageWorldWork(worksite).manage_image_world(type_point, type_process, type_control)` in `from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork`.   
    * `type_point` is the type of point you want to calcule `co_points` or `gcp2d`.   
    * `type_process` is the type of process you want to use intersection with key `inter` or least square methode with key `square`.  
    * `type_control` egal None by default, is used if the type_point = gcp2d and if you want just one type code point, else None to process on all point.  

    The result can be found in `worksite.co_pts_world['name_point']` when type_point = co_points or `worksite.img_pts_world['name_point]` when type_point = gcp2d.

* Can calculate the position of terrain points in images with `WorldImageWork(work).calculate_world_to_image(type_control)` in `from borea.transform_world_image.transform_worksite.world_image_work import WorldImageWork`, with `type_control` egal None by default, is used if the type_point = gcp2d and if you want just one type code point, else None to process on all point. . The result can be found in `worksite.shots['name_shot'].gcps['name_gcp']` for each image and each gcps.

* Can calculate spatial resection for each shot in worksite with `SpaceResection(work).space_resection_on_worksite(add_pixel = (0,0))` in `from borea.transform_world_image.transform_worksite.space_resection import SpaceResection`. `add_pixel` is used to add a mainiation to the position of the points to modify the shot's 6 external parameters for data conversion.

* Can calculate spatial resection in poitn of shot for creating worksite with `SpaceResection(work).space_resection_to_worksite(pt2d, pt3d, pinit)` in `from borea.transform_world_image.transform_worksite.space_resection import SpaceResection`.  
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
Example at the end of explanation of function [file](https://github.com/IGNF/Borea/tree/main/docs/functions/Space_resection.md).

* You can calculate some control point statistics to see how accurate your site is `stat = Stat(work, pathreturn, control_type)` to init the object and run for all stat with `stat.main_stat_and_save()`. Make stat on function image to world and world to image, if there are data. And save result on *pathreturn/Stat_{Name_worksite}.txt*.

Examples in section [examples](#examples) below.

## Write data

* Can write worksite object as different format OPK, RPC, Conical for GEOVIEW. The function is `manager_reader(writer, name, pathreturn, args, work)` in `from borea.writer.manage_writer import manager_writer`:
    * `writer` (str), is the type of output `"opk"`, `"rpc"`, `"con"`.
    * `name` (str), name of file to save, just to save in opk, for other format this args isn't read.
    * `pathreturn` (str), path of folder where you want to save data.
    * `args` (dict), Dictionary with different args for the format to save, detail at setion [args for writing file](#args-for-writing-file) below.
    * `work` (Worksite), the worksite to save.

Examples in section [examples](#examples) below.

## Examples

All examples are in [borea github ./examples/](https://github.com/IGNF/Borea/tree/main/examples):
* For build main class Worksite with file **eg_build_worksite_by_file.py** and with data **eg_build_worksite_by_data.py**.
* To make transformation image to world **eg_image_to_world.py**.
* To make transformation world to image **eg_world_to_image.py**.
* To make space resection on point to determine worksite **eg_space_resection.py**.
* To convert format opk to an other format opk rpc con **eg_opk_to_format.py**.

Examples of the different formats of file can be found in [borea github ./dataset/](https://github.com/IGNF/Borea/tree/main/dataset):
* An opk file **23FD1305_alt_test.OPK** with z unit is altitude.
* Cameras filesformat **Camera1.txt** and **Camera2.txt**.
* Geotiff of the French geoid for pyproj fr_ign_RAF20.tif** detail at section [info projection](#info-projection) below.
* Crops geotiff of the French DTM **MNT_France_25m_h_crop.tif** in height unit.
* Ground Control Point (GCP) in terrian **GCP_test.app** unit z in height.
* Ground Control Point (GCP) in image **terrain_test.mes**.
* Connecting points in image **liaisons_test.mes**.
* Image point to transform terrain coordinates to image coordinates to find out in which image the points are located **terrain_test0.mes**.

## Detail

### Header of file opk
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

### Header of point file

`header` is used to describe the format of the point file read. It provides information on what's in each column.   
Type is:
| Symbol | Details |
| :----: | :------ |
| S | to ignore the column |
| P | name of the point |
| N | name of shot |
| T | type of point |
| X | coordinate x of the shot position |
| Y | coordinate y of the shot position |
| Z | coordinate z altitude of the shot position |

### Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its **name** (str), **ppax** (float), **ppay** (float), **focal** (float), image size: **width** (int) and **height** (int) in pixels.   
**Ppax** and **ppay** are the main points of image deformation in x and y directions.  
Each line of the file corresponds to a piece of information, starting with the **type = info**.
```
name = UCE-M3-f120-s06
ppax = 13210.00
ppay = 8502.00
focal = 30975.00
width = 26460
height = 17004
```
Only these 7 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool, unless the attribute has been added to the Camera class in *borea/datastruct/camera.py*.
An example file can be found in repository *./dataset/Camera1.txt*.

### Info projection

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The varaible in example for adding a geoid is path_geoid, a list which contains paths of geoids, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

### Args for writing file

#### OPK

There are 4 keys in the dictionary:
* "order_axe" (str): **Order of rotation matrix axes**.
* "header" (list): **List of column type** file (same to read opk).
* "unit_angle" (str): Unit of angle **'degree' or 'radian'**.
* "linear_alteration" (bool): **True** if data corrected by linear alteration or else **False**.

#### RPC

There are 3 keys in the dictionary:
* "size_grid" (int): **size of the grip** to calcule rpc.
* "order" (int): order of the polynome of the rpc. **[1, 2, 3]**
* "fact_rpc" (float): rpc factor for world coordinate when not src, we recommend **None**.

#### CON

There is no need for an additional argument, you can set **None** to the argument.

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)