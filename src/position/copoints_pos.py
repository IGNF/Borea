"""
Module for calculate copoints position
"""
import numpy as np
from src.datastruct.worksite import Worksite


def copoints_position(work: Worksite) -> None:
    """
    Calculates the field position of connection points using the least squares.

    Args:
        work (Worksite): The site on which you want to calculate the position of the copoints.
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

                coord_i += [np.repeat(2 * pd_mes_pnt['index_mes'].to_numpy(), 6) + np.tile([0, 0, 0, 1, 1, 1], len(c_shot))]
                coord_j += [np.repeat(3 * pd_mes_pnt['index_pnt'].to_numpy(), 6) + np.tile([0, 1, 2, 0, 1, 2], len(c_shot))]
                data += [((np.tile(np.repeat(cam.focal / vect_u[2], 2), (3, 1)).T * mat_v @ shot.mat_rot_eucli).flatten())]
                v_res[2 * pd_mes_pnt['index_mes'].to_numpy()] = pd_mes_pnt["c"].to_numpy() - c_shot
                v_res[2 * pd_mes_pnt['index_mes'].to_numpy() + 1] = pd_mes_pnt["l"].to_numpy() - l_shot




