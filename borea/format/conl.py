"""
Class to write shot in conical IGN format
"""
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np
from borea.datastruct.camera import Camera
from borea.datastruct.shot import Shot
from borea.utils.xml.xml import format_xml, indent, add_elem

B_TIME = ["year", "month", "day", "hour", "minute", "second", "time_system"]
B_PT3D = ["x", "y", "z"]
B_ORI = ["easting", "northing", "altitude"]
B_TCAM = ["width", "height"]
B_CAM = ["c", "l", "focale"]


@dataclass
class Conl:
    """
    Class for light conical shot.
    File reading by software Geoview IGN on MacOs.

    Args:
        shot (Shot): Shot to convert in conical file.
        cam (Camera): Camera of the shot.
        proj (str): Projection of the shot for GEOVIEW.
    """
    shot: Shot
    cam: Camera
    proj: str

    def save_conl(self, path_conical: Path, linalt: bool = True) -> None:
        """
        Save the shot as light conical file.

        Args:
            path_conical (Path): path to the light conical file.
            linalt (bool): If you want z shot corrected by linear alteration.
        """
        date_now = datetime.now()

        # Scale factor correction
        self.shot.set_linear_alteration(linalt)

        # creation XML
        ori = ET.Element("orientation", {})
        ET.SubElement(ori, "lastmodificationbylibori",
                      {'date': date_now.strftime("%Y-%m-%d"),
                       "time": date_now.strftime("%H h %M min %S sec")})
        ET.SubElement(ori, "version").text = format_xml("1.0")

        auxiliary_data = ET.SubElement(ori, "auxiliarydata")
        ET.SubElement(auxiliary_data, "image_name").text = format_xml(self.shot.name_shot)

        image_date = ET.SubElement(auxiliary_data, "image_date")
        add_elem(image_date, B_TIME, [0, 0, 0, 0, 0, 0, None])

        ET.SubElement(auxiliary_data, "samples")

        self.set_geometry_xml(ori)

        tree = ET.ElementTree(ori)
        indent(ori)
        tree.write(path_conical, encoding='utf-8', xml_declaration=True)

    def set_geometry_xml(self, ori: ET) -> None:
        """
        Setup balise geometry of xml.

        Args:
            ori (ET): The xml.
        """
        pos_shot = np.round(np.copy(self.shot.pos_shot), 5)

        geometry = ET.SubElement(ori, "geometry", {'type': "physique"})

        extrinseque = ET.SubElement(geometry, "extrinseque")

        systeme = ET.SubElement(extrinseque, "systeme")

        euclidien = ET.SubElement(systeme, "euclidien", {'type': "MATISRTL"})
        add_elem(euclidien, B_PT3D[:2], pos_shot[:2])

        ET.SubElement(systeme, "geodesique").text = format_xml(self.proj).upper()

        ET.SubElement(extrinseque, "grid_alti").text = format_xml("UNKNOWN")

        sommet = ET.SubElement(extrinseque, "sommet")
        add_elem(sommet, B_ORI, [0, 0, pos_shot[2]])

        rotation = ET.SubElement(extrinseque, "rotation")
        ET.SubElement(rotation, "Image2Ground").text = format_xml('false')

        mat3d = ET.SubElement(rotation, "mat3d")

        l1_pt3d = ET.SubElement(ET.SubElement(mat3d, "l1"), "pt3d")
        add_elem(l1_pt3d, B_PT3D, [self.shot.mat_rot[0][0],
                                   self.shot.mat_rot[0][1],
                                   self.shot.mat_rot[0][2]], ".16f")

        l2_pt3d = ET.SubElement(ET.SubElement(mat3d, "l2"), "pt3d")
        add_elem(l2_pt3d, B_PT3D, [self.shot.mat_rot[1][0],
                                   self.shot.mat_rot[1][1],
                                   self.shot.mat_rot[1][2]], ".16f")

        l3_pt3d = ET.SubElement(ET.SubElement(mat3d, "l3"), "pt3d")
        add_elem(l3_pt3d, B_PT3D, [self.shot.mat_rot[2][0],
                                   self.shot.mat_rot[2][1],
                                   self.shot.mat_rot[2][2]], ".16f")

        self.set_camera_xml(geometry)

    def set_camera_xml(self, geometry: ET) -> None:
        """
        Setup balise camera of xml.

        Args:
            geometry (ET): The xml.
        """
        intrinseque = ET.SubElement(geometry, "intrinseque")

        sensor = ET.SubElement(intrinseque, "sensor")
        ET.SubElement(sensor, "name").text = self.cam.name_camera

        calibration_date = ET.SubElement(sensor, "calibration_date")
        add_elem(calibration_date, B_TIME, [0, 0, 0, 0, 0, 0, None])

        ET.SubElement(sensor, "serial_number").text = format_xml("UNKNOWN")

        image_size = ET.SubElement(sensor, "image_size")
        add_elem(image_size, B_TCAM, [self.cam.width, self.cam.height])

        sensor_size = ET.SubElement(sensor, "sensor_size")
        add_elem(sensor_size, B_TCAM, [self.cam.width, self.cam.height])

        ppa = ET.SubElement(sensor, "ppa")
        add_elem(ppa, B_CAM, [int(self.cam.ppax), int(self.cam.ppay), int(self.cam.focal)])

        ET.SubElement(sensor, "pixel_size").text = str(0.000004)
