# Welcome to Pink Lady !!!

Pink Lady is a photogrammetric conversion and acquisition program in .OPK format. Open-source with a few tools, such as calculation of the position in the image (l,c) of a terrain point (X,Y,Z), data control with GCP and statistical results .  
Why Pink Lady? Pink Lady is a B-17 owned by IGN France, originally used in the army, then used to acquire French territory. Now kept by an association, it became a historic monument in 2012.

## Functionality

1. Reading and writing an OPK file
2. Reading a camera file (XML and txt)
3. Reading connecting point (mes)
4. Reading ground control point (app)
5. Add projection and function to change of projection
6. Add DEM on the worksite
7. Calculation of the image coordinates of gcp by the image function
8. Calculation of the ground coordinates of connecting point with a z estimate
9. Calculation of the ground coordinates of connecting point by intersection
10. Calculation of 6 externa parameters of shot with space_resection
11. Calculation of statistics on ground contol point

## Installation

You need to retrieve the repository on this machine with ```git clone <link html>``` or with ssh key.  
Then, in an environment or on this machine, install the dependencies with pip or conda/mamba.
Pull the git repository on your computer and install the environment. By ```conda``` or ```mamba``` with ```environment.yml``` or ```pip``` with ```requirements.txt```.

#### Conda/Mamba
```
conda env create -f environment.yaml
```
```
mamba env create -f environment.yaml
```

#### Pip
```
pip install -r requirements.txt
```

You may experience errors when installing GDAL with pip.  
If you are working in an environment where GDAL is already installed on your machine. You need to retrieve the version of your gdal on your machine with ```ogrinfo --version``` then use the same version for ```pip install GDAL=<version>```.  
If GDAL does not exist, install libgdal-dev with sudo.
```
sudo apt-get install libgdal-dev
```
You’ll also need to export a couple of environment variables for the compiler.
```
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```
Now you can use pip to install the Python GDAL bindings ```ogrinfo --version```.
```
pip install GDAL==<GDAL VERSION FROM OGRINFO>
```

You can find more information on https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html .

## Utilisation

### Terminal use

Call the function in a terminal located in the directory of the pink_lady.py file. To view the information on the various parameters you can do : 

```python pink_lady.py -h``` 

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -w | File path of the workfile | | V |
| -i | Type of each column in the site file. e.g. N X Y Zal Od Pd Kd C |  | V |
| -f | Line number to start file playback. Does not take file header into account. | None | X |
| -z | Line number to end file playback. If not set, all lines below -l will be read. | None | X |
| -e | EPSG codifier number of the reference system used e.g. "2154" | "2154" | X |
| -p | Path to the json file which list the code epsg, you use | None | X |
| -y | Path to the folder which contains GeoTIFF | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -l | Files paths of connecting points (.mes) | None | X |
| -t | Files paths of ground image points (.mes) | None | X |
| -g | Files paths of ground control point (.app) | None | X |
| -d | Type of gcp to control. | [] | X |
| --fg | Format of GCP and ground image points "altitude" or "height". | None | X, unless gcp and gip is given |
| -m | DEM of the worksite. | None | X |
| --fm | Format of Dem "altitude" or "height". | None | X, unless dem is given |
| -o | Worksite output file format e.g. opk | None | X |
| -r | Conversion path e.g. "./" | "./" | X |

Some settings are optional, depending on what you want to do with Pink Lady.
Only -w and -i parameters is mandatory.

E.G.
```
python3 pink_lady.py -w dataset/23FD1305_alt_test.OPK -i N X Y Zal Od Pd Kd C -f 2 -e EPSG:2154 -p dataset/proj.json -y dataset/ -c dataset/Camera.txt -l dataset/liaisons_test.mes -t dataset/terrain_test.mes -g dataset/GCP_test.app --fg height -m dataset/MNT_France_25m_h_crop.tif --fm height -o opk
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
| Z | coordinate z of the shot position |
| O | omega rotation angle |
| P | phi rotation angle |
| K | kappa rotation angle |
| C | name of the camera |

Add unit for Z and angle:
| Symbol | Details |
| :----: | :------ |
| h | height for Z |
| hl | height with linear alteration for Z |
| a | altitude for Z |
| al | altitude with linear alteration for Z |
| d | degrees for O P K |
| r | radian for O P K |

### Python scripte use

Creation of a worksite object from a worksite file (.opk) to be read by `reader_orientation(pathfile, [first_line, last_line], header)`. `[first_line, last_line]` is an list of int that specifies the number of lines you want to read. `first_line` allows you to skip the file header, which must not be taken into account when reading the file, as specified in the `header` variable. If `first_line = None` skips everything up to `last_line`, if `lastline = None` skips everything from `first_line` to the end, and if both are None skips the entire file. And `header` described in the section above, is a list of str e.g. `['N', 'X', 'Y', 'Zal', 'Od', 'Pd', 'Kd', 'C']`

Once the object has been created, you can add other data to it:

* The camera with `read_camera([filepath], worksite)`, this function only reads txt and xml files referencing camera data, and can take several camera files if there are several.

* Link points with `read_copoints([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files.

* Link points with `read_gipoints([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files. In addition, the z data type 'h' for height and 'a' for altitude must be added to worksite `worksite.type_z_data = 'a'`. 

* Field points (GCPs) with `read_gcp([pathfile], worksite)`. Adds control and support terrain points in .app file format, can read multiple files. In addition, the z data type 'h' for height and 'a' for altitude must be added to worksite `worksite.type_z_data = 'a'`. 

* Add Dem to your worksite `work.add_dem(path_dem, type_dem)`, It converts z data between gcp and acquisition position if these are not in the same unit (one in altitude and one in height). `type_dem` is the unit of the dem 'altitude', 'a' or 'height', 'h'.

* Can calculate the position of terrain points in images with `worksite.calculate_world_to_image_gcp([n])` with n the code of the points whose position is to be calculated. The result can be found in `worksite.shots['name_shot'].gcps['name_gcp']` for each image and each gcps (more on this in the next section).

* You can calculate some control point statistics to see how accurate your site is `stat = Stat(work, pathreturn, control_type)` to init the object and run for all stat with `stat.main_stat_and_save()`. Make stat on function image to world and world to image, if there are data. And save result on *pathreturn/Stat_{Name_worksite}.txt*.

* Can write worksite object as .opk

```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_reader

############# Data ###############

# path to photogrammetric site file
path_opk = "dataset/23FD1305_alt_test.OPK"

# line taken and header
line_taken = [2, None]
header = ['N', 'X', 'Y', 'Zal', 'Od', 'Pd', 'Kd', 'C']

# info in epsg and epsg data
epsg = "EPSG:2154"
proj_json = "dataset/proj.json"
folder_geoid = "dataset/"

# path(s) to camera's file
path_camera = ["dataset/Camera1.txt"]

# path(s) to connecting points file
path_copoints = ["dataset/liaisons_test.mes"]

# path(s) to image ground control points file
path_gipoints = ["dataset/terrain_test.mes"]

# path(s) to ground control points file with unit of z and code of control point
path_gcps = ["dataset/GCP_test.app"]
type_z_data = 'height'
type_control = [13]

# path to dem file and unit of the dem
path_dem = "dataset/MNT_France_25m_h_crop.tif"
type_dem = "height"

# type of output file
writer = "opk"

# folder path for the output
pathreturn = "./"

################# Function ###################

# Readind data and create objet worksite
work = reader_orientation(path_opk, line_taken, header)

# Add a projection to the worksite
work.set_proj(epsg, proj_json, folder_geoid)

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_copoints(path_copoints, work)

# Reading ground controle point in image
read_gipoints(path_gipoints, work)

# Reading GCP
read_gcp(path_gcps, work)
work.type_z_data = type_z_data

# Add Dem to the worksite
work.add_dem(path_dem, type_dem)

# Calculate image coordinate of GCP if they exist for 2 type
work.calculate_world_to_image_gcp([3,13])

# Calculate shooting position with a factor pixel, to change projection for example
work.shootings_position(add_pixel = (0,0))

stat = Stat(work, pathreturn, type_control)
stat.main_stat_and_save()

# Writing data
manager_reader(writer, pathreturn, work)
```
Examples of the different formats can be found in *./dataset/*.

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

You can contribute by putting your structure in the *projection_list.json* file in *resources*.

![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)