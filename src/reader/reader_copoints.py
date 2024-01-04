"""
Script to read connecting point mes
"""
from src.datastruct.worksite import Worksite


def read_copoints(files: list, work: Worksite) -> None:
    """
    Read all files of connecting points

    Agrs:
        files (list): path list of files connecting points
        work (Worksite): Worksite which needs connecting points
    """
    for file in files:
        with open(file, 'r', encoding="utf-8") as file_copoints:
            for copoint in file_copoints.readlines():
                if copoint != '\n':
                    name_point, name_shot, x, y = copoint.split()
                    work.add_copoint(name_point, name_shot, float(x), float(y))
            file_copoints.close()
    work.check_cop = True
