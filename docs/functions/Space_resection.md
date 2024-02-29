# Documentation for the function space_resection in src/transform_world_image/transform_shot/space_resection.py

Function to recalculate the 6 external image parameters. 3 parameters for image position and 3 parameters for orientation angles omega, phi, kappa, per least square.

It is built in the src.orientation.shot_pos.py module.

## Parameters

It takes in parameters :
1. shot : shot to recalculate 6 external parameters
2. cam: Camera for the shot
3. projeucli: Euclidean projection system of the site
4. add_pixel: Pixel to be added to the change maker

The Camera object is the camera used for acquisition, defined by a name, its ppax, ppay and focal length.

The EuclidieanProj object, defined by two coordinates x and y, which are the barycentre of the construction site, and a ProjEngine object.

The add_pixel object is a tuple of dimension 2, used to add a number of pixels in columns and rows. Used to convert certain photogrammetric data formats.

## Calculation step

### Data initialization, l_obs, x0

* Inatialization of 20 points for shooting positions
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

### While loop of least squares
```
bool_iter = True
count_iter = 0
while bool_iter:
    count_iter += 1
```

* Setting up the $mat_A$ matrix
```
mat_a = mat_obs_axia(x_eucli, y_eucli, z_eucli, shot_adjust, cam)
```
The matrix $mat_A$ depends on the function used and the number of data items. It is defined as $\frac{df}{dx}|_{x0}$, each column representing a derivative of $f(x)$ with respect to a parameter of x0, and the number of rows the number of data.
The image formula used is: $m = F - (K^T * F * U) / (K^T * U)$  
with:
* $F$ the focal
* $A = M - S$
* $U = R @ A$
* $K$ the unit vector $\left(\begin{array}{cc}0&0&1\end{array}\right)$
* $M$ the vector $\left(\begin{array}{cc}X&Y&Z\end{array}\right)$ of the Euclidean position of the terrain point
* $S$ is the shot's position in the Euclidean reference frame
* $R$ the rotation matrix in the Euclidean reference frame
* $m$ the vector $\left(\begin{array}{cc}x&y\end{array}\right)$

$x0$ is $X$, $Y$, $Z$ the shot position and $oX$, $oY$, $oZ$ which defines its rotation matrix. We take the definition of $R = e^(omega*theta)$ defined by a vector $omega = \left(\begin{array}{cc}X&Y&Z\end{array}\right)$ and an angle $theta = o$.  
The derivative of the function is therefore equal to :  
$dm = (V/u3) * dF + (\frac{p}{u3²}) * V * R * (dS-dM) + (\frac{p}{u3²}) * V * R * axia_A * dO$  
with $V = \left(\begin{array}{cc} u3 & 0 & -u1\\0 & u3 & -u2 \end{array}\right)$, $U = \left(\begin{array}{cc}u1&u2&u3\end{array}\right)$ and $axia_A$ is the axiator of the matrix $A$.
$$
mat_A = \left(\begin{array}{cc} 
\frac{dfx1}{dX} & \frac{dfx1}{dY} & \frac{dfx1}{dZ} & \frac{dfx1}{doX} & \frac{dfx1}{doY} & \frac{dfx1}{doZ}\\
\frac{dfx2}{dX} & \frac{dfx2}{dY} & \frac{dfx2}{dZ} & \frac{dfx2}{doX} & \frac{dfx2}{doY} & \frac{dfx2}{doZ}\\
  ...   &   ...   &   ...   &   ...    &    ...   &    ...  \\
\frac{dfxn}{dX} & \frac{dfxn}{dY} & \frac{dfxn}{dZ} & \frac{dfxn}{doX} & \frac{dfxn}{doY} & \frac{dfxn}{doZ}\\
\frac{dfy1}{dX} & \frac{dfy1}{dY} & \frac{dfy1}{dZ} & \frac{dfy1}{doX} & \frac{dfy1}{doY} & \frac{dfy1}{doZ}\\
\frac{dfy2}{dX} & \frac{dfy2}{dY} & \frac{dfy2}{dZ} & \frac{dfy2}{doX} & \frac{dfy2}{doY} & \frac{dfy2}{doZ}\\
  ...   &   ...   &   ...   &   ...    &    ...   &    ...  \\
\frac{dfyn}{dX} & \frac{dfyn}{dY} & \frac{dfyn}{dZ} & \frac{dfyn}{doX} & \frac{dfyn}{doY} & \frac{dfyn}{doZ}
\end{array}\right)
$$
There are as many lines in mat_a as there are points*2.  
This gives the function :

```
def mat_obs_axia(x_eucli: np.array, y_eucli: np.array, z_eucli: np.array,
                 imc_adjust: Shot, cam: Camera) -> np.array:
    """
    Setting up the mat_a matrix to solve the system by axiator.

    Args:
        x_eucli (np.array): Coordinate x euclidean.
        y_eucli (np.array): Coordinate y euclidean.
        z_eucli (np.array): Coordinate z euclidean.
        imc_adjust (Shot): adjusted shot.
        cam (Camera): Camera of shot.

    Returns:
        np.array: Matrix A.
    """
    vect_a = np.vstack([x_eucli - imc_adjust.pos_shot_eucli[0],
                        y_eucli - imc_adjust.pos_shot_eucli[1],
                        z_eucli - imc_adjust.pos_shot_eucli[2]])
    vect_u = imc_adjust.mat_rot_eucli @ vect_a

    # Axiator of vect_a
    a_axiator = np.zeros((3 * len(vect_a[0]), 3))
    a_axiator[0::3, 1] = -vect_a[2]
    a_axiator[0::3, 2] = vect_a[1]
    a_axiator[1::3, 0] = vect_a[2]
    a_axiator[1::3, 2] = -vect_a[0]
    a_axiator[2::3, 0] = -vect_a[1]
    a_axiator[2::3, 1] = vect_a[0]

    mat_v = np.zeros((2 * len(vect_u[0]), 3))
    mat_v[::2, 0] = vect_u[2]
    mat_v[::2, 2] = -vect_u[0]
    mat_v[1::2, 1] = vect_u[2]
    mat_v[1::2, 2] = -vect_u[1]

    mat_a = -np.tile(np.repeat(cam.focal / vect_u[2] ** 2, 2), (6, 1)).T
    mat_a[:, :3] *= (mat_v @ imc_adjust.mat_rot_eucli)

    mat_a[:, 3:] *= np.einsum('lij, ljk->lik',
                              (mat_v @ imc_adjust.mat_rot_eucli).reshape(-1, 2, 3),
                              a_axiator.reshape(-1, 3, 3)).reshape(-1, 3)

    return mat_a
```

* Setting up calculated data $f(x0)$
```
c_f0, l_f0 = shot_adjust.world_to_image(x_world, y_world, z_world, cam, projeucli)
```

* Setting the residual vector $l_{obs} - f(x0)$
```
v_res = np.c_[c_obs - c_f0, l_obs - l_f0].reshape(2 * len(x_eucli), 1)
```

* Vector calculation $dx = (mat_A^T * mat_A)^{-1} * mat_A^T * B$
```
dx = np.squeeze(np.linalg.lstsq(mat_a, v_res, rcond=None)[0])
```

* Calculation of new parameter $x = x0 + dx$
```
new_pos_eucli = np.array([shot_adjust.pos_shot[0] + dx[0],
                          shot_adjust.pos_shot[1] + dx[1],
                          shot_adjust.pos_shot[2] + dx[2]])
new_mat_eucli = shot_adjust.mat_rot_eucli @ Rotation.from_rotvec(dx[3:]).as_matrix()
```

* Creation of a new image with the newly adjusted data
```
imc_new_adjust = Shot.from_param_euclidean(shot_adjust.name_shot, 
                                           new_pos_eucli, 
                                           new_mat_eucli, 
                                           shot_adjust.name_cam,
                                           projeucli)
```

* Data comparison and replacement
```
diff_coord = np.array([imc_new_adjust.pos_shot]) - np.array([shot_adjust.pos_shot])
diff_opk = np.array([imc_new_adjust.ori_shot]) - np.array([shot_adjust.ori_shot])

if (np.all(diff_coord < 10 ** -3) and np.all(diff_opk < 10 ** -6)) or count_iter > 10:
    bool_iter = False

        
shot_adjust = imc_new_adjust
```

* Return adjusted shot

## Example to use

This function is used in the shootings_position() function of the worksite class to loop over all the shots present on the worksite.

Example:
```
import numpy as np
from src.datastruct.worksite import Worksite

# Create worksite
work = Worksite("Test")

# Add 2 shots
# Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration)
# unit_angle = "degree" or "radian".
# linear_alteration True if z shot is corrected by linear alteration.
work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","d")
work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","d")

# Setup projection of the worksite
# set_epsg(epsg, proj_json, folder_geoid)
# the geoid is mandatory if type_z_data and type_z_shot are different
work.set_proj("EPSG:2154", "test/data/proj.json", "./test/data/")

# Add camera information
# add_camera(name_cam, ppax, ppay, focal, width, height)
# ppax and ppay image center in pixel with distortion
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)

# Setup z_nadir of shot
work.set_z_nadir_shot()

# Recalculate 6 externa parameters of all shots
work.shootings_position(add_pixel=(0,0))
```


![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)