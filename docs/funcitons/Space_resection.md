# Documentation for the function space_resection in src/orientation/shot_pos

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
Function to give the position of 20 points in the image at a fixed world height. The positions of the points are fixed and set by percentages for any image size. They will be the `l_obs` observation data.  
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

* Initialization of a new acquisition that will be modified, represents `x0`
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

* Setting up the `mat_A` matrix
```
mat_a = mat_obs_axia(x_eucli, y_eucli, z_eucli, shot_adjust, cam)
```
The matrix `mat_A` depends on the function used and the number of data items. It is defined as `df/dx|x0`, each column representing a derivative of `f(x)` with respect to a parameter of x0, and the number of rows the number of data.
The image formula used is: `m = F - (K.T @ F @ U) / (K.T @ U)`  
with:
* `F` the focal
* `A = M - S`
* `U = R @ A`
* `K` the unit vector `[0,0,1]`
* `M` the vector `[X, Y, Z]` of the Euclidean position of the terrain point
* `S` is the shot's position in the Euclidean reference frame
* `R` the rotation matrix in the Euclidean reference frame
* `m` the vector `[x, y]`

`x0` is `X, Y, Z` the shot position and `oX, oY, oZ` which defines its rotation matrix. We take the definition of `R = e^(omega*theta)` defined by a vector `omega = [X, Y, Z]` and an angle `theta = o`.  
The derivative of the function is therefore equal to :  
`dm = (V/u3) @ dF + (p/u3**2) @ V @ R @ (dS-dM) + (p/u3**2) @ V @ R @ axia_A @ dO`  
with `V = [[u3 0 -u1],[0 u3 -u2]]`, `U = [u1 u2 u3]` and `axia_A` is the axiator of the matrix `A`.
```
    mat_A = [ dfx1/dX  dfx1/dY  dfx1/dZ  dfx1/doX  dfx1/d0Y  dfx1/doZ ]
            [ dfx2/dX  dfx2/dY  dfx2/dZ  dfx2/doX  dfx2/d0Y  dfx2/doZ ]
            [   ...      ...      ...      ...        ...       ...   ]
            [ dfxn/dX  dfxn/dY  dfxn/dZ  dfxn/doX  dfxn/d0Y  dfxn/doZ ]
            [ dfy1/dX  dfy1/dY  dfy1/dZ  dfy1/doX  dfy1/d0Y  dfy1/doZ ]
            [ dfy2/dX  dfy2/dY  dfy2/dZ  dfy2/doX  dfy2/d0Y  dfy2/doZ ]
            [   ...      ...      ...      ...        ...       ...   ]
            [ dfyn/dX  dfyn/dY  dfyn/dZ  dfyn/doX  dfyn/d0Y  dfyn/doZ ]
```
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

* Setting up calculated data `f(x0)`
```
c_f0, l_f0 = shot_adjust.world_to_image(x_world, y_world, z_world, cam, projeucli)
```

* Setting the residual vector `l_obs - f(x0)`
```
v_res = np.c_[c_obs - c_f0, l_obs - l_f0].reshape(2 * len(x_eucli), 1)
```

* Vector calculation `dx = (mat_A.T @ mat_A)^(-1) @ mat_A.T @ B`
```
dx = np.squeeze(np.linalg.lstsq(mat_a, v_res, rcond=None)[0])
```

* Calculation of new parameter `x = x0 + dx`
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

Example for one shot:
```
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from src.geodesy.proj_engine import ProjEngine
from src.orientation.shot_pos import space_resection

# Create Shot
shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")

# Create Camera and add dimension of image
cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
cam.add_dim_image(26460.00, 17004.00)

# Create projection of worksite
proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
projeucli = EuclideanProj(814975.925, 6283986.148, proj)

# Setup euclidean parameter of shot
shot.set_param_eucli_shot(projeucli)

# Recalculate 6 externa parameter of the shot
adjusted _shot= space_resection(shot, cam, projeucli)
```

Example for a worksite:
```
import numpy as np
from src.datastruct.worksite import Worksite

# Create worksite
work = Worksite("Test")

# Add 2 shots
work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")

# Setup projection of the worksite
work.set_proj("EPSG:2154", "test/data/proj.json", "./test/data/")

# Add camera and dimension of image
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
work.cameras['cam_test'].add_dim_image(26460.00, 17004.00)

# Recalculate 6 externa parameters of all shots
work.shootings_position()
```

Example with file:
```
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp

path_opk = "Worksite_FR_2024.OPK"
path_camera = ["Camera.txt"]
path_copoints = ["liaison.mes", "terrain.mes"]
path_gcps = ["GCP.app"]
writer = "opk"
pathreturn = "tmp/"

# Readind data and create objet worksite
work = reader_orientation(path_opk, 1)

# Add a projection to the worksite
work.set_proj("EPSG:2154", "projection_epsg.json", "./data_geotiff/")

# Reading camera file
read_camera(path_camera, work)

# Reading connecting point
read_copoints(path_copoints, work)

# Reading GCP
read_gcp(path_gcps, work)

# Recalculate 6 externa parameters of all shots
work.shootings_position()
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)