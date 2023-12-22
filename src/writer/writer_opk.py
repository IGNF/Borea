"""
Photogrammetry site file reader module
"""
from src.datastruct.worksite import Worksite


def write(path: str, work: Worksite) -> None:
    """
    Write function, to save a photogrammetric site in .opk format

    Args:
        path (str): Path of registration file.
        work (Worksite): The site to be recorded.
    """
    path = path + work.name + ".opk"

    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write("NOM X   Y   Z   O   P   K   CAMERA")
            for shot in work.shots:
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
        raise ValueError("The path doesn't exist !!!") from e