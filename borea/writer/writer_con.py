"""
Photogrammetry worksite to writing in rpc.
"""
import os
from borea.utils.check.check_path import check_path
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

    if work.epsg_output:
        epsg_output = ProjEngine().epsg_output
    else:
        epsg_output = ProjEngine().epsg[0]

    work.set_unit_output(type_z="altitude", linear_alteration=True)
    geoview_proj = search_info("EPSG", str(epsg_output), "GEOVIEW")

    for name_shot, shot in work.shots.items():
        cam = work.cameras[shot.name_cam]
        path_conical = os.path.join(check_path(folder_con), f"{name_shot}.CON")

        Conl(shot, cam, geoview_proj).save_conl(path_conical)
