from dataclasses import dataclass, field
from itertools import chain
import logging
from typing import Iterator, Optional

from lcp.src.location import Size, Position
from lcp.src.container import FreeSpace


@dataclass
class DBLF:
    side: list[FreeSpace] = field(default_factory=list)
    top: list[FreeSpace] = field(default_factory=list)
    front: list[FreeSpace] = field(default_factory=list)
    MAX_DEPTH_ALLOWED: int = field(default=500, repr=False)

    def __iter__(self) -> Iterator[FreeSpace]:
        return chain(self.side, self.top, self.front)

    def __getitem__(self, index: int) -> FreeSpace:
        if index < len(self.side):
            return self.side[index]
        index -= len(self.side)
        if index < len(self.top):
            return self.top[index]
        index -= len(self.top)
        if index < len(self.front):
            return self.front[index]
        raise IndexError("Index out of range")

    def first_available(self, box_size: Size) -> Optional[FreeSpace]:
        for space in self:
            if space.size >= box_size:
                return space
        return None

    def remove(self, space: FreeSpace):
        if space in self.side:
            self.side.remove(space)
        elif space in self.top:
            self.top.remove(space)
        elif space in self.front:
            self.front.remove(space)

    def __iadd__(self, other: 'DBLF') -> 'DBLF':
        self.side.extend(other.side)
        self.top.extend(other.top)
        self.front.extend(other.front)
        # logging.debug("added new spaces")

        # logging.debug("side_%d: %s" %
        #              (len(self.side), (", ".join(["[%s]" % s for s in self.side]))))
        # logging.debug("top_%d: %s" %
        #              (len(self.top), ", ".join(["[%s]" % s for s in self.top])))
        # logging.debug("front_%d: %s" %
        #              (len(self.front), ", ".join(["[%s]" % s for s in self.front])))

        return self

    def remove_unreachable(self, min_pos: Position, max_pos: Position) -> 'DBLF':
        # logging.debug("Removiendo espacios no accesibles min %s max %s" %
        #              (min_pos, max_pos))
        changed = False
        for i in reversed(range(len(self.side))):
            space = self.side[i]
            if space.position.x < min_pos.x and \
                    (space.position.y < max_pos.y or
                        space.position.y < min_pos.y):
                # if (space.position.y < min_pos.y):
                # logging.debug("Caso raro: evaluar")
                # logging.debug("Modificar espacio side no accesible %s" % space)
                space.size.width -= max_pos.y - space.position.y
                space.position.y = max_pos.y
                if space.size.width <= 0:
                    del self.side[i]
                changed = True

        for i in reversed(range(len(self.top))):
            space = self.top[i]
            if space.position.x < min_pos.x and \
                    (space.position.z < max_pos.z or
                        space.position.z < min_pos.z):
                # if (space.position.z < min_pos.z):
                # logging.debug("Caso raro: evaluar")
                # logging.debug("Modificar espacio top no accesible %s" % space)
                space.size.height -= max_pos.z - space.position.z
                if space.size.height <= 0:
                    del self.top[i]
                changed = True

        for i in reversed(range(len(self.front))):
            space = self.front[i]
            if space.position.x < min_pos.x:
                # logging.debug(
                #    "Modificar espacio front no accesible %s" % space)
                del self.front[i]
                changed = True

        if changed:
            self.compact()

        # Cortar espacios profundos
        for i in reversed(range(len(self))):
            space = self[i]
            if space.position.x + space.size.length == max_pos.x and \
                    space.size.length > self.MAX_DEPTH_ALLOWED:
                # logging.debug("Acortando espacio muy profundo %s" % space)
                space.position.x += space.size.length - self.MAX_DEPTH_ALLOWED
                space.size.length = self.MAX_DEPTH_ALLOWED
            elif space.position.x + space.size.length < max_pos.x:
                # logging.debug("Eliminando espacio muy profundo %s" % space)
                self.remove(space)

        return self

    def compact(self) -> 'DBLF':
        # Unir los espacios de los lados si son contiguos y dimensiones similares
        for i in range(len(self)-1, 0, -1):
            side_next = self[i]
            for j in range(i-1, -1, -1):
                side_prev = self[j]
                if side_prev.position.x == side_next.position.x and \
                        side_prev.position.y == side_next.position.y and \
                        side_prev.size.length == side_next.size.length and \
                        side_prev.size.width == side_next.size.width:
                    side_prev.size.height += side_next.size.height
                    # logging.debug("Eliminando side vertical %s" % side_next)
                    self.remove(side_next)
                    break
                elif side_prev.position.y == side_next.position.y and \
                        side_prev.position.z == side_next.position.z and \
                        side_prev.size.width == side_next.size.width and \
                        side_prev.size.height == side_next.size.height:
                    side_prev.size.length += side_next.size.length
                    # logging.debug("Eliminando side horizontal %s" % side_next)
                    self.remove(side_next)
                    break
                elif side_prev.position.x == side_next.position.x and \
                        side_prev.position.z == side_next.position.z and \
                        side_prev.size.length == side_next.size.length and \
                        side_prev.size.height == side_next.size.height:
                    side_prev.size.width += side_next.size.width
                    # logging.debug("Eliminando top horizontal %s" % side_next)
                    self.remove(side_next)
                    break
                elif side_prev.position.y == side_next.position.y and \
                        side_prev.position.z == side_next.position.z and \
                        side_prev.size.width == side_next.size.width and \
                        side_prev.size.height == side_next.size.height:
                    side_prev.size.length += side_next.size.length
                    # logging.debug("Eliminando top vertical %s" % side_next)
                    self.remove(side_next)
                    break
                elif side_prev.position.y == side_next.position.y and \
                        side_prev.position.z == side_next.position.z and \
                        side_prev.size.width == side_next.size.width and \
                        side_prev.size.height == side_next.size.height:
                    side_prev.size.length += side_next.size.length
                    # logging.debug("Eliminando front horizontal %s" % side_next)
                    self.remove(side_next)
                    break
                elif side_prev.position.x == side_next.position.x and \
                        side_prev.position.z == side_next.position.z and \
                        side_prev.size.length == side_next.size.length and \
                        side_prev.size.height == side_next.size.height:
                    side_prev.size.width += side_next.size.width
                    # logging.debug("Eliminando front vertical %s" % side_next)
                    self.remove(side_next)
                    break

        # if len(self.top) > 1:
        #     for i in range(len(self.top)-1, 0, -1):
        #         top_prev = self.top[i-1]
        #         top_next = self.top[i]
        #         if top_prev.position.x == top_next.position.x and \
        #                 top_prev.position.z == top_next.position.z and \
        #                 top_prev.size.length == top_next.size.length and \
        #                 top_prev.size.height == top_next.size.height:
        #             top_prev.size.width += top_next.size.width
        #             #logging.debug("Eliminando top horizontal %s" % self.top[i])
        #             del self.top[i]
        #         elif top_prev.position.y == top_next.position.y and \
        #                 top_prev.position.z == top_next.position.z and \
        #                 top_prev.size.width == top_next.size.width and \
        #                 top_prev.size.height == top_next.size.height:
        #             top_prev.size.length += top_next.size.length
        #             #logging.debug("Eliminando top vertical %s" % self.top[i])
        #             del self.top[i]

        # if len(self.front) > 1:
        #     for i in range(len(self.front)-1, 0, -1):
        #         front_prev = self.front[i-1]
        #         front_next = self.front[i]
        #         if front_prev.position.y == front_next.position.y and \
        #                 front_prev.position.z == front_next.position.z and \
        #                 front_prev.size.width == front_next.size.width and \
        #                 front_prev.size.height == front_next.size.height:
        #             front_prev.size.length += front_next.size.length
        #             #logging.debug("Eliminando front horizontal %s" % self.front[i])
        #             del self.front[i]
        #         elif front_prev.position.x == front_next.position.x and \
        #                 front_prev.position.z == front_next.position.z and \
        #                 front_prev.size.length == front_next.size.length and \
        #                 front_prev.size.height == front_next.size.height:
        #             front_prev.size.width += front_next.size.width
        #             #logging.debug("Eliminando front vertical %s" % self.front[i])
        #             del self.front[i]
        return self

    def __len__(self):
        return len(self.side) + len(self.top) + len(self.front)
