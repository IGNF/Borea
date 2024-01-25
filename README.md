# Welcome to Pink Lady !!!

Pink Lady is a photogrammetric conversion and acquisition program in .OPK format. Open-source with a few tools, such as calculation of the position in the image (l,c) of a terrain point (X,Y,Z).

### Commit Message Header

```
<type>: <short summary>
  │            │
  │            └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|fix|refactor|test|clean|lint
```

### HTML documentation

Call the function in a terminal located in the directory of the pink_lady.py file. The command to run the function is:

```python pink_lady.py``` 

Then add the parameters:

| Symbol | Details | Default |
| :----: | :------ | :-----: |
| -f | File path of the workfile | |
| -skip | Number of lines to be skipped before reading the file | 1 |
| -epsg | EPSG codifier number of the reference system used ex: "EPSG:2154" | "EPSG:2154" |
| -pepsg | Path to the json file which list the code epsg, you use | None |
| -ptif | Path to the folder which contains GeoTIFF | None |
| -w | Worksite output file format ex:opk | None |
| -pr | Conversion path ex:test/tmp/ | 'test/tmp/' |
| -c | Files paths of cameras (.xml or .txt) | None |
| -wh | Width and height of the camera | None |
| -cp | Files paths of connecting points (.mes) | None |
| -gcp | Files paths of ground control point (.app) | None |

Some settings are optional, depending on what you want to do with Pink Lady.
Only the first -f parameter is mandatory

Html documentation python in docs/_build/html/index.hmlt
Markdown documentation function in docs/functions

### Functionality

1. Reading and writing an OPK file
2. Restructuring of read files to allow the addition of read files without modifying functions
    Structure file in reader folder: 
      - name : reader_ext.py
      - function : def read(file: str) -> Worksite:
3. Reading a camera file (XML and txt)
4. Reading connecting point (mes)
5. Reading ground control point (app)
6. Add projection and function to change of projection
7. Calculation of the image coordinates of gcp by the image function
8. Calculation of the ground coordinates of connecting point with a z estimate
9. Calculation of the ground coordinates of connecting point by intersection
10. Calculation of 6 externa parameters of shot with space_resection

### Utilisation

Creation of a worksite object from a worksite file (.opk) to be read by reader_orientation(pathfile, skip). Skip is an int that specifies the number of lines to skip at the beginning of the file.

Once the object has been created, you can add other data to it:

* The camera with read_camera([filepath], worksite), this function only reads txt and xml files referencing camera data, and can take several camera files if there are several.

* Link points with read_copoints([filepath], worksite). Add link points (.mes) to worksite. This function is also used to add the position of terrain points to images in .mes format (name_point name_shot col lig), can read several files.

* Field points (GCPs) with read_gcp([pathfile], worksite). Adds control and support terrain points in .app file format, can read multiple files.

* Can calculate the position of terrain points in images with worksite.calculate_world_to_image_gcp([n]) with n the code of the points whose position is to be calculated. The result can be found in worksite.shots['name_shot'].gcps['name_gcp'] for each image and each gcps (more on this in the next section).

* Can write worksite object as .opk

```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_reader

path_opk = "Worksite_FR_2024.OPK"
path_camera = ["Camera.txt"]
path_copoints = ["liaison.mes", "terrain.mes"]
path_gcps = ["GCP.app"]
writer = "opk"
pathreturn = "tmp/"

# Readind data and create objet worksite
work = reader_orientation(path_opk, 1)

# Add a projection to the worksite
work.set_proj("EPSG:2154", "projection_epsg.json", "./data_geotiff/")

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_copoints(path_copoints, work)

# Reading GCP
read_gcp(path_gcps, work)

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp([3])

# Calculate shooting position with a factor pixel, to change projection for example
work.shootings_position(add_pixel = (0,0))

# Writing data
manager_reader(writer, pathreturn, work)
```

### File projection JSON

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

More informations on functions in docs/function/  
Diagram of code structure Pink Lady in docs/diagram/

![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)