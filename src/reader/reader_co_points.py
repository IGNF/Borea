"""
Script to read connecting point mes.
"""
from pathlib import Path, PureWindowsPath
from src.datastruct.worksite import Worksite


def read_co_points(files: list, work: Worksite) -> None:
    """
    Read all files of connecting points.

    Agrs:
        files (list): Path list of files connecting points.
        work (Worksite): Worksite which needs connecting points.
    """
    for file in files:
        try:
            with open(Path(PureWindowsPath(file)), 'r', encoding="utf-8") as file_co_points:
                for copoint in file_co_points.readlines():
                    if copoint != '\n':
                        name_point, name_shot, x, y = copoint.split()
                        work.add_copoint(name_point, name_shot, float(x), float(y))
                file_co_points.close()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
    work.check_cop = True
