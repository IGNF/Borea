"""
Script test for module check_header
"""
# pylint: disable=import-error, missing-function-docstring
import pytest
from borea.utils.check.check_args_opk import check_args_opk, check_header_file, get_type_z_and_header


def test_check_args_opk():
    args = {"interval": [2, None],
            "header": list("NXYZOPKC"),
            "unit_angle": "degree",
            "linear_alteration": True}
    args, header, type_z = check_args_opk(args)
    assert args["interval"] == [1, None]
    assert header == ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    assert type_z == "altitude"


def test_check_header_file_goodz():
    header = ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    head, type_z = check_header_file(header)
    assert head == ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    assert type_z == "altitude"


def test_check_header_file_goodh():
    header = ['N', 'X', 'Y', 'H', 'O', 'P', 'K', 'C']
    head, type_z = check_header_file(header)
    assert head == ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    assert type_z == "height"


def test_check_header_file_goods():
    header = ['S', 'N', 'X', 'Y', 'Z', 'S', 'O', 'P', 'K', 'S', 'C']
    head, type_z = check_header_file(header)
    assert head == ['S', 'N', 'X', 'Y', 'Z', 'S', 'O', 'P', 'K', 'S', 'C']
    assert type_z == "altitude"


def test_check_header_file_missinfo():
    header = ['X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    with pytest.raises(ValueError):
        check_header_file(header)


def test_check_header_file_addinfo():
    header = ['N', 'N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    with pytest.raises(ValueError):
        check_header_file(header)


def test_check_header_file_addinfozh():
    header = ['N', 'X', 'Y', 'Z', 'H', 'O', 'P', 'K', 'C']
    with pytest.raises(ValueError):
        check_header_file(header)


def test_check_header_file_badinfolettre():
    header = ['N', 'X', 'Y', 'Z', 'A', 'O', 'P', 'K', 'C']
    with pytest.raises(ValueError):
        check_header_file(header)


def test_check_header_file_misszorh():
    header = ['N', 'X', 'Y', 'O', 'P', 'K', 'C']
    with pytest.raises(ValueError):
        check_header_file(header)


def test_get_type_z_and_header_z():
    header, type_z = get_type_z_and_header(["A", "Z", "B"])
    assert header == ["A", "Z", "B"]
    assert type_z == "altitude"


def test_get_type_z_and_header_h():
    header, type_z = get_type_z_and_header(["A", "L", "H", "G"])
    assert header == ["A", "L", "Z", "G"]
    assert type_z == "height"
