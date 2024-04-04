"""
Worksite data class module.
"""
import numpy as np
import pandas as pd
from src.datastruct.workshot import Workshot


class Worksite(Workshot):
    """
    Worksite class, class main of the tools.

    Args:
        name (str): Name of the worksite.
    """

    def getattr(self, attsrt: str) -> any:
        """
        Get attribut by str name.

        Args:
            attstr (str): String attribute.

        Returns:
            Any: The attribute of the class.
        """
        # pylint: disable-next=unnecessary-dunder-call
        return self.__getattribute__(attsrt)

    def get_point_image_dataframe(self, type_point: str, control_type: list) -> pd.DataFrame:
        """
        Retrieves id_pt, id_img, column, line in a pandas of the requested point type.

        Args:
            type_point (str): "co_points" or "gcp2d" depending on what you want to get.
            control_type (list): Type controle for gcp.

        Returns:
            pandas: Pandas table.
        """
        if type_point not in ["co_points", "gcp2d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d']")

        if type_point == "co_points":
            control_type = []

        id_pt = []
        id_img = []
        coor = []
        for name_pt, list_shot in self.getattr(type_point).items():
            if control_type and self.gcp3d[name_pt].code not in control_type:
                continue
            for name_shot in list_shot:
                id_pt.append(name_pt)
                id_img.append(name_shot)
                coor.append(self.shots[name_shot].getattr(type_point)[name_pt])

        coor = np.array(coor)
        return pd.DataFrame({"id_pt": id_pt, "id_img": id_img,
                             "column": coor[:, 0], "line": coor[:, 1]})

    def set_point_image_dataframe(self, pd_mes: pd.DataFrame, type_point: str) -> None:
        """
        Set requested point type by pandas table id_pt, id_img, column, line.

        Args:
            pd_mes (pd): Pandas table of data.
            type_point (str): "co_points" or "gcp2d" depending on what you want to set.
        """
        if type_point not in ["co_points", "gcp2d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d']")

        for _, row in pd_mes.iterrows():
            self.shots[row['id_img']].getattr(type_point)[row['id_pt']] = np.array([row['column'],
                                                                                   row['line']])

    def get_point_world_dataframe(self, type_point: str, control_type: list) -> pd.DataFrame:
        """
        Retrieves id_pt, x, y, z in a pandas of the requested point type.

        Args:
            type_point (str): "co_points" or "gcp2d" depending on what you want to get.
            control_type (list): Type controle for gcp.

        Returns:
            pandas: Pandas table.
        """
        if type_point not in ["co_points", "gcp2d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d']")

        if type_point == 'co_points':
            out_pt = "co_pts_world"
            control_type = []
        else:
            out_pt = "gcp2d_in_world"

        id_pt = []
        coor = []
        for name_pt, coor_pt in self.getattr(out_pt).items():
            if control_type and self.gcp3d[name_pt].code not in control_type:
                continue
            id_pt.append(name_pt)
            coor.append(coor_pt)

        coor = np.array(coor)
        return pd.DataFrame({"id_pt": id_pt, "x": coor[:, 0], "y": coor[:, 1], "z": coor[:, 2]})

    def set_point_world_dataframe(self, pd_mes: pd.DataFrame, type_point: str) -> None:
        """
        Set requested point type by pandas table id_pt, x, y, z.

        Args:
            pd_mes (pd): Pandas table of data.
            type_point (str): "co_points" or "gcp2d" depending on what you want to set.
        """
        if type_point not in ["co_points", "gcp2d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d']")

        if type_point == 'co_points':
            out_pt = "co_pts_world"
        else:
            out_pt = "gcp2d_in_world"

        for _, row in pd_mes.iterrows():
            self.getattr(out_pt)[row['id_pt']] = np.array([row['x'], row['y'], row['z']])

    def get_coor_pt_img_and_world(self, name_shot: str, type_point: str) -> tuple:
        """
        Recovers image and terrain data for all link points in the image.

        Args:
            name_shot (str): Name of shot to take.
            type_point (str): Type point to take "co_points" or "gcp2d".

        Returns:
            tuple: np.array(obs_image), np.array(pt_world).
        """
        if type_point not in ['co_points', 'gcp2d']:
            raise ValueError(f"type point {type_point} is incorrect.['co_points','gcp2d']")

        if type_point == 'co_points':
            out_pt = "co_pts_world"
        else:
            out_pt = "gcp2d_in_world"

        if not self.getattr(out_pt):
            raise ValueError(f"Attribut {out_pt} in worksite is empty.")

        co_point = self.shots[name_shot].getattr(type_point)
        world_pt = []
        img_pt = []
        for key_pt, img_coor in co_point.items():
            try:
                pt_world = self.getattr(out_pt)[key_pt]
                world_pt.append(pt_world)
                img_pt.append(img_coor)
            except KeyError:
                print(f"Point {key_pt}, doesn't have world coordinate, perhaps a single point.")

        return np.stack(img_pt, axis=-1), np.stack(world_pt, axis=-1)

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
