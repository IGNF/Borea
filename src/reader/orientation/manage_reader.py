"""
Photogrammetry site file reader module.
"""
import importlib
from src.datastruct.worksite import Worksite


def reader_orientation(file: str, skip: int) -> Worksite:
    """
    Photogrammetric site file reading function.

    Args:
        file (str): Path to the worksite.
        skip (int): Number of lines to be skipped before reading the file, Default=None.

    Returns:
        Worksite: The worksite.
    """
    # Attention multiple file management orientation
    # Attention management of files with the same extension but different formats
    splitpath = file.split('/')
    if len(splitpath) == 1:
        splitpath = file.split('\\')

    name_work, ext = splitpath[-1].split(".")

    work = Worksite(name_work)
    try:
        my_module = importlib.import_module("src.reader.orientation.reader_" + ext.lower())
        work = my_module.read(file, skip, work)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"{ext} file is not taken into account !!!") from e

    work.type_z = "al"
    return work
