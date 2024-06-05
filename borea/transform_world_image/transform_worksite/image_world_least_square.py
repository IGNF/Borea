"""
Class to calcule world coordinate by least square methode.
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from borea.worksite.worksite import Worksite
from borea.geodesy.local_euclidean_proj import LocalEuclideanProj
from borea.geodesy.approx_euclidean_proj import ApproxEuclideanProj
from borea.datastruct.dtm import Dtm
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from borea.utils.miscellaneous.sparse import invert_diag_sparse_matrix_3_3
from borea.utils.miscellaneous.param_bundle import set_param_bundle_diff


@dataclass
class WorldLeastSquare:
    """
    Class to calculate image coordinate to world coordinate in worksite by least square.

    Args:
        name (str): Name of the worksite.
    """
    work: Worksite

    def compute_image_world_least_square(self, type_point: str, control_type: list) -> None:
        """
        Calculates the mean of the result x y z of the point for each shot where it's visible.

        Args:
            type_point (str): "co_points" or "gcp2d"
                              depending on what you want to calculate.
            control_type (list): List of code gcp to take.
                                 To take all points or co_point, control_type = [].
        """
        # Creation of worksite's barycentre.
        bary = self.work.calculate_barycentre()
        if self.work.approxeucli:
            eucliproj = ApproxEuclideanProj(bary[0], bary[1])
        else:
            eucliproj = LocalEuclideanProj(bary[0], bary[1])

        # Retrieving point data from images.
        pd_mes = self.work.get_point_image_dataframe(type_point, control_type)
        pd_mes = pd_mes[pd_mes.duplicated(subset=['id_pt'], keep=False)]

        # Initialization of euclidean points.
        pd_pnt = self.init_eucli_points(pd_mes)

        # Do least square methode.
        pd_pnt = self.least_square_intersect(pd_mes, pd_pnt)

        # Transform euclidean point to world point.
        xw, yw, zw = eucliproj.eucli_to_world(np.array([pd_pnt["x"].to_numpy(),
                                                        pd_pnt["y"].to_numpy(),
                                                        pd_pnt["z"].to_numpy()]))
        pd_pnt["x"] = xw
        pd_pnt["y"] = yw
        pd_pnt["z"] = zw
        self.work.set_point_world_dataframe(pd_pnt, type_point)

    def init_eucli_points(self, pd_mes: pd.DataFrame) -> pd.DataFrame:
        """
        Initialization of ground points.

        Args:
            pd_mes (pd.Dataframe): Dataframe of image data, id_pt, id_img; column, line.

        Returns:
            pd.Dataframe: Dataframe of eucli data, id_pt, x, y, z.
        """
        pb_pnt_unique = pd_mes[~pd_mes['id_pt'].duplicated(keep='first')]
        group = pb_pnt_unique.groupby('id_img')
        frames = []

        for _, (id_shot, pd_mes_pnt) in enumerate(group):
            shot = self.work.shots[id_shot]
            cam = self.work.cameras[shot.name_cam]
            coor_img = np.array([pd_mes_pnt["column"].to_numpy(), pd_mes_pnt["line"].to_numpy()])
            z_world = np.squeeze(np.full(pd_mes_pnt.shape[0], Dtm().get_z_world(shot.pos_shot[:2])))

            # Calculation of world coordinate for all points in this shot
            coor_world = ImageWorldShot(shot, cam).image_z_to_world(coor_img,
                                                                    self.work.type_z_shot,
                                                                    z_world)

            # Transform of world coordinate to euclidean coordinate
            coor_eucli = shot.projeucli.world_to_eucli(coor_world)
            frames += [pd.DataFrame({"id_pt": pd_mes_pnt["id_pt"],
                                     "x": coor_eucli[0],
                                     "y": coor_eucli[1],
                                     "z": coor_eucli[2]})]

        pd_pnt = pd.concat(frames, ignore_index=True)
        pd_pnt["index_pnt"] = pd_pnt.index

        return pd_pnt

    def least_square_intersect(self, pd_mes: pd.DataFrame, pd_pnt: pd.DataFrame) -> pd.DataFrame:
        """
        Methode of least square to calcule world coordinate point.

        Args:
            pd_mes (pd.Dataframe): Dataframe of image data, id_pt, id_img; column, line.
            pd_pnt (pd.Dataframe): Dataframe of world data, id_pt, x, y, z.

        Returns:
            pd.Dataframe: Field data converged.
        """
        # Initialzsation number of observation
        nbr_obs = pd_mes.shape[0] * 2
        nbr_inc = pd_mes.nunique(axis=0)["id_pt"] * 3

        dx = 1.01
        nbr_iter = 0
        while not np.all(abs(dx) < 0.01) and nbr_iter < 5:
            # join data
            pd_mes_temp = pd_mes.join(pd_pnt.set_index('id_pt'), on="id_pt")
            pd_mes_temp = pd_mes_temp.sort_values(by=["index_pnt"]).reset_index(drop=True)
            pd_mes_temp["index_mes"] = pd_mes_temp.index

            mat_a, v_res = self.create_mat_a_and_vect_residu(pd_mes_temp, nbr_obs, nbr_inc)

            # Solving the system by inverting the block diagonal matrix
            dx = invert_diag_sparse_matrix_3_3(mat_a.T @ mat_a) @ mat_a.T @ v_res

            # Update World coordinate
            pd_pnt["x"] += dx[0::3]
            pd_pnt["y"] += dx[1::3]
            pd_pnt["z"] += dx[2::3]

            nbr_iter += 1

        return pd_pnt

    def create_mat_a_and_vect_residu(self, pd_mes_temp: pd.DataFrame,
                                     nbr_obs: int, nbr_inc: int) -> tuple:
        """
        Creation of matrix A and vector residu for the least square methode.

        Args:
            pd_mes_temp (pd.Dataframe): Dataframe of data.
            nbr_obs (int): Number of image observation.
            nbr_inc (int): Number of world observation.

        Returns:
            tuple: Matrix A and vector residu.
        """
        v_res = np.zeros(nbr_obs)
        coord_i, coord_j, data = [], [], []
        for _, (id_shot, pd_data) in enumerate(pd_mes_temp.groupby('id_img')):
            shot = self.work.shots[id_shot]
            cam = self.work.cameras[shot.name_cam]

            pti = WorldImageShot(shot, cam).eucli_to_image(np.array([pd_data["x"].to_numpy(),
                                                                     pd_data["y"].to_numpy(),
                                                                     pd_data["z"].to_numpy()]),
                                                           self.work.type_z_data,
                                                           self.work.type_z_shot)

            _, vect_u, mat_v = set_param_bundle_diff(shot,
                                                     np.array([pd_data["x"].to_numpy(),
                                                               pd_data["y"].to_numpy(),
                                                               pd_data["z"].to_numpy()]))

            coord_i += [np.repeat(2 * pd_data['index_mes'].to_numpy(), 6) +
                        np.tile([0, 0, 0, 1, 1, 1], len(pd_data["x"].to_numpy()))]
            coord_j += [np.repeat(3 * pd_data['index_pnt'].to_numpy(), 6) +
                        np.tile([0, 1, 2, 0, 1, 2], len(pd_data["y"].to_numpy()))]

            data += [(np.tile(np.repeat(cam.focal / vect_u[2]**2, 2), (3, 1)).T *
                      mat_v @ shot.mat_rot_eucli).flatten()]

            v_res[2 * pd_data['index_mes'].to_numpy()] = pd_data["column"].to_numpy() - pti[0]
            v_res[2 * pd_data['index_mes'].to_numpy() + 1] = pd_data["line"].to_numpy() - pti[1]

        # Creation matrix
        coord_i = np.concatenate(coord_i)
        coord_j = np.concatenate(coord_j)
        data = np.concatenate(data)

        return coo_matrix((data, (coord_i, coord_j)), shape=(nbr_obs, nbr_inc)).tocsr(), v_res
