import numpy as np
import code.worksite as ws

def to_opk(path:str, work:ws)-> None:
    """
    Write function, to save a photogrammetric site in .opk format
    
    :param str path : Path of registration file.
    :param Worksite work : The site to be recorded.
    """
    path = path + work.name + ".opk"

    try:
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
    except FileNotFoundError:
            raise ValueError("The path doesn't exist !!!")