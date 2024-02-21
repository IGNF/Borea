"""
Module dor class singleton
"""


class Singleton(type):
    """
    Class Singletonfor dtm.
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
        Singleton._instances = {}
