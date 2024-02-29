"""
Image world transformation module for worksite
"""
from dataclasses import dataclass
from src.worksite.worksite import Worksite
from src.transform_world_image.transform_worksite.image_world_intersection import WorldIntersection
from src.transform_world_image.transform_worksite.image_world_least_square import WorldLeastSquare


@dataclass
class ImageWorldWork:
    """
    Class to calculate image coordinate to world coordinate in worksite.

    Args:
        name (str): Name of the worksite.
    """
    work: Worksite

    def manage_image_world(self, type_point: str = "co_points", type_process: str = "intersection",
                           control_type: list = None) -> None:
        """
        Process to calcule image coordinate to world coordinate.

        Args:
            type_point (str): "co_points" or "ground_img_pts"
                              depending on what you want to calculate.
            type_process (str): Type of process you want to use.
                                * "intersection" by intersect bundle of point in each shot.
                                * "least_square" take all point and do methode.
            control_type (list): Type controle for gcp.
        """
        if type_point not in ["co_points", "ground_img_pts"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','ground_img_pts']")

        if type_process not in ["intersection", "least_square"]:
            raise ValueError(f"type_process {type_process} is incorrect, "
                             "['intersection','least_square']")

        if control_type is None or type_point == "co_points":
            control_type = []

        if type_process == "intersection":
            WorldIntersection(self.work).calculate_image_world_by_intersection(control_type,
                                                                               type_point)

        if type_process == "least_square":
            WorldLeastSquare(self.work).compute_image_world_least_square(type_point, control_type)
