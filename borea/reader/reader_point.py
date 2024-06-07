"""
Script to read point (connecting point, gcp2d gcp3d) format
.txt/.mes/.app with data arranged in columns.
"""
from pathlib import Path, PureWindowsPath
import pandas as pd
import numpy as np
from borea.worksite.worksite import Worksite
from borea.utils.check.check_args_reader_pt import check_header_file


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

    header, type_z = check_header_file(header, type_point)
    work.type_z_data = type_z

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

                    try:
                        getattr(work, "add_" + type_point)(info[header.index("P")],
                                                           info[header.index(type_2args)],
                                                           coor)
                    except ValueError as e:
                        raise ValueError("The letter T is missing "
                                         "from the header of the file.") from e
            file_pts.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {path} is incorrect !!!") from e


def read_file_pt_dataframe(path: str, header: list, type_point: str) -> pd.DataFrame:
    """
    Read file of points to save in Dataframe.

    Agrs:
        file (str): Path of points file.
        header (list): Header of file to read column.
        type_point (str): Type of point is reading (pt2d, pt3d).

    Returns:
        pd.Dataframe: Dataframe of data.
    """
    if type_point not in ["pt2d", "pt3d"]:
        raise ValueError(f"type {type_point} in incorrect. ['pt2d', 'pt3d']")

    header, _ = check_header_file(header, type_point)

    id_pt = []
    ttype = []
    coor = []
    try:
        with open(Path(PureWindowsPath(path)), 'r', encoding="utf-8") as file_pts:
            for pt in file_pts.readlines():
                if pt != '\n' and pt[0] != '#':
                    info = pt.split()

                    if type_point == "pt3d":
                        coor.append([float(info[header.index("X")]),
                                     float(info[header.index("Y")]),
                                     float(info[header.index("Z")])])
                        type_2args = "T"
                    else:
                        coor.append([float(info[header.index("X")]),
                                     float(info[header.index("Y")])])
                        type_2args = "N"

                    id_pt.append(info[header.index("P")])
                    try:
                        ttype.append(info[header.index(type_2args)])
                    except ValueError:
                        continue
            file_pts.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {path} is incorrect !!!") from e

    coor = np.array(coor)
    if type_point == "pt3d":
        df = pd.DataFrame({"id_pt": id_pt,
                           "type": ttype if ttype else None,
                           "x": coor[:, 0],
                           "y": coor[:, 1],
                           "z": coor[:, 2]})
    else:
        df = pd.DataFrame({"id_pt": id_pt,
                           "id_shot": ttype,
                           "column": coor[:, 0],
                           "line": coor[:, 1]})
    return df
