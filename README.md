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
* Transform projection of points file: [borea_tools/docs_tools/README_transform_proj_points.md](./borea_tools/docs_tools/README_transform_proj_points.md)
* Python lib: [README_borea_lib.md](./README_borea_lib.md)

## Dependency

Borea needs:
- python >= 3.9
- gdal >= 3.3.2
- numpy <= 1.26.4
- pyproj
- scipy
- pandas
- dataclasses

### Conda/Mamba
For conda/mamba environment is [borea_dependency/environment.yml](./borea_dependency/environment.yml).  

### Pip venv
For pip environment (venv) is [borea_dependency/requirements.txt](./borea_dependency/requirements.txt)  
and you need to install `libgdal-dev` and `GDAL>=3.3.2`.

## Installation

There are two ways to install Borea with the repository `git clone` or with pip `pip install ign-borea` [doc](./README_borea_lib.md).

With **the repository**, you also need to install the environment.  
With **pip** the environment comes with it but does not contain GDAL, which you have to install yourself.

### Installation of the environment
#### Conda/Mamba
GDAL is contained and installed in the conda/mamba environment.
```
conda env create -f ./borea_dependency/environment.yaml
```
```
mamba env create -f ./borea_dependency/environment.yaml
```

#### Pip
GDAL is not included in the pip environment, so you have to install it yourself.
```
pip install -r ./borea_dependency/requirements.txt
sudo apt-get install libgdal-dev
```
You need the version of `GDAL` and you can get it back with:
```
gdalinfo --version
```
after
```
pip install GDAL==<GDAL VERSION>
```
You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) if you have problems installing GDAL.

#### In the QGIS environment

View the doc at [./docs/installation/In_QGIS.md](docs/installation/In_QGIS.md).

## Contributing

link: [CONTRIBUTING.md](./CONTRIBUTING.md)

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)