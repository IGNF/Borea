# Bienvenue dans Borea !!!
[![IGNF badge](https://img.shields.io/badge/IGNF-8cbd3a)](https://www.ign.fr/) [![PyPI](https://img.shields.io/pypi/format/ign-borea)](https://pypi.org/project/ign-borea/)
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md)

Borea est une boîte à outils open source pour la conversion de formats photogrammétriques et les transformations de coordonnées entre images et données terrain.\
Pourquoi Borea ? Le « B » signifie « Box » et « orea » est un verlan de « aero ».

## Outils

* Conversion OPK vers OPK : [borea_tools/docs_tools/README_opk_to_opk.md](./borea_tools/docs_tools/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Conversion XML Micmac vers OPK : [borea_tools/docs_tools/README_mm_xml_to_opk.md](./borea_tools/docs_tools/README_mm_xml_to_opk.md) (Micmac = logiciel photogrammétrique open source)
* Contrôle du fichier OPK : [borea_tools/docs_tools/README_opk_control.md](./borea_tools/docs_tools/README_opk_control.md)
* Conversion OPK vers RPC : [borea_tools/docs_tools/README_opk_to_rpc.md](./borea_tools/docs_tools/README_opk_to_rpc.md) (RPC = Rational Polynomial Coefficients)
* Conversion OPK vers Conl : [borea_tools/docs_tools/README_opk_to_conl.md](./borea_tools/docs_tools/README_opk_to_conl.md) (Conl = fichier conique léger, format IGN France)
* Transforme les coordonnées du terrain depuis l'image : [borea_tools/docs_tools/README_pt_image_to_world.md](./borea_tools/docs_tools/README_pt_image_to_world.md)
* Transforme les coordonnées de l'image depuis le terrain : [borea_tools/docs_tools/README_pt_world_to_image.md](./borea_tools/docs_tools/README_pt_world_to_image.md)
* Transforme le fichier de coordonnées du terrain depuis l'image : [borea_tools/docs_tools/README_ptfile_image_to_world.md](./borea_tools/docs_tools/README_ptfile_image_to_world.md)
* Transforme le fichier de coordonnées de l'image depuis le terrain : [borea_tools/docs_tools/README_ptfile_world_to_image.md](./borea_tools/docs_tools/README_ptfile_world_to_image.md)
* Calcule l'OPK par résection spatiale : [borea_tools/docs_tools/README_spaceresection_opk.md](./borea_tools/docs_tools/README_spaceresection_opk.md)
* Transforme la projection d'un fichier de points : [borea_tools/docs_tools/README_transform_proj_points.md](./borea_tools/docs_tools/README_transform_proj_points.md)
* Bibliothèque Python : [README_borea_lib.md](./README_borea_lib.md)

## Dépendances

Borea nécessite :
- python >= 3.9
- gdal >= 3.3.2
- numpy
- pyproj
- scipy
- pandas
- dataclasses

### Conda/Mamba
Un environnement Conda/Mamba est disponible dans [borea_dependency/environment.yml](./borea_dependency/environment.yml).

### Pip/venv
Pour un environnement pip (venv), les dépendances sont disponibles dans [borea_dependency/requirements.txt](./borea_dependency/requirements.txt).
Vous devez également installer `libgdal-dev` et `GDAL>=3.3.2`.

## Installation

Il existe deux façons d'installer Borea : depuis le dépôt avec `git clone`, ou via pip avec `pip install ign-borea` ([documentation](./README_borea_lib.md)).

Avec la version du dépôt, vous devez également installer l'environnement.
Avec la version pip, l'environnement est inclus, mais GDAL ne l'est pas et vous devez l'installer manuellement.

### Configuration de l'environnement
#### Conda/Mamba
GDAL est inclus et installé dans l'environnement Conda/Mamba.
```
conda env create -f ./borea_dependency/environment.yaml
```
```
mamba env create -f ./borea_dependency/environment.yaml
```

#### Pip
GDAL n'est pas inclus dans l'environnement pip, donc vous devez l'installer manuellement.
```
pip install -r ./borea_dependency/requirements.txt
sudo apt-get install libgdal-dev
```
Vous devez utiliser la bonne version de `GDAL` ; vous pouvez la vérifier avec :
```
gdalinfo --version
```
Ensuite, installez la version correspondante :
```
pip install GDAL==<GDAL VERSION>
```
Vous trouverez plus d'informations sur [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) si vous rencontrez des difficultés lors de l'installation de GDAL.

#### Dans l'environnement QGIS

Consultez la documentation : [./docs/installation/In_QGIS.md](docs/installation/In_QGIS.md).

## Contribuer

Lien : [CONTRIBUTING.md](./CONTRIBUTING.md)

## Licence

Borea est distribué sous la [licence MIT](./LICENSE).

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)
