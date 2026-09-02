"""
A script to read micmac folder of xml image.
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from borea.worksite.worksite import Worksite


def read(path: Path, args: dict, work: Worksite) -> Worksite:
    """
    Reads an xml file to transform it into a Workside object.

    Args:
        path (Path): Regex to the path xml image worksite.
        args (dict): Information for reading an opk file.
                     keys:
                     "order_axe" (str): Order of rotation matrix axes of micmac,
                     "type_z" (str): Type of z height or altitude
                     "linear_alteration" (bool): True if data corrected by linear alteration.
        work (Worksite): Worksite to add shot.

    Returns:
        Worksite: The worksite.
    """
    # Check if file
    if os.path.isfile(path):
        work = read_ta(path, args, work)
    else:
        # Check regex
        try:
            re.compile(str(path))
        except re.error as error:
            raise SyntaxError(f"Le chemin ou le regex '{path}' n'est pas valide") from error

        work = read_images_xml(path, work)

    return work


def read_ta(path: Path, args: dict, work: Worksite) -> Worksite:
    """
    No implementation for TA.xml
    """
    raise ValueError("No implementation for TA.xml")


def read_images_xml(path: Path, work: Worksite) -> Worksite:
    """
    Reads an xml images to transform it into a Workside object.

    Args:
        path (Path): Regex to the path xml image worksite.
        work (Worksite): Worksite to add shot.

    Returns:
        Worksite: The worksite.
    """
    pattern = path.name
    regex = re.compile(pattern)
    path_dir = path.parent
    # browse all images
    for name_file in os.listdir(path_dir):
        if regex.match(name_file):
            tree = ET.parse(os.path.join(path_dir, name_file))
            root = tree.getroot()
            info_image = root.find("Data").find("CameraPose")
            # get name of image
            name_image = info_image.find("NameImage").text[1:-1]
            # get name of camera
            camera = info_image.find("NameInternalCalib").text[1:-1]
            # get position of image
            center = info_image.find("Center").text.split()
            xyz = np.array(convert_3val_to_float(center))
            # get rotation of image
            opk = info_image.find("WPK").text.strip().split(" ")
            opk = np.array(convert_3val_to_float(opk))
            # add shot
            work.add_shot(name_image, xyz, opk, camera, "degree",
                          True, "opk")

    return work


def convert_3val_to_float(values: list) -> tuple:
    """
    Converte a list of 3 str in 3 float

    Args:
        values (list): List of 3 str to convert in float

    Returns:
        tuple: 3 float of value
    """
    v1, v2, v3 = values
    return float(v1), float(v2), float(v3)
