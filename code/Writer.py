import numpy as np
import code.Worksite as ws

def to_opk(path:str, work:ws)-> None:
    """
    write function, to save a photogrammetric site in .opk format

    path : str
        path of registration file
    work : ws
        The site to be recorded
    """
    path = path + work.name + ".opk"
    print(path)
    file = open(path,"w")
    file.write("NOM X   Y   Z   O   P   K   CAMERA")
    for shot in work.shots:
        file.write("\n")
        file.write( shot.name_shot + "   " + 
                    str(shot.pos_shot[0]) + "   " +
                    str(shot.pos_shot[1]) + "   " +
                    str(shot.pos_shot[2]) + "   " +
                    str(shot.ori_shot[0]) + "   " +
                    str(shot.ori_shot[1]) + "   " +
                    str(shot.ori_shot[2]) + "   " +
                    shot.name_cam)
    file.close()