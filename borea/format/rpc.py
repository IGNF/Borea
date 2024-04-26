"""
Class module for Rpc
"""
import numpy as np
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera
from borea.geodesy.proj_engine import ProjEngine
from borea.datastruct.dtm import Dtm
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from borea.utils.miscellaneous.miscellaneous import normalize


class Rpc:
    """
    A class for computing RPC geometries.

    .. note::
        A RPC is always describing a transformation from
        geographical coordinates to images coordinates.
    """
    def __init__(self) -> None:
        self.param_rpc = {}
        self.fact_rpc = None

    @classmethod
    def from_shot(cls, shot: Shot, cam: Camera, param_rpc: dict, unit_data: dict) -> None:
        """
        Calculate RPC of the shot.

        Args:
            shot (Shot): Shot to calculate rpc.
            cam (Camera): Camera of the shot.
            param_rpc (dict): Dictionary of parameters for rpc calculation.
            key;
            "size_grid"; size of the grip to calcule rpc.
            "order"; order of the polynome of the rpc.
            "fact_rpc"; rpc factor for world coordinate when src is not WGS84.
            unit_data (dict): Dictionary of data unity.
            key;
            "unit_z_data"; Unity of z data.
            "unit_z_shot"; Unity of z shot.

        Returns:
            Rpc: The object rpc.
        """
        obj = cls()
        obj.fact_rpc = param_rpc["fact_rpc"]
        obj.param_rpc["ERR_BIAS"] = -1
        obj.param_rpc["ERR_RAND"] = -1

        grid_img, grid_world = obj.create_grid_rpc(shot, cam, unit_data, param_rpc["size_grid"])

        img_norm, world_norm = obj.normalize_data(grid_img, grid_world)

        coeffx = obj.least_square_rpc(img_norm[0], world_norm, param_rpc["order"])
        coeffy = obj.least_square_rpc(img_norm[1], world_norm, param_rpc["order"])

        # Save param
        obj.param_rpc["SAMP_NUM_COEFF"] = coeffx[0:20]  # X numerator
        obj.param_rpc["SAMP_DEN_COEFF"] = coeffx[20:]  # X denominator
        obj.param_rpc["LINE_NUM_COEFF"] = coeffy[0:20]  # Y numerator
        obj.param_rpc["LINE_DEN_COEFF"] = coeffy[20:]  # Y denominator
        return obj

    def create_grid_rpc(self, shot: Shot, cam: Camera,
                        unit_data: dict, size_grid: int = 100) -> tuple:
        """
        Creation of a grid on a size_grid buffer around the acquisition.

        Args:
            shot (Shot): The shot to create the grid.
            cam (Camera): The camera of the shot.
            unit_data (dict): Dictionary of data unity.
            key;
            "unit_z_data"; Unity of z data.
            "unit_z_shot"; Unity of z shot.
            size_grid (int): The size of the grid to add around the shot.

        Returns:
            tuple: Image coordinates [col, line] and world coordinates [X, Y, Z] of the grid.
        """
        corner_img = np.array([[0, cam.width, 0, cam.width], [0, cam.height, cam.height, 0]])
        pt_w = ImageWorldShot(shot, cam).image_to_world(corner_img,
                                                        unit_data["unit_z_data"],
                                                        unit_data["unit_z_shot"])
        pt_min = np.min(pt_w, axis=1)[0:2] - size_grid - 1
        pt_max = np.max(pt_w, axis=1)[0:2] + size_grid + 1
        x, y = np.mgrid[int(pt_min[0]):int(pt_max[0]) + size_grid:size_grid,
                        int(pt_min[1]):int(pt_max[1]) + size_grid:size_grid]
        x, y = x.ravel(), y.ravel()
        z = np.squeeze(Dtm().get_z_world(np.array([x, y])))
        pt_img = WorldImageShot(shot, cam).world_to_image(np.array([x, y, z]),
                                                          unit_data["unit_z_data"],
                                                          unit_data["unit_z_shot"])
        return pt_img, np.array([x, y, z])

    def normalize_data(self, grid_img: np.ndarray, grid_world: np.ndarray) -> tuple:
        """
        Normalize data grid to calculate Rpc.

        Args:
            grid_img (np.array): Image coordinates [c, l] of the grid.
            grid_world (np.array): World coordinates [x, y, z] of the grid.

        Returns:
            tuple: grid image normalize and grid world normalize.
        """
        if self.fact_rpc is None:
            x_geog, y_geog, z_geog = ProjEngine().carto_to_geog(grid_world[0],
                                                                grid_world[1],
                                                                grid_world[2])
        else:
            x_geog = grid_world[0]*self.fact_rpc
            y_geog = grid_world[1]*self.fact_rpc
            z_geog = grid_world[2]

        # Normalization of image coordinates
        col_n_o_s = normalize(grid_img[0])
        lin_n_o_s = normalize(grid_img[1])

        # Normalization of world coordinates
        x_n_o_s = normalize(x_geog)
        y_n_o_s = normalize(y_geog)
        z_n_o_s = normalize(z_geog)

        self.param_rpc["LINE_OFF"] = lin_n_o_s[1]
        self.param_rpc["SAMP_OFF"] = col_n_o_s[1]
        self.param_rpc["LAT_OFF"] = y_n_o_s[1]
        self.param_rpc["LONG_OFF"] = x_n_o_s[1]
        self.param_rpc["HEIGHT_OFF"] = z_n_o_s[1]
        self.param_rpc["LINE_SCALE"] = lin_n_o_s[2]
        self.param_rpc["SAMP_SCALE"] = col_n_o_s[2]
        self.param_rpc["LAT_SCALE"] = y_n_o_s[2]
        self.param_rpc["LONG_SCALE"] = x_n_o_s[2]
        self.param_rpc["HEIGHT_SCALE"] = z_n_o_s[2]

        coor_img = np.array([col_n_o_s[0], lin_n_o_s[0]])
        coor_world = np.array([x_n_o_s[0], y_n_o_s[0], z_n_o_s[0]])

        return coor_img, coor_world

    def least_square_rpc(self, img_norm: np.ndarray, world_norm: np.ndarray,
                         polynomial_degree: int) -> np.ndarray:
        """
        Calcule Rpc of the shot by least square methode for one image coordinate.

        Args:
            img_norm (np.array): Normalize coordinates column or line of point in image.
            world_norm (np.array): Normalize coordinate of world grid.
            polynomial_degree (int): Degree of the polynomial of the rpc (1, 2, 3).

        Returns:
            np.array: Rpc coefficients.
        """
        mat_obs = self.setup_matrix_obs_rpc(img_norm, world_norm, polynomial_degree)
        x = np.linalg.lstsq(mat_obs, img_norm, rcond=None)[0]

        coef_rpc = np.zeros(40)
        if polynomial_degree == 1:
            coef_rpc[0:4] = x[0:4]
            coef_rpc[20] = 1
            coef_rpc[21:24] = x[4:7]

        elif polynomial_degree == 2:
            coef_rpc[0:10] = x[0:10]
            coef_rpc[20] = 1
            coef_rpc[21:30] = x[10:19]

        elif polynomial_degree == 3:
            coef_rpc[0:20] = x[0:20]
            coef_rpc[20] = 1
            coef_rpc[21:40] = x[20:39]

        return coef_rpc

    def setup_matrix_obs_rpc(self, img_norm: np.ndarray, world_norm: np.ndarray,
                             polynomial_degree: int) -> np.ndarray:
        """
        Setup observation matrix of the rpc for least square methode.

        Args:
            img_norm (np.array): Normalize coordinates column or line of point in image.
            world_norm (np.array): Normalize coordinate of world grid.
            polynomial_degree (int): Degree of the polynomial of the rpc (1, 2, 3).

        Returns:
            np.array: Observation matrix of the Rpc.
        """
        mat_a1 = []
        mat_a2 = []
        ligne_a = np.ones((len(img_norm)))
        mat_a1.append(ligne_a)

        if polynomial_degree in [1, 2, 3]:
            mat_a1.append(ligne_a * world_norm[0])
            mat_a1.append(ligne_a * world_norm[1])
            mat_a1.append(ligne_a * world_norm[2])

            mat_a2.append(ligne_a * -img_norm * world_norm[0])
            mat_a2.append(ligne_a * -img_norm * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[2])
        else:
            raise ValueError("The degree of the polynomial must be 1, 2 or 3")

        if polynomial_degree in [2, 3]:
            mat_a1.append(ligne_a * world_norm[0] * world_norm[1])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[1] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[0])
            mat_a1.append(ligne_a * world_norm[1] * world_norm[1])
            mat_a1.append(ligne_a * world_norm[2] * world_norm[2])

            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[1] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[0])
            mat_a2.append(ligne_a * -img_norm * world_norm[1] * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[2] * world_norm[2])

        if polynomial_degree == 3:
            mat_a1.append(ligne_a * world_norm[0] * world_norm[1] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[0] * world_norm[0])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[1] * world_norm[1])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[2] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[0] * world_norm[1])
            mat_a1.append(ligne_a * world_norm[1] * world_norm[1] * world_norm[1])
            mat_a1.append(ligne_a * world_norm[1] * world_norm[2] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[0] * world_norm[0] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[1] * world_norm[1] * world_norm[2])
            mat_a1.append(ligne_a * world_norm[2] * world_norm[2] * world_norm[2])

            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[1] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[0] * world_norm[0])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[1] * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[2] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[0] * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[1] * world_norm[1] * world_norm[1])
            mat_a2.append(ligne_a * -img_norm * world_norm[1] * world_norm[2] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[0] * world_norm[0] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[1] * world_norm[1] * world_norm[2])
            mat_a2.append(ligne_a * -img_norm * world_norm[2] * world_norm[2] * world_norm[2])

        return np.concatenate((np.array(mat_a1), np.array(mat_a2)), axis=0).T
