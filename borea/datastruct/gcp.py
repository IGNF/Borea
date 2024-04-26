"""
Ground Control Point (GCP) class.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class GCP:
    """
    Ground Control Point class.

    Args:
        name_gcp (str): Name of the gcp.
        code (str): IGN code to differentiate between support points (1, 2, 3)
                    and control points (11, 12, 13)
                    1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
        coor (numpy.array): Array of ground coordinate [X, Y, Z].
    """
    name_gcp: str
    code: str
    coor: np.ndarray
