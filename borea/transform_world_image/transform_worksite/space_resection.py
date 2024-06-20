"""
Module for recalculate shooting position
"""
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
from borea.utils.miscellaneous.miscellaneous import angle_degree_2vect, min_max_pt, normalize
from borea.worksite.worksite import Worksite
from borea.datastruct.camera import Camera
from borea.datastruct.shot import Shot
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.image_world_intersection import WorldIntersection  # noqa: E501
from borea.utils.miscellaneous.param_bundle import set_param_bundle_diff


class SpaceResection:
    """
    Recalculates the shot's 6 external orientation parameters,
    the 3 angles omega, phi, kappa and its position x, y, z.

    Args:
        work (Woksite): Worksite to make space resection
    """
    def __init__(self, work: Worksite) -> None:
        self.work = work

    def space_resection_to_worksite(self, pt2d: pd.DataFrame, pt3d: pd.DataFrame,
                                    pinit: dict) -> None:
        """
        Calculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.
        For all shot with a variation pixel.

        Args:
            pt2d (pd.Dataframe): Table of image coordinate point with image.
            pt3d (pd.Dataframe): Table of ground coordinate point.
            pinit (dict): Dictionnary with 3d coordinate for initialization "coor_init".
        """
        for name_shot, group in pt2d.groupby("id_shot"):
            if group.shape[0] < 3:
                print(f"Shot {name_shot} has fewer than three points,"
                      " so it cannot calculate its position and orientation.")
                continue

            dfm = group.merge(pt3d, how="inner", on="id_pt")
            obs_img = np.array([dfm["column"].to_numpy(), dfm["line"].to_numpy()])
            obs_world = np.array([dfm["x"].to_numpy(), dfm["y"].to_numpy(), dfm["z"].to_numpy()])

            pinit["kappa"] = self.init_kappa(dfm)
            self.work.shots[name_shot] = self.space_resection_shot(name_shot, obs_img,
                                                                   obs_world, pinit)
        self.work.set_param_shot(self.work.approxeucli)

        if pt3d["type"].iloc[0]:
            type_pt = "gcp2d"
        else:
            type_pt = "co_points"
        self.work.set_point_image_dataframe(pt2d, type_pt)
        self.work.set_point_world_dataframe(pt3d, type_pt)

    def space_resection_on_worksite(self, add_pixel: tuple = (0, 0)) -> None:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.
        For all shot with a variation pixel.

        Args:
            add_pixel (tuple): Factor (column, line) added on observable point.
        """
        for key_shot, item_shot in self.work.shots.items():
            self.work.shots[key_shot] = self.space_resection_gap(item_shot, add_pixel)

    def space_resection_shot(self, name_shot: str, pt_img: np.ndarray,
                             pt_world: np.ndarray, pinit: dict) -> Shot:
        """
        Calculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.

        Args:
            name_shot (str): Name of shot to calculte externa parameters.
            pt_img (np.array): Coordonnees image of points.
            pt_world (np.array): Coordonnees world of points.
            pinit (dict): Dictionnary with 3d coordinate for initialization and kappa.

        Returns:
            Shot: Adjusted shot.
        """
        # Initialization of adjusted shot
        cam = self.work.cameras[list(self.work.cameras.keys())[0]]
        shot_adjust = Shot(name_shot, pinit["coor_init"], np.array([0, 0, pinit["kappa"]]),
                           cam.name_camera, "degree", False, "opk")
        shot_adjust.set_param_eucli_shot(self.work.approxeucli)
        z_nadir = ImageWorldShot(shot_adjust, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                                  self.work.type_z_shot,
                                                                  self.work.type_z_shot, False)[2]
        shot_adjust.set_z_nadir(z_nadir)

        # Calculate euclidean position
        pt_eucli = shot_adjust.projeucli.world_to_eucli(pt_world)

        # Least-square methode
        shot_adjust = self.least_square_shot(shot_adjust, pt_img, pt_eucli, pt_world)

        return shot_adjust

    def init_kappa(self, dfpt: pd.DataFrame) -> float:
        """
        Calculates a kappa angle for acquisition initialization.

        Args:
            dfpt (pd.DataFrame): Coordonnees of points in image and world.

        Returns:
            float: kappa angle.
        """
        pt_img = np.array([dfpt["column"].to_numpy(), dfpt["line"].to_numpy()])
        pt_mini, arg_min = min_max_pt(pt_img, "min")
        pt_maxi, arg_max = min_max_pt(pt_img, "max")
        pt_minw = dfpt.iloc[arg_min].get(["x", "y"]).to_numpy()
        pt_maxw = dfpt.iloc[arg_max].get(["x", "y"]).to_numpy()
        vect_i = pt_maxi - pt_mini
        vect_w = pt_maxw - pt_minw
        norm_vi = normalize(vect_i)[0]
        norm_vw = normalize(vect_w)[0]
        kappa = angle_degree_2vect(norm_vi, norm_vw)
        return np.floor(kappa)

    def space_resection_gap(self, shot: Shot, add_pixel: tuple = (0, 0)) -> Shot:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.

        Args:
            shot (Shot): Shot to recalculte externa parameters.
            add_pixel (tuble): Pixel to be added to change marker.

        Returns:
            Shot: Adjusted shot.
        """
        # Initialization observation point
        obs, pt_world = self.take_obs(shot)

        # Calculate euclidean position
        pt_eucli = shot.projeucli.world_to_eucli(pt_world)

        # Add factor
        obs[0] += add_pixel[0]
        obs[1] += add_pixel[1]

        # Initialization of adjusted shot
        shot_adjust = Shot(shot.name_shot, shot.pos_shot, shot.ori_shot,
                           shot.name_cam, shot.unit_angle, shot.linear_alteration, shot.order_axe)
        shot_adjust.set_param_eucli_shot(shot.approxeucli)
        shot_adjust.set_z_nadir(shot.z_nadir)

        # Least-square methode
        shot_adjust = self.least_square_shot(shot_adjust, obs, pt_eucli, pt_world)

        shot_adjust.co_points = shot.co_points
        shot_adjust.gcp2d = shot.gcp2d
        shot_adjust.gcp3d = shot.gcp3d

        return shot_adjust

    def least_square_shot(self, shot_adjust: Shot, obs: np.ndarray,
                          pt_eucli: np.ndarray, pt_world: np.ndarray) -> Shot:
        """
        Least-square methode to calcule the shot's 6 external orientation parameters.

        Args:
            shot_adjust (Shot): The shot to adjust.
            obs (np.array): Observation of point in image [c_obs, l_obs].
            pt_eucli (np.array): Observation of world point in euclidean system [X, Y, Z].
            pt_world (np.array): Observation of world point [X, Y, Z].

        Returns:
            Shot: Adjusted shot.
        """
        bool_iter = True
        count_iter = 0
        while bool_iter:
            count_iter += 1

            dx = self.func_least_square(shot_adjust, obs, pt_eucli, pt_world)

            # Calculate new x = x0 + dx for position and rotation matrix
            new_pos_eucli = np.array([shot_adjust.pos_shot[0] + dx[0],
                                      shot_adjust.pos_shot[1] + dx[1],
                                      shot_adjust.pos_shot[2] + dx[2]])
            new_mat_eucli = shot_adjust.mat_rot_eucli @ R.from_rotvec(dx[3:]).as_matrix()

            # Creation of new shot with new parameter
            imc_new_adjust = Shot.from_param_euclidean(shot_adjust.name_shot, new_pos_eucli,
                                                       new_mat_eucli, shot_adjust.name_cam,
                                                       shot_adjust.unit_angle,
                                                       shot_adjust.linear_alteration,
                                                       shot_adjust.order_axe,
                                                       shot_adjust.approxeucli)
            imc_new_adjust.set_z_nadir(shot_adjust.z_nadir)

            # Look difference to know if you want to stop the calculation
            diff_coord = np.array([imc_new_adjust.pos_shot]) - np.array([shot_adjust.pos_shot])
            diff_opk = np.array([imc_new_adjust.ori_shot]) - np.array([shot_adjust.ori_shot])

            if (np.all(diff_coord < 10 ** -3) and np.all(diff_opk < 10 ** -6)) or count_iter > 100:
                # print(count_iter)
                bool_iter = False

            # Replace adjusted place
            shot_adjust = imc_new_adjust

        return shot_adjust

    def func_least_square(self, shot_adjust: Shot, obs: np.ndarray,
                          pt_eucli: np.ndarray, pt_world: np.ndarray) -> np.ndarray:
        """
        Calculate the least-squares equation dx = (A.T @ A)**-1 @ A.T @ B

        Args:
            shot_adjust (Shot): The shot to adjust.
            obs (np.array): Observation of point in image [c_obs, l_obs].
            pt_eucli (np.array): Observation of world point in euclidean system [X, Y, Z].
            pt_world (np.array): Observation of world point [X, Y, Z].

        Returns:
            np.array: dx.
        """
        cam = self.work.cameras[shot_adjust.name_cam]
        # Calculate position column and line with new shot f(x0)
        f0 = WorldImageShot(shot_adjust,
                            cam
                            ).world_to_image(pt_world,
                                             self.work.type_z_data,
                                             self.work.type_z_shot)

        # Calculate residual vector B
        v_res = np.c_[obs[0] - f0[0], obs[1] - f0[1]].reshape(2 * len(pt_eucli[0]))

        # Creation of A with mat_obs_axia
        # Calculate dx = (A.T @ A)**-1 @ A.T @ B
        return np.squeeze(np.linalg.lstsq(self.mat_obs_axia(pt_eucli, shot_adjust),
                                          v_res, rcond=None)[0])

    def mat_obs_axia(self, pt_eucli: np.ndarray, imc_adjust: Shot) -> np.ndarray:
        """
        Setting up the mat_a matrix to solve the system by axiator.

        Args:
            pt_eucli (np.array): Coordinate [X, Y, Z] euclidean.
            imc_adjust (Shot): adjusted shot.

        Returns:
            np.array: Matrix A.
        """
        vect_a, vect_u, mat_v = set_param_bundle_diff(imc_adjust, pt_eucli)

        # Axiator of vect_a
        a_axiator = np.zeros((3 * len(vect_a[0]), 3))
        a_axiator[0::3, 1] = -vect_a[2]
        a_axiator[0::3, 2] = vect_a[1]
        a_axiator[1::3, 0] = vect_a[2]
        a_axiator[1::3, 2] = -vect_a[0]
        a_axiator[2::3, 0] = -vect_a[1]
        a_axiator[2::3, 1] = vect_a[0]

        cam = self.work.cameras[imc_adjust.name_cam]
        mat_a = -np.tile(np.repeat(cam.focal / vect_u[2] ** 2, 2), (6, 1)).T
        mat_a[:, :3] *= (mat_v @ imc_adjust.mat_rot_eucli)

        mat_a[:, 3:] *= np.einsum('lij, ljk->lik',
                                  (mat_v @ imc_adjust.mat_rot_eucli).reshape(-1, 2, 3),
                                  # pylint: disable-next=too-many-function-args
                                  a_axiator.reshape(-1, 3, 3)).reshape(-1, 3)

        return mat_a

    def take_obs(self, shot: Shot) -> tuple:
        """
        Check co point on the shot to use in observation.
        If there aren't enough points, add 20 random observation points.

        Args:
            shot (Shot): The shot to adjust.

        Returns:
            tuple: np.array(obs_image), np.array(pt_world).
        """
        add_pt = True
        pt_world_random = 0
        if shot.co_points:
            if not self.work.co_pts_world:
                WorldIntersection(self.work).calculate_image_world_by_intersection("co_points")
            obs, pt_world = self.work.get_coor_pt_img_and_world(shot.name_shot, "co_points")
            if obs.shape[1] >= 7:
                add_pt = False

        if add_pt:
            cam = self.work.cameras[shot.name_cam]
            # Initialization of 20 points for shooting position
            obs_random, z_world = self.seed_20_point(cam)
            # Calculate world position
            x_world, y_world, _ = ImageWorldShot(shot,
                                                 cam
                                                 ).image_z_to_world(obs_random,
                                                                    self.work.type_z_shot,
                                                                    z_world)
            pt_world_random = np.array([x_world, y_world, z_world])

        if add_pt and shot.co_points:
            obs = np.concatenate((obs, obs_random), axis=1)
            pt_world[2] += 350  # 350 is the mean of z_obs in seed_20_point
            pt_world = np.concatenate((pt_world, pt_world_random), axis=1)
            add_pt = False

        if add_pt:
            obs = obs_random
            pt_world = pt_world_random

        return obs, pt_world

    def seed_20_point(self, cam: Camera) -> tuple:
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

        return np.array([c_obs, l_obs]), z_obs
