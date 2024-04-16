from dataclasses import dataclass, field


@dataclass
class Size:
    """Representa las dimensiones de un espacio o caja"""
    length: int
    width: int
    height: int
    volume: int = field(init=False, repr=False)

    def __str__(self) -> str:
        return f"(l={self.length}, w={self.width}, h={self.height})"

    def __post_init__(self):
        self.volume = self.length * self.width * self.height

    def __iter__(self):
        return iter([self.length, self.width, self.height])

    def __ge__(self, other: 'Size'):
        if isinstance(other, Size):
            return self.volume >= other.volume and self.length >= other.length and self.width >= other.width and self.height >= other.height
        else:
            raise TypeError("Unsupported comparison between instances of 'Size' and '{}'".format(
                type(other).__name__))

    def __eq__(self, other: 'Size'):
        return self.length == other.length and self.width == other.width and self.height == other.height
