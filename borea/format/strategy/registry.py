"""
Registry class to converte format
"""
from borea.format.strategy.interface import FileReader, FileWriter


class FormatRegistry:
    """
    Format Registry of reader and writer orientation file
    """
    def __init__(self):
        self._readers: dict[str, FileReader] = {}
        self._writers: dict[str, FileWriter] = {}

    def register_reader(self, format_name: str, reader: FileReader) -> None:
        """
        Add a reader of the registry

        Args:
            format_name (str): Format name
            reader (FileReader): class of reader
        """
        self._readers[format_name] = reader

    def register_writer(self, format_name: str, writer: FileWriter) -> None:
        """
        Add a writer of the registry

        Args:
            format_name (str): Format name
            writer (FileWriter): class of writer
        """
        self._writers[format_name] = writer

    def get_reader(self, format_name: str) -> FileReader:
        """
        Get reader by her name

        Args:
            format_name (srt): Format name

        Returns:
            Class FileReader
        """
        if format_name not in self._readers:
            raise ValueError(f"Format d'entrée non supporté : {format_name}")
        return self._readers[format_name]

    def get_writer(self, format_name: str) -> FileWriter:
        """
        Get writer by her name

        Args:
            format_name (srt): Format name

        Returns:
            Class FileWriter
        """
        if format_name not in self._writers:
            raise ValueError(f"Format de sortie non supporté : {format_name}")
        return self._writers[format_name]

    def supported_inputs(self) -> list[str]:
        """
        Get all name of reader supported

        Returns:
            List of reader's name
        """
        return list(self._readers.keys())

    def supported_outputs(self) -> list[str]:
        """
        Get all name of writer supported

        Returns:
            List of writer's name
        """
        return list(self._writers.keys())
