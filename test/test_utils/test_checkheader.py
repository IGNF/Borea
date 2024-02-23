"""
Script test for module check_header
"""
import pytest
from src.utils.check.check_header import check_header_file, get_type_z_and_header


def test_check_header_file_goodZ():
    header = ['N','X','Y','Z','O','P','K','C']
    head, type_z = check_header_file(header)
    assert head ==  ['N','X','Y','Z','O','P','K','C']
    assert type_z == "altitude"

def test_check_header_file_goodH():
    header = ['N','X','Y','H','O','P','K','C']
    head, type_z = check_header_file(header)
    assert head ==  ['N','X','Y','Z','O','P','K','C']
    assert type_z == "height"


def test_check_header_file_goodS():
    header = ['S','N','X','Y','Z','S','O','P','K','S','C']
    head, type_z = check_header_file(header)
    assert head ==  ['S','N','X','Y','Z','S','O','P','K','S','C']
    assert type_z == "altitude"


def test_check_header_file_missinfo():
    header = ['X','Y','Z','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z = check_header_file(header)


def test_check_header_file_addinfo():
    header = ['N','N','X','Y','Z','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z = check_header_file(header)


def test_check_header_file_addinfoZH():
    header = ['N','X','Y','Z','H','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z = check_header_file(header)


def test_check_header_file_badinfolettre():
    header = ['N','X','Y','Z','A','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z = check_header_file(header)


def test_check_header_file_missZorH():
    header = ['N','X','Y','O','P','K','C']
    with pytest.raises(ValueError) as e_info:
        head, type_z = check_header_file(header)


def test_get_type_z_and_header_Z():
    header, type_z = get_type_z_and_header(["A","Z","B"])
    assert header == ["A","Z","B"]
    assert type_z == "altitude"


def test_get_type_z_and_header_H():
    header, type_z = get_type_z_and_header(["A","L","H","G"])
    assert header == ["A","L","Z","G"]
    assert type_z == "height"