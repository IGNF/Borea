"""
Module for recalculate shooting position
"""
import numpy as np
from scipy.spatial.transform import Rotation
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from src.math.param_bundle import param_bundle_diff


class SpaceResection:
    """
    Recalculates the shot's 6 external orientation parameters,
    the 3 angles omega, phi, kappa and its position x, y, z.

    Args:
        shot (Shot): Shot to recalculte externa parameters.
        cam (Camera): Camera of the shot.
        type_z_data (str): z's type of data, "height" or "altitude".
        type_z_shot (str): z's type of shot, "height" or "altitude".
    """
    def __init__(self, shot: Shot, cam: Camera, type_z_data: str, type_z_shot: str) -> None:
        self.shot = shot
        self.cam = cam
        self.type_z_data = type_z_data
        self.type_z_shot = type_z_shot

    def space_resection(self, add_pixel: tuple = (0, 0)) -> Shot:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.

        Args:
            add_pixel (tuble): Pixel to be added to change marker.

        Returns:
            Shot: Adjusted shot.
        """
        # Initialization of 20 points for shooting position
        obs, z_world = self.seed_20_point()

        # Calculate world position
        x_world, y_world, _ = ImageWorldShot(self.shot,
                                             self.cam).image_z_to_world(obs,
                                                                        self.type_z_shot, z_world)

        # Calculate euclidean position
        pt_world = np.array([x_world, y_world, z_world])
        pt_eucli = self.shot.projeucli.world_to_eucli(pt_world)

        # Add factor
        obs[0] += add_pixel[0]
        obs[1] += add_pixel[1]

        # Initialization of adjusted shot
        shot_adjust = Shot(self.shot.name_shot, self.shot.pos_shot, self.shot.ori_shot,
                           self.shot.name_cam, self.shot.unit_angle, self.shot.linear_alteration)
        shot_adjust.set_param_eucli_shot(self.shot.approxeucli)
        shot_adjust.set_z_nadir(self.shot.z_nadir)

        # Least-square methode
        shot_adjust = self.least_square_shot(shot_adjust, obs, pt_eucli, pt_world)

        shot_adjust.co_points = self.shot.co_points
        shot_adjust.ground_img_pts = self.shot.ground_img_pts
        shot_adjust.gcps = self.shot.gcps

        return shot_adjust

    def least_square_shot(self, shot_adjust: Shot, obs: np.ndarray,
                          pt_eucli: np.ndarray, pt_world: np.ndarray) -> Shot:
        """
        Least-square methode to calcule the shot's 6 external orientation parameters.

        Args:
            shot_adjust (Shot): The shot to adjust.
            obs (np.array): Observation of point in image [c_obs, l_obs].
            pt_eucli (np.array): Observation of world point in eucidean system [X, Y, Z].
            pt_world (np.array): Observation of world point [X, Y, Z].

        Returns:
            Shot: Adjusted shot.
        """
        bool_iter = True
        count_iter = 0
        while bool_iter:
            count_iter += 1

            # Calculate position column and line with new shot f(x0)
            f0 = WorldImageShot(shot_adjust, self.cam).world_to_image(pt_world,
                                                                      self.type_z_data,
                                                                      self.type_z_shot)

            # Calculate residual vector B
            v_res = np.c_[obs[0] - f0[0], obs[1] - f0[1]].reshape(2 * len(pt_eucli[0]), 1)

            # Creation of A with mat_obs_axia
            # Calculate dx = (A.T @ A)**-1 @ A.T @ B
            dx = np.squeeze(np.linalg.lstsq(self.mat_obs_axia(pt_eucli, shot_adjust),
                                            v_res, rcond=None)[0])

            # Calculate new x = x0 + dx for position and rotation matrix
            new_pos_eucli = np.array([shot_adjust.pos_shot[0] + dx[0],
                                      shot_adjust.pos_shot[1] + dx[1],
                                      shot_adjust.pos_shot[2] + dx[2]])
            new_mat_eucli = shot_adjust.mat_rot_eucli @ Rotation.from_rotvec(dx[3:]).as_matrix()

            # Creation of new shot with new parameter
            imc_new_adjust = Shot.from_param_euclidean(shot_adjust.name_shot, new_pos_eucli,
                                                       new_mat_eucli, shot_adjust.name_cam,
                                                       shot_adjust.unit_angle,
                                                       shot_adjust.linear_alteration,
                                                       shot_adjust.approxeucli)
            imc_new_adjust.set_z_nadir(self.shot.z_nadir)

            # Look difference to know if you want to stop the calculation
            diff_coord = np.array([imc_new_adjust.pos_shot]) - np.array([shot_adjust.pos_shot])
            diff_opk = np.array([imc_new_adjust.ori_shot]) - np.array([shot_adjust.ori_shot])

            if (np.all(diff_coord < 10 ** -3) and np.all(diff_opk < 10 ** -6)) or count_iter > 10:
                bool_iter = False

            # Replace adjusted place
            shot_adjust = imc_new_adjust

        return shot_adjust

    def mat_obs_axia(self, pt_eucli: np.ndarray, imc_adjust: Shot) -> np.ndarray:
        """
        Setting up the mat_a matrix to solve the system by axiator.

        Args:
            pt_eucli (np.array): Coordinate [X, Y, Z] euclidean.
            imc_adjust (Shot): adjusted shot.

        Returns:
            np.array: Matrix A.
        """
        vect_a, vect_u, mat_v = param_bundle_diff(imc_adjust, pt_eucli)

        # Axiator of vect_a
        a_axiator = np.zeros((3 * len(vect_a[0]), 3))
        a_axiator[0::3, 1] = -vect_a[2]
        a_axiator[0::3, 2] = vect_a[1]
        a_axiator[1::3, 0] = vect_a[2]
        a_axiator[1::3, 2] = -vect_a[0]
        a_axiator[2::3, 0] = -vect_a[1]
        a_axiator[2::3, 1] = vect_a[0]

        mat_a = -np.tile(np.repeat(self.cam.focal / vect_u[2] ** 2, 2), (6, 1)).T
        mat_a[:, :3] *= (mat_v @ imc_adjust.mat_rot_eucli)

        mat_a[:, 3:] *= np.einsum('lij, ljk->lik',
                                  (mat_v @ imc_adjust.mat_rot_eucli).reshape(-1, 2, 3),
                                  # pylint: disable-next=too-many-function-args
                                  a_axiator.reshape(-1, 3, 3)).reshape(-1, 3)

        return mat_a

    def seed_20_point(self) -> tuple:
        """
        Positioning of 20 points on an image by percentage position on width and height.
        The z-world position is given by fixed values.

        Returns:
            np.array: Tuple of 3 elements (position column obs, position line obs, z world).
        """
        pourcent_x = np.array([6.25, 12.5, 18.75, 25, 31.25, 37.5, 37.5, 43.75, 50, 56.25,
                               62.5, 62.5, 68.75, 68.75, 75, 81.25, 87.5, 87.5, 93.75, 93.75]) / 100
        pourcent_y = np.array([80, 20, 60, 90, 30, 10, 50, 70, 20, 40,
                               60, 90, 20, 80, 50, 20, 10, 70, 40, 90]) / 100
        z_obs = np.array([200, 320, 250, 240, 330, 335, 340, 330, 350, 360,
                          360, 350, 370, 355, 380, 400, 450, 400, 500, 300])
        c_obs = pourcent_x * self.cam.width
        l_obs = pourcent_y * self.cam.height

        return np.array([c_obs, l_obs]), z_obs
