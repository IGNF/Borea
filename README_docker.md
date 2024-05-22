# Using the dockerfile

## Setup docker on your machine

[Docker guide](https://docs.docker.com/get-docker/) for setup docker.

## Build dockerfile

Issue the following command in the Dockerfile directory to create docker image.
```
docker build -t <name_image> .
```
You can see the image with:
```
docker images
```
To remove the image:
```
docker image rm <name_image>
```

## Run docker image with volume

Once the docker image has been created, you can launch the container anywhere on your terminal with:
```
docker run --rm -v <absolute_path_folder_data>:/borea_tools/data <name_image> <tool.py and param>
```
`-v <absolute_path_folder_data>:/borea_tools/data` specifies the absolute path of the folder containing the data to be processed and stores it in the data folder which is in the borea_tools workdir, which means that for data parameter passing, you just need to put `/data/<name_data>` to retrieve it.  
`<name_image>` is the name of docker image you want to run.  
`<tool.py and param>` is the tools you want to use e.g. `opk_to_opk.py -h`.  
e.g.
```
docker run --rm -v docker run --rm -v /home/ACornu/Documents/Borea/dataset:/borea_tools/data boreai opk_to_opk.py -r /data/23FD1305_alt_test.OPK -i NXYZOPKC -f 2 -e 2154 -y /data/fr_ign_RAF20.tif -c /data/Camera1.txt -m /data/MNT_France_25m_h_crop.tif --fm height -n Test -w /data/ -o NXYHPOKC -ou radian -oa False
```

## Tools

Some tools are already implemented in the docker:
* Conversion OPK to OPK: `opk_to_opk.py -h` [doc](./borea_tools/docs_tools/README_opk_to_opk.md) (OPK = Omega Phi Kappa)
* Control OPK file: `opk_control.py -h` [doc](./borea_tools/docs_tools/README_opk_control.md)
* Conversion OPK to RPC: `opk_to_rpc.py -h` [doc](./borea_tools/docs_tools/README_opk_to_rpc.md)
* Conversion OPK to Conl: `opk_to_conl.py -h` [doc](./borea_tools/docs_tools/README_opk_to_conl.md) (Conl = light conical file, IGN France format)
* Transforms coordinates terrain from image: `pt_image_to_world.py -h` [doc](./borea_tools/docs_tools/README_pt_image_to_world.md)
* Transforms coordinates image from terrain: `pt_world_to_image.py -h` [doc](./borea_tools/docs_tools/README_pt_world_to_image.md)
* Transforms coordinates file terrain from image: `ptfile_image_to_world.py -h` [doc](./borea_tools/docs_tools/README_ptfile_image_to_world.md)
* Transforms coordinates file image from terrain: `ptfile_world_to_image.py -h` [doc](./borea_tools/docs_tools/README_ptfile_world_to_image.md)
* Calculates opk by space resection: `spaceresection_opk.py -h` [doc](./borea_tools/docs_tools/README_spaceresection_opk.md)


![logo ign](docs/image/logo_ign.png) ![logo fr](docs/image/Republique_Francaise_Logo.png)