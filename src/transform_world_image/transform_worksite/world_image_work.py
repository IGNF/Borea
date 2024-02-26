"""
World image transformation module for Worksite
"""
from src.datastruct.workdata import Workdata
from src.transform_world_image.transform_shot.world_image_shot import WorldImageShot


class WorldImageWork(Workdata):
    """
    Class to calculate world coordinate to image coordinate in worksite.

    Args:
        name (str): Name of the worksite.
    """

    def calculate_world_to_image(self, lcode: list) -> None:
        """
        Calculates the position of gcps which corresponds to the data code
        in the images they appear in.

        Args:
            lcode (list): gcp code.
        """
        if self.gcps and self.ground_img_pts:
            for name_gcp, gcp in self.gcps.items():
                if gcp.code in lcode or lcode == []:
                    try:
                        list_shots = self.ground_img_pts[name_gcp]
                        for name_shot in list_shots:
                            shot = self.shots[name_shot]
                            cam = self.cameras[shot.name_cam]
                            coor_img = WorldImageShot(shot, cam).world_to_image(gcp.coor,
                                                                                self.type_z_data,
                                                                                self.type_z_shot)
                            self.shots[name_shot].gcps[name_gcp] = coor_img
                    except KeyError:
                        print(f"Warning: id point {name_gcp} is present "
                              "in gcp but not in image control points.")
                        continue
