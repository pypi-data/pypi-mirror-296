from typing import Protocol


class ProgressCallback(Protocol):
    def __call__(self, bytes_done: int): ...
