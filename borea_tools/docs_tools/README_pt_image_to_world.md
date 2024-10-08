# Transforms world coordinate of image point

**pt_image_to_world** transforms the world coordinates of a image point in a given image.

## Application

Call the function from a terminal in the depot directory `python borea_tools/pt_image_to_world.py`. To view the information on the various parameters you can do : 

```python borea_tools/pt_image_to_world.py -h``` 

Or if you install the package by **pip** the commande is:

```pt-image-to-world -h```

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -n | Name of the shot. | 'Test' | X |
| -s | Position of the shot X Y Z. |  | V |
| -t | Unit of the z of the shot. "altitude" or "height" |  | V |
| -o | Orientation of the shot Omega Phi Kappa.|  | V |
| -p | Coordinate of the 2D point Column Line. |  | V |
| -d | Unit of the z of the data. "altitude" or "height". If None same type than z shot. | None | X |
| -b | Order of rotation matrix axes. | opk | X |
| -u | Unit of the angle of shooting, 'degree' or 'radian' | degree | X |
| -a | True if z shot corrected by linear alteration | True | X |
| -e | EPSG codifier number of the reference system used e.g. 2154 | None | X |
| -y | Path to the file pyproj GeoTIFF of geoid. | None | X |
| --geog | EPSG codifier number of the reference geographic system, filled in if pyproj error | None | X |
| --geoc | EPSG codifier number of the reference geocentric system, filled in if pyproj error | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -m | DTM of the worksite. | None | X |
| --fm | Format of Dtm "altitude" or "height". | None | X, unless dtm is given |
| -x | To use an approximate system. | False | X |

E.G.
```
python ./borea_tools/pt_image_to_world.py -n Test -s 814975.925 6283986.148 1771.280 -t altitude -o -0.245070686036 -0.069409621323 0.836320989726 -b opk -u degree -a True -e 2154 -y ./dataset/fr_ign_RAF20.tif -c ./dataset/Camera1.txt -m ./dataset/MNT_France_25m_h_crop.tif --fm height -p 24042.25 14781.17 -d height
```
or pip
```
pt-image-to-world -n Test -s 814975.925 6283986.148 1771.280 -t altitude -o -0.245070686036 -0.069409621323 0.836320989726 -b opk -u degree -a True -e 2154 -y ./dataset/fr_ign_RAF20.tif -c ./dataset/Camera1.txt -m ./dataset/MNT_France_25m_h_crop.tif --fm height -p 24042.25 14781.17 -d height
```

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
You can therefore specify as parameters the epsg ( --geog / --geoc ) you want to use for each type of projection.

![logo ign](../../docs/image/logo_ign.png) ![logo fr](../../docs/image/Republique_Francaise_Logo.png)