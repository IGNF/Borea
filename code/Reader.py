import numpy as np

import code.Worksite as ws

def from_file(file:str, skip:int=1) ->ws:
    """
    Photogrammetric site file reading function

    file : str
        path to the worksite
    skip : int
        number of lines to be skipped before reading the file
    """
    ext = file.split(".")[-1]
    if ext == "opk":
        return from_opk(file,skip)
    else:
         print("Input file not taken into account")


def from_opk(file:str, skip:int=1) -> ws:
    """
    Reads an opk file to transform it into a Workside object

    file : str
        path of the file .opk
    skip : int
        number of lines to be skipped before reading the file
    """
    #job name retrieval
    name_work = file.split('/')[-1]
    name_work = name_work.split('.')[0]

    #Create worksite
    work = ws.Worksite(name_work)

    try:
        with open(file, 'r') as file_opk:
            for item_opk in file_opk.readlines()[skip:]:
                item_shot = item_opk.split()
                work.add_shot(item_shot[0],
                              np.array([
                                   float(item_shot[1]),
                                   float(item_shot[2]),
                                   float(item_shot[3])], dtype=float),
                              np.array([
                                   float(item_shot[4]),
                                   float(item_shot[5]),
                                   float(item_shot[6])], dtype=float),
                              item_shot[7])
    except FileNotFoundError:
            raise ValueError("The path to the .opk file is incorrect !!!")

    return work

