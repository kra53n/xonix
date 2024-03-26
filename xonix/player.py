import enum

import pyxel as px

from tail import Tail


class PlayerMoveStatus(enum.Enum):
    Stop = enum.auto()
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()


class Player:
    def __init__(self, x: int, y: int, offset: int, size: int, col: int):
        assert offset % 2 == 0
        self.x = x
        self.y = y
        self._mx = 0
        self._my = 0
        self._offset = offset
        self.size = size
        self._col = col

        self.move_status = PlayerMoveStatus.Stop

        self._tail: Tail = None

    def set_tail(self, tail: Tail):
        self._tail = tail

    def up(self):
        #self._my -= self._offset
        self._tail.append((self.x, self.y))
        self.y -= self._offset

    def down(self):
        #self._my += self._offset
        self._tail.append((self.x, self.y))
        self.y += self._offset

    def left(self):
        #self._mx -= self._offset
        self._tail.append((self.x, self.y))
        self.x -= self._offset

    def right(self):
        #self._mx += self._offset
        self._tail.append((self.x, self.y))
        self.x += self._offset

    # def _smooth_x_movement(self):
    #     vx = self._mx / 2
    #     self._mx = vx
    #     if vx == 0.5:
    #         self._mx = 0
    #         vx = 1
    #     self.x += vx

    # def _smooth_y_movement(self):
    #     vy = self._my / 2
    #     self._my = vy
    #     if vy == 0.5:
    #         self._my = 0
    #         vy = 1
    #     self.y += vy

    def update(self):
        # self._smooth_x_movement()
        # self._smooth_y_movement()
        pass

    def draw(self):
        px.rect(self.x, self.y, self.size, self.size, self._col)
