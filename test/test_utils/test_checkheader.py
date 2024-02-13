"""
Script test for module check_header
"""
import pytest
from src.utils.check_header import check_header_file


def test_check_header_file_good():
    header = ['N','X','Y','Zal','Od','Pd','Kd','C']
    head, type_z, type_angle = check_header_file(header)
    assert head ==  ['N','X','Y','Z','O','P','K','C']
    assert type_z == 'al'
    assert type_angle == 'd'


def test_check_header_file_goodS():
    header = ['S','N','X','Y','Zh','S','Od','Pd','Kd','S','C']
    head, type_z, type_angle = check_header_file(header)
    assert head ==  ['S','N','X','Y','Z','S','O','P','K','S','C']
    assert type_z == 'h'
    assert type_angle == 'd'


def test_check_header_file_missinfo():
    header = ['X','Y','Zal','Od','Pd','Kd','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_addinfo():
    header = ['N','N','X','Y','Zal','Od','Pd','Kd','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_missinfotypez():
    header = ['N','X','Y','Z','Od','Pd','Kd','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_missinfotypeangleone():
    header = ['N','X','Y','Zal','O','Pd','Kd','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_missinfotypeangleall():
    header = ['N','X','Y','Zal','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_badinfotypeangleall():
    header = ['N','X','Y','Zal','Or','Pd','Kd','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_badinfo():
    header = ['Name','Xcoor','Ycoor','Za','Od','Pd','Kd','Camera']
    head, type_z, type_angle = check_header_file(header)
    assert head ==  ['N','X','Y','Z','O','P','K','C']
    assert type_z == 'a'
    assert type_angle == 'd'


def test_check_header_file_badinfo2():
    header = ['Salamie','Nime','Xylophone','Yeux','Zebre','Orange','Plasma','K-way','Classe']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)


def test_check_header_file_badinfolettre():
    header = ['N','X','Y','Z','A','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z, type_angle = check_header_file(header)

