"""
Class to manage and storage arguments
"""
from argparse import Namespace

from borea.utils.singleton.singleton import Singleton


class ArgsManager(metaclass=Singleton):
    """
    Manager of input args
    """
    def __init__(self, args: Namespace):
        self.args = args