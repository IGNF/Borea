# Welcome to Borea !!!
[![IGNF badge](https://img.shields.io/badge/IGNF-8cbd3a)](https://www.ign.fr/) [![PyPI Downloads](https://img.shields.io/pypi/dm/ign-borea.svg?label=PyPI%20downloads)](
https://pypi.org/project/ign-borea/)

Borea is an open-source tools-box photogrammetric conversion format and transformation coordinate of image and terrain.  
Why Borea? B for Box and orea is a back slang of aero.

## Tools

* Conversion OPK to OPK: [borea_tools/docs_tools/README_opk_to_opk.md](./borea_tools/docs_tools/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Control OPK file: [borea_tools/docs_tools/README_opk_control.md](./borea_tools/docs_tools/README_opk_control.md)
* Conversion OPK to RPC: [borea_tools/docs_tools/README_opk_to_rpc.md](./borea_tools/docs_tools/README_opk_to_rpc.md) (RPC = Rational Polynomial Coefficients)
* Conversion OPK to Conl: [borea_tools/docs_tools/README_opk_to_conl.md](./borea_tools/docs_tools/README_opk_to_conl.md) (Conl = light conical file, IGN France format)
* Transforms coordinates terrain from image: [borea_tools/docs_tools/README_pt_image_to_world.md](./borea_tools/docs_tools/README_pt_image_to_world.md)
* Transforms coordinates image from terrain: [borea_tools/docs_tools/README_pt_world_to_image.md](./borea_tools/docs_tools/README_pt_world_to_image.md)
* Transforms coordinates file terrain from image: [borea_tools/docs_tools/README_ptfile_image_to_world.md](./borea_tools/docs_tools/README_ptfile_image_to_world.md)
* Transforms coordinates file image from terrain: [borea_tools/docs_tools/README_ptfile_world_to_image.md](./borea_tools/docs_tools/README_ptfile_world_to_image.md)
* Calculates opk by space resection: [borea_tools/docs_tools/README_spaceresection_opk.md](./borea_tools/docs_tools/README_spaceresection_opk.md)
* Python lib: [README_borea_lib.md](./README_borea_lib.md)

## Dependency

### Conda/Mamba
For conda/mamba environment the depencency is [borea_dependency/environment.yml](./borea_dependency/environment.yml).  

### Pip venv
For pip environment (venv) the depencency is [borea_dependency/requirements.txt](./borea_dependency/requirements.txt)  
and you need to install `libgdal-dev` and `GDAL>=3.3.2`.

## Installation

You need to retrieve the repository with ```git clone``` and install the environment. By ```conda``` or ```mamba``` with ```environment.yml``` or ```pip``` with ```requirements.txt```.

#### Conda/Mamba
```
conda env create -f ./borea_dependency/environment.yaml
```
```
mamba env create -f ./borea_dependency/environment.yaml
```

#### Pip
The package exists on pip with `pip install ign-borea` without GDAL

```
pip install -r ./borea_dependency/requirements.txt
sudo apt-get install libgdal-dev
```
Please note that the `GDAL` version depends on the `libgdal-dev` version.
```
apt-cache show libgdal-dev
# or if you are ogr
ogrinfo --version
```
```
pip install GDAL==<GDAL VERSION FROM OGRINFO>
```
You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) if you have problems installing GDAL.

## Contributing

link: [CONTRIBUTING.md](./CONTRIBUTING.md)

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)