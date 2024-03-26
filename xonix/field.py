import pyxel as px

from player import Player, PlayerMoveStatus


class Field:
    def __init__(self, player: Player):
        self._x = 0
        self._y = 0
        self._w = 20
        self._h = 20
        self._block_size = 2
        self._thickness = 3
        self._col = 3

        self._field = []
        self._init_field()

        self._player = player
        self._prev_player_on_field = self._player_on_field

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

    @property
    def _player_pos(self) -> (int, int):
        x = (self._player.x - self._x) // self._player.size
        y = (self._player.y - self._y) // self._player.size
        return x, y

    @property
    def _player_on_field(self) -> int:
        x, y = self._player_pos
        return self._field[y][x]

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

        if self._prev_player_on_field == 0 and self._player_on_field == 1:
            self._player.move_status = PlayerMoveStatus.Stop
        self._prev_player_on_field = self._player_on_field

    def draw(self):
        self._draw_field()

    def update(self):
        self._move_player()
