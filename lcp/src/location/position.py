from dataclasses import dataclass


@dataclass
class Position:
    """Representa la posición de un objeto en un espacio"""
    x: int
    y: int
    z: int

    def __post_init__(self):
        if self.x < 0:
            raise ValueError("El valor de 'x' debe ser positivo")
        if self.y < 0:
            raise ValueError("El valor de 'y' debe ser positivo")
        if self.z < 0:
            raise ValueError("El valor de 'z' debe ser positivo")

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y}, z={self.z})"

    def __iter__(self):
        return iter([self.x, self.y, self.z])
