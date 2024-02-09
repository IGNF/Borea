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
| -f | File path of the workfile | | V |
| -s | Number of lines to be skipped before reading the file | 1 | X |
| -e | EPSG codifier number of the reference system used e.g. "2154" | "2154" | X |
| -p | Path to the json file which list the code epsg, you use | None | X |
| -y | Path to the folder which contains GeoTIFF | None | X |
| -o | Worksite output file format e.g. opk | None | X |
| -r | Conversion path e.g. "./" | "./" | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -l | Files paths of connecting points (.mes) | None | X |
| -t | Files paths of ground points image (.mes) | None | X |
| -g | Files paths of ground control point (.app) | None | X |
| -d | Type of gcp to control. | [] | X |
| -m | DEM of the worksite. | None | X |
| -a | Type of Dem "altitude" or "height". | None | X, unless dem is given |

Some settings are optional, depending on what you want to do with Pink Lady.
Only the first -f parameter is mandatory

E.G.
```
python3 pink_lady.py -f test/data/23FD1305_alt_test.OPK -e EPSG:2154 -w opk -c test/data/Camera.txt -w 26460 -a 17004 -l test/data/liaisons_test.mes -t test/data/terrain_test.mes -gcp test/data/GCP_test.app -m test/data/fr_ign_RAF20_test.tif
```

### Python scripte use

Creation of a worksite object from a worksite file (.opk) to be read by `reader_orientation(pathfile, skip)`. `skip` is an int that specifies the number of lines to skip at the beginning of the file.

Once the object has been created, you can add other data to it:

* The camera with `read_camera([filepath], worksite)`, this function only reads txt and xml files referencing camera data, and can take several camera files if there are several.

* Link points with `read_copoints([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files.

* Link points with `read_gipoints([filepath], worksite)`. Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files.

* Field points (GCPs) with `read_gcp([pathfile], worksite)`. Adds control and support terrain points in .app file format, can read multiple files.

* Can calculate the position of terrain points in images with `worksite.calculate_world_to_image_gcp([n])` with n the code of the points whose position is to be calculated. The result can be found in `worksite.shots['name_shot'].gcps['name_gcp']` for each image and each gcps (more on this in the next section).

* Can write worksite object as .opk

```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_reader

############# Data ###############

# path to photogrammetric site file
path_opk = "Worksite_FR_2024.OPK"

# path(s) to camera's file
path_camera = ["Camera.txt"]

# path(s) to connecting points file
path_copoints = ["liaison.mes"]

# path(s) to image ground control points file
path_gipoints = ["terrain.mes"]

# path(s) to ground control points file
path_gcps = ["GCP.app"]

# path to dem file
path_dem = "dem.tif"

# type of output file
writer = "opk"

# folder path for the output
pathreturn = "./"

################# Function ###################

# Readind data and create objet worksite
work = reader_orientation(path_opk, 1)

# Add a projection to the worksite
work.set_proj("EPSG:2154", "projection_epsg.json", "./data_geotiff/")

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_copoints(path_copoints, work)

# Reading ground controle point in image
read_gipoints(path_gipoints, work)

# Reading GCP
read_gcp(path_gcps, work)

# Add Dem to the worksite
work.add_dem(path_dem)

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp([3])

# Calculate shooting position with a factor pixel, to change projection for example
work.shootings_position(add_pixel = (0,0))

# Writing data
manager_reader(writer, pathreturn, work)
```
Examples of the different formats can be found in *test/data/*.

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
An example file can be found in ./test/data/Camera1.txt.

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
The important tags are : the first is the epsg code ("EPSG:2154") of the site's map projection, which refers to another dictionary that groups together the geocentric projection ("geoc") with its epsg code at the site location. The geographic projection ("geog") with its epsg code at the site location, and the geoid ("geoid"), which lists the names of the geotifs used by pyproj to obtain the value of the geoid on the site. Geoids can be found on pyproj's github (https://github.com/OSGeo/PROJ-data), then put in the usr/share/proj folder, which is native to pyproj, or in the env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj folder if you're using a special environment, or you can give in argument the path to the GeoTIFF forlder. You don't have to add the last "comment" tag.


![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)