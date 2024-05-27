# QGIS and OTB

[QGIS](https://www.qgis.org/en/site/) is a Free and Open Source Geographic Information System (GIS) with many plugins for manipulating geographic data, such as aerial, satellite or drone images. What's more, this GIS is compatible with [Orfeo ToolBox (OTB)](https://www.orfeo-toolbox.org/), a free open-source library developed by the French CNES that enables GDAL-readable image manipulation. OTB can also be used with terminal commands or its Python API.

## Image oriented 🖼️

QGIS does not read OPK files for image orientation, but reads <name_img>_RPC.TXT files that are in the same directory as the images. The <name_img>_RPC.TXT files are gdal RPCs (Rational Polynomial Coefficient) that enable image orientation using coefficients in the **WGS84 epsg:4326 projection**.

The Borea command for writing image RPC files is [opk_to_rpc.py](../../borea_tools/docs_tools/README_opk_to_rpc.md).  
This allows you to have oriented images and perform calculations on them, such as homologous point searches with OTB's **HomologousPointsExtraction** tool.

## Limit

Please note that some QGIS tools won't work on .jp2 oriented images, so you'll need to export them to Geotiff before you can process them.