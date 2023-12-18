import numpy as np
from PinkLady.Shot import Shot


class Worksite:
    def __init__(self, name: str) -> None:
        """
        class definition

        name : str
            name of the worksite
        shots: list
            Shots list of the worksite, list<Shot>
        """
        self.name = name
        self.shots =  []

    
    def add_shot(self, name_shot:str, pos_shot:np.array, ori_shot:np.array, name_cam:str) -> None :
        """
        Add Shot to the attribut Shots

        name_shot : str
            Name of the shot
        pos_shot : numpy.array
            array of coordinate position [X, Y, Z]
        ori_shot : numpy.array
            array of orientation of the shot [Omega, Phi, Kappa]
        name_cam : str
            name of the camera
        """
        self.shots.append(Shot(name_shot=name_shot, 
                               pos_shot=pos_shot, 
                               ori_shot=ori_shot, 
                               name_cam=name_cam))