# Welcome to Borea !!!
[![IGNF badge](https://img.shields.io/badge/IGNF-8cbd3a)](https://www.ign.fr/) [![PyPI](https://img.shields.io/pypi/format/ign-borea)](https://pypi.org/project/ign-borea/)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md)

Borea is an open-source tools-box photogrammetric conversion format and coordinate transformations of images and terrain data.  
Why Borea? "B" stands for "Box", and "orea" is a backslang of "aero".

## Tools

* Conversion OPK to OPK: [borea_tools/docs_tools/README_opk_to_opk.md](./borea_tools/docs_tools/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Conversion Micmac xml to OPK: [borea_tools/docs_tools/README_mm_xml_to_opk.md](./borea_tools/docs_tools/README_mm_xml_to_opk.md) (Micmac = open-source photogrammetric software)
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

## Dependencies

Borea requires:
- python >= 3.9
- gdal >= 3.3.2
- numpy
- pyproj
- scipy
- pandas
- dataclasses

### Conda/Mamba
A Conda/Mamba environment is available at [borea_dependency/environment.yml](./borea_dependency/environment.yml).  

### Pip/venv
A a pip environment (venv), the requirements are available at [borea_dependency/requirements.txt](./borea_dependency/requirements.txt).
You also need to install `libgdal-dev` and `GDAL>=3.3.2`.

## Installation

There are two ways to install Borea: from the repository with `git clone`, or with pip using `pip install ign-borea` [documentation](./README_borea_lib.md).

With **the repository** version, you also need to install the environment.  
With **pip** version, the environment is included, but GDAL is not, and you must install it manually.

### Setting up the environment
#### Conda/Mamba
GDAL is included and installed in the Conda/Mamba environment.
```
conda env create -f ./borea_dependency/environment.yaml
```
```
mamba env create -f ./borea_dependency/environment.yaml
```

#### Pip
GDAL is not included in the pip environment, so you need to install it manually.
```
pip install -r ./borea_dependency/requirements.txt
sudo apt-get install libgdal-dev
```
You need the correct version of `GDAL`; you can check it with:
```
gdalinfo --version
```
Then install the marching version:
```
pip install GDAL==<GDAL VERSION>
```
You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) if you encounter issues installing GDAL.

#### In the QGIS environment

View the doc at [./docs/installation/In_QGIS.md](docs/installation/In_QGIS.md).

## Contributing

link: [CONTRIBUTING.md](./CONTRIBUTING.md)

## Licensing

Borea is licensed under the [MIT License](./LICENSE).

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)