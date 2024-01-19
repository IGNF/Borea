"""
Script to read camera file txt or xml
"""
import xml.etree.ElementTree as ET
from src.datastruct.worksite import Worksite


def read_camera(files: list, work: Worksite) -> None:
    """
    Manage file in list files to read

    Args:
        files (list): path list of files cameras
        work (Worksite): Worksite which needs camera data
    """
    for file in files:
        ext = file.split('.')[-1].lower()
        if ext == 'xml':
            camera_xml(file, work)
        if ext == 'txt':
            camera_txt(file, work)


def camera_xml(file: str, work: Worksite) -> None:
    """
    Read xml file camera

    Args:
        files (list): path list of files cameras
        work (Worksite): Worksite which needs camera data
    """
    try:
        projet = ET.parse(file).getroot()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!") from e

    try:
        focal = projet.find("focal").find("pt3d")
        name_cam = projet.find("name").text.strip()
        work.add_camera(name_cam,
                        float(focal.find("x").text.strip()),
                        float(focal.find("y").text.strip()),
                        float(focal.find("z").text.strip()))
    except AttributeError as e:
        raise AttributeError("Your camera.xml is badly parameterized, must include a <name> tag"
                             " for the camera name, a <focal> tag, which includes a <pt3d> tag"
                             " which includes 3 <x>, <y>, <z> tags") from e

    try:
        dim_image = projet.find("usefull-frame").find("rect")
        work.cameras[name_cam].add_dim_image(float(dim_image.find("w").text.strip()),
                                             float(dim_image.find("h").text.strip()))
    except AttributeError as e:
        pass

def camera_txt(file: str, work: Worksite) -> None:
    """
    Read txt file camera

    Args:
        files (list): path list of files cameras
        work (Worksite): Worksite which needs camera data
    """
    try:
        with open(file, 'r', encoding="utf-8") as file_cam:
            # Recover the info line and take name camera
            name_cam, o_info = file_cam.readlines()[0].split(" / ")
            # Take information ppa focal
            o_info = o_info.split(" : ")[-1].split(" ")
            # Add to worksite
            work.add_camera(name_cam, float(o_info[2]), float(o_info[5]), float(o_info[8]))
            file_cam.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
