from abc import ABC, abstractmethod


class PrefixBase(ABC):
    @staticmethod
    @property
    @abstractmethod
    def prefix() -> str:
        """Common prefix URL."""
        pass