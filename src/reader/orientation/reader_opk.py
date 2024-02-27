"""
A script to read opk file.
"""
import platform
from pathlib import Path
import numpy as np
from src.worksite.worksite import Worksite
from src.utils.check.check_header import check_header_file


def read(file: Path, args: dict, work: Worksite) -> Worksite:
    """
    Reads an opk file to transform it into a Workside object.

    Args:
        file (Path): Path to the worksite.
        args (dict): Information for reading an opk file.
                    keys:
                    "interval" (list): Interval of lines taken into account,
                                       [i, j] if i or j is None = :.
                                       e.g. [1, None] = [1:]
                    "header" (list): List of column type file.
                    "unit_angle" (str): Unit of angle 'degrees' or 'radian'.
                    "linear_alteration" (bool): True if data corrected by linear alteration.
        work (Worksite): Worksite to add shot

    Returns:
        Worksite: The worksite.
    """
    if args["unit_angle"] not in ["degree", "radian"]:
        raise ValueError(f"Unit angles is incorrect {args['unit_angle']},"
                         "correct writing is degree or radian.")

    lf, ll = args["interval"]
    if lf is not None:
        lf -= 1
    if ll is not None:
        ll -= 1
    header, type_z = check_header_file(args["header"].split())
    try:
        with open(file, 'r', encoding="utf-8") as file_opk:
            for item_opk in file_opk.readlines()[lf:ll]:
                item_shot = item_opk.split()
                if len(item_shot) != len(header):
                    raise ValueError(f"The number of columns in your file {len(item_shot)}"
                                     " is different from the number of columns in your input"
                                     f" format {len(header)}.")
                work.add_shot(item_shot[header.index("N")],
                              np.array([
                                   float(item_shot[header.index("X")]),
                                   float(item_shot[header.index("Y")]),
                                   float(item_shot[header.index("Z")])], dtype=float),
                              np.array([
                                   float(item_shot[header.index("O")]),
                                   float(item_shot[header.index("P")]),
                                   float(item_shot[header.index("K")])], dtype=float),
                              item_shot[header.index("C")],
                              args["unit_angle"], args["linear_alteration"])
            file_opk.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!! "
                                f"or your os is {platform.system()}."
                                "For Windows path is \\,"
                                " for Linux and MacOS (Darwin) is / .") from e

    work.type_z_shot = type_z
    return work
