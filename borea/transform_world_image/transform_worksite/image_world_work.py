"""
Image world transformation module for worksite
"""
from dataclasses import dataclass
from borea.worksite.worksite import Worksite
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.image_world_intersection import WorldIntersection  # noqa: E501
from borea.transform_world_image.transform_worksite.image_world_least_square import WorldLeastSquare


@dataclass
class ImageWorldWork:
    """
    Class to calculate image coordinate to world coordinate in worksite.

    Args:
        name (str): Name of the worksite.
    """
    work: Worksite

    def manage_image_world(self, type_point: str = "co_points", type_process: str = "inter",
                           control_type: list = None) -> None:
        """
        Process to calcule image coordinate to world coordinate.

        Args:
            type_point (str): "co_points" or "gcp2d"
                              depending on what you want to calculate.
            type_process (str): Type of process you want to use.
                                * "inter" by intersect bundle of point in each shot.
                                * "square" take all point and do methode least square.
            control_type (list): Type controle for gcp.
        """
        if type_point not in ["co_points", "gcp2d"]:
            raise ValueError(f"type_point {type_point} is incorrect,['co_points','gcp2d']")

        if type_process not in ["inter", "square"]:
            raise ValueError(f"type_process {type_process} is incorrect, "
                             "['inter','square']")

        if control_type is None or type_point == "co_points":
            control_type = []

        if type_process == "inter":
            WorldIntersection(self.work).calculate_image_world_by_intersection(type_point,
                                                                               control_type)

        if type_process == "square":
            WorldLeastSquare(self.work).compute_image_world_least_square(type_point, control_type)
