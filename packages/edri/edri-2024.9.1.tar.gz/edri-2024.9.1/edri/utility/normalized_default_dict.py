from typing import TypeVar, Optional, Callable
from collections import defaultdict

K = TypeVar('K', bound=str)
V = TypeVar('V')


class NormalizedDefaultDict(defaultdict[K, V]):
    def __init__(
            self,
            default_factory: Optional[Callable[[], V]] = None,
            /,
            *args,
            normalization: Optional[Callable[[K], str]] = None,
            **kwargs
    ) -> None:
        self._normalization = normalization or self._default_normalization

        if args and isinstance(args[0], dict):
            normalized_dict = {self._normalization(k): v for k, v in args[0].items()}
            args = (normalized_dict, *args[1:])
        super().__init__(default_factory, *args, **kwargs)

    def __setitem__(self, key: K, value: V) -> None:
        key = self._normalization(key)
        super().__setitem__(key, value)

    def __getitem__(self, key: K) -> V:
        key = self._normalization(key)
        return super().__getitem__(key)

    @staticmethod
    def _default_normalization(key: K) -> str:
        return key.lower()

    def update(self, *args, **kwargs) -> None:
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
