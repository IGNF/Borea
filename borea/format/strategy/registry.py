"""
Registry class to converte format
"""
from borea.format.strategy.interface import FileReader, FileWriter


class FormatRegistry:
    def __init__(self):
        self._readers: dict[str, FileReader] = {}
        self._writers: dict[str, FileWriter] = {}

    def register_reader(self, format_name: str, reader: FileReader) -> None:
        self._readers[format_name] = reader

    def register_writer(self, format_name: str, writer: FileWriter) -> None:
        self._writers[format_name] = writer

    def get_reader(self, format_name: str) -> FileReader:
        if format_name not in self._readers:
            raise ValueError(f"Format d'entrée non supporté : {format_name}")
        return self._readers[format_name]

    def get_writer(self, format_name: str) -> FileWriter:
        if format_name not in self._writers:
            raise ValueError(f"Format de sortie non supporté : {format_name}")
        return self._writers[format_name]

    def supported_inputs(self) -> list[str]:
        return list(self._readers.keys())

    def supported_outputs(self) -> list[str]:
        return list(self._writers.keys())
