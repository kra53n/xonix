import enum

import pyxel as px

import action
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
        self._offset = offset
        self.size = size
        self._col = col

        self.move_status = PlayerMoveStatus.Stop

        self._tail: Tail = None

    @property
    def is_stepped_on_tail(self) -> bool:
        return (self.x, self.y) in self._tail

    def set_tail(self, tail: Tail):
        self._tail = tail

    def up(self):
        self._tail.append((self.x, self.y))
        self.y -= self._offset

    def down(self):
        self._tail.append((self.x, self.y))
        self.y += self._offset

    def left(self):
        self._tail.append((self.x, self.y))
        self.x -= self._offset

    def right(self):
        self._tail.append((self.x, self.y))
        self.x += self._offset

    def update(self):
        if (action.move_player_up() and
            self.move_status != PlayerMoveStatus.Down):
            self.move_status = PlayerMoveStatus.Up

        if (action.move_player_down() and
            self.move_status != PlayerMoveStatus.Up):
            self.move_status = PlayerMoveStatus.Down

        if (action.move_player_left() and
            self.move_status != PlayerMoveStatus.Right):
            self.move_status = PlayerMoveStatus.Left

        if (action.move_player_right() and
            self.move_status != PlayerMoveStatus.Left):
            self.move_status = PlayerMoveStatus.Right

    def draw(self):
        px.rect(self.x, self.y, self.size, self.size, self._col)
