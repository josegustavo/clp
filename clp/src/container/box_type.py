from dataclasses import dataclass

from clp.src.location import Size


@dataclass
class BoxType(Size):
    """Represent the type of box and its properties"""
    type: int  # Identifies the type of box
    min_count: int  # Number of minimum boxes of this type
    max_count: int  # Number of maximum boxes of this type
    value_individual: int  # Value of a single box of this type
    weight: int  # Weight of a single box of this type
