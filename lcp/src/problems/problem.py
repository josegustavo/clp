from typing import Container
from attr import dataclass

from lcp.src.container import Container, BoxType


@dataclass
class Problem:
    container: Container
    box_types: list[BoxType]

    def __str__(self): return f"Problem with {
        len(self.box_types)} box types and a container of size {self.container}"
