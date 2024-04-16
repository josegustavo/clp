from dataclasses import dataclass, field
import random

from lcp.src.container import BoxType
from lcp.src.location import Size


@dataclass
class Gene:
    """
    Represents a gene in a genetic algorithm.

    Attributes:
        type (BoxType): The type of the gene.
        box_count (int): The number of boxes of this gene.
        rotation (int): The type of rotation of the box type.
        size (Size): The size of the gene after rotation if any.
    """
    type: BoxType
    box_count: int
    rotation: int
    size: Size = field(init=False, repr=False)

    def __str__(self) -> str:
        return f"Gene of type {self.type} with {self.box_count} boxes and rotation {self.rotation}"

    def __post_init__(self):
        """
        Initializes the size attribute based on the rotation and type of the gene.
        """
        if self.rotation == 0:
            self.size = Size(self.type.length,
                             self.type.width, self.type.height)
        else:
            self.size = Size(self.type.width,
                             self.type.length, self.type.height)

    def __copy__(self) -> 'Gene':
        return Gene(self.type, self.box_count, self.rotation)

    def mutate_quantity(self, variation: float = 0.1) -> 'Gene':
        """
        Mutates the box count of the gene by a random percentage.

        Args:
            variation (float): The percentage by which to mutate the box count (default: 0.1).

        Returns:
            Gene: The mutated gene.
        """
        new_box_count = int(
            self.box_count * (1 + random.uniform(-variation, variation)))
        # Ensure the box count is within the allowed range
        self.box_count = min(max(new_box_count, self.type.min_count),
                             self.type.max_count)
        return self

    def mutate_rotation(self) -> 'Gene':
        """
        Mutates the rotation of the gene.

        Returns:
            Gene: The mutated gene.
        """
        self.rotation = 1 - self.rotation
        self.size.length, self.size.width = self.size.width, self.size.length
        return self
