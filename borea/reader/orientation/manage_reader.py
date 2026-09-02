"""
Photogrammetry site file reader module.
"""
import importlib
import re
from borea.utils.check.check_path import check_path
from borea.worksite.worksite import Worksite


def reader_orientation(path: str, args: dict) -> Worksite:
    """
    Photogrammetric site file reading function.

    Args:
        path (str): Path to the worksite.
        args (dict): Other information for reading the file.

    Returns:
        Worksite: The worksite.
    """
    # Attention multiple file management orientation
    # Attention management of files with the same extension but different formats
    path = check_path(path)
    name_work = path.stem
    if bool(re.search(r'[.^$*+?{}\[\]\\|()]', name_work)):
        name_work = path.parent.name
    ext = path.suffix[1:]

    work = Worksite(name_work)
    try:
        my_module = importlib.import_module("borea.reader.orientation.reader_" + ext.lower())
        work = my_module.read(path, args, work)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"{ext} file is not taken into account !!!") from e

    return work
