"""
Abstract Class for reader and writer
"""
from abc import ABC, abstractmethod
import argparse
from borea.worksite.worksite import Worksite


class FileReader(ABC):
    """
    Template class for Reader class
    """
    @abstractmethod
    def args(self, parser: argparse) -> argparse:
        """
        Method for retrieving the class parameters

        Args:
            parser (argparse): parser to add parameter

        Returns:
            parser with parameter to read file of the format
        """

    @abstractmethod
    def check_args(self, args: argparse.Namespace) -> None:
        """
        Method for checking the class parameters

        Args:
            args (argparse.Namespace): parameter with argument
        """

    @abstractmethod
    def read(self, args: argparse.Namespace) -> Worksite:
        """
        Method for reading the file

        Args:
            args (argparse.Namespace): parameter with argument

        Returns:
            Worsite with data of file
        """


class FileWriter(ABC):
    """
    Template class for Writer class
    """
    @abstractmethod
    def args(self, parser: argparse) -> argparse:
        """
        Method for retrieving the class parameters

        Args:
            parser (argparse): parser to add parameter

        Returns:
            parser with parameter to write file of the format
        """

    @abstractmethod
    def check_args(self, args: argparse.Namespace) -> None:
        """
        Method for checking the class parameters

        Args:
            args (argparse.Namespace): parameter with argument
        """

    @abstractmethod
    def write(self, args: argparse.Namespace, work: Worksite) -> None:
        """
        Method for writing the file

        Args:
            args (argparse.Namespace): parameter with argument
            work (Worksite): Data to write
        """
