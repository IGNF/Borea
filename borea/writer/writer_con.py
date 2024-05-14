"""
Photogrammetry worksite to writing in rpc.
"""
import os
from pathlib import Path, PureWindowsPath
from borea.worksite.worksite import Worksite
from borea.geodesy.proj_engine import ProjEngine
from borea.format.conl import Conl
from borea.geodesy.projectionlist.search_proj import search_info


def write(name: str, folder_con: str, param_con: dict, work: Worksite) -> None:
    """
    Converte Worksite in Conical class and save it in CON.

    Args:
        name (str): Name of file begin.
        folder_con (str): Path of folder to registration file .CON.
        param_con (dict): None.
        work (Worksite): The site to be recorded.
    """
    _, _ = name, param_con
    geoview_proj = search_info("EPSG", str(ProjEngine().epsg), "GEOVIEW")

    for name_shot, shot in work.shots.items():
        cam = work.cameras[shot.name_cam]
        path_conical = os.path.join(Path(PureWindowsPath(folder_con)), f"{name_shot}.CON")

        Conl(shot, cam, geoview_proj).save_conl(path_conical)
