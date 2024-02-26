"""
Worksite data class module.
"""
import numpy as np
from src.datastruct.workdata import Workdata
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from src.transform_world_image.transform_worksite.space_resection import SpaceResection
from src.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


class Worksite(Workdata):
    """
    Worksite class, class main of the tools.

    Args:
        name (str): Name of the worksite.
    """
    def __init__(self, name: str) -> None:
        Workdata.__init__(self, name)

    def calculate_barycentre(self) -> np.ndarray:
        """
        Calculate barycentre of the worksite.

        Returns:
            np.array: The barycentre [X, Y, Z].
        """
        size = len(self.shots)
        pos = np.zeros((size, 3))
        i = 0
        for shot in self.shots.values():
            pos[i, :] = shot.pos_shot
            i += 1
        return np.mean(pos, axis=0)

    def calculate_world_to_image_gcp(self, lcode: list) -> None:
        """
        Calculates the position of gcps which corresponds to the data code
        in the images they appear in.

        Args:
            lcode (list): gcp code.
        """
        if self.gcps and self.ground_img_pts:
            for name_gcp, gcp in self.gcps.items():
                if gcp.code in lcode or lcode == []:
                    try:
                        list_shots = self.ground_img_pts[name_gcp]
                        for name_shot in list_shots:
                            shot = self.shots[name_shot]
                            cam = self.cameras[shot.name_cam]
                            coor_img = WorldImageShot(shot, cam).world_to_image(gcp.coor,
                                                                                self.type_z_data,
                                                                                self.type_z_shot)
                            self.shots[name_shot].gcps[name_gcp] = coor_img
                    except KeyError:
                        print(f"Warning: id point {name_gcp} is present "
                              "in gcp but not in image control points.")
                        continue

    # pylint: disable-next=too-many-locals too-many-branches
    def calculate_init_image_world(self, type_point: str = "co_point",
                                   control_type: list = None) -> None:
        """
        Calculates the ground position of connecting point by intersection with
        the most distance between two shots or ground image point.

        Args:
            type_point (str): "co_point" or "ground_img_pt" depending on what you want to calculate.
            control_type (list): type controle for gcp.
        """
        if control_type is None:
            control_type = []

        check = False
        if type_point == "co_point":
            points = self.co_points
            check = bool(points)
            check_gcp = False

        if type_point == "ground_img_pt":
            points = self.ground_img_pts
            check = bool(points)
            check_gcp = True

        if check:
            for name_p, item_p in points.items():  # Loop on points
                if check_gcp and control_type != [] and self.gcps[name_p].code not in control_type:
                    continue
                if len(item_p) == 1:
                    continue
                shot1 = ""
                shot2 = ""
                dist = 0
                list_shot1 = item_p.copy()
                list_shot2 = list_shot1.copy()
                _ = list_shot1.pop(-1)
                for name_shot1 in list_shot1:  # Double loop on shots where see the point
                    _ = list_shot2.pop(0)
                    for name_shot2 in list_shot2:
                        pos_shot1 = self.shots[name_shot1].pos_shot
                        pos_shot2 = self.shots[name_shot2].pos_shot
                        new_dist = np.sqrt(np.sum((pos_shot1 - pos_shot2)**2))
                        if new_dist > dist:
                            dist = new_dist
                            shot1 = name_shot1
                            shot2 = name_shot2
                coor = self.eucli_intersection_2p(name_p, self.shots[shot1], self.shots[shot2])
                if type_point == "co_point":
                    self.co_pts_world[name_p] = coor
                if type_point == "ground_img_pt":
                    self.img_pts_world[name_p] = coor
        else:
            print(f"There isn't {type_point} or bad spelling co_point / ground_img_pt.")

    # pylint: disable-next=too-many-locals
    def eucli_intersection_2p(self, name_point: str, shot1: Shot, shot2: Shot) -> np.ndarray:
        """
        Calculates the euclidien position of a point from two shots.

        Args:
            name_point (str): Name of copoint to calcule coordinate.
            shot1 (Shot): Frist shot.
            shot2 (Shot): Second shot.

        Returns:
            np.array: Euclidien coordinate of the copoint.
        """
        if name_point in list(shot1.co_points):
            p_img1 = shot1.co_points[name_point]
            p_img2 = shot2.co_points[name_point]
        else:
            p_img1 = shot1.ground_img_pts[name_point]
            p_img2 = shot2.ground_img_pts[name_point]

        cam1 = self.cameras[shot1.name_cam]
        cam2 = self.cameras[shot2.name_cam]
        bary = (shot1.pos_shot + shot2.pos_shot)/2
        projeucli = EuclideanProj(bary[0], bary[1])
        mat_eucli1 = projeucli.mat_to_mat_eucli(shot1.pos_shot[0], shot1.pos_shot[1], shot1.mat_rot)
        mat_eucli2 = projeucli.mat_to_mat_eucli(shot2.pos_shot[0], shot2.pos_shot[1], shot2.mat_rot)
        pos_eucli1 = conv_z_shot_to_z_data(shot1, self.type_z_shot, self.type_z_data)
        pos_eucli2 = conv_z_shot_to_z_data(shot2, self.type_z_shot, self.type_z_data)
        pos_eucli1 = projeucli.world_to_euclidean(pos_eucli1)
        pos_eucli2 = projeucli.world_to_euclidean(pos_eucli2)
        base = pos_eucli2 - pos_eucli1
        vect1 = mat_eucli1.T @ ImageWorldShot(shot1, cam1).image_to_bundle(p_img1)
        vect2 = mat_eucli2.T @ ImageWorldShot(shot2, cam2).image_to_bundle(p_img2)
        norme_v1 = vect1 @ vect1
        norme_v2 = vect2 @ vect2
        v1_v2 = vect1 @ vect2
        b_v1 = base @ vect1
        b_v2 = base @ vect2
        num1 = b_v2*v1_v2 - b_v1*norme_v2
        num2 = b_v2*norme_v1 - b_v1*v1_v2
        denum = v1_v2**2 - norme_v1*norme_v2
        p1_world = pos_eucli1 + ((num1)/(denum))*vect1
        p2_world = pos_eucli2 + ((num2)/(denum))*vect2
        pt_world = (p1_world + p2_world) / 2
        return projeucli.euclidean_to_world(pt_world)

    def shootings_position(self, add_pixel: tuple = (0, 0)) -> None:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.
        For all shot with a variation pixel.

        Args:
            add_pixel (tuple): Factor (column, line) added on observable point.
        """
        for key_shot, item_shot in self.shots.items():
            cam = self.cameras[item_shot.name_cam]
            self.shots[key_shot] = SpaceResection(item_shot, cam,
                                                  self.type_z_data,
                                                  self.type_z_shot).space_resection(add_pixel)
