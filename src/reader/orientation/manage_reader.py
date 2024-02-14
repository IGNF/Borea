"""
Photogrammetry site file reader module.
"""
import importlib
from src.datastruct.worksite import Worksite
from src.utils.check_header import check_header_file


def reader_orientation(file: str, line_take: list, header: list) -> Worksite:
    """
    Photogrammetric site file reading function.

    Args:
        file (str): Path to the worksite.
        line_take (list): Interval of lines taken into account, [i, j] if i or j is None = :.
                          e.g. [1, None] = [1:]
        header (list): List of column type file.

    Returns:
        Worksite: The worksite.
    """
    # Attention multiple file management orientation
    # Attention management of files with the same extension but different formats
    splitpath = file.split('/')
    if len(splitpath) == 1:
        splitpath = file.split('\\')

    name_work, ext = splitpath[-1].split(".")

    header, type_z, type_angle = check_header_file(header)

    work = Worksite(name_work)
    try:
        my_module = importlib.import_module("src.reader.orientation.reader_" + ext.lower())
        work = my_module.read(file, line_take, header, type_angle, work)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"{ext} file is not taken into account !!!") from e

    work.type_z_shot = type_z
    work.type_angle = type_angle
    return work
