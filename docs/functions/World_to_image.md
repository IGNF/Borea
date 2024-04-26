# Formula documentation for the function world_to_image

Function to transform the image coordinates of a point, starting from a terrain point.  
It is built into the WorldImageShot class [borea/transform_world_image/transform_shot/world_image_shot.py](../../borea/transform_world_image/transform_shot/world_image_shot.py).  
Tools where transformation is used are : **opk_control.py**, **pt_world_to_image.py** and **ptfile_world_to_image.py**.

## Formula

### Conversion of terrain data into a Euclidean reference frame (local tangent)

* Convert the z of the data to the same unit (altitude, height), de-correct the z of the linear alteration acquisition if corrected

* Conversion from cartographic -> image to Euclidean -> image rotation matrix. With projeucli's mat_to_mat_eucli function.

### From Euclidean frame of reference to image frame of reference

* Calculation of the vector between the acquisition position and the terrain point and change of reference frame.
```math
p_{bundle} = \begin{pmatrix}x_{bundle}\\y_{bundle}\\z_{bundle}\end{pmatrix} = rot_{eucli} * (p_{eucli} – pos_{eucli})
```

* Change from 3d to 2d point in the image frame.
```math
x_{shot} = x_{bundle} * focal / z_{bundle}
```
```math
y_{shot} = y_{bundle} * focal / z_{bundle}
```
```math
z_{shot} = z_{bundle}
```

* Application of systematizations, if any (distortion correction function).
```math
x_{shot}, y_{shot}, z_{shot} = f_{sys}(x_{shot}, y_{shot}, z_{shot})
```
if there is no distortion or it has already been corrected f_sys() is an identity function.

* From vector image to image point.
```math
x_{col} = ppax + x_{shot}
```
```math
y_{line} = ppay + y_{shot}
```

* Returns $x_{col}$ and $y_{line}$ in an array (2,).

Link to see examples : [./examples/eg_world_to_image](../../examples/eg_world_to_image.py)

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)