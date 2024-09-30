# Transforms projection of points file and type of z

**transform_proj_points** change projection of points file. Give file of points, header, epsg of points and epsg you want in output.  
The transformation is made by pyproj. In addition, you can change the z type of data with a geoid and type of z you want in output. 

## Application

Call the function from a terminal in the depot directory `python borea_tools/transform_proj_points.py`. To view the information on the various parameters you can do : 

```python borea_tools/transform_proj_points.py -h``` 

Or if you install the package by **pip** the commande is:

```transform-proj-points -h```

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -g | File path of points in ground. |  | V |
| -l | Header of the file gcp3d. | PTXYZ | V |
| -e | EPSG codifier number of the reference system used e.g. 2154 | | V |
| -y | Path to the file pyproj GeoTIFF of geoid. | None | X |
| --geog | EPSG codifier number of the reference geographic system, filled in if pyproj error | None | X |
| --geoc | EPSG codifier number of the reference geocentric system, filled in if pyproj error | None | X |
| --oe | Code epsg for output data. If none keeps the input data projection. | None | X |
| --oz | Z type of data you want in output altitude or height | None | X |
| -n | Name of worksite output file |  | V |
| -w | Conversion path e.g. "./" | "./" | X |

E.G.
```
python ./borea_tools/transfom_proj_points.py -g ./dataset/GCP_test.app -l PTXYZ -e 2154 -y ./dataset/fr_ign_RAF20.tif --oe 4326 --oz height -n GCP_4326 -w ./test/tmp
```
or pip
```
transfom-proj-points -g ./dataset/GCP_test.app -l PTXYZ -e 2154 -y ./dataset/fr_ign_RAF20.tif --oe 4326 --oz height -n GCP_4326 -w ./test/tmp
```

## Detail for the header of point file -l

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