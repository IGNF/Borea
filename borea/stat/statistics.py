"""
Module for statistics
"""
import os
import io
from pathlib import Path, PureWindowsPath
import numpy as np
from borea.worksite.worksite import Worksite


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
        self.pathoutput = Path(PureWindowsPath(pathoutput))

        if type_point is None:
            self.type_point = []
        else:
            self.type_point = type_point

        self.res_world_image = []
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
        if self.res_world_image:
            self.stat_world_image = self.stat_list(self.res_world_image)

    def main_stat_image_to_world(self) -> None:
        """
        Calculates residual and statistics on control point for image to world function.
        """
        self.stat_image_to_world()
        if self.res_image_world:
            self.stat_image_world = self.stat_list(self.res_image_world)

    def stat_world_to_image(self) -> None:
        """
        Calculates residual of controle point for world to image.
        residual = image's ground point - calculated image's ground point
        """
        for name_gcp, l_shot in self.work.gcp2d.items():
            try:
                if self.work.gcp3d[name_gcp].code in self.type_point or self.type_point == []:
                    for shot in l_shot:
                        try:
                            img_coor = self.work.shots[shot].gcp2d[name_gcp]
                            img_coor_calculated = self.work.shots[shot].gcp3d[name_gcp]
                            l_data = [[name_gcp, shot], img_coor - img_coor_calculated]
                            self.res_world_image.append(l_data)
                        except KeyError:
                            continue
            except KeyError:
                continue

    def stat_image_to_world(self) -> None:
        """
        Calculates residual of controle point for image to world.
        residual = ground control point - calculated ground control point
        """
        for name_gcp in list(self.work.gcp2d):
            try:
                if self.work.gcp3d[name_gcp].code in self.type_point or self.type_point == []:
                    try:
                        gcp_coor = self.work.gcp3d[name_gcp].coor
                        gcp_coor_calculated = self.work.gcp2d_in_world[name_gcp]
                        l_data = [[name_gcp], gcp_coor - gcp_coor_calculated]
                        self.res_image_world.append(l_data)
                    except KeyError:
                        continue
            except KeyError:
                continue

    def stat_list(self, data_list: list) -> dict:
        """
        Calculates statistics on residual data.
        Min, Max, Median, Mean, Var, Sigma arithmetic and absolute.

        Args:
            data_list (list): List of data.
        """
        dict_output = {}
        data = []
        for ld in data_list:
            data.append(ld[-1])
        data = np.array(data)

        list_stat1 = [[np.amin, np.amax], ["Min", "Max"], [np.argmin, np.argmax]]
        list_stat2 = [[np.median, np.mean, np.var, np.std],
                      ["Median", "Mean", "Var", "Sigma"]]

        for func, name, argfunc in zip(list_stat1[0], list_stat1[1], list_stat1[2]):
            pstat = []
            abspstat = []
            for i, j in zip(argfunc(data, axis=0), argfunc(abs(data), axis=0)):
                if len(data_list[i][0]) == 1:
                    pstat.append(data_list[i][0][0])
                    abspstat.append(data_list[j][0][0])
                else:
                    pstat.append(data_list[i][0])
                    abspstat.append(data_list[j][0])
            dict_output[f"{name}_arith"] = {"val": func(data, axis=0), "data": pstat}
            dict_output[f"{name}_abs"] = {"val": func(abs(data), axis=0), "data": abspstat}

        for func, name in zip(list_stat2[0], list_stat2[1]):
            dict_output[f"{name}_arith"] = np.round(func(data, axis=0), 2)
            dict_output[f"{name}_abs"] = np.round(func(abs(data), axis=0), 2)

        return dict_output

    def save_stat_txt(self) -> None:
        """
        Save calculation statistics in a .txt file.
        """
        path_riw = os.path.join(self.pathoutput, f"Stat_residu_image_to_world_{self.work.name}.txt")
        path_miw = os.path.join(self.pathoutput, f"Stat_metric_image_to_world_{self.work.name}.txt")
        path_rwi = os.path.join(self.pathoutput, f"Stat_residu_world_to_image_{self.work.name}.txt")
        path_mwi = os.path.join(self.pathoutput, f"Stat_metric_world_to_image_{self.work.name}.txt")

        if self.res_image_world:
            try:
                with open(path_riw, "w", encoding="utf-8") as file_riw:
                    file_riw.write("Control point statistics file.\n")
                    file_riw.write("\n")
                    file_riw.write("\n")
                    file_riw.write("Residue of control points from image to terrain function.\n")
                    file_riw.write("residual = ground control point -"
                                   " calculated ground control point")
                    file_riw.write("\n")
                    file_riw.write("name_point  res_x  res_y  res_z\n")
                    for data in self.res_image_world:
                        file_riw.write(f"{data[0][0]}  {data[1][0]}  {data[1][1]}  {data[1][2]}\n")
                    file_riw.close()
            except FileNotFoundError as e:
                raise ValueError("The path doesn't exist !!!") from e

            with open(path_miw, "w", encoding="utf-8") as file_miw:
                file_miw.write("Control point statistics file.\n")
                file_miw.write("\n")
                file_miw.write("\n")
                file_miw.write("Statistics on residual function image to world.\n")
                file_miw.write("Name_stat: [stat_X, stat_Y, stat_Z]\n")
                self.write_stat(file_miw, self.stat_image_world)
                file_miw.close()

        if self.res_world_image:
            with open(path_rwi, "w", encoding="utf-8") as file_rwi:
                file_rwi.write("Control point statistics file.\n")
                file_rwi.write("\n")
                file_rwi.write("\n")
                file_rwi.write("Residual control points from terrain to image function.\n")
                file_rwi.write("residual = image's ground point - calculated image's ground point")
                file_rwi.write("\n")
                file_rwi.write("name_point  name_shot  res_column  res_line\n")
                for data in self.res_world_image:
                    file_rwi.write(f"{data[0][0]}  {data[0][1]}  {data[1][0]}  {data[1][1]}\n")
                file_rwi.close()

            with open(path_mwi, "w", encoding="utf-8") as file_mwi:
                file_mwi.write("Control point statistics file.\n")
                file_mwi.write("\n")
                file_mwi.write("\n")
                file_mwi.write("Statistics on residual function world to image.\n")
                file_mwi.write("Name_stat: [stat_column, stat_line]\n")
                self.write_stat(file_mwi, self.stat_world_image)
                file_mwi.close()

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
