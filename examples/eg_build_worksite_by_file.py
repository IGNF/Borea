"""
Example to build worksite with file (main ligne 124)
"""
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)[:-8], "implements/"))
from src.worksite.worksite import Worksite # type: ignore
from src.reader.orientation.manage_reader import reader_orientation # type: ignore
from src.reader.reader_camera import read_camera # type: ignore
from src.reader.reader_point import read_file_pt # type: ignore


PATH_OPK = "./dataset/23FD1305_alt_test.OPK"
PATH_CAM = ["./dataset/Camera1.txt"]
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
PATH_CO_PT = "./dataset/liaisons_test.mes"
PATH_GCP2D = "./dataset/terrain_test.mes"
PATH_GCP2D0 = "./dataset/terrain_test0.mes"
PATH_GCP3D = "./dataset/GCP_test.app"


def worksite_opk() -> Worksite:
    # reader_orientation is a function that builds the main worksite class.
    # There are 2 parameters at the function: 1.path of the file to read   2.dictonary
    # The dictonary contains differents parameters to read the file and build the class
    # "header" : Type of each column in the site file, detail below 1.
    # "intervale" : [i,j] with i the first ligne to read and j the last line if [None, None] read all the file.
    ######## WARNING if the file has a header, either delete it or skip it.
    # "unit_angle" : unit of angle in the opk ('degree' or 'radian').
    # "linear_alteration" : True if data is corrected by linear alteration.
    # "order_axe" : order of angle axe to build rotation matrix, frequently 'opk', rarely 'pok', you can make all form.
    work = reader_orientation(PATH_OPK, {"order_axe": 'opk',
                                         "interval": [2, None],
                                         "header": list("NXYZOPKC"),
                                         "unit_angle": "degree",
                                         "linear_alteration": True})
    
    # Add camera -> read_camera(list[str], worksite) take list of path camera if there are many camera on your worksite.
    read_camera(PATH_CAM, work)

    # Settup projection of your worksite
    # work.set_proj(code_epsg: int, path_geoid: list[str]) 
    # path geoid is a list of path if there are many geoid of the worksite or you can make just name of the file if they're in the right place for pyproj (*usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*)
    # The geoid is used to perform the height-altitude transformation or the inverse if the data are not in the same unit (if they are in the same unit, you can use None instead).
    work.set_proj(2154, PATH_GEOID)

    # Settup dtm of the worksite
    # work.set_dtm(path_dtm: str, unit_dtm: str)
    # Used for de-correcting linear fading data and for image-to-world transformations with least-square processing and space resection.
    work.set_dtm(PATH_DTM, "height")

    # Settup euclidean system of shots for transformation
    # work.set_param_shot(approx_system: bool) True if you want to use approximate euclidean system but it is less precise than the normal.
    work.set_param_shot(False)
    
    return work


def worksite_without_shot() -> Worksite:
    # Initialization of worksite with just a name
    work = Worksite("Example") 

    # Add camera -> read_camera(list[str], worksite) take list of path camera if there are many camera on your worksite.
    read_camera(PATH_CAM, work)

    # Settup projection of your worksite
    # work.set_proj(code_epsg: int, path_geoid: list[str]) 
    # path geoid is a list of path if there are many geoid of the worksite or you can make just name of the file if they're in the right place for pyproj (*usr/share/proj* or *env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj*)
    # The geoid is used to perform the height-altitude transformation or the inverse if the data are not in the same unit (if they are in the same unit, you can use None instead).
    work.set_proj(2154, PATH_GEOID)

    # Settup dtm of the worksite
    # work.set_dtm(path_dtm: str, unit_dtm: str)
    # Used for de-correcting linear fading data and for image-to-world transformations with least-square processing and space resection.
    work.set_dtm(PATH_DTM, "height")

    return work


def worksite_add_co_points(work: Worksite) -> Worksite:
    # Add connecting to the worksite
    # read_file_pt(path_file: str, header: list(str), type_point: str, work: Worksite)
    # "header" : Type of each column in the site file, detail below 2.
    read_file_pt(PATH_CO_PT, list("PNXY"), "co_point", work)

    return work


def worksite_add_gcp2d(work: Worksite) -> Worksite:
    # Add connecting to the worksite
    # read_file_pt(path_file: str, header: list(str), type_point: str, work: Worksite)
    # "header" : Type of each column in the site file, detail below 2.
    read_file_pt(PATH_GCP2D, list("PNXY"), "gcp2d", work)

    return work


def worksite_add_gcp3d(work: Worksite) -> Worksite:
    # Add connecting to the worksite
    # read_file_pt(path_file: str, header: list(str), type_point: str, work: Worksite)
    # "header" : Type of each column in the site file, detail below 2.
    read_file_pt(PATH_GCP3D, list("PTXYZ"), "gcp3d", work)

    # Settup z unit of gcp terrain "altitude" or "height"
    work.set_type_z_data("height")

    return work


def worksite_add_gcp2d0(work: Worksite) -> Worksite:
    # Add connecting to the worksite
    # read_file_pt(path_file: str, header: list(str), type_point: str, work: Worksite)
    # "header" : Type of each column in the site file, detail below 2.
    read_file_pt(PATH_GCP2D0, list("PNXY"), "gcp2d", work)

    return work


if __name__ == "__main__":
    # Build Worksite with an opk file
    work = worksite_opk()

    # Add connecting point (co_point)
    work = worksite_add_co_points(work)

    # Add ground control point image (gcp2d)
    work = worksite_add_gcp2d(work)

    # Add ground control point terrain (gcp3d)
    work = worksite_add_gcp3d(work)

    # Add ground control point image with 0 in coordinates (gcp2d)
    # Used in the world to image function to find out in which image the points are located.
    work = worksite_opk()
    work = worksite_add_gcp2d0(work)

    # Build Worksite without shot
    work = worksite_without_shot()

"""
####### detail letter in header opk ######## 1

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


####### detail letter in header file point ######## 2

S: to ignore the column
P: name of point
N: name of shot
T: Type of gcp to control.
X: coordinate x (column) in the image
Y: coordinate y (line) in the image
X: coordinate x of the shot position
Y: coordinate y of the shot position
Z: coordinate z of the shot position
"""