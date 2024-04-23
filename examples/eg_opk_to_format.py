"""
Example to use opk control in lib python (main line 22)
"""
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)[:-8], "implements/"))
from src.writer.manage_writer import manager_writer #type: ignore

from eg_build_worksite_by_file import worksite_opk


OUTPUT_PATH = "./implements/test/tmp"


def convert_opk_to_format(format: str, name: str, pathreturn: str, args: dict) -> None:
    # Build opk
    work = worksite_opk()

    # Convert in new format
    manager_writer(format, name, pathreturn, args, work)

if __name__ == "__main__":
    # Creation of folder
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Name of new file
    name = "New_file_test"

    # Path of the save folder 
    pathreturn = OUTPUT_PATH

    ############################
    # Convertion of format OPK #
    ############################
    format = "opk"

    # Parameters for good writing format
    args = {"header": list("NOPKCXYZ"),
            "unit_angle": "radian",
            "linear_alteration":True,
            "order_axe":'opk'}
    # header: Column type of opk
    # unit_angle: degree or radian
    # linear_alteration: True for data corrected and false for datat not corrected
    # order_axe: order of angle to build rotation matrix (opk, pok, ...)

    print(f"\nConvert worksite in OPK in path: {OUTPUT_PATH}{name}.OPK")
    convert_opk_to_format(format, name, pathreturn, args)


    ############################
    # Convertion of format RPC #
    ############################
    # It's a general format for QGIS (The file .RPC) 
    # the file just needs to be in the same folder as the image 
    # to be recognized by QGIS when the image is read, allowing it to be positioned in the system.
    format = "rpc"

    # Parameters for good writing format
    args = {"size_grid":100,
            "order":3,
            "fact_rpc":None}
    # size_grid: size of grid you want to use for the calculation
    # order: Order of RPC (Rational Polygone Coefficient) choices=[1, 2, 3]
    # fact_rpc: if there is no projection use a fact_rpc to replace in float or else put None

    print(f"\nConvert worksite in RPC in path: {OUTPUT_PATH}/name_shot_RPC.TXT")
    # The name parameter doesn't need to be filled in, as it will be ignored.
    convert_opk_to_format(format, None, pathreturn, args)


    ############################
    # Convertion of format CON #
    ############################
    # It's a general format for GEOVIEW IGN and other software.
    format = "con"

    print(f"\nConvert worksite in CON in path: {OUTPUT_PATH}/name_shot.CON")
    # The name parameter doesn't need to be filled in, as it will be ignored.
    # likewise args because you don't need any additional arguments to write the format.
    convert_opk_to_format(format, None, pathreturn, None)

"""
####### detail letter in header opk ########

S: to ignore the column
N: name of shot
X: coordinate x of the shot position
Y: coordinate y of the shot position
Z: coordinate z of the shot position in altitude
H: coordinate z of the shot position in height
O: omega rotation angle
P: phi rotation angle
K: kappa rotation angle
C: name of the camera
"""