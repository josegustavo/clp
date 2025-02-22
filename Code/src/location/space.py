from dataclasses import dataclass
from itertools import chain

from . import Position, Size


@dataclass
class Space:
    position: Position
    size: Size

    def __iter__(self):
        return iter(chain(self.position, self.size))

    def __str__(self) -> str:
        return f"{self.position} {self.size}"
