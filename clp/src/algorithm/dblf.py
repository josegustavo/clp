from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain
import logging
from typing import Iterator, Optional

from clp.src.location import Size, Position
from clp.src.container import FreeSpace


@dataclass
class DBLF:
    side: list[FreeSpace] = field(default_factory=list)
    top: list[FreeSpace] = field(default_factory=list)
    front: list[FreeSpace] = field(default_factory=list)
    MAX_DEPTH_ALLOWED: int = field(default=600, repr=False)
    unused: list[FreeSpace] = field(
        default_factory=list, init=False, repr=False)

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

    def first_available(self, box_size: Size, type: Optional[int]) -> Optional[FreeSpace]:
        for space in self:
            if space.size >= box_size and ((space.type is None) or (type is None) or (space.type == type)):
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
        return self

    def remove_unreachable(self, min_pos: Position, max_pos: Position, max_depth) -> 'DBLF':
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
                if space.size.width > max_pos.y - space.position.y:
                    old_space = deepcopy(space)
                    old_space.size.width = max_pos.y - space.position.y
                    self.unused.append(old_space)
                    space.size.width -= max_pos.y - space.position.y
                    space.position.y = max_pos.y
                else:
                    self.unused.append(deepcopy(space))
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
                self.unused.append(deepcopy(space))
                del self.top[i]
                changed = True

        for i in reversed(range(len(self.front))):
            space = self.front[i]
            if space.position.x < min_pos.x:
                # logging.debug(
                #    "Modificar espacio front no accesible %s" % space)
                self.unused.append(deepcopy(space))
                del self.front[i]
                changed = True

        if changed:
            self.compact()

        # Cortar espacios profundos
        for i in reversed(range(len(self))):
            space = self[i]
            depth_times = 1
            while max_depth > 0 and (max_depth * (depth_times+1)) < self.MAX_DEPTH_ALLOWED:
                depth_times += 1
            max_depth *= depth_times
            if space.position.x + space.size.length == max_pos.x and \
                    space.size.length > max_depth:
                # logging.debug("Acortando espacio muy profundo %s" % space)
                old_space = deepcopy(space)
                old_space.size.length = space.size.length - max_depth

                # Agregar espacio no utilizado
                self.unused.append(old_space)

                # Cortar el nuevo espacio
                space.position.x += space.size.length - max_depth
                space.size.length = max_depth

            elif space.position.x + space.size.length < max_pos.x:
                # logging.debug("Eliminando espacio muy profundo %s" % space)
                self.unused.append(space)
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

        return self

    def __len__(self):
        return len(self.side) + len(self.top) + len(self.front)
