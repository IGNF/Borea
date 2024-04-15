# README to calculate image coordinate of world point

Calculates the image coordinates of a terrain point in a given image.

## Utilisation

### Terminal use

Call the function in a terminal located in the directory of the pt_world_to_image.py file. To view the information on the various parameters you can do : 

```python pt_world_to_image.py -h``` 

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -n | Name of the shot. | 'Test' | X |
| -s | Position of the shot X Y Z. |  | V |
| -t | Unit of the z of the shot. "altitude" or "height" |  | V |
| -o | Orientation of the shot Omega Phi Kappa.|  | V |
| -p | Coordinate of the 3D point X Y Z. |  | V |
| -d | Unit of the z of the data. "altitude" or "height". If None same type than z shot. | None | X |
| -b | Order of rotation matrix axes. | opk | X |
| -u | Unit of the angle of shooting, 'degree' or 'radian' | degree | X |
| -a | True if z shot corrected by linear alteration | True | X |
| -e | EPSG codifier number of the reference system used e.g. 2154 | 2154 | X |
| -y | Path to the file pyproj GeoTIFF of geoid. | None | X |
| -c | Files paths of cameras (.xml or .txt) | None | X |
| -m | DTM of the worksite. | None | X |
| --fm | Format of Dtm "altitude" or "height". | None | X, unless dtm is given |
| -x | To use an approximate system. | False | X |

E.G.
```
python3 ./pt_world_to_image.py -n Test -s 814975.925 6283986.148 1771.280 -t altitude -o -0.245070686036 -0.069409621323 0.836320989726 -b opk -u degree -a True -e 2154 -y ./dataset/fr_ign_RAF20.tif -c ./dataset/Camera1.txt -m ./dataset/MNT_France_25m_h_crop.tif --fm height -p 24042.25 14781.17 -d height
```

### Camera file format

The camera file is a txt file, containing 6 pieces of information about the camera : its **name** (str), **ppax** (float), **ppay** (float), **focal** (float) and image size, **width** (int) and **height** (int) in pixels. .  
Ppax and ppay are the main points of image deformation in x and y directions.  
Each line of the file corresponds to a piece of information, starting with the **type = info**.
```
name = UCE-M3-f120-s06
ppax = 13210.00
ppay = 8502.00
focal = 30975.00
width = 26460
height = 17004
```
Only these 6 pieces of information will be read. You can add comments with a # in the first element of the line or other type = info, but they will not be read by the tool.
An example file can be found in *./dataset/Camera1.txt*.

### Info projection

This library can transform and process 3D data with a z in altitude or height. This is done by the pyproj library, which needs the geoid at site level to change units.

The command for adding a geoid is -y, where you can enter the paths to the various geoids. If the file is stored in pyproj's native folder (pyproj.datadir.get_data_dir(), *usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*) the file name is sufficient pyproj will find it on its own. 
Geoids file can be found on pyproj's github (https://github.com/OSGeo/PROJ-data).

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)