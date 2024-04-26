"""
Module to conversion z for WorldImageShot and ImageWorldShot
"""
import numpy as np
from borea.datastruct.shot import Shot
from borea.geodesy.proj_engine import ProjEngine


def conv_z_shot_to_z_data(shot: Shot, type_z_shot: str, type_z_data: str,
                          nonadir: bool = True, approx: bool = False) -> np.ndarray:
    """
    Convert type z shot to type z data. The Z of the object is NOT modified.

    Args:
        shot (Shot): Shot to process.
        type_z_shot (str): Shot type z "altitude" or "height".
        type_z_data (str): Data type z "altitude" or "height".
        nonadir (bool): To calculate nadir no take linear alteration.

    Returns:
        np.array: Shot position coordinate with type z asking.
    """
    pos_shot = shot.pos_shot.copy()

    if nonadir and shot.linear_alteration and not approx:
        new_z = shot.get_z_remove_scale_factor()
        pos_shot[2] = new_z

    if type_z_shot != type_z_data:
        if type_z_shot == "height":
            new_z = ProjEngine().tranform_altitude(pos_shot)
        else:
            new_z = ProjEngine().tranform_height(pos_shot)
        pos_shot[2] = new_z

    return pos_shot


def conv_output_z_type(coor: np.ndarray, type_z_input: str, type_z_output: str) -> np.ndarray:
    """
    Convert type z to the output given.

    Args:
        coor (Union[float, np.ndarray]): Coordinate [X, Y, Z].
        type_z_input (str): Z type in input "height" or "altitude".
        type_z_output (str): Z type in output "height" or "altitude".

    Returns:
        np.array: Coodinate x, y, z.
    """
    new_z = coor[2]
    if type_z_input != type_z_output:
        if type_z_input == "height":
            new_z = ProjEngine().tranform_altitude(coor)
        else:
            new_z = ProjEngine().tranform_height(coor)

    return np.array([coor[0], coor[1], new_z])
