# Convert opk to light conical file for GEOVIEW IGN

**opk_to_conl** Converts an opk file into a light conical file (.CON). This format is an xml format for [GEOVIEW]() **add link ???**, it's a IGN France software to view image.

## Application

Call the function from a terminal in the depot directory `python implements/opk_to_conl.py`. To view the information on the various parameters you can do : 

```python implements/opk_to_conl.py -h``` 

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
| -w | Conversion path e.g. "./" | "./" | X |

E.G.
```
python ./implements/opk_to_conical.py -r ./dataset/23FD1305_alt_test.OPK -i NXYZOPKC -f 2 -e 2154 -y ./dataset/fr_ign_RAF20.tif -c ./dataset/Camera1.txt -m ./dataset/MNT_France_25m_h_crop.tif --fm height
```

## Detail for the header of file -i and -o
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

## Detail for reading files

To read the opk file, you can select a line interval to be read using the -f parameter for the first line and -z for the last line. If not set, the entire file will be read. Please note that the header in the file is not taken into account and must therefore either be skipped with the -f parameter or commented out with a # at the beginning of the line. You can therefore add comments to the file with a # at the beginning of the line.

## Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its **name** (str), **ppax** (float), **ppay** (float), **focal** (float), image size: **width** (int) and **height** (int) in pixels and **size_pizel** (float) size of pixel in meter.    
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
Only these 7 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool, unless the attribute has been added to the [Camera class](./src/datastruct/camera.py).
An example file can be found in [./dataset/Camera1.txt](./dataset/Camera1.txt).

## Info projection

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The command for adding a geoid is -y, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

![logo ign](../../docs/image/logo_ign.png) ![logo fr](../../docs/image/Republique_Francaise_Logo.png)