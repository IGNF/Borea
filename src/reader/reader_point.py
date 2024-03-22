"""
Script to read point (connecting point, gcp2d gcp3d) format
.txt/.mes/.app with data arranged in columns.
"""
from pathlib import Path, PureWindowsPath

import numpy as np
from src.worksite.worksite import Worksite
from src.utils.check.check_head_file_pt import check_header_file


def read_file_pt(path: str, header: list, type_point: str, work: Worksite) -> None:
    """
    Read file of points.

    Agrs:
        file (str): Path of points file.
        header (list): Header of file to read column.
        type_point (str): Type of point is reading (co_point, gcp2d, gcp3d).
        work (Worksite): Worksite which needs connecting points.
    """
    if type_point not in ["co_point", "gcp2d", "gcp3d"]:
        raise ValueError(f"type {type_point} in incorrect. ['co_point', 'gcp2d', 'gcp3d']")

    check_header_file(header, type_point)

    try:
        with open(Path(PureWindowsPath(path)), 'r', encoding="utf-8") as file_pts:
            for pt in file_pts.readlines():
                if pt != '\n' and pt[0] != '#':
                    info = pt.split()

                    if type_point == "gcp3d":
                        coor = np.array([float(info[header.index("X")]),
                                         float(info[header.index("Y")]),
                                         float(info[header.index("Z")])])
                        type_2args = "T"
                    else:
                        coor = np.array([float(info[header.index("X")]),
                                         float(info[header.index("Y")])])
                        type_2args = "N"

                    work.getattr("add_" + type_point)(info[header.index("P")],
                                                      info[header.index(type_2args)],
                                                      coor)
            file_pts.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {path} is incorrect !!!") from e
