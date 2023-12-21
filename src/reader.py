"""
Photogrammetry site file reader module
"""
import numpy as np
from src.worksite import Worksite


def from_file(file: str, skip: int = None) -> Worksite:
    """
    Photogrammetric site file reading function

    Args:
        file (str): Path to the worksite.
        skip (int): Number of lines to be skipped before reading the file, Default=None.

    Returns:
        Worksite: The worksite
    """
    ext = file.split(".")[-1]
    if ext == "opk":
        if skip is None:
            skip = 1
        work = from_opk(file, skip)
    else:
        print("Input file not taken into account")
    return work


def from_opk(file: str, skip: int = 1) -> Worksite:
    """
    Reads an opk file to transform it into a Workside object

    Args:
        file (str): Path to the worksite.
        skip (int): Number of lines to be skipped before reading the file, Default=None.

    Returns:
        Worksite: The worksite
    """
    # Job name retrieval
    name_work = file.split('/')[-1]
    name_work = name_work.split('.')[0]

    # Create worksite
    work = Worksite(name_work)

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
    except FileNotFoundError as e:
        raise ValueError("The path to the .opk file is incorrect !!!") from e

    return work
