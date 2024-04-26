"""
Script to read camera file txt or xml.
"""
from pathlib import Path, PureWindowsPath
from borea.datastruct.camera import Camera
from borea.worksite.worksite import Worksite


def read_camera(files: list, work: Worksite) -> None:
    """
    Manage file in list files to read.

    Args:
        files (list): Path list of files cameras.
        work (Worksite): Worksite which needs camera data.
    """
    for file in files:
        camera_txt(Path(PureWindowsPath(file)), work)


def camera_txt(file: Path, work: Worksite) -> None:
    """
    Read txt file camera.

    Args:
        files (Path): Path list of files cameras.
        work (Worksite): Worksite which needs camera data.
    """
    dict_info = {}
    try:
        with open(file, 'r', encoding="utf-8") as file_cam:
            for info_cam in file_cam.readlines():
                if info_cam != '\n' and info_cam[0] != '#':
                    # Camera info retrieval
                    info_name, info_data = info_cam.split(" = ")
                    dict_info[info_name.lower()] = info_data[:-1]

            file_cam.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!") from e

    # Create Camera
    cam = Camera(dict_info["name"])

    for name_attr, item in dict_info.items():
        if name_attr != "name":
            type_item = int if name_attr in ["width", "height"] else float
            try:
                setattr(cam, name_attr.lower(), type_item(item))
            except ValueError:
                continue
    work.cameras[dict_info["name"]] = cam
