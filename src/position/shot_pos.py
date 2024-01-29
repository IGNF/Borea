"""
Module for recalculate shooting position
"""
import numpy as np
from scipy.spatial.transform import Rotation
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj


# pylint: disable-next=too-many-locals
def space_resection(shot: Shot, cam: Camera, projeucli: EuclideanProj,
                    add_pixel: tuple = (0, 0)) -> Shot:
    """
    Recalculates the shot's 6 external orientation parameters,
    the 3 angles omega, phi, kappa and its position x, y, z.

    Args:
        shot (Shot): Shot to recalculte externa parameters.
        cam (Camera): Camera of the shot.
        projeucli (EuclideanProj): Euclidiean projection system of the worksite.
        add_pixel (tuble): Pixel to be added to change marker.

    Returns:
        Shot: Adjusted shot
    """
    # Initialization of 20 points for shooting position
    c_obs, l_obs, z_world = seed_20_point(cam)

    # Calculate world position
    x_world, y_world, _ = shot.image_to_world(c_obs, l_obs, cam, projeucli, z_world)

    # Calculate euclidean position
    x_eucli, y_eucli, z_eucli = projeucli.world_to_euclidean(x_world, y_world, z_world)

    # Add factor
    c_obs += add_pixel[0]
    l_obs += add_pixel[1]

    # Initialization of adjusted shot
    shot_adjust = Shot(shot.name_shot, shot.pos_shot, shot.ori_shot, shot.name_cam)
    shot_adjust.set_param_eucli_shot(projeucli)

    bool_iter = True
    count_iter = 0
    while bool_iter:
        count_iter += 1

        # Creation of A
        mat_a = mat_obs_axia(x_eucli, y_eucli, z_eucli, shot_adjust, cam)

        # Calculate position column and line with new shot f(x0)
        c_f0, l_f0 = shot_adjust.world_to_image(x_world, y_world, z_world, cam, projeucli)

        # Calculate residual vector B
        v_res = np.c_[c_obs - c_f0, l_obs - l_f0].reshape(2 * len(x_eucli), 1)

        # Calculate dx = (A.T @ A)**-1 @ A.T @ B
        dx = np.squeeze(np.linalg.lstsq(mat_a, v_res, rcond=None)[0])

        # Calculate new x = x0 + dx for position and rotation matrix
        new_pos_eucli = np.array([shot_adjust.pos_shot[0] + dx[0],
                                  shot_adjust.pos_shot[1] + dx[1],
                                  shot_adjust.pos_shot[2] + dx[2]])
        new_mat_eucli = shot_adjust.mat_rot_eucli @ Rotation.from_rotvec(dx[3:]).as_matrix()

        # Creation of new shot with new parameter
        imc_new_adjust = Shot.from_param_euclidean(shot_adjust.name_shot, new_pos_eucli,
                                                   new_mat_eucli, shot_adjust.name_cam, projeucli)

        # Look difference to know if you want to stop the calculation
        diff_coord = np.array([imc_new_adjust.pos_shot]) - np.array([shot_adjust.pos_shot])
        diff_opk = np.array([imc_new_adjust.ori_shot]) - np.array([shot_adjust.ori_shot])

        if (np.all(diff_coord < 10 ** -3) and np.all(diff_opk < 10 ** -6)) or count_iter > 10:
            bool_iter = False

        # Replace adjusted place
        shot_adjust = imc_new_adjust

    return shot_adjust


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
                        z_eucli - imc_adjust.pos_shot_eucli[2]])  # vect_a = M-S
    vect_u = imc_adjust.mat_rot_eucli @ vect_a  # U = RA

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

    mat_a[:, 3:] *= np.einsum('lij, ljk->lik', (mat_v @ imc_adjust.mat_rot_eucli).reshape(-1, 2, 3),
                              # pylint: disable-next=too-many-function-args
                              a_axiator.reshape(-1, 3, 3)).reshape(-1, 3)

    return mat_a


def seed_20_point(cam: Camera) -> tuple:
    """
    Positioning of 20 points on an image by percentage position on width and height.
    The z-world position is given by fixed values.

    Args:
        cam (Camera): Camera of the shot.

    Returns:
        np.array: Tuple of 3 elements (position column obs, position line obs, z world).
    """
    pourcent_x = np.array([6.25, 12.5, 18.75, 25, 31.25, 37.5, 37.5, 43.75, 50, 56.25,
                           62.5, 62.5, 68.75, 68.75, 75, 81.25, 87.5, 87.5, 93.75, 93.75]) / 100
    pourcent_y = np.array([80, 20, 60, 90, 30, 10, 50, 70, 20, 40,
                           60, 90, 20, 80, 50, 20, 10, 70, 40, 90]) / 100
    z_obs = np.array([200, 320, 250, 240, 330, 335, 340, 330, 350, 360,
                      360, 350, 370, 355, 380, 400, 450, 400, 500, 300])
    c_obs = pourcent_x * cam.width
    l_obs = pourcent_y * cam.height

    return np.array(c_obs), np.array(l_obs), z_obs
