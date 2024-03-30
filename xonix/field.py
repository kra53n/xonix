import pyxel as px

from player import Player, PlayerMoveStatus
from tail import Tail


class Field:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._w = 20
        self._h = 20
        self._block_size = 2
        self._thickness = 3
        self._col = 3

        self._field = []
        self._init_field()

        self._player: Player = None
        self._prev_player_on_field: int = None
        self._tail: Tail = None

    def _init_field(self):
        for y in range(self._h):
            self._field.append([])
            for x in range(self._w):
                v = 0
                if any((x in range(self._thickness),
                        x in (self._w - i for i in range(1, self._thickness + 1)),
                        y in range(self._thickness),
                        y in (self._h - i for i in range(1, self._thickness + 1)))):
                    v = 1
                self._field[-1].append(v)

    def _draw_field(self):
        for i, y in enumerate(self._field):
            for j, x in enumerate(y):
                if x == 0:
                    continue
                px.rect(self._x + j * self._block_size,
                        self._y + i * self._block_size,
                        self._block_size,
                        self._block_size,
                        self._col)

    def set_player(self, player: Player):
        self._player = player
        self._prev_player_on_field = self._player_on_field

    @property
    def _player_pos(self) -> (int, int):
        x = (self._player.x - self._x) // self._player.size
        y = (self._player.y - self._y) // self._player.size
        return x, y

    @property
    def _player_on_field(self) -> int:
        x, y = self._player_pos
        return self._field[y][x]

    def set_tail(self, tail: Tail):
        self._tail = tail

    def _get_cells_around_cell(self, x: int, y: int) -> list[tuple[int, int, int]]:
        directions = (-1, 0, 1)
        cells = []
        for dx in directions:
            for dy in directions:
                if dx == 0 and dy == 0:
                    continue
                cell_x = dx + x
                cell_y = dy + y
                if any((cell_x == -1, cell_x == self._w, cell_y == -1, cell_y == self._h)):
                       continue
                cells.append((cell_x, cell_y, (self._field[cell_y][cell_x])))
        return cells

    def _replace_field_vals(self, src: int, dst: int):
        for y in range(self._h):
            for x in range(self._w):
                v = self._field[y][x]
                if v == src:
                    self._field[y][x] = dst

    def _count_cells(self, val: int) -> int:
        num = 0
        for y in range(self._h):
            for x in range(self._w):
                v = self._field[y][x]
                if v == val:
                    num += 1
        return num
        
    def _flood_fill(self, x: int, y: int, val: int):
        self._field[y][x] = val
        cells = self._get_cells_around_cell(x, y)
        for cell in cells:
            if cell[-1] in (1, val):
                continue
            self._flood_fill(cell[0], cell[1], val)

    def _fill_tail(self):
        for coord in self._tail:
            x, y = coord
            x = (x - self._x) // self._tail.size
            y = (y - self._y) // self._tail.size
            self._field[y][x] = 1

    def _fill_left_top_part(self):
        for y in range(self._h):
            for x in range(self._w):
                v = self._field[y][x]
                if v == 0:
                    self._flood_fill(x, y, 2)
                    return

    def _fill_right_bottom_part(self):
        for y in range(self._h):
            for x in range(self._w):
                x, y = self._w-x-1, self._h-y-1
                v = self._field[y][x]
                if v == 0:
                    self._flood_fill(x, y, 3)
                    return

    def _process_tail_filling(self):
        self._fill_tail()
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
        

    def _move_player(self):
        match self._player.move_status:
            case PlayerMoveStatus.Stop:
                pass
            case PlayerMoveStatus.Up:
                if self._player_pos[1] == self._y:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.up()
            case PlayerMoveStatus.Down:
                if self._player_pos[1] == self._h-1:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.down()
            case PlayerMoveStatus.Left:
                if self._player_pos[0] == self._x:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.left()
            case PlayerMoveStatus.Right:
                if self._player_pos[0] == self._w-1:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.right()

        if self._prev_player_on_field == 1:
            self._tail.clear()
        elif self._prev_player_on_field == 0 and self._player_on_field == 1:
            self._player.move_status = PlayerMoveStatus.Stop
            self._process_tail_filling()
            self._tail.clear()
        self._prev_player_on_field = self._player_on_field

    def draw(self):
        self._draw_field()

    def update(self):
        self._move_player()
