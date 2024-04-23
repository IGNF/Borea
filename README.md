# Welcome to Pink Lady !!!

Pink Lady is an open-source tools-box photogrammetric conversion format and transformation coordinate of image and terrain.  
Why Pink Lady? Pink Lady is a B-17 owned by IGN France, originally used in the army, then used to acquire French territory. Now kept by an association, it became a historic monument in 2012.

## Tools

* Conversion OPK to OPK: [implements/docs/README_opk_to_opk.md](./implements/docs/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Control OPK file: [implements/docs/README_opk_control.md](./implements/docs/README_opk_control.md)
* Convertion OPK to RPC: [implements/docs/README_opk_to_rpc.md](./implements/docs/README_opk_to_rpc.md) (RPC = Rational Polynomial Coefficients)
* Convertion OPK to Conl: [implements/docs/README_opk_to_conical.md](./implements/docs/README_opk_to_conical.md) (Conl = light conical file, IGN France format)
* Transforms coordinates terrain from image: [implements/docs/README_pt_image_to_world.md](./implements/docs/README_pt_image_to_world.md)
* Transforms coordinates image from terrain: [implements/docs/README_pt_world_to_image.md](./implements/docs/README_pt_world_to_image.md)
* Transforms coordinates file terrain from image: [implements/docs/README_ptfile_image_to_world.md](./implements/docs/README_ptfile_image_to_world.md)
* Transforms coordinates file image from terrain: [implements/docs/README_ptfile_world_to_image.md](./implements/docs/README_ptfile_world_to_image.md)
* Calculates opk by space resection: [implements/docs/README_spaceresection_opk.md](./implements/docs/README_spaceresection_opk.md)
* Python lib: [implements/docs/README_python_lib.md](./implements/docs/README_python_lib.md)

## Dependency

### Conda/Mamba
For conda/mamba environment the depencency is [dependency/environment.yml](./dependency/environment.yml).  

### Pip venv
For pip environment (venv) the depencency is [dependency/requirements.txt](./dependency/requirements.txt)  
and you need to install `libgdal-dev` and `GDAL>=3.3.2`.

## Installation

You need to retrieve the repository with ```git clone``` and install the environment. By ```conda``` or ```mamba``` with ```environment.yml``` or ```pip``` with ```requirements.txt```.

#### Conda/Mamba
```
conda env create -f ./dependency/environment.yaml
```
```
mamba env create -f ./dependency/environment.yaml
```

#### Pip
```
pip install -r ./dependency/requirements.txt
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