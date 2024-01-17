# Documentation for the function world_to_image in shot

Function for calculating the image coordinates of a point, starting from a terrain point.
It is built into the shot object to calculate the coordinates of the point in the desired acquisition.

## Parameters

It takes as parameters :
    1. point: a point in numpy format np.array([x, y, z]).
    2. cam: a Camera object.
    3. projeucli: a EuclideanProj object.

The Camera object is the camera used for acquisition, defined by a name, its ppax, ppay and focal length.

The EuclidieanProj object, defined by two coordinates x and y, which are the barycentre of the building site, and a ProjEngine object.

The ProjEngine object is defined by a string giving the ESPG code of the site's map projection, e.g. "EPSG:2154", followed by a dictionary found in src.data.projection_list.json, which groups together 3 important tags:
 * "geoc" returns the EPSG code of the geocentric projection on site.
 * "geog" returns the EPSG code of the geographic projection on the building site.
 * "geoid" returns a list of GeoTIFF names at site level.

These GeoTIFFs represent the geoid grid on the site. They can be found on the PROJ-data github (https://github.com/OSGeo/PROJ-data/tree/master ) and will be used by pyproj to calculate the acquisition altitude (so as not to take into account corrections already made to the acquisition coordinates in the original data). For it to be taken into account, it must be added to a proj folder. If you're not using an environment, the path is usr/share/proj; if you are using an environment, the path is env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.

## Calculation step

### Conversion of terrain data into a Euclidean reference frame (local tangent)

* Recovery of the acquisition altitude (z_alti) without alteration by pyproj (thanks to GeoTIFF).

* Convert terrain data into Euclidean reference frame, point [x, y, z] and acquisition position [x_pos, y_pos, z_alti], replacing z_pos with z_alti. With projeucli's world_to_eucliean() function.

* Conversion from cartographic -> image to Euclidean -> image rotation matrix. With projeucli's mat_to_mat_eucli function.

### From Euclidean frame of reference to image frame of reference

* Calculation of the vector between the acquisition position and the terrain point and change of reference frame.
```
p_bundle = mat_eucli @ (p_eucli – pos_eucli)
```

* Change from 3d to 2d point in the image frame.
```
x_shot = p_bundle[0] * cam.focal / p_bundle[2]
y_shot = p_bundle[1] * cam.focal / p_bundle[2]
z_shot = p_bundle[2]
```

* Application of systematizations, if any (distortion correction function).
```
x_shot, y_shot, z_shot = self.f_sys(x_shot, y_shot, z_shot)
```
if there is no distortion or it has already been corrected f_sys() is an identity function.

* From vector to image point.
```
x_col = cam.ppax + x_shot
y_lig = cam.ppay + y_shot
```

* Returns x_col and y_lig in an array (2,).

![logo ign](../logo/IGN_logo_2012.svg =50x) ![logo fr](../logo/Republique_Francaise_Logo.png =50x)