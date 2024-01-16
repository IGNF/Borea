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
| -w | Worksite output file format ex:opk | None |
| -pr | Conversion path ex:test/tmp/ | 'test/tmp/' |
| -c | Files paths of cameras (.xml or .txt) | None |
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
8. Calculation of the ground coordinates of connecting point by intersection

### Utilisation

------------- A REMPLIR ---------------- (descriptif du pink_lady.py) 

### Image function

To use the image function, you need :
- a terrain points file (.app) with points in code 1, 2 or 3
- a file (.mes) listing the position of the points in the images they appear in, this .mes file can be started with coordinates 0, 0 for the point coordinates, it just lets you know in which images the terrain points appear.
- a projection and its characteristics in a JSON, example of JSON structure:
```
{
"EPSG:2154": {
  "geoc": "EPSG:4964", 
  "geog": "EPSG:7084",
  "geoid": ["fr_ign_RAF20"],
  "comment": "Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93"}
}
```
The important tags are : the first is the epsg code ("EPSG:2154") of the site's map projection, which refers to another dictionary that groups together the geocentric projection ("geoc") with its epsg code at the site location. The geographic projection ("geog") with its epsg code at the site location, and the geoid ("geoid"), which lists the names of the geotifs used by pyproj to obtain the value of the geoid on the site. Geoids can be found on pyproj's github (https://github.com/OSGeo/PROJ-data), then put in the usr/share/proj folder, which is native to pyproj, or in the env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj folder if you're using a special environment. You don't have to add the last "comment" tag.

### Ground coordinates by intersection



![logo ign](docs/logo/IGN_logo_2012.svg =50x) ![logo fr](docs/logo/Republique_Francaise_Logo.png =50x)