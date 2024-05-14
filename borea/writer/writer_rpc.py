"""
Photogrammetry worksite to writing in rpc.
"""
import os
from pathlib import Path, PureWindowsPath
from borea.format.rpc import Rpc
from borea.worksite.worksite import Worksite
from borea.datastruct.dtm import Dtm


def write(name: str, folder_rpc: str, param_rpc: dict, work: Worksite) -> None:
    """
    Converte Worksite in RPC class and save it in txt.

    Args:
        name (str): Name of file begin.
        folder_rpc (str): Path of folder to registration file .txt.
        param_rpc (dict): Dictionary of parameters for rpc calculation.
        key;
        "size_grid"; size of the grip to calcule rpc.
        "order"; order of the polynome of the rpc.
        "fact_rpc"; rpc factor for world coordinate when src is not WGS84.
        work (Worksite): The site to be recorded.
    """
    _ = name
    keys = ["ERR_BIAS", "ERR_RAND", "LINE_OFF", "SAMP_OFF",
            "LAT_OFF", "LONG_OFF", "HEIGHT_OFF", "LINE_SCALE",
            "SAMP_SCALE", "LAT_SCALE", "LONG_SCALE",
            "HEIGHT_SCALE"]

    work.set_unit_shot(type_z=Dtm().type_dtm)

    for name_shot, shot in work.shots.items():
        cam = work.cameras[shot.name_cam]

        rpc = Rpc.from_shot(shot, cam, param_rpc,
                            {"unit_z_data": work.type_z_data, "unit_z_shot": work.type_z_shot})

        list_txt_rpc = [f"{key}: {rpc.param_rpc[key]}" for key in keys]

        for idx, val in enumerate(rpc.param_rpc["LINE_NUM_COEFF"]):
            list_txt_rpc += [f"LINE_NUM_COEFF_{idx + 1}: {val}"]

        for idx, val in enumerate(rpc.param_rpc["LINE_DEN_COEFF"]):
            list_txt_rpc += [f"LINE_DEN_COEFF_{idx + 1}: {val}"]

        for idx, val in enumerate(rpc.param_rpc["SAMP_NUM_COEFF"]):
            list_txt_rpc += [f"SAMP_NUM_COEFF_{idx + 1}: {val}"]

        for idx, val in enumerate(rpc.param_rpc["SAMP_DEN_COEFF"]):
            list_txt_rpc += [f"SAMP_DEN_COEFF_{idx + 1}: {val}"]

        path_rpc = os.path.join(Path(PureWindowsPath(folder_rpc)),
                                f"{name_shot}_RPC.TXT")
        Path(path_rpc).write_text("\n".join(list_txt_rpc), encoding="UTF-8")
