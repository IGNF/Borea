# Transforms position and orientation of shot with point coordinate

**spaceresection_opk** transforms the 6 external parameters of an acquisition, X, Y, Z for its position and O, P, K for the 3 angles of orientation. To do this, we use least squares on points whose positions in the image and on the ground are known.

## Application

Call the function from a terminal in the depot directory `python borea_tools/spaceresection_opk.py`. To view the information on the various parameters you can do : 

```python borea_tools/spaceresection_opk.py -h``` 

Or if you install the package by **pip** the commande is:

```spaceresection-opk -h```

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -p | 3d coordinates of a point on the site at an approximate flying height to initialize the calculation. |  | V |
| -d | Unit of the z of the 3D point. |  | V |
| -t | File path of ground control points in images. |  | V |
| -k | Header of the file gcp2d. | PNXY | X |
| -g | File path of ground control points in ground. |  | V |
| -l | Header of the file gcp3d. | PTXYZ | V |
| -e | EPSG codifier number of the reference system used e.g. 2154 | 2154 | X |
| -y | Path to the file pyproj GeoTIFF of geoid. | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -m | DTM of the worksite. | None | X |
| --fm | Format of Dtm "altitude" or "height". | None | X, unless dtm is given |
| -x | To use an approximate system. | False | X |
| -n | Name of worksite output file |  | V |
| -w | Conversion path e.g. "./" | "./" | X |
| -o | Type of each column in the site file. e.g. NXYZOPKC with Z origin | NXY(Z/H)OPKC | X |
| -ob | Order of rotation matrix axes you want in output. | None | X |
| -ou | Unit of the angle of shooting, 'degree' or 'radian' | "degree" | X |
| -oa | True if z shot corrected by linear alteration. | True | X |

E.G.
```
python ./borea_tools/spaceresection_opk.py -p 825439 6289034 1500 -d height -c ./dataset/Camera1.txt -e 2154 -y ./dataset/fr_ign_RAF20.tif -m ./dataset/MNT_France_25m_h_crop.tif --fm height -t ./tools/test/data/dataset2/all_liaisons2.mes -k PNXY -g ./tools/test/data/dataset2/all_liaisons2_world.mes -l PXYH -n SpaceResection -o NXYZOPKC -ou degree -oa True
```
or pip
```
spaceresection-opk -p 825439 6289034 1500 -d height -c ./dataset/Camera1.txt -e 2154 -y ./dataset/fr_ign_RAF20.tif -m ./dataset/MNT_France_25m_h_crop.tif --fm height -t ./tools/test/data/dataset2/all_liaisons2.mes -k PNXY -g ./tools/test/data/dataset2/all_liaisons2_world.mes -l PXYH -n SpaceResection -o NXYZOPKC -ou degree -oa True
```

## Detail for the header of file -o
`header` is used to describe the format of the opk file read. It provides information on what's in each column, and gives the data unit for Z and angles.   
Type is:
| Symbol | Details |
| :----: | :------ |
| S | to ignore the column just for -i |
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
| H | coordinate z height of the shot position |

## Camera file format

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
Only these 7 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool, unless the attribute has been added to the [Camera class](../../borea/datastruct/camera.py).
An example file can be found in [./dataset/Camera1.txt](../../dataset/Camera1.txt).  
No camera-related distortion is taken into account (distortion-free camera).

## Info projection

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The command for adding a geoid is -y, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

This transformation is accompanied by other cartographic, geographic and geocentric transformations. And pyproj may not be able to find the other systems on its own.  
e.g.
```
>>>crsm = crs.CRS.from_epsg(4326)
>>>crs_geoc = pyproj.crs.GeocentricCRS(name=crsm.name, datum=crsm.datum.name)
File "...", line 171, in <module>
    crs_geoc = pyproj.crs.GeocentricCRS(name=crsm.name, datum=crsm.datum.name)
  File "...", line 1918, in __init__
    super().__init__(geocentric_crs_json)
  File "...", line 348, in __init__
    self._local.crs = _CRS(self.srs)
  File "pyproj/_crs.pyx", line 2378, in pyproj._crs._CRS.__init__
pyproj.exceptions.CRSError: Invalid projection: 
```
You can therefore specify as parameters the epsg ( -e ) you want to use for each type of projection in a precise order.  
[data_projection, geographic, geocentric]  
e.g. in commande line for 4326 error GeocentricCRS
```
-e 4326 None 4328
```
None allows you to ignore a system if it is found by pyproj, after you just need to find the right epsg.

![logo ign](../../docs/image/logo_ign.png) ![logo fr](../../docs/image/Republique_Francaise_Logo.png)