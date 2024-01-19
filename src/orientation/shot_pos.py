"""
Module for recalculate shooting position 
"""
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from scipy.spatial.transform import Rotation


# pylint: disable-next=too-many-locals
def shooting_position(shot: Shot, cam: Camera, projeucli: EuclideanProj,
                      add_pixel: tuple = (0, 0)) -> Shot:
    """
    Recalculates the shot's 6 external orientation parameters, 
    the 3 angles omega, phi, kappa and its position x, y, z.

    Args:
        shot (Shot): Shot to recalculte externa parameters.
        cam (Camera): Camera of the shot.
        projeucli (EuclideanProj): Euclidiean projection system of the worksite.
        add_pixel (tuble): Pixel to be added to change marker 
    """
    # Change of data system
    mat_eucli = projeucli.mat_to_mat_eucli(shot.pos_shot[0], shot.pos_shot[1], shot.mat_rot)
    pos_eucli = projeucli.world_to_euclidean(shot.pos_shot[0],shot.pos_shot[1],shot.pos_shot[2])

    # Initialisation of 20 points for shooting position
    c_obs = np.random.randint(cam.width, size=20)
    l_obs = np.random.randint(cam.height, size=20)
    z_world = np.random.randint(500, size=20)
    x_world, y_world, _ = shot.image_to_world(c_obs, l_obs, cam, projeucli, z_world)
    x_eucli, y_eucli, z_eucli = projeucli.world_to_euclidean(x_world, y_world, z_world)
    c_obs, l_obs = c_obs + add_pixel[0], l_obs + add_pixel[1]

    shot_adjust = Shot(shot.name_shot, shot.pos_shot, shot.ori_shot, shot.name_cam)

    bool_iter = True
    count_iter = 0
    # while bool_iter:
    count_iter += 1

    mat_a = mat_a_11_param(x_eucli, y_eucli, z_eucli, c_obs, l_obs)
    col_c, line_c = shot_adjust.world_to_image(x_world, y_world, z_world, cam, projeucli)
    v_res = np.concatenate(((c_obs - col_c).reshape((20,1)),
                            (l_obs - line_c).reshape((20,1))))
    dx = np.squeeze(np.linalg.lstsq(mat_a, v_res, rcond=None)[0])
    print(dx)
    dpos_eucli, dmat_eucli = conv_11_to_6_param(dx, cam)

    # mat_Y = np.concatenate((x_col.reshape((20,1)), y_lig.reshape((20,1))))
    # mat_X = np.matrix(mat_a).I @ mat_Y
    return shot_adjust


def mat_a_11_param(x: np, y: np, z: np, c: np, l: np) -> np:
    """
    Setting up the A matrix to solve the system.

    Args:
        x (np.array): Coordinate x euclidean
        y (np.array): Coordinate y euclidean
        z (np.array): Coordinate z euclidean
        c (np.array): Coordinate c image (column)
        l (np.array): Coordinate l image (line)
    """
    t = x.shape[0]
    t2 = t*2
    mat_a = np.zeros((t2, 11))
    mat_a[0:t,0] = x
    mat_a[0:t,1] = y
    mat_a[0:t,2] = z
    mat_a[0:t,3] = 1
    mat_a[t:t2,4] = x
    mat_a[t:t2,5] = y
    mat_a[t:t2,6] = z
    mat_a[t:t2,7] = 1
    mat_a[0:t,8] = -x * c
    mat_a[0:t,9] = -y * c
    mat_a[0:t,10] = -z * c
    mat_a[t:t2,8] = -x * l
    mat_a[t:t2,9] = -y * l
    mat_a[t:t2,10] = -z * l
    return mat_a


def conv_11_to_6_param(param: np, cam: Camera) -> tuple:
    """
    Convert 11 parameters to 6 parameters of image function

    Args:
        param (np): 11 parameters
        cam (Camera): Camera of the shot

    Returns:
        tuple: position and rotation matrix
    """
    mat_a = param[0:3]
    mat_b = param[4:7]
    mat_c = param[8:11]
    num_a4 = param[3]
    num_b4 = param[7]
    mat_d = np.vstack((mat_a, mat_b, mat_c))
    mat_e = np.array([-num_a4, -num_b4, -1])
    pos_eucli = np.linalg.inv(mat_d) @ mat_e
    norm_c = np.sqrt(mat_c @ mat_c)
    mat_l1 = (mat_a - cam.ppax * mat_c) / (cam.focal * norm_c)
    mat_l2 = (mat_b - cam.ppay * mat_c) / (cam.focal * norm_c)
    mat_l3 = - mat_c / norm_c
    mat_rot_eucli = np.vstack((mat_l1, mat_l2, mat_l3))
    return pos_eucli, mat_rot_eucli
