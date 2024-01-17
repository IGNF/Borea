"""
Photogrammetry site file writer module
"""
import importlib
from src.datastruct.worksite import Worksite


def manager_reader(writer: str, pathreturn: str, work: Worksite) -> None:
    """
    Photogrammetric site file writing function

    Args:
        writer (str): output file format
        pathreturn (str): Path to save the project
    """
    try:
        my_module = importlib.import_module("src.writer.writer_" + writer.lower())
        work = my_module.write(pathreturn, work)
    except ModuleNotFoundError as e:
        raise ValueError(f"{writer} file is not taken into account !!!") from e
