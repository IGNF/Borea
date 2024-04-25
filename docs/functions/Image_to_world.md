# Formula documentation for the function image_to_world

Function to transform a terrain coordinates of an image coordinates, starting from a given z.  
It is built into the ImageWorldShot class [src/transform_world_image/transform_shot/image_world_shot.py](../../src/transform_world_image/transform_shot/image_world_shot.py).  
Tools where transformation is used are : **opk_control.py**, **pt_image_to_world.py** and **ptfile_image_to_world.py**.

## Formula

* Creation of 3d vector in image frame minus perceptual center. Switches from a 2D image frame to a 3D image frame.
```math
x_{shot} = col - ppa_x
```
```math
y_{shot} = line - ppa_y
```
```math
z_{shot} = focal
```
 **PPAx** and **PPAy** are the main points of image deformation in x and y directions. **col** and **line** is the image coordinates and **focal** is the focal of the camera.
* Application of inverse systematizations if available (inverse distortion correction function).
```math
x_{shot}, y_{shot}, z_{shot} = f_{sys inv}(x_{shot}, y_{shot}, z_{shot})
```
if there is no distortion or it has already been corrected $f_{sys inv}()$ is an identity function.

* Passage through the beam frame.
```math
x_{bundle} = x_{shot} / focal * z_{shot}
```
```math
y_{bundle} = y_{shot} / focal * z_{shot}
```
```math
z_{bundle} = z_{shot}
```

* Transition to the Euclidean reference frame.
```math
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} = rot_{eucli}^T * 
\begin{pmatrix} 
x_{bundle}\\
y_{bundle}\\
z_{bundle}
\end{pmatrix}
```
With Shot.projeucli.mat_rot_euclidean_local() the rotation matrix of the Euclidean frame of reference set up from the site's barycentre.

* Converting the acquisition position to the Euclidean reference frame. With projeucli's world_to_eucliean() function. Warning: $z_{posShot}$ must be de-corrected for linear alteration and must be of the same unit as the others (altitude or height).

* Addition of local point acquisition.
```math
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} = 
\begin{pmatrix} 
x_{local}\\
y_{local}\\
z_{local}
\end{pmatrix} + 
\begin{pmatrix}
x_{posEucli}\\
y_{posEucli}\\
z_{posEucli}
\end{pmatrix}
```


* Create lambda to convert local point into Euclidean point.
```math
lamb = (z - z_{posEucli})/(z_{local} - z_{posEucli})
```
```math
x_{local} = x_{posEucli} + (x_{local} - x_{posEucli}) * lamb
```
```math
y_{local} = y_{posEucli} + (y_{local} - y_{posEucli}) * lamb
```

* Convert Euclidean point to terrain point, using proj's euclidean_to_world(x, y, z) function.

* Returns the point as an array (3,). However, the z coordinate is wrong, but with a DTM we can find the Z value with the X and Y position we've just calculated.

Link to see examples : [./examples/eg_image_to_world](../../examples/eg_image_to_world.py)

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)