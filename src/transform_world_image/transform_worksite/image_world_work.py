"""
Image world transformation module for Worksite
"""
import numpy as np
from src.datastruct.workdata import Workdata
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


class ImageWorldWork(Workdata):
    """
    Class to calculate image coordinate to world coordinate in worksite.

    Args:
        name (str): Name of the worksite.
    """

    # pylint: disable-next=unused-argument
    def copoints_position(self) -> None:
        """
        Calculates the field position of connection points using the least squares.

        Args:
            work (Worksite): The site on which you want to calculate the position of the copoints.
        """
        # pylint: disable-next=pointless-string-statement
        """
        #Initialization of world coordinate copoints
        work.calculate_init_image_world_copoints()

        for name_cop, coor_cop in work.cop_world.items():
            bool_cond = True
            it_count = 0
            while bool_cond:
                it_count +=1

                coord_i, coord_j, data = [], [], []
                v_res = np.zeros(2*len(work.copoints[name_cop]))
                for name_shot in work.copoints[name_cop]:
                    shot = work.shots[name_shot]
                    cam = work.cameras[shot.name_cam]
                    c_shot, l_shot = shot.world_to_image(coor_cop[0], coor_cop[1], coor_cop[2],
                                                        cam, work.projeucli)
                    coor_eucli = work.projeucli.world_to_euclidean(coor_cop[0],
                                                                coor_cop[1],
                                                                coor_cop[2])
                    vect_a = coor_eucli - shot.pos_shot_eucli
                    vect_u = shot.mat_rot_eucli @ vect_a

                    mat_v = np.zeros((2 * len(vect_u[0]), 3))
                    mat_v[::2, 0] = 1
                    mat_v[::2, 2] = -vect_u[0] / vect_u[2]
                    mat_v[1::2, 1] = 1
                    mat_v[1::2, 2] = -vect_u[1] / vect_u[2]

                    coord_i += [np.repeat(2 * pd_mes_pnt['index_mes'].to_numpy(), 6) +
                                np.tile([0, 0, 0, 1, 1, 1], len(c_shot))]
                    coord_j += [np.repeat(3 * pd_mes_pnt['index_pnt'].to_numpy(), 6) +
                                np.tile([0, 1, 2, 0, 1, 2], len(c_shot))]
                    data += [((np.tile(np.repeat(cam.focal / vect_u[2], 2), (3, 1)).T *
                            mat_v @ shot.mat_rot_eucli).flatten())]
                    v_res[2 * pd_mes_pnt['index_mes'].to_numpy()] =pd_mes_pnt["c"].to_numpy()-c_shot
                    v_res[2 * pd_mes_pnt['index_mes'].to_numpy() + 1] = pd_mes_pnt["l"].to_numpy() -
                    l_shot
"""

    def calculate_image_world_by_intersection(self, type_point: str = "co_point",
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
            for name_pt, list_shot in points.items():  # Loop on points
                if check_gcp and control_type != [] and self.gcps[name_pt].code not in control_type:
                    continue
                if len(list_shot) == 1:
                    continue

                coor = self.comput_inter_in_2_more_distant_shot(name_pt, list_shot)

                if type_point == "co_point":
                    self.co_pts_world[name_pt] = coor
                if type_point == "ground_img_pt":
                    self.img_pts_world[name_pt] = coor
        else:
            print(f"There isn't {type_point} or bad spelling co_point / ground_img_pt.")

    def comput_inter_in_2_more_distant_shot(self, name_pt: str, list_shot: list) -> np.ndarray:
        """
        Search for the two most distant images where the point is visible,
        to calculate the point's position.

        Args:
            name_pt (str): Name of the point.
            list_shot (list): List of name shot where the point is visible.
        
        Returns:
            np.ndarray: World coordinate of the point.
        """
        shot1 = ""
        shot2 = ""
        dist = 0
        list_shot1 = list_shot.copy()
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
        return self.intersection_pt_in_2shot(name_pt, self.shots[shot1], self.shots[shot2])

    def intersection_pt_in_2shot(self, name_point: str, shot1: Shot, shot2: Shot) -> np.ndarray:
        """
        Calculates the euclidien position of a point from two shots.

        Args:
            name_point (str): Name of copoint to calcule coordinate.
            shot1 (Shot): Frist shot.
            shot2 (Shot): Second shot.

        Returns:
            np.array: Euclidien coordinate of the copoint.
        """
        # Retrieve coordinates of points in the image.
        if name_point in list(shot1.co_points):
            p_img1 = shot1.co_points[name_point]
            p_img2 = shot2.co_points[name_point]
        else:
            p_img1 = shot1.ground_img_pts[name_point]
            p_img2 = shot2.ground_img_pts[name_point]

        # Setting up a Euclidean projection centered on the two images.
        bary = (shot1.pos_shot + shot2.pos_shot)/2
        projeucli = EuclideanProj(bary[0], bary[1])

        # Calculates data specific to Euclidean projection.
        mat_eucli1 = projeucli.mat_to_mat_eucli(shot1.pos_shot[0], shot1.pos_shot[1], shot1.mat_rot)
        mat_eucli2 = projeucli.mat_to_mat_eucli(shot2.pos_shot[0], shot2.pos_shot[1], shot2.mat_rot)
        pos_eucli1 = conv_z_shot_to_z_data(shot1, self.type_z_shot, self.type_z_data)
        pos_eucli2 = conv_z_shot_to_z_data(shot2, self.type_z_shot, self.type_z_data)
        pos_eucli1 = projeucli.world_to_euclidean(pos_eucli1)
        pos_eucli2 = projeucli.world_to_euclidean(pos_eucli2)

        # Calculates the director vectors of the point bundles in the Euclidean reference system.
        vect1 = mat_eucli1.T @ ImageWorldShot(shot1,
                                              self.cameras[shot1.name_cam]).image_to_bundle(p_img1)
        vect2 = mat_eucli2.T @ ImageWorldShot(shot2,
                                              self.cameras[shot2.name_cam]).image_to_bundle(p_img2)

        # Calculating the intersection of two lines
        pt_inter = self.intersection_line_3d(vect1, pos_eucli1, vect2, pos_eucli2)

        # Converting the point to the world system.
        pt_inter = projeucli.euclidean_to_world(pt_inter)
        return pt_inter

    def intersection_line_3d(self, vect1: np.ndarray, point1: np.ndarray,
                             vect2: np.ndarray, point2: np.ndarray) -> np.ndarray:
        """
        Calculation of the intersection point between 2 line in a 3d system.

        Args:
            vect1 (np.array): Directing vector of the first line.
            point1 (np.array): A point on the first line.
            vect2 (np.array): Directing vector of the second line.
            point2 (np.array): A point on the second line.

        Returns:
            np.array: The point of the intersection of the lines.
        """
        base = point2 - point1
        norme_v1 = vect1 @ vect1
        norme_v2 = vect2 @ vect2
        v1_v2 = vect1 @ vect2
        b_v1 = base @ vect1
        b_v2 = base @ vect2
        denum = v1_v2**2 - norme_v1*norme_v2
        p1_eucli = point1 + ((b_v2*v1_v2 - b_v1*norme_v2)/(denum))*vect1
        p2_eucli = point2 + ((b_v2*norme_v1 - b_v1*v1_v2)/(denum))*vect2
        return (p1_eucli + p2_eucli) / 2
