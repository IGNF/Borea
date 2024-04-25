"""
Photogrammetry site file writer module.
"""
import importlib
from src.worksite.worksite import Worksite


def manager_writer(writer: str, name: str, pathreturn: str, args: dict, work: Worksite) -> None:
    """
    Photogrammetric site file writing function.

    Args:
        writer (str): Output file format.
        name (str): Name of the file.
        pathreturn (str): Path to save the project.
        args (dict): Other information for writing the file.
        work (Worksite): The site to be recorded.
    """
    try:
        my_module = importlib.import_module("src.writer.writer_" + writer.lower())
        work = my_module.write(name, pathreturn, args, work)
    except ModuleNotFoundError as e:
        raise ValueError(f"{writer} file is not taken into account !!!") from e
