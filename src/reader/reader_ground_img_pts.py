"""
Script to read ground points in image .mes.
"""
from pathlib import Path, PureWindowsPath
from src.worksite.worksite import Worksite


def read_ground_image_points(files: list, work: Worksite) -> None:
    """
    Read all files of connecting points.

    Agrs:
        files (list): Path list of files connecting points.
        work (Worksite): Worksite which needs connecting points.
    """
    for file in files:
        try:
            with open(Path(PureWindowsPath(file)), 'r', encoding="utf-8") as file_gipoints:
                for gipoint in file_gipoints.readlines():
                    if gipoint != '\n':
                        name_point, name_shot, x, y = gipoint.split()
                        work.add_ground_img_pt(name_point, name_shot, float(x), float(y))
                file_gipoints.close()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
    work.check_gip = True
