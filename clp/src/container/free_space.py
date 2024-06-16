from dataclasses import dataclass
import logging
from dataclasses import dataclass, field
from typing import Optional

from clp.src.location import Space, Size, Position


@dataclass
class FreeSpace(Space):
    group: str
    type: Optional[int] = field(default=None, repr=False)

    def split(self, size: Size, box_type: int) -> tuple[list['FreeSpace'], list['FreeSpace'], list['FreeSpace']]:
        """Divide the space into three spaces: side, front and top"""
        x, y, z, l, w, h = self
        inner_l, inner_w, inner_h = size

        if inner_l <= 0 or inner_w <= 0 or inner_h <= 0:
            logging.warning(
                "The size of the box to be inserted is invalid. It must be greater than 0")
            return [], [], []

        if inner_l > l or inner_w > w or inner_h > h:
            logging.warning(
                "The size of the box to be inserted is greater than the space")
            return [], [], []

        # side = [FreeSpace(Position(x, y + inner_w, z),
        #                  Size(inner_l, w - inner_w, inner_h))] if w - inner_w > 0 else []
        side = [FreeSpace(Position(x, y + inner_w, z),
                          Size(inner_l, w - inner_w, h), 'side', box_type)] if w - inner_w > 0 else []
        # top = [FreeSpace(Position(x, y, z + inner_h),
        #                 Size(inner_l, w, h - inner_h))] if h > inner_h else []
        top = [FreeSpace(Position(x, y, z + inner_h),
                         Size(inner_l, inner_w, h - inner_h), 'top', box_type)] if h > inner_h else []

        front = [FreeSpace(Position(x + inner_l, y, z),
                           Size(l - inner_l, w, h), 'front', box_type)] if l - inner_l > 0 else []

        return side, top, front
