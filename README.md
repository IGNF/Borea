# Welcome to Pink Lady !!!

Pink Lady is an open-source tools-box photogrammetric conversion format and transformation coordinate of image and terrain.  
Why Pink Lady? Pink Lady is a B-17 owned by IGN France, originally used in the army, then used to acquire French territory. Now kept by an association, it became a historic monument in 2012.

## Tools

* Conversion OPK to OPK: [README_opk_to_opk.md](./README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Control OPK file: [README_opk_control.md](./README_opk_control.md)
* Convertion OPK to RPC: [README_opk_to_rpc.md](./README_opk_to_rpc.md) (RPC = Rational Polynomial Coefficients)
* Convertion OPK to Conl: [README_opk_to_conical.md](./README_opk_to_conical.md) (Conl = light conical file, IGN France format)
* Transforms coordinate terrain from image: [README_pt_image_to_world.md](./README_pt_image_to_world.md)
* Transforms coordinate image from terrain: [README_pt_world_to_image.md](./README_pt_world_to_image.md)
* Transforms coordinate file terrain from image: [README_ptfile_image_to_world.md](./README_ptfile_image_to_world.md)
* Transforms coordinate file image from terrain: [README_ptfile_world_to_image.md](./README_ptfile_world_to_image.md)
* Calculates opk by space resection: [README_spaceresection_opk.md](./README_spaceresection_opk.md)
* Python lib: [README_python_lib.md](./README_python_lib.md)

## Dependency

For conda/mamba environment the depencency is [dependency/environment.yml](./dependency/environment.yml).  
For pip environment (venv) the depencency is [dependency/requirements.txt](./dependency/requirements.txt) and you need to install `libgdal-dev`.

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
```

You can find more information on [mothergeo-py](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) if you have problems installing GDAL.

## Contributing

link: [CONTRIBUTING.md](./CONTRIBUTING.md)

![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)