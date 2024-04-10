"""
Script test for module check_head_file_pt
"""
import pytest
from src.utils.check.check_args_reader_pt import check_header_file


def test_head_file_pt3d():
    head = list("SPTXYZ")
    type = "gcp3d"
    check_header_file(head, type)


def test_head_file_pt2d():
    head = list("SPNXY")
    type = "gcp2d"
    check_header_file(head, type)


def test_head_file_ptco():
    head = list("SPNXY")
    type = "co_point"
    check_header_file(head, type)


def test_head_file_ptbad3d():
    head = list("SPNXY")
    type = "gcp3d"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)


def test_head_file_ptbad2d():
    head = list("SPTXYZ")
    type = "gcp2d"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)
    type = "co_point"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)


def test_head_file_pt_doublon():
    head = list("PTXYZSX")
    type = "gcp3d"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)


def test_head_file_pt_TN():
    head = list("PNXYZ")
    type = "gcp3d"
    check_header_file(head, type)

    head = list("PTXY")
    type = "gcp2d"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)


def test_order():
    head = list("SSZSPSYSTSSXS")
    type = "gcp3d"
    check_header_file(head, type)


def test_head_file_pt_unknowL():
    head = list("PTXYZO")
    type = "gcp3d"
    with pytest.raises(ValueError) as info_e:
        check_header_file(head, type)
