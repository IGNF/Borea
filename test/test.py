import numpy as np

from Pink_Lady.code.Shot import Shot
from Pink_Lady.code.Worksite import Worksite



if __name__=="__main__":
    ws = Worksite(name = "Test")
    s = Shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    ws.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    print(s.name_cam, s.pos_shot, s.ori_shot, s.name_cam)
    print(ws.name)
    print(ws.shots[-1].name_cam)
                

