"""
Worksite data class module.
"""
import numpy as np
import pandas as pd
from src.datastruct.workshot import Workshot
from src.transform_world_image.transform_shot.space_resection import SpaceResection


class Worksite(Workshot):
    """
    Worksite class, class main of the tools.

    Args:
        name (str): Name of the worksite.
    """

    def getatt(self, attsrt: str) -> any:
        """
        Get attribut by str name.

        Args:
            attstr (str): String attribute.

        Returns:
            Any: The attribute of the class.
        """
        # pylint: disable-next=unnecessary-dunder-call
        return self.__getattribute__(attsrt)

    def get_point_image_pandas(self, type_point: str, control_type: list) -> pd.DataFrame:
        """
        Retrieves id_pt, id_img, column, line in a pandas of the requested point type.

        Args:
            type_point (str): "co_points" or "ground_img_pts" depending on what you want to get.
            control_type (list): Type controle for gcp.

        Returns:
            pandas: Pandas table.
        """
        if type_point not in ["co_points", "ground_img_pts"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','ground_img_pts']")

        if type_point == "co_points":
            control_type = []

        id_pt = []
        id_img = []
        coor = []
        for name_pt, list_shot in self.getatt(type_point).items():
            if control_type != [] and self.gcps[name_pt].code not in control_type:
                continue
            for name_shot in list_shot:
                id_pt.append(name_pt)
                id_img.append(name_shot)
                coor.append(self.shots[name_shot].getatt(type_point)[name_pt])

        coor = np.array(coor)
        return pd.DataFrame({"id_pt": id_pt, "id_img": id_img,
                             "column": coor[:, 0], "line": coor[:, 1]})

    def set_point_image_pandas(self, pd_mes: pd.DataFrame, type_point: str) -> None:
        """
        Set requested point type by pandas table id_pt, id_img, column, line.

        Args:
            pd_mes (pd): Pandas table of data.
            type_point (str): "co_points" or "ground_img_pts" depending on what you want to set.
        """
        if type_point not in ["co_points", "ground_img_pts"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','ground_img_pts']")

        for _, row in pd_mes.iterrows():
            self.shots[row['id_img']].getatt(type_point)[row['id_pt']] = np.array([row['column'],
                                                                                   row['line']])

    def get_point_world_pandas(self, type_point: str, control_type: list) -> pd.DataFrame:
        """
        Retrieves id_pt, x, y, z in a pandas of the requested point type.

        Args:
            type_point (str): "co_points" or "ground_img_pts" depending on what you want to get.
            control_type (list): Type controle for gcp.

        Returns:
            pandas: Pandas table.
        """
        if type_point not in ["co_points", "ground_img_pts"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','ground_img_pts']")

        if type_point == 'co_points':
            out_pt = "co_pts_world"
            control_type = []
        else:
            out_pt = "img_pts_world"

        id_pt = []
        coor = []
        for name_pt, coor_pt in self.getatt(out_pt).items():
            if control_type != [] and self.gcps[name_pt].code not in control_type:
                continue
            id_pt.append(name_pt)
            coor.append(coor_pt)

        coor = np.array(coor)
        return pd.DataFrame({"id_pt": id_pt, "x": coor[:, 0], "y": coor[:, 1], "z": coor[:, 2]})

    def set_point_world_pandas(self, pd_mes: pd.DataFrame, type_point: str) -> None:
        """
        Set requested point type by pandas table id_pt, x, y, z.

        Args:
            pd_mes (pd): Pandas table of data.
            type_point (str): "co_points" or "ground_img_pts" depending on what you want to set.
        """
        if type_point not in ["co_points", "ground_img_pts"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','ground_img_pts']")

        if type_point == 'co_points':
            out_pt = "co_pts_world"
        else:
            out_pt = "img_pts_world"

        for _, row in pd_mes.iterrows():
            self.getatt(out_pt)[row['id_pt']] = np.array([row['x'], row['y'], row['z']])

    def calculate_barycentre(self) -> np.ndarray:
        """
        Calculate barycentre of the worksite.

        Returns:
            np.array: The barycentre [X, Y, Z].
        """
        size = len(self.shots)
        pos = np.zeros((size, 3))
        i = 0
        for shot in self.shots.values():
            pos[i, :] = shot.pos_shot
            i += 1
        return np.mean(pos, axis=0)

    def shootings_position(self, add_pixel: tuple = (0, 0)) -> None:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.
        For all shot with a variation pixel.

        Args:
            add_pixel (tuple): Factor (column, line) added on observable point.
        """
        for key_shot, item_shot in self.shots.items():
            cam = self.cameras[item_shot.name_cam]
            self.shots[key_shot] = SpaceResection(item_shot, cam,
                                                  self.type_z_data,
                                                  self.type_z_shot).space_resection(add_pixel)
