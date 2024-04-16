from dataclasses import dataclass


@dataclass
class Position:
    """Representa la posición de un objeto en un espacio"""
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y}, z={self.z})"

    def __iter__(self):
        return iter([self.x, self.y, self.z])
