# Contributor information to Pink Lady

Make an issue on a new feature or bug found.  
Or get the repository and code the new functionality you want on a new branch and pull request on dev branch.

## Commit message header

Based on: https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit

```
<type>: <short summary>
  │            │
  │            └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|refactor|test
```
Type must be one of the following:

  * build: Changes that affect the build system or external dependencies (e.g. scopes: gulp, broccoli, npm)
  * ci: Changes to our CI configuration files and scripts (e.g. CircleCi, SauceLabs)
  * docs: Documentation only changes
  * feat: A new feature
  * fix: A bug fix
  * refactor: A code change that neither fixes a bug nor adds a feature
  * test: Coding tests or correcting existing tests

## Contributing of format reading/writing functions

Restructuring of read files to allow the addition of read files without modifying functions.  
Same thing with write files.
- Structure file in reader folder [borea/reader/orientation](./borea/reader/orientation/):
    - name : reader_{ext}.py
    - function : def read(file: str, args: dict, work: **Worksite**) -> **Worksite**:
- Structure file in writer folder [borea/writer](./borea/writer/): 
    - name : writer_{ext}.py
    - function : def write(name_file: str, path_folder: str, args: dict, work: **Worksite**) -> converted file:

args is a dictionary with different parameter which depends on what you read or write.  
e.g. to read opk
```
args = {"order_axe":'opk',
        "interval": [2, None],
        "header": list("NXYZOPKC"),
        "unit_angle": "degree",
        "linear_alteration":True}
```

## Contributing for new function to process Worksite

To add a new feature/function to process a worksite (*Worksite*). Adds a new class to enter a **Worksite**. Its file must be located in the folder corresponding to its theme: 
* [datastruct](./borea/datastruct/): Module for data structure class.
* [format](./borea/format/): Module for specific format class.
* [geodesy](./borea/geodesy/): Module for geodesic and projection class.
* [process](./borea/process/): Module to process of data (detail [below](#adding-a-processing-step)).
* [reader](./borea/reader/): Module for file reading functions.
* [stat](./borea/stat/): Module for statistic class.
* [transform_world_image](./borea/transform_world_image/): Module for transformation world to image and image to world class in different module.
* [utils](./borea/utils/): Various functions.
* [worksite](./borea/worksite/): Module for main class **Worksite**.
* [writer](./borea/writer/): Module for file writing functions.

If it's a new theme, add a new folder with an explicit name.

## Structure of main class Worksite

**Worksite** is the main class in the code that stores and manipulates data. It is located in [borea/worksite/worksite.py](./borea/worksite/worksite.py) and inherits from Workdata in [borea/datastruct/workdata.py](./borea/datastruct/workdata.py). The worksite class has no constructor; **Workdata** does. The constructor requires a single attribute, which is the name of the construction site.  
The class has 11 attributes:
* **name**: name of worksite
* **shots**: dictionary of shot {"name_shot": **Shot**}
* **cameras**: dictionary of cameras {"name_camera": Camera}
* **co_points**: dictionary of connecting point {"name_point": list["names_shots"]} to find out which image they fit into
* **gcp2d**: dictionary of gcp 2d {"name_gcp2d": list["names_shots"]} to find out which image they fit into
* **gcp3d**: dictionary of gcp 2d {"name_gcp3d": GCP}
* **co_pts_world**: dictionary of connecting point coordinate on the ground {"name_point": array[X, Y, Z]}
* **gcp2d_in_world**: dictionary of gcp2d on the ground {"name_point": array[X, Y, Z]}
* **type_z_data**: string which given unit of z of point "altitude" or "height"
* **type_z_shot**: string which given unit of z shot "altitude" or "height"
* **approxeucli**: boolean True to use approximate euclidean system and False to use reel euclidean system

Function to implement attributes:
* add_shot() for **shots**
* add_camera() for **cameras**
* add_co_point() for **co_points** in **Worksite** and in **Shot** (shots needs to implement before co_point)
* add_gcp2d() for **gcp2d** in **Worksite** and in **Shot** (shots needs to implement before gcp2d)
* add_gcp3d() for **gcp3d**
* set_approx_eucli_proj() for **approxeucli**
* set_type_z_shot() for **type_z_shot**
* set_type_z_data() for **type_z_data** if None in input type_z_data = type_z_shot (type_z_shot must be implement before)


**co_pts_world** and **gcp2d_in_world** are only implemented if world to image or image to world functions are used.

The class includes two other functions that implement two other singleton classes essential for calculations and conversions:
* **ProjEngine**, with set_proj(), which defines the site projection and lets you change the z-unit of altitude or height data if a geoid is specified.
* **Dtm**, with set_dtm(), which stores the DTM for linear alteration corrections.

## Adding a processing step

Processing files are used to build [function files](#functionality-file), and are divided into two parts (2 functions):
* The first function take an argparse in input and return an argparse with new arguments.
* The second function take argparse.parse_args() in input and **Worksite** or no to make the process of input parameters.

Processing files are grouped in [process](./borea/process/) folder and divided into 3 categories (3 folders):
* [p_add_data](./borea/process/p_add_data/): Reading files and data.
* [p_format](./borea/process/p_format/): Additional information on the different formats.
* [p_func](./borea/process/p_func/): Data processing, with some specific info sometimes.

If it's a new theme, add a new folder with an explicit name.

## Functionality file

Functionality file are grouped in [process](./tools) with an explicit file name for their function.  
The construction of such a file normally requires:
* Only 3 imports (argparse, the processing file to add the data, the processing file to process the data).
* Creating an argparse `parser = argparse.ArgumentParser(description='descriptif functionality')`.
* Retrieve arguments.
* Transforms parser into args `args = parser.parse_args()`.
* Processing arguments.

Look at the .py files already in [source](./borea).

## Re-generating sphinx documentation

In folder *./docs/sphinx/* do:
```
make clean
```
If you add new file, delete all file .rst in the repertory *./docs/sphinx/* except index.rst.  
At the root of the repository do:
```
sphinx-apidoc -o docs/sphinx borea
```
And in *./docs/sphinx/* do:
```
make html
```

## More information

Sphinx html documentation python code in *./docs/sphinx/_build/html/index.html*  
Mathematics documentation functions in [docs/functions/](./docs/functions/)  
Diagram of code structure Pink Lady in [docs/diagram/](./docs/diagram/)

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)