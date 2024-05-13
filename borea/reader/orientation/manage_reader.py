"""
Photogrammetry site file reader module.
"""
import importlib
from pathlib import Path, PureWindowsPath
from borea.worksite.worksite import Worksite


def reader_orientation(file: str, args: dict) -> Worksite:
    """
    Photogrammetric site file reading function.

    Args:
        file (str): Path to the worksite.
        args (dict): Other information for reading the file.

    Returns:
        Worksite: The worksite.
    """
    # Attention multiple file management orientation
    # Attention management of files with the same extension but different formats
    file = Path(PureWindowsPath(file))
    name_work = file.stem
    ext = file.suffix[1:]

    work = Worksite(name_work)
    try:
        my_module = importlib.import_module("borea.reader.orientation.reader_" + ext.lower())
        work = my_module.read(file, args, work)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"{ext} file is not taken into account !!!") from e

    return work
