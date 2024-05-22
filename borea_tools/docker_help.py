"""
Print console for docker container, if  0 args.
"""

print("""
      Warning: no arguments given for tools.
      Args tools (with -h to see args of tools):
      - opk_to_opk.py: to convert OPK file to an other OPK file.
      - opk_control.py: to control OPK file with GCP.
      - opk_to_rpc.py: to convert OPK file to RPC (QGIS format).
      - opk_to_conl.py: to convert OPK file to light conical format for GEOVIEW IGN.
      - pt_image_to_world.py: to convert one image coordinate in terrain coordinate.
      - pt_world_to_image.py: to convert one terrain coordinate in image coordinate.
      - ptfile_image_to_world.py: to convert file of image coordinates in terrain coordinates.
      - ptfile_world_to_image.py: to convert file of terrain coordinates in image coordinates.
      - spaceresection_opk.py: to calcule OPK by spaceresection with
        coordinates points terrain and image.""")
