from dataclasses import dataclass

from clp.src.location import Space, Size, Position


@dataclass
class Box(Space):
    type: int

    def __init__(self, position: Position, size: Size, box_type: int):
        super().__init__(position, size)
        self.type = box_type
