"""
Module to conversion z for WorldImageShot and ImageWorldShot
"""
from typing import Union
import numpy as np
from src.datastruct.shot import Shot
from src.geodesy.proj_engine import ProjEngine


def conv_z_shot_to_z_data(shot: Shot, type_z_shot: str, type_z_data: str,
                          nonadir: bool = True) -> float:
    """
    Convert type z shot to type z data.

    Args:
        type_z_shot (str): Shot type z "altitude" or "height".
        type_z_data (str): Data type z "altitude" or "height".
        nonadir (bool): To calculate nadir no take linear alteration.
    """
    new_z = shot.pos_shot[0]

    if nonadir and shot.linear_alteration:
        new_z = shot.get_z_remove_scale_factor()

    if type_z_shot != type_z_data:
        if type_z_shot == "height":
            new_z = ProjEngine().tranform_altitude(shot.pos_shot[0],
                                                   shot.pos_shot[1],
                                                   new_z)
        else:
            new_z = ProjEngine().tranform_height(shot.pos_shot[0],
                                                 shot.pos_shot[1],
                                                 new_z)

    return new_z


def conv_output_z_type(x: Union[float, np.ndarray],
                       y: Union[float, np.ndarray],
                       z: Union[float, np.ndarray],
                       type_z_input: str, type_z_output: str) -> tuple:
    """
    Convert type z to the output given.

    Args:
        x (Union[float, np.ndarray]): Coordinate X
        y (Union[float, np.ndarray]): Coordinate Y
        z (Union[float, np.ndarray]): Coordinate Z
        type_z_input (str): Z type in input "height" or "altitude"
        type_z_output (str): Z type in output "height" or "altitude"

    Returns:
        tuple: Coodinate x, y, z
    """
    new_z = z
    if type_z_input != type_z_output:
        if type_z_input == "height":
            new_z = ProjEngine().tranform_altitude(x, y, z)
        else:
            new_z = ProjEngine().tranform_height(x, y, z)

    return x, y, new_z
