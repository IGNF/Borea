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
    projet = ET.parse(file).getroot()
    focal = projet.find("focal").find("pt3d")
    work.add_camera(projet.find("name").text.strip(),
                    float(focal.find("x").text.strip()),
                    float(focal.find("y").text.strip()),
                    float(focal.find("z").text.strip()))


def camera_txt(file: str, work: Worksite) -> None:
    """
    Read txt file camera

    Args:
        files (list): path list of files cameras
        work (Worksite): Worksite which needs camera data
    """
    with open(file, 'r', encoding="utf-8") as file_cam:
        # Recover the info line and take name camera
        name_cam, o_info = file_cam.readlines()[0].split(" / ")
        # Take information ppa focal
        o_info = o_info.split(" : ")[-1].split(" ")
        # Add to worksite
        work.add_camera(name_cam, float(o_info[2]), float(o_info[5]), float(o_info[8]))
        file_cam.close()