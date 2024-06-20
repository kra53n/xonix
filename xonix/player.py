import enum

import pyxel as px

import action
import config
from tail import Tail


class PlayerMoveStatus(enum.Enum):
    Stop = enum.auto()
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()


class Player:
    def __init__(
        self,
        x: int,
        y: int,
        col: int = config.PLAYER_COL,
        tail_col: int = config.TAIL_COL,
    ):
        self.x = x
        self.y = y
        self._offset = config.BLOCK_SIZE
        self.size = config.BLOCK_SIZE
        self._col = col

        self.move_status = PlayerMoveStatus.Stop
        self.prev_on_field: int = None
        self.on_field: int = None

        self.tail = Tail(tail_col)

    @property
    def is_stepped_on_tail(self) -> bool:
        return (self.x, self.y) in self.tail

    def is_stepped_on_other_tail(self, tail: Tail) -> bool:
        return (self.x, self.y) in tail

    def set_tail(self, tail: Tail):
        self.tail = tail

    def up(self):
        self.tail.append((self.x, self.y))
        self.y -= self._offset

    def down(self):
        self.tail.append((self.x, self.y))
        self.y += self._offset

    def left(self):
        self.tail.append((self.x, self.y))
        self.x -= self._offset

    def right(self):
        self.tail.append((self.x, self.y))
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

        self.tail.update()

    def draw(self):
        self.tail.draw()
        self.draw_only_player()

    def draw_only_player(self):
        px.rect(self.x, self.y, self.size, self.size, self._col)

    def draw_tail(self):
        self.tail.draw()
