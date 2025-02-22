from dataclasses import dataclass, field

from lcp.src.location import Size


@dataclass
class Container(Size):
    dimension: list[int] = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.dimension = [self.length, self.width, self.height]
