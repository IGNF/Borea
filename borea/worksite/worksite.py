"""
Worksite data class module.
"""
import numpy as np
import pandas as pd
from borea.datastruct.dtm import Dtm
from borea.datastruct.workdata import Workdata
from borea.geodesy.proj_engine import ProjEngine
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


class Worksite(Workdata):
    """
    Worksite class, class main of the tools.

    Args:
        name (str): Name of the worksite.
    """

    def get_point_image_dataframe(self, type_point: str, control_type: list = None) -> pd.DataFrame:
        """
        Retrieves id_pt, id_img, column, line in a pandas of the requested point type.

        Args:
            type_point (str): "co_points" or "gcp2d" depending on what you want to get.
            control_type (list): Type controle for gcp.

        Returns:
            pandas: Pandas table.
        """
        if type_point not in ["co_points", "gcp2d", "gcp3d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d','gcp3d']")

        if type_point == "co_points" or not control_type:
            control_type = []

        type_iter = type_point if type_point != "gcp3d" else "gcp2d"

        id_pt = []
        id_img = []
        coor = []
        for name_pt, list_shot in getattr(self, type_iter).items():
            if control_type and self.gcp3d[name_pt].code not in control_type:
                continue
            for name_shot in list_shot:
                id_pt.append(name_pt)
                id_img.append(name_shot)
                coor.append(getattr(self.shots[name_shot], type_point)[name_pt])

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
            try:
                getattr(self.shots[row['id_img']],
                        type_point)[row['id_pt']] = np.array([row['column'], row['line']])
            except KeyError:
                continue

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

        out_pt, control_type = self.get_attr_transfo_pt(type_point, control_type)

        id_pt = []
        coor = []
        for name_pt, coor_pt in getattr(self, out_pt).items():
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

        out_pt, _ = self.get_attr_transfo_pt(type_point, None)

        if "type" not in list(pd_mes.columns):
            for _, row in pd_mes.iterrows():
                getattr(self, out_pt)[row['id_pt']] = np.array([row['x'], row['y'], row['z']])
        else:
            for _, row in pd_mes.iterrows():
                self.add_gcp3d(row['id_pt'], row['type'], np.array([row['x'], row['y'], row['z']]))

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

        out_pt, _ = self.get_attr_transfo_pt(type_point, None)

        if not getattr(self, out_pt):
            raise ValueError(f"Attribut {out_pt} in worksite is empty.")

        co_point = getattr(self.shots[name_shot], type_point)
        world_pt = []
        img_pt = []
        for key_pt, img_coor in co_point.items():
            try:
                pt_world = getattr(self, out_pt)[key_pt]
                world_pt.append(pt_world)
                img_pt.append(img_coor)
            except KeyError:
                print(f"Point {key_pt}, doesn't have world coordinate, perhaps a single point.")

        return np.stack(img_pt, axis=-1), np.stack(world_pt, axis=-1)

    def set_param_shot(self, approx=False) -> None:
        """
        Setting up different parameters in shot by data ressources.

        Args:
            approx (bool): True if you want to use approx euclidean system.
        """
        check_dtm = True
        if not Dtm().path_dtm:
            check_dtm = False

        if not ProjEngine().geoid:
            raise ValueError("you have not entered all the information required to set up"
                             " the projection system. Because type z shot != type z data.")

        self.approxeucli = approx
        for shot in self.shots.values():
            shot.set_param_eucli_shot(approx)
            if check_dtm:
                cam = self.cameras[shot.name_cam]
                z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                                   self.type_z_shot,
                                                                   self.type_z_shot, False)[2]
                shot.set_z_nadir(z_nadir)

    def set_unit_shot(self, type_z: str = None, unit_angle: str = None,
                      linear_alteration: bool = None, order_axe: str = None) -> None:
        """
        Allows you to change unit or parameter of shots.

        Args:
            type_z (str): Unit of z shot you want.
            unit_angle (str): Unit angle you want.
            linear_alteration (bool): True if you want data corrected.
            order_axe (str): Order of rotation matrice you want in your angle.
        """
        if unit_angle not in ["degree", "radian", None]:
            raise ValueError(f"unit_angle: {unit_angle} is not recognized,"
                             "recognized values are degree and radian.")

        if type_z not in ["height", "altitude", None]:
            raise ValueError(f"type_z: {type_z} is not recognized,"
                             "recognized values are altitude and height.")

        if type_z == self.type_z_shot:
            type_z = None
        else:
            self.type_z_shot = type_z

        for shot in self.shots.values():
            if unit_angle is not None:
                shot.set_unit_angle(unit_angle)
            if type_z is not None:
                shot.set_type_z(type_z)
            if linear_alteration is not None:
                shot.set_linear_alteration(linear_alteration)
            if order_axe is not None:
                shot.set_order_axe(order_axe)

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

    def get_attr_transfo_pt(self, type_point: str, control_type: list) -> tuple:
        """
        Get string name of attribut where is save transformation image to world point.

        Args:
            type_point (str):"co_points" or "gcp2d"
                              depending on what you want.
            control_type (list): Type controle for gcp.
        """
        if type_point == 'co_points':
            out_pt = "co_pts_world"
            control_type = []
        else:
            out_pt = "gcp2d_in_world"

        return out_pt, control_type
