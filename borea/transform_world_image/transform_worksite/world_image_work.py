"""
World image transformation module for Worksite
"""
from dataclasses import dataclass
from borea.worksite.worksite import Worksite
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot


@dataclass
class WorldImageWork:
    """
    Class to calculate world coordinate to image coordinate in worksite.

    Args:
        name (str): Name of the worksite.
    """
    work: Worksite

    def calculate_world_to_image(self, lcode: list) -> None:
        """
        Calculates the position of gcp3d which corresponds to the data code
        in the images they appear in.

        Args:
            lcode (list): gcp code.
        """
        if self.work.gcp3d and self.work.gcp2d:
            for name_gcp, gcp in self.work.gcp3d.items():
                if gcp.code in lcode or lcode == []:
                    try:
                        list_shots = self.work.gcp2d[name_gcp]
                        for name_shot in list_shots:
                            shot = self.work.shots[name_shot]
                            cam = self.work.cameras[shot.name_cam]
                            coor_img = WorldImageShot(shot,
                                                      cam).world_to_image(gcp.coor,
                                                                          self.work.type_z_data,
                                                                          self.work.type_z_shot)
                            self.work.shots[name_shot].gcp3d[name_gcp] = coor_img
                    except KeyError:
                        print(f"Warning: id point {name_gcp} is present "
                              "in gcp3d but not in gcp2d.")
                        continue
