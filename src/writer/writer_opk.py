"""
Photogrammetry site file reader module.
"""
import os
import numpy as np
from src.datastruct.worksite import Worksite


def write(path_opk: str, work: Worksite) -> None:
    """
    Write function, to save a photogrammetric site in .opk format.

    Args:
        path_opk (str): Path of registration file .opk.
        work (Worksite): The site to be recorded.
    """
    path_opk = os.path.join(path_opk, f"{work.name}.opk")

    try:
        with open(path_opk, "w", encoding="utf-8") as file:
            file.write("NOM X   Y   Z   O   P   K   CAMERA")
            keys = np.sort(list(work.shots))
            for k in keys:
                shot = work.shots[k]
                file.write("\n")
                file.write(shot.name_shot + "   " +
                           str(shot.pos_shot[0]) + "   " +
                           str(shot.pos_shot[1]) + "   " +
                           str(shot.pos_shot[2]) + "   " +
                           str(shot.ori_shot[0]) + "   " +
                           str(shot.ori_shot[1]) + "   " +
                           str(shot.ori_shot[2]) + "   " +
                           shot.name_cam)
            file.close()
    except FileNotFoundError as e:
        raise ValueError("The path doesn't exist !!!", e) from e
