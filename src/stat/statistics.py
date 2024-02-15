"""
Module for statistics
"""
import os
import io
import numpy as np
from src.datastruct.worksite import Worksite


# pylint: disable-next=too-many-instance-attributes
class Stat:
    """
    Calculates site statistics.
    """
    def __init__(self, work: Worksite, pathoutput: str, type_point: list = None) -> None:
        """
        Definition of the class Stat.

        Args:
            work (Worksite): The worksite to be treated.
            pathoutput (str): Path to save the file.
            type_point (list): List of type point on which we make the stats.
        """
        self.work = work
        self.pathoutput = pathoutput

        if type_point is None:
            self.type_point = []
        else:
            self.type_point = type_point

        self.check_stat_wi = True
        self.res_world_image = []
        self.check_stat_iw = True
        self.res_image_world = []
        self.stat_world_image = {}
        self.stat_image_world = {}

    def main_stat_and_save(self) -> None:
        """
        Calculates and saves all site statistics.
        """
        self.main_stat_world_to_image()
        self.main_stat_image_to_world()
        self.save_stat_txt()

    def main_stat_world_to_image(self) -> None:
        """
        Calculates residual and statistics on control point for world to image function.
        """
        self.stat_world_to_image()
        if self.check_stat_wi:
            self.stat_world_image = self.stat_list(self.res_world_image)

    def main_stat_image_to_world(self) -> None:
        """
        Calculates residual and statistics on control point for image to world function.
        """
        self.stat_image_to_world()
        if self.check_stat_iw:
            self.stat_image_world = self.stat_list(self.res_image_world)

    def stat_world_to_image(self) -> None:
        """
        Calculates residual of controle point for world to image.
        residual = image's ground point - calculated image's ground point
        """
        for name_gcp, l_shot in self.work.gipoints.items():
            try:
                if self.work.gcps[name_gcp].code in self.type_point or self.type_point == []:
                    for shot in l_shot:
                        try:
                            img_coor = self.work.shots[shot].gipoints[name_gcp]
                            img_coor_calculated = self.work.shots[shot].gcps[name_gcp]
                            l_data = [[name_gcp, shot], img_coor - img_coor_calculated]
                            self.res_world_image.append(l_data)
                        except KeyError:
                            continue
            except KeyError:
                continue
        if not self.res_world_image:
            self.check_stat_wi = False

    def stat_image_to_world(self) -> None:
        """
        Calculates residual of controle point for image to world.
        residual = ground control point - calculated ground control point
        """
        for name_gcp in list(self.work.gipoints):
            try:
                if self.work.gcps[name_gcp].code in self.type_point or self.type_point == []:
                    try:
                        gcp_coor = self.work.gcps[name_gcp].coor
                        gcp_coor_calculated = self.work.gip_world[name_gcp]
                        l_data = [[name_gcp], gcp_coor - gcp_coor_calculated]
                        self.res_image_world.append(l_data)
                    except KeyError:
                        continue
            except KeyError:
                continue
        if not self.res_image_world:
            self.check_stat_iw = False

    # pylint: disable-next=too-many-locals
    def stat_list(self, data_list: list) -> dict:
        """
        Calculates statistics on residual data.
        Min, Max, Median, Mean, Var, Sigma arithmetic and absolute

        Args:
            data_list (list): List of data
        """
        dict_output = {}
        data = []
        for ld in data_list:
            data.append(ld[-1])
        data = np.array(data)
        adata = abs(data)

        list_stat1 = [np.amin, np.amax]
        name_stat1 = ["Min", "Max"]
        list_stat12 = [np.argmin, np.argmax]
        list_stat2 = [np.median, np.mean, np.var, np.std]
        name_stat2 = ["Median", "Mean", "Var", "Sigma"]

        for func, name, argfunc in zip(list_stat1, name_stat1, list_stat12):
            stat = func(data, axis=0)
            abstat = func(adata, axis=0)
            argstat = argfunc(data, axis=0)
            absagrstat = argfunc(adata, axis=0)
            pstat = []
            abspstat = []
            for i, j in zip(argstat, absagrstat):
                if len(data_list[i][0]) == 1:
                    pstat.append(data_list[i][0][0])
                    abspstat.append(data_list[j][0][0])
                else:
                    pstat.append(data_list[i][0])
                    abspstat.append(data_list[j][0])
            dict_output[f"{name}_arith"] = {"val": stat, "data": pstat}
            dict_output[f"{name}_abs"] = {"val": abstat, "data": abspstat}

        for func, name in zip(list_stat2, name_stat2):
            dict_output[f"{name}_arith"] = np.round(func(data, axis=0), 2)
            dict_output[f"{name}_abs"] = np.round(func(adata, axis=0), 2)

        return dict_output

    def save_stat_txt(self) -> None:
        """
        Save calculation statistics in a .txt file
        """
        path_txt = os.path.join(self.pathoutput, f"Stat_{self.work.name}.txt")

        try:
            with open(path_txt, "w", encoding="utf-8") as file:
                file.write("Control point statistics file.\n")
                file.write("\n")
                file.write("\n")
                if self.res_image_world:
                    file.write("Residue of control points from image to terrain function.\n")
                    file.write("residual = ground control point - calculated ground control point")
                    file.write("\n")
                    file.write("name_point  res_x  res_y  res_z\n")
                    for data in self.res_image_world:
                        file.write(f"{data[0][0]}  {data[1][0]}  {data[1][1]}  {data[1][2]}\n")

                    if self.stat_image_world:
                        file.write("\nStatistics on residual function image to world.\n")
                        file.write("Name_stat: [stat_X, stat_Y, stat_Z]\n")
                        self.write_stat(file, self.stat_image_world)

                    file.write("\n")
                    file.write("\n")
                if self.res_world_image:
                    file.write("Residual control points from terrain to image function.\n")
                    file.write("residual = image's ground point - calculated image's ground point")
                    file.write("\n")
                    file.write("name_point  name_shot  res_column  res_line\n")
                    for data in self.res_world_image:
                        file.write(f"{data[0][0]}  {data[0][1]}  {data[1][0]}  {data[1][1]}\n")

                    if self.stat_world_image:
                        file.write("\nStatistics on residual function world to image.\n")
                        file.write("Name_stat: [stat_column, stat_line]\n")
                        self.write_stat(file, self.stat_world_image)

                file.close()
        except FileNotFoundError as e:
            raise ValueError("The path doesn't exist !!!") from e

    def write_stat(self, file: io.TextIOWrapper, data: dict) -> None:
        """
        Write dictionary data statistics of the stat_list function on a file.

        Args:
            file (io.TextIOWrapper): File to write on.
            data (dict): Dictionary on data statistics to stat_list.
        """
        file.write(f"Minimum_arithmetic: {data['Min_arith']['val']}\n")
        file.write(f"Associated_point: {data['Min_arith']['data']}\n")
        file.write(f"Minimum_absolute: {data['Min_abs']['val']}\n")
        file.write(f"Associated_point: {data['Min_abs']['data']}\n")
        file.write(f"Maximum_arithmetic: {data['Max_arith']['val']}\n")
        file.write(f"Associated_point: {data['Max_arith']['data']}\n")
        file.write(f"Maximum_absolute: {data['Max_abs']['val']}\n")
        file.write(f"Associated_point: {data['Max_abs']['data']}\n")
        file.write(f"Median_arithmetic: {data['Median_arith']}\n")
        file.write(f"Median_absolute: {data['Median_abs']}\n")
        file.write(f"Mean_arithmetic: {data['Mean_arith']}\n")
        file.write(f"Mean_absolute: {data['Mean_abs']}\n")
        file.write(f"Variance_arithmetic: {data['Var_arith']}\n")
        file.write(f"Variance_absolute: {data['Var_abs']}\n")
        file.write(f"Sigma_arithmetic: {data['Sigma_arith']}\n")
        file.write(f"Sigma_absolute: {data['Sigma_abs']}\n")
