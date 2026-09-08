"""
Abstract Class for reader and writer
"""
from abc import ABC, abstractmethod
import argparse
from borea.worksite.worksite import Worksite


class FileReader(ABC):
    @abstractmethod
    def args(self, parser: argparse) -> argparse:
        ...

    @abstractmethod
    def check_args(self, args: argparse.Namespace) -> None:
        ...

    @abstractmethod
    def read(self, args: argparse.Namespace) -> Worksite:
        ...


class FileWriter(ABC):
    @abstractmethod
    def args(self, parser: argparse) -> argparse:
        ...

    @abstractmethod
    def check_args(self, args: argparse.Namespace) -> None:
        ...

    @abstractmethod
    def write(self, args: argparse.Namespace, work: Worksite) -> None:
        ...
