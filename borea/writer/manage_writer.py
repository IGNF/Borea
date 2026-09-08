"""
Photogrammetry site file writer module.
"""
import importlib
from borea.worksite.worksite import Worksite


def manager_writer(writer: str, name: str, path_return: str, args: dict, work: Worksite) -> None:
    """
    Photogrammetric site file writing function.

    Args:
        writer (str): Output file format.
        name (str): Name of the file.
        path_return (str): Path to save the project.
        args (dict): Other information for writing the file.
        work (Worksite): The site to be recorded.
    """
    try:
        my_module = importlib.import_module("borea.writer.writer_" + writer.lower())
        work = my_module.write(name, path_return, args, work)
    except ModuleNotFoundError as e:
        raise ValueError(f"{writer} file is not taken into account !!!") from e
