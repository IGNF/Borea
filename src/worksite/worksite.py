"""
Worksite data class module.
"""
import numpy as np
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork
from src.transform_world_image.transform_worksite.space_resection import SpaceResection


class Worksite(WorldImageWork, ImageWorldWork):
    """
    Worksite class, class main of the tools.

    Args:
        name (str): Name of the worksite.
    """

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
