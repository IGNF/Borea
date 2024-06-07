"""
Script test for module check_head_file_pt
"""
# pylint: disable=import-error, missing-function-docstring
import pytest
from borea.utils.check.check_args_reader_pt import check_header_file


def test_head_file_pt3d():
    head = list("SPTXYZ")
    type_pt = "gcp3d"
    header, type_z = check_header_file(head, type_pt)
    assert header == head
    assert type_z == "altitude"


def test_head_file_pt2d():
    head = list("SPNXY")
    type_pt = "gcp2d"
    check_header_file(head, type_pt)


def test_head_file_ptco():
    head = list("SPNXY")
    type_pt = "co_point"
    check_header_file(head, type_pt)


def test_head_file_ptbad3d():
    head = list("SPNXY")
    type_pt = "gcp3d"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)


def test_head_file_ptbad2d():
    head = list("SPTXYZ")
    type_pt = "gcp2d"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)
    type_pt = "co_point"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)


def test_head_file_pt_doublon():
    head = list("PTXYZSX")
    type_pt = "gcp3d"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)


def test_head_file_pt_tn():
    head = list("PNXYZ")
    type_pt = "gcp3d"
    check_header_file(head, type_pt)

    head = list("PTXY")
    type_pt = "gcp2d"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)


def test_order():
    head = list("SSZSPSYSTSSXS")
    type_pt = "gcp3d"
    check_header_file(head, type_pt)


def test_head_file_pt_unknowl():
    head = list("PTXYZO")
    type_pt = "gcp3d"
    with pytest.raises(ValueError):
        check_header_file(head, type_pt)


def test_head_file_pt3dh():
    head = list("SPTXYH")
    type_pt = "gcp3d"
    header, type_z = check_header_file(head, type_pt)
    assert header == list("SPTXYZ")
    assert type_z == "height"
