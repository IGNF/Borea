# Welcome to Pink Lady !!!

Pink Lady is a photogrammetric conversion and acquisition program in .OPK format. Open-source with a few tools, such as calculation of the position in the image (l,c) of a terrain point (X,Y,Z), data control with GCP and statistical results. Or convert OPK file to RPC and save to txt.  
Why Pink Lady? Pink Lady is a B-17 owned by IGN France, originally used in the army, then used to acquire French territory. Now kept by an association, it became a historic monument in 2012.

## Functionality

* Conversion OPK to OPK: [README_opk_to_opk.md](./README_opk_to_opk.md)
* Control OPK file: [README_opk_control.md](./README_opk_control.md)
* Convertion OPK to RPC: [README_opk_to_rpc.md](./README_opk_to_rpc.md)
* Calculate image coordinate of one ground point: [README_calc_pt_image.md](./README_calc_pt_image.md)
* Calculate world coordinate of one image point: [README_calc_pt_world.md](./README_calc_pt_world.md)
* Python lib: [README_python_lib.md](./README_python_lib.md)

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

You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) .

![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)