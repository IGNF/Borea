"""
Script to read GCP app.
"""
import numpy as np
from src.datastruct.worksite import Worksite


def read_gcp(files: list, work: Worksite) -> None:
    """
    Read all files gcp.

    Agrs:
        files (list): Path list of files gcp.
        work (Worksite): Worksite which needs gcp.
    """
    for file in files:
        try:
            with open(file, 'r', encoding="utf-8") as file_gcp:
                for gcp in file_gcp.readlines():
                    if gcp != '\n':
                        name_gcp, code_gcp, x, y, z = gcp.split()
                        work.add_gcp(name_gcp, int(code_gcp), np.array([float(x),
                                                                        float(y),
                                                                        float(z)]))
                file_gcp.close()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
    work.check_gcp = True
