# Formula documentation for the function eucli_intersection_2p

Function to transform the Euclidean coordinates of a point, visible on two acquisitions. Function built in WorldIntersection in [src/transform_world_image/transform_worksite/image_world_intersection.py](../../src/transform_world_image/transform_worksite/image_world_intersection.py).  
Tools where transformation is used are : opk_control.py and ptfile_image_to_world.py with parameter -p "inter"

## Formula

### Data recovery
Recover point position in images
```math
p_{img1} = \begin{pmatrix}
c_{img1}\\
l_{img1}
\end{pmatrix}
```
```math
p_{img2} = \begin{pmatrix}
c_{img2}\\
l_{img2}
\end{pmatrix}
```
Recover camera for each image
```math
cam_1 = \begin{pmatrix}
ppa_{x1} & ppa_{y1} & focal_1
\end{pmatrix}
```
```math
cam_2 = \begin{pmatrix}
ppa_{x2} & ppa_{y2} & focal_2
\end{pmatrix}
```
**PPAx** and **PPAy** are the main points of image deformation in x and y directions

### Converting image data to Euclidean projection

* Conversion of acquisition positions in the Euclidean reference frame
```math
pos_{eucli1} = \begin{pmatrix}
x_{posEucli1}\\y_{posEucli1}\\z_{posEucli1}
\end{pmatrix} = 
f_{world\_to\_eucli}(x_{posShot1},y_{posShot1},z_{posShot1})
```
```math
pos_{eucli2} = \begin{pmatrix}
x_{posEucli2}\\y_{posEucli2}\\z_{posEucli2}
\end{pmatrix} = 
f_{world\_to\_eucli}(x_{posShot2},y_{posShot2},z_{posShot2})
```

* Calculates image-to-Euclidean reference frame change matrices for each shot (rot is the rotation matrix)
```math
rot_{eucli1} = 
f_{mat\_to\_mat\_eucli}(x_{posShot1},y_{posShot1},rot_{shot1})
```
```math
rot_{eucli2} = 
f_{mat\_to\_mat\_eucli}(x_{posShot2},y_{posShot2},rot_{shot2})
```

### Euclidean position calculation

* Base calculation
```math
base = pos_{eucli1} - pos_{eucli2}
```

* Calculates the vectors of each beam by acquisition
```math
vect_1 = rot_{eucli1} * \begin{pmatrix}
c_{img1} - ppa_{x1}\\l_{img1} - ppa_{y1}\\-focal_1
\end{pmatrix}
```
```math
vect_2 = rot_{eucli2} * \begin{pmatrix}
c_{img2} - ppa_{x2}\\l_{img2} - ppa_{y2}\\-focal_2
\end{pmatrix}
```

* Calculates products scalar product
```math
norme_{v1} = vect_1 * vect_1
```
```math
norme_{v2} = vect_2 * vect_2
```
```math
v_1v_2 = vect_1 * vect_2
```
```math
bv_1 = base * vect_1
```
```math
bv_2 = base * vect_2
```

* Calculates the position of the point on the beam
```math
p_{eucli1} = pos_{eucli1} + \frac{bv_2*v_1v_2 - bv_1*norme_{v1}}{v_1v_2^2 - norme_{v1}*norme_{v2}} * vect_1
```
```math
p_{eucli2} = pos_{eucli2} + \frac{bv_2*norme_{v1} - bv_1*v_1v_2}{v_1v_2^2 - norme_{v1}*norme_{v2}} * vect_2
```


* Return the average position between the two points
```math
p_{eucli} = 0.5 * (p_{eucli1} + p_{eucli2})
```
All that remains is to convert the Euclidean coordinates back into terrain coordinates.

Link to see examples : [./examples/eg_image_to_world](../../examples/eg_image_to_world.py)

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)