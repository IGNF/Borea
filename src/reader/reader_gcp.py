"""
Script to read GCP app
"""
import numpy as np
from src.datastruct.worksite import Worksite


def read_gcp(files: list, work: Worksite) -> None:
    """
    Read all files gcp

    Agrs:
        files (list): path list of files gcp
        work (Worksite): Worksite which needs gcp
    """
    for file in files:
        with open(file, 'r', encoding="utf-8") as file_gcp:
            for gcp in file_gcp.readlines():
                if gcp != '\n':
                    name_gcp, code_gcp, x, y, z = gcp.split()
                    work.add_gcp(name_gcp, int(code_gcp), np.array([float(x), float(y), float(z)]))
