"""
Script to read camera file txt or xml.
"""
from src.datastruct.worksite import Worksite


def read_camera(files: list, work: Worksite) -> None:
    """
    Manage file in list files to read.

    Args:
        files (list): Path list of files cameras.
        work (Worksite): Worksite which needs camera data.
    """
    for file in files:
        camera_txt(file, work)


def camera_txt(file: str, work: Worksite) -> None:
    """
    Read txt file camera.

    Args:
        files (list): Path list of files cameras.
        work (Worksite): Worksite which needs camera data.
    """
    dict_info = {}
    try:
        with open(file, 'r', encoding="utf-8") as file_cam:
            for info_cam in file_cam.readlines():
                # Camera info retrieval
                info_name, info_data = info_cam.split(" = ")
                dict_info[info_name.lower()] = info_data[:-1]

            # Add to worksite
            work.add_camera(dict_info["name"],
                            float(dict_info["ppax"]),
                            float(dict_info["ppay"]),
                            float(dict_info["focal"]),
                            float(dict_info["width"]),
                            float(dict_info["height"]))
            file_cam.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
