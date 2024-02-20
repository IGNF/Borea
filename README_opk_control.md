# README to convert opk to opk

Converts an opk file into an opk file by changing column order, rotation angle units, a transformation of z into altitude or height with or without correction for linear alteration

## Utilisation

### Terminal use

Call the function in a terminal located in the directory of the pink_lady.py file. To view the information on the various parameters you can do : 

```python opk_control.py -h``` 

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -r | File path of the workfile | | V |
| -i | Type of each column in the site file. e.g. "N X Y Z O P K C" |  | V |
| -u | Unit of the angle of shooting, 'degree' or 'radian' | degree | X |
| -a | True if z shot corrected by linear alteration | True | X |
| -f | Line number to start file playback. Does not take file header into account. | None | X |
| -z | Line number to end file playback. If not set, all lines below -l will be read. | None | X |
| -e | EPSG codifier number of the reference system used e.g. 2154 | 2154 | X |
| -j | Path to the json file which list the code epsg, you use | None | X |
| -y | Path to the folder which contains GeoTIFF | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -m | DEM of the worksite. | None | X |
| --fm | Format of Dem "altitude" or "height". | None | X, unless dem is given |
| -t | Files paths of ground image points (.mes) | None | X |
| -g | Files paths of ground control point (.app) | None | X |
| -d | Type of gcp to control. | [] | X |
| --fg | Format of GCP and ground image points "altitude" or "height". | None | X, unless gcp and gip is given |
| -w | Path stat e.g. "./" | "./" | X |

E.G.
```
python3 ./opk_control.py -r ./dataset/23FD1305_alt_test.OPK -i "N X Y Z O P K C" -f 2 -c ./dataset/Camera1.txt -e 2154 -j ./dataset/proj.json -y ./dataset/ -m ./dataset/MNT_France_25m_h_crop.tif --fm height -t ./dataset/terrain_test.mes -g ./dataset/GCP_test.app -d 13 --fg height
```

#### Detail for the header of file -i
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

### Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its name, ppax, ppay, focal and image size, width and height in pixels.
Ppax and ppay are the main points of image deformation in x and y directions.
Each line of the file corresponds to a piece of information, starting with the type = info.
```
name = UCE-M3-f120-s06
ppax = 13210.00
ppay = 8502.00
focal = 30975.00
width = 26460.00
height = 17004.00
```
An example file can be found in *./dataset/Camera1.txt*.

### File projection JSON format

This library requires different projection data to transform coordinates from terrain to image and image to terrain. To do this, a JSON file containing the various projections and epsg code required is requested as input if you want to perform transformations, bearings or an aerial triangulation data, example of JSON structure:
```
{
"EPSG:2154": {
  "geoc": "EPSG:4964", 
  "geog": "EPSG:7084",
  "geoid": ["fr_ign_RAF20"],
  "comment": "Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93"}
}
```
The important tags are : the first is the epsg code ("EPSG:2154") of the site's map projection, which refers to another dictionary that groups together the geocentric projection ("geoc") with its epsg code at the site location. The geographic projection ("geog") with its epsg code at the site location, and the geoid ("geoid"), which lists the names of the geotifs used by pyproj to obtain the value of the geoid on the site. Geoids can be found on pyproj's github (https://github.com/OSGeo/PROJ-data), then put in the *usr/share/proj* folder, which is native to pyproj, or in the *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj* folder if you're using a special environment, or you can give in argument the path to the GeoTIFF forlder. You don't have to add the last "comment" tag.

You can contribute by putting your structure in the *projection_list.json* file in *./resources/*.

![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)