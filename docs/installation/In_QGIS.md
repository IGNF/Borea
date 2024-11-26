# Installing borea in the QGIS environment.

Borea is installed in the QGIS environment using pip.

## Compatibility

You need to be aware of the compatibility of python versions and python libraries.
- python >= 3.9
- gdal >= 3.3.2
- numpy <= 1.26.4

Check that your QGIS uses a version of python higher than 3.9 .  
To see this: 
- you can open QGIS and click on *Help*, then *About* you should see the version of python and GDAL. 
- If not, go to the **C:\Program File\QGIS{n°version}\apps** folder, where you'll find a **Pyhton{n°version}** folder.  
If you want to know more about the python version and libraries. Enter the folder, open a terminal in this folder (type cmd in the path bar), then in the terminal type `python --version` for the python version and `python -m pip list` to see the python libraries linked to QGIS.

## Installation by linking the QGIS environment to your terminal

To do this, you need the path to the QGIS python folder, which should look like **C:\Program File\QGIS{n°version}\apps\Python{n°version}** and inside you'll find a python executable, a Scripts folder, Lib ... and in the Lib folder a site-package or ...-package folder containing folders for python libraries such as numpy.

The paths must be added to the Path variable:
- C:\Program Files\QGIS{n°version}\apps\Python{n°version}\
- C:\Program Files\QGIS{n°version}\apps\Python{n°version}\Scripts

And create a new PYTHONPATH variable with the path C:\Program Files\QGIS{n°version}\apps\Python{n°version}\Lib\site-packages

**Warning**, change the paths according to your needs - this is just an example.

You can open a terminal and use the `python` and `pip` commands, which will be linked to your QGIS environment. You can check with `python --version` to see if you have the QGIS python version, or core `pip list` to see all the python libraries used by QGIS

All you have to do is:
```
pip install ign-borea
```
to use it in QGIS with executables.

## Link details

- C:\Program Files\QGIS{n°version}\apps\Python{n°version}\ : allows you to use QGIS python with the `python` command.
- C:\Program Files\QGIS{n°version}\apps\Python{n°version}\Scripts: use executables linked to this environment (e.g. `opk-to-opk -h` or `pip` this is what allows you to make a pip list and see the QGIS python environment).
- C:\Program Files\QGIS{n°version}\apps\Python{n°version}\Lib\site-packages : allows you to link python packages from the QGIS environment to python (borea, numpy, ...).

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)