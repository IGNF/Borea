"""
A module for manipulating an euclidean projection.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class EuclideanProj:
    """
    This class represents a Euclidean projection system.

    Args:
        x_central (float): x coordinate of the central point of the Euclidean system.
        y_central (float): y coordinate of the central point of the Euclidean system.

    .. note::
        A Euclidean system is a local Euclidean reference system in which
        the collinear equation is valid.
    """
    x_central: float
    y_central: float

    def __post_init__(self) -> None:
        self.pt_central = np.array([self.x_central, self.y_central, 0])
