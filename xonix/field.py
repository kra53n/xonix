from collections import deque

import pyxel as px

import config
from player import Player, PlayerMoveStatus
from tail import Tail


class Field:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = config.FIELD_WDT
        self.h = config.FIELD_HGT
        self.block_size = config.BLOCK_SIZE
        self.thickness = config.BORDER_THICKNESS
        self._col = config.FIELD_COL

        self._field = []
        self._init_field()

        self._prev_player_on_field: int = None

    def _init_field(self):
        for y in range(self.h):
            self._field.append([])
            for x in range(self.w):
                v = 0
                if any((x in range(self.thickness),
                        x in (self.w - i for i in range(1, self.thickness + 1)),
                        y in range(self.thickness),
                        y in (self.h - i for i in range(1, self.thickness + 1)))):
                    v = 1
                self._field[-1].append(v)

    def obj_relative_pos(self, obj, scale: int) -> (int, int):
        x = (obj.x - self.x) // scale
        y = (obj.y - self.y) // scale
        return x, y

    def obj_on_field(self, obj, scale: int) -> int:
        x, y = self.obj_relative_pos(obj, scale)
        return self._field[y][x]

    def _get_cells_around_cell(self, x: int, y: int) -> list[tuple[int, int, int]]:
        directions = (-1, 0, 1)
        cells = []
        for dx in directions:
            for dy in directions:
                if dx == 0 and dy == 0:
                    continue
                cell_x = dx + x
                cell_y = dy + y
                if any((cell_x == -1, cell_x == self.w, cell_y == -1, cell_y == self.h)):
                       continue
                cells.append((cell_x, cell_y, (self._field[cell_y][cell_x])))
        return cells

    def _replace_field_vals(self, src: int, dst: int):
        for y in range(self.h):
            for x in range(self.w):
                v = self._field[y][x]
                if v == src:
                    self._field[y][x] = dst

    def _count_cells(self, val: int) -> int:
        num = 0
        for y in range(self.h):
            for x in range(self.w):
                v = self._field[y][x]
                if v == val:
                    num += 1
        return num
        
    def _flood_fill(self, x: int, y: int, val: int):
        s = deque()
        s.append((x, y, self._field[y][x]))
        while s:
            curr_cell = s.pop()
            x, y, c = curr_cell
            if c in (1, val):
                continue
            self._field[y][x] = val
            s.extend(self._get_cells_around_cell(x, y))

    def _fill_tail(self, tail: Tail):
        for coord in tail:
            x, y = coord
            x = (x - self.x) // tail.size
            y = (y - self.y) // tail.size
            self._field[y][x] = 1

    def _fill_left_top_part(self):
        for y in range(self.h):
            for x in range(self.w):
                v = self._field[y][x]
                if v == 0:
                    self._flood_fill(x, y, 2)
                    return

    def _fill_right_bottom_part(self):
        for y in range(self.h):
            for x in range(self.w):
                x, y = self.w-x-1, self.h-y-1
                v = self._field[y][x]
                if v == 0:
                    self._flood_fill(x, y, 3)
                    return

    def process_filling(self, tail: Tail):
        self._fill_tail(tail)
        self._fill_left_top_part()
        self._fill_right_bottom_part()
        left_top = self._count_cells(2)
        right_bottom = self._count_cells(3)
        if right_bottom == 0:
            self._replace_field_vals(2, 0)
        elif left_top < right_bottom:
            self._replace_field_vals(2, 1)
            self._replace_field_vals(3, 0)
        else:
            self._replace_field_vals(3, 1)
            self._replace_field_vals(2, 0)

    def intersect(self, x: int, y: int, scale: int) -> bool:
        _x = x // scale
        _y = y // scale
        return (0 <= x < self.w * self.block_size and
                0 <= y < self.h * self.block_size and
                self._field[_y][_x] == 1)

    def get_empty_cells_coords(self) -> tuple[tuple[int, int]]:
        return tuple((x * self.block_size + self.x, y * self.block_size + self.y)
                     for x in range(self.w)
                     for y in range(self.h)
                     if self._field[y][x] == 0)

    @property
    def fullness(self) -> float:
        return sum(1 for x in range(self.w) for y in range(self.h) if self._field[y][x]) / self.w / self.h

    def draw(self):
        for i, y in enumerate(self._field):
            for j, x in enumerate(y):
                if x == 0:
                    continue
                px.rect(self.x + j * self.block_size,
                        self.y + i * self.block_size,
                        self.block_size,
                        self.block_size,
                        self._col)
