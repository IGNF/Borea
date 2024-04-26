"""
Photogrammetry worksite to writing in opk.
"""
import os
from pathlib import Path, PureWindowsPath
import numpy as np
from borea.worksite.worksite import Worksite
from borea.utils.check.check_args_opk import check_header_file


def write(name_opk: str, path_opk: str, args: dict, work: Worksite) -> None:
    """
    Write function, to save a photogrammetric site in .opk format.

    Args:
        name_opk (str): Name of the file writing.
        path_opk (str): Path of folder to registration file .opk.
        args (dict): Information for writing an opk file.
                     keys:
                     "order_axe" (str): Order of rotation matrix axes,
                     "header" (list): List of column type file.
                     "unit_angle" (str): Unit of angle 'degree' or 'radian'.
                     "linear_alteration" (bool): True if data corrected by
                     linear alteration.
        work (Worksite): The site to be recorded.
    """
    path_opk = os.path.join(Path(PureWindowsPath(path_opk)), f"{name_opk}.opk")

    if args["header"]:
        header, type_z = check_header_file(args["header"])
    else:
        header = ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
        type_z = work.type_z_shot

    if "S" in header:
        raise ValueError("Letter S doesn't existe in writing header opk.")

    work.set_unit_shot(type_z, args["unit_angle"], args["linear_alteration"], args["order_axe"])

    header_file = ""
    for i in header:
        header_file += i + "   "

    try:
        with open(path_opk, "w", encoding="utf-8") as file:
            file.write(header_file)
            file.write("\n")
            keys = np.sort(list(work.shots))
            line_writing = ""
            for k in keys:
                shot = work.shots[k]
                dict_letter = {"N": shot.name_shot,
                               "X": str(shot.pos_shot[0]),
                               "Y": str(shot.pos_shot[1]),
                               "Z": str(shot.pos_shot[2]),
                               "O": str(shot.ori_shot[0]),
                               "P": str(shot.ori_shot[1]),
                               "K": str(shot.ori_shot[2]),
                               "C": shot.name_cam}
                for i in range(8):
                    line_writing += dict_letter[header[i]]
                    if i != 7:
                        line_writing += "   "
                    else:
                        line_writing += "\n"

            file.write(line_writing)
        file.close()
    except FileNotFoundError as e:
        raise ValueError("The path doesn't exist !!!", e) from e
