# Formula documentation for the function space_resection

Function to re/calculate the 6 external image parameters. 3 parameters for image position and 3 parameters for orientation angles omega, phi, kappa, per least square.  
It is built in the SpaceResection class [src/transform_world_image/transform_worksite/space_resection.py](../../src/transform_world_image/transform_worksite/space_resection.py).  
Tools where transformation is used are : **opk_by_space_resection.py**

## Functions

There are two main functions in this class.
* One for spatial bearing on images whose parameters are already known, where you can add a deviation to the image point position if you wish to offset an image. Function is [space_resection_on_worksite()](#Space-resection-on-worksite).
* The other allows you to calculate the 6 external parameters of an acquisition using the coordinates of points present on the image and in the field. Function is [space_resection_to_worksite()](#Space-resection-to-worksite).

## Space resection on worksite

### Data initialization, l_obs, x0

The first step is to check the number of connection points entered, and if there are fewer than 7, to add dummy points for calculation.

* Initialization of 20 points for shooting positions
```
c_obs, l_obs, z_world = seed_20_point(cam)
```
Function to give the position of 20 points in the image at a fixed world height. The positions of the points are fixed and set by percentages for any image size. They will be the $c_{obs}$ and $l_{obs}$ observation data.  
Distribution of the 20 points in the image with z given.
```
                               widht
        -------------------------------------------------- 0%
        |                 *                       * 450  | 10%
        |     *          335    *        *     *         | 20%
    h   |    320       *       350      370   400        | 30%
    e   |             330          *                 *   | 40%
    i   |                 *       360       *       500  | 50%
    g   |        *       340          *    380           | 60%
    h   |       250          *       360          * 400  | 70%
    t   |  *                330          * 355           | 80%
        | 200       * 240             * 350      300 *   | 90%
        -------------------------------------------------- 100%
        0%          25%         50%          75%          100%
```

* Calculates terrain position and Euclidean position
```
# Calculate world position
x_world, y_world, _ = shot.image_to_world(c_obs, l_obs, cam, projeucli, z_world)

# Calculate euclidean position
x_eucli, y_eucli, z_eucli = projeucli.world_to_euclidean(x_world, y_world, z_world)
```
The calculation is performed in a Euclidean reference frame (local tangent).

* Add factor
```
c_obs += add_pixel[0]
l_obs += add_pixel[1]
```
Enables data format conversion when different from 0

* Initialization of a new acquisition that will be modified, represents $x0$
```
shot_adjust = Shot(shot.name_shot, shot.pos_shot, shot.ori_shot, shot.name_cam)
shot_adjust.set_param_eucli_shot(projeucli)
```

## Space resection to worksite()

### Data initialization

Data initialization is the initialization of an acquisition that will be adjusted by the points.
Each shot is initiated with its name, the position given as input, the angles omega, phi = 0 and kappa, an approximate angle calculated with the points (to avoid a divergence of the least squares if the initial solution is too far from the final solution), the name of the camera given as input, then more optional parameters that can be modified afterwards, in angle in degree, no linear correction and an angle axis "opk" for the rotation matrix. `Shot(name_shot, pinit["coor_init"], np.array([0, 0, pinit["kappa"]]),cam.name_camera, "degree", False, "opk")`

The number of points in the image is set to a minimum of 3 for calculation. If there are fewer, the image in question will not be calculated, and a message to that effect will be displayed in the console.

## Function and least squares

### Colinearity equation
<p align="center"> <img src="../image/schema_repere.png"> </p>
<p align="center"><i> by Y.EGELS </i></p>

```math
M = \begin{pmatrix} X_M \\ Y_M \\ Z_M \end{pmatrix},~
S = \begin{pmatrix} X_S \\ Y_S \\ Z_S\end{pmatrix},~
F = \begin{pmatrix} x_c \\ y_c \\ p \end{pmatrix},~
m = \begin{pmatrix} x \\ y \\ 0 \end{pmatrix},~
K = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix},~
R~the~rotation~matrix
```


m is image coordinate of M. K the unit vector orthogonal to the shot.

$m \in shot \Leftrightarrow K^tm = 0$ hence $\lambda = \frac{-K^tF}{K^tR(M-S)}$  
Let's set $A = M-S$ and $U = RA$, we have $\lambda=\frac{-K^tF}{K^tU}$ hence $m = F - \frac{K^tFU}{K^tU}$ 

The image formula used is: $$m = F - (K^T F U) / (K^T U)$$ 

### Differential relationship between m and beam parameters

The above equation is non-linear, and to solve the systems corresponding to analytical photogrammetry, it needs to be linearized. The variables to be taken into account are F,M,S and R.  
$dm = dF - \frac{K^tdFU}{K^tU} - (\frac{K^tF}{K^tU} - \frac{K^tFUK^t}{(K^tU)²})dU $  
$dU = R(dM-dS)+dRA = r(dM-dS-\tilde{A}d\Theta) $  
On the other hand, $K^tF$ being a scalar, $K^tFU = UK^tF$ and $K^tdFU = UK^tdF$
We have: $dm = \frac{K^tU-UK^t}{(K^tU)²}(K^tUdF-K^tFR(dM-dS-\tilde{A}d\Theta))$  
Let's set 
```math
p = K^tF,~
U = \begin{pmatrix} u1 & u2 & u3 \end{pmatrix}~and~
V = \begin{pmatrix} u3 & 0 & -u1 \\ 0 & u3 & -u2 \end{pmatrix}
```  

which results in: $$dm = \frac{V}{u3} dF + (\frac{p}{u3²}) V R (dS-dM) + (\frac{p}{u3²}) V R \tilde{A}d\Theta$$

### Construction of the matrix A of least squares

The matrix $mat_A$ depends on the function used and the number of data items. It is defined as $\frac{df}{dx}|_{x0}$, each column representing a derivative of $f(x)$ with respect to a parameter of x0, and the number of rows the number of data.  
$x0$ is the 6 externals parameters of the shot: 
```math
position~S = \begin{pmatrix}X_S \\ Y_S \\ Z_S\end{pmatrix}~and~orientation~ \Theta = \begin{pmatrix}\omega \\ \phi \\ \kappa\end{pmatrix} 
```
so:
```math
mat_A = \begin{pmatrix}
\frac{dfx1}{dX_S} & \frac{dfx1}{dY_S} & \frac{dfx1}{dZ_S} & \frac{dfx1}{d\omega } & \frac{dfx1}{d\phi } & \frac{dfx1}{d\kappa } \\
\frac{dfx2}{dX_S} & \frac{dfx2}{dY_S} & \frac{dfx2}{dZ_S} & \frac{dfx2}{d\omega } & \frac{dfx2}{d\phi } & \frac{dfx2}{d\kappa } \\
  ...   &   ...   &   ...   &   ...    &    ...   &    ...  \\
\frac{dfxn}{dX_S} & \frac{dfxn}{dY_S} & \frac{dfxn}{dZ_S} & \frac{dfxn}{d\omega } & \frac{dfxn}{d\phi } & \frac{dfxn}{d\kappa } \\
\frac{dfy1}{dX_S} & \frac{dfy1}{dY_S} & \frac{dfy1}{dZ_S} & \frac{dfy1}{d\omega } & \frac{dfy1}{d\phi } & \frac{dfy1}{d\kappa } \\
\frac{dfy2}{dX_S} & \frac{dfy2}{dY_S} & \frac{dfy2}{dZ_S} & \frac{dfy2}{d\omega } & \frac{dfy2}{d\phi } & \frac{dfy2}{d\kappa } \\
  ...   &   ...   &   ...   &   ...    &    ...   &    ...  \\
\frac{dfyn}{dX_S} & \frac{dfyn}{dY_S} & \frac{dfyn}{dZ_S} & \frac{dfyn}{d\omega } & \frac{dfyn}{d\phi } & \frac{dfyn}{d\kappa }
\end{pmatrix}
```
There are as many lines in mat_a as there are number of points x2.  

## Example to use

This function is used in SpaceResection class the **space_resection_on_worksite()** function of the worksite class to loop over all the shots present on the worksite. e.g. link: [./examples/eg_space_resection.py](../../examples/eg_space_resection.py)

This function is used in SpaceResection class the **space_resection_to_worksite()** function of the worksite class to calculate 6 externals parameters of shot and implemente him in worksite. e.g. link: [./examples/eg_space_resection.py](../../examples/eg_space_resection.py)

![logo ign](../image/logo_ign.png) ![logo fr](../image/Republique_Francaise_Logo.png)