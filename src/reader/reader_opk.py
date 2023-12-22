"""
A script to read opk file
"""
import numpy as np
from src.worksite import Worksite


def read(file: str, skip: int) -> Worksite:
    """
    Reads an opk file to transform it into a Workside object

    Args:
        file (str): Path to the worksite.
        skip (int): Number of lines to be skipped before reading the file, Default=None.

    Returns:
        Worksite: The worksite
    """
    if skip is None:
        skip = 1

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
