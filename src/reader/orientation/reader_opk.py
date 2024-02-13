"""
A script to read opk file.
"""
import platform
import numpy as np
from src.datastruct.worksite import Worksite


def read(file: str, skip: int, work: Worksite) -> Worksite:
    """
    Reads an opk file to transform it into a Workside object.

    Args:
        file (str): Path to the worksite.
        skip (int): Number of lines to be skipped before reading the file.
        work (Worksite): Worksite to add shot

    Returns:
        Worksite: The worksite.
    """
    try:
        with open(file, 'r', encoding="utf-8") as file_opk:
            for item_opk in file_opk.readlines()[skip:]:
                item_shot = item_opk.split()
                work.add_shot(item_shot[0],
                              np.array([
                                   float(item_shot[1]),
                                   float(item_shot[2]),
                                   float(item_shot[3])], dtype=float),
                              np.array([
                                   float(item_shot[4]),
                                   float(item_shot[5]),
                                   float(item_shot[6])], dtype=float),
                              item_shot[7])
            file_opk.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!"
                                f"Your os is {platform.system()}."
                                "For Windows path is \\,"
                                " for Linux and MacOS (Darwin) is / .") from e

    return work
