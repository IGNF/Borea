"""
A script to read opk file.
"""
import platform
import numpy as np
from src.datastruct.worksite import Worksite


def read(file: str, lines: int, header: list, unit_angle: str, work: Worksite) -> Worksite:
    """
    Reads an opk file to transform it into a Workside object.

    Args:
        file (str): Path to the worksite.
        lines (list): Interval of lines taken into account, [i, j] if i or j is None = :.
                          e.g. [1, None] = [1:]
        header (list): List of column type file.
        unit_angle (str): unit of angle 'd' degrees, 'r' radian.
        work (Worksite): Worksite to add shot

    Returns:
        Worksite: The worksite.
    """
    try:
        with open(file, 'r', encoding="utf-8") as file_opk:
            for item_opk in file_opk.readlines()[lines[0]:lines[1]]:
                item_shot = item_opk.split()
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
                              unit_angle)
            file_opk.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!"
                                f"Your os is {platform.system()}."
                                "For Windows path is \\,"
                                " for Linux and MacOS (Darwin) is / .") from e

    return work
