"""
Module for class singleton
"""


class Singleton(type):
    """
    Class Singleton for Dtm and ProjEngine.
    It's a design pattern, belonging to the category of creation patterns,
    whose aim is to restrict the instantiation of a class to a single object.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        """
        Clear instances
        """
        _ = cls._instances.pop(cls, None)
