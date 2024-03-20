"""
Workshot data shot class module.
"""
import numpy as np
from src.datastruct.workdata import Workdata
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm


class Workshot(Workdata):
    """
    Workshot class, class to manage shot data in workdata.

    Args:
        name (str): Name of the worksite.
    """

    def set_param_shot(self, approx=False) -> None:
        """
        Setting up different parameters in shot by data ressources.

        Args:
            approx (bool): True if you want to use approx euclidean system.
        """
        check_dtm = True
        if not Dtm().path_dtm:
            check_dtm = False

        if not ProjEngine().projection_list:
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
                      linear_alteration: bool = None) -> None:
        """
        Allows you to change the orientation angle unit.

        Args:
            unit_angle (str): Unit angle.
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
