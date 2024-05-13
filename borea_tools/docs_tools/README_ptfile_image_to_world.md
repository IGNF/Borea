# Transforms file of image point in ground.

**ptfile_image_to_world** transforms the terrain coordinates of an image point file from the images in the opk file.

## Application

Call the function from a terminal in the depot directory `python borea_tools/ptfile_image_to_world.py`. To view the information on the various parameters you can do : 

```python borea_tools/ptfile_image_to_world.py -h``` 

Or if you install the package by **pip** the commande is:

```ptfile-image-to-world -h```

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -r | File path of the workfile | | V |
| -i | Type of each column in the site file. e.g. NXYZOPKC with Z in altitude | NXYZOPKC | X |
| -b | Order of rotation matrix axes. | opk | X |
| -u | Unit of the angle of shooting, 'degree' or 'radian' | degree | X |
| -a | True if z shot corrected by linear alteration | True | X |
| -f | Line number to start file playback. Does not take file header into account. | None | X |
| -z | Line number to end file playback. If not set, all lines below -l will be read. | None | X |
| -e | EPSG codifier number of the reference system used e.g. 2154 | 2154 | X |
| -y | Path to the file pyproj GeoTIFF of geoid. | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -m | DTM of the worksite. | None | X |
| --fm | Format of Dtm "altitude" or "height". | None | X, unless dtm is given |
| -x | To use an approximate system. | False | X |
| -t | Files paths of ground image points |  | V |
| -k | Header of the file gcp2d. | PNXY | X |
| -p | Type of process for the function image to world, "inter" for intersection or "square" for least-square | "inter" | X |
| -n | Name of the file to save. |  | V |
| -w | Path stat e.g. "./" | "./" | X |

E.G.
```
python ./borea_tools/ptfile_image_to_world.py -r ./dataset/23FD1305_alt_test.OPK -i NXYZOPKC -f 2 -c ./dataset/Camera1.txt -e 2154 -y ./dataset/fr_ign_RAF20.tif -m ./dataset/MNT_France_25m_h_crop.tif --fm height -t ./dataset/terrain_test.mes -p square -n Coor3d_pt_image
```
or pip
```
ptfile-image-to-world -r ./dataset/23FD1305_alt_test.OPK -i NXYZOPKC -f 2 -c ./dataset/Camera1.txt -e 2154 -y ./dataset/fr_ign_RAF20.tif -m ./dataset/MNT_France_25m_h_crop.tif --fm height -t ./dataset/terrain_test.mes -p square -n Coor3d_pt_image
```

## Detail for the header of file -i

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

## Detail for the header of point file -k and -l

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

## Detail for reading files

To read the opk file, you can select a line interval to be read using the -f parameter for the first line and -z for the last line. If not set, the entire file will be read. Please note that the header in the file is not taken into account and must therefore either be skipped with the -f parameter or commented out with a # at the beginning of the line. You can therefore add comments to the file with a # at the beginning of the line.

Connecting point files, gcp in the field and gcp in images must not have a file header in the file, or the header must be commented out with a # in front of it. You can therefore add comments to the file with a # at the beginning of the line.

## Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its **name** (str), **ppax** (float), **ppay** (float), **focal** (float), image size: **width** (int) and **height** (int) in pixels and **size_pizel** (float) size of pixel in meter.  
**size_pixel** is optional except for conversion to a conical file.  
**Ppax** and **ppay** are the main points of image deformation in x and y directions.  
Each line of the file corresponds to a piece of information, starting with the **type = info**.
```
name = UCE-M3-f120-s06
ppax = 13210.00
ppay = 8502.00
focal = 30975.00
width = 26460
height = 17004
size_pixel = 4e-6
```
Only these 7 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool, unless the attribute has been added to the [Camera class](../../borea/datastruct/camera.py).
An example file can be found in [./dataset/Camera1.txt](../../dataset/Camera1.txt).

## Info projection

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The command for adding a geoid is -y, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

## Detail for process

### Intersection

Calculations of world coordinates by intersect bundle of point in 2 more distant shots.  
Needs:
* at least one point on two images, otherwise it won't calculate the coordinates.

No needs:
* DTM (if no dtm and z shot is corrected by the linear alteration the result won't be as good)

### Least square

Calculations of world coordinates by least square methode.  
Needs:
* DTM

`intersection` has a better accuracy than `least_square`.

## Detail for approx system

The approximate system is used to set up a local tangent frame of reference for each acquisition in a purely mathematical way, without geodesy. To be used if the **data is corrected by linear alteration**, all data must be in the **same Z coordinate system** (altimetric or height), and there is **no need for the .json projection file**, **nor for DTM** if you are not using the image to world function with least square processing.  
You can also use it with data not in the same Z repository, but you need the data in the .json projection file.  
However, the calculation is less accurate in the approximate system.

![logo ign](../../docs/image/logo_ign.png) ![logo fr](../../docs/image/Republique_Francaise_Logo.png)